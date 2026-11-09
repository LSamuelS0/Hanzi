import re,json,sys,collections
sys.path.insert(0,'.')
from build_sent_audio import pinyin_syllables
from curriculum import G,L,NAMES_EXTRA
from data import SENTENCES,VOCAB
HAN=re.compile(r'[一-鿿]')
TONE={}
for b,m in {"a":"āáǎà","e":"ēéěè","i":"īíǐì","o":"ōóǒò","u":"ūúǔù","v":"ǖǘǚǜ"}.items():
    for t,c in enumerate(m,1):TONE[(b,t)]=c
def mark(s,t):
    if t not in (1,2,3,4):return s.replace("v","ü")
    v="a" if "a" in s else "e" if "e" in s else "o" if "ou" in s else [c for c in s if c in "aeiouv"][-1]
    return s.replace(v,TONE[(v,t)],1).replace("v","ü")
cm=collections.defaultdict(collections.Counter)
def learn(h,p):
    ch=[c for c in h if HAN.match(c)];sy=pinyin_syllables(p)
    if sy and len(sy)==len(ch):
        for c,(s,t) in zip(ch,sy):cm[c][mark(s,t)]+=1
for k,(p,m,n) in G.items():learn(k,p)
for v in VOCAB:learn(v[0],v[1])
for s in SENTENCES:learn(s[0],s[1])
for l in L:
    for z,p,pt in l[4]:learn(z.replace(" ",""),p)
EXTRA={"开":"kāi","准":"zhǔn","备":"bèi","走":"zǒu","们":"men","老":"lǎo","儿":"ér","那":"nà","午":"wǔ","姓":"xìng","贵":"guì","友":"yǒu","子":"zi","星":"xīng","经":"jīng","事":"shì","马":"mǎ","上":"shàng","问":"wèn"}
WORDS={k:v[0] for k,v in G.items()}
WORDS.update({v[0]:v[1] for v in VOCAB})
def py_of(run):
    out=[];i=0
    while i<len(run):
        for Ln in range(min(6,len(run)-i),0,-1):
            w=run[i:i+Ln]
            if Ln>1 and w in WORDS:out.append(WORDS[w]);i+=Ln;break
        else:
            c=run[i]
            if not HAN.match(c):i+=1;continue
            p=WORDS.get(c) if c in WORDS else (cm[c].most_common(1)[0][0] if cm[c] else EXTRA.get(c))
            if not p:return None
            out.append(p);i+=1
    return " ".join(out)
PYW=re.compile(r"^\s*[A-Za-zāáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜü']+")
def annotate(text,missing):
    res=[];pos=0
    for m in re.finditer(r'[一-鿿]+(?:[？！，]?[一-鿿]+)*[？！]?',text):
        res.append(text[pos:m.end()]);pos=m.end()
        after=text[pos:]
        nxt=PYW.match(after)
        if nxt and any(c in "āáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜ" for c in nxt.group(0)):continue  # já tem pinyin
        if after.lstrip().startswith("("):continue
        p=py_of(m.group(0))
        if p is None:missing.add(m.group(0));continue
        res.append(f" ({p})")
    res.append(text[pos:]);return "".join(res)

# ---- v2: sandhi, parênteses existentes, pinyin solto
OVR={"上":"shàng","午":"wǔ","一":"yī","不":"bù"}
TONECH="āáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜ"
def tone_of(s):
    for c in s:
        i=TONECH.find(c)
        if i>=0:return i%4+1
    return 5
NUM=set("零一二三四五六七八九十百千两几")
def py_list(run):
    out=[];i=0
    while i<len(run):
        for Ln in range(min(6,len(run)-i),0,-1):
            w=run[i:i+Ln]
            if Ln>1 and w in WORDS:out.append((w,WORDS[w]));i+=Ln;break
        else:
            c=run[i]
            if not HAN.match(c):i+=1;continue
            p=OVR.get(c) or WORDS.get(c) or (cm[c].most_common(1)[0][0] if cm[c] else EXTRA.get(c))
            if not p:return None
            out.append((c,p));i+=1
    # sandhi de 一 e 不 (palavras de um caractere)
    for k,(w,p) in enumerate(out):
        nxt=out[k+1] if k+1<len(out) else None
        prv=out[k-1] if k>0 else None
        if w=="一" and nxt and not (prv and prv[0][-1] in NUM) and nxt[0][0] not in NUM:
            t=4 if nxt[0][0]=="个" else tone_of(nxt[1].split()[0]);out[k]=(w,"yí" if t==4 else "yì")
        if w=="不" and nxt:
            if prv and nxt[0]==prv[0]:out[k]=(w,"bu")
            elif prv and prv[0] in ("听","看","来","做","说") :out[k]=(w,"bu")
            else:
                t=tone_of(nxt[1].split()[0]);out[k]=(w,"bú" if t==4 else "bù")
    return " ".join(p for w,p in out)
def valid_py(s):
    for w in s.strip().split():
        if pinyin_syllables(w) is None:return False
    return True
def is_py(s):
    s=s.strip()
    if not valid_py(s):return False
    return bool(re.match(r"^[A-Za-zāáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜü' ]+$",s)) and any(c in TONECH for c in s) and len(s)>=2 and not re.search(r"\b(é|à|está|não|até|lá|já)\b",s)
def annotate2(text,missing):
    res=[];pos=0
    for m in re.finditer(r'[一-鿿]+(?:[？！，…]?[一-鿿]+)*[？！]?',text):
        res.append(text[pos:m.end()]);pos=m.end()
        after=text[pos:]
        p=py_list(m.group(0).replace("…",""))
        if p is None:missing.add(m.group(0));continue
        # pinyin solto logo depois: transforma em parênteses
        loose=re.match(r"^ ([A-Za-zāáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜü']+(?: [a-zāáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜü']+)?)",after)
        if loose and is_py(loose.group(1)) and loose.group(1) not in ("é",):
            # só a parte que é pinyin (até palavra portuguesa)
            words=loose.group(1).split(" ");keep=[]
            for w in words:
                if is_py(w):keep.append(w)
                else:break
            if keep:
                seg=" "+" ".join(keep);pos+=len(seg)
                par2=re.match(r"^ ?\(([^)]*)\)",text[pos:])
                if par2:res.append(" ("+" ".join(keep)+", "+par2.group(1)+")");pos+=par2.end()
                else:res.append(" ("+" ".join(keep)+")")
                continue
        par=re.match(r"^ ?\(([^)]*)\)",after)
        if par:
            inner=par.group(1)
            head=inner.split(",")[0].split("=")[0].strip()
            if is_py(head) or head.lower()==p.lower():continue
            res.append(f" ({p}, {inner})");pos+=par.end();continue
        res.append(f" ({p})")
    res.append(text[pos:]);return "".join(res)
WORDS.update({"哪儿":"nǎr","他们":"tāmen","你们":"nǐmen","陈老师":"Chén lǎoshī","王明":"Wáng Míng","葡萄牙":"Pútáoyá","关系":"guānxi"})
