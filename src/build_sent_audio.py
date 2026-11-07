# Monta um mp3 por frase a partir das gravações nativas (palavras -> caracteres -> sílabas).
import json, subprocess, base64, os, sys, tempfile, unicodedata
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from curriculum import G, L
from data import SENTENCES
R = "dl/audio-cmn"
SYL = set(open("syllables.txt").read().split())
names = subprocess.run(["git","-c","core.quotepath=off","ls-tree","--name-only","HEAD","24k-abr/hsk/"],cwd=R,capture_output=True,text=True).stdout.split("\n")
HSK = {n.split("cmn-")[1][:-4] for n in names if "cmn-" in n}
MARK = {}
for base, marks in {"a":"āáǎà","e":"ēéěè","i":"īíǐì","o":"ōóǒò","u":"ūúǔù","v":"ǖǘǚǜ"}.items():
    for t, m in enumerate(marks, 1): MARK[m] = (base, t)
MARK["ü"] = ("v", 0)
HAN = lambda c: "一" <= c <= "鿿"

def pinyin_syllables(p):
    """devolve [(silaba_sem_tom, tom)] para um texto em pinyin"""
    import re
    out = []
    for tok in re.split(r"[\s,.!?;:，。！？'’\-…]+", p):
        if not tok: continue
        raw = list(tok); norm = []; tones = []
        for c in raw:
            if c in MARK: b, t = MARK[c]; norm.append(b); tones.append(t)
            else: norm.append(c.lower()); tones.append(0)
        s = "".join(norm); n = len(s); best = [None]*(n+1); best[0] = []
        for i in range(n):
            if best[i] is None: continue
            for Ln in range(1, 7):
                if i+Ln <= n and s[i:i+Ln] in SYL:
                    cand = best[i] + [(i, i+Ln)]
                    if best[i+Ln] is None or len(cand) < len(best[i+Ln]): best[i+Ln] = cand
        if best[n] is None: return None
        for a, b in best[n]:
            t = max(tones[a:b]) or 5
            out.append((s[a:b], t))
    return out

def checkout(paths):
    paths = [p for p in paths if not os.path.exists(os.path.join(R, p))]
    for i in range(0, len(paths), 200):
        subprocess.run(["git","checkout","HEAD","--"]+paths[i:i+200], cwd=R, check=True, capture_output=True)

def pieces_for(tokens, pinyin):
    """lista de arquivos mp3 (por palavra) para a frase"""
    chars = [c for t in tokens for c in t if HAN(c)]
    syl = pinyin_syllables(pinyin)
    if syl is None or len(syl) != len(chars): syl = None
    words = []; ci = 0
    for t in tokens:
        hz = [c for c in t if HAN(c)]
        if not hz: continue
        if t in HSK: words.append([f"24k-abr/hsk/cmn-{t}.mp3"])
        else:
            files = []
            for k, c in enumerate(hz):
                if c in HSK: files.append(f"24k-abr/hsk/cmn-{c}.mp3")
                elif syl:
                    s, tn = syl[ci+k]; tn = tn if tn in (1,2,3,4) else 1
                    files.append(f"24k-abr/syllabs/cmn-{s}{tn}.mp3")
                else: return None
            words.append(files)
        ci += len(hz)
    return words

TMP = tempfile.mkdtemp(dir=".")
def clean(src, idx):
    out = os.path.join(TMP, f"p{idx}.wav")
    f = "silenceremove=start_periods=1:start_threshold=-42dB,areverse,silenceremove=start_periods=1:start_threshold=-42dB,areverse,loudnorm=I=-18:TP=-2:LRA=7"
    subprocess.run(["ffmpeg","-loglevel","error","-y","-i",os.path.join(R,src),"-af",f,"-ar","24000","-ac","1",out],check=True)
    return out

def build(words, out):
    lst = []; n = 0
    gap = os.path.join(TMP, "gap.wav"); gap_s = os.path.join(TMP, "gaps.wav")
    if not os.path.exists(gap):
        subprocess.run(["ffmpeg","-loglevel","error","-y","-f","lavfi","-i","anullsrc=r=24000:cl=mono","-t","0.07",gap],check=True)
        subprocess.run(["ffmpeg","-loglevel","error","-y","-f","lavfi","-i","anullsrc=r=24000:cl=mono","-t","0.02",gap_s],check=True)
    for wi, files in enumerate(words):
        for fi, f in enumerate(files):
            lst.append(clean(f, f"{abs(hash(out))}_{n}")); n += 1
            if fi < len(files)-1: lst.append(gap_s)
        if wi < len(words)-1: lst.append(gap)
    listf = os.path.join(TMP, "list.txt")
    open(listf, "w").write("".join(f"file '{os.path.abspath(p)}'\n" for p in lst))
    subprocess.run(["ffmpeg","-loglevel","error","-y","-f","concat","-safe","0","-i",listf,"-af","apad=pad_dur=0.15","-ac","1","-ar","24000","-b:a","32k",out],check=True)
    return base64.b64encode(open(out,"rb").read()).decode()

def main():
    audio = json.load(open("audio.json"))
    jobs = []
    for z, p, pt, cat in SENTENCES:
        # mesma segmentação do app (palavras com gravação)
        segs = json.load(open("content.json"))["sentences"]
    seg_map = {s[0]: [w for w, a in s[4]] for s in segs}
    for z, p, pt, cat in SENTENCES: jobs.append((z, seg_map[z], p))
    for (i, lv, t, goal, ph) in L:
        for z, p, pt in ph:
            tk = z.split(); jobs.append(("".join(tk), tk, p))
    # palavras do glossário sem gravação própria
    word_jobs = [(k, [k], G[k][0]) for k in G if k not in HSK]
    allp = set()
    plans = {}
    for key, tk, p in jobs + word_jobs:
        w = pieces_for(tk, p)
        if w is None: print("sem plano:", key, p); continue
        plans[key] = w; allp |= {f for ws in w for f in ws}
    checkout(sorted(allp))
    os.makedirs("sent_mp3", exist_ok=True)
    for key, tk, p in jobs:
        if key in plans and "f:"+key not in audio:
            audio["f:"+key] = build(plans[key], f"sent_mp3/{abs(hash(key))}.mp3")
    for key, tk, p in word_jobs:
        if key in plans and "w:"+key not in audio:
            audio["w:"+key] = build(plans[key], f"sent_mp3/w{abs(hash(key))}.mp3")
    json.dump(audio, open("audio.json","w"), ensure_ascii=False, separators=(",",":"))
    print("frases:", sum(1 for k in audio if k.startswith("f:")), "bytes:", os.path.getsize("audio.json"))

main()
