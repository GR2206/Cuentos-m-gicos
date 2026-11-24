"""Episodio 17 — miniatura. Uso: python3 ep17_extras.py miniatura -> ep17_miniatura.png (1280x720)"""
import cairo, sys
import ep17_carta as E
from logos import word

def miniatura(path):
    W, H = 1280, 720
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(s)
    c.save(); c.scale(1.15, 1.15); c.translate(-150, -330)
    E.world(c, 59.98); c.restore()
    word(c, 'La carta', 930, 120, 105, colors=['#E53935', '#43A047', '#FFD600'], tilt=0.06, outline=10)
    word(c, 'de Coco', 930, 230, 105, colors=['#43A047', '#FFD600', '#E53935'], tilt=0.06, outline=10)
    s.write_to_png(path)

if __name__ == '__main__' and sys.argv[1:] == ['miniatura']:
    miniatura('ep17_miniatura.png')
