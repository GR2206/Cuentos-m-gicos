"""Música del short de La gran carrera (41 s). Original."""
import numpy as np, wave

SR = 44100; DUR = 41.0
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

# ---------- efectos nuevos ----------
def snore(v=0.07, d=2.4):
    t = T(d); x = rng.standard_normal(len(t)); x = np.convolve(x, np.ones(60) / 60, 'same') * 6
    hum = np.sin(2 * np.pi * 85 * t) * (1 + 0.5 * np.sin(2 * np.pi * 30 * t))
    env = np.where(t < d / 2, np.sin(np.pi * t / d) ** 2, 0.4 * np.sin(np.pi * t / d) ** 2)
    return v * (x + 0.6 * hum) * env
def knock(v=0.3):
    t = T(0.18); return v * (np.sin(2 * np.pi * 320 * t) * np.exp(-t * 45) + 0.3 * rng.standard_normal(len(t)) * np.exp(-t * 120))
def rustle(d=1.5, v=0.05):
    t = T(d); x = rng.standard_normal(len(t)); x = np.diff(x, prepend=0)
    return v * x * (0.5 + 0.5 * np.abs(np.sin(2 * np.pi * 6 * t))) * np.sin(np.pi * t / d)
def sneaky(t0, t1, v=0.8):
    pat = [48, 50, 51, 52, 55, 52, 51, 50]
    k = 0; t = t0
    while t < t1 - 0.1:
        add(t, pluck(pat[k % 8] + 12, 0.14), 0.15 * np.sin(k), v)
        if k % 4 == 0: add(t, bass(pat[k % 8] - 12, 0.18), 0, v)
        if k % 8 == 6: add(t + 0.15, marimba(79, 0.08), 0.4, v)
        t += 0.38; k += 1
def found(t0):
    for k, m in enumerate((72, 76, 79, 84)): add(t0 + k * 0.09, marimba(m, 0.28), (k - 1.5) * 0.2)
    sparkle_sfx(t0 + 0.3, 0.07); add(t0, pad((60, 64, 67, 72), 1.8, 0.04))

# ---------- efectos de lluvia ----------
def rain_bed(t0, t1, v=0.06):
    d = t1 - t0; t = T(d); x = rng.standard_normal(len(t))
    x = np.convolve(x, np.ones(4) / 4, 'same')
    env = np.clip(np.minimum((t - 0) / 3.0, (d - t) / 4.0), 0, 1)
    return v * x * env
def plip(v=0.08, f0=1800):
    t = T(0.12); fr = f0 * (1 + 0.6 * np.exp(-t * 40))
    return v * np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-t * 30)
def harp(t0, notes, dur, v=0.12):
    for k, m in enumerate(notes):
        add(t0 + k * dur / len(notes), bell(m, v * 0.7, 2.0), 0.6 * np.sin(k)); add(t0 + k * dur / len(notes), musicbox(m, v, 2.0))

def squelch(v=0.06):
    t = T(0.18); fr = 120 + 200 * np.exp(-t * 20)
    x = rng.standard_normal(len(t)); x = np.convolve(x, np.ones(30) / 30, 'same') * 5
    return v * (np.sin(2 * np.pi * np.cumsum(fr) / SR) + x) * np.exp(-t * 15)
def water_bed(t0, t1, v=0.04):
    d = t1 - t0; t = T(d); x = rng.standard_normal(len(t)); x = np.convolve(x, np.ones(3) / 3, 'same')
    env = np.clip(np.minimum(t / 3.0, (d - t) / 3.0), 0, 1)
    add(t0, v * x * env)

def bloop(v=0.07, f0=500):
    t = T(0.25); fr = f0 * (1 + 1.5 * t / 0.25)
    return v * np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.sin(np.pi * t / 0.25)
def plop(t0):
    add(t0, bloop(0.06, 700)); add(t0 + 0.05, plip(0.08, 1100)); sparkle_sfx(t0 + 0.05, 0.06)

def clap(v=0.12):
    t = T(0.09); x = rng.standard_normal(len(t)); x = np.diff(x, prepend=0)
    return v * x * np.exp(-t * 50)

def squeak(v=0.06):
    t = T(0.22); fr = 900 + 700 * np.sin(np.pi * t / 0.22)
    return v * np.sign(np.sin(2 * np.pi * np.cumsum(fr) / SR)) * 0.4 * np.sin(np.pi * t / 0.22)

# ---------- partitura ----------
add(0.0, bell(91, 0.12, 1.2)); add(0.0, slide(500, 1200, 0.5, 0.05)); sparkle_sfx(0.1, 0.06)
theme(0.3, 7.5, beat=0.3, v=0.75, shake=True)
add(7.6, boing(0.08, 0.5, up=False)); add(7.6, pad((57, 60, 63), 3.8, 0.04))
theme(8.0, 11.5, beat=0.4, inst=pluck, v=0.5)
add(11.6, boing(0.08, 0.4)); sparkle_sfx(12.5, 0.05)
theme(12.0, 15.5, beat=0.3, v=0.7, shake=True)
add(15.6, thump(0.15)); add(16.0, pad((57, 60, 63), 3.0, 0.04))
add(18.5, slide(200, 600, 2.0, 0.04)); add(21.0, whoosh(0.05, 1.2)); add(22.4, thump(0.2))
theme(23.0, 30.5, beat=0.28, v=0.75, shake=True)
add(28.0, slide(400, 1300, 0.6, 0.05)); add(28.1, clap(0.15)); add(28.3, clap(0.15)); sparkle_sfx(28.2, 0.1)
for k, m in enumerate((72, 76, 79, 84, 88)): add(28.1 + k * 0.08, bell(m, 0.08, 2.5))
for k in range(4): add(30.5 + 0.6 * k, bell(88 + 3 * k, 0.07, 1.2)); sparkle_sfx(30.6 + 0.6 * k, 0.04)
theme(30.5, 38.0, beat=0.38, v=0.75, shake=True)
for k, m in enumerate((72, 76, 79, 84, 79, 84)): add(38.0 + k * 0.22, bell(m, 0.06, 1.2), 0.3 * np.sin(k))
add(39.2, clap(0.12)); add(39.5, clap(0.1))
for k in range(6): add(39.6 + k * 0.12, bell(96, 0.04, 0.6), 0.4 * np.sin(k))
add(38.0, pad((60, 64, 67, 72), 3.0, 0.04))
t = np.arange(n) / SR
fade = np.minimum(1, (DUR - t) / 1.5) * np.minimum(1, t / 0.3)
st = np.stack([L, R], 1) * fade[:, None]
st = st / np.abs(st).max() * 0.88
with wave.open('ep21_short_musica.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((st * 32767).astype('<i2').tobytes())
print('ok')
