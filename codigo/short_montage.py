"""Short vertical armado con tramos de un episodio (plantilla nueva de short_kit).
montage(draw, SEGS, TT, STORY, bg) devuelve frame(c, ts) y DUR:
  draw(c, t)   dibuja el episodio 1920x1080 en el instante t
  SEGS         [(inicio en el short, inicio en el episodio, x de cámara en pantalla)]
  TT           [(inicio, línea 1, línea 2 o None)] títulos de arriba (el primero aparece desde el cuadro 1)
  bg           (color de arriba, color de abajo) del fondo vertical"""
import cairo, sys
from amigos import hexc, OUT
from short_kit import SW, SH, FPS, END, top_title, end_card, logo_band

TOP, BOX_H = 380, 1240
Z = BOX_H / 1080
VIEW_W = SW / Z

def montage(draw, SEGS, TT, STORY, bg):
    def frame(c, ts):
        if ts >= STORY:
            end_card(c, ts - STORY); return
        for k in range(len(SEGS) - 1, -1, -1):
            if ts >= SEGS[k][0]: s0, e0, cx = SEGS[k]; break
        t = e0 + (ts - s0)
        g = cairo.LinearGradient(0, 0, 0, SH)
        g.add_color_stop_rgb(0, *hexc(bg[0])[:3]); g.add_color_stop_rgb(1, *hexc(bg[1])[:3])
        c.set_source(g); c.paint()
        x = max(VIEW_W / 2, min(1920 - VIEW_W / 2, cx))
        c.save(); c.rectangle(0, TOP, SW, BOX_H); c.clip()
        c.translate(0, TOP); c.scale(Z, Z); c.translate(-(x - VIEW_W / 2), 0)
        draw(c, t); c.restore()
        c.rectangle(0, TOP, SW, BOX_H); c.set_source_rgba(*OUT); c.set_line_width(10); c.stroke()
        for k in range(len(TT) - 1, -1, -1):
            if ts >= TT[k][0]:
                top_title(c, ts, TT[k][0], TT[k][1], TT[k][2], first=(k == 0)); break
        logo_band(c)
    return frame, STORY + END

def cli(frame, DUR, tag, miniatura=None):
    args = sys.argv[1:]
    if args and args[0] == 'miniatura':
        miniatura(f'{tag}_miniatura.png'); return
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, SW, SH); c = cairo.Context(surf)
    if args and args[0] == 'stills':
        for ts in map(float, args[1:]):
            c.save(); frame(c, ts); c.restore(); surf.write_to_png(f'short_{tag}_{ts}.png')
    else:
        a0, a1 = (float(args[1]), float(args[2])) if len(args) > 2 else (0, DUR)
        out = sys.stdout.buffer
        for i in range(int(round(a0 * FPS)), int(round(a1 * FPS))):
            c.save(); frame(c, i / FPS); c.restore(); surf.flush(); out.write(surf.get_data())
