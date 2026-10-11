# Original 5s ClipRally audio signature: impact -> digital whoosh -> snap -> 3-note electronic chime.
import numpy as np, wave
SR=48000; D=5.0; N=int(SR*D); t=np.arange(N)/SR
L=np.zeros(N); R=np.zeros(N); rs=np.random.default_rng(11); noise=rs.standard_normal(N)
def lp(x,a):
    y=np.empty_like(x); acc=0.0
    for i in range(len(x)): acc+=a*(x[i]-acc); y[i]=acc
    return y
def hp(x,a): return x-lp(x,a)
def at(t0,dur): m=(t>=t0)&(t<t0+dur); return m,t[m]-t0
def put(sig_fn,t0,dur,g=1.,pan=0.):
    m,x=at(t0,dur); s=sig_fn(x)*g; L[m]+=s*(1-pan*.6); R[m]+=s*(1+pan*.6)
def verb(x,g=.25):  # tiny multi-tap room
    y=x.copy()
    for d,a in [(0.023,.5),(0.041,.4),(0.067,.32),(0.097,.25),(0.131,.18),(0.173,.12)]:
        k=int(d*SR); y[k:]+=x[:-k]*a*g/0.25*0.25
    return y
# 1) IMPACT at 0.03: sub drop + body + crack
t0=0.03
put(lambda x: np.sin(2*np.pi*(38+70*np.exp(-x*14))*x)*np.exp(-x*3.2),t0,1.2,1.0)
put(lambda x: np.sin(2*np.pi*(140*np.exp(-x*20)+60)*x)*np.exp(-x*12),t0,.4,.6)
crack=hp(noise,.35); m,x=at(t0,.25); L[m]+=crack[m]*np.exp(-x*28)*.55; R[m]+=crack[m]*np.exp(-x*30)*.55
air=lp(noise,.06); m,x=at(t0,1.1); L[m]+=air[m]*np.exp(-x*3.5)*.5; R[m]+=np.roll(air,97)[m]*np.exp(-x*3.5)*.5
# 2) glitch ticks 0.08-0.6 (digital distortion)
r=np.random.default_rng(5)
for i in range(9):
    tt=0.08+i*0.06+r.random()*0.02; f=1800+r.random()*3000
    put(lambda x,f=f: np.sign(np.sin(2*np.pi*f*x))*np.exp(-x*160),tt,.03,.10*(1-i/10),(-1)**i*.7)
# 3) WHOOSH 1.30 -> 2.00, rising filtered noise, stereo sweep
m,x=at(1.30,.72); k=x/.72
cut=np.clip(.01+.5*k**2,0,1)
y=np.zeros(m.sum()); acc=0.0; src=noise[m]
for i in range(len(src)): acc+=cut[i]*(src[i]-acc); y[i]=acc
env=(k**2.2)*np.where(k>.97,np.clip((1-k)/.03,0,1),1)
L[m]+=y*env*1.1*(1-k*.6); R[m]+=y*env*1.1*(.4+k*.6)
put(lambda x: np.sin(2*np.pi*(200+1600*(x/.7)**2)*x)*(x/.7)**3*.25,1.30,.7,.35)
# 4) SNAP at 2.00: click + punch + metallic clack
put(lambda x: np.sin(2*np.pi*(55+180*np.exp(-x*35))*x)*np.exp(-x*10),2.0,.6,.95)
m,x=at(2.0,.05); L[m]+=hp(noise,.5)[m]*np.exp(-x*220)*.7; R[m]+=hp(noise,.5)[m]*np.exp(-x*220)*.7
put(lambda x: (np.sin(2*np.pi*1180*x)+.6*np.sin(2*np.pi*1730*x)+.4*np.sin(2*np.pi*2610*x))*np.exp(-x*22),2.0,.35,.16)
# text wipe tick
put(lambda x: np.sin(2*np.pi*3200*x)*np.exp(-x*90),2.13,.06,.08,.3)
# 5) SIGNATURE chime 3.15: 3-note rising FM arpeggio A5-E6-A6, bright + sub tap
def fm(f,dec):
    return lambda x: np.sin(2*np.pi*f*x + 1.6*np.exp(-x*7)*np.sin(2*np.pi*f*2*x))*np.exp(-x*dec)*(1-np.exp(-x*400))
for i,(f,p) in enumerate([(880,-.35),(1318.5,.35),(1760,0)]):
    put(fm(f,3.4-i*.4),3.15+i*0.075,1.75-i*0.07,.30 if i<2 else .36,p)
    put(fm(f*2.003,6),3.15+i*0.075,.8,.06,-p)
put(lambda x: np.sin(2*np.pi*(70+60*np.exp(-x*30))*x)*np.exp(-x*7),3.15,.6,.45)
m,x=at(3.30,1.5); sh=hp(noise,.6); L[m]+=sh[m]*np.exp(-x*3)*.04*np.sin(2*np.pi*14*x)**2; R[m]+=np.roll(sh,53)[m]*np.exp(-x*3)*.04*np.cos(2*np.pi*14*x)**2
# room + master
L=verb(L); R=verb(R)
mx=max(np.abs(L).max(),np.abs(R).max()); L/=mx/0.89; R/=mx/0.89
st=np.tanh(np.stack([L,R],1)*1.15)/np.tanh(1.15)
st[-int(.008*SR):]*=np.linspace(1,0,int(.008*SR))[:,None]   # declick at the hard cut
w=wave.open('sig.wav','wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((st*32767*.87).astype(np.int16).tobytes()); w.close()
print('ok')
