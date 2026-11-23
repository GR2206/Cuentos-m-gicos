"""Episodio 26 — miniatura. Uso: python3 ep26_extras.py miniatura"""
import cairo, sys
import ep26_concierto as E
from logos import word

def miniatura(path):
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, 1280, 720); c = cairo.Context(s)
    c.save(); c.scale(0.8, 0.8); c.translate(-180, -120); E.frame(c, 82.0); c.restore()
    word(c, '¡El concierto', 640, 95, 92, colors=['#E91E63', '#FFD600', '#1E88E5', '#43A047'], tilt=0.04, outline=10)
    word(c, 'de la selva!', 640, 195, 92, colors=['#43A047', '#E91E63', '#FFD600'], tilt=0.04, outline=10)
    s.write_to_png(path)

if __name__ == '__main__' and sys.argv[1:] == ['miniatura']: miniatura('ep26_miniatura.png')
