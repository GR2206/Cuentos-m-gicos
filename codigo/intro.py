"""Intro del canal (5,5 s): los 5 amigos aparecen uno por uno y el título salta letra por letra."""
import cairo, math, random, sys
import amigos as A
from amigos import hexc, ellipse, fill, OUT
from logos import leaf, sparkle, font, PALETTE

W, H, FPS, DUR = 1920, 1080, 30, 5.5
NAMES = ['tomi', 'pipa', 'coco', 'tito', 'lola']
POP = [0.40, 0.75, 1.10, 1.45, 1.80]          # cuándo aparece cada personaje
TITLE = 'Cuentos mágicos de la selva'
T_TITLE, STAGGER = 2.25, 0.035

def back(p):  # easeOutBack
    p = max(0.0, min(1.0, p)); k = 1.70158
    return 1 + (k + 1) * (p - 1) ** 3 + k * (p - 1) ** 2

def background():
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(s)
    g = cairo.LinearGradient(0, 0, 0, H)
    g.add_color_stop_rgb(0, *hexc('#29B6F6')[:3]); g.add_color_stop_rgb(0.6, *hexc('#8FDBFF')[:3]); g.add_color_stop_rgb(1, *hexc('#C8F0FF')[:3])
    c.set_source(g); c.paint()
    for (yb, col) in ((820, '#66BB6A'), (930, '#43A047'), (1030, '#8BC34A')):
        c.move_to(0, yb); c.curve_to(500, yb - 110, 1300, yb - 100, W, yb - 20)
        c.line_to(W, H); c.line_to(0, H); c.close_path(); c.set_source_rgba(*hexc(col)); c.fill()
    random.seed(5)
    for side in (0, 1):
        for i in range(8):
            x = -60 if side == 0 else W + 60
            y = 40 + i * 140 + random.uniform(-30, 30)
            ang = random.uniform(-0.5, 0.5) + (0 if side == 0 else math.pi)
            leaf(c, x, y, ang, random.uniform(300, 400), ['#2E7D32', '#43A047', '#1B8A4B'][i % 3])
    return s

BG = background()

def clouds(c, t):
    for (x0, y0, s, sp) in ((150, 150, 1.0, 40), (820, 90, 0.8, 30), (1450, 170, 0.9, 45)):
        c.save(); c.translate(x0 + sp * t, y0); c.scale(s, s)
        for (cx, cy, r) in ((0, 0, 60), (70, -30, 75), (150, 0, 60), (75, 20, 60)): ellipse(c, cx, cy, r, r)
        c.set_source_rgba(1, 1, 1, 1); c.fill(); c.restore()

def title(c, t):
    size = 120
    font(c, size)
    while c.text_extents(TITLE).x_advance > 1500:
        size -= 2; font(c, size)
    x = W / 2 - c.text_extents(TITLE).x_advance / 2
    y = 800
    for i, ch in enumerate(TITLE):
        adv = c.text_extents(ch).x_advance
        t0 = T_TITLE + i * STAGGER
        p = (t - t0) / 0.3
        if ch != ' ' and p > 0:
            s = back(p)
            wob = 0.06 * math.sin(i * 1.7) + (0.05 * math.sin(t * 6 + i) if t > 3.6 else 0)
            hop = -14 * abs(math.sin((t - 3.6) * 4 + i * 0.4)) if t > 3.6 else 0
            c.save(); c.translate(x + adv / 2, y - size * 0.35 + hop); c.rotate(wob); c.scale(s, s)
            c.translate(-adv / 2, size * 0.35)
            c.move_to(0, 0); c.text_path(ch)
            c.set_line_join(cairo.LINE_JOIN_ROUND)
            c.set_source_rgba(*OUT); c.set_line_width(18); c.stroke_preserve()
            c.set_source_rgba(1, 1, 1, 1); c.set_line_width(9); c.stroke_preserve()
            c.set_source_rgba(*hexc(PALETTE[i % len(PALETTE)])); c.fill()
            c.restore()
        x += adv

def frame(c, t):
    c.set_source_surface(BG, 0, 0); c.paint()
    clouds(c, t)
    xs = [W / 2 + k * 285 for k in (-2, -1, 0, 1, 2)]
    order = [0, 1, 3, 4, 2]  # Coco se dibuja último: queda adelante
    for i in order:
        n, x = NAMES[i], xs[i]
        p = (t - POP[i]) / 0.4
        if p <= 0: continue
        s = (1.0 if n == 'coco' else 0.88) * back(p)
        y = 480 + {'coco': -10, 'pipa': 10, 'tomi': 30}.get(n, 0)
        y += -60 * math.sin(math.pi * min(1, p))           # pop jump
        if t > 2.3: y += 10 * math.sin(2 * math.pi * 1.4 * t + i * 1.2)
        look = ((W / 2 - x) / 800, 0.3) if t > 2.3 else (0, 0)
        A.draw(c, n, x, y, s, look=look, rot=0.05 * math.sin(t * 3 + i) * min(1, p))
    title(c, t)
    # magic sparkles
    random.seed(11)
    for k in range(16):
        sx, sy = random.uniform(250, 1670), random.uniform(160, 900)
        ph = random.uniform(0, 1)
        tw = (t * 0.9 + ph) % 1.0
        if t > 2.0:
            sparkle(c, sx, sy, 26 * math.sin(math.pi * tw), '#FFF59D' if k % 2 else '#FFFFFF')
    # white flash at the very start
    if t < 0.3:
        c.set_source_rgba(1, 1, 1, 1 - t / 0.3); c.paint()

if __name__ == '__main__':
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(surf)
    if len(sys.argv) > 1 and sys.argv[1] == 'stills':
        for t in map(float, sys.argv[2:]):
            c.save(); frame(c, t); c.restore(); surf.write_to_png(f'intro_{t}.png')
    else:
        out = sys.stdout.buffer
        for i in range(int(DUR * FPS)):
            c.save(); frame(c, i / FPS); c.restore(); surf.flush(); out.write(surf.get_data())
