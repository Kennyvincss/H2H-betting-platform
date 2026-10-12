# Original 5s audio signature for "One clip. Everywhere.":
# glass crack -> burst -> accelerating fly-by whooshes -> suction -> deep impact -> sweep shimmer -> digital finish.
import numpy as np, wave
SR=48000; N=int(SR*5.0); t=np.arange(N)/SR
L=np.zeros(N); R=np.zeros(N); rs=np.random.default_rng(23); noise=rs.standard_normal(N)
def lp(x,a):
    y=np.empty_like(x); acc=0.0
    for i in range(len(x)): acc+=a*(x[i]-acc); y[i]=acc
    return y
def hp(x,a): return x-lp(x,a)
def win(t0,dur): m=(t>=t0)&(t<t0+dur); return m,t[m]-t0
def put(fn,t0,dur,g=1.,pan=0.):
    m,x=win(t0,dur); s=fn(x)*g; L[m]+=s*(1-pan); R[m]+=s*(1+pan)
HN=hp(noise,.55)
# 1) GLASS CRACK at 0.10: hard transient, crackle grains, glassy tinkles
put(lambda x: HN[:len(x)]*np.exp(-x*90),0.10,.12,.9)
put(lambda x: np.sin(2*np.pi*(90+300*np.exp(-x*40))*x)*np.exp(-x*18),0.10,.3,.55)
g=np.random.default_rng(4)
for i in range(38):
    t0=0.10+abs(g.normal(0,.07)); f=3500+g.random()*6500; pan=g.uniform(-.8,.8)
    put(lambda x,f=f: (np.sin(2*np.pi*f*x)+.5*np.sin(2*np.pi*f*1.53*x))*np.exp(-x*(60+g.random()*80)),t0,.09,.07*(1-i/45),pan)
for i in range(60):   # crackle grains
    t0=0.10+g.random()*.28; put(lambda x: HN[:len(x)]*np.exp(-x*900),t0,.008,.25*np.exp(-(t0-.1)*6),g.uniform(-.9,.9))
# 2) SHATTER BURST at 0.40: wide noise swell + low thump
m,x=win(.38,.6); b=lp(noise,.12)[m]; e=np.clip(x/.04,0,1)*np.exp(-x*5.5); L[m]+=b*e*.9; R[m]+=np.roll(lp(noise,.12),311)[m]*e*.9
put(lambda x: np.sin(2*np.pi*(60+90*np.exp(-x*22))*x)*np.exp(-x*9),.40,.5,.6)
# 3) FLY-BY WHOOSHES 0.9 -> 2.3, accelerating (cards passing the camera)
def whoosh(t0,dur,g,pan_from,pan_to,bright):
    m,x=win(t0,dur); k=x/dur; env=np.sin(np.pi*k)**2
    src=noise[m]; y=np.zeros(len(src)); acc=0.0
    for i in range(len(src)):
        a=bright*(.03+.35*np.sin(np.pi*k[i])); acc+=a*(src[i]-acc); y[i]=acc
    pan=pan_from+(pan_to-pan_from)*k
    L[m]+=y*env*g*(1-pan); R[m]+=y*env*g*(1+pan)
tt=0.92; i=0
while tt<2.3:
    tau=(tt-.92)/1.38; dur=.32-.2*tau; gap=.2-.14*tau
    p=1 if i%2 else -1
    whoosh(tt,dur,.75+.5*tau,-.8*p,.8*p,1+tau)
    tt+=gap; i+=1
# rising tonal drone under the vortex
put(lambda x: (np.sin(2*np.pi*(110+180*(x/1.4)**2)*x)+.4*np.sin(2*np.pi*(220+360*(x/1.4)**2)*x))*(x/1.4)**1.5*.25,0.95,1.45,.6)
# 4) SUCTION into the snap 2.18 -> 2.42 (reverse swell)
m,x=win(2.16,.26); k=x/.26; y=hp(noise,.2)[m]*k**3; L[m]+=y*.9; R[m]+=y*.9
# 5) DEEP IMPACT at 2.42: sub drop, body, crack, long tail
T0=2.42
put(lambda x: np.sin(2*np.pi*(32+90*np.exp(-x*9))*x)*np.exp(-x*2.2),T0,1.8,1.25)
put(lambda x: np.sin(2*np.pi*(120*np.exp(-x*25)+55)*x)*np.exp(-x*10),T0,.5,.8)
put(lambda x: HN[:len(x)]*np.exp(-x*60),T0,.15,.6)
m,x=win(T0,1.6); tail=lp(noise,.04)[m]*np.exp(-x*2.6)*.55; L[m]+=tail; R[m]+=np.roll(lp(noise,.04),977)[m]*np.exp(-x*2.6)*.55
# 6) LIGHT SWEEP shimmer 2.80 -> 3.20
put(lambda x: hp(noise,.7)[:len(x)]*np.sin(np.pi*x/.4)**2*.12,2.80,.4,1.,0)
put(lambda x: np.sin(2*np.pi*(2400+2600*x/.4)*x)*np.sin(np.pi*x/.4)**2,2.80,.4,.05,.4)
# text ticks + ripple swells
for i in range(10): put(lambda x: np.sin(2*np.pi*4200*x)*np.exp(-x*140),2.98+i*.036,.04,.035,(-1)**i*.3)
for t0 in (3.2,3.75,4.3): put(lambda x: lp(noise,.02)[:len(x)]*np.sin(np.pi*x/.9)**2*2.5,t0,.9,.18)
# 7) DIGITAL FINISH at 4.50: quick two-tone blip + bitcrushed sparkle, done by ~4.95
def blip(f): return lambda x: np.sign(np.sin(2*np.pi*f*x))*.35*np.exp(-x*30)+np.sin(2*np.pi*f*x)*np.exp(-x*18)
put(blip(1046.5),4.50,.3,.32,-.2); put(blip(1568),4.585,.36,.36,.2)
put(lambda x: np.round(np.sin(2*np.pi*3136*x)*4)/4*np.exp(-x*22),4.585,.25,.08)
put(lambda x: np.sin(2*np.pi*(65+40*np.exp(-x*30))*x)*np.exp(-x*12),4.50,.3,.5)
# room + master
def room(x):
    y=x.copy()
    for d,a in [(.019,.35),(.031,.28),(.047,.22),(.071,.16),(.103,.11),(.149,.07)]: k=int(d*SR); y[k:]+=x[:-k]*a
    return y
L=room(L); R=room(R)
mx=max(np.abs(L).max(),np.abs(R).max()); st=np.stack([L,R],1)/mx
st=np.tanh(st*1.3)/np.tanh(1.3)
st[-int(.006*SR):]*=np.linspace(1,0,int(.006*SR))[:,None]
w=wave.open('sig2.wav','wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((st*32767*.73).astype(np.int16).tobytes()); w.close()
print('ok')
