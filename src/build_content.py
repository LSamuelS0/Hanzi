# Gera ctest.json (conteúdo do app), áudios e traços a partir dos arquivos de conteúdo.
import json, re, sys, os, base64, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import addpy
from addpy import annotate2
from curriculum import G, L, NAMES_EXTRA
from modules import G2, M_LESSONS, PHASES
from grammar import GP
from stories import ST
from build_sent_audio import pieces_for, build, checkout, HSK, R

HAN = re.compile(r'[一-鿿]')
P = set("！？。，")
GG = dict(G)
for k, v in G2.items():
    if k not in GG: GG[k] = v
# ensina o anotador as palavras e frases novas
for k, v in GG.items(): addpy.WORDS.setdefault(k, v[0])
for (i, t, goal, ph) in M_LESSONS:
    for z, p, pt in ph: addpy.learn(z.replace(" ", ""), p)
miss = set()

byid = {l[0]: {"id": l[0], "t": l[2], "goal": l[3], "ph": l[4]} for l in L}
for (i, t, goal, ph) in M_LESSONS: byid[i] = {"id": i, "t": t, "goal": goal, "ph": ph}

old = json.load(open("ctest.json"))
c = {k: old[k] for k in ("vocab", "sentences", "bases", "syll")}
lessons = []; seen = set(); n = 0; mods = []
for phase, ms in PHASES:
    for name, ids in ms:
        n += 1; mods.append({"n": n, "name": name, "phase": phase, "ids": ids})
        for i in ids:
            b = byid[i]; new = []
            for z, p, pt in b["ph"]:
                for tk in z.split():
                    if tk in P: continue
                    assert tk in GG, (i, tk)
                    if tk not in seen: seen.add(tk); new.append(tk)
            d = {"id": i, "lvl": f"Módulo {n} · {name}", "mod": n, "phase": phase, "t": b["t"], "goal": b["goal"],
                 "new": new, "ph": [[z.split(), p, pt] for z, p, pt in b["ph"]]}
            if i == 16: d["extra"] = {"groups": NAMES_EXTRA["groups"], "notes": [annotate2(x, miss) for x in NAMES_EXTRA["notes"]]}
            lessons.append(d)
c["lessons"] = lessons; c["modules"] = mods
c["gloss"] = {k: [v[0], annotate2(v[1], miss), annotate2(v[2], miss)] for k, v in GG.items()}
c["gloss"]["哪里"][2] = "Também se fala 哪儿 (nǎr) no norte da China."
vm = {}
from data import VOCAB
for v in VOCAB: vm[v[0]] = v
for v in c["vocab"]:
    if v[0] in vm: v[2] = annotate2(vm[v[0]][2], miss)
c["gp"] = {str(k): [{"t": annotate2(t, miss), "f": f, "x": annotate2(x, miss), "tk": tk.split(), "p": p, "m": m} for (t, f, x, tk, p, m) in v] for k, v in GP.items()}

# leitura padrão de cada caractere (dicionário Make Me a Hanzi)
mm = {}
for line in open("dl/mmah/dictionary.txt", encoding="utf8"):
    d = json.loads(line)
    if d.get("pinyin"): mm[d["character"]] = d["pinyin"][0]
for ch, p in mm.items():
    if len(ch) == 1 and HAN.match(ch): addpy.OVR.setdefault(ch, p)
fix = {"子": "zǐ", "么": "me", "们": "men", "的": "de", "了": "le", "吗": "ma", "呢": "ne", "吧": "ba", "个": "gè"}
c["story"] = {}
for ch, s in ST.items():
    a = annotate2(s, miss).replace("子 (zi,", "子 (zǐ,").replace("宀 (gài,", "宀 (mián,")
    c["story"][ch] = a
c["cpy"] = {ch: fix.get(ch, mm.get(ch, "")) for ch in ST}
print("sem pinyin nas notas:", miss)

# ---------- áudio ----------
audio = json.load(open("audio.json"))
need = [k for k in GG if k in HSK and "w:" + k not in audio]
for k in GG:
    if k not in HSK:
        for ch in k:
            if ch in HSK and "w:" + ch not in audio and ch not in need: need.append(ch)
if need:
    checkout([f"24k-abr/hsk/cmn-{w}.mp3" for w in need])
    for w in need: audio["w:" + w] = base64.b64encode(open(f"{R}/24k-abr/hsk/cmn-{w}.mp3", "rb").read()).decode()
jobs = [("".join(tk), tk, p) for l in lessons for tk, p, pt in l["ph"]]
for l in lessons:
    for z, p, pt in [(x[0], x[1], x[2]) for x in []]: pass
for k, v in GP.items():
    for (t, f, x, tk, p, m) in v: jobs.append((tk.replace(" ", ""), tk.split(), p))
wjobs = [(k, [k], GG[k][0]) for k in GG if k not in HSK and "w:" + k not in audio]
plans = {}; files = set()
for key, tk, p in jobs + wjobs:
    if ("f:" + key in audio) and (key, tk, p) in jobs: continue
    w = pieces_for(tk, p)
    if w is None: print("sem áudio possível:", key, p); continue
    plans[key] = w; files |= {f for ws in w for f in ws}
checkout(sorted(files))
os.makedirs("sent_mp3", exist_ok=True)
for key, tk, p in jobs:
    if key in plans and "f:" + key not in audio: audio["f:" + key] = build(plans[key], f"sent_mp3/{abs(hash(key))}.mp3")
for key, tk, p in wjobs:
    if key in plans and "w:" + key not in audio: audio["w:" + key] = build(plans[key], f"sent_mp3/w{abs(hash(key))}.mp3")
json.dump(audio, open("audio.json", "w"), ensure_ascii=False, separators=(",", ":"))

# ---------- traços ----------
strokes = json.load(open("strokes.json"))
chars = sorted({ch for ch in json.dumps(c, ensure_ascii=False) if HAN.match(ch)} - set(strokes))
if chars:
    subprocess.run(["git", "-c", "core.quotepath=off", "checkout", "HEAD", "--"] + [f"data/{ch}.json" for ch in chars], cwd="dl/hwd", capture_output=True)
    for ch in chars:
        p = f"dl/hwd/data/{ch}.json"
        if os.path.exists(p): strokes[ch] = json.load(open(p))
json.dump(strokes, open("strokes.json", "w"), ensure_ascii=False, separators=(",", ":"))
json.dump(c, open("ctest.json", "w"), ensure_ascii=False)
print("lições", len(lessons), "módulos", len(mods), "glossário", len(c["gloss"]), "áudios", len(audio), "traços", len(strokes),
      "MB áudio", round(os.path.getsize("audio.json") / 1e6, 1))
