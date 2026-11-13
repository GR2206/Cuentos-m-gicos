import numpy as np, wave
SR=44100; DUR=40.0
n=int(SR*DUR); L=np.zeros(n); R=np.zeros(n)
def f(m): return 440*2**((m-69)/12)
def add(buf,start,sig):
    i=int(start*SR); j=min(n,i+len(sig)); buf[i:j]+=sig[:j-i]
def soft(m,d=3.0,v=0.2):
    t=np.arange(int(SR*d))/SR; fr=f(m)
    s=np.sin(2*np.pi*fr*t)+0.15*np.sin(2*np.pi*2*fr*t)*np.exp(-t*4)
    env=np.exp(-t*1.3)*np.minimum(1,t/0.03)
    return v*s*env
def pad(ms,d,v=0.05):
    t=np.arange(int(SR*d))/SR
    s=sum(np.sin(2*np.pi*f(m)*t)+0.3*np.sin(2*np.pi*f(m)*1.003*t) for m in ms)
    env=np.minimum(1,t/0.8)*np.minimum(1,(d-t)/0.8)
    return v*s*env
def boing(d=0.35,v=0.04):
    t=np.arange(int(SR*d))/SR; fr=250+300*t/d
    return v*np.sin(2*np.pi*np.cumsum(fr)/SR)*np.exp(-t*8)
C,D,E,F,G,A=72,74,76,77,79,81
q=1.0; start=4.0
mel=[C,C,G,G,A,A,G,None,F,F,E,E,D,D,C,None]*2
for k,m in enumerate(mel):
    if m is None: continue
    long=(k%8)==6
    s=soft(m,4.0 if long else 3.0)
    add(L,start+k*q,s); add(R,start+k*q+0.012,s*0.9)
    e=soft(m,2.0,0.05); add(R,start+k*q+0.5,e); add(L,start+k*q+0.55,e*0.8)
chords={'C':[48,55,64],'F':[53,57,60],'G':[55,59,62]}
prog=['C','C','F','C','F','C','G','C']*2
for k,ch in enumerate(prog):
    p=pad(chords[ch],2.6); add(L,start+k*2.0-0.2,p); add(R,start+k*2.0-0.2,p)
for k,m in enumerate([60,64,67,72,76,79]):
    s=soft(m,3.0,0.12); add(L,0.5+k*0.45,s); add(R,0.5+k*0.45,s)
for k in range(3):
    land=0.5+5.5*(k+1)/3
    b=boing(); add(L,land-0.03,b); add(R,land-0.03,b)
for t0 in (3.5, 9.0, 31.0):
    for k,m in enumerate([96,93,91,88,84]):
        s=soft(m,1.5,0.035); add(L,t0+k*0.1,s); add(R,t0+k*0.1+0.01,s)
for k,m in enumerate([60,64,67,72]):
    s=soft(m,5.0,0.13); add(L,36.0+k*0.15,s); add(R,36.0+k*0.15,s)
add(L,35.8,pad([48,55,64],4.2)); add(R,35.8,pad([48,55,64],4.2))
t=np.arange(n)/SR; fade=np.minimum(1,(DUR-t)/3.0)
st=np.stack([L,R],1)*fade[:,None]
# gentle low-pass for a softer tone
k=np.ones(9)/9
st=np.stack([np.convolve(st[:,0],k,'same'),np.convolve(st[:,1],k,'same')],1)
st=st/np.abs(st).max()*0.7
with wave.open('sleep_music.wav','wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((st*32767).astype('<i2').tobytes())
