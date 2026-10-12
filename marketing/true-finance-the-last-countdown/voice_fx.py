# Process each line (tempo, character EQ/space), save a 60 fps loudness envelope for jaw animation, and build the dialogue stem.
import json,wave,subprocess,numpy as np
SR=48000; N=SR*60
T=json.load(open('vo/timeline.json')); L=T['lines']
FX={'M':"highpass=f=85,equalizer=f=3000:t=q:w=1:g=2,acompressor=threshold=0.15:ratio=3,aecho=0.8:0.4:28:0.10,volume=1.3",
    'E':"highpass=f=110,equalizer=f=3500:t=q:w=1:g=2,acompressor=threshold=0.15:ratio=3,aecho=0.8:0.4:28:0.10,volume=1.35",
    'C':"highpass=f=340,lowpass=f=3300,acompressor=threshold=0.1:ratio=5,volume=1.7",
    'N':"highpass=f=50,equalizer=f=120:t=q:w=1:g=3,acompressor=threshold=0.12:ratio=3,aecho=0.8:0.6:60|110:0.25|0.15,volume=1.4"}
def rd(f):
    w=wave.open(f);x=np.frombuffer(w.readframes(w.getnframes()),np.int16).astype(float)/32768;return x.reshape(-1,w.getnchannels()),w.getframerate()
voice=np.zeros(N); env={}
for l in L:
    x,sr=rd(f"vo/raw{l['i']:02d}.wav"); a,b=l['trim']; seg=f"vo/s{l['i']:02d}.wav"
    w=wave.open(seg,'wb');w.setnchannels(1);w.setsampwidth(2);w.setframerate(sr);w.writeframes((x[a:b,0]*32767).astype(np.int16).tobytes());w.close()
    o=f"vo/p{l['i']:02d}.wav"
    subprocess.run(['ffmpeg','-y','-v','error','-i',seg,'-af',f"atempo={l['tempo']},{FX[l['who']]},aresample={SR}",'-ac','1',o],check=True)
    y,_=rd(o);y=y[:,0];s=int(l['A']*SR);e=min(N,s+len(y));voice[s:e]+=y[:e-s]
    hop=SR//60; fr=[float(np.sqrt(np.mean(y[i:i+hop]**2))) for i in range(0,len(y),hop)]
    m=max(fr) or 1; env[l['i']]=[round(min(1,v/m*1.3),3) for v in fr]
json.dump(env,open('vo/env.json','w'))
w=wave.open('vo/dialogue.wav','wb');w.setnchannels(1);w.setsampwidth(2);w.setframerate(SR);w.writeframes((np.clip(voice,-1,1)*32767).astype(np.int16).tobytes());w.close()
print('ok', len(env))
