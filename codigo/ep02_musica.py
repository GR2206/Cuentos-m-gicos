"""Música y efectos del episodio 2 — El puente del río (126 s). Todo original.
El tema principal usa la frase del canal (Mi Sol La Sol Mi Re Do) de la intro."""
import numpy as np, wave

SR = 44100; DUR = 126.0
n = int(SR * DUR); L = np.zeros(n); R = np.zeros(n)
rng = np.random.default_rng(3)

def f(m): return 440 * 2 ** ((m - 69) / 12)
def add(t0, sig, pan=0.0, v=1.0):
    i = int(t0 * SR)
    if i >= n or i < 0: return
    j = min(n, i + len(sig))
    L[i:j] += v * sig[:j - i] * (1 - pan); R[i:j] += v * sig[:j - i] * (1 + pan)
def T(d): return np.arange(int(SR * d)) / SR

# ---------- instrumentos ----------
def marimba(m, v=0.25, d=1.0):
    t = T(d); fr = f(m)
    s = np.sin(2 * np.pi * fr * t) * np.exp(-t * 5) + 0.45 * np.sin(2 * np.pi * 4 * fr * t) * np.exp(-t * 30)
    return v * s * np.minimum(1, t / 0.002)
def musicbox(m, v=0.2, d=2.5):
    t = T(d); fr = f(m)
    s = np.sin(2 * np.pi * fr * t) + 0.15 * np.sin(2 * np.pi * 2 * fr * t) * np.exp(-t * 4)
    return v * s * np.exp(-t * 1.5) * np.minimum(1, t / 0.02)
def flute(m, v=0.12, d=0.4):
    t = T(d); fr = f(m) * (1 + 0.006 * np.sin(2 * np.pi * 5.5 * t))
    s = np.sin(2 * np.pi * np.cumsum(fr) / SR) + 0.2 * np.sin(4 * np.pi * np.cumsum(fr) / SR)
    env = np.minimum(1, t / 0.04) * np.minimum(1, (d - t) / 0.08)
    return v * s * env
def pluck(m, v=0.22, d=0.5):
    t = T(d); fr = f(m)
    return v * (np.sin(2 * np.pi * fr * t) + 0.3 * np.sin(4 * np.pi * fr * t)) * np.exp(-t * 9)
def bass(m, v=0.25, d=0.45):
    t = T(d); fr = f(m)
    return v * (np.sin(2 * np.pi * fr * t) + 0.25 * np.sin(4 * np.pi * fr * t)) * np.exp(-t * 4) * np.minimum(1, t / 0.01)
def bell(m, v=0.07, d=1.4):
    t = T(d); fr = f(m)
    return v * (np.sin(2 * np.pi * fr * t) + 0.4 * np.sin(2 * np.pi * 2.76 * fr * t) * np.exp(-t * 6)) * np.exp(-t * 3)
def pad(ms, d, v=0.04):
    t = T(d)
    s = sum(np.sin(2 * np.pi * f(m) * t) + 0.3 * np.sin(2 * np.pi * f(m) * 1.004 * t) for m in ms)
    return v * s * np.minimum(1, t / 0.5) * np.minimum(1, (d - t) / 0.6)
def shaker(v=0.03):
    t = T(0.06); x = np.diff(rng.standard_normal(len(t)), prepend=0)
    return v * x * np.exp(-t * 60)

# ---------- efectos ----------
def boing(v=0.12, d=0.3, up=True):
    t = T(d); fr = (250 + 500 * t / d) if up else (700 - 450 * t / d)
    return v * np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-t * 6)
def slide(f0, f1, d, v=0.1):
    t = T(d); fr = f0 + (f1 - f0) * (t / d) ** 1.2
    fr = fr * (1 + 0.01 * np.sin(2 * np.pi * 6 * t))
    return v * np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.minimum(1, t / 0.05) * np.minimum(1, (d - t) / 0.1)
def thump(v=0.3):
    t = T(0.35); fr = 45 + 60 * np.exp(-t * 25)
    return v * np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-t * 10)
def tick(v=0.06):
    t = T(0.05); return v * np.sin(2 * np.pi * 1400 * t) * np.exp(-t * 90)
def splash(v=0.25, d=0.9):
    t = T(d); x = rng.standard_normal(len(t))
    k = np.ones(6) / 6; x = np.convolve(x, k, 'same')
    return v * x * np.exp(-t * 4) * np.minimum(1, t / 0.01)
def whoosh(v=0.12, d=0.6):
    t = T(d); x = rng.standard_normal(len(t)); x = np.convolve(x, np.ones(25) / 25, 'same')
    return v * 4 * x * np.sin(np.pi * t / d)
def crunch(v=0.07):
    t = T(0.12); x = rng.standard_normal(len(t)) * (rng.random(len(t)) > 0.6)
    return v * x * np.exp(-t * 30)
def creak(v=0.06, d=0.7):
    t = T(d); fr = 180 + 60 * np.sin(2 * np.pi * 3 * t)
    s = np.sign(np.sin(2 * np.pi * np.cumsum(fr) / SR))
    return v * np.convolve(s, np.ones(30) / 30, 'same') * np.sin(np.pi * t / d)
def chirp(v=0.05):
    t = T(0.09); fr = 3200 + 1800 * np.sin(np.pi * t / 0.09)
    return v * np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.sin(np.pi * t / 0.09)
def sparkle_sfx(t0, v=0.06):
    for k, m in enumerate((84, 88, 91, 96, 100)): add(t0 + k * 0.05, bell(m, v))

# ---------- tema del canal ----------
C, D, E, F, G, A, B = 60, 62, 64, 65, 67, 69, 71
THEME = [(E, 1), (G, 1), (A, 1), (G, 1), (E, 1), (D, 1), (C, 2),
         (D, 1), (E, 1), (F, 1), (E, 1), (D, 1), (C, 1), (D, 2),
         (E, 1), (G, 1), (A, 1), (G, 1), (E, 1), (D, 1), (C, 1), (E, 1),
         (D, 1), (G, 1), (F, 1), (D, 1), (C, 4)]
CHORDS = ['C', 'C', 'G', 'G', 'C', 'F', 'G', 'C']
ROOT = {'C': 48, 'F': 53, 'G': 55, 'Am': 57}
TRI = {'C': (60, 64, 67), 'F': (60, 65, 69), 'G': (59, 62, 67), 'Am': (57, 60, 64)}

def theme(t0, t1, beat=0.5, inst=marimba, octave=12, v=1.0, bassline=True, shake=False, chords=True):
    t = t0; i = 0; bar = 0
    while t < t1 - 0.05:
        m, d = THEME[i % len(THEME)]
        add(t, inst(m + octave), pan=0.1 * np.sin(i), v=v)
        t += d * beat; i += 1
    total_beats = int((t1 - t0) / beat)
    for b in range(total_beats):
        tb = t0 + b * beat
        ch = CHORDS[(b // 4) % len(CHORDS)]
        if bassline and b % 2 == 0: add(tb, bass(ROOT[ch] - 12 + (7 if b % 4 == 2 else 0)), v=v)
        if chords and b % 4 == 0: add(tb, pad(TRI[ch], beat * 4.2), v=v)
        if shake: add(tb + beat / 2, shaker(0.035), 0.3, v); add(tb, shaker(0.02), -0.3, v)

# ---------- partitura del episodio ----------
for t0 in (0.9, 1.05, 1.25, 7.0, 7.12): add(t0, chirp(), 0.6)
sparkle_sfx(0.6)
theme(1.0, 16.0, beat=0.5, v=0.9, shake=True)
for k in range(5): add(3.0 + k * 1.4 + 0.7, boing(0.07), -0.2)           # saltitos de Coco
add(11.0, bell(91, 0.06)); add(11.3, bell(96, 0.05))                     # globito de pensamiento
add(13.6, boing(0.06)); add(14.2, boing(0.06)); add(14.8, boing(0.06))
add(16.8, creak()); add(17.6, boing(0.1, 0.5, up=False)); add(18.25, splash(), 0.3)
for k, m in enumerate((67, 66, 65, 64)): add(19.0 + k * 0.35, pluck(m, 0.18))   # "oh-oh"
# triste
for k, m in enumerate((69, 72, 76, 74, 72, 71, 69, 68, 69)):
    add(22.0 + k * 0.9, musicbox(m, 0.16, 2.0))
add(22.0, pad((57, 60, 64), 4.0, 0.035)); add(25.6, pad((53, 57, 60), 4.0, 0.035))
# Lola
add(30.0, whoosh(0.1, 0.8), 0.6); add(30.3, chirp(), 0.4); add(30.5, chirp(), 0.4)
theme(30.5, 38.0, beat=0.36, inst=flute, octave=24, v=0.7, bassline=False, chords=True)
add(37.5, whoosh(0.13, 0.7), -0.6)
for t0 in (41.6, 41.75, 41.95): add(t0, chirp(), -0.5)
# llegan los amigos
theme(42.0, 58.0, beat=0.5, v=0.9, shake=True)
for k in range(16): add(43.2 + k * 0.45, thump(0.22), -0.3)            # pasos de Tito
for k in range(20): add(44.5 + k * 0.7, tick(0.05), -0.4)              # pasitos de Tomi
add(57.9, boing(0.08)); sparkle_sfx(58.1, 0.04)
# pensando
add(58.0, pad((60, 64, 67), 5.0, 0.03))
for k in range(9): add(58.2 + k * 0.5, pluck([72, 74][k % 2], 0.08))
add(58.0, slide(400, 700, 1.4, 0.05))                                   # cuello de Pipa
sparkle_sfx(60.3, 0.09); add(60.3, bell(96, 0.1, 2.0))                  # ¡idea!
add(63.0, slide(200, 900, 4.5, 0.08))                                   # trompa que se estira
for k, m in enumerate((60, 64, 67, 72, 76, 79)): add(63.2 + k * 0.7, marimba(m, 0.2))
add(67.8, pad((60, 64, 67, 72), 2.5, 0.05)); sparkle_sfx(67.8, 0.08)
for k in range(6): add(68.0 + k * 0.12, shaker(0.06))
# cruzando con cuidado
add(70.5, pad((60, 67), 13.5, 0.025))
for k in range(20):
    add(71.0 + k * 0.63, pluck([60, 62, 64, 65, 67, 69, 71, 72][k % 8] + 12, 0.11), 0.2 * np.sin(k))
add(84.0, boing(0.08, 0.3, up=False)); sparkle_sfx(84.3, 0.05)
theme(84.5, 95.0, beat=0.5, v=0.85, shake=True)
add(87.0, boing(0.12, 0.45)); sparkle_sfx(88.5, 0.09)
# vuelta rápida
theme(95.0, 101.0, beat=0.33, v=0.8, bassline=True, shake=True, chords=False)
add(101.5, slide(900, 250, 2.0, 0.07))
# reparte bananas
for k, (t0, m) in enumerate(((104.0, 72), (105.5, 76), (107.0, 79), (108.5, 84))):
    add(t0, whoosh(0.08, 0.5)); add(t0 + 0.6, marimba(m, 0.3)); add(t0 + 0.6, bell(m + 12, 0.05))
add(103.5, pad((60, 64, 67), 7.0, 0.03))
for k in range(12): add(110.6 + k * 0.28 + 0.05 * (k % 3), crunch(), 0.3 * np.sin(k))
# baile final
theme(112.0, 118.4, beat=0.4, v=1.0, shake=True)
# final: frase del canal + acorde
for k, (m, dt) in enumerate(zip((76, 79, 81, 79, 76, 74), (0, .2, .4, .6, .9, 1.1))):
    add(118.6 + dt, marimba(m, 0.3))
for k, m in enumerate((60, 64, 67, 72, 76)): add(120.2 + k * 0.03, marimba(m, 0.2, 2.5))
add(120.1, pad((48, 55, 64, 72), 5.5, 0.05)); sparkle_sfx(120.3, 0.07)
add(120.2, thump(0.3))

t = np.arange(n) / SR
fade = np.minimum(1, (DUR - t) / 2.0) * np.minimum(1, t / 0.3)
st = np.stack([L, R], 1) * fade[:, None]
st = st / np.abs(st).max() * 0.89
with wave.open('ep02_musica.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((st * 32767).astype('<i2').tobytes())
print('ok')
