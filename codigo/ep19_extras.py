"""Episodio 19 — miniatura y short vertical.
Uso: python3 ep19_extras.py miniatura | short [a b] | stills 0 20"""
import cairo
import ep19_luciernaga as E
from logos import word
from short_montage import montage, cli

def draw(c, t): E.frame(c, t)

SEGS = [(0.0, 7.6, 1100), (4.5, 15.8, 600), (8.5, 30.8, 1000), (12.5, 34.0, 1000), (18.5, 56.0, 1250),
        (24.5, 70.0, 1260), (30.5, 77.0, 1260), (35.5, 94.0, 960)]
TT = [(0, '¡Una luciérnaga', 'perdida!'), (4.5, '¿Dónde está', 'su familia?'), (8.5, '¡Qué oscuro!', None),
      (12.5, '¡Cantamos', 'y brilla!'), (18.5, '¡Encontró', 'a su mamá!'), (24.5, '¡Un corazón', 'de luces!'),
      (30.5, '¡Y una', 'estrella!'), (35.5, '¡Buenas', 'noches!')]
frame, DUR = montage(draw, SEGS, TT, 39.5, ('#0D0B3B', '#4A3B8F'))

def miniatura(path):
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, 1280, 720); c = cairo.Context(s)
    c.save(); c.scale(1.2, 1.2); c.translate(-560, -330); E.frame(c, 74.5); c.restore()
    word(c, 'La luciérnaga', 330, 110, 92, colors=['#FFEB3B', '#FFF59D', '#B2FF59'], tilt=0.05, outline=9)
    word(c, 'perdida', 330, 215, 100, colors=['#B2FF59', '#FFEB3B', '#80D8FF'], tilt=0.05, outline=9)
    s.write_to_png(path)

if __name__ == '__main__': cli(frame, DUR, 'ep19', miniatura)
