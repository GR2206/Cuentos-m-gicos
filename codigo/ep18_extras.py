"""Episodio 18 — miniatura. Uso: python3 ep18_extras.py miniatura -> ep18_miniatura.png (1280x720)"""
import cairo, sys
import ep18_galletitas as E
from logos import word

def miniatura(path):
    W, H = 1280, 720
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(s)
    c.save(); c.scale(1.1, 1.1); c.translate(-560, -280)
    E.world(c, 99.5); c.restore()
    word(c, '¡Galletitas navideñas!', 640, 95, 80, colors=['#E53935', '#43A047', '#FFD600'], tilt=0.04, outline=9)
    word(c, 'Receta fácil', 1080, 660, 62, colors=['#FF7043'], tilt=-0.05, outline=7)
    s.write_to_png(path)

if __name__ == '__main__' and sys.argv[1:] == ['miniatura']:
    miniatura('ep18_miniatura.png')
