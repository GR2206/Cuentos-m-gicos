"""Episodio 4 — La lluvia mágica (aventurita, 110 s).
Los amigos juegan a la pelota, se nubla y empieza a llover. Tito abre sus orejas como un paraguas
y todos se refugian abajo. Cuando para, sale un arcoíris y saltan en los charcos.

Uso:  python3 ep04_lluvia_magica.py                -> cuadros crudos por stdout
      python3 ep04_lluvia_magica.py range 0 55     -> solo un tramo
      python3 ep04_lluvia_magica.py stills 12 65   -> PNG sueltos"""
import cairo, math, random, sys
import amigos as A, cuerpos as K
from amigos import hexc, ellipse, fill, OUT
from logos import word, sparkle, font
from ep02_puente_del_rio import kf, ss, moving, K_back, music_note, palm
from ep03_donde_esta_tomi import bubble

W, H, FPS = 1920, 1080, 30
DUR = 110.0
GROUND = 880
TITO_SHELTER = 960

def mix(a, b, k): return tuple(x + (y - x) * k for x, y in zip(a, b))

# ---------------- escenario (versión soleada y versión lluviosa) ----------------
def make_layers(rainy):
    sky = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(sky)
    g = cairo.LinearGradient(0, 0, 0, H)
    cols = ('#78909C', '#B0BEC5', '#CFD8DC') if rainy else ('#29B6F6', '#81D4FA', '#B3E5FC')
    for k, col in enumerate(cols): g.add_color_stop_rgb(k / 2, *hexc(col)[:3])
    c.set_source(g); c.paint()
    land = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(land)
    hl = ['#4E8F55', '#3B7F3F', '#7FA84A'] if rainy else ['#66BB6A', '#43A047', '#8BC34A']
    c.move_to(0, 640); c.curve_to(350, 520, 700, 540, 980, 650); c.curve_to(1250, 560, 1600, 520, 1920, 620)
    c.line_to(1920, H); c.line_to(0, H); c.close_path(); c.set_source_rgba(*hexc(hl[0])); c.fill()
    c.move_to(0, 750); c.curve_to(450, 690, 900, 710, 1920, 740); c.line_to(1920, H); c.line_to(0, H); c.close_path()
    c.set_source_rgba(*hexc(hl[1])); c.fill()
    c.rectangle(0, 805, W, H - 805); c.set_source_rgba(*hexc(hl[2])); c.fill()
    c.move_to(0, 810); c.curve_to(600, 785, 1300, 785, 1920, 810); c.line_to(1920, 830); c.line_to(0, 830); c.close_path(); c.fill()
    palm(c, 40, GROUND, 540, 1); palm(c, 1880, GROUND, 500, -1)
    for (bx, by, sc) in ((300, 805, 0.45), (1620, 805, 0.5)):
        c.save(); c.translate(bx, by); c.scale(sc, sc)
        for (cx, cy, r) in ((-110, 0, 90), (0, -50, 120), (110, 0, 95), (0, 30, 100)): ellipse(c, cx, cy, r, r)
        c.set_source_rgba(*hexc('#2E6B32' if rainy else '#2E7D32')); c.fill(); c.restore()
    for k, (fx, col) in enumerate(((200, '#FF4081'), (430, '#FF9100'), (1500, '#E040FB'), (1760, '#FFEA00'))):
        c.set_line_width(7); c.set_source_rgba(*hexc('#2E7D32')); c.move_to(fx, 970); c.line_to(fx, 925); c.stroke()
        for i in range(6):
            a = i * math.pi / 3; ellipse(c, fx + 20 * math.cos(a), 920 + 20 * math.sin(a), 15, 15)
            c.set_source_rgba(*hexc(col)); c.fill()
        ellipse(c, fx, 920, 12, 12); c.set_source_rgba(*hexc('#FFEB3B')); c.fill()
    return sky, land

SKY_SUN, LAND_SUN = make_layers(False)
SKY_RAIN, LAND_RAIN = make_layers(True)

def gloom(t):   # 0 = sol, 1 = nublado
    return ss(14, 20, t) * (1 - ss(59, 65, t))
def rain(t):    # intensidad de la lluvia
    return ss(21, 24, t) * (1 - ss(57, 61, t))

def sun(c, t):
    x, y = 1650, 170
    for i in range(12):
        c.save(); c.translate(x, y); c.rotate(i * math.pi / 6 + t * 0.2)
        c.move_to(-20, -115); c.line_to(0, -165 - 8 * math.sin(t * 3 + i)); c.line_to(20, -115); c.close_path()
        c.set_source_rgba(*hexc('#FFB300')); c.fill(); c.restore()
    ellipse(c, x, y, 95, 95); fill(c, hexc('#FFEB3B'), hexc('#F9A825'), 7)
    c.set_source_rgba(*OUT); c.set_line_width(7); c.set_line_cap(cairo.LINE_CAP_ROUND)
    for ex in (-32, 32): c.arc(x + ex, y - 12, 15, math.pi * 1.1, math.pi * 1.9); c.stroke()
    c.arc(x, y + 12, 34, 0.15 * math.pi, 0.85 * math.pi); c.stroke()

RAIN_CLOUDS = [(-700, 260, 180, 1.5), (2600, 1450, 120, 1.7), (-900, 760, 90, 1.4), (2800, 1750, 230, 1.3), (-600, 160, 60, 1.2)]
def rain_clouds(c, t):
    k_in, k_out = ss(13.5, 20, t), ss(59, 66, t)
    for i, (x_off, x_on, y, s) in enumerate(RAIN_CLOUDS):
        x = x_off + (x_on - x_off) * k_in
        x = x + (x_off * 1.2 - x_on) * k_out if k_out > 0 else x
        if k_in <= 0: continue
        x += 15 * math.sin(t * 0.5 + i)
        c.save(); c.translate(x, y); c.scale(s, s)
        blobs = ((0, 0, 70), (80, -40, 85), (170, 0, 70), (85, 25, 70))
        for (cx, cy, r) in blobs: ellipse(c, cx, cy, r, r)
        c.set_source_rgba(*hexc('#546E7A')); c.set_line_width(10); c.stroke()
        for (cx, cy, r) in blobs: ellipse(c, cx, cy, r, r)
        c.set_source_rgba(*hexc('#90A4AE')); c.fill()
        c.set_source_rgba(*OUT); c.set_line_width(6); c.set_line_cap(cairo.LINE_CAP_ROUND)
        for ex in (55, 115): c.arc(ex, 5, 12, 0.15 * math.pi, 0.85 * math.pi); c.stroke()
        c.arc(85, 30, 14, 0.2 * math.pi, 0.8 * math.pi); c.stroke()
        c.restore()

def white_clouds(c, t):
    a = 1 - gloom(t)
    if a <= 0: return
    c.push_group()
    for (x0, y0, s, sp) in ((150, 160, 0.9, 12), (820, 100, 0.7, 8), (1250, 240, 0.6, 15)):
        c.save(); c.translate((x0 + sp * t) % 2300 - 250, y0); c.scale(s, s)
        for (cx, cy, r) in ((0, 0, 60), (70, -30, 75), (150, 0, 60), (75, 20, 60)): ellipse(c, cx, cy, r, r)
        c.set_source_rgba(1, 1, 1, 1); c.fill(); c.restore()
    c.pop_group_to_source(); c.paint_with_alpha(a)

def rainbow(c, t):
    p = ss(66, 69.5, t)
    if p <= 0: return
    cols = ['#F44336', '#FF9800', '#FFEB3B', '#4CAF50', '#2196F3', '#3F51B5', '#9C27B0']
    cx, cy = 960, 980
    c.save(); c.set_line_cap(cairo.LINE_CAP_BUTT)
    for k, col in enumerate(cols):
        r = 860 - k * 34
        c.set_source_rgba(*hexc(col, 0.85)); c.set_line_width(36)
        c.arc(cx, cy, r, math.pi, math.pi + math.pi * p); c.stroke()
    c.restore()
    if p < 1:
        a = math.pi + math.pi * p
        sparkle(c, cx + 760 * math.cos(a), cy + 760 * math.sin(a), 40, '#FFFFFF')

PUDDLES = [(560, 160), (1000, 190), (1330, 130), (1560, 120)]
def puddles(c, t):
    grow = ss(25, 50, t)
    if grow <= 0: return
    for i, (x, w) in enumerate(PUDDLES):
        rx, ry = w * grow, 26 * grow
        ellipse(c, x, 905, rx, ry); fill(c, hexc('#64B5F6'), hexc('#1E88E5'), 5)
        ellipse(c, x - rx * 0.3, 900, rx * 0.35, ry * 0.3); c.set_source_rgba(1, 1, 1, 0.5); c.fill()
        r = rain(t)
        if r > 0.1:
            for k in range(3):
                ph = (t * 1.3 + k / 3 + i * 0.37) % 1
                ellipse(c, x + (k - 1) * rx * 0.5, 905, 30 * ph + 4, 8 * ph + 1)
                c.set_source_rgba(1, 1, 1, (1 - ph) * r); c.set_line_width(3); c.stroke()

DROPS = [(random.Random(i).uniform(-200, 2100), random.Random(i * 7 + 1).random(), random.Random(i * 13 + 2).uniform(0.9, 1.3)) for i in range(260)]
def ear_top(x, t):
    """Si Tito tiene las orejas abiertas, devuelve la altura donde chocan las gotas (o None)."""
    u = umbrella(t)
    if u < 0.3: return None
    dx = abs(x - TITO_SHELTER)
    if dx > 440 * u: return None
    return 470 + 140 * (dx / (440 * u)) ** 2

def rain_drops(c, t):
    r = rain(t)
    if r <= 0: return
    n = int(len(DROPS) * r)
    c.set_line_cap(cairo.LINE_CAP_ROUND); c.set_line_width(5)
    for (x0, ph, sp) in DROPS[:n]:
        u = (ph + t * 1.1 * sp) % 1.0
        y = -60 + u * (GROUND + 120)
        x = x0 - 0.18 * y
        top = ear_top(x, t)
        if top is not None and y > top:
            if y - top < 40:
                ellipse(c, x, top, 9, 4); c.set_source_rgba(1, 1, 1, 0.8); c.fill()
            continue
        c.move_to(x, y); c.line_to(x + 7, y - 34)
        c.set_source_rgba(*hexc('#E3F2FD', 0.85)); c.stroke()

def splash(c, t, t0, x, y, big=1.0):
    p = (t - t0) / 0.8
    if not 0 <= p <= 1: return
    for k in range(8):
        a = math.pi * (0.1 + 0.8 * k / 7)
        r = 130 * big * p
        dx, dy = r * math.cos(a), -r * math.sin(a) * 1.5 + 220 * big * p * p
        ellipse(c, x + dx, y + dy, 12 * big * (1 - p) + 3, 14 * big * (1 - p) + 3)
        c.set_source_rgba(*hexc('#90CAF9', 1 - p)); c.fill()

def ball(c, x, y, rot):
    c.save(); c.translate(x, y); c.rotate(rot)
    cols = ['#F44336', '#FFFFFF', '#2196F3', '#FFFFFF', '#FFEB3B', '#FFFFFF']
    for k, col in enumerate(cols):
        c.move_to(0, 0); c.arc(0, 0, 42, k * math.pi / 3, (k + 1) * math.pi / 3); c.close_path()
        c.set_source_rgba(*hexc(col)); c.fill()
    ellipse(c, 0, 0, 42, 42); c.set_source_rgba(*OUT); c.set_line_width(5); c.stroke()
    ellipse(c, 0, 0, 9, 9); fill(c, hexc('#FFFFFF'), OUT, 3)
    c.restore()

# ---------------- historia ----------------
COCO_X = [(0, 760), (22.5, 760), (24, 600), (25.5, 860), (27, 640), (31, 640), (33, 700),
          (64.5, 700), (66, 640), (72.5, 640), (73.4, 560), (79.5, 560), (81, 760), (95, 760)]
TITO_X = [(0, 1160), (22, 1160), (26, TITO_SHELTER), (82, TITO_SHELTER), (84.5, 1000), (95, 1000)]
PIPA_X = [(0, 470), (22, 470), (25, 520), (31, 520), (34, 1300), (64.5, 1300), (66, 1330), (86, 1330), (87.4, 1330)]
TOMI_X = [(0, 1420), (24, 1420), (36.5, 1120), (64.5, 1120), (66.5, 1200), (88, 1200), (92.5, 1560), (110, 1560)]
BALL = [(5.0, 'coco'), (7.0, 'tito'), (9.0, 'coco'), (11.0, 'tito')]

def umbrella(t): return ss(28, 30, t) * (1 - ss(63, 64.8, t))

def hop(t, t0, h=120, d=0.9):
    p = (t - t0) / d
    return h * math.sin(math.pi * p) if 0 <= p <= 1 else 0.0

COCO_JUMPS = [73.4, 75.2, 77.0, 96.0, 97.8, 99.6]
PIPA_JUMPS = [87.4, 89.0]
TITO_STOMP = 84.6
TOMI_SPLASH = 92.6

def frame(c, t):
    cx, cy, z = camera(t)
    c.save(); c.translate(W / 2, H / 2); c.scale(z, z); c.translate(-cx, -cy)
    world(c, t)
    c.restore()
    overlay(c, t)

CAM = [(0, 1.1, 960, 600), (13, 1.1, 960, 600), (15, 1.0, 960, 540), (26, 1.0, 960, 540), (28.5, 1.3, 980, 640),
       (57, 1.3, 980, 640), (60, 1.0, 960, 540), (71.5, 1.0, 960, 540), (73, 1.25, 700, 640), (80, 1.25, 700, 640),
       (82, 1.1, 1100, 600), (93, 1.1, 1100, 600), (95, 1.0, 960, 540)]
def camera(t):
    z = kf(t, [(a, b) for a, b, _, _ in CAM]); x = kf(t, [(a, d) for a, _, d, _ in CAM]); y = kf(t, [(a, e) for a, _, _, e in CAM])
    x = max(W / (2 * z), min(W - W / (2 * z), x)); y = max(H / (2 * z), min(H - H / (2 * z), y))
    return x, y, z

def dance(t): return 98 < t < 106

def world(c, t):
    g = gloom(t)
    c.set_source_surface(SKY_SUN, 0, 0); c.paint()
    if g > 0: c.set_source_surface(SKY_RAIN, 0, 0); c.paint_with_alpha(g)
    rainbow(c, t)
    sun(c, t)
    white_clouds(c, t)
    rain_clouds(c, t)
    c.set_source_surface(LAND_SUN, 0, 0); c.paint()
    if g > 0: c.set_source_surface(LAND_RAIN, 0, 0); c.paint_with_alpha(g)
    puddles(c, t)
    bounce = lambda ph: -25 * abs(math.sin(t * 4.5 + ph)) if (1 < t < 5 or dance(t)) else 0.0
    look_up = 14 < t < 21 or 66 < t < 72
    # Pipa
    px = kf(t, PIPA_X)
    neck = kf(t, [(35.5, 300), (37.5, 110), (64.5, 110), (65.8, 300)])
    pj = sum(hop(t, j, 110, 0.9) for j in PIPA_JUMPS)
    plook = (0, -1) if look_up else ((1, 0.2) if 4 < t < 13 else (-0.3, 0))
    if 33.5 < t < 37.5: plook = (0, -1)
    K.put(c, K.pipa, px, GROUND + bounce(0.5) - pj, 0.55, t=t, neck=neck, look=plook, walk=t * 7 if moving(t, PIPA_X) else 0)
    # Tito
    tx = kf(t, TITO_X)
    u = umbrella(t)
    tj = hop(t, TITO_STOMP - 0.6, 50, 0.6)
    tlook = (0, -1) if look_up else ((-1, 0) if 4 < t < 13 else (0, 0.3))
    K.put(c, K.tito, tx, GROUND + bounce(1.0) - tj, 0.6, t=t, look=tlook, umbrella=u, walk=t * 6 if moving(t, TITO_X) else 0)
    # Tomi
    tmx = kf(t, TOMI_X)
    tmj = hop(t, TOMI_SPLASH - 0.5, 40, 0.5)
    tmlook = (0, -1) if look_up else (-1, 0) if 4 < t < 13 else (0, 0)
    K.put(c, K.tomi, tmx, GROUND + bounce(1.5) - tmj, 0.55, t=t, look=tmlook, walk=t * 3 if moving(t, TOMI_X) else 0)
    # Coco
    x = kf(t, COCO_X)
    cj = sum(hop(t, j, 130, 0.9) for j in COCO_JUMPS)
    mood, look = 'smile', (1, -0.2) if 4 < t < 13 else (0, 0)
    arm_r, arm_l = math.radians(65 + 6 * math.sin(t * 2)), math.radians(115 - 6 * math.sin(t * 2))
    if 1 < t < 5 or dance(t):
        arm_r, arm_l = math.radians(-58 + 25 * math.sin(t * 9)), math.radians(-122 - 25 * math.sin(t * 9))
    for (bt, who) in BALL:
        if who == 'coco' and bt - 0.4 < t < bt + 0.3: arm_r = math.radians(-60); arm_l = math.radians(-120)
    if look_up: look = (0, -1)
    if 20.3 < t < 22.5: mood = 'o'; look = (0, -1)
    if 22.5 < t < 28: mood = 'o'; arm_r, arm_l = math.radians(-100), math.radians(-80); look = (math.sin(t * 3), -0.5)
    if 66.5 < t < 70: mood = 'o'
    if 79.5 < t < 87.5: look = (1, 0)
    if 85.2 < t < 87.5: mood = 'closed'; look = (0, 0)
    blink = 0.0
    for bt in (3.0, 16.0, 33.0, 45.0, 55.0, 75.0, 90.0, 102.0):
        if abs(t - bt) < 0.12: blink = 1 - abs(t - bt) / 0.12
    K.put(c, K.coco, x, GROUND + bounce(0) - cj, 0.55, t=t, mood=mood, look=look, lid=blink, arm_r=arm_r, arm_l=arm_l,
          walk=t * 9 if moving(t, COCO_X) else 0)
    # Lola
    if t < 31.5:
        lx = kf(t, [(0, 960), (24, 960), (26, 700), (28, 1200), (30, 900), (31.5, TITO_SHELTER)])
        ly = 430 + 20 * math.sin(t * 3) - (20 * abs(math.sin(t * 4.5)) if 1 < t < 5 else 0)
        if 4 < t < 13: lx = 960 + 120 * math.sin(t * 0.9)
        K.put(c, K.lola, lx, ly, 0.5, t=t, flap=20, look=(0, -1) if look_up else (0.5, 0.5))
    elif t < 64.8:
        perch = GROUND - 0.6 * 470 + 6
        K.put(c, K.lola, TITO_SHELTER, perch, 0.5, t=t, flap=None, look=(0, -0.6) if t > 58 else (0.4, 0.6))
        if 40 < t < 56:
            for k in range(3):
                ph = (t * 0.6 + k / 3) % 1
                music_note(c, TITO_SHELTER + 40 + 60 * ph + 20 * math.sin(ph * 8), perch - 140 - 140 * ph, math.sin(math.pi * ph), ['#E91E63', '#1E88E5', '#FF9800'][k])
    else:
        if 78 < t < 86:  # flies along the rainbow
            p = (t - 78) / 8; a = math.pi + math.pi * p
            lx, ly = 960 + 760 * math.cos(a), 980 + 760 * math.sin(a)
            for k in range(4):
                q = p - k * 0.03
                if q > 0:
                    aa = math.pi + math.pi * q
                    sparkle(c, 960 + 760 * math.cos(aa), 980 + 760 * math.sin(aa) + 30, 18 - 3 * k)
        else:
            lx = kf(t, [(64.8, TITO_SHELTER), (67, 1150), (78, 1150), (86, 1760), (88, 1300)])
            ly = kf(t, [(64.8, GROUND - 0.6 * 470), (67, 450), (78, 450), (86, 300), (88, 430)]) + 15 * math.sin(t * 3)
        if dance(t): ly -= 25 * abs(math.sin(t * 4.5))
        K.put(c, K.lola, lx, ly, 0.5, t=t, flap=22, look=(0, -1) if 66 < t < 72 else (0.5, 0.5))
        if dance(t):
            for k in range(3):
                ph = (t * 0.7 + k / 3) % 1
                music_note(c, lx + 40 + 60 * ph, ly - 150 - 160 * ph, math.sin(math.pi * ph), ['#E91E63', '#1E88E5', '#FF9800'][k])
    # ball game
    for (bt, who) in BALL:
        p = (t - bt) / 2.0
        if 0 <= p < 1:
            x0, x1 = (kf(bt, COCO_X) + 40, kf(bt, TITO_X) - 40) if who == 'coco' else (kf(bt, TITO_X) - 40, kf(bt, COCO_X) + 40)
            bx = x0 + (x1 - x0) * p; by = GROUND - 200 - 200 * math.sin(math.pi * p)
            ball(c, bx, by, t * (5 if who == 'coco' else -5))
    if 13 <= t < 15:
        ball(c, kf(13, COCO_X) + 50, GROUND - 40 - 200 * max(0, math.sin(math.pi * (t - 13) / 1.2)) * (1 - (t - 13) / 2), t * 3)
    elif 15 <= t < 22:
        ball(c, kf(13, COCO_X) + 50 + 60 * min(1, (t - 15) / 3), GROUND - 40, 0)
    rain_drops(c, t)
    # splashes
    for j in COCO_JUMPS[:3]: splash(c, t, j + 0.9, 560, 900, 1.0)
    for j in PIPA_JUMPS: splash(c, t, j + 0.9, 1330, 900, 0.9)
    splash(c, t, TITO_STOMP, 1000, 900, 2.0)
    splash(c, t, TOMI_SPLASH, 1560, 900, 0.6)
    # the first drop on Coco's nose
    if 19.6 < t < 20.5:
        p = (t - 19.6) / 0.7
        ellipse(c, kf(t, COCO_X), GROUND - 260 - 400 * (1 - min(1, p)), 9, 13); c.set_source_rgba(*hexc('#90CAF9')); c.fill()
    # speech bubbles
    cx_ = kf(t, COCO_X)
    bubble(c, cx_, GROUND - 300, '¡Llueve!', (t - 20.6) / 2.4)
    bubble(c, TITO_SHELTER + 40, GROUND - 0.6 * 470 - 40 if t < 29 else GROUND - 470, '¡Vengan!', (t - 28.6) / 2.6)
    bubble(c, cx_, GROUND - 300, '¡Un arcoíris!', (t - 67.0) / 3.0)
    if 85 < t < 88:
        bubble(c, cx_, GROUND - 300, '¡Jajaja!', (t - 85.2) / 2.6)

def overlay(c, t):
    if t < 5.5:
        a = 1 - ss(4.6, 5.4, t)
        c.push_group(); word(c, 'La lluvia mágica', W / 2, 230, 125 * K_back((t - 0.6) / 0.6) + 0.01, tilt=0.05, outline=9)
        c.pop_group_to_source(); c.paint_with_alpha(a)
    if t > 99:
        s = K_back((t - 99) / 0.7)
        word(c, '¡Después de la lluvia', W / 2, 170, 100 * s + 0.01, tilt=0.06, outline=9)
        word(c, 'sale el sol!', W / 2, 300, 120 * s + 0.01, start=3, tilt=0.06, outline=10)
    a = max(1 - ss(0, 0.8, t), ss(DUR - 2.0, DUR, t))
    if a > 0: c.set_source_rgba(1, 1, 1, a); c.paint()

if __name__ == '__main__':
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(surf)
    args = sys.argv[1:]
    if args and args[0] == 'stills':
        for t in map(float, args[1:]):
            c.save(); frame(c, t); c.restore(); surf.write_to_png(f'ep04_{t}.png')
    else:
        t0, t1 = (float(args[1]), float(args[2])) if args and args[0] == 'range' else (0, DUR)
        out = sys.stdout.buffer
        for i in range(int(round(t0 * FPS)), int(round(t1 * FPS))):
            c.save(); frame(c, i / FPS); c.restore(); surf.flush(); out.write(surf.get_data())
