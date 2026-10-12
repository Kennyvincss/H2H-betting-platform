# Lay the voiced lines onto the 60 s timeline and derive scene boundaries for the picture.
import json
L=json.load(open('vo/lines.json'))
OPEN=1.35; G_SAME=.14; G_SPK=.2; G_SCENE=.3; BILLBOARD=1.1; DIM=.55; BLACK=2.0; PRE_N=.45
t=OPEN; scenes={}
for i,l in enumerate(L):
    if i>0:
        p=L[i-1]
        if l['scene']!=p['scene']:
            t+=G_SCENE
            if p['scene']==3: t+=BILLBOARD           # silent beat at the billboard
            if l['scene']==6: t+=DIM+BLACK+PRE_N        # lights dim, 2 s of black, the pulse, then the narrator
        else: t+=G_SAME if l['who']==p['who'] else G_SPK
    l['A']=round(t,3); l['B']=round(t+l['dur'],3); t=l['B']
    sc=scenes.setdefault(l['scene'],{'first':l['A'],'last':l['B']}); sc['last']=l['B']
# scene picture boundaries
S={}
S[1]=[0.0, scenes[2]['first']-.15]
S[2]=[S[1][1], scenes[3]['first']-.15]
S[3]=[S[2][1], scenes[3]['last']+BILLBOARD+.15]
S[4]=[S[3][1], scenes[5]['first']-.15]
S[5]=[S[4][1], scenes[5]['last']+DIM]
S[6]=[S[5][1], 60.0]
out={'lines':L,'scenes':{k:v for k,v in S.items()},'billboard':scenes[3]['last']+.15,'black':S[5][1],'narr':L[-1]['A'],'narrEnd':L[-1]['B']}
json.dump(out,open('vo/timeline.json','w'),indent=1)
for l in L: print(f"{l['i']:2d} s{l['scene']} {l['who']} {l['A']:6.2f}-{l['B']:6.2f} {l['txt'][:55]}")
print({k:[round(a,2),round(b,2)] for k,(a,b) in S.items()}, 'title hold after narrator: %.2f s'%(60-L[-1]['B']))
