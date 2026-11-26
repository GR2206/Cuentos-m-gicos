"""Bloque de 60 s que se repite sin corte: los amigos dormidos bajo las estrellas (escena final del ep. 25).
Sirve para el final largo de las recopilaciones "para dormir" (se repite N veces con el concat de ffmpeg).
Para que empalme, los últimos 3 s se funden con el principio: L(u) = (1-s)·F(u) + s·F(u-60).
Uso: python3 cancion_de_cuna_loop.py [range a b] | stills 0 30 | musica"""
import cairo, math, sys
import numpy as np
import ep25_noche_estrellada as E
from ep02_puente_del_rio import ss

W, H, FPS = 1920, 1080, 30
LOOP = 60.0
T0 = 107.0        # todos ya dormidos, la luna con los ojos cerrados
XF = 3.0

def scene(c, u):
    E.frame(c, T0 + u)

def frame(c, surf2, c2, u):
    scene(c, u)
    s = ss(LOOP - XF, LOOP, u)
    if s > 0:
        c2.save(); scene(c2, u - LOOP); c2.restore()
        c.set_source_surface(surf2, 0, 0); c.paint_with_alpha(s)

def musica():
    """canción de cuna de 60 s exactos, con la cola fundida al principio para que empalme."""
    import subprocess, importlib.util, os
    spec = importlib.util.spec_from_file_location('m25', os.path.join(os.path.dirname(__file__), 'ep25_musica.py'))
    src = open(spec.origin).read()
    lib = src[:src.index('# ---------- partitura')]
    lib = lib.replace('DUR = 110.0', 'DUR = 66.0')
    score = '''
LUL = [(72, 2), (69, 1), (67, 2), (69, 1), (72, 2), (74, 1), (72, 3), (67, 2), (65, 1), (64, 2), (65, 1), (67, 3), (64, 3)]
CH = [(60, 64, 67), (57, 60, 64), (53, 57, 60), (55, 59, 62)]
for k in range(20): add(k * 3.0, pad(CH[k % 4], 3.3, 0.028))
t = 0.5
for rep in range(2):
    for (m, d) in LUL: add(t, musicbox(m, 0.075, 2.8)); t += d * 0.95
    t += 1.6
for k in range(12): add(2.0 + 5.0 * k, bell(91 + (k * 7) % 12, 0.012, 1.6), np.sin(k))
'''
    code = lib + score
    g = {}
    exec(compile(code, 'cuna', 'exec'), g)
    L, R = g['L'], g['R']; SR = g['SR']
    n = int(LOOP * SR); x = int(XF * SR)
    L2, R2 = L[:n].copy(), R[:n].copy()
    w = np.linspace(0, 1, x)
    L2[:x] = L2[:x] * w + L[n:n + x] * (1 - w)
    R2[:x] = R2[:x] * w + R[n:n + x] * (1 - w)
    st = np.stack([L2, R2], 1); st /= max(1e-6, np.abs(st).max()) / 0.6
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'f32le', '-ar', str(SR), '-ac', '2', '-i', '-', 'cuna_loop.wav'],
                   input=st.astype(np.float32).tobytes(), check=True)
    print('ok')

if __name__ == '__main__':
    args = sys.argv[1:]
    if args and args[0] == 'musica':
        musica(); sys.exit()
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(surf)
    surf2 = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c2 = cairo.Context(surf2)
    if args and args[0] == 'stills':
        for u in map(float, args[1:]):
            c.save(); frame(c, surf2, c2, u); c.restore(); surf.write_to_png(f'cuna_{u}.png')
    else:
        a, b = (float(args[1]), float(args[2])) if args and args[0] == 'range' else (0, LOOP)
        out = sys.stdout.buffer
        for i in range(int(round(a * FPS)), int(round(b * FPS))):
            c.save(); frame(c, surf2, c2, i / FPS); c.restore(); surf.flush(); out.write(surf.get_data())
