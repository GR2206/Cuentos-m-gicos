"""Episodio 9 — La semilla mágica (aventurita, 112 s, pensada para voz en off).
Tomi encuentra una semilla brillante. Coco hace un pocito, Tomi la planta, Tito la riega,
Lola le canta y Pipa corre una nube para que le dé el sol. Esperan toda la noche...
¡y crece un árbol mágico con frutas de colores para todos!

El guion de la narración (con tiempos) está en NARRACION y se exporta a .srt con:
      python3 ep09_semilla_magica.py srt
Uso:  python3 ep09_semilla_magica.py                -> cuadros crudos por stdout
      python3 ep09_semilla_magica.py range 0 56     -> solo un tramo
      python3 ep09_semilla_magica.py stills 12 65   -> PNG sueltos"""
import cairo, math, sys
import amigos as A, cuerpos as K
from amigos import hexc, ellipse, fill, OUT
from logos import word, sparkle, font
from ep02_puente_del_rio import kf, ss, moving, K_back, music_note, palm
from ep03_donde_esta_tomi import bubble

W, H, FPS = 1920, 1080, 30
DUR = 112.0
GROUND = 880
SPOT = 960
SUN = (1450, 170)

NARRACION = [  # (inicio, fin, texto)
    (6.5, 11.0, 'Una mañana, Tomi encontró algo brillante en el pasto.'),
    (12.0, 16.0, '¡Era una semilla mágica!'),
    (17.0, 22.0, 'Los amigos tuvieron una idea: ¡plantarla todos juntos!'),
    (23.5, 28.5, 'Coco hizo un pocito en la tierra.'),
    (30.0, 35.5, 'Tomi puso la semilla con mucho cuidado.'),
    (37.5, 42.5, 'Tito la regó con su trompa.'),
    (44.0, 49.0, 'Lola le cantó una canción.'),
    (50.5, 56.5, 'Y Pipa corrió una nube para que le diera el sol.'),
    (58.0, 63.0, 'Esperaron... y esperaron... toda la noche.'),
    (64.5, 69.5, '¡Y a la mañana, la semilla empezó a crecer!'),
    (73.5, 79.5, '¡Era un árbol mágico, lleno de frutas de colores!'),
    (81.5, 87.5, 'Y hubo una fruta para cada amigo.'),
    (95.0, 101.0, 'Lo que cuidamos con amor... ¡crece!'),
]

SKY, LAND = None, None
def make_bg():
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
    palm(c, 90, GROUND, 540, 1); palm(c, 1840, GROUND, 500, -1)
    for (fx, col) in ((250, '#FF4081'), (560, '#FF9100'), (1340, '#E040FB'), (1650, '#FFEA00')):
        c.set_line_width(7); c.set_source_rgba(*hexc('#2E7D32')); c.move_to(fx, 975); c.line_to(fx, 930); c.stroke()
        for i in range(6):
            a = i * math.pi / 3; ellipse(c, fx + 20 * math.cos(a), 925 + 20 * math.sin(a), 15, 15); c.set_source_rgba(*hexc(col)); c.fill()
        ellipse(c, fx, 925, 12, 12); c.set_source_rgba(*hexc('#FFEB3B')); c.fill()
    return sky, land
SKY, LAND = make_bg()

def night(t): return ss(57.5, 59.5, t) * (1 - ss(62.5, 64.5, t))

def sun(c, t):
    x, y = SUN
    for i in range(12):
        c.save(); c.translate(x, y); c.rotate(i * math.pi / 6 + t * 0.2)
        c.move_to(-20, -110); c.line_to(0, -155); c.line_to(20, -110); c.close_path(); c.set_source_rgba(*hexc('#FFB300')); c.fill(); c.restore()
    ellipse(c, x, y, 90, 90); fill(c, hexc('#FFEB3B'), hexc('#F9A825'), 7)
    c.set_source_rgba(*OUT); c.set_line_width(7); c.set_line_cap(cairo.LINE_CAP_ROUND)
    for ex in (-30, 30): c.arc(x + ex, y - 12, 14, math.pi * 1.1, math.pi * 1.9); c.stroke()
    c.arc(x, y + 12, 32, 0.15 * math.pi, 0.85 * math.pi); c.stroke()

def cloud(c, x, y, s, col=(1, 1, 1, 1)):
    c.save(); c.translate(x, y); c.scale(s, s)
    for (cx, cy, r) in ((0, 0, 60), (70, -30, 75), (150, 0, 60), (75, 20, 60)): ellipse(c, cx, cy, r, r)
    c.set_source_rgba(*col); c.fill(); c.restore()

def sun_cloud_x(t): return kf(t, [(0, SUN[0] - 115), (52.5, SUN[0] - 115), (55.0, SUN[0] + 330)])

def seed(c, x, y, t, s=1.0):
    g = cairo.RadialGradient(x, y, 0, x, y, 70 * s)
    g.add_color_stop_rgba(0, 1, 0.95, 0.5, 0.6); g.add_color_stop_rgba(1, 1, 0.95, 0.5, 0)
    c.set_source(g); c.arc(x, y, 70 * s, 0, 2 * math.pi); c.fill()
    c.save(); c.translate(x, y); c.rotate(0.3 * math.sin(t * 3)); c.scale(s, s)
    c.move_to(0, -26); c.curve_to(20, -20, 20, 18, 0, 26); c.curve_to(-20, 18, -20, -20, 0, -26); c.close_path()
    fill(c, hexc('#FFB74D'), OUT, 4)
    c.move_to(0, -18); c.curve_to(6, -6, 6, 6, 0, 18); c.set_source_rgba(*hexc('#E65100')); c.set_line_width(3); c.stroke()
    c.restore()
    sparkle(c, x + 26 * s, y - 26 * s, (10 + 5 * math.sin(t * 6)) * s, '#FFFFFF')

def hole(c, t):
    dig = ss(24.0, 28.0, t)
    if dig <= 0: return
    filled = ss(34.0, 35.5, t)
    if filled < 1:
        ellipse(c, SPOT, 902, 70 * dig, 18 * dig); fill(c, hexc('#5D4037'), OUT, 4)
    if filled > 0 or dig > 0.3:  # mound of dirt beside / over the hole
        mx = SPOT - 120 * (1 - filled) if filled < 1 else SPOT
        c.move_to(mx - 70, 905); c.curve_to(mx - 50, 905 - 45 * max(dig, filled), mx + 50, 905 - 45 * max(dig, filled), mx + 70, 905)
        c.close_path(); fill(c, hexc('#795548'), OUT, 4)

FRUIT_COLS = ['#F44336', '#FF9800', '#FFEB3B', '#AB47BC', '#29B6F6', '#EC407A', '#66BB6A']
FRUITS = [(-170, -560), (-60, -640), (80, -600), (190, -520), (-130, -440), (30, -470), (150, -420)]

def tree(c, t):
    g = ss(64.5, 69.5, t)   # stem
    cr = ss(68.5, 73.0, t)  # crown
    if g <= 0: return
    hgt = 40 + 330 * g
    x = SPOT
    # trunk / stem
    w0 = 10 + 38 * cr
    c.move_to(x - w0, GROUND - 5); c.curve_to(x - w0 * 0.7, GROUND - hgt * 0.5, x - w0 * 0.5, GROUND - hgt * 0.8, x - w0 * 0.4, GROUND - hgt)
    c.line_to(x + w0 * 0.4, GROUND - hgt); c.curve_to(x + w0 * 0.5, GROUND - hgt * 0.8, x + w0 * 0.7, GROUND - hgt * 0.5, x + w0, GROUND - 5)
    c.close_path(); fill(c, hexc('#8D5524') if cr > 0.3 else hexc('#7CB342'), OUT, 5)
    if cr < 0.2:  # two sprout leaves
        for side in (-1, 1):
            c.save(); c.translate(x, GROUND - hgt + 5); c.rotate(side * 0.7 - math.pi / 2)
            L = 60 + 40 * g
            c.move_to(0, 0); c.curve_to(L * 0.3, -L * 0.3, L * 0.8, -L * 0.2, L, 0); c.curve_to(L * 0.8, L * 0.2, L * 0.3, L * 0.3, 0, 0)
            c.close_path(); fill(c, hexc('#7CB342'), OUT, 4); c.restore()
        return
    s = K_back((cr - 0.2) / 0.8)
    cx, cy = x, GROUND - hgt - 120
    blobs = ((-170, 30, 120), (170, 30, 120), (0, -60, 170), (-100, -110, 120), (100, -110, 120), (0, 60, 130))
    for (bx, by, r) in blobs:
        ellipse(c, cx + bx * s, cy + by * s, r * s, r * s); c.set_source_rgba(*OUT); c.set_line_width(12); c.stroke()
    for k, (bx, by, r) in enumerate(blobs):
        ellipse(c, cx + bx * s, cy + by * s, r * s, r * s); c.set_source_rgba(*hexc(['#43A047', '#43A047', '#66BB6A', '#4CAF50', '#4CAF50', '#388E3C'][k])); c.fill()
    for k, ((fx, fy), col) in enumerate(zip(FRUITS, FRUIT_COLS)):
        t0 = 72.5 + k * 0.25
        if t < t0 or fruit_taken(k, t): continue
        fs = K_back((t - t0) / 0.4)
        fruit(c, x + fx, GROUND + fy + 5 * math.sin(t * 2 + k), col, fs)
    if 72.5 < t < 80:
        for j in range(10):
            ph = (t * 0.8 + j / 10) % 1
            a = j * 2 * math.pi / 10
            sparkle(c, cx + 260 * math.cos(a), cy + 200 * math.sin(a), 24 * math.sin(math.pi * ph), '#FFF59D')

def fruit(c, x, y, col, s=1.0):
    if s <= 0.01: return
    ellipse(c, x, y, 30 * s, 30 * s); fill(c, hexc(col), OUT, 4)
    ellipse(c, x - 10 * s, y - 10 * s, 8 * s, 8 * s); c.set_source_rgba(1, 1, 1, 0.6); c.fill()
    c.move_to(x, y - 28 * s); c.line_to(x + 4 * s, y - 42 * s); c.set_source_rgba(*hexc('#5D4037')); c.set_line_width(4 * s); c.stroke()
    ellipse(c, x + 12 * s, y - 38 * s, 10 * s, 5 * s); c.set_source_rgba(*hexc('#43A047')); c.fill()

# who gets which fruit, when
GIVE = [(82.0, 0, 'coco'), (83.0, 1, 'tomi'), (84.0, 3, 'lola'), (85.0, 2, 'pipa'), (86.0, 4, 'tito')]
def fruit_taken(k, t):
    for (t0, kk, _) in GIVE:
        if kk == k and t >= t0: return True
    return False

# ---------------- personajes ----------------
COCO_X = [(0, 600), (21, 600), (23, 840), (29, 840), (31, 700), (33.5, 860), (35.7, 860), (37, 680)]
TOMI_X = [(0, 2050), (4, 1500), (8, 1100), (11, 1060), (15, 1060), (18, 1190), (29.5, 1190), (31.5, 1060), (35, 1060), (36.5, 1210)]
TITO_X = [(0, 1500), (16, 1500), (36.5, 1500), (37.3, 1440), (44, 1440), (45, 1490)]
PIPA_X = [(0, 420), (49.5, 420), (52, 1300), (56.8, 1300), (59.5, 420)]

def hero_targets(name):
    return {'coco': (lambda t: kf(t, COCO_X)), 'tomi': (lambda t: kf(t, TOMI_X)), 'tito': (lambda t: kf(t, TITO_X)),
            'pipa': (lambda t: kf(t, PIPA_X)), 'lola': (lambda t: lola_pos(t)[0])}[name]

def lola_pos(t):
    x = kf(t, [(0, 2100), (16, 2100), (19, 1200), (43, 1200), (44.5, SPOT + 40), (49.5, SPOT + 40), (51, 760)])
    y = kf(t, [(0, 300), (16, 300), (19, 420), (43, 420), (44.5, 560), (49.5, 560), (51, 420)])
    return x, y + 15 * math.sin(t * 3)

def party(t): return 88 < t < 104 or 1 < t < 5

def world(c, t):
    c.set_source_surface(SKY, 0, 0); c.paint()
    nt = night(t)
    if nt > 0:
        c.set_source_rgba(*hexc('#1A1556', 0.85 * nt)); c.paint()
        for k in range(30):
            sx, sy = (k * 137) % 1900, 40 + (k * 71) % 480
            ellipse(c, sx, sy, 3, 3); c.set_source_rgba(1, 1, 0.85, nt * (0.6 + 0.4 * math.sin(t * 3 + k))); c.fill()
        ellipse(c, 480, 180, 80, 80); fill(c, (1, 0.96, 0.62, nt), (0.98, 0.75, 0.18, nt), 6)
    if nt < 1:
        c.push_group()
        sun(c, t)
        for i, (x0, y0, s, sp) in enumerate(((150, 160, 0.9, 10), (700, 110, 0.7, 7))):
            cloud(c, (x0 + sp * t) % 2300 - 250, y0, s)
        # the cloud that hides the sun
        cloud(c, sun_cloud_x(t), SUN[1] + 10, 1.25, hexc('#ECEFF1'))
        c.pop_group_to_source(); c.paint_with_alpha(1 - nt)
    c.set_source_surface(LAND, 0, 0); c.paint()
    if nt > 0: c.set_source_rgba(*hexc('#1A1556', 0.55 * nt)); c.mask_surface(LAND, 0, 0)
    # sunbeam on the seed
    beam = ss(55.0, 56.5, t) * (1 - nt) * (1 - ss(72, 76, t))
    if beam > 0:
        c.move_to(SUN[0] - 60, SUN[1] + 60); c.line_to(SUN[0] + 20, SUN[1] + 90); c.line_to(SPOT + 90, 905); c.line_to(SPOT - 90, 905); c.close_path()
        g = cairo.LinearGradient(SUN[0], SUN[1], SPOT, 905)
        g.add_color_stop_rgba(0, 1, 0.95, 0.5, 0.5 * beam); g.add_color_stop_rgba(1, 1, 0.95, 0.5, 0.15 * beam)
        c.set_source(g); c.fill()
    hole(c, t)
    tree(c, t)
    bounce = lambda ph: -25 * abs(math.sin(t * 4.5 + ph)) if party(t) else 0
    sleepy = ss(58.5, 59.5, t) * (1 - ss(63.5, 64.5, t))
    # Pipa
    px = kf(t, PIPA_X)
    neck = kf(t, [(51.5, 300), (52.8, 780), (55.5, 780), (56.8, 300)])
    lean = kf(t, [(51.5, 0), (52.8, 170), (55.5, 170), (56.8, 0)])
    pl = (1, -1) if 51.5 < t < 56 else ((-0.4, -1) if 70 < t < 81 else (0, 0))
    pj = 60 * math.sin(math.pi * (t - 85.6) / 0.6) if 85.6 < t < 86.2 else 0
    K.put(c, K.pipa, px, GROUND + bounce(0.5) - pj, 0.55, t=t, neck=neck, lean=lean, look=pl, walk=t * 7 if moving(t, PIPA_X) else 0)
    # Tito (faces left)
    tx = kf(t, TITO_X)
    reach = None
    if 38 < t < 43.5: reach = kf(t, [(38, 150), (39, (tx - SPOT) / 0.6 - 10), (42.5, (tx - SPOT) / 0.6 - 10), (43.5, 150)])
    tl = (1, 0.2) if 38 < t < 43.5 else ((1, -1) if 70 < t < 81 else (1, 0))
    K.put(c, K.tito, tx, GROUND + bounce(1.0), 0.6, flip=True, t=t, look=tl, reach=reach, lid=sleepy,
          walk=t * 6 if moving(t, TITO_X) else 0)
    if 39 < t < 43:
        tipx = tx - 0.6 * ((tx - SPOT) / 0.6 - 10)
        for k in range(10):
            q = ((t - 39) * 1.6 + k / 10) % 1
            ellipse(c, tipx + (k % 3 - 1) * 14, GROUND - 36 + 70 * q, 7, 11); c.set_source_rgba(*hexc('#4FC3F7', 1 - q * 0.5)); c.fill()
    # Tomi
    tmx = kf(t, TOMI_X)
    tmlook = (-1, 0.4) if 8 < t < 16 else ((-0.5, -1) if 70 < t < 81 else (-0.6, 0))
    K.put(c, K.tomi, tmx, GROUND + bounce(1.5), 0.55, t=t, look=tmlook, walk=t * 3 if moving(t, TOMI_X) else 0)
    # the seed
    if t < 11: seed(c, SPOT + 100, 895, t, 0.9)
    elif t < 30.5:
        sx, sy = tmx - 10, GROUND - 0.55 * 290
        if t < 12: q = t - 11; sx, sy = SPOT + 100 + (sx - SPOT - 100) * q, 895 + (sy - 895) * q - 80 * math.sin(math.pi * q)
        seed(c, sx, sy, t, 1.0)
    elif t < 32.0:
        q = (t - 30.5) / 1.5
        sx0, sy0 = kf(30.5, TOMI_X) - 10, GROUND - 0.55 * 290
        seed(c, sx0 + (SPOT - sx0) * q, sy0 + (900 - sy0) * q - 120 * math.sin(math.pi * q), t, 1.0)
    elif t < 34.5: seed(c, SPOT, 900, t, 0.8)
    # Coco
    cx = kf(t, COCO_X)
    mood, look = 'smile', (0.6, 0.3)
    arm_r, arm_l = math.radians(65 + 6 * math.sin(t * 2)), math.radians(115 - 6 * math.sin(t * 2))
    if party(t):
        arm_r, arm_l = math.radians(-58 + 25 * math.sin(t * 9)), math.radians(-122 - 25 * math.sin(t * 9))
    if 12 < t < 16: mood = 'o'; look = (1, 0.3)
    if 17 < t < 21: arm_r, arm_l = math.radians(-60), math.radians(-120)
    if 23.5 < t < 28.5 or 34 < t < 35.6:  # digging / covering
        arm_r = math.radians(40 + 45 * abs(math.sin(t * 7))); arm_l = math.radians(140 - 45 * abs(math.sin(t * 7 + 1)))
        look = (0.8, 1)
    if 57 < t < 64: look = (0.6, 0.8)
    if 70 < t < 81: look = (0.5, -1); mood = 'o' if t < 75 else 'smile'
    cj = 70 * math.sin(math.pi * (t - 82.3) / 0.6) if 82.3 < t < 82.9 else 0
    if t > 82.5 and t < 88: mood = 'chew'
    K.put(c, K.coco, cx, GROUND + bounce(0) - cj, 0.55, t=t, mood=mood, look=look, lid=sleepy, arm_r=arm_r, arm_l=arm_l,
          walk=t * 8 if moving(t, COCO_X) else 0, chew=t)
    if 24 < t < 28.5 or 34 < t < 35.6:  # flying dirt
        for k in range(5):
            q = ((t * 1.8) + k / 5) % 1
            ellipse(c, SPOT - 40 - 120 * q, 890 - 120 * math.sin(math.pi * q), 8, 8); c.set_source_rgba(*hexc('#6D4C41')); c.fill()
    # Lola
    lx, ly = lola_pos(t)
    K.put(c, K.lola, lx, ly + bounce(2.0), 0.5, t=t, flap=20, look=(-0.5, 0.6) if 44 < t < 50 else ((-0.3, -1) if 70 < t < 81 else (0, 0.4)),
          lid=sleepy if t < 64 else 0)
    if 44.5 < t < 50 or 90 < t < 104:
        for k in range(3):
            ph = (t * 0.7 + k / 3) % 1
            music_note(c, lx + 40 + 60 * ph, ly - 150 - 160 * ph, math.sin(math.pi * ph), ['#E91E63', '#1E88E5', '#FF9800'][k])
    # fruits flying to each friend
    for (t0, k, who) in GIVE:
        q = (t - t0) / 0.8
        fx, fy = SPOT + FRUITS[k][0], GROUND + FRUITS[k][1]
        tx_ = {'coco': cx + 40, 'tomi': tmx, 'lola': lx + 40, 'pipa': px + 20, 'tito': tx - 60}[who]
        ty_ = {'coco': GROUND - 270, 'tomi': GROUND - 200, 'lola': ly - 100, 'pipa': GROUND - 0.55 * 735 + 40, 'tito': GROUND - 250}[who]
        if 0 <= q < 1:
            fruit(c, fx + (tx_ - fx) * q, fy + (ty_ - fy) * q - 140 * math.sin(math.pi * q), FRUIT_COLS[k])
        elif 1 <= q < 2.2:
            fruit(c, tx_, ty_, FRUIT_COLS[k], 1 - ss(1.6, 2.2, q))
            if q < 1.8:
                for j in range(6):
                    a = j * math.pi / 3
                    sparkle(c, tx_ + 60 * (q - 1) * math.cos(a), ty_ + 60 * (q - 1) * math.sin(a), 16, FRUIT_COLS[k])
    # bubbles
    bubble(c, tmx, GROUND - 230, '¡Una semilla!', (t - 12.2) / 3.0, 48)
    bubble(c, cx, GROUND - 300, '¡Plantémosla!', (t - 18.0) / 3.0, 48)
    bubble(c, cx, GROUND - 300, '¡Guau!', (t - 74.0) / 2.6, 56)
    bubble(c, tmx, GROUND - 230, '¡Mmm, qué rica!', (t - 84.0) / 3.0, 46)

def overlay(c, t):
    if t < 5.6:
        a = 1 - ss(4.8, 5.5, t)
        c.push_group(); word(c, 'La semilla mágica', W / 2, 230, 125 * K_back((t - 0.6) / 0.6) + 0.01, tilt=0.05, outline=9)
        c.pop_group_to_source(); c.paint_with_alpha(a)
    if t > 101.5:
        s = K_back((t - 101.5) / 0.7)
        word(c, '¡Lo que cuidamos', W / 2, 180, 110 * s + 0.01, tilt=0.06, outline=10)
        word(c, 'con amor, crece!', W / 2, 320, 110 * s + 0.01, start=3, tilt=0.06, outline=10)
    a = max(1 - ss(0, 0.8, t), ss(DUR - 2.0, DUR, t))
    if a > 0: c.set_source_rgba(1, 1, 1, a); c.paint()

CAM = [(0, 1.0, 960, 540), (6, 1.0, 960, 540), (8, 1.3, 1150, 650), (16, 1.3, 1100, 650), (18, 1.0, 960, 540),
       (22.5, 1.0, 960, 540), (24, 1.35, 940, 680), (36, 1.35, 1000, 680), (37.5, 1.2, 1150, 640), (44, 1.2, 1150, 640),
       (45, 1.15, 980, 600), (50, 1.15, 980, 600), (51.5, 1.0, 1100, 540), (57, 1.0, 960, 540),
       (64, 1.0, 960, 540), (65.5, 1.3, 960, 640), (68.5, 1.3, 960, 640), (71, 1.0, 960, 540)]
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

def srt(lines, offset=0.0):
    def ts(x):
        x += offset; h = int(x // 3600); m = int(x % 3600 // 60); s = x % 60
        return f'{h:02d}:{m:02d}:{int(s):02d},{int(round((s - int(s)) * 1000)):03d}'
    return '\n'.join(f'{i + 1}\n{ts(a)} --> {ts(b)}\n{txt}\n' for i, (a, b, txt) in enumerate(lines))

if __name__ == '__main__':
    args = sys.argv[1:]
    if args and args[0] == 'srt':
        print(srt(NARRACION, float(args[1]) if len(args) > 1 else 0.0)); sys.exit()
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(surf)
    if args and args[0] == 'stills':
        for t in map(float, args[1:]):
            c.save(); frame(c, t); c.restore(); surf.write_to_png(f'ep09_{t}.png')
    else:
        t0, t1 = (float(args[1]), float(args[2])) if args and args[0] == 'range' else (0, DUR)
        out = sys.stdout.buffer
        for i in range(int(round(t0 * FPS)), int(round(t1 * FPS))):
            c.save(); frame(c, i / FPS); c.restore(); surf.flush(); out.write(surf.get_data())
