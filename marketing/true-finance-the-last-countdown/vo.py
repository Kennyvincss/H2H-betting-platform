import json,subprocess,wave,numpy as np,sys
sys.path.insert(0,'.'); from lines import LINES
V='../voices/'
CFG={'M':(V+'en-us-ryan-high/en-us-ryan-high.onnx',None,.88,1.14),
     'E':(V+'en-us-libritts-high/en-us-libritts-high.onnx','250',.92,1.14),
     'C':(V+'en-gb-alan-low/en-gb-alan-low.onnx',None,.92,1.12),
     'N':(V+'en-us-libritts-high/en-us-libritts-high.onnx','800',1.05,0.94)}
out=[]
for i,row in enumerate(LINES):
    sc,who,txt=row[:3]; disp=row[3] if len(row)>3 else None
    m,spk,ls,tempo=CFG[who]; f=f'vo/raw{i:02d}.wav'
    cmd=['python3','-m','piper','-m',m,'--length-scale',str(ls),'-f',f]+(['-s',spk] if spk else [])
    subprocess.run(cmd,input=txt.encode(),capture_output=True,check=True)
    w=wave.open(f);x=np.frombuffer(w.readframes(w.getnframes()),np.int16).astype(float);sr=w.getframerate()
    e=np.convolve(np.abs(x),np.ones(256)/256,'same');idx=np.where(e>400)[0];a,b=max(0,idx[0]-int(.03*sr)),min(len(x),idx[-1]+int(.06*sr))
    out.append(dict(i=i,scene=sc,who=who,txt=txt,disp=disp,sr=sr,trim=[int(a),int(b)],tempo=tempo,dur=(b-a)/sr/tempo))
    print(i,sc,who,'%.2f'%out[-1]['dur'],txt[:60])
json.dump(out,open('vo/lines.json','w'),indent=1)
print('total speech %.1f'%sum(o['dur'] for o in out))
