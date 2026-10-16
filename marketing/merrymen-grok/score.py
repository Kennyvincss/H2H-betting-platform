# Original score + UI sound design for the HEY explainer, laid on the timeline; dialogue mixed on top with ducking.
import json,wave,numpy as np
import sys; sys.path.insert(0,'.'); from lines import LINES
TL=json.load(open('vo/timeline.json')); L=TL['lines']
for l,row in zip(L,LINES): l['shot']=row[4]
CH={int(k):v for k,v in TL['chap'].items()}
SR=48000; END=TL['end']; N=int(SR*END); t=np.arange(N)/SR; rs=np.random.default_rng(7); noise=rs.standard_normal(N)
Lc=np.zeros(N); Rc=np.zeros(N)
def lp(x,a):
    from scipy.signal import lfilter
    return lfilter([a],[1,-(1-a)],x)
def env(a,b,fi,fo): return np.clip((t-a)/max(fi,1e-3),0,1)*np.clip((b-t)/max(fo,1e-3),0,1)
def add(sig,pan=0,g=1.):
    global Lc,Rc; Lc+=sig*g*(1-pan); Rc+=sig*g*(1+pan)
def put(fn,t0,dur,g=1.,pan=0.):
    s0=int(t0*SR); s1=min(N,int((t0+dur)*SR))
    if s0>=N or s1<=0: return
    x=np.arange(s1-s0)/SR; y=fn(x)*g; Lc[s0:s1]+=y*(1-pan); Rc[s0:s1]+=y*(1+pan)
HN=noise-lp(noise,.4)
cold_end=L[2]['B']+.25; last=L[-1]; endA=L[-2]['PB']
# --- cold open: noisy, anxious market hum, ticking hats; resolves when Nico speaks
hum=np.sin(2*np.pi*55*t)+.5*np.sin(2*np.pi*82.4*t+np.sin(2*np.pi*.3*t))+.3*lp(noise,.02)*4
add(hum*env(0,cold_end,1.2,.6)*.12)
for k,tt in enumerate(np.arange(.5,L[2]['A'],60/128/2)): put(lambda x: HN[:len(x)]*np.exp(-x*300),tt,.04,.05+.03*(k%2),(-1)**k*.4)
# --- chord bed: minor-ish progression, warm saw pads, one chord per 4 bars (bpm 96)
bpm=96; beat=60/bpm; bar=4*beat
prog=[[110.0,130.8,164.8],[87.3,110.0,130.8],[130.8,164.8,196.0],[98.0,123.5,146.8]]   # Am F C G
pad=np.zeros(N)
start=L[2]['A']
for j,b0 in enumerate(np.arange(start,endA,bar*2)):
    fs=prog[j%4]; m=(t>=b0)&(t<b0+bar*2+.5); x=t[m]-b0
    sig=sum(np.sin(2*np.pi*f*x)+.4*np.sin(2*np.pi*2*f*x+.3)+.2*np.sin(2*np.pi*f*1.003*x) for f in fs)/len(fs)
    e=np.clip(x/.8,0,1)*np.clip((bar*2+.5-x)/.6,0,1); pad[m]+=sig*e
add(lp(pad,.08)*.10)
# --- soft pulse: kick on 1 and 3, shaker on off-beats, bass on the root; drops out on chapter cards and close-ups
cards=[(a,L[[l['scene'] for l in L].index(k)]['A']) for k,a in CH.items() if k<11]
def in_card(x): return any(a-.05<=x<b for a,b in cards)
tt=start; i=0
while tt<endA-.2:
    if not in_card(tt):
        if i%2==0: put(lambda x: np.sin(2*np.pi*(48+70*np.exp(-x*30))*x)*np.exp(-x*10),tt,.4,.22)
        put(lambda x: HN[:len(x)]*np.exp(-x*120),tt+beat/2,.08,.035,.3*(-1)**i)
        root=prog[int((tt-start)//(bar*2))%4][0]/2
        put(lambda x: (np.sin(2*np.pi*root*x)+.3*np.sin(2*np.pi*2*root*x))*np.exp(-x*3)*np.clip(x/.01,0,1),tt,beat*.95,.10)
    tt+=beat; i+=1
# --- chapter cards: whoosh in, hit on the number
for a,b in cards:
    put(lambda x: lp(noise,.06)[:len(x)]*np.sin(np.pi*np.clip(x/.7,0,1))**2*2,a-.25,.7,.18)
    put(lambda x: np.sin(2*np.pi*(60+90*np.exp(-x*12))*x)*np.exp(-x*4)+HN[:len(x)]*np.exp(-x*30)*.3,a+.1,1.2,.45)
    put(lambda x: np.sin(2*np.pi*1320*x)*np.exp(-x*8)*.4+np.sin(2*np.pi*1980*x)*np.exp(-x*10)*.25,a+.12,.8,.12)
# --- UI: a soft tick when each highlight lands, a swish when the screen changes
for l in L:
    s=l['shot']; shots=s.get('seq',[s]) if (s.get('img') or s.get('seq')) else []
    if not shots: continue
    span=(l['PB']-l['PA'])/len(shots)
    for j,sh in enumerate(shots):
        t0=l['PA']+j*span
        put(lambda x: HN[:len(x)]*np.sin(np.pi*np.clip(x/.25,0,1))**2*.6,t0,.25,.06)
        n=len(sh['hl'])
        for h in range(n):
            th=t0+span*(.16+h*.62/n)
            put(lambda x: np.sin(2*np.pi*2200*x)*np.exp(-x*60)+np.sin(2*np.pi*3300*x)*np.exp(-x*80)*.5,th,.12,.05,.2)
        if sh.get('q'): put(lambda x: np.sin(2*np.pi*660*x)*np.exp(-x*14)*np.clip(x/.005,0,1),t0+span*.33,.4,.06)
# --- end card: riser, impact, warm final chord
put(lambda x: lp(noise,.03)[:len(x)]*(x/1.4)**2*3,endA-1.3,1.4,.2)
put(lambda x: np.sin(2*np.pi*(32+90*np.exp(-x*7))*x)*np.exp(-x*1.3)+HN[:len(x)]*np.exp(-x*25)*.4,endA+.05,3,.9)
fin=sum(np.sin(2*np.pi*f*t)+.3*np.sin(2*np.pi*2*f*t) for f in [110,164.8,220,261.6,329.6])/5
add(lp(fin,.1)*env(endA,END-.1,1.2,1.5)*.16)
for k in range(3): put(lambda x: np.sin(2*np.pi*880*x)*np.exp(-x*5)*.5,last['B']+.3+k*.35,1,.08*(1-.25*k))
# --- master: duck under dialogue
fade=np.clip((END-t)/.8,0,1)*np.clip(t/.05,0,1)
w=wave.open('vo/dialogue.wav');d=np.frombuffer(w.readframes(w.getnframes()),np.int16).astype(float)/32768;d=np.pad(d,(0,max(0,N-len(d))))[:N]
act=np.convolve((np.abs(d)>.01).astype(float),np.ones(SR//4)/(SR//4),'same');duck=1-.5*np.clip(act*4,0,1)
Lm=(Lc*duck*.8+d)*fade; Rm=(Rc*duck*.8+d)*fade
st=np.stack([Lm,Rm],1); st/=np.abs(st).max()/0.95; st=np.tanh(st*1.1)/np.tanh(1.1)
w=wave.open('mix_raw.wav','wb');w.setnchannels(2);w.setsampwidth(2);w.setframerate(SR);w.writeframes((st*32767*.9).astype(np.int16).tobytes());w.close()
print('mix ok',END)
