"""Episodio 8 — El arcoíris perdido (aventurita para aprender los colores, 112 s).
El arcoíris pierde sus colores y se esconden por la selva. Cada amigo encuentra uno:
Coco el ROJO en una flor, Lola el NARANJA en un árbol, Tito el AMARILLO en las bananas,
Pipa el VERDE en la palmera, Tomi el AZUL en la laguna y Coco el VIOLETA en una mariposa.

Uso:  python3 ep08_arcoiris_perdido.py                -> cuadros crudos por stdout
      python3 ep08_arcoiris_perdido.py range 0 56     -> solo un tramo
      python3 ep08_arcoiris_perdido.py stills 12 65   -> PNG sueltos"""
import cairo, math, sys
import amigos as A, cuerpos as K
from amigos import hexc, ellipse, fill, OUT
from logos import word, sparkle, font
from ep02_puente_del_rio import kf, ss, moving, K_back, music_note, palm
from ep03_donde_esta_tomi import bubble
from ep04_lluvia_magica import sun
from escena_dia import butterfly

W, H, FPS = 1920, 1080, 30
DUR = 112.0
GROUND = 880
RB = (960, 1000)                          # centro del arcoíris

COLORS = [  # nombre, color, lugar donde se esconde, quién lo encuentra
    ('¡ROJO!', '#F44336', (395, 800), 'coco'),
    ('¡NARANJA!', '#FF9800', (1470, 560), 'lola'),
    ('¡AMARILLO!', '#FFEB3B', (1745, 790), 'tito'),
    ('¡VERDE!', '#4CAF50', (215, 370), 'pipa'),
    ('¡AZUL!', '#2196F3', (1090, 915), 'tomi'),
    ('¡VIOLETA!', '#9C27B0', None, 'coco'),
]
STARTS = [16.0, 28.5, 41.0, 53.5, 66.0, 78.5]
LOSS = 6.5
BAND_ANG = [math.pi * (1.15 + 0.14 * k) for k in range(6)]

# ---------------- escenario ----------------
def make_layers():
    sky = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(sky)
    g = cairo.LinearGradient(0, 0, 0, H)
    for k, col in enumerate(('#29B6F6', '#81D4FA', '#B3E5FC')): g.add_color_stop_rgb(k / 2, *hexc(col)[:3])
    c.set_source(g); c.paint()
    land = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(land)
    c.move_to(0, 650); c.curve_to(350, 520, 700, 540, 980, 650); c.curve_to(1250, 560, 1600, 520, 1920, 620)
    c.line_to(1920, H); c.line_to(0, H); c.close_path(); c.set_source_rgba(*hexc('#66BB6A')); c.fill()
    c.move_to(0, 750); c.curve_to(450, 690, 900, 710, 1920, 740); c.line_to(1920, H); c.line_to(0, H); c.close_path()
    c.set_source_rgba(*hexc('#43A047')); c.fill()
    c.rectangle(0, 805, W, H - 805); c.set_source_rgba(*hexc('#8BC34A')); c.fill()
    c.move_to(0, 810); c.curve_to(600, 785, 1300, 785, 1920, 810); c.line_to(1920, 830); c.line_to(0, 830); c.close_path(); c.fill()
    # pond
    ellipse(c, 1090, 925, 170, 38); fill(c, hexc('#4FC3F7'), hexc('#0288D1'), 6)
    ellipse(c, 1040, 918, 60, 9); c.set_source_rgba(1, 1, 1, 0.5); c.fill()
    # orange tree
    x = 1470
    c.move_to(x - 25, GROUND); c.line_to(x - 18, 640); c.line_to(x + 18, 640); c.line_to(x + 25, GROUND); c.close_path()
    fill(c, hexc('#8D5524'), OUT, 6)
    for (cx, cy, r) in ((x - 90, 600, 85), (x + 90, 600, 85), (x, 520, 110), (x, 630, 90)):
        ellipse(c, cx, cy, r, r); c.set_source_rgba(*hexc('#2E7D32')); c.fill()
    for (fx, fy) in ((x - 110, 570), (x + 70, 520), (x + 115, 620), (x - 40, 470), (x - 60, 650)):
        ellipse(c, fx, fy, 20, 20); fill(c, hexc('#FB8C00'), OUT, 4)
    # banana plant
    x = 1760
    c.set_line_cap(cairo.LINE_CAP_ROUND)
    c.move_to(x, GROUND); c.line_to(x, 620); c.set_source_rgba(*OUT); c.set_line_width(58); c.stroke()
    c.move_to(x, GROUND); c.line_to(x, 620); c.set_source_rgba(*hexc('#9CCC65')); c.set_line_width(46); c.stroke()
    for i, ang in enumerate((-150, -110, -70, -30, 200)):
        c.save(); c.translate(x, 620); c.rotate(math.radians(ang))
        c.move_to(0, 0); c.curve_to(50, -60, 180, -60, 240, 0); c.curve_to(180, 35, 50, 35, 0, 0); c.close_path()
        c.set_source_rgba(*hexc('#43A047' if i % 2 else '#66BB6A')); c.fill(); c.restore()
    c.set_source_rgba(*hexc('#558B2F')); c.set_line_width(8); c.move_to(x - 10, 650); c.line_to(x - 25, 740); c.stroke()
    K.bunch(c, x - 25, 745, 0.9)
    # big red flower
    x = 395
    c.set_line_width(12); c.set_source_rgba(*hexc('#2E7D32')); c.move_to(x, GROUND); c.line_to(x, 820); c.stroke()
    for side in (-1, 1):
        c.save(); c.translate(x, 860); c.rotate(side * 0.6); ellipse(c, side * 30, 0, 34, 14); fill(c, hexc('#43A047'), OUT, 4); c.restore()
    for i in range(6):
        a = i * math.pi / 3; ellipse(c, x + 38 * math.cos(a), 800 + 38 * math.sin(a), 30, 30); fill(c, hexc('#E53935'), OUT, 4)
    ellipse(c, x, 800, 24, 24); fill(c, hexc('#FFEB3B'), OUT, 4)
    for (fx, col) in ((620, '#FF4081'), (1300, '#E040FB'), (60, '#FF9100')):
        c.set_line_width(7); c.set_source_rgba(*hexc('#2E7D32')); c.move_to(fx, 975); c.line_to(fx, 930); c.stroke()
        for i in range(6):
            a = i * math.pi / 3; ellipse(c, fx + 20 * math.cos(a), 925 + 20 * math.sin(a), 15, 15); c.set_source_rgba(*hexc(col)); c.fill()
        ellipse(c, fx, 925, 12, 12); c.set_source_rgba(*hexc('#FFEB3B')); c.fill()
    return sky, land

SKY, LAND = make_layers()

def clouds(c, t):
    for (x0, y0, s, sp) in ((150, 150, 0.9, 12), (820, 90, 0.7, 8), (1250, 210, 0.6, 15)):
        c.save(); c.translate((x0 + sp * t) % 2300 - 250, y0); c.scale(s, s)
        for (cx, cy, r) in ((0, 0, 60), (70, -30, 75), (150, 0, 60), (75, 20, 60)): ellipse(c, cx, cy, r, r)
        c.set_source_rgba(1, 1, 1, 1); c.fill(); c.restore()

def band_color(k, t):
    """Cuánto color tiene la banda k (1 = completa, 0 = gris)."""
    lost = ss(LOSS + 0.25 * k, LOSS + 0.25 * k + 0.6, t)
    back = ss(STARTS[k] + 9.6, STARTS[k] + 10.4, t)
    return max(1 - lost, back)

def rainbow(c, t):
    c.save(); c.set_line_cap(cairo.LINE_CAP_BUTT)
    for k, (_, col, _, _) in enumerate(COLORS):
        r = 860 - k * 44
        c.set_source_rgba(*hexc('#ECEFF1', 0.55)); c.set_line_width(46); c.arc(RB[0], RB[1], r, math.pi, 2 * math.pi); c.stroke()
        a = band_color(k, t)
        if a > 0:
            c.set_source_rgba(*hexc(col, 0.9 * a)); c.set_line_width(46); c.arc(RB[0], RB[1], r, math.pi, 2 * math.pi); c.stroke()
    c.restore()

def orb(c, x, y, col, t, r=26, glow=1.0):
    g = cairo.RadialGradient(x, y, 0, x, y, r * 2.6)
    g.add_color_stop_rgba(0, *hexc(col)[:3], 0.55 * glow); g.add_color_stop_rgba(1, *hexc(col)[:3], 0)
    c.set_source(g); c.arc(x, y, r * 2.6, 0, 2 * math.pi); c.fill()
    ellipse(c, x, y, r, r); fill(c, hexc(col), OUT, 4)
    ellipse(c, x - r * 0.35, y - r * 0.35, r * 0.3, r * 0.3); c.set_source_rgba(1, 1, 1, 0.7); c.fill()
    sparkle(c, x + r * 0.9, y - r * 0.9, 10 + 4 * math.sin(t * 5), '#FFFFFF')

def band_point(k):
    r = 860 - k * 44; a = BAND_ANG[k]
    return RB[0] + r * math.cos(a), RB[1] + r * math.sin(a)

BFLY_REST = (1300, 880)
def butterfly_pos(t):
    s = STARTS[5]
    if t < LOSS + 2.0: return None
    if t < s: return BFLY_REST[0], BFLY_REST[1] + 3 * math.sin(t * 2)
    if t < s + 2.0:
        q = (t - s) / 2.0
        return BFLY_REST[0] + (760 - BFLY_REST[0]) * q, BFLY_REST[1] + (560 - BFLY_REST[1]) * q - 120 * math.sin(math.pi * q)
    w = 2 * math.pi / 4.5
    if t < s + 6.5:
        return 760 + 220 * math.sin(w * (t - s - 2.0)), 560 + 60 * math.sin(2 * w * (t - s - 2.0))
    return 760 + 120 * (t - s - 6.5), 560 - 60 * (t - s - 6.5)

def orb_pos(k, t):
    """Dónde está la bolita de color k: None si ya volvió al arcoíris."""
    name, col, spot, who = COLORS[k]
    s = STARTS[k]
    if t < LOSS + 0.25 * k: return None
    if spot is None:
        bp = butterfly_pos(t)
        spot = bp if bp else (760, 560)
    t_fly0 = LOSS + 0.25 * k + 0.4
    if t < t_fly0 + 2.2:  # flies from the band to its hiding spot
        bx, by = band_point(k)
        q = max(0.0, min(1.0, (t - t_fly0) / 2.2))
        if k == 5: spot = BFLY_REST
        return bx + (spot[0] - bx) * q, by + (spot[1] - by) * q - 260 * math.sin(math.pi * q), 0.8
    if t < s + 6.5: return spot[0], spot[1], 0.45 + 0.25 * math.sin(t * 4 + k)   # hidden, glowing softly
    if t < s + 8.0: return spot[0], spot[1] - 80 * K_back((t - s - 6.5) / 0.5), 1.0  # pops out
    if t < s + 10.2:  # back to the rainbow
        q = (t - s - 8.0) / 2.2
        sx, sy = spot[0], spot[1] - 80
        bx, by = band_point(k)
        return sx + (bx - sx) * q, sy + (by - sy) * q - 200 * math.sin(math.pi * q), 1.0
    return None

# ---------------- personajes ----------------
def seg(t, k): return STARTS[k], (t - STARTS[k])

COCO_BASE, PIPA_BASE, TITO_BASE, TOMI_BASE = 760, 560, 960, 1240
def go(t, s, base, target, d_out=4.5, ret=10.0, d_ret=2.2):
    return kf(t, [(s, base), (s + d_out, target), (s + ret, target), (s + ret + d_ret, base)])

def coco_x(t):
    if t < STARTS[3]: return go(t, STARTS[0], COCO_BASE, 470)
    return COCO_BASE

def tito_x(t): return go(t, STARTS[2], TITO_BASE, 1560)
def pipa_x(t): return go(t, STARTS[3], PIPA_BASE, 300)
def tomi_x(t): return go(t, STARTS[4] - 2.0, TOMI_BASE, 1180, d_out=6.5, ret=12.0, d_ret=0.1)

def lola_pos(t):
    s = STARTS[1]
    x = kf(t, [(s, 900), (s + 4.5, 1400), (s + 10, 1400), (s + 12, 900)])
    y = kf(t, [(s, 450), (s + 4.5, 520), (s + 10, 520), (s + 12, 450)])
    return x, y + 15 * math.sin(t * 3)

def party(t): return t < 5.5 or t > 92

def world(c, t):
    c.set_source_surface(SKY, 0, 0); c.paint()
    sun(c, t); clouds(c, t)
    rainbow(c, t)
    c.set_source_surface(LAND, 0, 0); c.paint()
    palm(c, 150, GROUND, 520, 1, t)
    # hidden orbs (behind characters, in front of the land)
    for k in range(6):
        p = orb_pos(k, t)
        if p and k != 5 and t < STARTS[k] + 6.5 and t > LOSS + 3: orb(c, p[0], p[1], COLORS[k][1], t, 24, p[2])
    bounce = lambda ph: -25 * abs(math.sin(t * 4.5 + ph)) if party(t) else 0
    sad = 8.5 < t < 12.5
    # Pipa
    s = STARTS[3]
    px = pipa_x(t)
    neck = kf(t, [(s + 4.0, 300), (s + 5.5, 620), (s + 9.5, 620), (s + 11, 300)])
    lean = kf(t, [(s + 4.0, 0), (s + 5.5, -150), (s + 9.5, -150), (s + 11, 0)])
    pl = (-1, -0.6) if s + 4 < t < s + 10 else ((0, -1) if sad else (0.3, 0))
    K.put(c, K.pipa, px, GROUND + bounce(0.5), 0.55, t=t, neck=neck, lean=lean, look=pl, walk=t * 7 if moving(t, [(s, PIPA_BASE), (s + 4.5, 300), (s + 10, 300), (s + 12.2, PIPA_BASE)]) else 0)
    # Tito
    s = STARTS[2]
    tx = tito_x(t)
    reach = None
    if s + 4.6 < t < s + 10.5: reach = kf(t, [(s + 4.6, 150), (s + 6.0, 270), (s + 9.5, 270), (s + 10.5, 150)])
    tl = (1, 0.3) if s + 4 < t < s + 10 else ((0, -1) if sad else (0, 0))
    K.put(c, K.tito, tx, GROUND + bounce(1.0), 0.6, t=t, look=tl, reach=reach,
          walk=t * 6 if moving(t, [(s, TITO_BASE), (s + 4.5, 1560), (s + 10, 1560), (s + 12.2, TITO_BASE)]) else 0)
    # Tomi
    s = STARTS[4]
    tmx = tomi_x(t)
    tml = (-1, 0.6) if s < t < s + 10 else ((0, -1) if sad else (0, 0))
    K.put(c, K.tomi, tmx, GROUND + bounce(1.5), 0.55, t=t, look=tml, walk=t * 3 if moving(t, [(s - 2, TOMI_BASE), (s + 4.5, 1180)]) else 0)
    if s + 5.5 < t < s + 7:  # bubbles in the pond
        for k in range(4):
            q = ((t - s - 5.5) * 1.5 + k * 0.25) % 1
            ellipse(c, 1090 + (k - 1.5) * 30, 915 - 60 * q, 8 + 4 * q, 8 + 4 * q); c.set_source_rgba(1, 1, 1, 0.8 * (1 - q)); c.set_line_width(3); c.stroke()
    # Coco
    cx = coco_x(t)
    s5 = STARTS[5]
    cj = 0.0
    for j in (s5 + 5.3, s5 + 6.1):
        p = (t - j) / 0.7
        if 0 <= p <= 1: cj = 150 * math.sin(math.pi * p)
    mood, look = 'smile', (0, 0)
    arm_r, arm_l = math.radians(65 + 6 * math.sin(t * 2)), math.radians(115 - 6 * math.sin(t * 2))
    if party(t):
        arm_r, arm_l = math.radians(-58 + 25 * math.sin(t * 9)), math.radians(-122 - 25 * math.sin(t * 9))
    if LOSS < t < 12.5: mood = 'o'; look = (0, -1)
    if 9 < t < 12.5: mood, look = 'sad', (0, -0.5)
    s0 = STARTS[0]
    if s0 + 4.5 < t < s0 + 8: look = (-0.6, 0.8)
    if s5 < t < s5 + 7:
        bp = butterfly_pos(t)
        look = (max(-1, min(1, (bp[0] - cx) / 300)), -0.8)
        if t > s5 + 5: arm_r, arm_l = math.radians(-70), math.radians(-110)
    blink = 0.0
    for bt in (3.0, 14.0, 26.0, 38.0, 50.0, 62.0, 75.0, 95.0, 104.0):
        if abs(t - bt) < 0.12: blink = 1 - abs(t - bt) / 0.12
    K.put(c, K.coco, cx, GROUND + bounce(0) - cj, 0.55, t=t, mood=mood, sad=1.0 if mood == 'sad' else 0.0, look=look, lid=blink,
          arm_r=arm_r, arm_l=arm_l, walk=t * 8 if moving(t, [(s0, COCO_BASE), (s0 + 4.5, 470), (s0 + 10, 470), (s0 + 12.2, COCO_BASE)]) else 0)
    # Lola
    lx, ly = lola_pos(t)
    K.put(c, K.lola, lx, ly + bounce(2.0), 0.5, t=t, flap=20, look=(0.6, 0.4) if STARTS[1] + 4 < t < STARTS[1] + 10 else (0, -0.8) if sad else (0, 0.3))
    if t > 93:
        for k in range(3):
            ph = (t * 0.7 + k / 3) % 1
            music_note(c, lx + 40 + 60 * ph, ly - 150 - 160 * ph, math.sin(math.pi * ph), ['#E91E63', '#1E88E5', '#FF9800'][k])
    # butterfly carrying violet
    bp = butterfly_pos(t)
    if bp and t < s5 + 12: butterfly(c, bp[0], bp[1], t, '#9C27B0')
    # orbs in flight / popping (on top)
    for k in range(6):
        p = orb_pos(k, t)
        if not p: continue
        hidden = LOSS + 3 <= t < STARTS[k] + 6.5
        if hidden and k != 5: continue
        if hidden and k == 5: orb(c, p[0], p[1] + 26, COLORS[k][1], t, 16, 0.8); continue
        orb(c, p[0], p[1], COLORS[k][1], t, 28, p[2])
    # sparkles when a color is found and when it goes back
    for k in range(6):
        s = STARTS[k]
        for (t0, (x0, y0)) in ((s + 6.5, orb_spot(k, s + 6.5)), (s + 10.2, band_point(k))):
            q = (t - t0) / 1.0
            if 0 <= q <= 1:
                for j in range(8):
                    a = j * math.pi / 4
                    sparkle(c, x0 + 120 * q * math.cos(a), y0 + 90 * q * math.sin(a), 26 * math.sin(math.pi * q), '#FFFFFF' if j % 2 else COLORS[k][1])
    if t > 91:
        for j in range(10):
            ph = (t * 0.6 + j / 10) % 1
            a = math.pi + math.pi * (j + 0.5) / 10
            sparkle(c, RB[0] + 760 * math.cos(a), RB[1] + 760 * math.sin(a), 26 * math.sin(math.pi * ph))
    bubble(c, cx, GROUND - 300, '¡Oh, no!', (t - 8.6) / 2.4, 52)
    bubble(c, cx, GROUND - 300, '¡Busquemos los colores!', (t - 12.0) / 3.4, 46)

def orb_spot(k, t):
    sp = COLORS[k][2]
    if sp is None:
        bp = butterfly_pos(t); return bp if bp else (760, 560)
    return sp

def overlay(c, t):
    if t < 5.6:
        a = 1 - ss(4.8, 5.5, t)
        c.push_group(); word(c, 'El arcoíris perdido', W / 2, 230, 120 * K_back((t - 0.6) / 0.6) + 0.01, tilt=0.05, outline=9)
        c.pop_group_to_source(); c.paint_with_alpha(a)
    for k, (name, col, _, _) in enumerate(COLORS):
        t0 = STARTS[k] + 6.5
        if t0 <= t < t0 + 3.2:
            s = K_back((t - t0) / 0.4) * (1 - ss(t0 + 2.9, t0 + 3.2, t))
            word(c, name, W / 2, 220 + 6 * math.sin(t * 6), 170 * s + 0.01, colors=[col], tilt=0.05, outline=12)
    if 93 <= t < 101:
        # the six colors in a row, one by one
        names = ['rojo', 'naranja', 'amarillo', 'verde', 'azul', 'violeta']
        font(c, 70); widths = [c.text_extents(n + ' ').x_advance for n in names]
        x = W / 2 - sum(widths) / 2
        for k, n in enumerate(names):
            t0 = 93.3 + k * 0.9
            if t >= t0:
                s = K_back((t - t0) / 0.4)
                word(c, n, x + widths[k] / 2, 220, 70 * s + 0.01, colors=[COLORS[k][1]], outline=7)
            x += widths[k]
    if t > 101:
        s = K_back((t - 101) / 0.7)
        word(c, '¡El arcoíris', W / 2, 180, 115 * s + 0.01, tilt=0.06, outline=10)
        word(c, 'volvió!', W / 2, 320, 125 * s + 0.01, start=3, tilt=0.06, outline=10)
    a = max(1 - ss(0, 0.8, t), ss(DUR - 2.0, DUR, t))
    if a > 0: c.set_source_rgba(1, 1, 1, a); c.paint()

FOCUS = [(420, 640), (1430, 560), (1640, 640), (300, 520), (1130, 660), (820, 600)]
def camera(t):
    z, x, y = 1.0, 960.0, 540.0
    for k, (fx, fy) in enumerate(FOCUS):
        s = STARTS[k]
        w = ss(s + 3.5, s + 5.0, t) * (1 - ss(s + 8.5, s + 10.0, t))
        z += 0.3 * w; x += (fx - 960) * w; y += (fy - 540) * w
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
            c.save(); frame(c, t); c.restore(); surf.write_to_png(f'ep08_{t}.png')
    else:
        t0, t1 = (float(args[1]), float(args[2])) if args and args[0] == 'range' else (0, DUR)
        out = sys.stdout.buffer
        for i in range(int(round(t0 * FPS)), int(round(t1 * FPS))):
            c.save(); frame(c, i / FPS); c.restore(); surf.flush(); out.write(surf.get_data())
