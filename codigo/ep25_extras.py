"""Episodio 25 — miniatura. Uso: python3 ep25_extras.py miniatura"""
import cairo, sys
import ep25_noche_estrellada as E
from logos import word

def miniatura(path):
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, 1280, 720); c = cairo.Context(s)
    c.save(); c.scale(0.667, 0.667); E.frame(c, 36.5); c.restore()
    word(c, 'Noche estrellada', 560, 110, 96, colors=['#FFF59D', '#80D8FF', '#FF80AB'], tilt=0.03, outline=9)
    s.write_to_png(path)

if __name__ == '__main__' and sys.argv[1:] == ['miniatura']: miniatura('ep25_miniatura.png')
