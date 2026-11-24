"""Cuentos mágicos de la selva — personajes de cuerpo entero, de frente (referencia 2D para las hojas 3D).
Las cabezas salen SIEMPRE de amigos.py; acá solo se agregan cuerpos y ropa en el mismo estilo.
Uso: python3 cuerpos.py  → guarda <nombre>-cuerpo-2d.png en la carpeta actual (1024×1280, fondo crema)."""
import math, cairo
import amigos
from amigos import hexc, ellipse, fill, OUT

CREAM = hexc('#FFF4E0')

def limb(c, x0, y0, x1, y1, col, w=40):
    c.set_line_cap(cairo.LINE_CAP_ROUND)
    c.move_to(x0, y0); c.line_to(x1, y1); c.set_source_rgba(*OUT); c.set_line_width(w + 12); c.stroke()
    c.move_to(x0, y0); c.line_to(x1, y1); c.set_source_rgba(*col); c.set_line_width(w); c.stroke()

def shadow(c, y, rx):
    ellipse(c, 0, y, rx, rx * 0.12); c.set_source_rgba(0.55, 0.42, 0.3, 0.18); c.fill()

# ---------------- Lola: lorita roja, sin ropa ----------------
def lola(c):
    RED, BLUE, YEL = hexc('#E53935'), hexc('#1E88E5'), hexc('#FDD835')
    shadow(c, 372, 120)
    for i, col in enumerate((BLUE, YEL, RED)):  # tail feathers behind the body
        c.save(); c.translate(0, 290); c.rotate(math.radians(-40 + i * 40))
        ellipse(c, 0, 60, 24, 62); fill(c, col, OUT, 5); c.restore()
    for fx in (-42, 42):  # feet
        for k in (-16, 0, 16):
            ellipse(c, fx + k, 352, 11, 20); fill(c, hexc('#FFC107'), OUT, 4)
    ellipse(c, 0, 205, 112, 135); fill(c, RED, OUT, 6)
    ellipse(c, 0, 230, 70, 85); c.set_source_rgba(*hexc('#FF7043', 0.55)); c.fill()  # soft chest
    for ex in (-1, 1):  # wings
        c.save(); c.translate(ex * 105, 190); c.rotate(ex * 0.25)
        ellipse(c, 0, 40, 42, 95); fill(c, RED, OUT, 6)
        c.save(); ellipse(c, 0, 40, 42, 95); c.clip()
        ellipse(c, 0, 105, 50, 45); c.set_source_rgba(*BLUE); c.fill()
        ellipse(c, 0, 72, 50, 14); c.set_source_rgba(*YEL); c.fill()
        c.restore(); ellipse(c, 0, 40, 42, 95); c.set_source_rgba(*OUT); c.set_line_width(6); c.stroke()
        c.restore()
    amigos.draw(c, 'lola', 0, 0)

# ---------------- Tito: elefantito celeste, jardinero rojo ----------------
def tito(c):
    BLUE, RED = hexc('#8FB8E8'), hexc('#E53935')
    shadow(c, 452, 170)
    for lx in (-62, 62):  # legs
        c.move_to(lx - 46, 300); c.line_to(lx - 46, 420); c.curve_to(lx - 46, 448, lx + 46, 448, lx + 46, 420)
        c.line_to(lx + 46, 300); c.close_path(); fill(c, BLUE, OUT, 6)
        for k in (-22, 0, 22):
            ellipse(c, lx + k, 428, 11, 9); fill(c, hexc('#FFF8E7'), OUT, 3)
    ellipse(c, 0, 250, 140, 130); fill(c, BLUE, OUT, 6)
    c.save(); ellipse(c, 0, 250, 140, 130); c.clip()  # overall shorts
    c.rectangle(-200, 255, 400, 200); c.set_source_rgba(*RED); c.fill()
    c.rectangle(-58, 175, 116, 90); c.fill()
    c.restore()
    c.set_source_rgba(*OUT); c.set_line_width(5)
    c.move_to(-130, 255); c.line_to(-58, 255); c.line_to(-58, 175); c.line_to(58, 175); c.line_to(58, 255); c.line_to(130, 255); c.stroke()
    for ex in (-1, 1):  # straps + buttons
        c.move_to(ex * 48, 178); c.line_to(ex * 85, 128); c.set_source_rgba(*OUT); c.set_line_width(30); c.stroke()
        c.move_to(ex * 48, 178); c.line_to(ex * 85, 128); c.set_source_rgba(*RED); c.set_line_width(20); c.stroke()
        ellipse(c, ex * 44, 190, 10, 10); fill(c, hexc('#FDD835'), OUT, 4)
    c.move_to(-58, 300); c.line_to(-62, 380); c.move_to(58, 300); c.line_to(62, 380)  # shorts legs split
    c.set_source_rgba(*OUT); c.set_line_width(5); c.stroke()
    for ex in (-1, 1):  # arms
        limb(c, ex * 125, 175, ex * 190, 290, BLUE, 44)
        ellipse(c, ex * 192, 296, 26, 24); fill(c, BLUE, OUT, 6)
    amigos.draw(c, 'tito', 0, 0)

# ---------------- Pipa: jirafita amarilla, collar de perlas ----------------
def pipa(c):
    YEL, SPOT, BROWN = hexc('#FFCF40'), hexc('#F08A24'), hexc('#8D5524')
    shadow(c, 592, 130)
    for lx in (-45, 45):  # legs with hooves
        limb(c, lx, 420, lx, 545, YEL, 36)
        c.move_to(lx - 27, 545); c.line_to(lx + 27, 545); c.line_to(lx + 25, 582); c.line_to(lx - 25, 582); c.close_path()
        fill(c, BROWN, OUT, 5)
    c.rectangle(-50, 100, 100, 210); fill(c, YEL, OUT, 6)  # neck
    ellipse(c, 0, 375, 118, 95); fill(c, YEL, OUT, 6)  # body
    c.rectangle(-44, 270, 88, 60); c.set_source_rgba(*YEL); c.fill()  # join neck-body
    c.save(); c.rectangle(-44, 100, 88, 230); ellipse(c, 0, 375, 112, 89); c.clip()
    for (sx, sy, r) in ((-18, 170, 16), (20, 220, 14), (-60, 370, 20), (58, 350, 22), (12, 420, 16), (-25, 330, 12)):
        ellipse(c, sx, sy, r, r * 0.85); c.set_source_rgba(*SPOT); c.fill()
    c.restore()
    for ex in (-1, 1):  # arms
        limb(c, ex * 98, 330, ex * 155, 435, YEL, 32)
        ellipse(c, ex * 157, 441, 20, 18); fill(c, BROWN, OUT, 5)
    n = 9  # pearl necklace at the base of the neck
    for i in range(n):
        a = math.pi * (0.15 + 0.7 * i / (n - 1))
        px, py = 64 * math.cos(a), 262 + 24 * math.sin(a)
        ellipse(c, px, py, 13, 13); fill(c, hexc('#FFFDF6'), OUT, 3)
        ellipse(c, px - 4, py - 4, 4, 4); c.set_source_rgba(1, 1, 1, 1); c.fill()
    amigos.draw(c, 'pipa', 0, 0)

# ---------------- Tomi: tortuguita verde, bufandita naranja ----------------
def tomi(c):
    GREEN, SHELL, SHELL2, BELLY = hexc('#7CCB5B'), hexc('#8D6E63'), hexc('#BCAAA4'), hexc('#FFE9B0')
    ORANGE = hexc('#FF8F00')
    shadow(c, 432, 160)
    ellipse(c, 0, 255, 175, 160); fill(c, SHELL, OUT, 6)  # shell behind
    for (hx, hy) in ((-140, 230), (140, 230), (-120, 330), (120, 330)):
        ellipse(c, hx, hy, 26, 36); c.set_source_rgba(*SHELL2); c.fill()
    for lx in (-58, 58):  # legs
        ellipse(c, lx, 395, 40, 36); fill(c, GREEN, OUT, 6)
    for ex in (-1, 1):  # arms
        limb(c, ex * 110, 200, ex * 175, 290, GREEN, 38)
        ellipse(c, ex * 177, 296, 24, 22); fill(c, GREEN, OUT, 6)
    ellipse(c, 0, 260, 118, 140); fill(c, BELLY, OUT, 6)  # belly plate
    c.set_source_rgba(*hexc('#D7B98A')); c.set_line_width(5)
    for yy in (210, 265, 320):
        c.move_to(-105, yy); c.curve_to(-40, yy + 12, 40, yy + 12, 105, yy); c.stroke()
    # scarf
    c.move_to(-95, 112); c.curve_to(-40, 150, 40, 150, 95, 112); c.line_to(92, 145); c.curve_to(40, 182, -40, 182, -92, 145)
    c.close_path(); fill(c, ORANGE, OUT, 6)
    c.move_to(50, 150); c.line_to(85, 240); c.line_to(45, 245); c.line_to(25, 160); c.close_path(); fill(c, ORANGE, OUT, 6)
    # head from amigos.py, without the shell drawn behind it
    c.save(); ellipse(c, 0, -10, 128.5, 121.5); c.clip(); amigos.draw(c, 'tomi', 0, 0); c.restore()

FIGS = {'lola': (lola, 1.75, 470), 'tito': (tito, 1.55, 470), 'pipa': (pipa, 1.45, 390), 'tomi': (tomi, 1.75, 440)}

if __name__ == '__main__':
    for name, (fn, s, y) in FIGS.items():
        surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, 1024, 1280); c = cairo.Context(surf)
        c.set_source_rgba(*CREAM); c.paint()
        c.save(); c.translate(512, y); c.scale(s, s); fn(c); c.restore()
        surf.write_to_png(f'{name}-cuerpo-2d.png')
