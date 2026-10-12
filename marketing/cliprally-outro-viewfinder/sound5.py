# Viewfinder: REC beep, timecode ticks, focus motor, shutter clack, deep hit, typing, final shutter + beep.
import sys; sys.path.insert(0,'.')
from sfx_common import *
TS,TO=1.40,1.56
put(lambda x: np.sin(2*np.pi*1975*x)*np.clip(x/.005,0,1)*np.exp(-x*9),0.10,.18,.12)     # REC beep
put(lambda x: LN[:len(x)]*.9*np.clip(x/.3,0,1),0.08,TS-.08,.35)                            # sensor hum / air
put(lambda x: np.sin(2*np.pi*60*x)*.5*np.clip(x/.3,0,1),0.08,TS-.08,.05)
for i in range(int((TO-.2)/.05)):                                                          # running timecode ticks
    put(lambda x: np.sin(2*np.pi*3800*x)*np.exp(-x*400),0.2+i*.05,.02,.035,(-1)**i*.2)
for t0,d,f in [(.55,.18,240),(.78,.12,300),(.92,.14,260),(1.08,.12,330),(1.22,.1,290),(1.33,.06,360)]:   # focus motor whirrs
    put(lambda x,f=f,d=d: (np.sign(np.sin(2*np.pi*f*x))*.4+np.sin(2*np.pi*f*2*x))*np.sin(np.pi*x/d)**2,t0,d,.06,.3)
    put(lambda x: np.sin(2*np.pi*2600*x)*np.exp(-x*300),t0+d,.02,.05)                     # AF confirm tick
def clack(t0,g):                                                                          # mechanical shutter
    put(lambda x: HN[:len(x)]*np.exp(-x*180)+np.sin(2*np.pi*1400*x)*np.exp(-x*90)*.6,t0,.08,g)
    put(lambda x: np.sin(2*np.pi*(180*np.exp(-x*40)+90)*x)*np.exp(-x*30),t0,.15,g*.8)
clack(TS,.55); clack(TO,.6)
boom(TO,1.1); snap(TO,.4)
put(lambda x: LN[:len(x)]*np.exp(-x*2.4),TO,1.6,.45)
put(lambda x: (np.sin(2*np.pi*110*x)+.6*np.sin(2*np.pi*164.8*x)+.4*np.sin(2*np.pi*220*x))*np.clip(x/.6,0,1)*np.clip((4.95-TO-x)/.3,0,1),TO+.1,4.95-TO-.1,.07)  # filmic pad
for i in range(20): put(lambda x: HN[:len(x)]*np.exp(-x*500)+np.sin(2*np.pi*2100*x)*np.exp(-x*300)*.5,1.95+i*.025,.03,.12,(-1)**i*.2)  # typing
clack(4.46,.5); clack(4.58,.5)
put(lambda x: np.sin(2*np.pi*1568*x)*np.exp(-x*14)+np.sin(2*np.pi*2093*x)*np.exp(-x*16)*.6,4.6,.35,.22)
kick(4.58,.6,50,120)
save('sig5.wav')
print('ok')
