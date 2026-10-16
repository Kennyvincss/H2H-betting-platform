# Lay the voiced lines onto exactly 60 s: opening beat, scaled gaps, a held end card.
import json
L=json.load(open('vo/lines.json'))
END=60.0; LEAD=2.0; TAIL=3.6
gaps=[]
for i in range(len(L)-1):
    a,b=L[i],L[i+1]
    g=.18 if a['who']==b['who'] else .14
    if a['scene']!=b['scene']: g=.5
    if b['scene']==6: g=.9          # the beat before the last line on the end card
    gaps.append(g)
speech=sum(l['dur'] for l in L); scale=(END-LEAD-TAIL-speech)/sum(gaps); gaps=[g*scale for g in gaps]
t=LEAD
for i,l in enumerate(L):
    l['A']=round(t,3); l['B']=round(t+l['dur'],3); t=l['B']+(gaps[i] if i<len(gaps) else 0)
for i,l in enumerate(L):
    l['PA']=L[i-1]['PB'] if i>0 else round(l['A']-.15,3)
    l['PB']=round(L[i+1]['A']-.12,3) if i+1<len(L) else END
json.dump({'lines':L,'chap':{},'end':END},open('vo/timeline.json','w'),indent=1)
print('gap scale %.2f'%scale); [print(l['i'],l['who'],l['A'],l['B'],l['txt'][:40]) for l in L]
