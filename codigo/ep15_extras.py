"""Episodio 15 — miniatura y short vertical (plantilla nueva de short_kit).
Uso: python3 ep15_extras.py miniatura        -> ep15_miniatura.png (1280x720)
     python3 ep15_extras.py short [a b]      -> cuadros crudos 1080x1920 por stdout (41.5 s)
     python3 ep15_extras.py stills 0 20      -> PNG sueltos del short"""
import cairo, math, sys
import ep15_navidad as E
from amigos import hexc, OUT
from logos import word
from short_kit import SW, SH, FPS, END, top_title, end_card, logo_band

# ---------------- miniatura ----------------
def miniatura(path):
    W, H = 1280, 720
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(s)
    c.save(); c.scale(W / 1920 * 1.12, W / 1920 * 1.12); c.translate(-60, -60)
    E.world(c, 72.6); c.restore()
    word(c, '¡Navidad', 330, 115, 110, colors=['#E53935', '#43A047', '#FFD600'], tilt=0.06, outline=10)
    word(c, 'en la selva!', 330, 225, 92, colors=['#43A047', '#FFD600', '#E53935'], tilt=0.06, outline=9)
    s.write_to_png(path)

# ---------------- short ----------------
# (inicio en el short, inicio en el episodio, cámara x)  -> cortes rápidos de la historia
SEGS = [(0.0, 13.6, 520), (4.0, 18.2, 1450), (8.0, 23.3, 1150), (14.5, 31.5, 1000), (19.5, 43.6, 1060),
        (22.5, 47.0, 1150), (26.5, 56.0, 960), (30.5, 69.0, 640)]
STORY = 38.5
DUR = STORY + END
TOP, BOX_H = 380, 1240
Z = BOX_H / 1080
VIEW_W = SW / Z

def seg(ts):
    for k in range(len(SEGS) - 1, -1, -1):
        if ts >= SEGS[k][0]: return SEGS[k]

def frame(c, ts):
    if ts >= STORY:
        end_card(c, ts - STORY); return
    s0, e0, cx = seg(ts)
    t = e0 + (ts - s0)
    nt = E.night(t)
    g = cairo.LinearGradient(0, 0, 0, SH)
    top = ('#29B6F6', '#141048')[nt > 0.5]; bot = ('#2E7D32', '#1B5E20')[nt > 0.5]
    g.add_color_stop_rgb(0, *hexc(top)[:3]); g.add_color_stop_rgb(1, *hexc(bot)[:3])
    c.set_source(g); c.paint()
    x = max(VIEW_W / 2, min(1920 - VIEW_W / 2, cx))
    c.save(); c.rectangle(0, TOP, SW, BOX_H); c.clip()
    c.translate(0, TOP); c.scale(Z, Z); c.translate(-(x - VIEW_W / 2), 0)
    E.world(c, t); c.restore()
    c.rectangle(0, TOP, SW, BOX_H); c.set_source_rgba(*OUT); c.set_line_width(10); c.stroke()
    if ts < 8.0: top_title(c, ts, 0, 'En la selva', '¡no hay pinos!', first=True)
    elif ts < 26.5: top_title(c, ts, 8.0, '¡Decoramos', 'la palmera!')
    elif ts < 30.5: top_title(c, ts, 26.5, '¡Se prenden', 'las lucecitas!')
    else:
        k = 0 if ts < 34.5 else 1
        a, b, _ = E.LYRICS[k]
        top_title(c, ts, 30.5 + 4 * k, a, b)
    logo_band(c)

if __name__ == '__main__':
    args = sys.argv[1:]
    if args[0] == 'miniatura':
        miniatura('ep15_miniatura.png')
    else:
        surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, SW, SH); c = cairo.Context(surf)
        if args[0] == 'stills':
            for ts in map(float, args[1:]):
                c.save(); frame(c, ts); c.restore(); surf.write_to_png(f'short15_{ts}.png')
        else:
            a0, a1 = (float(args[1]), float(args[2])) if len(args) > 2 else (0, DUR)
            out = sys.stdout.buffer
            for i in range(int(round(a0 * FPS)), int(round(a1 * FPS))):
                c.save(); frame(c, i / FPS); c.restore(); surf.flush(); out.write(surf.get_data())
