# Bundle the timeline, jaw envelopes and the current shot specs from lines.py for film.html.
import json
from lines import LINES,CHAPTERS
T=json.load(open('vo/timeline.json'));E=json.load(open('vo/env.json'))
for l,row in zip(T['lines'],LINES): l.pop('trim',None); l['shot']=row[4]; l['disp']=row[3]
open('vo/data.js','w').write('const TL='+json.dumps(T)+';\nconst ENV='+json.dumps(E)+';\nconst CHAPTERS='+json.dumps(CHAPTERS)+';\n')
