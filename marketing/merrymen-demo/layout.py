# Trim each voice line, apply tempo, and lay the dialogue out over 60s.
# Writes vo/layout.json (line timings) and vo/warp.json (new-time -> film-time map used by film.html).
import json,wave,numpy as np
L=json.load(open('vo/lines.json'))
TEMPO={'M':1.08,'T':1.10}
for l in L:
    w=wave.open(f"vo/l{l['i']:02d}.wav");x=np.frombuffer(w.readframes(w.getnframes()),np.int16).astype(float);sr=w.getframerate()
    e=np.convolve(np.abs(x),np.ones(256)/256,'same'); idx=np.where(e>400)[0]
    a,b=max(0,idx[0]-int(.03*sr)),min(len(x),idx[-1]+int(.06*sr))
    l['trim']=[int(a),int(b)]; l['sr']=sr; l['tempo']=TEMPO[l['who']]; l['tdur']=(b-a)/sr/l['tempo']
speech=sum(l['tdur'] for l in L); lead=2.4; tail=3.5
gaps=[.2 if L[i]['who']==L[i+1]['who'] else .16 for i in range(len(L)-1)]
gaps[3]=.25; gaps[9]=.35; gaps[17]=1.6; gaps[20]=.6   # beats: "...Merrymen", demo start, market crash, laptop close
scale=(60-lead-tail-speech)/sum(gaps); gaps=[g*scale for g in gaps]
t=lead
for i,l in enumerate(L):
    l['A']=round(t,3); l['B']=round(t+l['tdur'],3); t=l['B']+(gaps[i] if i<len(gaps) else 0)
json.dump(L,open('vo/layout.json','w'),indent=1)
pts=[(0,0)]+[p for l in L for p in ((l['A'],l['a']),(l['B'],l['b']))]+[(60,60)]
json.dump(pts,open('vo/warp.json','w'))
