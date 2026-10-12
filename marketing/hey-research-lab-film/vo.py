# Voice every line with Piper, trim silence, record durations.
import json,subprocess,wave,numpy as np,sys
sys.path.insert(0,'.'); from lines import LINES
V='../voices/'
CFG={'J':(V+'en-us-libritts-high/en-us-libritts-high.onnx','650',.95,1.08),
     'K':(V+'en-us-ryan-high/en-us-ryan-high.onnx',None,.92,1.08),
     'N':(V+'en-us-libritts-high/en-us-libritts-high.onnx','800',1.08,0.94)}
out=[]
for i,(sc,who,txt,disp,shot) in enumerate(LINES):
    m,spk,ls,tempo=CFG[who]; f=f'vo/raw{i:02d}.wav'
    cmd=['python3','-m','piper','-m',m,'--length-scale',str(ls),'-f',f]+(['-s',spk] if spk else [])
    subprocess.run(cmd,input=txt.encode(),capture_output=True,check=True)
    w=wave.open(f);x=np.frombuffer(w.readframes(w.getnframes()),np.int16).astype(float);sr=w.getframerate()
    e=np.convolve(np.abs(x),np.ones(256)/256,'same');idx=np.where(e>400)[0];a,b=max(0,idx[0]-int(.03*sr)),min(len(x),idx[-1]+int(.06*sr))
    out.append(dict(i=i,scene=sc,who=who,txt=txt,disp=disp,shot=shot,sr=sr,trim=[int(a),int(b)],tempo=tempo,dur=(b-a)/sr/tempo))
    print(i,sc,who,'%.2f'%out[-1]['dur'],txt[:50],flush=True)
json.dump(out,open('vo/lines.json','w'),indent=1)
print('total speech %.1f'%sum(o['dur'] for o in out))
