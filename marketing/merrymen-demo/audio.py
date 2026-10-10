import numpy as np, wave, json
_P=json.load(open('vo/warp.json')); _new=[p[0] for p in _P]; _old=[p[1] for p in _P]
W=lambda x: float(np.interp(x,_old,_new))
SR=48000; D=60.0; N=int(SR*D); t=np.arange(N)/SR
L=np.zeros(N); R=np.zeros(N)
rs=np.random.default_rng(7)
def env(a,b,fi,fo):
    e=np.clip((t-a)/max(fi,1e-3),0,1)*np.clip((b-t)/max(fo,1e-3),0,1); return e
def add(sig,pan=0.0,g=1.0):
    global L,R
    L+=sig*g*(1-pan)/1.0; R+=sig*g*(1+pan)/1.0
def lp(x,a):  # one-pole lowpass
    y=np.empty_like(x); acc=0.0
    for i in range(0,len(x)):
        acc+=a*(x[i]-acc); y[i]=acc
    return y
noise=rs.standard_normal(N)
# --- drone bed: A minor, tense in S1, brighter in S2/S3, dark in S4
drone=(np.sin(2*np.pi*55*t)+.6*np.sin(2*np.pi*55.4*t)+.35*np.sin(2*np.pi*82.4*t)+.2*np.sin(2*np.pi*110.7*t))
add(drone*(env(W(0),W(12),2,1)*.22+env(W(42),W(53),.3,1)*.28),0,1)
# filtered noise air
air=lp(noise,0.02)*3
add(air*env(W(0),W(60),2,2)*.05,0.2)
# --- heartbeat pulses S1 accelerating
def kick(at,g=1.0,f0=90):
    m=(t>=at)&(t<at+0.35); x=t[m]-at
    s=np.zeros(N); s[m]=np.sin(2*np.pi*(f0*np.exp(-x*9)+38)*x)*np.exp(-x*11)*g; return s
tt=0.6
while tt<10.6:
    k=kick(W(tt),.9); add(k,0,.8); add(kick(W(tt)+.18,.5),0,.8)
    tt+= max(.55, 1.0-tt*.05)
# --- phone vibration 2.2-3.2
vib=np.sign(np.sin(2*np.pi*150*t))*(np.sin(2*np.pi*4*t)>0)
add(lp(vib,.15)*env(W(2.2),W(3.2),.02,.05)*.18,.4)
# --- whooshes at cuts
def whoosh(at,dur=.6,g=.35):
    e=env(at-dur*.7,at+dur*.3,dur*.7,dur*.3); s=lp(noise*e,.08)*4; return s*g
for c in [5.0,8.3,10.75,12.0,16.0,22.0,25.4,31.0,34.4,37.1,44.6,51.4]: add(whoosh(W(c),.5,.22),(-.3 if int(c)%2 else .3))
# --- hit on "Merrymen"
add(kick(W(10.85),1.4,70),0,1); 
# --- product groove S2/S3: muted pulse + arps in A minor -> C major
notes=[220,261.63,329.63,392,329.63,261.63,220,196]
step=60/112/2; tt=W(12.0); i=0
while tt<W(42):
    f=notes[i%8]*(1 if tt<W(32) else 1.122)
    m=(t>=tt)&(t<tt+.25); x=t[m]-tt
    s=np.zeros(N); s[m]=(np.sin(2*np.pi*f*x)+.3*np.sin(2*np.pi*2*f*x))*np.exp(-x*14)
    add(s,(.35 if i%2 else -.35),.10)
    if i%4==0: add(kick(tt,.6,80),0,.55)
    tt+=step; i+=1
pad=sum(np.sin(2*np.pi*f*t) for f in [220,261.63,329.63])*.33
add(pad*env(W(12),W(42),1.2,.6)*.07,0)
# UI ticks typing 31.5-33.1
for k in range(26):
    at=W(31.5+k*1.6/26); m=(t>=at)&(t<at+.02); s=np.zeros(N); s[m]=noise[m]*np.exp(-(t[m]-at)*300); add(s,.2,.25)
# highlight blips
for at in [16.4,17.6,18.8,23.2,25.7,28.4,34.8,37.5,39.2,40.6,45.4,46.6,51.6]:
    at=W(at); m=(t>=at)&(t<at+.15); s=np.zeros(N); x=t[m]-at; s[m]=np.sin(2*np.pi*1320*x)*np.exp(-x*30); add(s,0,.08)
# --- crash: alarm + sub drop + impact
add(kick(W(42.0),1.6,60),0,1.1)
alarm=np.sin(2*np.pi*(660+220*(np.sin(2*np.pi*2*t)>0))*t)
add(alarm*env(W(42.1),W(44.6),.05,.3)*.07,0)
sub=np.sin(2*np.pi*(45-12*np.clip((t-W(42))/2.5,0,1))*t)
add(sub*env(W(42),W(44.8),.05,.4)*.35,0)
# refused "thunk"s
for at in [45.4,46.6]: add(kick(W(at),.8,140),0,.6)
# --- resolution pad S4 tail into S5 + riser
pad2=sum(np.sin(2*np.pi*f*t) for f in [130.81,196,261.63,329.63])*.25
add(pad2*env(W(47),W(60),2,1.2)*.09,0)
rise=lp(noise,.05)*np.clip((t-W(52.5))/(W(55.6)-W(52.5)),0,1)**2*(t<W(55.6))*2.2
add(rise*.18,0)
# laptop close click
_c=W(55.15); m=(t>=_c)&(t<_c+.15); s=np.zeros(N); x=t[m]-_c; s[m]=lp(noise,.3)[m]*np.exp(-x*60); add(s,0,.5)
# logo hit with long tail
_h=W(55.6); hit=np.zeros(N); m=t>=_h; x=t[m]-_h
hit[m]=(np.sin(2*np.pi*55*x)*1.0+np.sin(2*np.pi*110*x)*.5+np.sin(2*np.pi*220*x)*.3+np.sin(2*np.pi*329.63*x)*.25+np.sin(2*np.pi*440*x)*.15)*np.exp(-x*.9)
add(hit,0,.42); add(kick(_h,1.5,70),0,1)
# final fade
fade=np.clip((60-t)/0.8,0,1)
L*=fade; R*=fade
peak=max(np.abs(L).max(),np.abs(R).max()); L/=peak/0.89; R/=peak/0.89
st=np.stack([L,R],1); st=(np.tanh(st*1.2)/np.tanh(1.2)*32767*.95).astype(np.int16)
w=wave.open('music.wav','wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(st.tobytes()); w.close()
print('ok')
