"""Episodio 12 — miniatura de YouTube y short vertical (Las burbujas mágicas).
Uso: python3 ep12_extras.py miniatura          -> ep03_miniatura.png (1920x1080)
     python3 ep12_extras.py short [a b]        -> cuadros crudos 1080x1920 por stdout (59 s)
     python3 ep12_extras.py short_stills 5 30  -> PNG sueltos del short"""
import cairo, math, os, sys
import ep12_burbujas_magicas as E
from amigos import hexc, OUT
from logos import word, sparkle

# ---------------- miniatura ----------------
def miniatura(path):
    W, H = 1920, 1080
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(s)
    c.save(); c.translate(W / 2, H / 2); c.scale(1.1, 1.1); c.translate(-960, -560)
    E.world(c, 69.5)
    for (x, y, r) in ((300, 300, 60), (1650, 420, 50), (560, 180, 40), (1400, 250, 35)): E.soap_bubble(c, x, y, r, 1.0)
    c.restore()
    word(c, 'Las burbujas', 660, 130, 125, tilt=0.06, outline=11)
    word(c, 'mágicas', 660, 265, 135, start=4, tilt=0.06, outline=11)
    s.write_to_png(path)

# ---------------- short vertical ----------------
SW, SH = 1080, 1920
T0, T1 = 18.0, 77.0
TOP, BOX_H = 300, 1350
Z = BOX_H / 1080
VIEW_W = SW / Z

def cam_x(t):
    keys = [(18, 1100), (21, 760), (25, 760), (27, 720), (31, 450), (35, 450), (37, 1000), (41, 1150), (47, 1150), (49, 1250),
            (53, 1250), (57, 1250), (60, 1250), (64, 1150), (72, 960)]
    return max(VIEW_W / 2, min(1920 - VIEW_W / 2, E.kf(t, keys)))

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
    if t < 59.5:
        sc = E.K_back(ts / 0.5)
        word(c, '¡Burbujas', SW / 2, 125, 104 * sc + 0.01, tilt=0.05, outline=8)
        word(c, 'mágicas!', SW / 2, 245, 104 * sc + 0.01, start=3, tilt=0.05, outline=8)
    else:
        sc = E.K_back((t - 59.5) / 0.5)
        word(c, '¡Coco está', SW / 2, 125, 100 * sc + 0.01, tilt=0.06, outline=8)
        word(c, 'volando!', SW / 2, 245, 108 * sc + 0.01, start=2, tilt=0.06, outline=8)
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
        miniatura('ep12_miniatura.png')
    else:
        surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, SW, SH); c = cairo.Context(surf)
        if args[0] == 'short_stills':
            for ts in map(float, args[1:]):
                c.save(); short_frame(c, ts); c.restore(); surf.write_to_png(f'short12_{ts}.png')
        else:
            a0, a1 = (float(args[1]), float(args[2])) if len(args) > 2 else (0, T1 - T0)
            out = sys.stdout.buffer
            for i in range(int(round(a0 * 30)), int(round(a1 * 30))):
                c.save(); short_frame(c, i / 30); c.restore(); surf.flush(); out.write(surf.get_data())
