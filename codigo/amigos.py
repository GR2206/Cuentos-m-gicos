"""Cuentos mágicos de la selva — cabezas de los personajes (estilo oficial).
Cada función dibuja la cabeza centrada en (0,0), radio aprox. 140 px a escala 1."""
import math, cairo

def hexc(h, a=1.0):
    h = h.lstrip('#')
    return (int(h[0:2], 16)/255, int(h[2:4], 16)/255, int(h[4:6], 16)/255, a)

OUT = hexc('#3B2314')

def ellipse(c, x, y, rx, ry):
    c.save(); c.translate(x, y); c.scale(rx, ry); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()

def fill(c, col, outline=None, lw=6):
    c.set_source_rgba(*col)
    if outline:
        c.fill_preserve(); c.set_source_rgba(*outline); c.set_line_width(lw); c.stroke()
    else:
        c.fill()

def eye(c, x, y, rx=34, ry=42, look=(0, 0), lashes=False):
    ellipse(c, x, y, rx, ry); fill(c, (1, 1, 1, 1), OUT, 5)
    ellipse(c, x + look[0] * 10, y + 3 + look[1] * 10, rx * 0.56, ry * 0.5); fill(c, hexc('#1A1A1A'))
    ellipse(c, x + look[0] * 10 + rx * 0.2, y - ry * 0.12 + look[1] * 10, rx * 0.2, rx * 0.2); c.set_source_rgba(1, 1, 1, 1); c.fill()
    if lashes:
        c.set_source_rgba(*OUT); c.set_line_width(6); c.set_line_cap(cairo.LINE_CAP_ROUND)
        for a in (-0.75, -0.6):
            ang = a * math.pi
            c.move_to(x + rx * 0.95 * math.cos(ang) * (1 if x > 0 else -1), y + ry * math.sin(ang))
            c.line_to(x + (rx + 16) * math.cos(ang) * (1 if x > 0 else -1), y + (ry + 14) * math.sin(ang))
            c.stroke()

def open_smile(c, y=55, w=48, d=65):
    path = lambda: (c.move_to(-w, y), c.curve_to(-w * 0.83, y + d, w * 0.83, y + d, w, y), c.close_path())
    path(); fill(c, hexc('#B71C1C'), OUT, 6)
    c.save(); path(); c.clip()
    ellipse(c, 0, y + d * 0.77, w * 0.62, d * 0.3); c.set_source_rgba(*hexc('#FF8A80')); c.fill(); c.restore()

def cheeks(c, dx=98, y=45, col='#FF5C8A'):
    for cx in (-dx, dx):
        ellipse(c, cx, y, 24, 17); c.set_source_rgba(*hexc(col, 0.6)); c.fill()

# ---------------- Coco el monito ----------------
def coco(c, look=(0, 0)):
    BROWN, BEIGE = hexc('#A0582C'), hexc('#FFD9A8')
    for ex in (-1, 1):
        ellipse(c, ex * 138, -5, 52, 52); fill(c, BROWN, OUT, 6)
        ellipse(c, ex * 138, -5, 30, 30); fill(c, BEIGE)
    for i, dx in enumerate((-22, 0, 22)):
        ellipse(c, dx, -140 - (10 if i == 1 else 0), 18, 26); fill(c, BROWN, OUT, 5)
    ellipse(c, 0, 0, 138, 132); fill(c, BROWN, OUT, 6)
    for ex in (-50, 50): ellipse(c, ex, -10, 62, 64)
    ellipse(c, 0, 55, 98, 66); c.set_source_rgba(*BEIGE); c.fill()
    for ex in (-48, 48): eye(c, ex, -15, look=look)
    for nx in (-13, 13): ellipse(c, nx, 32, 6, 8); fill(c, OUT)
    open_smile(c); cheeks(c)

# ---------------- Lola la lorita ----------------
def lola(c, look=(0, 0)):
    RED = hexc('#E53935')
    for i, (col, a) in enumerate((('#1E88E5', -0.45), ('#FDD835', -0.15), ('#E53935', 0.15))):
        c.save(); c.translate(0, -110); c.rotate(a)
        ellipse(c, 0, -55, 24, 60); fill(c, hexc(col), OUT, 5); c.restore()
    ellipse(c, 0, 0, 128, 130); fill(c, RED, OUT, 6)
    for ex in (-52, 52):
        ellipse(c, ex, -15, 50, 54); c.set_source_rgba(1, 1, 1, 1); c.fill()
        eye(c, ex, -15, 28, 34, look)
    # hooked beak
    c.move_to(-34, 30); c.curve_to(-30, -5, 30, -5, 34, 30)
    c.curve_to(36, 70, 15, 105, 0, 112); c.curve_to(-14, 95, -34, 70, -34, 30); c.close_path()
    fill(c, hexc('#FFC107'), OUT, 6)
    c.move_to(-30, 55); c.curve_to(-10, 65, 10, 65, 30, 55); c.set_source_rgba(*OUT); c.set_line_width(5); c.stroke()
    cheeks(c, 95, 50, '#FF8A80')

# ---------------- Tito el elefantito ----------------
def tito(c, look=(0, 0)):
    BLUE, PINK = hexc('#8FB8E8'), hexc('#F8BBD0')
    for ex in (-1, 1):
        c.save(); c.scale(ex, 1)
        c.move_to(90, -80); c.curve_to(260, -150, 290, 80, 100, 70); c.close_path(); fill(c, BLUE, OUT, 6)
        c.move_to(110, -50); c.curve_to(230, -100, 245, 50, 115, 40); c.close_path(); fill(c, PINK)
        c.restore()
    ellipse(c, 0, 0, 135, 128); fill(c, BLUE, OUT, 6)
    for ex in (-50, 50): eye(c, ex, -25, 30, 38, look)
    # trunk curling up
    c.set_line_cap(cairo.LINE_CAP_ROUND)
    tr = lambda: (c.move_to(0, 20), c.curve_to(0, 110, 50, 150, 85, 110))
    tr(); c.set_source_rgba(*OUT); c.set_line_width(58); c.stroke()
    tr(); c.set_source_rgba(*BLUE); c.set_line_width(46); c.stroke()
    for k in (60, 85):
        c.move_to(-18, k); c.line_to(18, k + 4); c.set_source_rgba(*OUT); c.set_line_width(4); c.stroke()
    c.set_line_width(7); c.set_source_rgba(*OUT)
    c.arc(-55, 55, 30, 0.2 * math.pi, 0.8 * math.pi); c.stroke()
    cheeks(c, 95, 35)

# ---------------- Pipa la jirafita ----------------
def pipa(c, look=(0, 0)):
    YEL, SPOT, MUZ = hexc('#FFCF40'), hexc('#F08A24'), hexc('#FFE9B0')
    for ex in (-1, 1):  # horns
        c.set_line_cap(cairo.LINE_CAP_ROUND)
        c.move_to(ex * 40, -110); c.line_to(ex * 55, -185); c.set_source_rgba(*OUT); c.set_line_width(26); c.stroke()
        c.move_to(ex * 40, -110); c.line_to(ex * 55, -185); c.set_source_rgba(*YEL); c.set_line_width(15); c.stroke()
        ellipse(c, ex * 55, -190, 20, 20); fill(c, hexc('#8D5524'), OUT, 5)
        c.save(); c.translate(ex * 115, -75); c.rotate(ex * 0.6)
        ellipse(c, 0, 0, 45, 22); fill(c, YEL, OUT, 6); c.restore()
    ellipse(c, 0, -5, 120, 140); fill(c, YEL, OUT, 6)
    c.save(); ellipse(c, 0, -5, 120, 140); c.clip()
    for (sx, sy, r) in ((-85, -70, 26), (90, -40, 22), (-95, 30, 18), (70, -110, 16)):
        ellipse(c, sx, sy, r, r * 0.85); c.set_source_rgba(*SPOT); c.fill()
    c.restore()
    ellipse(c, 0, 75, 95, 62); fill(c, MUZ, OUT, 6)
    for ex in (-48, 48): eye(c, ex, -30, 30, 38, look, lashes=True)
    for nx in (-25, 25): ellipse(c, nx, 60, 8, 10); fill(c, OUT)
    c.set_source_rgba(*OUT); c.set_line_width(7); c.set_line_cap(cairo.LINE_CAP_ROUND)
    c.arc(0, 85, 30, 0.2 * math.pi, 0.8 * math.pi); c.stroke()
    cheeks(c, 88, 25)

# ---------------- Tomi la tortuguita ----------------
def tomi(c, look=(0, 0)):
    GREEN, SHELL, SHELL2 = hexc('#7CCB5B'), hexc('#8D6E63'), hexc('#BCAAA4')
    # shell behind the head
    ellipse(c, 0, 55, 205, 105); fill(c, SHELL, OUT, 6)
    for (hx, hy) in ((-135, 55), (135, 55), (-60, 115), (60, 115)):
        ellipse(c, hx, hy, 42, 30); c.set_source_rgba(*SHELL2); c.fill()
    ellipse(c, 0, -10, 125, 118); fill(c, GREEN, OUT, 6)
    for ex in (-48, 48): eye(c, ex, -25, 32, 40, look)
    for nx in (-12, 12): ellipse(c, nx, 25, 5, 6); fill(c, OUT)
    open_smile(c, 45, 42, 50)
    cheeks(c, 90, 30)

ALL = {'coco': coco, 'lola': lola, 'tito': tito, 'pipa': pipa, 'tomi': tomi}
COLORS = {'coco': '#A0582C', 'lola': '#E53935', 'tito': '#5C8FD6', 'pipa': '#F08A24', 'tomi': '#4CAF50'}

def draw(c, name, x, y, s=1.0, look=(0, 0), rot=0.0):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s); ALL[name](c, look); c.restore()
