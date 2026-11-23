"""Episodio 16 — miniatura y short vertical (plantilla nueva de short_kit).
Uso: python3 ep16_extras.py miniatura        -> ep16_miniatura.png (1280x720)
     python3 ep16_extras.py short [a b]      -> cuadros crudos 1080x1920 por stdout (43 s)
     python3 ep16_extras.py stills 0 20      -> PNG sueltos del short"""
import cairo, math, sys
import ep16_chipa as E
from amigos import hexc, OUT
from logos import word
from short_kit import SW, SH, FPS, END, top_title, end_card, logo_band

# ---------------- miniatura ----------------
def miniatura(path):
    W, H = 1280, 720
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(s)
    c.save(); c.scale(1.05, 1.05); c.translate(-560, -250)
    E.world(c, 93.6); c.restore()
    word(c, '¡Chipá con Mamá Coco!', 640, 95, 82, tilt=0.04, outline=9)
    word(c, 'Receta fácil', 1080, 660, 62, colors=['#FF7043'], tilt=-0.05, outline=7)
    s.write_to_png(path)

# ---------------- short ----------------
# (inicio en el short, inicio en el episodio, cámara x)  -> cortes rápidos de la historia
SEGS = [(0.0, 7.0, 900), (4.0, 15.5, 520), (8.0, 35.5, 900), (14.0, 47.0, 900), (19.0, 57.5, 900),
        (25.0, 70.0, 1050), (29.0, 81.5, 1420), (34.0, 89.0, 1300), (37.0, 98.5, 820)]
STORY = 40.0
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
    g = cairo.LinearGradient(0, 0, 0, SH)
    g.add_color_stop_rgb(0, *hexc('#FFB74D')[:3]); g.add_color_stop_rgb(1, *hexc('#FF7043')[:3])
    c.set_source(g); c.paint()
    x = max(VIEW_W / 2, min(1920 - VIEW_W / 2, cx))
    c.save(); c.rectangle(0, TOP, SW, BOX_H); c.clip()
    c.translate(0, TOP); c.scale(Z, Z); c.translate(-(x - VIEW_W / 2), 0)
    E.world(c, t); c.restore()
    c.rectangle(0, TOP, SW, BOX_H); c.set_source_rgba(*OUT); c.set_line_width(10); c.stroke()
    TT = [(0, '¡Chipá', 'para chicos!'), (4, '1. ¡Manos', 'limpias!'), (8, '2. Almidón,', 'queso y sal'), (14, '3. Manteca', 'y huevos'),
          (19, '4. Leche', 'y a amasar'), (25, '5. ¡Hacemos', 'bolitas!'), (29, '6. Al horno', '¡con un adulto!'), (34, '¡Quedaron', 'doraditos!'),
          (37, '¡A compartir!', None)]
    for k in range(len(TT) - 1, -1, -1):
        if ts >= TT[k][0]:
            top_title(c, ts, TT[k][0], TT[k][1], TT[k][2], first=(k == 0)); break
    logo_band(c)

if __name__ == '__main__':
    args = sys.argv[1:]
    if args[0] == 'miniatura':
        miniatura('ep16_miniatura.png')
    else:
        surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, SW, SH); c = cairo.Context(surf)
        if args[0] == 'stills':
            for ts in map(float, args[1:]):
                c.save(); frame(c, ts); c.restore(); surf.write_to_png(f'short16_{ts}.png')
        else:
            a0, a1 = (float(args[1]), float(args[2])) if len(args) > 2 else (0, DUR)
            out = sys.stdout.buffer
            for i in range(int(round(a0 * FPS)), int(round(a1 * FPS))):
                c.save(); frame(c, i / FPS); c.restore(); surf.flush(); out.write(surf.get_data())
