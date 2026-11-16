"""Episodio 4 — miniatura de YouTube y short vertical (La lluvia mágica).
Uso: python3 ep04_extras.py miniatura          -> ep03_miniatura.png (1920x1080)
     python3 ep04_extras.py short [a b]        -> cuadros crudos 1080x1920 por stdout (59 s)
     python3 ep04_extras.py short_stills 5 30  -> PNG sueltos del short"""
import cairo, math, os, sys
import ep04_lluvia_magica as E
from amigos import hexc, OUT
from logos import word, sparkle

# ---------------- miniatura ----------------
def miniatura(path):
    W, H = 1920, 1080
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(s)
    t = 47.0
    c.save(); c.translate(W / 2, H / 2); c.scale(1.4, 1.4); c.translate(-975, -610)
    E.world(c, t); c.restore()
    word(c, 'La lluvia', 480, 175, 165, tilt=0.06, outline=13)
    word(c, 'mágica', 1440, 175, 165, start=4, tilt=0.06, outline=13)
    s.write_to_png(path)

# ---------------- short vertical ----------------
SW, SH = 1080, 1920
T0, T1 = 27.0, 86.0
TOP, BOX_H = 300, 1350
Z = BOX_H / 1080
VIEW_W = SW / Z

def cam_x(t):
    x = E.kf(t, [(27, 960), (71.5, 960), (73, 700), (79.5, 700), (81.5, 1120)])
    return max(VIEW_W / 2, min(1920 - VIEW_W / 2, x))

LOGO = None
def logo():
    global LOGO
    if LOGO is None:
        p = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'imagenes', 'logo_perfil.png')
        LOGO = cairo.ImageSurface.create_from_png(p)
    return LOGO

def short_frame(c, ts):
    t = T0 + ts
    g = cairo.LinearGradient(0, 0, 0, SH)
    g.add_color_stop_rgb(0, *hexc('#29B6F6')[:3]); g.add_color_stop_rgb(1, *hexc('#2E7D32')[:3])
    c.set_source(g); c.paint()
    x = cam_x(t)
    c.save(); c.rectangle(0, TOP, SW, BOX_H); c.clip()
    c.translate(0, TOP); c.scale(Z, Z); c.translate(-(x - VIEW_W / 2), 0)
    E.world(c, t); c.restore()
    c.rectangle(0, TOP, SW, BOX_H); c.set_source_rgba(*OUT); c.set_line_width(10); c.stroke()
    if t < 66:
        sc = E.K_back(ts / 0.5)
        word(c, '¡Llueve', SW / 2, 125, 100 * sc + 0.01, tilt=0.05, outline=8)
        word(c, 'en la selva!', SW / 2, 245, 100 * sc + 0.01, start=3, tilt=0.05, outline=8)
    elif t < 72:
        sc = E.K_back((t - 66) / 0.5)
        word(c, '¡Un arcoíris!', SW / 2, 185, 110 * sc + 0.01, tilt=0.06, outline=9)
    else:
        sc = E.K_back((t - 72) / 0.5)
        word(c, '¡A saltar en', SW / 2, 125, 100 * sc + 0.01, tilt=0.06, outline=8)
        word(c, 'los charcos!', SW / 2, 245, 100 * sc + 0.01, start=2, tilt=0.06, outline=8)
    lg = logo(); d = 200; cy = TOP + BOX_H + 140
    c.save(); c.arc(170, cy, d / 2, 0, 2 * math.pi); c.clip()
    c.translate(170 - d / 2, cy - d / 2); c.scale(d / lg.get_width(), d / lg.get_height())
    c.set_source_surface(lg, 0, 0); c.paint(); c.restore()
    c.arc(170, cy, d / 2, 0, 2 * math.pi); c.set_source_rgba(1, 1, 1, 1); c.set_line_width(8); c.stroke()
    word(c, 'Cuentos mágicos', 640, cy - 15, 66, outline=6)
    word(c, 'de la selva', 640, cy + 65, 66, start=5, outline=6)
    a = max(1 - E.ss(0, 0.4, ts), E.ss(T1 - T0 - 1.0, T1 - T0, ts))
    if a > 0: c.set_source_rgba(1, 1, 1, a); c.paint()

if __name__ == '__main__':
    args = sys.argv[1:]
    if args[0] == 'miniatura':
        miniatura('ep04_miniatura.png')
    else:
        surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, SW, SH); c = cairo.Context(surf)
        if args[0] == 'short_stills':
            for ts in map(float, args[1:]):
                c.save(); short_frame(c, ts); c.restore(); surf.write_to_png(f'short4_{ts}.png')
        else:
            a0, a1 = (float(args[1]), float(args[2])) if len(args) > 2 else (0, T1 - T0)
            out = sys.stdout.buffer
            for i in range(int(round(a0 * 30)), int(round(a1 * 30))):
                c.save(); short_frame(c, i / 30); c.restore(); surf.flush(); out.write(surf.get_data())
