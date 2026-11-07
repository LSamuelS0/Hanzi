# Código-fonte do app

O `index.html` publicado na raiz é gerado a partir destes arquivos. Não edite o `index.html` direto.

| Arquivo | O que é |
|---|---|
| `app.tpl.html` | Modelo do app: telas, estilo e JavaScript |
| `ctest.json` | Conteúdo pronto: lições, glossário, gramática, histórias e cenas |
| `curriculum.py`, `modules.py`, `grammar.py`, `stories.py`, `scenes.py`, `data.py` | Fontes do conteúdo |
| `build_content.py` | Gera `ctest.json`, `audio.json` e `strokes.json` a partir das fontes. Precisa dos downloads em `dl/` (audio-cmn, hanzi-writer-data, makemeahanzi, twemoji), que não ficam no repositório |
| `build_app.py` | Junta modelo, conteúdo e Hanzi Writer no `../index.html` e atualiza a versão do `../sw.js` |
| `firebase.json` | Configuração pública do Firebase. Não é segredo |
| `conv_api.txt` | (opcional, fora do git) Endereço do servidor da conversa |

Para publicar uma mudança no app, rode dentro de `src/`:

```
python build_app.py
```
