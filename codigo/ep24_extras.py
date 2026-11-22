"""Episodio 24 — miniatura. Uso: python3 ep24_extras.py miniatura"""
import cairo, sys
import ep24_barrilete as E
from logos import word

def miniatura(path):
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, 1280, 720); c = cairo.Context(s)
    c.save(); c.scale(0.95, 0.95); c.translate(-280, -30); E.frame(c, 65.0); c.restore()
    word(c, '¡El barrilete', 400, 110, 95, tilt=0.05, outline=10)
    word(c, 'perdido!', 400, 215, 105, start=3, tilt=0.05, outline=10)
    s.write_to_png(path)

if __name__ == '__main__' and sys.argv[1:] == ['miniatura']: miniatura('ep24_miniatura.png')
