import numpy as np, wave
SR=44100; DUR=20.0
n=int(SR*DUR); L=np.zeros(n); R=np.zeros(n)
def f(m): return 440*2**((m-69)/12)
def add(buf,start,sig):
    i=int(start*SR); j=min(n,i+len(sig)); buf[i:j]+=sig[:j-i]
def musicbox(m,d=1.6,v=0.25):
    t=np.arange(int(SR*d))/SR; fr=f(m)
    s=np.sin(2*np.pi*fr*t)+0.35*np.sin(2*np.pi*2*fr*t)*np.exp(-t*6)+0.12*np.sin(2*np.pi*4.01*fr*t)*np.exp(-t*10)
    env=np.exp(-t*2.6)*np.minimum(1,t/0.004)
    return v*s*env
def pad(ms,d,v=0.06):
    t=np.arange(int(SR*d))/SR
    s=sum(np.sin(2*np.pi*f(m)*t)+0.3*np.sin(2*np.pi*f(m)*1.003*t) for m in ms)
    env=np.minimum(1,t/0.25)*np.minimum(1,(d-t)/0.35)
    return v*s*env
def boing(d=0.25,v=0.12):
    t=np.arange(int(SR*d))/SR; fr=300+500*t/d
    return v*np.sin(2*np.pi*np.cumsum(fr)/SR)*np.exp(-t*10)
C,D,E,F,G,A=72,74,76,77,79,81
q=0.5
mel=[C,C,G,G,A,A,G,None,F,F,E,E,D,D,C,None]*2
start=2.0
for k,m in enumerate(mel):
    if m is None: continue
    dur=2*q if (k%8)==6 else q
    s=musicbox(m, 2.0 if dur>q else 1.4)
    add(L,start+k*q,s); add(R,start+k*q,s*0.9)
    # soft echo an octave down-ish sparkle
    add(R,start+k*q+0.25,musicbox(m,1.0,0.07)); add(L,start+k*q+0.25,musicbox(m,1.0,0.05))
chords={'C':[48,55,64],'F':[53,57,60],'G':[55,59,62]}
prog=['C','C','F','C','F','C','G','C']*2
for k,ch in enumerate(prog):
    p=pad(chords[ch],1.0+0.3); add(L,start+k*1.0,p); add(R,start+k*1.0,p)
# intro arpeggio
for k,m in enumerate([60,64,67,72,76,79,84]):
    s=musicbox(m,1.5,0.17); add(L,0.3+k*0.22,s); add(R,0.3+k*0.22,s)
# hops
for ht in (0.4+3.6/6, 0.4+3.6/2, 0.4+3.6*5/6, 4.0):
    pass
for k in range(3):
    land=0.4+3.6*(k+1)/3
    b=boing(); add(L,land-0.02,b); add(R,land-0.02,b)
# final chord
for k,m in enumerate([60,64,67,72]):
    s=musicbox(m,3.0,0.18); add(L,18.0+k*0.08,s); add(R,18.0+k*0.08,s)
add(L,18.0,pad([48,55,64],2.0)); add(R,18.0,pad([48,55,64],2.0))
t=np.arange(n)/SR; fade=np.minimum(1,(DUR-t)/1.2)
st=np.stack([L,R],1)*fade[:,None]
st=st/np.abs(st).max()*0.85
with wave.open('music.wav','wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((st*32767).astype('<i2').tobytes())
