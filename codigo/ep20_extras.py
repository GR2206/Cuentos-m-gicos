"""Episodio 20 — miniatura y short vertical.
Uso: python3 ep20_extras.py miniatura | short [a b] | stills 0 20"""
import cairo
import ep20_tesoro as E
from logos import word
from short_montage import montage, cli

def draw(c, t): E.frame(c, t); E.overlay(c, t)

SEGS = [(0.0, 8.9, 960), (3.5, 10.5, 960), (7.0, 26.0, 1150), (11.0, 44.0, 1200), (17.0, 62.0, 1240),
        (20.0, 64.8, 1240), (24.0, 70.5, 1240), (28.5, 73.0, 1140), (32.0, 86.0, 960)]
TT = [(0, '¡Un mapa', 'del tesoro!'), (3.5, '¿Adónde', 'nos lleva?'), (7.0, '1. ¡La piedra', 'corazón!'),
      (11.0, '2. ¡El árbol', 'más alto!'), (17.0, '3. ¡La X!', None), (20.0, '¡A cavar!', None), (24.0, '¡Un cofre!', None),
      (28.5, '¡Frutas!', None), (32.0, 'El mejor tesoro:', '¡los amigos!')]
frame, DUR = montage(draw, SEGS, TT, 38.0, ('#29B6F6', '#8BC34A'))

def miniatura(path):
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, 1280, 720); c = cairo.Context(s)
    c.save(); c.scale(1.15, 1.15); c.translate(-650, -340); E.frame(c, 71.8); c.restore()
    word(c, '¡El tesoro', 330, 110, 100, tilt=0.05, outline=10)
    word(c, 'del bosque!', 330, 220, 100, start=3, tilt=0.05, outline=10)
    s.write_to_png(path)

if __name__ == '__main__': cli(frame, DUR, 'ep20', miniatura)
