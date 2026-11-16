"""Recopilación de aventuritas: cierre animado (8 s) y miniatura.
Uso: python3 recopilacion.py cierre      -> cuadros crudos 1920x1080 por stdout (8 s)
     python3 recopilacion.py miniatura   -> recop_miniatura.png
     python3 recopilacion.py stills 3 6  -> PNG sueltos del cierre"""
import cairo, math, os, sys
import amigos as A
from amigos import hexc, ellipse, fill, OUT
from logos import word, sparkle
from ep02_puente_del_rio import ss, K_back
import ep10_cruzando_el_bosque as E10

W, H, FPS = 1920, 1080, 30
DUR = 8.0
HERE = os.path.dirname(os.path.abspath(__file__))
BANNER = cairo.ImageSurface.create_from_png(os.path.join(HERE, '..', 'imagenes', 'banner_canal.png'))

def cierre(c, t):
    s = W / BANNER.get_width()
    c.save(); c.scale(s, s); c.set_source_surface(BANNER, 0, 0); c.paint(); c.restore()
    sc = K_back((t - 0.6) / 0.6)
    word(c, '¡Hasta la próxima', W / 2, 170, 115 * sc + 0.01, tilt=0.06, outline=10)
    word(c, 'aventura!', W / 2, 310, 125 * sc + 0.01, start=3, tilt=0.06, outline=10)
    for k in range(14):
        ph = (t * 0.6 + k / 14) % 1
        sparkle(c, 120 + k * 130, 420 + 260 * ((k * 5) % 7) / 7, 30 * math.sin(math.pi * ph), '#FFF59D' if k % 2 else '#FFFFFF')
    a = max(1 - ss(0, 0.6, t), ss(DUR - 1.5, DUR, t))
    if a > 0: c.set_source_rgba(1, 1, 1, a); c.paint()

def miniatura(path):
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(s)
    c.save(); c.translate(W / 2, H / 2); c.scale(1.12, 1.12); c.translate(-960, -600)
    E10.frame(c, 98.0); c.restore()
    word(c, '¡Todas las', 620, 150, 140, tilt=0.06, outline=12)
    word(c, 'aventuritas!', 620, 300, 140, start=3, tilt=0.06, outline=12)
    # badge
    c.save(); c.translate(1580, 230); c.rotate(-0.12)
    ellipse(c, 0, 0, 200, 130); fill(c, hexc('#FF4081'), OUT, 8)
    word(c, '+15', 0, 0, 120, colors=['#FFFFFF'], outline=6)
    word(c, 'minutos', 0, 80, 60, colors=['#FFF59D'], outline=5)
    c.restore()
    s.write_to_png(path)

if __name__ == '__main__':
    args = sys.argv[1:]
    if args[0] == 'miniatura':
        miniatura('recop_miniatura.png')
    else:
        surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(surf)
        if args[0] == 'stills':
            for t in map(float, args[1:]):
                c.save(); cierre(c, t); c.restore(); surf.write_to_png(f'cierre_{t}.png')
        else:
            out = sys.stdout.buffer
            for i in range(int(DUR * FPS)):
                c.save(); cierre(c, i / FPS); c.restore(); surf.flush(); out.write(surf.get_data())
