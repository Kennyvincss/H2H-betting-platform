# Original score + sound design for "The Last Countdown", laid on the scene timeline.
import json,wave,numpy as np
TL=json.load(open('vo/timeline.json')); S={int(k):v for k,v in TL['scenes'].items()}; L=TL['lines']
SR=48000; END=TL['end']; N=int(SR*END); t=np.arange(N)/SR; rs=np.random.default_rng(3); noise=rs.standard_normal(N)
Lc=np.zeros(N); Rc=np.zeros(N)
def lp(x,a):
    y=np.empty_like(x); acc=0.0
    for i in range(len(x)): acc+=a*(x[i]-acc); y[i]=acc
    return y
def env(a,b,fi,fo): return np.clip((t-a)/max(fi,1e-3),0,1)*np.clip((b-t)/max(fo,1e-3),0,1)
def add(sig,pan=0,g=1.):
    global Lc,Rc; Lc+=sig*g*(1-pan); Rc+=sig*g*(1+pan)
def put(fn,t0,dur,g=1.,pan=0.):
    m=(t>=t0)&(t<t0+dur); x=t[m]-t0; s=np.zeros(N); s[m]=fn(x)*g; add(s,pan)
LN=lp(noise,.05); HN=noise-lp(noise,.4)
BB=TL['billboard']; BLACK=TL['black']; PULSE=BLACK+2.0; NE=TL['narrEnd']
silent=1-env(BB,S[3][1],.03,.25)*1.0                 # the billboard silence
silent*=1-env(BLACK,PULSE,.05,.05)                    # two seconds of black silence
# --- rain + thunder (S1-S3), softer behind glass indoors
rain=(lp(noise,.35)*.6+HN*.15)
rainLvl=env(0,1.5,.3,.2)*1.0+env(1.5,S[2][1],.2,.3)*.35+env(S[3][0],BB,.3,.05)*1.0+env(BB,S[3][1],.1,.3)*.25
add(rain*rainLvl*.06*silent,.1); add(np.roll(rain,4800)*rainLvl*.06*silent,-.1)
for t0 in (.47,.62,5.0,17.5): put(lambda x: lp(noise,.01)[:len(x)]*8*np.exp(-x*1.4)*np.clip(x/.08,0,1),t0,2.5,.35)
# --- tension drone, building score
drone=np.sin(2*np.pi*43.65*t)+.6*np.sin(2*np.pi*65.4*t)+.3*np.sin(2*np.pi*87.3*t+np.sin(2*np.pi*.2*t))
add(drone*(env(0,S[2][0],1.5,.5)*.14+env(S[2][0],S[3][1],.5,.2)*.18+env(S[3][1],S[5][1],.3,.1)*.22)*silent)
def chord(fs,a,b,g,fi=1.,fo=.5,bright=.35):
    sig=sum(np.sin(2*np.pi*f*t)+bright*np.sin(2*np.pi*2*f*t)+.15*np.sign(np.sin(2*np.pi*f*t)) for f in fs)/len(fs)
    add(lp(sig,.15)*env(a,b,fi,fo)*g*silent)
Dm=[146.8,174.6,220.0]; Bb=[116.5,146.8,174.6]; F_=[174.6,220.0,261.6]; C_=[130.8,164.8,196.0]
chord(Dm,S[2][0],S[2][1],.10,2); chord(Bb,S[3][0],BB,.12,1.5,.05)
chord(Dm,S[4][0],S[4][0]+6,.14,.8); chord(Bb,S[4][0]+6,S[4][1],.16,.5)
chord(F_,S[5][0],S[5][0]+4,.2,.4); chord(C_,S[5][0]+4,S[5][1],.24,.3,.05,.5)
# --- pulses and percussion
bpm=100; beat=60/bpm
def kick(t0,g=1,f=50,top=110): put(lambda x: np.sin(2*np.pi*(f+top*np.exp(-x*25))*x)*np.exp(-x*9),t0,.5,g)
def tom(t0,g=1,f=70): put(lambda x: np.sin(2*np.pi*(f+60*np.exp(-x*20))*x)*np.exp(-x*6)+lp(noise,.08)[:len(x)]*np.exp(-x*20)*.4,t0,.8,g)
tt=S[2][0]+1
while tt<S[3][1]:
    if not (BB-.05<tt<S[3][1]): kick(tt,.35)
    tt+=beat
tt=S[4][0]; i=0
while tt<S[5][1]-.2:
    tom(tt,.5 if i%4==0 else .3, 65 if i%2==0 else 80); 
    if tt>S[5][0]: kick(tt+beat/2,.3)
    tt+=beat/(1 if tt<S[5][0] else 2); i+=1
# braams
for t0 in (S[4][0]+.05, S[5][0]+.05): put(lambda x: lp(np.sign(np.sin(2*np.pi*55*x))+np.sign(np.sin(2*np.pi*55.6*x)),.05)*np.exp(-x*1.2)*np.clip(x/.05,0,1),t0,2.5,.18)
# --- UI and story sounds
put(lambda x: np.sin(2*np.pi*1760*x)*np.exp(-x*12)+np.sin(2*np.pi*2637*x)*np.exp(-x*16)*.6,1.6,.4,.18)        # encrypted message
for k in range(14): put(lambda x: HN[:len(x)]*np.exp(-x*500),1.9+k*.085,.03,.12,(-1)**k*.3)                   # decrypt glitches
put(lambda x: np.sin(2*np.pi*(1800*np.exp(-x*30)+60)*x)*np.exp(-x*40),1.62,.08,.15)                            # light flicker buzz
tp=L[3]['A']+1.3
while tp<L[4]['A']-.1: put(lambda x: np.sin(2*np.pi*2400*x)*np.exp(-x*120),tp,.05,.08); tp+=1.6                  # tablet taps
for k,t0 in enumerate(np.arange(S[3][0]+.3,BB-.4,1.25)):                                                          # traffic pass-bys
    put(lambda x: lp(noise,.08)[:len(x)]*np.sin(np.pi*x/1.4)**2*1.5,t0,1.4,.25,-.8+1.6*(k%2))
put(lambda x: np.sin(2*np.pi*425*x)*(np.sin(2*np.pi*25*x)>0)*.5,L[9]['B']+.05,.25,.08)                            # call ended tone
tap=[l for l in L if l['scene']==4][4]['A']-.25; put(lambda x: np.sin(2*np.pi*1200*x)*np.exp(-x*30)+lp(noise,.3)[:len(x)]*np.exp(-x*60)*.4,tap,.3,.2)
put(lambda x: (np.sin(2*np.pi*(300+900*x)*x))*np.sin(np.pi*x/.6)**2,tap+.05,.6,.08)                               # screens unify sweep
for k in range(int(S[5][1]-S[5][0])): put(lambda x: np.sin(2*np.pi*3000*x)*np.exp(-x*200)+HN[:len(x)]*np.exp(-x*900)*.3,S[5][0]+k,.03,.12)  # clock ticks
put(lambda x: lp(noise,.03)[:len(x)]*(x/1.2)**2*3,S[5][1]-1.25,1.2,.25)                                              # riser
put(lambda x: np.sin(2*np.pi*(30+80*np.exp(-x*8))*x)*np.exp(-x*1.6)+HN[:len(x)]*np.exp(-x*40)*.3,S[5][1]-.05,1.8,1.0)  # impact before the reveal
# --- final reveal: electronic pulse, orchestral finale, one deep impact, silence
for k in range(5): put(lambda x: np.sin(2*np.pi*55*x)*np.exp(-x*8)+np.sin(2*np.pi*880*x)*np.exp(-x*30)*.15,PULSE+k*.6,.5,.35*(1-k*.12))
fin=sum(np.sin(2*np.pi*f*t)+.3*np.sin(2*np.pi*2*f*t) for f in [73.4,110,146.8,174.6,220,293.7])/6
add(lp(fin,.12)*env(PULSE+.8,END-.1,1.6,.6)*.28)
put(lambda x: np.sin(2*np.pi*(28+90*np.exp(-x*7))*x)*np.exp(-x*1.1)+lp(noise,.04)[:len(x)]*np.exp(-x*2)*.6,NE+.1,2.8,1.1)
# --- music/effects stem only (dialogue is mixed on top in ffmpeg with sidechain ducking)
fade=np.clip((END-t)/.6,0,1)
st=np.stack([Lc*fade,Rc*fade],1); st/=np.abs(st).max()/0.9; st=np.tanh(st*1.1)/np.tanh(1.1)
w=wave.open('music.wav','wb');w.setnchannels(2);w.setsampwidth(2);w.setframerate(SR);w.writeframes((st*32767*.9).astype(np.int16).tobytes());w.close()
print('ok')
# --- master: duck the music under dialogue, add dialogue, write the mix
w=wave.open('vo/dialogue.wav');d=np.frombuffer(w.readframes(w.getnframes()),np.int16).astype(float)/32768;d=np.pad(d,(0,max(0,N-len(d))))[:N]
act=np.convolve((np.abs(d)>.01).astype(float),np.ones(SR//4)/(SR//4),'same');duck=1-.55*np.clip(act*4,0,1)
Lm=(Lc*duck+d*.95)*fade; Rm=(Rc*duck+d*.95)*fade
st=np.stack([Lm,Rm],1); st/=np.abs(st).max()/0.95; st=np.tanh(st*1.15)/np.tanh(1.15)
w=wave.open('mix_raw.wav','wb');w.setnchannels(2);w.setsampwidth(2);w.setframerate(SR);w.writeframes((st*32767*.9).astype(np.int16).tobytes());w.close()
print('mix ok')
