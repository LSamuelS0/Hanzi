# -*- coding: utf-8 -*-
# Formal e informal no Módulo 1.
# Cada tema tem duas lições em sequência: a formal (chefe, cliente, pessoa mais velha,
# desconhecido) e a informal (colegas próximos e amigos). O objetivo é que o aluno saiba
# falar nos dois registros e não soe "de livro" com os colegas chineses.

# registro de cada lição (aparece no mapa e na página da lição)
REG = {1: "formal", 50: "informal", 2: "formal", 51: "informal",
       3: "formal", 52: "informal", 25: "formal", 53: "informal"}

REG_INFO = {
    "formal": "Use com chefes, clientes, pessoas mais velhas e quem você não conhece. Sempre educado, nunca soa estranho.",
    "informal": "Use com colegas próximos e amigos. É assim que os chineses falam no dia a dia. Com o chefe ou um cliente, prefira a lição formal.",
}

# lições informais novas: (id, título, objetivo, frases)
R_LESSONS = [
 (50, "Olá e tchau · informal", "Cumprimentar e se despedir de colegas e amigos, do jeito do dia a dia.", [
  ("早 ！", "Zǎo!", "Bom dia! (entre colegas)"),
  ("嗨 ！", "Hāi!", "Oi!"),
  ("拜拜 ！", "Báibái!", "Tchau!"),
  ("回头 见 ！", "Huítóu jiàn!", "Até mais!"),
  ("明天 见 ！", "Míngtiān jiàn!", "Até amanhã!"),
  ("我 先 走 了 ！", "Wǒ xiān zǒu le!", "Vou indo! (ao sair do trabalho)"),
  ("晚安 ！", "Wǎn'ān!", "Boa noite! (ao dormir)"),
 ]),
 (51, "Como você está? · informal", "Perguntar como a pessoa está do jeito que os chineses falam entre amigos.", [
  ("好久 不见 ！", "Hǎojiǔ bú jiàn!", "Quanto tempo!"),
  ("最近 怎么样 ？", "Zuìjìn zěnmeyàng?", "E aí, como andam as coisas?"),
  ("挺 好 ！", "Tǐng hǎo!", "Tudo ótimo!"),
  ("还 行 。", "Hái xíng.", "Vai indo."),
  ("还 不错 ， 你 呢 ？", "Hái búcuò, nǐ ne?", "Até que bem, e você?"),
  ("忙 死 了 ！", "Máng sǐ le!", "Tô atolado! (exagero, só entre amigos)"),
  ("老 样子 。", "Lǎo yàngzi.", "O de sempre."),
 ]),
 (52, "Meu nome é… · informal", "Se apresentar para colegas da sua idade e puxar conversa com quem é novo.", [
  ("你 叫 什么 名字 ？", "Nǐ jiào shénme míngzi?", "Como você se chama?"),
  ("叫 我 保罗 就 行 。", "Jiào wǒ Bǎoluó jiù xíng.", "Pode me chamar de Paulo."),
  ("你 是 新 来 的 吗 ？", "Nǐ shì xīn lái de ma?", "Você é novo aqui?"),
  ("对 ， 我 是 新 来 的 。", "Duì, wǒ shì xīn lái de.", "Sou, cheguei agora."),
  ("很 高兴 认识 你 。", "Hěn gāoxìng rènshi nǐ.", "Prazer!"),
 ]),
 (53, "Como vai o seu dia? · informal", "Puxar conversa com colegas no corredor e na hora do almoço.", [
  ("吃 了 吗 ？", "Chī le ma?", "Já comeu? (cumprimento perto do almoço)"),
  ("吃 了 ， 你 呢 ？", "Chī le, nǐ ne?", "Já, e você?"),
  ("今天 忙 不 忙 ？", "Jīntiān máng bu máng?", "Hoje tá corrido?"),
  ("还 好 。", "Hái hǎo.", "Tranquilo."),
  ("累 死 了 ！", "Lèi sǐ le!", "Tô morto de cansado!"),
  ("走 ， 吃饭 去 ！", "Zǒu, chīfàn qù!", "Bora comer!"),
 ]),
]

# palavras novas: hanzi -> (pinyin, significado, explicação)
R_GLOSS = {
 "大家": ("dàjiā", "todos / pessoal", "大家好 (dàjiā hǎo) abre reuniões e apresentações."),
 "早": ("zǎo", "cedo; bom dia! (curto)", "Entre colegas, de manhã, basta dizer 早 (zǎo). Com o chefe, prefira 早上好 (zǎoshang hǎo)."),
 "嗨": ("hāi", "oi", "Vem do inglês “hi”. Bem informal, entre jovens e amigos."),
 "拜拜": ("báibái", "tchau", "Vem do inglês “bye-bye”. É a despedida mais comum no dia a dia e no telefone. Também se ouve bāibāi."),
 "回头": ("huítóu", "daqui a pouco / depois", "回头见 (huítóu jiàn) = até mais."),
 "先": ("xiān", "primeiro / antes", ""),
 "走": ("zǒu", "ir embora / andar", "我先走了 (wǒ xiān zǒu le) = vou indo (antes de vocês). É o jeito educado de sair do escritório no fim do dia. Sozinho, 走 (zǒu) também é “vamos!”."),
 "最近": ("zuìjìn", "ultimamente / esses dias", ""),
 "挺": ("tǐng", "bem / bastante", "Mais leve que 很 (hěn) e muito usado na fala: 挺好 (tǐng hǎo) = tá bom."),
 "行": ("xíng", "ok / dá / pode ser", "还行 (hái xíng) = vai indo. Sozinho, 行 (xíng) = beleza, combinado."),
 "死": ("sǐ", "morrer; (…死了) demais", "Exagero do dia a dia, como “morto de cansado”: 累死了 (lèi sǐ le). Só entre amigos."),
 "老": ("lǎo", "velho; de sempre", "老样子 (lǎo yàngzi) = do jeito de sempre. 老 (lǎo) + sobrenome chama um colega mais velho com intimidade: 老王 (lǎo Wáng)."),
 "样子": ("yàngzi", "jeito / aparência", ""),
 "好久": ("hǎojiǔ", "muito tempo", ""),
 "不见": ("bú jiàn", "não ver", "好久不见 (hǎojiǔ bú jiàn) = quanto tempo (lit. muito tempo sem ver)."),
 "称呼": ("chēnghu", "chamar (alguém de) / tratamento", "您怎么称呼？(nín zěnme chēnghu) pergunta com educação como chamar a pessoa. Ela costuma responder com o sobrenome e o cargo."),
 "名片": ("míngpiàn", "cartão de visita", "Entregue e receba com as duas mãos e olhe o cartão por um instante antes de guardar. É sinal de respeito."),
 "就": ("jiù", "já / então / só isso", "…就行 (jiù xíng) = e pronto, basta: 叫我保罗就行 (jiào wǒ Bǎoluó jiù xíng) = pode me chamar só de Paulo."),
 "新": ("xīn", "novo", ""),
 "对": ("duì", "certo / isso mesmo", "Para confirmar: 对 (duì) = isso, é."),
}

# gramática das lições novas: (título, fórmula, explicação, exemplo em tokens, pinyin, português)
R_GP = {
 50: [
  ("Despedida com 见 (ver)", "Quando + 见 (jiàn)",
   "Para se despedir, diga QUANDO vocês vão se ver de novo e acrescente 见 (jiàn, ver). Em português seria “amanhã nos vemos”.",
   "明天 见 ！", "Míngtiān jiàn!", "Até amanhã!"),
  ("Formal ou informal?", "早上好 (zǎoshang hǎo) → 早 (zǎo) · 再见 (zàijiàn) → 拜拜 (báibái)",
   "Entre colegas, os chineses encurtam: 早 (zǎo) no lugar de 早上好 (zǎoshang hǎo) e 拜拜 (báibái) no lugar de 再见 (zàijiàn). Com o chefe ou um cliente, use as formas completas da lição formal.",
   "拜拜 ！", "Báibái!", "Tchau!"),
 ],
 51: [
  ("挺 no lugar de 很", "挺 (tǐng) + adjetivo",
   "Na conversa, os chineses usam muito 挺 (tǐng) no lugar de 很 (hěn). Soa mais leve e natural: 挺好 (tǐng hǎo) = tá ótimo. Você também vai ouvir 挺好的 (tǐng hǎo de), com o mesmo sentido.",
   "挺 好 ！", "Tǐng hǎo!", "Tudo ótimo!"),
  ("Exagero com 死了", "Adjetivo + 死了 (sǐ le)",
   "Igual ao “morto de cansado” do português: 忙死了 (máng sǐ le) = ocupadíssimo. Use só com colegas próximos e amigos; com o chefe soa exagerado.",
   "忙 死 了 ！", "Máng sǐ le!", "Tô atolado!"),
 ],
 52: [
  ("A palavra de pergunta fica no lugar da resposta", "Você + 叫 (jiào) + 什么 (shénme)？ → Eu + 叫 + nome",
   "Em português a pergunta começa com “como” ou “qual”. Em chinês a palavra de pergunta fica exatamente onde a resposta vai estar. Pergunta: você chama O QUÊ? Resposta: eu chamo PAULO.",
   "你 叫 什么 名字 ？", "Nǐ jiào shénme míngzi?", "Como você se chama?"),
  ("…的 = “aquele que…”", "新来的 (xīn lái de) = o que chegou agora",
   "O 的 (de) também transforma uma descrição em uma pessoa: 新来的 (xīn lái de) = o novato. É muito usado no trabalho.",
   "你 是 新 来 的 吗 ？", "Nǐ shì xīn lái de ma?", "Você é novo aqui?"),
 ],
 53: [
  ("吃了吗？ como cumprimento", "吃了吗 (chī le ma)？",
   "Perto do almoço ou do jantar, perguntar se a pessoa já comeu é um jeito de dizer oi. Não é convite: basta responder 吃了 (chī le, já comi) ou 还没 (hái méi, ainda não).",
   "吃 了 吗 ？", "Chī le ma?", "Já comeu?"),
 ],
}

# palavras que soam diferente da leitura do caractere sozinho: o áudio é montado pelas sílabas do pinyin
FORCE_SYL = {"拜拜"}
