"""Suma los efectos reales (Openverse, CC0) a la música del ep. 28 y escribe ep28_musica.wav.
Los archivos están en ../sfx/ y sus créditos en ../sfx/creditos_sonidos.csv."""
import subprocess, numpy as np
SR = 48000
def load(p):
    raw = subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', p, '-ac', '2', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, 2).copy()
def db(x): return 10 ** (x / 20)
mus = load('ep28_base_musica.wav'); out = mus.copy(); N = len(out)
S = {k: load(f'../sfx/{k}.mp3') for k in ('379345', '351408', '554312', '336612', '498180', '463903', '245834')}
for k, v in S.items(): S[k] = v / max(1e-6, np.abs(v).max())
def place(name, at, src0, dur, gain_db, fade=0.3):
    seg = S[name][int(src0 * SR): int((src0 + dur) * SR)].copy()
    f = min(int(fade * SR), len(seg) // 2)
    if f: seg[:f] *= np.linspace(0, 1, f)[:, None]; seg[-f:] *= np.linspace(1, 0, f)[:, None]
    a = int(at * SR); b = min(N, a + len(seg)); out[a:b] += seg[:b - a] * db(gain_db)
place('463903', 0.0, 2.0, 35.5, -30, 1.5)          # pajaritos de la mañana
place('463903', 46.0, 40.0, 54.0, -31, 1.5)
place('245834', 36.5, 5.0, 4.5, -28, 0.8)          # grillos de las noches
place('245834', 41.5, 20.0, 5.0, -28, 0.8)
place('379345', 16.5, 0.0, 6.8, -22, 0.2)          # ñam ñam
for t0 in (48.0, 49.6, 51.2): place('336612', t0 - 0.85, 0.0, 1.6, -14, 0.05)   # crac (pico a 0,85 s)
place('351408', 55.0 - 2.25, 0.0, 5.4, -16, 0.1)   # campanitas del gran momento (pico a 2,25 s)
place('554312', 55.2, 0.0, 6.0, -24, 0.6)          # brillos
place('498180', 64.5, 0.0, 25.0, -26, 1.0)         # aleteo
for t0 in (68.0, 72.5, 76.8): place('351408', t0 - 2.25, 1.5, 2.0, -22, 0.1)
pk = np.abs(out).max(); out *= min(1.0, 0.89 / pk)
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'f32le', '-ar', str(SR), '-ac', '2', '-i', '-', 'ep28_musica.wav'],
               input=out.astype(np.float32).tobytes(), check=True)
print('ok')
