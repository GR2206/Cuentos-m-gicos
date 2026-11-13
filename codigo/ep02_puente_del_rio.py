"""Episodio 2 — El puente del río (aventurita, ~2 min).
Coco quiere bananas del otro lado del río, el puente está roto, Lola llama a los amigos
y Tito hace un puente con la trompa. Al final comparten las bananas.

Uso:  python3 ep02_puente_del_rio.py                 -> cuadros crudos de todo el episodio por stdout
      python3 ep02_puente_del_rio.py range 0 30      -> solo de 0 a 30 s
      python3 ep02_puente_del_rio.py stills 12 65    -> PNG sueltos para revisar"""
import cairo, math, random, sys
import amigos as A, cuerpos as K
from amigos import hexc, ellipse, fill, OUT
from logos import word, sparkle, leaf

W, H, FPS = 1920, 1080, 30
DUR = 126.0
GROUND = 880
RIV_L, RIV_R = 760, 1180
TRUNK_Y = GROUND - 50          # altura de la trompa de Tito como puente
TITO_X = 640
TREE_X = 1590

def ss(e0, e1, x):
    t = max(0.0, min(1.0, (x - e0) / (e1 - e0))); return t * t * (3 - 2 * t)

def kf(t, keys):
    """Interpolación suave entre keyframes [(t, valor), ...]."""
    if t <= keys[0][0]: return keys[0][1]
    for (t0, v0), (t1, v1) in zip(keys, keys[1:]):
        if t <= t1:
            return v0 + (v1 - v0) * ss(t0, t1, t)
    return keys[-1][1]

def moving(t, keys):
    for (t0, v0), (t1, v1) in zip(keys, keys[1:]):
        if t0 < t < t1 and v0 != v1: return True
    return False

# ---------------- escenario ----------------
def make_bg():
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(s)
    g = cairo.LinearGradient(0, 0, 0, H)
    g.add_color_stop_rgb(0, *hexc('#29B6F6')[:3]); g.add_color_stop_rgb(0.55, *hexc('#81D4FA')[:3]); g.add_color_stop_rgb(1, *hexc('#B3E5FC')[:3])
    c.set_source(g); c.paint()
    # sun
    for i in range(12):
        c.save(); c.translate(1700, 150); c.rotate(i * math.pi / 6 + 0.1)
        c.move_to(-20, -115); c.line_to(0, -165); c.line_to(20, -115); c.close_path()
        c.set_source_rgba(*hexc('#FFB300')); c.fill(); c.restore()
    ellipse(c, 1700, 150, 95, 95); fill(c, hexc('#FFEB3B'), hexc('#F9A825'), 7)
    # hills
    c.move_to(0, 640); c.curve_to(300, 500, 650, 520, 940, 640)
    c.curve_to(1200, 540, 1550, 500, 1920, 610); c.line_to(1920, H); c.line_to(0, H); c.close_path()
    c.set_source_rgba(*hexc('#66BB6A')); c.fill()
    c.move_to(0, 740); c.curve_to(400, 670, 800, 700, 1920, 720); c.line_to(1920, H); c.line_to(0, H); c.close_path()
    c.set_source_rgba(*hexc('#43A047')); c.fill()
    # ground (both banks)
    c.rectangle(0, 800, W, H - 800); c.set_source_rgba(*hexc('#8BC34A')); c.fill()
    c.move_to(0, 805); c.curve_to(600, 780, 1300, 780, 1920, 805); c.line_to(1920, 830); c.line_to(0, 830); c.close_path()
    c.set_source_rgba(*hexc('#8BC34A')); c.fill()
    # river
    river(c)
    # palms at the edges
    palm(c, 30, GROUND, 520, 1)
    # bushes & flowers in the back
    for (bx, by, sc, col) in ((330, 805, 0.45, '#2E7D32'), (1380, 805, 0.5, '#388E3C')):
        c.save(); c.translate(bx, by); c.scale(sc, sc)
        for (cx, cy, r) in ((-110, 0, 90), (0, -50, 120), (110, 0, 95), (0, 30, 100)): ellipse(c, cx, cy, r, r)
        c.set_source_rgba(*hexc(col)); c.fill(); c.restore()
    return s

def river(c):
    c.move_to(905, 700); c.line_to(1005, 700)
    c.curve_to(1060, 780, 1150, 840, RIV_R, 880); c.line_to(1250, H); c.line_to(690, H); c.line_to(RIV_L, 880)
    c.curve_to(800, 830, 870, 770, 905, 700); c.close_path()
    g = cairo.LinearGradient(0, 700, 0, H)
    g.add_color_stop_rgb(0, *hexc('#4FC3F7')[:3]); g.add_color_stop_rgb(1, *hexc('#0288D1')[:3])
    c.set_source(g); c.fill_preserve()
    c.set_source_rgba(*hexc('#6D4C41')); c.set_line_width(10); c.stroke()

def palm(c, x, y, h, flip, t=0.0):
    sway = math.sin(t * 2 * math.pi / 3.2)
    tipx, tipy = x + flip * (60 + 10 * sway), y - h
    c.set_line_cap(cairo.LINE_CAP_ROUND)
    c.move_to(x, y); c.curve_to(x + flip * 10, y - h * 0.4, x + flip * 50, y - h * 0.8, tipx, tipy)
    c.set_line_width(46); c.set_source_rgba(*hexc('#8D5524')); c.stroke()
    for i, ang in enumerate((-160, -125, -90, -55, -20, -195, 15)):
        a = math.radians(ang + 5 * sway)
        c.save(); c.translate(tipx, tipy); c.rotate(a)
        c.move_to(0, 0); c.curve_to(80, -45, 170, -30, 240, 30); c.curve_to(160, 10, 80, 20, 0, 0); c.close_path()
        c.set_source_rgba(*hexc('#2E7D32' if i % 2 else '#43A047')); c.fill(); c.restore()

BG = make_bg()

def water(c, t):
    random.seed(4)
    for k in range(26):
        u = (random.random() + t * 0.18) % 1.0
        y = 700 + u * 380
        half = 50 + u * 230
        x = 955 + (random.random() - 0.5) * 2 * half * 0.8
        w = 20 + 40 * u
        c.set_source_rgba(1, 1, 1, 0.55 * math.sin(math.pi * u)); c.set_line_width(4 + 3 * u)
        c.set_line_cap(cairo.LINE_CAP_ROUND)
        c.move_to(x - w, y); c.curve_to(x - w / 2, y - 8, x + w / 2, y + 8, x + w, y); c.stroke()

def plank(c, x, y, rot=0.0):
    c.save(); c.translate(x, y); c.rotate(rot)
    c.rectangle(-15, -14, 30, 28); fill(c, hexc('#A1887F'), OUT, 4)
    c.move_to(-8, -6); c.line_to(6, -6); c.set_source_rgba(*hexc('#6D4C41')); c.set_line_width(3); c.stroke()
    c.restore()

def bridge(c, t):
    for (px, dir_) in ((RIV_L - 10, 1), (RIV_R + 10, -1)):
        c.rectangle(px - 9, GROUND - 90, 18, 100); fill(c, hexc('#795548'), OUT, 4)
        ellipse(c, px, GROUND - 92, 12, 8); fill(c, hexc('#8D6E63'), OUT, 4)
    # planks on both sides; gap in the middle
    fall_t = 17.6
    xs = [RIV_L + 15 + 32 * i for i in range(14)]
    for i, x in enumerate(xs):
        if 905 < x < 1030: continue
        if i == 9:  # the plank that falls
            p = (t - fall_t) / 0.7
            if p > 1: continue
            if p > 0:
                plank(c, x + 30 * p, GROUND + 160 * p * p, 2.5 * p); continue
            wob = math.sin(t * 25) * 0.15 if t > fall_t - 0.8 else 0
            plank(c, x, GROUND, wob); continue
        sag = 10 * math.sin(math.pi * (x - RIV_L) / (RIV_R - RIV_L))
        plank(c, x, GROUND + sag)
    # ropes, broken in the middle
    c.set_source_rgba(*hexc('#5D4037')); c.set_line_width(6); c.set_line_cap(cairo.LINE_CAP_ROUND)
    c.move_to(RIV_L - 10, GROUND - 85); c.curve_to(820, GROUND - 60, 880, GROUND - 40, 900, GROUND + 10); c.stroke()
    c.move_to(RIV_R + 10, GROUND - 85); c.curve_to(1120, GROUND - 60, 1060, GROUND - 40, 1040, GROUND + 15); c.stroke()

def splash(c, t, t0, x, y):
    p = (t - t0) / 0.9
    if not 0 <= p <= 1: return
    for k in range(6):
        a = math.pi * (0.15 + 0.7 * k / 5)
        r = 90 * p
        dx, dy = r * math.cos(a), -r * math.sin(a) * 1.4 + 160 * p * p
        ellipse(c, x + (dx if k % 2 else -dx), y + dy, 10 * (1 - p) + 2, 12 * (1 - p) + 2)
        c.set_source_rgba(1, 1, 1, 1 - p); c.fill()
    ellipse(c, x, y + 10, 70 * p, 16 * p); c.set_source_rgba(1, 1, 1, 0.8 * (1 - p)); c.set_line_width(5); c.stroke()

def banana_tree(c, t, has_bunch):
    x, y = TREE_X, GROUND
    c.set_line_cap(cairo.LINE_CAP_ROUND)
    c.move_to(x, y); c.curve_to(x - 10, y - 150, x + 10, y - 260, x, y - 360)
    c.set_source_rgba(*OUT); c.set_line_width(62); c.stroke()
    c.move_to(x, y); c.curve_to(x - 10, y - 150, x + 10, y - 260, x, y - 360)
    c.set_source_rgba(*hexc('#9CCC65')); c.set_line_width(50); c.stroke()
    sway = math.sin(t * 1.6)
    for i, ang in enumerate((-150, -110, -70, -30, 190)):
        c.save(); c.translate(x, y - 360); c.rotate(math.radians(ang + 4 * sway))
        c.move_to(0, 0); c.curve_to(60, -70, 210, -70, 280, 0); c.curve_to(210, 40, 60, 40, 0, 0); c.close_path()
        c.set_source_rgba(*hexc('#43A047' if i % 2 else '#66BB6A')); c.fill_preserve()
        c.set_source_rgba(*hexc('#2E7D32')); c.set_line_width(4); c.stroke()
        c.move_to(10, 0); c.line_to(270, 0); c.stroke(); c.restore()
    if has_bunch:
        c.set_source_rgba(*hexc('#558B2F')); c.set_line_width(8)
        c.move_to(x - 20, y - 330); c.line_to(x - 70, y - 250); c.stroke()
        K.bunch(c, x - 70, y - 250, 1.3)
        if 9 < t < 16:
            for k in range(3):
                ph = (t * 1.2 + k / 3) % 1
                sparkle(c, x - 60 + 70 * math.cos(k * 2.1 + t), y - 230 + 50 * math.sin(k * 2.1 + t), 20 * math.sin(math.pi * ph))

def thought(c, x, y, p):
    if p <= 0: return
    s = K.ss if False else None
    for k, (dx, dy, r) in enumerate(((0, 0, 10), (25, -35, 16))):
        if p > k * 0.2:
            ellipse(c, x + dx, y + dy, r, r); fill(c, (1, 1, 1, 1), OUT, 4)
    if p > 0.4:
        q = min(1, (p - 0.4) / 0.3)
        c.save(); c.translate(x + 110, y - 120); c.scale(q, q)
        for (cx, cy, r) in ((-60, 0, 55), (0, -25, 65), (60, 0, 55), (0, 25, 55)):
            ellipse(c, cx, cy, r, r)
        c.set_source_rgba(*OUT); c.set_line_width(10); c.stroke_preserve(); c.set_source_rgba(1, 1, 1, 1); c.fill()
        for (cx, cy, r) in ((-60, 0, 55), (0, -25, 65), (60, 0, 55), (0, 25, 55)):
            ellipse(c, cx, cy, r, r)
        c.fill()
        K.bunch(c, 0, -45, 0.95)
        c.restore()

def bulb(c, x, y, p, t):
    if p <= 0: return
    c.save(); c.translate(x, y); c.scale(K_back(p), K_back(p))
    for i in range(8):
        a = i * math.pi / 4 + t
        c.move_to(55 * math.cos(a), 55 * math.sin(a) - 10); c.line_to(80 * math.cos(a), 80 * math.sin(a) - 10)
        c.set_source_rgba(*hexc('#FFD600')); c.set_line_width(8); c.set_line_cap(cairo.LINE_CAP_ROUND); c.stroke()
    ellipse(c, 0, -10, 38, 40); fill(c, hexc('#FFF176'), OUT, 5)
    c.rectangle(-18, 25, 36, 22); fill(c, hexc('#B0BEC5'), OUT, 4)
    c.restore()

def K_back(p):
    p = max(0.0, min(1.0, p)); k = 1.70158
    return 1 + (k + 1) * (p - 1) ** 3 + k * (p - 1) ** 2

def music_note(c, x, y, a, col):
    c.set_source_rgba(*hexc(col, a)); ellipse(c, x, y, 16, 12); c.fill()
    c.set_line_width(5); c.move_to(x + 14, y); c.line_to(x + 14, y - 50); c.line_to(x + 34, y - 38); c.stroke()

# ---------------- historia ----------------
# Coco: posición x
COCO_X = [(3.0, -200), (10.0, 450), (16.0, 450), (18.0, 700), (19.2, 700), (20.0, 620),
          (41.0, 620), (43.0, 420), (68.0, 420), (71.0, 690), (72.0, 700), (84.0, 1230),
          (85.0, 1260), (87.0, 1470), (92.0, 1470), (95.0, 1230), (100.5, 700), (102.5, 470)]
TITO_KF = [(43.0, -300), (50.0, TITO_X)]
PIPA_KF = [(44.0, -300), (51.0, 150)]
TOMI_KF = [(44.0, -250), (58.0, 300)]
TOSS = [(104.0, 'tito'), (105.5, 'pipa'), (107.0, 'lola'), (108.5, 'tomi')]

def coco_state(t):
    x = kf(t, COCO_X)
    y = GROUND
    mood, sad, look, lid = 'smile', 0.0, (0.0, 0.0), 0.0
    arm_r, arm_l, tilt, hold, chew = math.radians(65 + 6 * math.sin(t * 2)), math.radians(115 - 6 * math.sin(t * 2)), 0.0, None, 0.0
    walk = t * 9 if moving(t, COCO_X) else 0.0
    if 3 < t < 10:  # hops in
        y -= 70 * abs(math.sin(math.pi * (t - 3) / 1.4))
        arm_r, arm_l = math.radians(20 + 30 * math.sin(t * 5)), math.radians(160 - 30 * math.sin(t * 5))
    if 10 < t < 16:
        look = (1, -0.4)
        arm_l = math.radians(kf(t, [(10, 115), (10.6, 70)]))  # rubs tummy
        arm_l += 0.15 * math.sin(t * 8) * ss(10.5, 11, t) * (1 - ss(13, 13.5, t))
        if 13.5 < t < 16:
            arm_r = math.radians(-20 + 10 * math.sin(t * 6)); arm_l = math.radians(115)  # points
            y -= 30 * abs(math.sin(t * 6)) * ss(14, 14.3, t)
    if 16 <= t < 18: look = (1, 0.3)
    if 17.5 < t < 22:
        mood = 'o'; look = (0.7, 0.8)
        arm_r, arm_l = math.radians(-60), math.radians(-120)
    if 22 <= t < 41:
        mood, sad, tilt = 'sad', ss(22, 23, t), math.radians(-8) * ss(22, 23, t)
        look = (0.6, 0.9) if t < 30 else ((-0.8, -0.6) if t < 36 else (-1, 0))
        arm_r, arm_l = math.radians(85), math.radians(95)
        if 30 < t < 38: mood = 'closed'
        if t > 38: mood, sad = 'o', 0
    if 39.5 < t < 44:
        mood, sad = 'smile', 0
        arm_l = math.radians(-120 + 25 * math.sin(t * 9)); look = (-1, 0)  # waves at friends
    if 44 <= t < 68:
        look = (-1, 0) if t < 58 else ((0.8, -0.8) if t < 63 else (1, 0.3))
        if 50 < t < 58 and int(t * 2) % 2 == 0: mood = 'closed'
        if 63 < t < 70:
            arm_r, arm_l = math.radians(-60 + 20 * math.sin(t * 9)), math.radians(-120 - 20 * math.sin(t * 9))
            y -= 40 * abs(math.sin(t * 5)) * ss(67.5, 68, t)
    if 71 < t < 84:  # on the trunk
        y = TRUNK_Y - 15 * math.sin(math.pi * ss(71, 72, t)) if t < 72 else TRUNK_Y
        arm_r, arm_l = math.radians(-10 + 12 * math.sin(t * 3)), math.radians(190 + 12 * math.sin(t * 3))
        tilt = math.radians(8) * math.sin(t * 3); look = (1, 0.4)
        mood = 'closed' if t < 80 else 'smile'
        walk = t * 5
    if 84 <= t < 85: y = kf(t, [(84, TRUNK_Y), (84.5, GROUND - 60), (85, GROUND)])
    if 85 <= t < 92:
        look = (1, -0.8)
        if 87 < t < 89:  # jump & grab
            y -= 150 * math.sin(math.pi * (t - 87) / 2)
            arm_r = math.radians(-70)
        if t > 88: hold = 'bunch'; arm_r = math.radians(-70 + 15 * math.sin(t * 8)) if t > 89 else arm_r
        if 89 < t < 92: y -= 40 * abs(math.sin(t * 6))
    if 92 <= t < 104: hold = 'bunch'; arm_r = math.radians(-50); look = (-1, 0)
    if 95 < t < 100.5:
        y = TRUNK_Y; walk = t * 9
        if t < 95.5: y = kf(t, [(95, GROUND), (95.5, TRUNK_Y)])
    if 100.5 <= t < 101: y = kf(t, [(100.5, TRUNK_Y), (101, GROUND)])
    if 103.5 < t < 110:
        hold = 'bunch'; look = (-0.5, -0.3)
        for (tt, _) in TOSS:
            if tt - 0.3 < t < tt + 0.3: arm_r = math.radians(-50 - 60 * math.sin(math.pi * (t - tt + 0.3) / 0.6))
    if t >= 110:
        hold = 'banana' if t < 118 else None
        mood = 'chew' if 110.5 < t < 114 else 'smile'; chew = t
        arm_r = math.radians(-60) if hold else arm_r
    if 114 < t < 118:
        y -= 30 * abs(math.sin(t * 4.5)); arm_l = math.radians(-120 + 25 * math.sin(t * 9))
    if t >= 118:
        arm_r = math.radians(-58 + 25 * math.sin(t * 9)); arm_l = math.radians(-122 - 25 * math.sin(t * 9)); look = (0, 0)
    blink = 0.0
    for bt in (6.0, 12.5, 26.0, 33.0, 47.0, 55.0, 61.0, 76.0, 97.0, 112.0, 121.0):
        if abs(t - bt) < 0.12: blink = 1 - abs(t - bt) / 0.12
    return dict(x=x, y=y, mood=mood, sad=sad, look=look, lid=max(lid, blink), arm_r=arm_r, arm_l=arm_l,
                tilt=tilt, hold=hold, walk=walk, chew=chew)

def tito_reach(t):
    full = (RIV_R + 30 - TITO_X) / 0.6
    if t < 63: return None
    if t < 101.5: return kf(t, [(63, 150), (67.5, full)])
    if t < 104: return kf(t, [(101.5, full), (103.5, 150)])
    return None

CAM_Z = [(0, 1.0), (9, 1.0), (11, 1.3), (16, 1.3), (17.5, 1.5), (29, 1.5), (31, 1.25), (39, 1.25), (42, 1.0),
         (57, 1.0), (59, 1.12), (69, 1.12), (71, 1.35), (91, 1.35), (93, 1.2), (102, 1.2), (104.5, 1.0)]
CAM_X = [(0, 960), (9, 960), (11, 880), (16, 880), (17.5, 700), (29, 700), (31, 760), (39, 760), (42, 960),
         (57, 960), (59, 840), (69, 840)]
CAM_Y = [(0, 540), (9, 540), (11, 620), (16, 620), (17.5, 690), (29, 690), (31, 640), (39, 640), (42, 540),
         (57, 540), (59, 590), (69, 590), (71, 650), (91, 650), (93, 620), (102, 620), (104.5, 540)]

def camera(t, coco_x):
    z, y = kf(t, CAM_Z), kf(t, CAM_Y)
    if t < 69: x = kf(t, CAM_X)
    else:
        follow = max(W / (2 * z), min(W - W / (2 * z), coco_x))
        base = kf(t, CAM_X)
        k = ss(69, 71, t) * (1 - ss(102, 104.5, t))
        x = base * (1 - k) + follow * k
        if t > 104.5: x = 960
    # never show outside the picture
    x = max(W / (2 * z), min(W - W / (2 * z), x)); y = max(H / (2 * z), min(H - H / (2 * z), y))
    return x, y, z

def frame(c, t):
    cx, cy, z = camera(t, kf(t, COCO_X))
    c.save(); c.translate(W / 2, H / 2); c.scale(z, z); c.translate(-cx, -cy)
    world(c, t)
    c.restore()
    overlay(c, t)

def world(c, t):
    c.set_source_surface(BG, 0, 0); c.paint()
    # clouds
    for i, (x0, y0, s, sp) in enumerate(((150, 160, 0.9, 12), (800, 90, 0.7, 8), (1250, 230, 0.6, 15))):
        c.save(); c.translate((x0 + sp * t) % 2300 - 250, y0); c.scale(s, s)
        for (cx, cy, r) in ((0, 0, 60), (70, -30, 75), (150, 0, 60), (75, 20, 60)): ellipse(c, cx, cy, r, r)
        c.set_source_rgba(1, 1, 1, 1); c.fill(); c.restore()
    water(c, t)
    bridge(c, t)
    splash(c, t, 18.25, 1075, 980)
    banana_tree(c, t, t < 88)

    cs = coco_state(t)
    # Pipa
    px = kf(t, PIPA_KF)
    if t > 44:
        neck = kf(t, [(57.5, 300), (59, 440), (62, 440), (63.5, 300)])
        if 105.2 < t < 106.2: neck = kf(t, [(105.2, 300), (105.5, 330), (106.2, 300)])
        look = (1, -0.3) if 58 < t < 63 else ((-1, 0.2) if 51 < t < 58 else (0.6, 0.1))
        lean = 40 * ss(58, 59, t) * (1 - ss(62, 63.5, t))
        bob = -8 * abs(math.sin(t * 4.5)) if 114 < t < 118 else 0
        K.put(c, K.pipa, px, GROUND + bob, 0.55, t=t, neck=neck, lean=lean, look=look,
              walk=t * 7 if moving(t, PIPA_KF) else 0, hold='banana' if 106 < t < 112 else None)
    # Tomi
    tx = kf(t, TOMI_KF)
    if t > 44:
        bob = -10 * abs(math.sin(t * 4.5)) if 114 < t < 118 else 0
        K.put(c, K.tomi, tx, GROUND + bob, 0.55, t=t, look=(1, -0.2) if t > 58 else (1, 0),
              walk=t * 3 if moving(t, TOMI_KF) else 0, hold='banana' if 109 < t < 112 else None)
    # Tito
    ttx = kf(t, TITO_KF)
    if t > 43:
        look = (-1, 0.2) if 51 < t < 58 else ((0.5, -0.5) if 58 < t < 63 else (1, 0.3))
        bob = -10 * abs(math.sin(t * 4.5)) if 114 < t < 118 else 0
        hold = 'banana' if 104.5 < t < 112 else None
        tip = K.put(c, K.tito, ttx, GROUND + bob, 0.6, t=t, look=look, reach=tito_reach(t),
                    walk=t * 6 if moving(t, TITO_KF) else 0, hold=hold)
        bulb(c, ttx, GROUND - 330, ss(60.2, 60.6, t) * (1 - ss(63, 63.4, t)) + 0.0001 * 0, t)
    # Coco
    K.put(c, K.coco, cs['x'], cs['y'], 0.55, t=t, look=cs['look'], lid=cs['lid'], mood=cs['mood'], sad=cs['sad'],
          arm_r=cs['arm_r'], arm_l=cs['arm_l'], walk=cs['walk'], head_tilt=cs['tilt'], hold=cs['hold'], chew=cs['chew'])
    thought(c, cs['x'] + 40, cs['y'] - 290, ss(11, 11.8, t) * (1 - ss(15.2, 15.6, t)) * 1.0 if 11 < t < 15.6 else 0)
    # Lola
    if 30 < t < 40:
        lx = kf(t, [(30, 2050), (34, 560), (37.5, 560), (40, -250)])
        ly = kf(t, [(30, 250), (34, 560), (37.5, 560), (40, 350)]) + 15 * math.sin(t * 4)
        K.put(c, K.lola, lx, ly, 0.5, t=t, flap=22, look=(0.8, 0.6) if t < 37 else (-1, 0))
    if t > 42:
        lx = kf(t, [(42, -250), (46, 520), (106.6, 520), (107.0, 560)])
        ly = kf(t, [(42, 400), (46, 560)]) + 15 * math.sin(t * 3.5)
        if 114 < t < 118: ly -= 30 * abs(math.sin(t * 4.5))
        K.put(c, K.lola, lx, ly, 0.5, t=t, flap=18, look=(1, 0.5), hold='banana' if 107.5 < t < 112 else None)
        if 113 < t < 119:
            for k in range(3):
                ph = (t * 0.7 + k / 3) % 1
                music_note(c, lx + 40 + 60 * ph + 20 * math.sin(ph * 8), ly - 150 - 160 * ph, math.sin(math.pi * ph),
                           ['#E91E63', '#1E88E5', '#FF9800'][k])
    # banana tosses
    for (tt, who) in TOSS:
        p = (t - tt) / 0.6
        if 0 <= p <= 1:
            sx, sy = cs['x'] + 40, GROUND - 260
            if who == 'tito': ex, ey = ttx + (150 + 30) * 0.6, GROUND - 115 * 0.6 - 30
            elif who == 'pipa': ex, ey = px + 20, GROUND - 0.55 * 560 + 60
            elif who == 'lola': ex, ey = 560, 560 - 60
            else: ex, ey = tx + 50, GROUND - 60
            bx, by = sx + (ex - sx) * p, sy + (ey - sy) * p - 160 * math.sin(math.pi * p)
            K.banana(c, bx, by, 1.0, p * 8)
        if 0.95 < p < 1.6:
            q = (p - 0.95) / 0.65
            ex2 = {'tito': ttx + 110, 'pipa': px + 20, 'lola': 560, 'tomi': tx + 50}[who]
            ey2 = {'tito': GROUND - 100, 'pipa': GROUND - 250, 'lola': 500, 'tomi': GROUND - 60}[who]
            for k in range(4):
                a = k * math.pi / 2 + q
                sparkle(c, ex2 + 50 * q * math.cos(a), ey2 + 50 * q * math.sin(a), 22 * (1 - q))
    # cheer sparkles when the trunk-bridge is done and when Coco grabs the bananas
    for (t0, x0, y0) in ((67.8, 950, 760), (88.5, 1470, 560)):
        q = (t - t0) / 1.2
        if 0 <= q <= 1:
            for k in range(8):
                a = k * math.pi / 4
                sparkle(c, x0 + 160 * q * math.cos(a), y0 + 120 * q * math.sin(a), 30 * math.sin(math.pi * q), '#FFF59D' if k % 2 else '#FFFFFF')

def overlay(c, t):
    if t < 5.5:
        a = 1 - ss(4.5, 5.3, t)
        if a > 0:
            c.push_group(); word(c, 'El puente del río', W / 2, 250, 120 * K_back((t - 0.6) / 0.6) + 0.01, tilt=0.05, outline=9)
            c.pop_group_to_source(); c.paint_with_alpha(a)
    if t > 118.5:
        s = K_back((t - 118.5) / 0.7)
        word(c, '¡Juntos se puede!', W / 2, 260, 130 * s + 0.01, tilt=0.06, outline=10)
        for k in range(10):
            ph = (t * 0.8 + k / 10) % 1
            sparkle(c, 300 + k * 150, 120 + 230 * ((k * 37) % 7) / 7, 26 * math.sin(math.pi * ph))
    a = max(1 - ss(0, 0.8, t), ss(DUR - 2.0, DUR, t))
    if a > 0: c.set_source_rgba(1, 1, 1, a); c.paint()

if __name__ == '__main__':
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(surf)
    args = sys.argv[1:]
    if args and args[0] == 'stills':
        for t in map(float, args[1:]):
            c.save(); frame(c, t); c.restore(); surf.write_to_png(f'ep02_{t}.png')
    else:
        t0, t1 = (float(args[1]), float(args[2])) if args and args[0] == 'range' else (0, DUR)
        out = sys.stdout.buffer
        for i in range(int(round(t0 * FPS)), int(round(t1 * FPS))):
            c.save(); frame(c, i / FPS); c.restore(); surf.flush(); out.write(surf.get_data())
