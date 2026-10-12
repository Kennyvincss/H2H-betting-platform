# Original 5s audio signature: black -> rising energy vortex -> suction -> deep logo impact
# -> sweep shimmer -> text ticks -> ripple swells -> final punch + two-tone digital finish.
import numpy as np, wave
SR=48000; N=int(SR*5.0); t=np.arange(N)/SR; T0=1.62
L=np.zeros(N); R=np.zeros(N); noise=np.random.default_rng(23).standard_normal(N)
def lp(x,a):
    y=np.empty_like(x); acc=0.0
    for i in range(len(x)): acc+=a*(x[i]-acc); y[i]=acc
    return y
def hp(x,a): return x-lp(x,a)
HN=hp(noise,.55)
def win(t0,dur): m=(t>=t0)&(t<t0+dur); return m,t[m]-t0
def put(fn,t0,dur,g=1.,pan=0.):
    m,x=win(t0,dur); s=fn(x)*g; L[m]+=s*(1-pan); R[m]+=s*(1+pan)
# 1) a low pulse out of the black
put(lambda x: np.sin(2*np.pi*(48+20*np.exp(-x*6))*x)*np.exp(-x*2.5)*np.clip(x/.05,0,1),0.05,.9,.5)
# 2) rising energy 0.15 -> T0: filtered noise riser + tonal sweep
m,x=win(.15,T0-.15); k=x/(T0-.15); y=np.zeros(m.sum()); acc=0.0; src=noise[m]
for i in range(len(src)): a=.01+.4*k[i]**2; acc+=a*(src[i]-acc); y[i]=acc
L[m]+=y*k**1.6*1.1*(1-.5*np.sin(2*np.pi*3*x)); R[m]+=y*k**1.6*1.1*(1+.5*np.sin(2*np.pi*3*x))
put(lambda x: (np.sin(2*np.pi*(90+420*(x/1.47)**2)*x)+.4*np.sin(2*np.pi*(180+840*(x/1.47)**2)*x))*(x/1.47)**1.5,.15,T0-.15,.28)
# 3) swirling whooshes accelerating with the vortex
def whoosh(t0,dur,g,p0,p1):
    m,x=win(t0,dur); k=x/dur; env=np.sin(np.pi*k)**2; src=noise[m]; y=np.zeros(len(src)); acc=0.0
    for i in range(len(src)): a=.03+.35*np.sin(np.pi*k[i]); acc+=a*(src[i]-acc); y[i]=acc
    pan=p0+(p1-p0)*k; L[m]+=y*env*g*(1-pan); R[m]+=y*env*g*(1+pan)
tt=.35; i=0
while tt<T0-.25:
    tau=(tt-.35)/(T0-.6); d=.34-.2*tau; p=1 if i%2 else -1
    whoosh(tt,d,.45+.5*tau,-.8*p,.8*p); tt+=.22-.14*tau; i+=1
# 4) suction into the punch
m,x=win(T0-.26,.26); k=x/.26; y=hp(noise,.2)[m]*k**3; L[m]+=y*.9; R[m]+=y*.9
# 5) DEEP IMPACT: the mascot punches out
put(lambda x: np.sin(2*np.pi*(32+90*np.exp(-x*9))*x)*np.exp(-x*2.2),T0,1.8,1.25)
put(lambda x: np.sin(2*np.pi*(120*np.exp(-x*25)+55)*x)*np.exp(-x*10),T0,.5,.8)
put(lambda x: HN[:len(x)]*np.exp(-x*60),T0,.15,.6)
m,x=win(T0,1.6); L[m]+=lp(noise,.04)[m]*np.exp(-x*2.6)*.55; R[m]+=np.roll(lp(noise,.04),977)[m]*np.exp(-x*2.6)*.55
# 6) light sweep shimmer, text ticks, ripple swells
put(lambda x: hp(noise,.7)[:len(x)]*np.sin(np.pi*x/.42)**2*.12,T0+.4,.42)
put(lambda x: np.sin(2*np.pi*(2400+2600*x/.42)*x)*np.sin(np.pi*x/.42)**2,T0+.4,.42,.05,.4)
for i in range(10): put(lambda x: np.sin(2*np.pi*4200*x)*np.exp(-x*140),T0+.5+i*.036,.04,.035,(-1)**i*.3)
for t0 in (T0+.75,T0+1.35,T0+1.95): put(lambda x: lp(noise,.02)[:len(x)]*np.sin(np.pi*x/.9)**2*2.5,t0,.9,.18)
# 7) final punch + two-tone digital finish at 4.50
def blip(f): return lambda x: np.sign(np.sin(2*np.pi*f*x))*.35*np.exp(-x*30)+np.sin(2*np.pi*f*x)*np.exp(-x*18)
put(blip(1046.5),4.50,.3,.32,-.2); put(blip(1568),4.585,.36,.36,.2)
put(lambda x: np.round(np.sin(2*np.pi*3136*x)*4)/4*np.exp(-x*22),4.585,.25,.08)
put(lambda x: np.sin(2*np.pi*(65+40*np.exp(-x*30))*x)*np.exp(-x*12),4.50,.3,.6)
def room(x):
    y=x.copy()
    for d,a in [(.019,.35),(.031,.28),(.047,.22),(.071,.16),(.103,.11),(.149,.07)]: k=int(d*SR); y[k:]+=x[:-k]*a
    return y
L=room(L); R=room(R)
st=np.stack([L,R],1); st/=np.abs(st).max(); st=np.tanh(st*1.3)/np.tanh(1.3)
st[-int(.006*SR):]*=np.linspace(1,0,int(.006*SR))[:,None]
w=wave.open('sig4.wav','wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((st*32767*.73).astype(np.int16).tobytes()); w.close()
print('ok')
