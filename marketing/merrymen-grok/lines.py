# "Now in Grok" — a 60 s Merrymen × Grok demo. M = Marcus, T = the trader.
# Every product claim is from merrymen.si/grok (captured 16 Oct 2026). Screens are real captures.
# Shot: img = capture (cap/*.jpg); a/b = camera [cx, cy, zoom] start -> end; hl = highlight boxes [x0,y0,x1,y1]; cu = close-up; cold = opening scene.
CHAPTERS={1:'The problem',2:'Merrymen × Grok',3:'Set it up',4:'Just ask',5:'Your rules'}
def S(img,a,b,hl=(),q=None): return dict(img=img,a=a,b=b,hl=list(hl),q=q)
def CU(who): return dict(cu=who)
LINES=[
 (0,'T',"I ask Grok everything. Markets, news, what's moving.",None,dict(cold=1)),
 (0,'M',"And then?",None,dict(cold=1)),
 (0,'T',"Then I close the chat, and do the trading myself.",None,dict(cold=2)),
 (0,'M',"Not anymore. Your Merryman just moved into Grok.",None,dict(cold=3)),
 (2,'M',"Merrymen times Grok. Your trading agent, right in the conversation.","Merrymen × Grok. Your trading agent, right in the conversation.",
   S('hero',[.5,.5,1.0],[.32,.36,1.6],[[.14,.26,.50,.46]])),
 (3,'M',"Add Merrymen to Grok as a custom connector, once. No model API key needed.",None,
   S('steps',[.5,.4,1.15],[.5,.45,1.35],[[.14,.32,.40,.40],[.428,.565,.858,.64]])),
 (3,'M',"Sign in, and choose which Merryman and permissions Grok can see.",None,S('step3',[.5,.2,1.2],[.5,.2,1.35],[[.14,.10,.86,.29]])),
 (3,'T',"Then what do I type?",None,CU('T')),
 (3,'M',"Set up a practice Merryman for me.",None,S('hero',[.72,.45,1.7],[.72,.42,2.2],[[.635,.37,.835,.425]])),
 (3,'M',"Grok prepares the setup. You review it, and sign the limits in Merrymen.",None,S('hero',[.72,.5,1.8],[.72,.6,1.9],[[.605,.48,.85,.60],[.605,.62,.85,.68]])),
 (4,'T',"What remains before my Merryman is running?",None,S('convo',[.5,.3,1.2],[.68,.2,1.7],[[.53,.12,.86,.23]])),
 (4,'T',"Why hasn't my agent traded?",None,S('convo',[.68,.25,1.7],[.68,.3,1.8],[[.53,.24,.86,.35]])),
 (4,'M',"And it shows you the receipts. Practice and live, kept separate.",None,S('convo',[.68,.35,1.7],[.68,.42,1.8],[[.53,.36,.86,.47]])),
 (4,'T',"Wait. Can Grok move my money?",None,CU('T')),
 (5,'M',"No. The connector can't sign wallet transactions, or loosen your signed limits.",None,
   S('rules',[.5,.3,1.3],[.68,.28,1.7],[[.53,.31,.86,.365]])),
 (5,'M',"Your Merryman still trades inside the wall you signed. And you can disconnect any time.",None,S('rules',[.68,.28,1.7],[.68,.3,1.8],[[.53,.21,.86,.365]])),
 (5,'T',"So Grok is the conversation. The wall is still mine.",None,CU('T')),
 (5,'M',"The conversation changes. Your control doesn't.",None,S('rules',[.3,.26,1.5],[.28,.25,1.9],[[.14,.17,.42,.33]])),
 (6,'T',"You should've shown me this sooner.",None,dict(end=1)),
]
