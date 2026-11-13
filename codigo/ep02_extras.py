"""Episodio 2 — miniatura de YouTube y short vertical.
Uso: python3 ep02_extras.py miniatura          -> ep02_miniatura.png (1920x1080, se achica a 1280x720)
     python3 ep02_extras.py short              -> cuadros crudos 1080x1920 por stdout (59 s)
     python3 ep02_extras.py short_stills 5 30  -> PNG sueltos del short"""
import cairo, math, sys
import ep02_puente_del_rio as E
import amigos as A
from amigos import hexc, ellipse, fill, OUT
from logos import word, sparkle, font

# ---------------- miniatura ----------------
def miniatura(path):
    W, H = 1920, 1080
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(s)
    t = 80.6
    cx, cy, z = 1000, 640, 1.55
    c.save(); c.translate(W / 2, H / 2); c.scale(z, z); c.translate(-cx, -cy)
    E.world(c, t); c.restore()
    # big bananas in the corner to make it pop
    for (x, y, r) in ((1560, 520, 40), (1890, 470, 34), (1640, 760, 30)):
        sparkle(c, x, y, r, '#FFF59D')
    word(c, 'El puente', 760, 175, 190, tilt=0.06, outline=14)
    word(c, 'del río', 760, 355, 190, start=4, tilt=0.06, outline=14)
    s.write_to_png(path)

# ---------------- short vertical ----------------
SW, SH = 1080, 1920
T0, T1 = 63.0, 122.0                    # tramo del episodio que usa el short
TOP, BOX_H = 300, 1350                   # banda de arriba y alto de la escena
Z = BOX_H / 1080                         # zoom para que la escena llene la caja
VIEW_W = SW / Z

CAMX = [(63, 830), (69.5, 830), (71, None)]

def short_cam(t):
    cx_coco = E.kf(t, E.COCO_X)
    if t < 69.5: x = 830
    elif t < 102.5: x = cx_coco
    else: x = E.kf(t, [(102.5, cx_coco), (104.5, 470)])
    if 69.5 <= t < 71: x = 830 + (cx_coco - 830) * E.ss(69.5, 71, t)
    return max(VIEW_W / 2, min(1920 - VIEW_W / 2, x))

LOGO = None
def logo_disc():
    global LOGO
    if LOGO is None:
        import os
        p = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'imagenes', 'logo_perfil.png')
        LOGO = cairo.ImageSurface.create_from_png(p)
    return LOGO

def short_frame(c, ts):
    t = T0 + ts
    # background bands
    g = cairo.LinearGradient(0, 0, 0, SH)
    g.add_color_stop_rgb(0, *hexc('#29B6F6')[:3]); g.add_color_stop_rgb(1, *hexc('#2E7D32')[:3])
    c.set_source(g); c.paint()
    # scene
    x = short_cam(t)
    c.save(); c.rectangle(0, TOP, SW, BOX_H); c.clip()
    c.translate(0, TOP); c.scale(Z, Z); c.translate(-(x - VIEW_W / 2), 0)
    E.world(c, t); c.restore()
    c.rectangle(0, TOP, SW, BOX_H); c.set_source_rgba(*OUT); c.set_line_width(10); c.stroke()
    # top band text
    if ts < 4.0:
        sc = E.K_back(ts / 0.5)
        word(c, '¿Cómo cruzará', SW / 2, 125, 92 * sc + 0.01, tilt=0.05, outline=8)
        word(c, 'Coco el río?', SW / 2, 240, 92 * sc + 0.01, start=3, tilt=0.05, outline=8)
    elif t < 118.5:
        sc = E.K_back((ts - 4.0) / 0.5)
        word(c, 'El puente', SW / 2, 125, 100 * sc + 0.01, tilt=0.05, outline=8)
        word(c, 'del río', SW / 2, 245, 100 * sc + 0.01, start=4, tilt=0.05, outline=8)
    else:
        sc = E.K_back((t - 118.5) / 0.5)
        word(c, '¡Juntos', SW / 2, 125, 105 * sc + 0.01, tilt=0.06, outline=8)
        word(c, 'se puede!', SW / 2, 245, 105 * sc + 0.01, start=2, tilt=0.06, outline=8)
    # bottom band: logo + channel name
    lg = logo_disc(); d = 200
    c.save(); c.arc(170, TOP + BOX_H + 140, d / 2, 0, 2 * math.pi); c.clip()
    c.translate(170 - d / 2, TOP + BOX_H + 140 - d / 2); c.scale(d / lg.get_width(), d / lg.get_height())
    c.set_source_surface(lg, 0, 0); c.paint(); c.restore()
    c.arc(170, TOP + BOX_H + 140, d / 2, 0, 2 * math.pi); c.set_source_rgba(1, 1, 1, 1); c.set_line_width(8); c.stroke()
    word(c, 'Cuentos mágicos', 640, TOP + BOX_H + 125, 66, outline=6)
    word(c, 'de la selva', 640, TOP + BOX_H + 205, 66, start=5, outline=6)
    # fades
    a = max(1 - E.ss(0, 0.4, ts), E.ss(T1 - T0 - 1.0, T1 - T0, ts))
    if a > 0: c.set_source_rgba(1, 1, 1, a); c.paint()

if __name__ == '__main__':
    args = sys.argv[1:]
    if args[0] == 'miniatura':
        miniatura('ep02_miniatura.png')
    else:
        surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, SW, SH); c = cairo.Context(surf)
        if args[0] == 'short_stills':
            for ts in map(float, args[1:]):
                c.save(); short_frame(c, ts); c.restore(); surf.write_to_png(f'short_{ts}.png')
        else:
            a0, a1 = (float(args[1]), float(args[2])) if len(args) > 2 else (0, T1 - T0)
            out = sys.stdout.buffer
            for i in range(int(round(a0 * 30)), int(round(a1 * 30))):
                c.save(); short_frame(c, i / 30); c.restore(); surf.flush(); out.write(surf.get_data())
