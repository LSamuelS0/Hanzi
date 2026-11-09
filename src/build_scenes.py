import json,subprocess,os,sys,re
sys.path.insert(0,'.')
from scenes import W,P
R='dl/twe'
ems=set()
for v in W.values():ems.add(v.split()[1])
for k,v in P:
    for p in v.split("|"):ems.add(p.split()[1])
names=set(subprocess.run(["git","ls-tree","--name-only","HEAD","assets/svg/"],cwd=R,capture_output=True,text=True).stdout.split())
def fn(e):
    cps=[f"{ord(c):x}" for c in e]
    for cand in ["-".join(cps),"-".join(c for c in cps if c!="fe0f")]:
        if f"assets/svg/{cand}.svg" in names:return f"assets/svg/{cand}.svg"
    return None
miss=[e for e in ems if not fn(e)];print("sem imagem:",miss)
paths=[fn(e) for e in ems if fn(e)]
subprocess.run(["git","-c","gc.auto=0","checkout","HEAD","--"]+paths,cwd=R,check=True,capture_output=True)
out={e:open(os.path.join(R,fn(e))).read().strip() for e in ems if fn(e)}
json.dump(out,open("emoji.json","w"),ensure_ascii=False,separators=(",",":"))
c=json.load(open("ctest.json"))
c["wimg"]={k:v.split() for k,v in W.items() if v.split()[1] in out}
c["pscene"]=[[k,[p.split() for p in v.split("|") if p.split()[1] in out]] for k,v in P]
json.dump(c,open("ctest.json","w"),ensure_ascii=False)
print(len(out),"imagens",os.path.getsize("emoji.json"),"bytes")
