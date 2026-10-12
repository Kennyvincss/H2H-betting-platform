# Knockout: charge-up, three panel stomps, page swoosh, wind-up, punch + paper rip, caption slam, boxing bell.
import sys; sys.path.insert(0,'.')
from sfx_common import *
TP=1.36
m,x=win(.02,.3); k=x/.3; y=lp(noise,.06)[m]*k**2; L[m]+=y*.6; R[m]+=y*.6                  # charge-up
for t0 in (.30,.55,.80):                                                                   # stomps
    kick(t0,1.0,48,170); snap(t0,.45,45)
    put(lambda x: np.sin(2*np.pi*(900-500*x/.12)*x)*np.exp(-x*25),t0,.12,.06)
put(lambda x: hp(noise,.3)[:len(x)]*np.sin(np.pi*x/.2)**2,1.0,.2,.3)                     # page swoosh
m,x=win(1.16,TP-1.16); k=x/(TP-1.16)                                                        # wind-up: rising whistle
put(lambda x: np.sin(2*np.pi*(300+1500*(x/.2)**2)*x)*(x/.2)**1.5,1.16,TP-1.16,.12)
m,x=win(1.16,TP-1.16); y=hp(noise,.25)[m]*k**3; L[m]+=y*.5; R[m]+=y*.5
boom(TP,1.25,30,110,2.0,1.8); kick(TP,1.0,60,220); snap(TP,.7,40)                          # PUNCH
rip=np.zeros(N); g=np.random.default_rng(3)
for i in range(70):                                                                         # paper rip crackle
    t0=TP+g.random()*.32; put(lambda x: HN[:len(x)]*np.exp(-x*700),t0,.01,.35*np.exp(-(t0-TP)*5),g.uniform(-.8,.8))
put(lambda x: lp(noise,.2)[:len(x)]*np.exp(-x*7),TP,.4,.6)
kick(1.95,.8,70,180); snap(1.95,.35,70)                                                    # caption slam
# light bouncy groove under the hold
for i,t0 in enumerate(np.arange(2.3,4.4,60/124/2)):
    if i%4==0: kick(t0,.45,52,120)
    if i%4==2: snap(t0,.12,80)
    put(lambda x: np.sin(2*np.pi*(98 if (i//4)%2==0 else 110)*x)*np.exp(-x*9),t0,.2,.12 if i%2==0 else .06)
def bell(t0,g):                                                                             # boxing bell
    put(lambda x: sum(a*np.sin(2*np.pi*f*x)*np.exp(-x*d) for f,a,d in [(1180,1,2.8),(2950,.55,4),(4320,.35,6),(587,.3,3)])*np.clip(x/.002,0,1),t0,5-t0,g)
bell(4.50,.32); bell(4.66,.32); kick(4.48,.7,50,160)
save('sig6.wav')
print('ok')
