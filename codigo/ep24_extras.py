"""Episodio 24 — miniatura y short vertical (con la voz de Malena).
Uso: python3 ep24_extras.py miniatura | short [a b] | stills 0 20
El audio del short (música del episodio + voz) se arma con `python3 ep24_extras.py audio voz.wav`."""
import cairo, sys
import ep24_barrilete as E
from logos import word
from short_montage import montage, cli

def draw(c, t): E.frame(c, t)

# (inicio en el short, inicio en el episodio, x de cámara)
SEGS = [(0.0, 16.6, 650), (4.5, 23.0, 1100), (8.8, 30.8, 1150), (12.3, 46.8, 1250), (16.3, 52.8, 1300),
        (20.6, 59.6, 1300), (26.6, 66.0, 1300), (29.4, 80.0, 1350), (33.4, 95.8, 960)]
TT = [(0, '¡El viento se llevó', 'el barrilete!'), (4.5, '¡Hay que', 'alcanzarlo!'), (8.8, '¡Coco salta!', None),
      (12.3, '¡Quedó', 'enganchado!'), (16.3, 'Pipa', 'no llega…'), (20.6, '¡Una torre', 'de amigos!'),
      (26.6, '¡Lo tenemos!', None), (29.4, '¡Más alto', 'que nunca!'), (33.4, '¡Juntos llegamos', 'más alto!')]
STORY = 38.5
frame, DUR = montage(draw, SEGS, TT, STORY, ('#29B6F6', '#8BC34A'))

# frases de la voz: (inicio y fin en el audio de Malena, momento del short)
VOZ = [((6.28, 10.30), 0.1), ((10.62, 14.38), 4.6), ((14.73, 17.65), 9.0), ((22.12, 25.55), 12.5), ((25.90, 29.78), 16.4),
       ((30.20, 35.93), 20.7), ((36.20, 38.33), 26.7), ((45.48, 48.10), 33.6)]

def audio(voz_wav, out='ep24_short_audio.wav'):
    import numpy as np, subprocess
    SR = 48000
    def load(p):
        raw = subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', p, '-ac', '2', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True, check=True).stdout
        return np.frombuffer(raw, np.float32).reshape(-1, 2).copy()
    mus, voz, endm = load('ep24_musica.wav'), load(voz_wav), load('ep21_short_musica.wav')
    total = int((DUR) * SR); bed = np.zeros((total, 2), np.float32)
    xf = int(0.25 * SR)
    for k, (s0, e0, _) in enumerate(SEGS):
        s1 = SEGS[k + 1][0] if k + 1 < len(SEGS) else STORY
        a, n = int(s0 * SR), int((s1 - s0) * SR) + xf
        piece = mus[int(e0 * SR): int(e0 * SR) + n].copy()
        if len(piece) < n: piece = np.pad(piece, ((0, n - len(piece)), (0, 0)))
        ramp = np.linspace(0, 1, xf)[:, None]
        if k > 0: piece[:xf] *= ramp
        piece[-xf:] *= ramp[::-1]
        end = min(total, a + n); bed[a:end] += piece[:end - a]
    tail = endm[int(38.5 * SR): int(38.5 * SR) + total - int(STORY * SR)]   # jingle de la tarjeta final
    bed[int(STORY * SR): int(STORY * SR) + len(tail)] += tail
    gain = np.ones(total, np.float32); vtrack = np.zeros((total, 2), np.float32)
    for (vs, ve), at in VOZ:
        seg = voz[int((vs - 0.08) * SR): int((ve + 0.15) * SR)].copy()
        f = int(0.05 * SR); seg[:f] *= np.linspace(0, 1, f)[:, None]; seg[-f:] *= np.linspace(1, 0, f)[:, None]
        a = int(at * SR); vtrack[a:a + len(seg)] += seg[:total - a]
        w0, w1 = max(0, int((at - 0.35) * SR)), int((at + ve - vs + 0.4) * SR); r = int(0.3 * SR)
        g = np.ones(total, np.float32); g[w0:w1] = 0.28
        g[max(0, w0 - r):w0] = np.linspace(1, 0.28, w0 - max(0, w0 - r)); g[w1:w1 + r] = np.linspace(0.28, 1, len(g[w1:w1 + r]))
        gain = np.minimum(gain, g)
    vtrack *= 10 ** (-1.5 / 20) / max(1e-6, np.abs(vtrack).max())
    mix = bed * gain[:, None] * 0.55 + vtrack
    mix /= max(1.0, np.abs(mix).max() / 0.95)
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'f32le', '-ar', str(SR), '-ac', '2', '-i', '-',
                    '-af', 'loudnorm=I=-15:TP=-1.5:LRA=11', '-ar', str(SR), out], input=mix.astype(np.float32).tobytes(), check=True)

def miniatura(path):
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, 1280, 720); c = cairo.Context(s)
    c.save(); c.scale(0.95, 0.95); c.translate(-280, -30); E.frame(c, 65.0); c.restore()
    word(c, '¡El barrilete', 400, 110, 95, tilt=0.05, outline=10)
    word(c, 'perdido!', 400, 215, 105, start=3, tilt=0.05, outline=10)
    s.write_to_png(path)

if __name__ == '__main__':
    if sys.argv[1:2] == ['audio']: audio(sys.argv[2])
    else: cli(frame, DUR, 'ep24', miniatura)
