import numpy as np, wave
SR=48000; N=int(SR*5.0); t=np.arange(N)/SR
L=np.zeros(N); R=np.zeros(N); noise=np.random.default_rng(23).standard_normal(N)
def lp(x,a):
    y=np.empty_like(x); acc=0.0
    for i in range(len(x)): acc+=a*(x[i]-acc); y[i]=acc
    return y
def hp(x,a): return x-lp(x,a)
HN=hp(noise,.55); LN=lp(noise,.04)
def win(t0,dur): m=(t>=t0)&(t<t0+dur); return m,t[m]-t0
def put(fn,t0,dur,g=1.,pan=0.):
    global L,R
    m,x=win(t0,dur); s=fn(x)*g; L[m]+=s*(1-pan); R[m]+=s*(1+pan)
def boom(t0,g=1.,f0=32,f1=90,dec=2.2,dur=1.6): put(lambda x: np.sin(2*np.pi*(f0+f1*np.exp(-x*9))*x)*np.exp(-x*dec),t0,dur,g)
def kick(t0,g=1.,f=55,top=150): put(lambda x: np.sin(2*np.pi*(f+top*np.exp(-x*28))*x)*np.exp(-x*11),t0,.45,g)
def snap(t0,g=.6,dec=60): put(lambda x: HN[:len(x)]*np.exp(-x*dec),t0,.15,g)
def save(name,lufs=-15):
    global L,R
    def room(x):
        y=x.copy()
        for d,a in [(.019,.35),(.031,.28),(.047,.22),(.071,.16),(.103,.11),(.149,.07)]: k=int(d*SR); y[k:]+=x[:-k]*a
        return y
    st=np.stack([room(L),room(R)],1); st/=np.abs(st).max(); st=np.tanh(st*1.3)/np.tanh(1.3)
    st[-int(.006*SR):]*=np.linspace(1,0,int(.006*SR))[:,None]
    w=wave.open(name,'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((st*32767*.7).astype(np.int16).tobytes()); w.close()
