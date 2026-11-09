# Código-fonte do app

O `index.html` publicado na raiz é gerado a partir destes arquivos. Não edite o `index.html` direto.

| Arquivo | O que é |
|---|---|
| `app.tpl.html` | Modelo do app: telas, estilo e JavaScript |
| `ctest.json` | Conteúdo pronto: lições, glossário, gramática, histórias e cenas |
| `curriculum.py`, `modules.py`, `grammar.py`, `stories.py`, `scenes.py`, `data.py` | Fontes do conteúdo |
| `registro.py` | Lições formais e informais do Módulo 1: registro de cada lição, as 4 lições informais novas (50 a 53), palavras e gramática delas |
| `syllables.txt` | Lista de sílabas do pinyin, usada para montar o áudio de palavras sem gravação própria |
| `build_content.py` | Gera `ctest.json`, `audio.json` e `strokes.json` a partir das fontes. Precisa dos downloads em `dl/` (audio-cmn, hanzi-writer-data, makemeahanzi, twemoji), que não ficam no repositório |
| `build_app.py` | Junta modelo, conteúdo e Hanzi Writer no `../index.html` e atualiza a versão do `../sw.js` |
| `firebase.json` | Configuração pública do Firebase. Não é segredo |
| `conv_api.txt` | (opcional, fora do git) Endereço do servidor da conversa |

Para gerar o conteúdo, baixe as fontes em `src/dl/` (só os índices; os arquivos são baixados conforme a necessidade):

```
git clone --no-checkout --filter=blob:none --depth 1 https://github.com/hugolpz/audio-cmn dl/audio-cmn
git clone --no-checkout --filter=blob:none --depth 1 https://github.com/chanind/hanzi-writer-data dl/hwd
git clone --no-checkout --filter=blob:none --depth 1 https://github.com/skishore/makemeahanzi dl/mmah
git -C dl/mmah checkout HEAD -- dictionary.txt
cp ../audio.json ../strokes.json .
python build_content.py
```

Para publicar uma mudança no app, rode dentro de `src/`:

```
python build_app.py
```
