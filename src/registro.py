# -*- coding: utf-8 -*-
# Formal e informal no Módulo 1.
# Cada tema tem duas lições em sequência: a formal (chefe, cliente, pessoa mais velha,
# desconhecido) e a informal (colegas próximos e amigos). O objetivo é que o aluno saiba
# falar nos dois registros e não soe "de livro" com os colegas chineses.

# registro de cada lição (aparece no mapa e na página da lição)
REG = {1: "formal", 50: "informal", 2: "formal", 51: "informal",
       3: "formal", 52: "informal", 25: "formal", 53: "informal",
       9: "formal", 59: "informal", 14: "formal", 61: "informal"}

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

# Módulo 2: ferramentas para não travar (moldes que o aluno reaproveita trocando uma peça)
R_LESSONS += [
 (54, "Apontar: este e aquele", "Apontar para coisas e lugares, mesmo sem saber o nome delas.", [
  ("这个 是 什么 ？", "Zhège shì shénme?", "O que é isto?"),
  ("那个 是 什么 ？", "Nàge shì shénme?", "O que é aquilo?"),
  ("这个 叫 什么 ？", "Zhège jiào shénme?", "Como isto se chama?"),
  ("我 要 这个 。", "Wǒ yào zhège.", "Quero este."),
  ("不 是 这个 ， 是 那个 。", "Bú shì zhège, shì nàge.", "Não é este, é aquele."),
  ("在 这里 。", "Zài zhèlǐ.", "Está aqui."),
  ("在 那里 。", "Zài nàlǐ.", "Está ali."),
 ]),
 (55, "Perguntar qualquer coisa", "Perguntar quem, qual, quando, por quê e como, trocando uma só peça da frase.", [
  ("他 是 谁 ？", "Tā shì shéi?", "Quem é ele?"),
  ("他 是 我 的 同事 。", "Tā shì wǒ de tóngshì.", "Ele é meu colega de trabalho."),
  ("你 要 哪个 ？", "Nǐ yào nǎge?", "Qual você quer?"),
  ("你 什么 时候 来 ？", "Nǐ shénme shíhou lái?", "Quando você vem?"),
  ("我 明天 来 。", "Wǒ míngtiān lái.", "Venho amanhã."),
  ("你 为什么 学 中文 ？", "Nǐ wèishénme xué Zhōngwén?", "Por que você estuda chinês?"),
  ("因为 我 的 同事 是 中国 人 。", "Yīnwèi wǒ de tóngshì shì Zhōngguó rén.", "Porque meus colegas são chineses."),
  ("这个 怎么 用 ？", "Zhège zěnme yòng?", "Como se usa isto?"),
 ]),
 (56, "Sim e não sem “sim”", "Responder perguntas de sim ou não do jeito chinês: repetindo o verbo.", [
  ("你 有 微信 吗 ？", "Nǐ yǒu Wēixìn ma?", "Você tem WeChat?"),
  ("有 。", "Yǒu.", "Tenho. (= sim)"),
  ("这个 是 你 的 吗 ？", "Zhège shì nǐ de ma?", "Isto é seu?"),
  ("不 是 。", "Bú shì.", "Não (é)."),
  ("我 可以 坐 这里 吗 ？", "Wǒ kěyǐ zuò zhèlǐ ma?", "Posso sentar aqui?"),
  ("可以 ， 请 坐 。", "Kěyǐ, qǐng zuò.", "Pode, sente-se."),
  ("你 去 不 去 ？", "Nǐ qù bu qù?", "Você vai?"),
  ("去 ！", "Qù!", "Vou!"),
 ]),
 (57, "Quero, gostaria, acho", "Dizer o que você quer, o que gostaria e o que acha, e admitir que não sabe.", [
  ("我 想 喝 水 。", "Wǒ xiǎng hē shuǐ.", "Eu gostaria de beber água."),
  ("我 要 一 杯 咖啡 。", "Wǒ yào yì bēi kāfēi.", "Quero um café."),
  ("我 不 想 去 。", "Wǒ bù xiǎng qù.", "Não estou a fim de ir."),
  ("你 觉得 怎么样 ？", "Nǐ juéde zěnmeyàng?", "O que você acha?"),
  ("我 觉得 很 好 。", "Wǒ juéde hěn hǎo.", "Acho que está ótimo."),
  ("我 不 知道 。", "Wǒ bù zhīdào.", "Não sei."),
  ("我 知道 了 。", "Wǒ zhīdào le.", "Tá bom, entendi."),
 ]),
 (58, "Pedir sem mandar", "Pedir as coisas de um jeito gentil, sem soar como ordem.", [
  ("你 能 说 慢 一点 吗 ？", "Nǐ néng shuō màn yìdiǎn ma?", "Você pode falar mais devagar?"),
  ("帮 我 看 一下 ， 好 吗 ？", "Bāng wǒ kàn yíxià, hǎo ma?", "Dá uma olhadinha pra mim?"),
  ("麻烦 你 等 一下 。", "Máfan nǐ děng yíxià.", "Espera um pouquinho, por favor."),
  ("我们 去 吃饭 吧 ！", "Wǒmen qù chīfàn ba!", "Vamos comer?"),
  ("你 说 吧 。", "Nǐ shuō ba.", "Pode falar."),
  ("你 是 巴西 人 吧 ？", "Nǐ shì Bāxī rén ba?", "Você é brasileiro, né?"),
 ]),
 (59, "Pedindo ajuda · informal", "Pedir ajuda e mostrar que entendeu, do jeito que se fala entre colegas.", [
  ("帮 个 忙 ！", "Bāng ge máng!", "Me dá uma força!"),
  ("你 说 什么 ？", "Nǐ shuō shénme?", "O quê? / Como?"),
  ("能 慢 一点 吗 ？", "Néng màn yìdiǎn ma?", "Dá pra ir mais devagar?"),
  ("这个 怎么 写 ？", "Zhège zěnme xiě?", "Como se escreve isso?"),
  ("懂 了 ！", "Dǒng le!", "Entendi!"),
  ("好 的 。", "Hǎo de.", "Tá bom. / Ok."),
  ("收到 ！", "Shōudào!", "Recebido! / Pode deixar!"),
 ]),
 (60, "Quando falta a palavra", "Ganhar tempo, descrever o que você não sabe nomear e confirmar se entendeu.", [
  ("那个 ， 怎么 说 呢 ？", "Nèige, zěnme shuō ne?", "É… como posso dizer?"),
  ("我 不 知道 用 中文 怎么 说 。", "Wǒ bù zhīdào yòng Zhōngwén zěnme shuō.", "Não sei dizer isso em chinês."),
  ("就是 一 个 东西 ， 用来 开 门 的 。", "Jiùshì yí ge dōngxi, yònglái kāi mén de.", "É uma coisa que serve para abrir a porta."),
  ("你 的 意思 是 这个 吗 ？", "Nǐ de yìsi shì zhège ma?", "Você quer dizer isto?"),
  ("是 不 是 这个 ？", "Shì bu shì zhège?", "É este?"),
  ("对 ， 就是 这个 ！", "Duì, jiùshì zhège!", "Isso, é este mesmo!"),
 ]),
 (61, "Gentilezas · informal", "Agradecer, se desculpar e responder elogios entre colegas.", [
  ("辛苦 了 ！", "Xīnkǔ le!", "Bom trabalho! (do chefe para a equipe, ou entre colegas)"),
  ("谢 啦 ！", "Xiè la!", "Valeu!"),
  ("没事 。", "Méi shì.", "Tranquilo. / De nada."),
  ("小意思 。", "Xiǎo yìsi.", "Não foi nada."),
  ("别 客气 。", "Bié kèqi.", "Fique à vontade."),
  ("不好意思 ， 我 来 晚 了 。", "Bù hǎoyìsi, wǒ lái wǎn le.", "Foi mal, cheguei atrasado."),
  ("还 差 得 远 呢 。", "Hái chà de yuǎn ne.", "Ainda falta muito. (resposta a elogio)"),
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
 "那个": ("nàge", "aquele / aquilo", "Também se fala nèige. Sozinho, no meio da frase, é o “é…” dos chineses quando procuram uma palavra."),
 "那里": ("nàlǐ", "ali / lá", ""),
 "为什么": ("wèishénme", "por quê", ""),
 "因为": ("yīnwèi", "porque", "Resposta para 为什么 (wèishénme, por quê)."),
 "杯": ("bēi", "copo / xícara (classificador)", "一杯咖啡 (yì bēi kāfēi) = um café (lit. uma xícara de café)."),
 "知道": ("zhīdào", "saber", "我不知道 (wǒ bù zhīdào) = não sei. 我知道了 (wǒ zhīdào le) = entendi, tá bom."),
 "写": ("xiě", "escrever", ""),
 "收到": ("shōudào", "receber; recebido!", "No trabalho e no WeChat, 收到 (shōudào) é a resposta padrão a um pedido: “recebido, pode deixar”."),
 "就是": ("jiùshì", "é justamente / é que", "对，就是这个 (duì, jiùshì zhège) = isso, é este mesmo."),
 "东西": ("dōngxi", "coisa / objeto", ""),
 "用来": ("yònglái", "servir para", "一个东西，用来… (yí ge dōngxi, yònglái…) = uma coisa que serve para…"),
 "过奖": ("guòjiǎng", "elogiar demais", "过奖了 (guòjiǎng le) = o senhor exagera. Resposta educada e modesta a um elogio."),
 "谢": ("xiè", "agradecer", "谢啦 (xiè la) = valeu."),
 "啦": ("la", "(partícula de fala animada)", "Deixa a frase mais leve e simpática: 谢啦 (xiè la) = valeu!"),
 "没事": ("méi shì", "tudo bem / de nada", "Serve para responder a um obrigado e a um pedido de desculpas: tranquilo, não foi nada."),
 "小意思": ("xiǎo yìsi", "não foi nada", "Lit. “pequena intenção”. Resposta modesta quando alguém agradece."),
 "清楚": ("qīngchu", "claro / com clareza", "没听清楚 (méi tīng qīngchu) = não ouvi direito. É diferente de 听不懂 (tīng bu dǒng), que é ouvir e não entender."),
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
 54: [
  ("这 = perto, 那 = longe", "这个 (zhège) · 那个 (nàge) · 这里 (zhèlǐ) · 那里 (nàlǐ)",
   "这 (zhè) é o que está perto de você; 那 (nà), o que está longe. Com 个 (ge) vira objeto: este, aquele. Com 里 (lǐ) vira lugar: aqui, ali. Apontando com o dedo, você já se comunica sem saber o nome da coisa.",
   "不 是 这个 ， 是 那个 。", "Bú shì zhège, shì nàge.", "Não é este, é aquele."),
  ("Lógica: dá para tirar o sujeito", "在 (zài) + lugar",
   "Quando todo mundo sabe do que se fala, o chinês tira o sujeito. Pergunta: 钥匙在哪里？(yàoshi zài nǎlǐ, onde está a chave?). Resposta: 在这里 (zài zhèlǐ), “está aqui”, sem repetir a chave.",
   "在 这里 。", "Zài zhèlǐ.", "Está aqui."),
 ],
 55: [
  ("A pergunta é a resposta com um buraco", "Monte a resposta → troque a parte que você não sabe",
   "Em português a palavra de pergunta vai para o começo e a ordem muda. Em chinês, NADA muda de lugar: você monta a frase como se fosse a resposta e põe a palavra de pergunta no lugar da informação que falta. 我明天来 (wǒ míngtiān lái, venho amanhã) → 你什么时候来？(nǐ shénme shíhou lái, quando você vem?).",
   "你 什么 时候 来 ？", "Nǐ shénme shíhou lái?", "Quando você vem?"),
  ("As peças de pergunta", "谁 (shéi) quem · 哪个 (nǎge) qual · 什么时候 (shénme shíhou) quando · 为什么 (wèishénme) por quê · 怎么 (zěnme) como",
   "Cada uma ocupa o lugar exato da resposta: 他是谁？(tā shì shéi) → 他是我的同事 (tā shì wǒ de tóngshì). Para responder um 为什么 (wèishénme), comece com 因为 (yīnwèi, porque).",
   "他 是 谁 ？", "Tā shì shéi?", "Quem é ele?"),
 ],
 56: [
  ("Não existe “sim”: repita o verbo", "Pergunta com 吗 (ma) → responda com o verbo",
   "Para dizer sim, repita o verbo da pergunta: 有 (yǒu, tenho), 是 (shì, é), 可以 (kěyǐ, pode), 去 (qù, vou). Para dizer não, ponha 不 (bù) antes: 不是 (bú shì), 不去 (bú qù). Com 有 (yǒu), o não é 没 (méi): 没有 (méiyǒu, não tenho). 对 (duì) só serve para confirmar uma informação.",
   "你 有 微信 吗 ？", "Nǐ yǒu Wēixìn ma?", "Você tem WeChat?"),
  ("Verbo + 不 + verbo", "去不去 (qù bu qù)？ = vai ou não vai?",
   "Outro jeito de perguntar, sem 吗 (ma): diga o verbo, 不 (bu) e o verbo de novo. A resposta é a mesma: repita o verbo.",
   "你 去 不 去 ？", "Nǐ qù bu qù?", "Você vai?"),
 ],
 57: [
  ("想 ou 要?", "想 (xiǎng) = gostaria · 要 (yào) = quero",
   "要 (yào) é direto: num pedido no restaurante é normal, mas com o chefe pode soar exigente. 想 (xiǎng) é mais suave, como “eu queria”. Na dúvida, use 想.",
   "我 想 喝 水 。", "Wǒ xiǎng hē shuǐ.", "Eu gostaria de beber água."),
  ("Eu + 觉得 + opinião", "我觉得 (wǒ juéde) + frase",
   "觉得 (juéde) apresenta a sua opinião: depois dele vem uma frase completa. Para perguntar a opinião do outro: 你觉得怎么样？(nǐ juéde zěnmeyàng, o que você acha?).",
   "我 觉得 很 好 。", "Wǒ juéde hěn hǎo.", "Acho que está ótimo."),
 ],
 58: [
  ("Pedido vira pergunta", "你能 (nǐ néng) … 吗 (ma)？",
   "Verbo + objeto, sozinho, soa como ordem. Para pedir com gentileza, transforme em pergunta: você consegue…? 你能说慢一点吗？(nǐ néng shuō màn yìdiǎn ma). No fim, 好吗？(hǎo ma, pode ser?) também suaviza.",
   "你 能 说 慢 一点 吗 ？", "Nǐ néng shuō màn yìdiǎn ma?", "Você pode falar mais devagar?"),
  ("一下 e 麻烦你 diminuem o pedido", "verbo + 一下 (yíxià) · 麻烦你 (máfan nǐ) + pedido",
   "一下 (yíxià) depois do verbo transforma em “rapidinho”: 等一下 (děng yíxià, espera um pouquinho). 麻烦你 (máfan nǐ) no começo é “desculpe incomodar”. Com os dois, o pedido fica educado mesmo sem 请 (qǐng).",
   "麻烦 你 等 一下 。", "Máfan nǐ děng yíxià.", "Espera um pouquinho, por favor."),
  ("吧: convite, permissão e palpite", "…吧 (ba)",
   "No fim de uma sugestão, 吧 (ba) vira convite: 我们去吃饭吧 (wǒmen qù chīfàn ba, vamos comer?). Também dá permissão: 你说吧 (nǐ shuō ba, pode falar). E confirma um palpite: 你是巴西人吧？(você é brasileiro, né?). Para pedir que alguém faça algo por você, prefira a pergunta com 能 (néng).",
   "我们 去 吃饭 吧 ！", "Wǒmen qù chīfàn ba!", "Vamos comer?"),
 ],
 59: [
  ("收到 e 好的 no trabalho", "收到 (shōudào) · 好的 (hǎo de)",
   "Quando um colega ou o chefe pede algo, principalmente por WeChat, a resposta padrão é 收到 (shōudào, recebido) ou 好的 (hǎo de, ok). Ficar em silêncio parece que você não viu.",
   "收到 ！", "Shōudào!", "Recebido! / Pode deixar!"),
 ],
 60: [
  ("Ganhar tempo como um nativo", "那个… (nèige) · 怎么说呢 (zěnme shuō ne)",
   "Quando procuram uma palavra, os chineses dizem 那个… (nèige), como o nosso “é…”, ou 怎么说呢 (zěnme shuō ne, como posso dizer). Usar isso soa natural e te dá tempo para pensar.",
   "那个 ， 怎么 说 呢 ？", "Nèige, zěnme shuō ne?", "É… como posso dizer?"),
  ("Descrever o que não sabe nomear", "一个东西 (yí ge dōngxi)，用来 (yònglái) + verbo + 的 (de)",
   "Não sabe o nome? Diga para que serve: uma coisa que serve para abrir a porta = a chave. A pessoa vai te dizer a palavra, e você aprende na hora.",
   "就是 一 个 东西 ， 用来 开 门 的 。", "Jiùshì yí ge dōngxi, yònglái kāi mén de.", "É uma coisa que serve para abrir a porta."),
 ],
 61: [
  ("对不起 ou 不好意思?", "对不起 (duìbuqǐ) = erro sério · 不好意思 (bù hǎoyìsi) = foi mal",
   "对不起 (duìbuqǐ) é para quando você errou de verdade. Para coisas pequenas, como esbarrar em alguém, chegar um pouco atrasado ou interromper, use 不好意思 (bù hǎoyìsi).",
   "不好意思 ， 我 来 晚 了 。", "Bù hǎoyìsi, wǒ lái wǎn le.", "Foi mal, cheguei atrasado."),
  ("辛苦了: quem diz para quem", "辛苦了 (xīnkǔ le) · 您辛苦了 (nín xīnkǔ le)",
   "辛苦了 (xīnkǔ le) é o que o chefe diz para a equipe, ou o que colegas dizem entre si. Para agradecer ao chefe ou a um cliente, diga 您辛苦了 (nín xīnkǔ le).",
   "辛苦 了 ！", "Xīnkǔ le!", "Bom trabalho!"),
 ],
 53: [
  ("吃了吗？ como cumprimento", "吃了吗 (chī le ma)？",
   "Perto do almoço ou do jantar, perguntar se a pessoa já comeu é um jeito de dizer oi. Não é convite: basta responder 吃了 (chī le, já comi) ou 还没 (hái méi, ainda não).",
   "吃 了 吗 ？", "Chī le ma?", "Já comeu?"),
 ],
}

# palavras que soam diferente da leitura do caractere sozinho: o áudio é montado pelas sílabas do pinyin
FORCE_SYL = {"拜拜"}
