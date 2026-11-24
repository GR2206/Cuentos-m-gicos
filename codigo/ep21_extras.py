"""Episodio 21 — miniatura y short vertical.
Uso: python3 ep21_extras.py miniatura | short [a b] | stills 0 20"""
import cairo
import ep21_carrera as E
from logos import word
from short_montage import montage, cli

def draw(c, t): E.frame(c, t); E.overlay(c, t)

SEGS = [(0.0, 13.3, 960), (3.5, 15.0, 1100), (7.5, 19.8, 470), (11.5, 24.0, 750), (15.5, 37.5, 1100),
        (23.0, 52.0, 1100), (26.5, 55.5, 960), (30.5, 62.0, 960), (34.5, 93.0, 960)]
TT = [(0, '¡La gran', 'carrera!'), (3.5, '¡Coco va', 'primero!'), (7.5, '¡Tomi se', 'dio vuelta!'), (11.5, '¡Coco', 'la ayuda!'),
      (15.5, '¡Un tronco', 'gigante!'), (23.0, '¡Esperemos', 'a todos!'), (26.5, '¡Llegamos', 'juntos!'),
      (30.5, '¡Medallas', 'para todos!'), (34.5, '¡Ganaron', 'todos!')]
frame, DUR = montage(draw, SEGS, TT, 38.0, ('#29B6F6', '#8BC34A'))

def miniatura(path):
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, 1280, 720); c = cairo.Context(s)
    c.save(); c.scale(1.12, 1.12); c.translate(-420, -330); E.frame(c, 65.0); c.restore()
    word(c, '¡La gran', 1000, 100, 100, tilt=0.05, outline=10)
    word(c, 'carrera!', 1000, 205, 110, start=3, tilt=0.05, outline=10)
    s.write_to_png(path)

if __name__ == '__main__': cli(frame, DUR, 'ep21', miniatura)
