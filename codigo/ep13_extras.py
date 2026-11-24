"""Episodio 13 — miniatura y short vertical.
Uso: python3 ep13_extras.py miniatura          -> ep03_miniatura.png (1920x1080)
     python3 ep13_extras.py short [a b]        -> cuadros crudos 1080x1920 por stdout (59 s)
     python3 ep13_extras.py short_stills 5 30  -> PNG sueltos del short"""
import cairo, math, os, sys
import ep13_buenos_dias as E
from amigos import hexc, OUT
from logos import word, sparkle

# ---------------- miniatura ----------------
def miniatura(path):
    W, H = 1920, 1080
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(s)
    c.save(); c.translate(W / 2, H / 2); c.scale(1.1, 1.1); c.translate(-960, -560)
    E.world(c, 40.0); c.restore()
    word(c, '¡Buenos días,', 620, 150, 140, tilt=0.06, outline=12)
    word(c, 'selva!', 620, 300, 150, start=4, tilt=0.06, outline=12)
    s.write_to_png(path)

# ---------------- short vertical ----------------
SW, SH = 1080, 1920
T0, T1 = 25.0, 84.0
TOP, BOX_H = 300, 1350
Z = BOX_H / 1080
VIEW_W = SW / Z

def cam_x(t):
    return max(VIEW_W / 2, min(1920 - VIEW_W / 2, E.kf(t, [(25, 1300), (29, 1180), (31, 1000), (52, 700), (58.5, 700), (59.5, 1180), (65.5, 1180), (67, 960)])))

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
    acts = [a for a in E.ACTIONS if a[0] <= t < a[1]]
    if t < 31:
        sc = E.K_back(ts / 0.5)
        word(c, '¡Buenos días!', SW / 2, 185, 110 * sc + 0.01, tilt=0.05, outline=9)
    elif acts:
        a0, a1, txt = acts[0]; sc = E.K_back((t - a0) / 0.4)
        word(c, txt, SW / 2, 185, 84 * sc + 0.01, tilt=0.05, outline=8)
    else:
        sc = E.K_back((t - 72.5) / 0.5)
        word(c, '¿Lo hacés', SW / 2, 125, 100 * sc + 0.01, tilt=0.06, outline=8)
        word(c, 'conmigo?', SW / 2, 245, 104 * sc + 0.01, start=2, tilt=0.06, outline=8)
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
        miniatura('ep13_miniatura.png')
    else:
        surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, SW, SH); c = cairo.Context(surf)
        if args[0] == 'short_stills':
            for ts in map(float, args[1:]):
                c.save(); short_frame(c, ts); c.restore(); surf.write_to_png(f'short13_{ts}.png')
        else:
            a0, a1 = (float(args[1]), float(args[2])) if len(args) > 2 else (0, T1 - T0)
            out = sys.stdout.buffer
            for i in range(int(round(a0 * 30)), int(round(a1 * 30))):
                c.save(); short_frame(c, i / 30); c.restore(); surf.flush(); out.write(surf.get_data())
