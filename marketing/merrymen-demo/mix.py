import json,wave,subprocess,numpy as np
SR=48000;N=SR*60
L=json.load(open('vo/layout.json'))
def rd(f):
    w=wave.open(f);x=np.frombuffer(w.readframes(w.getnframes()),np.int16).astype(float)/32768
    return x.reshape(-1,w.getnchannels()),w.getframerate()
voice=np.zeros(N)
for l in L:
    x,sr=rd(f"vo/l{l['i']:02d}.wav"); a,b=l['trim']
    seg=f"vo/s{l['i']:02d}.wav"
    w=wave.open(seg,'wb');w.setnchannels(1);w.setsampwidth(2);w.setframerate(sr);w.writeframes((x[a:b,0]*32767).astype(np.int16).tobytes());w.close()
    if l['who']=='M' and l['A']<12.5:   # Marcus on the phone
        fx="highpass=f=320,lowpass=f=3400,acompressor=threshold=0.1:ratio=4,volume=1.6"
    elif l['who']=='M':                   # Marcus on speakerphone / video call
        fx="highpass=f=140,lowpass=f=7000,acompressor=threshold=0.15:ratio=3,volume=1.3"
    else:                                 # trader, in the room
        fx="highpass=f=85,equalizer=f=3000:t=q:w=1:g=3,acompressor=threshold=0.15:ratio=3,aecho=0.8:0.5:35:0.12,volume=1.25"
    o=f"vo/p{l['i']:02d}.wav"
    subprocess.run(['ffmpeg','-y','-v','error','-i',seg,'-af',f"atempo={l['tempo']},{fx},aresample={SR}",'-ac','1',o],check=True)
    y,_=rd(o); y=y[:,0]; s=int(l['A']*SR); e=min(N,s+len(y)); voice[s:e]+=y[:e-s]
    l['B_real']=l['A']+len(y)/SR
m,_=rd('music.wav')
# duck music under dialogue
act=(np.abs(voice)>0.01).astype(float)
k=int(.25*SR); act=np.convolve(act,np.ones(k)/k,'same'); act=np.clip(act*4,0,1)
duck=1-0.62*act
mix=m*duck[:,None]*0.9 + np.stack([voice,voice],1)*0.95
mix/=max(1,np.abs(mix).max()/0.97)
w=wave.open('score.wav','wb');w.setnchannels(2);w.setsampwidth(2);w.setframerate(SR);w.writeframes((mix*32767).astype(np.int16).tobytes());w.close()
for l in L: print(l['i'], l['who'], round(l['A'],2), round(l['B'],2), round(l['B_real'],2))
