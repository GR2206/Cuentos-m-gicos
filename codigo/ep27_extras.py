"""Episodio 27 — miniatura. Uso: python3 ep27_extras.py miniatura"""
import cairo, sys
import ep27_desayuno as E
from logos import word

def miniatura(path):
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, 1280, 720); c = cairo.Context(s)
    c.save(); c.scale(0.95, 0.95); c.translate(-280, -280); E.frame(c, 73.0); c.restore()
    word(c, '¡El desayuno', 640, 95, 95, colors=['#FFB300', '#E53935', '#43A047', '#8E24AA'], tilt=0.04, outline=10)
    word(c, 'de los amigos!', 640, 200, 95, colors=['#43A047', '#8E24AA', '#FFB300', '#E53935'], tilt=0.04, outline=10)
    s.write_to_png(path)

if __name__ == '__main__' and sys.argv[1:] == ['miniatura']: miniatura('ep27_miniatura.png')
