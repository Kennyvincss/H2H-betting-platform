import re,json,subprocess,wave,sys
src=open('film.html').read()
block=src[src.index('const LINES=['):src.index('];',src.index('const LINES=['))]
rows=re.findall(r"\[([\d.]+),([\d.]+),'([^']+)',(M|T),'(.*?)'\],",block)
V='voices/'; out=[]
ls=float(sys.argv[1]) if len(sys.argv)>1 else 1.0
for i,(a,b,who,c,text) in enumerate(rows):
    txt=re.sub(r'<br>',' ',text).replace('“','').replace('”','').replace('…','... ')
    txt=txt.replace('Merrymen','Merry-men')
    f=f'vo/l{i:02d}.wav'
    if c=='M': cmd=['python3','-m','piper','-m',V+'en-us-libritts-high/en-us-libritts-high.onnx','-s','400','--length-scale',str(ls*.9),'-f',f]
    else: cmd=['python3','-m','piper','-m',V+'en-us-ryan-high/en-us-ryan-high.onnx','--length-scale',str(ls*.86),'-f',f]
    subprocess.run(cmd,input=txt.encode(),capture_output=True,check=True)
    w=wave.open(f);d=w.getnframes()/w.getframerate()
    out.append(dict(i=i,a=float(a),b=float(b),who=c,dur=round(d,2),slot=round(float(b)-float(a),2),txt=txt))
    print(f"{i:2d} {c} slot {float(b)-float(a):4.1f}  vo {d:4.2f}  {'OVER' if d>float(b)-float(a)-0.05 else ''}  {txt}")
json.dump(out,open('vo/lines.json','w'),indent=1)
