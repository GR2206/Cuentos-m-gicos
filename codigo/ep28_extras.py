"""Episodio 28 — miniatura. Uso: python3 ep28_extras.py miniatura"""
import cairo, sys
import ep28_oruguita as E
from logos import word

def miniatura(path):
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, 1280, 720); c = cairo.Context(s)
    c.save(); c.scale(1.25, 1.25); c.translate(-470, -150); E.frame(c, 59.0); c.restore()
    E.oruga(c, 640, 680, 1.05, 2.0)
    word(c, '¡La oruguita', 300, 110, 92, colors=['#8BC34A', '#FF4081', '#FFD600'], tilt=0.05, outline=10)
    word(c, 'Mari!', 300, 215, 110, colors=['#7C4DFF', '#40C4FF', '#FF4081'], tilt=0.05, outline=10)
    s.write_to_png(path)

if __name__ == '__main__' and sys.argv[1:] == ['miniatura']: miniatura('ep28_miniatura.png')
