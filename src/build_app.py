# Monta o app a partir do modelo (app.tpl.html) e do conteúdo (ctest.json).
# Rode dentro de src/:  python build_app.py
# Gera hanzi.html (versão sem login, para o Claude) e o index.html publicado.
# A pasta de saída é ../ (raiz do repositório) ou pwa/ se existir ao lado.
import json, re, shutil, os
OUT = 'pwa' if os.path.isdir('pwa') else '..'
t = open('app.tpl.html').read(); c = json.load(open('ctest.json'))
hw = open('hanzi-writer.js').read().replace('</script', '<\\/script')
h = t.replace('/*CONTENT*/null', json.dumps(c, ensure_ascii=False, separators=(',', ':'))).replace('/*HANZIWRITER*/', hw)
open('hanzi.html', 'w').write(h)
hp = h
if os.path.exists('firebase.json'): hp = hp.replace('/*FIREBASE_CONFIG*/null', open('firebase.json').read().strip())
# endereço do servidor da conversa (Cloudflare Worker); vazio = conversa desligada
if os.path.exists('conv_api.txt'): hp = hp.replace('/*CONV_API*/""', json.dumps(open('conv_api.txt').read().strip()))
p = open(f'{OUT}/index.html').read(); s0 = p.index('<title>'); e0 = p.index('<script>if("serviceWorker"')
open(f'{OUT}/index.html', 'w').write(p[:s0] + hp + p[e0:])
for f in ('strokes.json', 'audio.json'):
    if os.path.exists(f) and os.path.abspath(f) != os.path.abspath(f'{OUT}/{f}'): shutil.copy(f, f'{OUT}/{f}')
sw = open(f'{OUT}/sw.js').read()
v = int(re.search(r'hanzi-v(\d+)', sw).group(1)) + 1
sw = re.sub(r'const V="hanzi-v\d+"', f'const V="hanzi-v{v}"', sw)
open(f'{OUT}/sw.js', 'w').write(sw); print('saída', OUT, 'sw', v)
