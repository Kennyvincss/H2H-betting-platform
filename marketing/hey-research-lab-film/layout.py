# Lay the voiced lines on the timeline; a chapter card sits in the gap before each chapter.
import json
L=json.load(open('vo/lines.json'))
OPEN=2.2; G_SAME=.22; G_SPK=.3; G_CHAP=1.7; PRE_END=1.2
t=OPEN; chap={}
for i,l in enumerate(L):
    if i>0:
        p=L[i-1]
        if l['scene']!=p['scene']: t+=G_CHAP if l['scene']<11 else PRE_END; chap[l['scene']]=round(t-(G_CHAP if l['scene']<11 else PRE_END)+.1,3)
        else: t+=G_SAME if l['who']==p['who'] else G_SPK
    l['A']=round(t,3); l['B']=round(t+l['dur'],3); t=l['B']
# each line's picture runs from just before it starts until just before the next one starts
for i,l in enumerate(L):
    l['PA']=L[i-1]['PB'] if i>0 and L[i-1]['scene']==l['scene'] else round(l['A']-.15,3)
    l['PB']=round(L[i+1]['A']-.15,3) if i+1<len(L) and L[i+1]['scene']==l['scene'] else round(l['B']+.25,3)
END=round(L[-1]['B']+4.2,2)
json.dump({'lines':L,'chap':chap,'end':END},open('vo/timeline.json','w'),indent=1)
print('END',END,'chapters',chap)
