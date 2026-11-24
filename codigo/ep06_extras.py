"""Episodio 6 — miniatura de YouTube y short vertical (Tito se va a dormir).
Uso: python3 ep06_extras.py miniatura          -> ep01_miniatura.png (1920x1080)
     python3 ep06_extras.py short [t0 t1]      -> cuadros crudos 1080x1920 por stdout (40 s)
     python3 ep06_extras.py short_stills 5 30  -> PNG sueltos del short"""
import cairo, math, os, sys
import ep06_tito_a_dormir as E
from amigos import hexc, OUT
from logos import word, sparkle

NIGHT = ['#FFF59D', '#FFD54F', '#B39DDB', '#81D4FA', '#F48FB1', '#FFFFFF']

def back(p):
    p = max(0.0, min(1.0, p)); k = 1.70158
    return 1 + (k + 1) * (p - 1) ** 3 + k * (p - 1) ** 2

# ---------------- miniatura ----------------
def miniatura(path):
    W, H = 1920, 1080
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(s)
    t = 40.5
    c.save(); c.translate(W / 2, H / 2); c.scale(1.45, 1.45); c.translate(-1060, -640)
    E.world(c, t); c.restore()
    word(c, 'Tito se va', 520, 190, 160, colors=NIGHT, tilt=0.06, outline=13)
    word(c, 'a dormir', 520, 360, 160, colors=NIGHT, start=3, tilt=0.06, outline=13)
    s.write_to_png(path)

# ---------------- short vertical ----------------
SW, SH = 1080, 1920
TOP, BOX_H = 300, 1350
Z = BOX_H / 1080
VIEW_W = SW / Z
DUR = 59.0

def cam_x(t):
    x = max(560, E.kf(t, E.TITO_W)) if t < 6.5 else E.TX + 60
    return max(VIEW_W / 2, min(1920 - VIEW_W / 2, x))

LOGO = None
def logo():
    global LOGO
    if LOGO is None:
        p = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'imagenes', 'logo_perfil.png')
        LOGO = cairo.ImageSurface.create_from_png(p)
    return LOGO

def short_frame(c, t):
    g = cairo.LinearGradient(0, 0, 0, SH)
    g.add_color_stop_rgb(0, *hexc('#120F4A')[:3]); g.add_color_stop_rgb(1, *hexc('#1F7A4A')[:3])
    c.set_source(g); c.paint()
    x = cam_x(t)
    c.save(); c.rectangle(0, TOP, SW, BOX_H); c.clip()
    c.translate(0, TOP); c.scale(Z, Z); c.translate(-(x - VIEW_W / 2), 0)
    E.world(c, t); c.restore()
    c.rectangle(0, TOP, SW, BOX_H); c.set_source_rgba(*hexc('#FFF59D')); c.set_line_width(8); c.stroke()
    if t < 34:
        sc = back((t - 0.3) / 0.5)
        word(c, 'Tito se va', SW / 2, 125, 98 * sc + 0.01, colors=NIGHT, tilt=0.05, outline=8)
        word(c, 'a dormir', SW / 2, 245, 98 * sc + 0.01, colors=NIGHT, start=3, tilt=0.05, outline=8)
    else:
        sc = back((t - 34) / 0.6)
        word(c, '¡Buenas', SW / 2, 125, 105 * sc + 0.01, colors=NIGHT, tilt=0.06, outline=8)
        word(c, 'noches!', SW / 2, 245, 105 * sc + 0.01, colors=NIGHT, start=2, tilt=0.06, outline=8)
    for k in range(6):  # twinkles in the top band
        ph = (t * 0.5 + k / 6) % 1
        sparkle(c, 60 + k * 190 + (40 if k % 2 else 0), 40 + 220 * ((k * 3) % 5) / 5, 16 * math.sin(math.pi * ph), '#FFF59D')
    lg = logo(); d = 200; cy = TOP + BOX_H + 140
    c.save(); c.arc(170, cy, d / 2, 0, 2 * math.pi); c.clip()
    c.translate(170 - d / 2, cy - d / 2); c.scale(d / lg.get_width(), d / lg.get_height())
    c.set_source_surface(lg, 0, 0); c.paint(); c.restore()
    c.arc(170, cy, d / 2, 0, 2 * math.pi); c.set_source_rgba(1, 1, 1, 1); c.set_line_width(8); c.stroke()
    word(c, 'Cuentos mágicos', 640, cy - 15, 66, outline=6)
    word(c, 'de la selva', 640, cy + 65, 66, start=5, outline=6)
    a = max(1 - E.ss(0, 0.8, t), E.ss(DUR - 3.0, DUR, t)) * 0.9
    if a > 0: c.set_source_rgba(0.05, 0.04, 0.2, a); c.paint()

if __name__ == '__main__':
    args = sys.argv[1:]
    if args[0] == 'miniatura':
        miniatura('ep06_miniatura.png')
    else:
        surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, SW, SH); c = cairo.Context(surf)
        if args[0] == 'short_stills':
            for t in map(float, args[1:]):
                c.save(); short_frame(c, t); c.restore(); surf.write_to_png(f'short6_{t}.png')
        else:
            a0, a1 = (float(args[1]), float(args[2])) if len(args) > 2 else (0, DUR)
            out = sys.stdout.buffer
            for i in range(int(round(a0 * 30)), int(round(a1 * 30))):
                c.save(); short_frame(c, i / 30); c.restore(); surf.flush(); out.write(surf.get_data())
