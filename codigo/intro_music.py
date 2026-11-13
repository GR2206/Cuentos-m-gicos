"""Jingle original del canal (5,5 s): pajarito, marimba, campanitas y acorde final.
Uso: python3 intro_music.py            -> intro_music.wav (versión alegre)
     python3 intro_music.py cuna       -> intro_cuna.wav  (versión lenta para dormir)"""
import numpy as np, wave, sys

CUNA = len(sys.argv) > 1 and sys.argv[1] == 'cuna'
SR = 44100
SPEED = 2.0 if CUNA else 1.0
DUR = 5.5 * (1.6 if CUNA else 1.0)
n = int(SR * DUR); L = np.zeros(n); R = np.zeros(n)
rng = np.random.default_rng(1)

def f(m): return 440 * 2 ** ((m - 69) / 12)
def add(t0, sig, pan=0.0):
    i = int(t0 * SR); j = min(n, i + len(sig))
    if i >= n: return
    L[i:j] += sig[:j - i] * (1 - pan) ; R[i:j] += sig[:j - i] * (1 + pan)

def marimba(m, v=0.3, d=1.2):
    t = np.arange(int(SR * d)) / SR; fr = f(m)
    s = np.sin(2 * np.pi * fr * t) * np.exp(-t * 5) + 0.5 * np.sin(2 * np.pi * 4 * fr * t) * np.exp(-t * 30)
    s += 0.25 * np.sin(2 * np.pi * 10 * fr * t) * np.exp(-t * 80)
    return v * s * np.minimum(1, t / 0.002)

def musicbox(m, v=0.25, d=2.5):
    t = np.arange(int(SR * d)) / SR; fr = f(m)
    s = np.sin(2 * np.pi * fr * t) + 0.15 * np.sin(2 * np.pi * 2 * fr * t) * np.exp(-t * 4)
    return v * s * np.exp(-t * 1.6) * np.minimum(1, t / 0.02)

def bell(m, v=0.08, d=1.5):
    t = np.arange(int(SR * d)) / SR; fr = f(m)
    s = np.sin(2 * np.pi * fr * t) + 0.4 * np.sin(2 * np.pi * 2.76 * fr * t) * np.exp(-t * 6)
    return v * s * np.exp(-t * 3)

def chirp(v=0.06):
    d = 0.09; t = np.arange(int(SR * d)) / SR
    fr = 3200 + 1800 * np.sin(np.pi * t / d)
    return v * np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.sin(np.pi * t / d)

def shaker(v=0.035):
    d = 0.06; t = np.arange(int(SR * d)) / SR
    x = rng.standard_normal(len(t)); x = np.diff(x, prepend=0)
    return v * x * np.exp(-t * 60)

def thump(v=0.35):
    d = 0.5; t = np.arange(int(SR * d)) / SR
    fr = 50 + 70 * np.exp(-t * 25)
    return v * np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-t * 8)

def pad(ms, d, v=0.05):
    t = np.arange(int(SR * d)) / SR
    s = sum(np.sin(2 * np.pi * f(m) * t) + 0.3 * np.sin(2 * np.pi * f(m) * 1.004 * t) for m in ms)
    return v * s * np.minimum(1, t / 0.3) * np.minimum(1, (d - t) / 0.8)

note = musicbox if CUNA else marimba
S = SPEED if CUNA else 1.0
if not CUNA:
    for k, t0 in enumerate((0.05, 0.16, 0.3)):  # pajarito
        add(t0, chirp(), 0.5)
# pop de cada personaje: G4 C5 E5 G5 C6
for k, (t0, m) in enumerate(zip((0.40, 0.75, 1.10, 1.45, 1.80), (67, 72, 76, 79, 84))):
    add(t0 * S, note(m), (k - 2) * 0.2)
# brillo mágico al empezar el título
for k, m in enumerate((84, 88, 91, 96, 100)):
    add(2.15 * S + k * 0.04 * S, bell(m), 0.3)
# frase pegadiza: "Cuen-tos má-gi-cos" (E G A G E D C)
for k, (m, dt) in enumerate(zip((76, 79, 81, 79, 76, 74), (0, .14, .28, .42, .62, .76))):
    add((2.35 + dt) * S, note(m, 0.32))
# acorde final + golpe suave
T_END = 3.35 * S
for k, m in enumerate((60, 64, 67, 72, 76)):
    add(T_END + k * 0.03, note(m, 0.22, 2.5))
for k, m in enumerate((96, 91, 88, 84)):
    add(T_END + 0.3 + k * 0.08, bell(m, 0.05))
add(T_END - 0.05, pad((48, 55, 64, 72), DUR - T_END + 0.05))
if not CUNA:
    add(T_END, thump())
    for k in range(12):
        add(0.4 + k * 0.245, shaker(0.035 if k % 2 else 0.05))

t = np.arange(n) / SR
fade = np.minimum(1, (DUR - t) / 0.6)
st = np.stack([L, R], 1) * fade[:, None]
st = st / np.abs(st).max() * (0.7 if CUNA else 0.89)
name = 'intro_cuna.wav' if CUNA else 'intro_music.wav'
with wave.open(name, 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((st * 32767).astype('<i2').tobytes())
print(name, DUR)
