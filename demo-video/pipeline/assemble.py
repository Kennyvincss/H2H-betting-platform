import json, subprocess, re, os
R='../rec/clips/'; os.makedirs('seg',exist_ok=True)
T=json.load(open('timing.json'))
def run(c): subprocess.run(c,shell=True,check=True)
def ts(t):
    h=int(t//3600); m=int(t%3600//60); s=t%60; return f"{h:02}:{m:02}:{s:06.3f}".replace('.',',')
def chunks(text, maxc=70):
    parts=re.split(r'(?<=[.,:;])\s+',text); out=[]; cur=''
    for p in parts:
        if cur and len(cur)+1+len(p)>maxc: out.append(cur); cur=p
        else: cur=(cur+' '+p).strip()
    if cur: out.append(cur)
    res=[]
    for c in out:   # hard-wrap any still-too-long chunk on word boundaries
        while len(c)>maxc+15:
            k=c.rfind(' ',0,maxc); res.append(c[:k]); c=c[k+1:]
        res.append(c)
    return res
t=0.0; srt=[]; n=1; lst=[]
for s in T:
    j=json.load(open(R+s['id']+'.json'))
    need=j['used']+0.2; L=round(min(max(j['dur'],need), j['dur']+1.5),2); sp=max(1.0, need/L); src=round(L*sp,2)
    out=f"seg/{s['id']}.mp4"
    run(f"ffmpeg -loglevel error -y -ss {j['ready']:.2f} -t {src} -i {R}{s['id']}.webm -i vo/{s['id']}.wav -filter_complex "
        f"\"[0:v]setpts=PTS/{sp:.4f},fps=30,scale=1920:1080,setsar=1,format=yuv420p[v];[1:a]aresample=48000,apad,atrim=0:{L}[a]\" "
        f"-map [v] -map [a] -t {L} -c:v libx264 -preset medium -crf 18 -c:a aac -b:a 192k -ar 48000 -ac 2 {out}")
    d=float(subprocess.check_output(f"ffprobe -v error -show_entries format=duration -of csv=p=0 {out}",shell=True))
    cs=chunks(s['text']); tot=sum(len(c) for c in cs); a=t+0.05
    for c in cs:
        b=a+s['dur']*len(c)/tot
        srt.append(f"{n}\n{ts(a)} --> {ts(b-0.04)}\n{c}\n"); n+=1; a=b
    lst.append(f"file '{out}'"); print(s['id'], 'len', round(d,2), 'speed', round(sp,2)); t+=d
open('list.txt','w').write('\n'.join(lst)+'\n'); open('neatspace-demo.srt','w').write('\n'.join(srt))
print('TOTAL', round(t,2))
