"""Episodio 10 — Cruzando el bosque (aventurita, 112 s, pensada para voz en off).
Los amigos caminan hasta la cascada. En el camino: un tronco gigante (Tito lo levanta),
un charco de barro (Coco salta, Tomi cruza arriba de Tito), el bosque oscuro
(Lola llama a las luciérnagas) y por fin la cascada.
El escenario se desplaza (coordenadas de "mundo" en X, cámara que sigue al grupo).

      python3 ep10_cruzando_el_bosque.py srt 5.5     -> subtítulos .srt de la narración
Uso:  python3 ep10_cruzando_el_bosque.py              -> cuadros crudos por stdout
      python3 ep10_cruzando_el_bosque.py range 0 56   -> solo un tramo
      python3 ep10_cruzando_el_bosque.py stills 12 65 -> PNG sueltos"""
import cairo, math, random, sys
import amigos as A, cuerpos as K
from amigos import hexc, ellipse, fill, OUT
from logos import word, sparkle, font
from ep02_puente_del_rio import kf, ss, K_back, music_note
from ep03_donde_esta_tomi import bubble
from ep09_semilla_magica import srt

W, H, FPS = 1920, 1080, 30
DUR = 112.0
GROUND = 880
LOG_X = 2600
MUD = (4900, 5250)
DARK = (6300, 6900, 8600, 9200)
FALL_X = 9850
POND = (9600, 520)

NARRACION = [
    (6.5, 11.5, 'Los amigos querían llegar a la cascada, del otro lado del bosque.'),
    (12.5, 18.0, 'Caminaron y caminaron entre los árboles.'),
    (21.0, 25.0, '¡Pero un tronco gigante tapaba el camino!'),
    (26.0, 31.0, 'Tito, que es muy fuerte, lo levantó con su trompa.'),
    (33.5, 38.5, 'Y siguieron caminando, muy contentos.'),
    (41.5, 46.0, '¡Un charco de barro! Coco lo cruzó de un salto.'),
    (47.0, 53.0, 'Y Tomi se subió a la espalda de Tito para cruzarlo.'),
    (59.0, 64.5, 'El bosque se puso cada vez más oscuro...'),
    (67.0, 71.5, 'Lola llamó a sus amigas, las luciérnagas.'),
    (73.0, 79.0, '¡Y las luciérnagas iluminaron el camino!'),
    (81.5, 86.5, 'Pipa estiró el cuello y vio... ¡la cascada!'),
    (93.0, 99.0, '¡Llegaron! Y todos se refrescaron en el agua.'),
    (103.5, 109.0, 'Cuando vamos juntos... ¡llegamos más lejos!'),
]

# ---------------- posiciones (mundo) ----------------
FORM = {'coco': 0, 'tomi': -230, 'tito': -480, 'pipa': -760}
BK = [(0, 550), (10, 550), (20, 2180), (31, 2180), (41, 4700), (58, 6050), (66, 7400), (72, 7400), (81, 9000), (86, 9000), (92, 9650)]
def B(t): return kf(t, BK)

def x_of(name, t):
    if name == 'tito' and 24 <= t < 33:
        return kf(t, [(24, 1700), (26, 2300), (30.5, 2300), (33, B(33) - 480)])
    if 41 <= t < 58:
        keys = {'coco': [(41, 4700), (42, 4700), (43.4, 5450), (53, 5450), (55.5, 6050)],
                'tito': [(41, 4220), (44, 4220), (46, 4470), (47, 4470), (53, 5570)],
                'pipa': [(41, 3940), (47.5, 3940), (53.5, 5290)],
                'tomi': None}[name]
        if name == 'tomi':
            if t < 46.3: return 4470
            if t < 53.5: return x_of('tito', t) - 70
            return kf(t, [(53.5, x_of('tito', 53.5) - 70), (55.0, 5820)])
        return kf(t, keys)
    return B(t) + FORM[name]

def walking(name, t): return abs(x_of(name, t + 0.05) - x_of(name, t)) > 1.0

def tomi_lift(t):
    if 46 < t < 46.8: return 165 * ss(46, 46.8, t) + 60 * math.sin(math.pi * (t - 46) / 0.8)
    if 46.8 <= t < 53.5: return 165
    if 53.5 <= t < 55: return 165 * (1 - ss(53.5, 55, t)) + 60 * math.sin(math.pi * (t - 53.5) / 1.5)
    return 0

def coco_jump(t):
    return 230 * math.sin(math.pi * (t - 42) / 1.4) if 42 < t < 43.4 else 0

def lola_world(t):
    return x_of('coco', t - 0.6) - 150 + 40 * math.sin(t * 0.7), 430 + 18 * math.sin(t * 3)

def cam_x(t):
    xs = [x_of(n, t) for n in ('coco', 'tomi', 'tito', 'pipa')]
    pan = kf(t, [(81.5, 0), (83.5, 350), (86.5, 350), (89, 0)])
    return sum(xs) / 4 + 60 + pan

def darkness(cx):
    return ss(DARK[0], DARK[1], cx) * (1 - ss(DARK[2], DARK[3], cx))

# ---------------- dibujo ----------------
def rnd(k, s=0): return random.Random(k * 7919 + s).random()

def far_hills(c, cam):
    f = 0.15; off = -(cam * f) % 900
    for k in range(-1, 4):
        x = off + k * 900 - 200
        c.move_to(x, 700); c.curve_to(x + 200, 470, x + 600, 470, x + 900, 700)
    c.line_to(W + 300, H); c.line_to(-300, H); c.close_path(); c.set_source_rgba(*hexc('#66BB6A')); c.fill()

def back_trees(c, cam):
    f = 0.5; base = cam * f
    k0 = int((base - 1200) // 230); k1 = int((base + 1200) // 230)
    for k in range(k0, k1 + 1):
        x = k * 230 - base + 960; h = 260 + 140 * rnd(k, 1); col = ['#2E7D32', '#388E3C', '#33691E'][int(rnd(k, 2) * 3)]
        c.rectangle(x - 14, 780 - h * 0.45, 28, h * 0.45); c.set_source_rgba(*hexc('#6D4C41')); c.fill()
        for (dx, dy, r) in ((-55, -h * 0.5, 70), (55, -h * 0.5, 70), (0, -h * 0.72, 90)):
            ellipse(c, x + dx, 780 + dy, r, r); c.set_source_rgba(*hexc(col)); c.fill()
    c.rectangle(0, 760, W, 60); c.set_source_rgba(*hexc('#43A047')); c.fill()

def ground(c, cam):
    c.rectangle(0, 805, W, H - 805); c.set_source_rgba(*hexc('#8BC34A')); c.fill()
    c.move_to(0, 850); c.curve_to(600, 840, 1300, 840, 1920, 850); c.line_to(1920, 930); c.curve_to(1300, 920, 600, 920, 0, 930)
    c.close_path(); c.set_source_rgba(*hexc('#D7C08A')); c.fill()   # path

def path_trees(c, cam):
    k0 = int((cam - 1300) // 520); k1 = int((cam + 1300) // 520)
    for k in range(k0, k1 + 1):
        wx = k * 520 + 180 * rnd(k, 3)
        if FALL_X - 900 < wx: continue
        x = wx - cam + 960; h = 380 + 120 * rnd(k, 4)
        c.move_to(x - 30, 820); c.curve_to(x - 20, 820 - h * 0.4, x - 25, 820 - h * 0.7, x - 18, 820 - h * 0.75)
        c.line_to(x + 18, 820 - h * 0.75); c.curve_to(x + 25, 820 - h * 0.7, x + 20, 820 - h * 0.4, x + 30, 820); c.close_path()
        fill(c, hexc('#8D5524'), OUT, 5)
        blobs = ((-90, -h * 0.78, 85), (90, -h * 0.78, 85), (0, -h * 0.95, 115), (0, -h * 0.7, 90))
        for (dx, dy, r) in blobs: ellipse(c, x + dx, 820 + dy, r, r); c.set_source_rgba(*OUT); c.set_line_width(10); c.stroke()
        for j, (dx, dy, r) in enumerate(blobs):
            ellipse(c, x + dx, 820 + dy, r, r); c.set_source_rgba(*hexc(['#43A047', '#43A047', '#4CAF50', '#388E3C'][j])); c.fill()
        if rnd(k, 5) > 0.5:
            for j in range(3):
                ellipse(c, x - 60 + j * 55, 820 - h * (0.8 + 0.07 * (j % 2)), 13, 13); fill(c, hexc(['#FF7043', '#FFCA28', '#EC407A'][j]), OUT, 3)

def flowers_front(c, cam):
    k0 = int((cam - 1100) // 300); k1 = int((cam + 1100) // 300)
    for k in range(k0, k1 + 1):
        wx = k * 300 + 120 * rnd(k, 6)
        x = wx - cam + 960; y = 960 + 40 * rnd(k, 7); col = ['#FF4081', '#FF9100', '#E040FB', '#FFEA00'][int(rnd(k, 8) * 4)]
        c.set_line_width(7); c.set_source_rgba(*hexc('#2E7D32')); c.move_to(x, y + 45); c.line_to(x, y); c.stroke()
        for i in range(6):
            a = i * math.pi / 3; ellipse(c, x + 18 * math.cos(a), y + 18 * math.sin(a), 13, 13); c.set_source_rgba(*hexc(col)); c.fill()
        ellipse(c, x, y, 10, 10); c.set_source_rgba(*hexc('#FFEB3B')); c.fill()

def fg_bushes(c, cam):
    f = 1.35; base = cam * f
    k0 = int((base - 1300) // 640); k1 = int((base + 1300) // 640)
    for k in range(k0, k1 + 1):
        x = k * 640 + 200 * rnd(k, 9) - base + 960
        for (dx, dy, r) in ((-80, 0, 85), (0, -40, 105), (80, 0, 85)):
            ellipse(c, x + dx, 1080 + dy, r, r)
        c.set_source_rgba(*hexc('#2E7D32')); c.fill()

def log_state(t):
    """(x, y, escala, rotación, atrás?) del tronco en el mundo."""
    if t < 27: return LOG_X, GROUND - 52, 1.0, 0.0, False
    if t < 29: q = ss(27, 29, t); return LOG_X + 40 * q, GROUND - 52 - 170 * q, 1.0, -0.25 * q, False
    q = ss(29, 30.5, t)
    return LOG_X + 40 + 260 * q, GROUND - 222 + 50 * q, 1.0 - 0.45 * q, -0.25 + 0.25 * q, q > 0.5

def draw_log(c, sx, y, s, rot):
    c.save(); c.translate(sx, y); c.rotate(rot); c.scale(s, s)
    c.rectangle(-160, -55, 320, 110); fill(c, hexc('#8D6E63'), OUT, 6)
    for k in range(4):
        c.move_to(-130 + k * 70, -35); c.line_to(-95 + k * 70, -35); c.set_source_rgba(*hexc('#6D4C41')); c.set_line_width(5); c.stroke()
    ellipse(c, 160, 0, 30, 55); fill(c, hexc('#D7B899'), OUT, 6)
    ellipse(c, 160, 0, 15, 30); c.set_source_rgba(*hexc('#A1887F')); c.set_line_width(4); c.stroke()
    ellipse(c, -60, -62, 30, 12); fill(c, hexc('#7CB342'), OUT, 3)
    c.restore()

def mud(c, cam, t):
    x0 = (MUD[0] + MUD[1]) / 2 - cam + 960
    if x0 < -400 or x0 > W + 400: return
    ellipse(c, x0, 905, (MUD[1] - MUD[0]) / 2 + 40, 34); fill(c, hexc('#6D4C41'), OUT, 5)
    ellipse(c, x0 - 60, 898, 70, 9); c.set_source_rgba(*hexc('#8D6E63')); c.fill()
    for k in range(3):
        q = (t * 0.6 + k / 3) % 1
        ellipse(c, x0 - 100 + k * 100, 902 - 10 * q, 8 * (1 - q) + 3, 8 * (1 - q) + 3)
        c.set_source_rgba(*hexc('#A1887F', 1 - q)); c.set_line_width(3); c.stroke()

def mud_splash(c, sx, t, ph):
    for k in range(4):
        q = (t * 2.2 + k / 4 + ph) % 1
        ellipse(c, sx + (k - 1.5) * 30 + 40 * q * (1 if k % 2 else -1), 900 - 80 * math.sin(math.pi * q), 7, 7)
        c.set_source_rgba(*hexc('#6D4C41', 1 - q * 0.5)); c.fill()

def waterfall(c, cam, t, back=True):
    xf = FALL_X - cam + 960
    if xf > W + 900: return
    px = POND[0] - cam + 960
    if back:
        c.move_to(xf - 120, GROUND - 20); c.line_to(xf - 70, 320); c.curve_to(xf + 100, 250, xf + 600, 250, xf + 900, 300)
        c.line_to(xf + 900, GROUND + 60); c.close_path(); fill(c, hexc('#8D9A8E'), OUT, 6)
        for (dx, dy, r) in ((60, 480, 50), (420, 380, 60), (650, 600, 70), (300, 700, 45)):
            ellipse(c, xf + dx, dy, r, r * 0.6); c.set_source_rgba(*hexc('#78887B')); c.fill()
        for (dx, r) in ((-60, 70), (90, 90), (300, 80), (520, 95), (760, 80)):
            ellipse(c, xf + dx, 300, r, r * 0.55); fill(c, hexc('#43A047'), OUT, 5)
        c.rectangle(xf + 90, 300, 240, GROUND - 300); g = cairo.LinearGradient(xf + 90, 0, xf + 330, 0)
        g.add_color_stop_rgb(0, *hexc('#81D4FA')[:3]); g.add_color_stop_rgb(0.5, *hexc('#E1F5FE')[:3]); g.add_color_stop_rgb(1, *hexc('#81D4FA')[:3])
        c.set_source(g); c.fill_preserve(); c.set_source_rgba(*OUT); c.set_line_width(5); c.stroke()
        c.set_line_cap(cairo.LINE_CAP_ROUND)
        for k in range(9):
            q = (t * 1.2 + k / 9) % 1
            sx = xf + 110 + (k * 23) % 200
            c.move_to(sx, 300 + q * (GROUND - 360)); c.line_to(sx, 300 + q * (GROUND - 360) + 70)
            c.set_source_rgba(1, 1, 1, 0.9); c.set_line_width(6); c.stroke()
        # mist rainbow
        for k, col in enumerate(('#F44336', '#FF9800', '#FFEB3B', '#4CAF50', '#2196F3', '#9C27B0')):
            c.set_source_rgba(*hexc(col, 0.45)); c.set_line_width(14)
            c.arc(xf + 210, GROUND + 40, 260 - k * 14, math.pi * 1.05, math.pi * 1.95); c.stroke()
        ellipse(c, px, GROUND + 25, POND[1], 62); fill(c, hexc('#4FC3F7'), hexc('#0277BD'), 6)
        for k in range(5):
            q = (t * 0.8 + k / 5) % 1
            ellipse(c, xf + 210 + (k - 2) * 50, GROUND + 15, 30 + 40 * q, 10 + 8 * q); c.set_source_rgba(1, 1, 1, 0.8 * (1 - q)); c.set_line_width(5); c.stroke()
    else:  # water in front of the legs of whoever is in the pond
        c.save(); ellipse(c, px, GROUND + 25, POND[1], 62); c.clip()
        c.rectangle(px - POND[1], GROUND - 8, 2 * POND[1], 120); c.set_source_rgba(*hexc('#4FC3F7', 0.75)); c.fill()
        c.restore()

FIRE = [(random.Random(i).uniform(-1, 1), random.Random(i + 50).uniform(0, 1), random.Random(i + 99).uniform(0, 6.28)) for i in range(16)]
def fireflies(t, cam):
    """Posiciones en pantalla de las luciérnagas que acompañan al grupo."""
    come = ss(67.5, 71, t)
    if come <= 0 or t > 90: return []
    leave = ss(86, 90, t)
    pts = []
    for (u, v, ph) in FIRE:
        tx = 960 + 760 * u + 60 * math.sin(t * 1.3 + ph)
        ty = 320 + 380 * v + 40 * math.sin(t * 1.7 + ph)
        sx0, sy0 = 960 + 1300 * (1 if u > 0 else -1), 200 + 500 * v
        x = sx0 + (tx - sx0) * come; y = sy0 + (ty - sy0) * come - 600 * leave
        pts.append((x, y, 0.6 + 0.4 * math.sin(t * 5 + ph)))
    return pts

def put(c, name, t, cam, **kw):
    sx = x_of(name, t) - cam + 960
    return sx

def party(t): return t < 5 or 93 < t < 110

def frame(c, t):
    cam = cam_x(t)
    g = cairo.LinearGradient(0, 0, 0, H)
    for k, col in enumerate(('#29B6F6', '#81D4FA', '#B3E5FC')): g.add_color_stop_rgb(k / 2, *hexc(col)[:3])
    c.set_source(g); c.paint()
    for (x0, y0, s, sp) in ((150, 150, 0.9, 12), (820, 100, 0.7, 8), (1450, 200, 0.6, 15)):
        c.save(); c.translate((x0 - cam * 0.05 + sp * t) % 2300 - 250, y0); c.scale(s, s)
        for (cx, cy, r) in ((0, 0, 60), (70, -30, 75), (150, 0, 60), (75, 20, 60)): ellipse(c, cx, cy, r, r)
        c.set_source_rgba(1, 1, 1, 1); c.fill(); c.restore()
    far_hills(c, cam); back_trees(c, cam); ground(c, cam); path_trees(c, cam)
    waterfall(c, cam, t, back=True)
    lx, ly, ls, lr, lback = log_state(t)
    if lback: draw_log(c, lx - cam + 960, ly, ls, lr)
    mud(c, cam, t)
    bounce = lambda ph: -25 * abs(math.sin(t * 4.5 + ph)) if party(t) else 0
    dark = darkness(cam)
    scared = dark > 0.5 and 64 < t < 71
    # Pipa
    sx = x_of('pipa', t) - cam + 960
    neck = kf(t, [(81.5, 300), (83.2, 720), (86.2, 720), (87.5, 300)])
    pl = (1, -0.8) if 81.5 < t < 87 else ((0.6, -0.4) if scared else (1, 0))
    K.put(c, K.pipa, sx, GROUND + bounce(0.5), 0.55, t=t, neck=neck, look=pl, walk=t * 7 if walking('pipa', t) else 0)
    if MUD[0] < x_of('pipa', t) < MUD[1] and walking('pipa', t): mud_splash(c, sx, t, 0.3)
    # Tito
    sx = x_of('tito', t) - cam + 960
    reach = None
    if 26 < t < 30: reach = kf(t, [(26, 150), (27, 270), (29, 270), (30, 150)])
    tl = (1, -0.6) if 26 < t < 30 else ((0.6, -0.4) if scared else (1, 0))
    if 93 < t < 103: reach = None
    K.put(c, K.tito, sx, GROUND + bounce(1.0), 0.6, t=t, look=tl, reach=reach, walk=t * 6 if walking('tito', t) else 0)
    if MUD[0] < x_of('tito', t) < MUD[1] and walking('tito', t): mud_splash(c, sx, t, 0.0)
    if 95 < t < 103:  # water fountain from the trunk
        tipx, tipy = sx + 0.6 * 180, GROUND - 0.6 * 115
        for k in range(14):
            q = ((t - 95) * 1.3 + k / 14) % 1
            ellipse(c, tipx + 160 * q * (1 if k % 2 else -0.6), tipy - 420 * q + 520 * q * q, 8, 10)
            c.set_source_rgba(*hexc('#4FC3F7', 1 - q * 0.6)); c.fill()
    if not lback: draw_log(c, lx - cam + 960, ly, ls, lr)
    # Tomi
    sx = x_of('tomi', t) - cam + 960
    K.put(c, K.tomi, sx, GROUND + bounce(1.5) - tomi_lift(t), 0.55, t=t, look=(0.7, -0.3) if scared else (1, 0),
          walk=t * 3 if walking('tomi', t) and tomi_lift(t) == 0 else 0)
    # Coco
    sx = x_of('coco', t) - cam + 960
    mood, look = 'smile', (1, 0)
    arm_r, arm_l = math.radians(65 + 6 * math.sin(t * 2)), math.radians(115 - 6 * math.sin(t * 2))
    if party(t): arm_r, arm_l = math.radians(-58 + 25 * math.sin(t * 9)), math.radians(-122 - 25 * math.sin(t * 9))
    if 20 < t < 26: mood, look = 'o', (1, -0.2)
    if 30 < t < 31.5: arm_r, arm_l = math.radians(-60), math.radians(-120)
    if 41 < t < 42.2: mood = 'o'; look = (1, 0.6)
    if 42 < t < 43.4: arm_r, arm_l = math.radians(-60), math.radians(-120)
    if 44 < t < 53: look = (-1, 0); arm_l = math.radians(-120 + 25 * math.sin(t * 9))
    if scared: mood = 'o'; look = (math.sin(t * 2.5), -0.3); arm_r, arm_l = math.radians(-100), math.radians(-80)
    if 81.5 < t < 87: look = (1, -0.6); mood = 'o' if t < 84 else 'smile'
    if 91.5 < t < 93: arm_r, arm_l = math.radians(-60), math.radians(-120)
    blink = 0.0
    for bt in (3.0, 15.0, 35.0, 50.0, 62.0, 75.0, 88.0, 100.0):
        if abs(t - bt) < 0.12: blink = 1 - abs(t - bt) / 0.12
    K.put(c, K.coco, sx, GROUND + bounce(0) - coco_jump(t), 0.55, t=t, mood=mood, look=look, lid=blink, arm_r=arm_r, arm_l=arm_l,
          walk=t * 8 if walking('coco', t) and coco_jump(t) == 0 else 0)
    waterfall(c, cam, t, back=False)
    if 92.5 < t < 94.5:  # big splash when Coco jumps in
        q = (t - 92.5) / 2.0
        for k in range(10):
            a = math.pi * (0.1 + 0.8 * k / 9)
            ellipse(c, sx + 200 * q * math.cos(a), GROUND - 20 - 260 * q * math.sin(a) + 300 * q * q, 12 * (1 - q) + 3, 14 * (1 - q) + 3)
            c.set_source_rgba(*hexc('#81D4FA', 1 - q)); c.fill()
    # Lola
    lwx, ly = lola_world(t)
    lx_ = lwx - cam + 960
    K.put(c, K.lola, lx_, ly + bounce(2.0), 0.5, t=t, flap=20, look=(1, 0.3))
    if 95 < t < 110:
        for k in range(3):
            ph = (t * 0.7 + k / 3) % 1
            music_note(c, lx_ + 40 + 60 * ph, ly - 150 - 160 * ph, math.sin(math.pi * ph), ['#E91E63', '#1E88E5', '#FF9800'][k])
    flowers_front(c, cam)
    # darkness with holes of light around the fireflies
    ff = fireflies(t, cam)
    if dark > 0.01:
        c.push_group()
        c.set_source_rgba(*hexc('#0D1240', 0.82 * dark)); c.paint()
        c.set_operator(cairo.OPERATOR_DEST_OUT)
        for (x, y, k) in ff:
            rg = cairo.RadialGradient(x, y, 0, x, y, 300)
            rg.add_color_stop_rgba(0, 0, 0, 0, 0.75 * k); rg.add_color_stop_rgba(1, 0, 0, 0, 0)
            c.set_source(rg); c.arc(x, y, 300, 0, 2 * math.pi); c.fill()
        c.set_operator(cairo.OPERATOR_OVER)
        c.pop_group_to_source(); c.paint()
    for (x, y, k) in ff:
        rg = cairo.RadialGradient(x, y, 0, x, y, 40)
        rg.add_color_stop_rgba(0, 1, 1, 0.5, 0.7 * k); rg.add_color_stop_rgba(1, 1, 1, 0.5, 0)
        c.set_source(rg); c.arc(x, y, 40, 0, 2 * math.pi); c.fill()
        ellipse(c, x, y, 8, 8); c.set_source_rgba(1, 1, 0.6, 0.6 + 0.4 * k); c.fill()
    if dark > 0.3 and t < 71:  # little eyes peeking in the dark
        for k in range(3):
            ex, ey = 300 + k * 650, 520 + 60 * (k % 2)
            for d in (-12, 12):
                ellipse(c, ex + d, ey, 6, 8 * (0.2 if (t * 0.7 + k) % 3 < 0.15 else 1)); c.set_source_rgba(1, 1, 0.8, dark * 0.8); c.fill()
    fg_bushes(c, cam)
    # bubbles (screen coordinates)
    cx_ = x_of('coco', t) - cam + 960
    bubble(c, cx_, GROUND - 300, '¡Un tronco gigante!', (t - 20.5) / 3.0, 46)
    bubble(c, cx_, GROUND - 300 - coco_jump(t), '¡Vengan!', (t - 44.0) / 2.6, 50)
    bubble(c, cx_, GROUND - 300, '¡Qué oscuro!', (t - 64.5) / 2.6, 50)
    bubble(c, lx_, ly - 120, '¡Luciérnagas, ayúdennos!', (t - 67.0) / 3.0, 44)
    psx = x_of('pipa', t) - cam + 960
    bubble(c, psx + 60, GROUND - 0.55 * (260 + 720 + 175) - 130, '¡Veo la cascada!', (t - 83.3) / 3.0, 46)
    bubble(c, cx_, GROUND - 300, '¡Al agua!', (t - 91.0) / 2.4, 52)

def overlay(c, t):
    if t < 5.6:
        a = 1 - ss(4.8, 5.5, t)
        c.push_group(); word(c, 'Cruzando el bosque', W / 2, 230, 120 * K_back((t - 0.6) / 0.6) + 0.01, tilt=0.05, outline=9)
        c.pop_group_to_source(); c.paint_with_alpha(a)
    if t > 103:
        s = K_back((t - 103) / 0.7)
        word(c, '¡Juntos llegamos', W / 2, 180, 110 * s + 0.01, tilt=0.06, outline=10)
        word(c, 'más lejos!', W / 2, 320, 120 * s + 0.01, start=3, tilt=0.06, outline=10)
    a = max(1 - ss(0, 0.8, t), ss(DUR - 2.0, DUR, t))
    if a > 0: c.set_source_rgba(1, 1, 1, a); c.paint()

def full(c, t):
    frame(c, t); overlay(c, t)

if __name__ == '__main__':
    args = sys.argv[1:]
    if args and args[0] == 'srt':
        print(srt(NARRACION, float(args[1]) if len(args) > 1 else 0.0)); sys.exit()
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(surf)
    if args and args[0] == 'stills':
        for t in map(float, args[1:]):
            c.save(); full(c, t); c.restore(); surf.write_to_png(f'ep10_{t}.png')
    else:
        t0, t1 = (float(args[1]), float(args[2])) if args and args[0] == 'range' else (0, DUR)
        out = sys.stdout.buffer
        for i in range(int(round(t0 * FPS)), int(round(t1 * FPS))):
            c.save(); full(c, i / FPS); c.restore(); surf.flush(); out.write(surf.get_data())
