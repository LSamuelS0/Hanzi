// Servidor do "Professor Virtual" do Caderno de Hanzi (Cloudflare Worker).
// Guarda a chave do Gemini longe do app, confere o login do Firebase e devolve
// a resposta do professor em JSON. Segredos/variáveis (painel do Cloudflare):
//   GEMINI_API_KEY   (segredo, obrigatório)  chave do Google AI Studio
//   FIREBASE_PROJECT (opcional) padrão "caderno-hanzi"
//   ALLOWED_ORIGINS  (opcional) padrão "https://lsamuels0.github.io"
//   GEMINI_MODEL     (opcional) padrão "gemini-2.5-flash"
//   GEMINI_FALLBACK  (opcional) padrão "gemini-2.5-flash-lite"
//   DAILY_LIMIT      (opcional) chamadas por usuário por dia, padrão 200

const DEF = {
  FIREBASE_PROJECT: "caderno-hanzi",
  ALLOWED_ORIGINS: "https://lsamuels0.github.io",
  GEMINI_MODEL: "gemini-2.5-flash",
  GEMINI_FALLBACK: "gemini-2.5-flash-lite",
  DAILY_LIMIT: "200",
};
const cfg = (env, k) => (env && env[k]) || DEF[k];
const MAX_AUDIO_B64 = 1_400_000; // ~30 s de WAV 16 kHz mono
const MAX_BODY = 1_600_000;

export default {
  async fetch(req, env) {
    const origin = req.headers.get("Origin") || "";
    const allowed = cfg(env, "ALLOWED_ORIGINS").split(",").map(s => s.trim());
    const okOrigin = allowed.includes(origin) || allowed.includes("*");
    const cors = {
      "Access-Control-Allow-Origin": okOrigin ? origin : allowed[0],
      "Access-Control-Allow-Methods": "POST, OPTIONS",
      "Access-Control-Allow-Headers": "Authorization, Content-Type",
      "Access-Control-Max-Age": "86400",
      "Vary": "Origin",
    };
    const out = (obj, status = 200) => new Response(JSON.stringify(obj), { status, headers: { ...cors, "Content-Type": "application/json; charset=utf-8", "Cache-Control": "no-store" } });
    if (req.method === "OPTIONS") return new Response(null, { status: 204, headers: cors });
    const url = new URL(req.url);
    if (req.method === "GET" && url.pathname === "/") return out({ ok: true, service: "caderno-hanzi-professor", configured: !!(env && env.GEMINI_API_KEY) });
    if (req.method !== "POST" || url.pathname !== "/chat") return out({ error: "not_found" }, 404);
    if (!okOrigin) return out({ error: "origin" }, 403);
    if (!env || !env.GEMINI_API_KEY) return out({ error: "no_key", msg: "Falta configurar GEMINI_API_KEY no Worker." }, 500);

    // 1) login
    const tok = (req.headers.get("Authorization") || "").replace(/^Bearer\s+/i, "");
    let uid;
    try { uid = await verifyFirebaseToken(tok, cfg(env, "FIREBASE_PROJECT")); }
    catch (e) { return out({ error: "auth", msg: "Entre na sua conta para conversar." }, 401); }

    // 2) limite diário (aproximado: memória do Worker)
    if (!rateOk(uid, +cfg(env, "DAILY_LIMIT"))) return out({ error: "limit", msg: "Você chegou ao limite de conversas de hoje. Volte amanhã!" }, 429);

    // 3) pedido
    const raw = await req.text();
    if (raw.length > MAX_BODY) return out({ error: "too_big" }, 413);
    let b; try { b = JSON.parse(raw); } catch (e) { return out({ error: "bad_json" }, 400); }
    if (b.audio && (typeof b.audio !== "string" || b.audio.length > MAX_AUDIO_B64)) return out({ error: "audio_too_big", msg: "Gravação longa demais (máximo 30 s)." }, 413);

    try {
      const r = await askTeacher(env, b);
      return out(r);
    } catch (e) {
      const busy = e && (e.status === 429 || e.status === 503);
      return out({ error: busy ? "busy" : "llm", msg: busy ? "O professor está ocupado (limite gratuito). Espere um minuto e tente de novo." : "Não consegui falar com o professor agora. Tente de novo." }, busy ? 503 : 502);
    }
  },
};

/* ---------------- login do Firebase (ID token RS256) ---------------- */
const JWKS_URL = "https://www.googleapis.com/service_accounts/v1/jwk/securetoken@system.gserviceaccount.com";
let JWKS = null, JWKS_AT = 0;
async function getKeys() {
  if (JWKS && Date.now() - JWKS_AT < 3600_000) return JWKS;
  const r = await fetch(JWKS_URL);
  if (!r.ok) throw new Error("jwks");
  JWKS = (await r.json()).keys; JWKS_AT = Date.now();
  return JWKS;
}
const b64urlBytes = s => Uint8Array.from(atob(s.replace(/-/g, "+").replace(/_/g, "/").padEnd(Math.ceil(s.length / 4) * 4, "=")), c => c.charCodeAt(0));
const b64urlJson = s => JSON.parse(new TextDecoder().decode(b64urlBytes(s)));
export async function verifyFirebaseToken(token, project) {
  const parts = (token || "").split(".");
  if (parts.length !== 3) throw new Error("format");
  const head = b64urlJson(parts[0]), pay = b64urlJson(parts[1]);
  if (head.alg !== "RS256" || !head.kid) throw new Error("alg");
  const now = Math.floor(Date.now() / 1000);
  if (pay.aud !== project || pay.iss !== "https://securetoken.google.com/" + project) throw new Error("aud");
  if (!(pay.exp > now - 30) || !(pay.iat <= now + 300) || !pay.sub) throw new Error("time");
  const jwk = (await getKeys()).find(k => k.kid === head.kid);
  if (!jwk) throw new Error("kid");
  const key = await crypto.subtle.importKey("jwk", jwk, { name: "RSASSA-PKCS1-v1_5", hash: "SHA-256" }, false, ["verify"]);
  const ok = await crypto.subtle.verify("RSASSA-PKCS1-v1_5", key, b64urlBytes(parts[2]), new TextEncoder().encode(parts[0] + "." + parts[1]));
  if (!ok) throw new Error("sig");
  return pay.sub;
}

const USE = new Map();
function rateOk(uid, lim) {
  const d = new Date().toISOString().slice(0, 10), k = uid + ":" + d;
  const n = (USE.get(k) || 0) + 1; USE.set(k, n);
  if (USE.size > 5000) for (const key of USE.keys()) if (!key.endsWith(d)) USE.delete(key);
  return n <= lim;
}

/* ---------------- professor (Gemini) ---------------- */
const S = (desc) => ({ type: "STRING", description: desc });
const LINE = (desc) => ({ type: "OBJECT", description: desc, properties: { zh: S("chinês em hanzi simplificado"), py: S("pinyin com marcas de tom, palavras separadas"), pt: S("tradução natural em português do Brasil") }, required: ["zh", "py", "pt"] });
const TURN_SCHEMA = {
  type: "OBJECT",
  properties: {
    heard: { type: "OBJECT", description: "o que o aluno disse, transcrito fielmente (mesmo com erros). Se ele escreveu, copie.", properties: { zh: S("hanzi (ou o texto original se não for chinês)"), py: S("pinyin"), pt: S("tradução") }, required: ["zh", "py", "pt"] },
    understood: { type: "BOOLEAN", description: "false se não deu para entender a fala" },
    correction: { type: "OBJECT", description: "só quando a frase do aluno tinha erro ou soava pouco natural, ou quando ele falou em português", properties: { zh: S("forma natural"), py: S("pinyin"), pt: S("tradução"), note: S("explicação curta e gentil em português, com pinyin entre parênteses depois de cada hanzi") }, required: ["zh", "py", "pt", "note"] },
    praise: S("elogio curto e específico em português quando a fala foi boa; vazio se não houver"),
    reply: LINE("a fala do professor neste turno: reação natural + uma pergunta ou deixa para o aluno continuar"),
    hint: LINE("começo de uma resposta possível para o aluno completar, ex.: 我叫…"),
    suggestions: { type: "ARRAY", description: "2 respostas curtas e diferentes que o aluno poderia dar", items: LINE("resposta possível") },
    new_words: { type: "ARRAY", description: "palavras da fala do professor que NÃO estão no vocabulário do aluno", items: LINE("palavra nova") },
    finished: { type: "BOOLEAN", description: "true quando o objetivo do cenário foi cumprido e a conversa pode terminar" },
  },
  required: ["heard", "understood", "reply", "hint", "suggestions", "new_words", "finished"],
};
const START_SCHEMA = { type: "OBJECT", properties: { reply: TURN_SCHEMA.properties.reply, hint: TURN_SCHEMA.properties.hint, suggestions: TURN_SCHEMA.properties.suggestions, new_words: TURN_SCHEMA.properties.new_words }, required: ["reply", "hint", "suggestions", "new_words"] };
const SUMMARY_SCHEMA = {
  type: "OBJECT",
  properties: {
    good: { type: "ARRAY", items: S("algo que o aluno fez bem, em português, curto"), description: "2 itens" },
    train: { type: "ARRAY", items: { type: "OBJECT", properties: { zh: S("hanzi"), py: S("pinyin"), pt: S("tradução"), why: S("por que treinar, em português") }, required: ["zh", "py", "pt", "why"] }, description: "1 ou 2 frases ou palavras para treinar" },
    memory: S("resumo atualizado do aluno (até 600 caracteres, em português): o que já consegue dizer, erros frequentes, assuntos de interesse"),
  },
  required: ["good", "train", "memory"],
};

function systemPrompt(b) {
  const sc = b.scenario || {};
  const disp = { full: "o aluno vê hanzi, pinyin e tradução", py: "o aluno vê hanzi e pinyin", zh: "o aluno vê só hanzi" }[b.display] || "o aluno vê hanzi, pinyin e tradução";
  const vocab = Array.isArray(b.vocab) ? b.vocab.slice(0, 600).join(" ") : "";
  return `Você é um professor de mandarim nativo e caloroso, conversando com um aluno brasileiro iniciante que trabalha na Midea (empresa chinesa) e quer conversar de verdade com colegas chineses.

PAPEL NESTA CONVERSA: ${clip(sc.role, 300)}
CENÁRIO: ${clip(sc.title, 200)}
OBJETIVO DO ALUNO: ${clip(sc.goal, 300)}
NÍVEL: ${clip(b.level, 80)} (${disp})
O QUE JÁ SABEMOS DO ALUNO: ${clip(b.memory, 700) || "nada ainda"}
VOCABULÁRIO QUE O ALUNO JÁ VIU: ${vocab}

COMO CONVERSAR
- Fale como um chinês de verdade fala no dia a dia, não como livro didático: frases curtas, partículas naturais (呢, 吧, 啊, 哦) quando couberem.
- Cada fala sua: no máximo 2 frases curtas (até ~14 hanzi no total), reagindo ao que o aluno disse e terminando com UMA pergunta ou deixa simples para ele continuar.
- Use quase só o vocabulário que o aluno já viu. Se precisar de palavra nova, no máximo 1 por turno, e liste em new_words.
- Mantenha o papel e o cenário. Puxe assuntos do cenário para o aluno praticar o objetivo.

COMO CORRIGIR (muito importante)
- Nunca diga "errado". Se a fala do aluno deu para entender, responda ao conteúdo normalmente e coloque em correction a forma natural, com uma nota curta e gentil.
- Se a fala estava boa, não preencha correction; escreva um elogio específico em praise.
- Corrija no máximo 1 ponto por turno, o mais importante para ser entendido.
- Se o aluno falar em português, responda em chinês simples e coloque em correction como dizer aquilo em chinês.
- Se não deu para entender (áudio ruim ou palavras soltas sem sentido), understood=false e peça com carinho para repetir, em chinês simples (ex.: 不好意思，请再说一遍。).
- Não julgue tons nem pronúncia fina: isso é treinado em outra parte do app.

FORMATO
- Hanzi simplificado. Pinyin com marcas de tom, separado por palavra, com pontuação.
- Português do Brasil natural. Em textos em português, todo hanzi deve vir seguido do pinyin entre parênteses, ex.: 叫 (jiào).
- hint é o começo de uma resposta que o aluno completa. suggestions são 2 respostas curtas diferentes, usando o vocabulário dele.`;
}
const clip = (s, n) => (typeof s === "string" ? s.slice(0, n) : "");

function historyParts(b) {
  const h = Array.isArray(b.history) ? b.history.slice(-16) : [];
  return h.map(m => ({ role: m.r === "s" ? "user" : "model", parts: [{ text: clip(m.zh, 300) }] }));
}

export async function askTeacher(env, b) {
  const mode = b.mode === "start" || b.mode === "summary" ? b.mode : "turn";
  const contents = historyParts(b);
  let schema = TURN_SCHEMA;
  if (mode === "start") {
    schema = START_SCHEMA;
    contents.push({ role: "user", parts: [{ text: "(Comece a conversa agora, no seu papel, com uma saudação e uma pergunta simples.)" }] });
  } else if (mode === "summary") {
    schema = SUMMARY_SCHEMA;
    contents.push({ role: "user", parts: [{ text: "(A conversa terminou. Avalie o aluno com carinho: 2 coisas que fez bem, 1 ou 2 frases para treinar, e atualize o resumo do aluno juntando o resumo anterior com o que viu agora.)" }] });
  } else {
    const parts = [];
    if (b.audio) parts.push({ inlineData: { mimeType: "audio/wav", data: b.audio } }, { text: "(Fala do aluno no áudio acima. Transcreva em heard e responda.)" });
    else parts.push({ text: clip(b.text, 400) || "(silêncio)" });
    contents.push({ role: "user", parts });
  }
  // a API pede que a conversa comece com o usuário
  if (contents.length && contents[0].role === "model") contents.unshift({ role: "user", parts: [{ text: "(início)" }] });
  const body = {
    systemInstruction: { parts: [{ text: systemPrompt(b) }] },
    contents,
    generationConfig: { responseMimeType: "application/json", responseSchema: schema, temperature: mode === "summary" ? 0.3 : 0.8, maxOutputTokens: 1200 },
  };
  const models = [cfg(env, "GEMINI_MODEL"), cfg(env, "GEMINI_FALLBACK")];
  let lastErr;
  for (const m of models) {
    try {
      const j = await callGemini(env, m, body);
      const res = parseJson(j);
      res.model = m;
      if (mode !== "summary") res.unknown = unknownChars(res.reply && res.reply.zh, b.vocab);
      return res;
    } catch (e) { lastErr = e; if (!(e.status === 429 || e.status === 503 || e.status === 500 || e.parse)) break; }
  }
  throw lastErr;
}

async function callGemini(env, model, body) {
  const r = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/${encodeURIComponent(model)}:generateContent`, {
    method: "POST",
    headers: { "Content-Type": "application/json", "x-goog-api-key": env.GEMINI_API_KEY },
    body: JSON.stringify(body),
  });
  if (!r.ok) { const e = new Error("gemini " + r.status + " " + (await r.text()).slice(0, 300)); e.status = r.status; throw e; }
  return r.json();
}
function parseJson(j) {
  const t = j && j.candidates && j.candidates[0] && j.candidates[0].content && (j.candidates[0].content.parts || []).map(p => p.text || "").join("");
  try { return JSON.parse(t); } catch (e) { const er = new Error("parse"); er.parse = true; throw er; }
}
function unknownChars(zh, vocab) {
  if (!zh || !Array.isArray(vocab)) return [];
  const known = new Set(vocab.join(""));
  return [...new Set([...zh].filter(c => /[一-鿿]/.test(c) && !known.has(c)))];
}
