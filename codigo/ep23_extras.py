"""Episodio 23 — miniatura y short vertical.
Uso: python3 ep23_extras.py miniatura | short [a b] | stills 0 20"""
import cairo
import ep23_cueva as E
from logos import word
from short_montage import montage, cli

def draw(c, t): E.frame(c, t); E.overlay(c, t)

SEGS = [(0.0, 16.4, 1100), (4.0, 22.8, 960), (8.0, 26.2, 470), (11.5, 31.3, 1100), (15.0, 36.8, 1100),
        (18.5, 42.4, 1100), (22.5, 55.8, 960), (26.0, 60.5, 960), (33.0, 87.3, 1100), (36.0, 95.5, 960)]
TT = [(0, '¡Una cueva', 'que habla!'), (4.0, '¿Quién está', 'ahí?'), (8.0, '¡Es el eco!', None), (11.5, '¡La la la!', None),
      (15.0, '¡Prrrú!', None), (18.5, '¡Tomi', 'se animó!'), (22.5, '¡Adentro!', None), (26.0, '¡Cristales', 'mágicos!'),
      (33.0, '¡Chau, cueva!', None), (36.0, '¡Somos más', 'valientes!')]
frame, DUR = montage(draw, SEGS, TT, 38.5, ('#7E57C2', '#29B6F6'))

def miniatura(path):
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, 1280, 720); c = cairo.Context(s)
    c.save(); c.scale(0.8, 0.8); c.translate(-160, -270); E.frame(c, 78.0); c.restore()
    word(c, '¡La cueva', 640, 100, 100, colors=['#80D8FF', '#B388FF', '#FFD600'], tilt=0.05, outline=10)
    word(c, 'del eco!', 640, 205, 105, colors=['#FFD600', '#80D8FF', '#B388FF'], tilt=0.05, outline=10)
    s.write_to_png(path)

if __name__ == '__main__': cli(frame, DUR, 'ep23', miniatura)
