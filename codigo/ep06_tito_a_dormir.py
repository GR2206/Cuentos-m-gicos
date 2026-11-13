"""Episodio 6 — Tito se va a dormir (A dormir con…, 60 s).
Es de noche. Tito llega despacito, bosteza, Lola le canta una canción de cuna
y los dos se quedan dormidos en una cama de hojas bajo la luna.

Uso:  python3 ep06_tito_a_dormir.py                -> cuadros crudos por stdout
      python3 ep06_tito_a_dormir.py range 0 30     -> solo un tramo
      python3 ep06_tito_a_dormir.py stills 12 40   -> PNG sueltos"""
import cairo, math, sys
import escena_noche as N
import cuerpos as K
from amigos import hexc, ellipse, fill, OUT
from logos import word, sparkle, font
from ep02_puente_del_rio import kf, ss, moving, K_back, music_note

W, H, FPS = 1920, 1080, 30
DUR = 60.0
GROUND = 880
TX = 900
N.SHOOT = ((9.5, 250, 60), (41.0, 300, 120))

NIGHT = ['#FFF59D', '#FFD54F', '#B39DDB', '#81D4FA', '#F48FB1', '#FFFFFF']

def make_bg():
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(s)
    N.sky(c); return s
SKY = make_bg()

def leaf_bed(c, x, y, front=True):
    """Cama de hojas: atrás (front=False) un colchón, adelante (front=True) la 'frazada'."""
    if not front:
        ellipse(c, x, y - 10, 300, 45); fill(c, hexc('#2E7D32'), OUT, 6)
        return
    # a big leaf blanket lying across Tito, plus two small leaves at the sides
    for (dx, dy, L, ht, ang, col) in ((-250, 40, 170, 60, -0.5, '#43A047'), (250, 40, 170, 60, 0.5, '#43A047')):
        c.save(); c.translate(x + dx, y + dy); c.rotate(ang)
        ellipse(c, 0, 0, L * 0.5, ht * 0.5); fill(c, hexc(col), OUT, 5); c.restore()
    c.move_to(x - 280, y + 20)
    c.curve_to(x - 200, y - 75, x + 200, y - 75, x + 290, y + 10)
    c.curve_to(x + 220, y + 150, x - 220, y + 150, x - 280, y + 20); c.close_path()
    fill(c, hexc('#66BB6A'), OUT, 6)
    c.move_to(x - 260, y + 18); c.curve_to(x - 100, y + 5, x + 100, y + 5, x + 270, y + 12)
    c.set_source_rgba(*hexc('#2E7D32')); c.set_line_width(5); c.stroke()
    for k in range(-3, 4):
        c.move_to(x + k * 70, y + 10); c.line_to(x + k * 70 + 30, y - 35 + abs(k) * 8)
        c.move_to(x + k * 70, y + 14); c.line_to(x + k * 70 + 30, y + 55 - abs(k) * 8)
    c.set_line_width(3); c.stroke()

def zzz(c, x, y, t, t0):
    if t < t0: return
    font(c, 60)
    for k in range(3):
        p = ((t - t0) / 3.0 - k / 3.0)
        if p < 0: continue
        p %= 1.0
        a = math.sin(math.pi * p)
        c.save(); c.translate(x - 60 * p + 25 * math.sin(p * 6), y - 150 * p)
        c.set_font_size(50 + 50 * p); c.move_to(0, 0); c.text_path('Z')
        c.set_source_rgba(1, 1, 1, a); c.fill_preserve(); c.set_source_rgba(0.24, 0.2, 0.55, a); c.set_line_width(4); c.stroke()
        c.restore()

TITO_W = [(0.5, -300), (6.5, TX)]
YAWNS = [(11.5, 14.0), (23.5, 26.0)]

def tito_state(t):
    x = kf(t, TITO_W)
    yawn = 0.0
    for (a, b) in YAWNS:
        if a < t < b: yawn = math.sin(math.pi * (t - a) / (b - a))
    sleepy = ss(14, 26, t)
    lid = max(0.35 * ss(13, 15, t), 0.55 * ss(20, 22, t), ss(31, 34, t), 0.8 * yawn)
    for bt in (4.0, 9.0):
        if abs(t - bt) < 0.13: lid = max(lid, 1 - abs(t - bt) / 0.13)
    if 18.5 < t < 19.5: lid = max(lid, 1 - abs(t - 19) / 0.5)
    sink = 95 * ss(27, 31, t)
    breathe = 4 * math.sin(2 * math.pi * t / 3.5) * ss(33, 35, t)
    look = (0.5, -0.8) if 6.5 < t < 11 else ((0.3, -1) if 15 < t < 23 else (0, 0))
    return x, sink + breathe, lid, yawn, look

def lola_state(t):
    if t < 15: return 2100, 300, 0.0, 22
    x = kf(t, [(15, 2100), (18.5, TX + 160), (28.5, TX + 160), (30.5, TX)])
    head_top = GROUND + tito_state(t)[1] - 0.6 * 455
    y = kf(t, [(15, 260), (18.5, 520), (28.5, 520), (30.5, head_top)])
    flap = 18 if t < 30.5 else None
    lid = ss(33.5, 35.5, t)
    if t < 30.5: y += 15 * math.sin(t * 3)
    return x, y, lid, flap

def world(c, t):
    c.set_source_surface(SKY, 0, 0); c.paint()
    N.stars(c, t); N.shooting(c, t)
    for i, (x0, y0, s, sp) in enumerate(((200, 170, 1.0, 10), (900, 110, 0.8, 7), (1250, 300, 0.7, 12))):
        N.cloud(c, (x0 + sp * t) % 2300 - 250, y0 + 8 * math.sin(t * 0.5 + i), s)
    N.sun(c, t)
    N.hills(c)
    N.palm(c, 160, 900, 560, t * 0.5, 0, 1)
    N.palm(c, 1780, 900, 520, t * 0.5, 1.7, -1)
    N.bush(c, 420, 840, 0.6, '#2E7D32'); N.bush(c, 1500, 850, 0.6, '#388E3C')
    for i, (fx, col) in enumerate(((300, '#FF4081'), (560, '#FF9100'), (1330, '#E040FB'), (1620, '#FF4081'))):
        N.flower(c, fx, 900, col, t * 0.5, i * 1.3)
    x, sink, lid, yawn, look = tito_state(t)
    leaf_bed(c, TX, GROUND, front=False)
    K.put(c, K.tito, x, GROUND + sink, 0.6, t=t, look=look, lid=lid, yawn=yawn, walk=t * 4 if moving(t, TITO_W) else 0)
    if t > 26.5:
        c.push_group(); leaf_bed(c, TX, GROUND - 20, front=True); c.pop_group_to_source()
        c.paint_with_alpha(ss(26.5, 28.5, t))
    lx, ly, llid, flap = lola_state(t)
    if t > 15:
        K.put(c, K.lola, lx, ly, 0.5, t=t, flap=flap, lid=llid, look=(-0.6, 0.4))
        if 19 < t < 31:
            for k in range(3):
                ph = (t * 0.45 + k / 3) % 1
                music_note(c, lx + 40 + 60 * ph + 20 * math.sin(ph * 8), ly - 150 - 160 * ph, math.sin(math.pi * ph), ['#F48FB1', '#81D4FA', '#FFF59D'][k])
    zzz(c, TX - 160, GROUND + sink - 250, t, 35.0)
    N.fireflies(c, t * 0.5)

def overlay(c, t):
    if t < 6.0:
        a = 1 - ss(5.0, 5.8, t)
        c.push_group(); word(c, 'Tito se va a dormir', W / 2, 230, 115 * K_back((t - 0.8) / 0.6) + 0.01, colors=NIGHT, tilt=0.05, outline=9)
        c.pop_group_to_source(); c.paint_with_alpha(a)
    if t > 44:
        a = ss(44, 45, t)
        s = K_back((t - 44) / 0.8)
        c.push_group()
        word(c, '¡Buenas noches,', W / 2, 190, 105 * s + 0.01, colors=NIGHT, tilt=0.05, outline=9)
        word(c, 'Tito!', W / 2, 330, 130 * s + 0.01, colors=NIGHT, start=2, tilt=0.05, outline=10)
        c.pop_group_to_source(); c.paint_with_alpha(a)
    a = max(1 - ss(0, 1.0, t), ss(DUR - 4.0, DUR, t))
    if a > 0: c.set_source_rgba(0.05, 0.04, 0.2, a); c.paint()

CAM = [(0, 1.0, 960, 540), (8, 1.0, 960, 540), (12, 1.2, 1000, 600), (26, 1.25, 1000, 620), (34, 1.4, 960, 660), (60, 1.5, 960, 660)]
def camera(t):
    z = kf(t, [(a, b) for a, b, _, _ in CAM]); x = kf(t, [(a, d) for a, _, d, _ in CAM]); y = kf(t, [(a, e) for a, _, _, e in CAM])
    x = max(W / (2 * z), min(W - W / (2 * z), x)); y = max(H / (2 * z), min(H - H / (2 * z), y))
    return x, y, z

def frame(c, t):
    cx, cy, z = camera(t)
    c.save(); c.translate(W / 2, H / 2); c.scale(z, z); c.translate(-cx, -cy)
    world(c, t)
    c.restore()
    overlay(c, t)

if __name__ == '__main__':
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(surf)
    args = sys.argv[1:]
    if args and args[0] == 'stills':
        for t in map(float, args[1:]):
            c.save(); frame(c, t); c.restore(); surf.write_to_png(f'ep06_{t}.png')
    else:
        t0, t1 = (float(args[1]), float(args[2])) if args and args[0] == 'range' else (0, DUR)
        out = sys.stdout.buffer
        for i in range(int(round(t0 * FPS)), int(round(t1 * FPS))):
            c.save(); frame(c, i / FPS); c.restore(); surf.flush(); out.write(surf.get_data())
