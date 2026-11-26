"""Recopilación "Cuentos para dormir" (~20 min): miniatura. El video lo arma /tmp/recop_noche.sh:
intro + ep01, ep06, ep07, ep19, ep25 (sin sus intros) + 13 min de canción de cuna (cancion_de_cuna_loop.py).
Uso: python3 recop_dormir.py miniatura"""
import cairo, sys
from amigos import hexc, ellipse, fill, OUT
from logos import word
import ep25_noche_estrellada as E

def miniatura(path):
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, 1280, 720); c = cairo.Context(s)
    c.save(); c.scale(0.95, 0.95); c.translate(-330, -240); E.frame(c, 107.0); c.restore()
    word(c, 'Cuentos', 360, 110, 120, colors=['#FFF59D', '#80D8FF', '#FF80AB'], tilt=0.04, outline=11)
    word(c, 'para dormir', 360, 235, 105, colors=['#B9F6CA', '#FFF59D', '#80D8FF'], tilt=0.04, outline=10)
    c.save(); c.translate(1100, 130); c.rotate(-0.12)
    ellipse(c, 0, 0, 140, 92); fill(c, hexc('#7E57C2'), OUT, 7)
    word(c, '20', 0, 5, 96, colors=['#FFFFFF'], outline=6)
    word(c, 'minutos', 0, 62, 44, colors=['#FFF59D'], outline=5)
    c.restore()
    s.write_to_png(path)

if __name__ == '__main__' and sys.argv[1:] == ['miniatura']: miniatura('recop_dormir_miniatura.png')
