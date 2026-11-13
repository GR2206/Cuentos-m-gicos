import cairo, math, random
import amigos as A
from amigos import hexc, ellipse, fill, OUT

FONT = 'Fredoka Light'
PALETTE = ['#FF4081', '#FF9100', '#FFD600', '#00C853', '#00B0FF', '#AA00FF']

def font(c, size):
    c.select_font_face(FONT, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(size)

def word(c, text, cx, y, size, colors=None, start=0, tilt=0.0, outline=11):
    """Bubbly title text, each letter its own colour, centred on cx."""
    font(c, size)
    w = c.text_extents(text).x_advance
    x = cx - w / 2
    colors = colors or PALETTE
    for i, ch in enumerate(text):
        adv = c.text_extents(ch).x_advance
        if ch != ' ':
            c.save(); c.translate(x + adv / 2, y); c.rotate(tilt * math.sin(i * 1.7))
            c.move_to(-adv / 2, 0); c.text_path(ch)
            c.set_line_join(cairo.LINE_JOIN_ROUND)
            c.set_source_rgba(*OUT); c.set_line_width(outline * 2.0); c.stroke_preserve()
            c.set_source_rgba(1, 1, 1, 1); c.set_line_width(outline); c.stroke_preserve()
            col = hexc(colors[(start + i) % len(colors)])
            c.set_source_rgba(*col); c.fill()
            c.restore()
        x += adv
    return w

def text_width(c, text, size):
    font(c, size); return c.text_extents(text).x_advance

def sparkle(c, x, y, r, col='#FFF59D'):
    c.save(); c.translate(x, y); c.move_to(0, -r)
    for k in range(4):
        c.rotate(math.pi / 2); c.curve_to(r * 0.12, -r * 0.12, r * 0.12, -r * 0.12, 0, -r) if False else None
    c.restore()
    c.move_to(x, y - r); c.curve_to(x + r * .15, y - r * .15, x + r * .15, y - r * .15, x + r, y)
    c.curve_to(x + r * .15, y + r * .15, x + r * .15, y + r * .15, x, y + r)
    c.curve_to(x - r * .15, y + r * .15, x - r * .15, y + r * .15, x - r, y)
    c.curve_to(x - r * .15, y - r * .15, x - r * .15, y - r * .15, x, y - r)
    c.set_source_rgba(*hexc(col)); c.fill()

def leaf(c, x, y, ang, L, col):
    c.save(); c.translate(x, y); c.rotate(ang)
    c.move_to(0, 0); c.curve_to(L * 0.3, -L * 0.28, L * 0.75, -L * 0.22, L, 0)
    c.curve_to(L * 0.75, L * 0.22, L * 0.3, L * 0.28, 0, 0); c.close_path()
    c.set_source_rgba(*hexc(col)); c.fill_preserve()
    c.set_source_rgba(*hexc('#1B5E20', 0.5)); c.set_line_width(L * 0.025); c.stroke()
    c.move_to(L * 0.05, 0); c.line_to(L * 0.9, 0); c.stroke()
    c.restore()

def arm(c, sx, sy, hx, hy, s=1.0):
    BROWN, BEIGE = hexc('#A0582C'), hexc('#FFD9A8')
    c.set_line_cap(cairo.LINE_CAP_ROUND)
    c.move_to(sx, sy); c.line_to(hx, hy); c.set_source_rgba(*OUT); c.set_line_width(60 * s); c.stroke()
    c.move_to(sx, sy); c.line_to(hx, hy); c.set_source_rgba(*BROWN); c.set_line_width(44 * s); c.stroke()

def hand(c, x, y, s=1.0):
    ellipse(c, x, y, 36 * s, 32 * s); fill(c, hexc('#FFD9A8'), OUT, 6)
    c.set_source_rgba(*OUT); c.set_line_width(4)
    for dx in (-12, 0, 12):
        c.move_to(x + dx * s, y + 8 * s); c.line_to(x + dx * s, y + 26 * s); c.stroke()

# ---------------- profile logo (square) ----------------
def profile(path, S=1024):
    sf = cairo.ImageSurface(cairo.FORMAT_ARGB32, S, S); c = cairo.Context(sf)
    k = S / 1024; c.scale(k, k)
    g = cairo.RadialGradient(512, 430, 60, 512, 512, 620)
    g.add_color_stop_rgb(0, *hexc('#FFF8C4')[:3]); g.add_color_stop_rgb(0.45, *hexc('#7FE0B0')[:3]); g.add_color_stop_rgb(1, *hexc('#0E9F6E')[:3])
    c.set_source(g); c.paint()
    # leaves framing the circle
    random.seed(3)
    for i in range(22):
        a = i / 22 * 2 * math.pi
        col = ['#2E7D32', '#43A047', '#1B8A4B'][i % 3]
        leaf(c, 512 + 560 * math.cos(a), 512 + 560 * math.sin(a), a + math.pi + random.uniform(-0.5, 0.5), 260, col)
    for (x, y, r) in ((215, 250, 26), (820, 240, 30), (180, 520, 18), (850, 500, 20), (300, 140, 14), (720, 130, 16)):
        sparkle(c, x, y, r)
    # Coco: body peeks behind the title, arms hug it
    ellipse(c, 512, 600, 150, 120); fill(c, hexc('#A0582C'), OUT, 7)
    A.draw(c, 'coco', 512, 365, 1.32)
    word(c, 'Cuentos', 512, 700, 172, start=0, tilt=0.06)
    word(c, 'mágicos', 512, 838, 150, start=3, tilt=0.06)
    word(c, 'de la selva', 512, 940, 92, colors=['#FFFFFF'], outline=7)
    arm(c, 400, 560, 330, 585); arm(c, 624, 560, 694, 585)
    hand(c, 322, 583, 0.95); hand(c, 702, 583, 0.95)
    sparkle(c, 790, 760, 34, '#FFFFFF'); sparkle(c, 240, 800, 22, '#FFFFFF')
    sf.write_to_png(path)

# ---------------- channel banner 2560x1440 ----------------
def banner_bg(c, t=0.0):
    W, H = 2560, 1440
    g = cairo.LinearGradient(0, 0, 0, H)
    g.add_color_stop_rgb(0, *hexc('#29B6F6')[:3]); g.add_color_stop_rgb(0.6, *hexc('#8FDBFF')[:3]); g.add_color_stop_rgb(1, *hexc('#C8F0FF')[:3])
    c.set_source(g); c.paint()
    # sun & clouds outside the safe area
    for i in range(12):
        c.save(); c.translate(2330, 230); c.rotate(i * math.pi / 6 + 0.3 * t)
        c.move_to(-26, -160); c.line_to(0, -225); c.line_to(26, -160); c.close_path()
        c.set_source_rgba(*hexc('#FFB300')); c.fill(); c.restore()
    ellipse(c, 2330, 230, 135, 135); fill(c, hexc('#FFEB3B'), hexc('#F9A825'), 8)
    for (x, y, s) in ((300, 230, 1.3), (1100, 150, 0.9), (1750, 260, 1.0)):
        c.save(); c.translate(x + 25 * t, y); c.scale(s, s)
        for (cx, cy, r) in ((0, 0, 60), (70, -30, 75), (150, 0, 60), (75, 20, 60)): ellipse(c, cx, cy, r, r)
        c.set_source_rgba(1, 1, 1, 1); c.fill(); c.restore()
    # hills
    for (yb, col) in ((980, '#66BB6A'), (1110, '#43A047'), (1260, '#8BC34A')):
        c.move_to(0, yb); c.curve_to(700, yb - 140, 1700, yb - 120, W, yb - 20)
        c.line_to(W, H); c.line_to(0, H); c.close_path(); c.set_source_rgba(*hexc(col)); c.fill()
    # big jungle leaves on both sides
    random.seed(5)
    for side in (0, 1):
        for i in range(9):
            x = -40 if side == 0 else W + 40
            y = 120 + i * 150 + random.uniform(-40, 40)
            ang = (random.uniform(-0.6, 0.6)) + (0 if side == 0 else math.pi) + 0.04 * math.sin(t * 1.6 + i)
            leaf(c, x, y, ang, random.uniform(380, 520), ['#2E7D32', '#43A047', '#1B8A4B'][i % 3])

def banner(path):
    W, H = 2560, 1440
    sf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(sf)
    banner_bg(c)
    # safe area: 1546 x 423 centred -> x 507..2053, y 508..931
    names = ['tomi', 'pipa', 'coco', 'tito', 'lola']
    xs = [800, 1040, 1280, 1520, 1760]
    for n, x in zip(names, xs):
        dy = {'coco': -10, 'pipa': 10, 'tomi': 30}.get(n, 0)
        A.draw(c, n, x, 625 + dy, 0.8, look=((1280 - x) / 900, 0.3))
    title = 'Cuentos mágicos de la selva'
    size = 150
    while text_width(c, title, size) > 1440: size -= 2
    word(c, title, 1280, 905, size, tilt=0.05, outline=9)
    for (x, y, r) in ((600, 560, 30), (1980, 540, 34), (560, 760, 18), (2010, 750, 22)):
        sparkle(c, x, y, r)
    sf.write_to_png(path)

if __name__ == '__main__':
    profile('logo_perfil.png')
    banner('banner_canal.png')
