"""Episodio 8 — miniatura de YouTube y short vertical (El arcoíris perdido).
Uso: python3 ep08_extras.py miniatura          -> ep03_miniatura.png (1920x1080)
     python3 ep08_extras.py short [a b]        -> cuadros crudos 1080x1920 por stdout (59 s)
     python3 ep08_extras.py short_stills 5 30  -> PNG sueltos del short"""
import cairo, math, os, sys
import ep08_arcoiris_perdido as E
from amigos import hexc, OUT
from logos import word, sparkle

# ---------------- miniatura ----------------
def miniatura(path):
    W, H = 1920, 1080
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(s)
    t = 49.0   # three colors back, the rest still missing
    c.save(); c.translate(W / 2, H / 2); c.scale(1.12, 1.12); c.translate(-960, -600)
    E.world(c, t)
    for k in (3, 4, 5):  # show the missing colors as glowing orbs to find
        x, y = [(260, 330), (1090, 890), (1300, 860)][k - 3]
        E.orb(c, x, y, E.COLORS[k][1], t, 30, 1.0)
    c.restore()
    word(c, 'El arcoíris', 960, 160, 150, tilt=0.06, outline=12)
    word(c, 'perdido', 960, 310, 150, start=4, tilt=0.06, outline=12)
    s.write_to_png(path)

# ---------------- short vertical ----------------
SW, SH = 1080, 1920
T0, T1 = 6.0, 65.0
TOP, BOX_H = 300, 1350
Z = BOX_H / 1080
VIEW_W = SW / Z

def cam_x(t):
    keys = [(6, 960), (16, 760)]
    for k, (fx, _) in enumerate(E.FOCUS[:4]):
        s = E.STARTS[k]; keys += [(s + 3.5, fx), (s + 9.5, fx), (s + 11.5, 760)]
    keys = sorted(keys)
    x = E.kf(t, keys)
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
    if t < 16:
        sc = E.K_back(ts / 0.5)
        word(c, '¡El arcoíris', SW / 2, 125, 100 * sc + 0.01, tilt=0.05, outline=8)
        word(c, 'perdió sus colores!', SW / 2, 245, 84 * sc + 0.01, start=3, tilt=0.05, outline=7)
    else:
        found = [k for k in range(6) if t >= E.STARTS[k] + 6.5]
        if found and t < E.STARTS[found[-1]] + 9.8:
            k = found[-1]; sc = E.K_back((t - E.STARTS[k] - 6.5) / 0.4)
            word(c, E.COLORS[k][0], SW / 2, 190, 140 * sc + 0.01, colors=[E.COLORS[k][1]], tilt=0.05, outline=10)
        else:
            word(c, '¿Dónde están', SW / 2, 125, 96, tilt=0.05, outline=8)
            word(c, 'los colores?', SW / 2, 245, 96, start=3, tilt=0.05, outline=8)
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
        miniatura('ep08_miniatura.png')
    else:
        surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, SW, SH); c = cairo.Context(surf)
        if args[0] == 'short_stills':
            for ts in map(float, args[1:]):
                c.save(); short_frame(c, ts); c.restore(); surf.write_to_png(f'short8_{ts}.png')
        else:
            a0, a1 = (float(args[1]), float(args[2])) if len(args) > 2 else (0, T1 - T0)
            out = sys.stdout.buffer
            for i in range(int(round(a0 * 30)), int(round(a1 * 30))):
                c.save(); short_frame(c, i / 30); c.restore(); surf.flush(); out.write(surf.get_data())
