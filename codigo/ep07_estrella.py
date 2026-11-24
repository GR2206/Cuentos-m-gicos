"""Episodio 7 — La estrella que se cayó (A dormir con…, 100 s).
Una estrellita bebé se cae del cielo a la selva. Coco la encuentra y todos intentan devolverla:
Coco salta, Pipa estira el cuello, Tito sopla con la trompa... y Lola la lleva volando.
La estrellita les agradece dibujando un corazón de estrellas en el cielo.

Uso:  python3 ep07_estrella.py                -> cuadros crudos por stdout
      python3 ep07_estrella.py range 0 50     -> solo un tramo
      python3 ep07_estrella.py stills 12 65   -> PNG sueltos"""
import cairo, math, sys
import escena_noche as N
import cuerpos as K
from amigos import hexc, ellipse, fill, OUT
from logos import word, sparkle, font
from ep02_puente_del_rio import kf, ss, moving, K_back, music_note
from ep03_donde_esta_tomi import bubble

W, H, FPS = 1920, 1080, 30
DUR = 100.0
GROUND = 880
SLOT = (680, 150)                 # el lugar de la estrellita en el cielo
BUSH = (1350, 840)
NIGHT = ['#FFF59D', '#FFD54F', '#B39DDB', '#81D4FA', '#F48FB1', '#FFFFFF']
N.SHOOT = ()

SKY = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); N.sky(cairo.Context(SKY))

def baby_star(c, x, y, t, r=55, mood='happy', glow=1.0, lid=0.0):
    g = cairo.RadialGradient(x, y, 0, x, y, r * 3.2)
    g.add_color_stop_rgba(0, 1, 0.95, 0.5, 0.55 * glow); g.add_color_stop_rgba(1, 1, 0.95, 0.5, 0)
    c.set_source(g); c.arc(x, y, r * 3.2, 0, 2 * math.pi); c.fill()
    c.save(); c.translate(x, y); c.rotate(0.08 * math.sin(t * 2.5))
    pts = []
    for i in range(10):
        rr = r if i % 2 == 0 else r * 0.52
        a = -math.pi / 2 + i * math.pi / 5
        pts.append((rr * math.cos(a), rr * math.sin(a)))
    c.move_to(*pts[0])
    for p in pts[1:]: c.line_to(*p)
    c.close_path(); c.set_line_join(cairo.LINE_JOIN_ROUND)
    fill(c, hexc('#FFE14D'), hexc('#E0A800'), 6)
    s = r / 55
    for ex in (-16, 16):
        if lid > 0.9:
            c.set_source_rgba(*OUT); c.set_line_width(4 * s); c.arc(ex * s, 2 * s, 7 * s, 0.15 * math.pi, 0.85 * math.pi); c.stroke()
        else:
            ellipse(c, ex * s, 0, 8 * s, 10 * s); fill(c, hexc('#3B2314'))
            ellipse(c, ex * s + 3 * s, -3 * s, 3 * s, 3 * s); c.set_source_rgba(1, 1, 1, 1); c.fill()
    for ex in (-28, 28):
        ellipse(c, ex * s, 12 * s, 7 * s, 5 * s); c.set_source_rgba(*hexc('#FF7043', 0.6)); c.fill()
    c.set_source_rgba(*OUT); c.set_line_width(4 * s); c.set_line_cap(cairo.LINE_CAP_ROUND)
    if mood == 'sad':
        c.arc(0, 24 * s, 9 * s, 1.2 * math.pi, 1.8 * math.pi); c.stroke()
        for ex in (-1, 1):
            c.move_to(ex * 8 * s, -16 * s); c.line_to(ex * 22 * s, -12 * s); c.stroke()
    else:
        c.arc(0, 10 * s, 10 * s, 0.15 * math.pi, 0.85 * math.pi); c.stroke()
    c.restore()

def slot_outline(c, t, a):
    if a <= 0: return
    c.save(); c.set_dash([10, 10], t * 20)
    N.star_shape(c, SLOT[0], SLOT[1], 60, 0)
    c.set_source_rgba(1, 1, 0.8, a * (0.5 + 0.5 * math.sin(t * 5))); c.set_line_width(5); c.stroke()
    c.restore()

HEART = [(0, -40), (60, -110), (140, -110), (180, -40), (140, 50), (70, 120), (0, 180), (-70, 120), (-140, 50), (-180, -40), (-140, -110), (-60, -110)]
def constellation(c, t, t0, cx=430, cy=300):
    if t < t0: return
    n = len(HEART)
    p = (t - t0) / 6.0
    shown = min(n, int(p * n) + 1)
    c.set_source_rgba(1, 1, 0.85, 0.75); c.set_line_width(4); c.set_line_cap(cairo.LINE_CAP_ROUND)
    for i in range(shown - 1 if p < 1 else n):
        x0, y0 = HEART[i]; x1, y1 = HEART[(i + 1) % n]
        c.move_to(cx + x0, cy + y0); c.line_to(cx + x1, cy + y1); c.stroke()
    for i in range(shown):
        x, y = HEART[i]
        k = 0.7 + 0.3 * math.sin(t * 4 + i)
        g = cairo.RadialGradient(cx + x, cy + y, 0, cx + x, cy + y, 40)
        g.add_color_stop_rgba(0, 1, 0.95, 0.6, 0.6 * k); g.add_color_stop_rgba(1, 1, 0.95, 0.6, 0)
        c.set_source(g); c.arc(cx + x, cy + y, 40, 0, 2 * math.pi); c.fill()
        N.star_shape(c, cx + x, cy + y, 16 * k, 0); c.set_source_rgba(1, 0.95, 0.5, 1); c.fill()

# ---------------- historia ----------------
COCO_X = [(10, -250), (15, 1180), (19, 1180), (20, 1100), (29, 1100), (31, 820), (82, 820)]
PIPA_X = [(29, -300), (32.5, 980), (82, 980)]
TITO_X = [(38, -350), (41.5, 1250), (82, 1250)]
TOMI_X = [(66, -250), (80, 560), (100, 560)]
COCO_JUMPS = [24.6, 25.9, 27.2]
FALL = (7.6, 10.0)

def star_pos(t):
    """Posición, ánimo y brillo de la estrellita."""
    if t < FALL[0]:
        wob = 6 * math.sin(t * 20) if t > 6.4 else 0
        return SLOT[0] + wob, SLOT[1], 'happy' if t < 6.4 else 'sad', 1.0
    if t < FALL[1]:
        p = (t - FALL[0]) / (FALL[1] - FALL[0]); e = p * p
        return SLOT[0] + (BUSH[0] - SLOT[0]) * p, SLOT[1] + (BUSH[1] - 60 - SLOT[1]) * e, 'sad', 1.0
    if t < 16: return BUSH[0], BUSH[1] - 60 - (90 * ss(15.2, 16, t)), 'sad', 0.6 + 0.4 * ss(15, 16, t)
    cx = kf(t, COCO_X)
    above_coco = (cx + 10, GROUND - 0.55 * 480 - 80 - sum(hop(t, j) for j in COCO_JUMPS))
    if t < 32.5:
        if t < 17.5: return kf(t, [(16, BUSH[0]), (17.5, above_coco[0])]), kf(t, [(16, BUSH[1] - 150), (17.5, above_coco[1])]), 'sad', 1.0
        return above_coco[0], above_coco[1], 'sad' if t < 21 else 'happy', 1.0
    px = kf(t, PIPA_X)
    neck = pipa_neck(t)
    pipa_top = (px, GROUND - 0.55 * (260 + neck + 175) - 40)
    if t < 33.6:
        q = (t - 32.5) / 1.1
        return above_coco[0] + (pipa_top[0] - above_coco[0]) * q, above_coco[1] + (pipa_top[1] - above_coco[1]) * q - 120 * math.sin(math.pi * q), 'happy', 1.0
    if t < 51.2:
        y = pipa_top[1] - hop(t, 36.0, 90, 1.2) - (kf(t, [(43, 0), (45, 190), (47, 0)]) if 43 < t < 47 else 0)
        return pipa_top[0], y, 'happy', 1.0
    lx, ly = lola_pos(t)
    if t < 58.5: return lx, ly + 40, 'happy', 1.0
    return SLOT[0], SLOT[1], 'happy', 1.0 + 0.8 * math.sin(math.pi * ss(58.5, 62, t))

def hop(t, t0, h=150, d=0.9):
    p = (t - t0) / d
    return h * math.sin(math.pi * p) if 0 <= p <= 1 else 0.0

def pipa_neck(t): return kf(t, [(33.8, 300), (35.5, 650), (37.2, 650), (38.5, 300)])

def lola_pos(t):
    if t < 48: return 2150, 250
    x = kf(t, [(48, 2150), (50.5, 1060), (51.2, 1000), (57.5, SLOT[0]), (58.5, SLOT[0] + 60), (63, 1100)])
    y = kf(t, [(48, 250), (50.5, 330), (51.2, kf(51.2, [(0, 0)]) + 330), (57.5, SLOT[1] - 60), (58.5, SLOT[1] - 90), (63, 470)])
    return x, y + 12 * math.sin(t * 3)

def world(c, t):
    c.set_source_surface(SKY, 0, 0); c.paint()
    N.stars(c, t)
    for i, (x0, y0, s, sp) in enumerate(((1500, 330, 0.7, 6), (300, 420, 0.6, 5))):
        N.cloud(c, (x0 + sp * t) % 2300 - 250, y0 + 8 * math.sin(t * 0.5 + i), s)
    N.sun(c, t)
    slot_outline(c, t, ss(20.5, 21.5, t) * (1 - ss(57.5, 58.5, t)))
    constellation(c, t, 63.5)
    # shower of sparkles when the star is back home
    q = (t - 58.5) / 2.0
    if 0 <= q <= 1:
        for k in range(12):
            a = k * math.pi / 6
            sparkle(c, SLOT[0] + 220 * q * math.cos(a), SLOT[1] + 180 * q * math.sin(a), 30 * math.sin(math.pi * q), '#FFF59D' if k % 2 else '#FFFFFF')
    N.hills(c)
    N.palm(c, 120, 900, 560, t * 0.5, 0, 1)
    N.palm(c, 1800, 900, 520, t * 0.5, 1.7, -1)
    for i, (fx, col) in enumerate(((300, '#FF4081'), (560, '#FF9100'), (1600, '#E040FB'))):
        N.flower(c, fx, 900, col, t * 0.5, i * 1.3)
    sx, sy, smood, sglow = star_pos(t)
    falling = FALL[0] <= t < FALL[1]
    if falling:  # trail
        for k in range(1, 9):
            tt = t - k * 0.05
            if tt < FALL[0]: break
            px_, py_, _, _ = star_pos(tt)
            sparkle(c, px_, py_, 22 - 2 * k, '#FFF59D')
    in_bush = FALL[1] <= t < 15.4
    if in_bush:  # glow behind the bush
        g = cairo.RadialGradient(BUSH[0], BUSH[1] - 40, 0, BUSH[0], BUSH[1] - 40, 220)
        g.add_color_stop_rgba(0, 1, 0.95, 0.5, 0.6 + 0.2 * math.sin(t * 4)); g.add_color_stop_rgba(1, 1, 0.95, 0.5, 0)
        c.set_source(g); c.arc(BUSH[0], BUSH[1] - 40, 220, 0, 2 * math.pi); c.fill()
    N.bush(c, BUSH[0], BUSH[1], 0.75 + (0.03 * math.sin(t * 30) if 14.5 < t < 15.5 else 0), '#2E7D32')
    N.bush(c, 420, 845, 0.55, '#388E3C')
    # Pipa
    if t > 29:
        px = kf(t, PIPA_X); neck = pipa_neck(t)
        pl = (0.3, -1) if 34 < t < 47 else ((0, -1) if 51 < t < 75 else (0.4, 0))
        K.put(c, K.pipa, px, GROUND, 0.55, t=t, neck=neck, look=pl, walk=t * 7 if moving(t, PIPA_X) else 0)
    # Tito
    if t > 38:
        tx = kf(t, TITO_X)
        tl = (-0.6, -1) if 41 < t < 75 else (-0.3, 0)
        lid = ss(86, 90, t) * 0.9
        K.put(c, K.tito, tx, GROUND, 0.6, t=t, look=tl, lid=lid, walk=t * 6 if moving(t, TITO_X) else 0)
        if 43 < t < 45.5:  # trumpet puff upwards
            q = (t - 43) / 2.5
            tipx, tipy = tx + 0.6 * 180, GROUND - 0.6 * 115
            for k in range(5):
                u = (q * 1.5 - k * 0.12)
                if 0 < u < 1:
                    ellipse(c, tipx - (tipx - kf(t, PIPA_X)) * u, tipy - 300 * u, 16 + 20 * u, 12 + 14 * u)
                    c.set_source_rgba(1, 1, 1, 0.6 * (1 - u)); c.fill()
    # Tomi
    if t > 66:
        tmx = kf(t, TOMI_X)
        K.put(c, K.tomi, tmx, GROUND, 0.55, t=t, look=(0.5, -0.6), walk=t * 3 if moving(t, TOMI_X) else 0)
    # Coco
    if t > 10:
        cx = kf(t, COCO_X)
        cj = sum(hop(t, j) for j in COCO_JUMPS)
        mood, look = 'smile', (1, 0)
        arm_r, arm_l = math.radians(65 + 6 * math.sin(t * 2)), math.radians(115 - 6 * math.sin(t * 2))
        if 13 < t < 16: mood = 'o'; look = (1, 0.3)
        if 16 < t < 32.5:
            arm_r, arm_l = math.radians(-65), math.radians(-115); look = (0, -1)
            mood = 'o' if t < 19 else 'smile'
        if 32.5 < t < 82: look = (0.3, -1) if t < 75 else (0, -0.5)
        if 58.5 < t < 62: y_cheer = -30 * abs(math.sin(t * 6))
        else: y_cheer = 0
        lid = ss(86, 90, t) * 0.95
        K.put(c, K.coco, cx, GROUND - cj + y_cheer, 0.55, t=t, mood=mood if t < 84 else 'closed', look=look, lid=lid,
              arm_r=arm_r, arm_l=arm_l, walk=t * 8 if moving(t, COCO_X) else 0)
    # the baby star (on top of everybody)
    if not in_bush or t > 15.2:
        r = 55 if t < 58.5 else 55 - 20 * ss(62, 66, t)
        baby_star(c, sx, sy, t, r, smood, sglow, lid=ss(90, 92, t))
    # Lola
    if t > 48:
        lx, ly = lola_pos(t)
        K.put(c, K.lola, lx, ly, 0.5, t=t, flap=20 if t < 85 else None, look=(-0.5, 0.6) if t < 58 else (0, -0.6),
              lid=ss(86, 90, t))
    # bubbles
    bubble(c, sx + 180, sy - 60, '¡Me caí del cielo!', (t - 16.2) / 3.2, 46)
    bubble(c, kf(t, COCO_X), GROUND - 300, '¡Te ayudamos!', (t - 21.4) / 2.8, 46)
    bubble(c, kf(t, PIPA_X) + 40, GROUND - 0.55 * (260 + pipa_neck(t) + 175) - 150, '¡Casi!', (t - 45.6) / 2.2, 52)
    bubble(c, SLOT[0] + 40, SLOT[1] + 150, '¡Gracias, amigos!', (t - 59.0) / 3.2, 46)
    bubble(c, kf(t, TOMI_X), GROUND - 200, '¡Qué lindo!', (t - 80.2) / 2.8, 48)
    N.fireflies(c, t * 0.5)

def overlay(c, t):
    if t < 6.0:
        a = 1 - ss(5.0, 5.8, t)
        c.push_group()
        word(c, 'La estrella', W / 2, 360, 115 * K_back((t - 0.8) / 0.6) + 0.01, colors=NIGHT, tilt=0.05, outline=9)
        word(c, 'que se cayó', W / 2, 490, 115 * K_back((t - 1.0) / 0.6) + 0.01, colors=NIGHT, start=3, tilt=0.05, outline=9)
        c.pop_group_to_source(); c.paint_with_alpha(a)
    if t > 88:
        s = K_back((t - 88) / 0.8)
        c.push_group()
        word(c, '¡Buenas noches,', W / 2, 190, 105 * s + 0.01, colors=NIGHT, tilt=0.05, outline=9)
        word(c, 'estrellita!', W / 2, 330, 120 * s + 0.01, colors=NIGHT, start=2, tilt=0.05, outline=10)
        c.pop_group_to_source(); c.paint_with_alpha(ss(88, 89, t))
    a = max(1 - ss(0, 1.0, t), ss(DUR - 4.0, DUR, t))
    if a > 0: c.set_source_rgba(0.05, 0.04, 0.2, a); c.paint()

CAM = [(0, 1.0, 960, 540), (11, 1.0, 960, 540), (13.5, 1.35, 1150, 640), (29, 1.35, 1100, 620), (31, 1.0, 960, 540),
       (84, 1.0, 960, 540), (90, 1.15, 960, 560), (100, 1.2, 960, 560)]
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
            c.save(); frame(c, t); c.restore(); surf.write_to_png(f'ep07_{t}.png')
    else:
        t0, t1 = (float(args[1]), float(args[2])) if args and args[0] == 'range' else (0, DUR)
        out = sys.stdout.buffer
        for i in range(int(round(t0 * FPS)), int(round(t1 * FPS))):
            c.save(); frame(c, i / FPS); c.restore(); surf.flush(); out.write(surf.get_data())
