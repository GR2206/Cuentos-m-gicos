"""Episodio 22 — miniatura y short vertical.
Uso: python3 ep22_extras.py miniatura | short [a b] | stills 0 20"""
import cairo
import ep22_huevo as E
from logos import word
from short_montage import montage, cli

def draw(c, t): E.frame(c, t); E.overlay(c, t)

SEGS = [(0.0, 8.2, 750), (3.5, 29.8, 650), (7.5, 39.8, 800), (14.0, 46.3, 800), (18.0, 52.0, 1300),
        (22.0, 59.5, 900), (26.0, 64.5, 1300), (32.0, 70.5, 1350), (36.0, 94.0, 700)]
TT = [(0, '¡Un huevo', 'misterioso!'), (3.5, '¡Tito lo tapa', 'de la lluvia!'), (7.5, '¡Crac, crac!', None),
      (14.0, '¡Nació Pío!', None), (18.0, '¿Dónde está', 'su mamá?'), (22.0, '¡Pipa', 'lo ayuda!'),
      (26.0, '¡Bien alto!', None), (32.0, '¡Encontró', 'a su mamá!'), (36.0, '¡Ayudar es', 'lo más lindo!')]
frame, DUR = montage(draw, SEGS, TT, 39.0, ('#29B6F6', '#8BC34A'))

def miniatura(path):
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, 1280, 720); c = cairo.Context(s)
    c.save(); c.scale(1.35, 1.35); c.translate(-300, -420); E.frame(c, 48.6); c.restore()
    word(c, '¡El huevo', 900, 100, 100, colors=['#29B6F6', '#FFD600', '#E91E63'], tilt=0.05, outline=10)
    word(c, 'misterioso!', 900, 205, 100, colors=['#E91E63', '#29B6F6', '#FFD600'], tilt=0.05, outline=10)
    s.write_to_png(path)

if __name__ == '__main__': cli(frame, DUR, 'ep22', miniatura)
