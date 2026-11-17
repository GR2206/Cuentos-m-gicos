"""Episodio 15 — Navidad en la selva (102 s).
En la selva no hay pinos... ¡así que los amigos decoran una palmera! Tito cuelga bolas,
Lola enrolla una guirnalda, Tomi trae regalitos, Pipa pone la estrella y de noche las
luciérnagas son las lucecitas. Llegan Mamá y Papá Coco con gorros y todos cantan.

      python3 ep15_navidad.py srt 5.5     -> subtítulos .srt de la narración
Uso:  python3 ep15_navidad.py              -> cuadros crudos por stdout
      python3 ep15_navidad.py range 0 51   -> solo un tramo
      python3 ep15_navidad.py stills 12 65 -> PNG sueltos"""
import cairo, math, sys
import cuerpos as K
from amigos import hexc, ellipse, fill, OUT
from logos import word, sparkle
from ep02_puente_del_rio import kf, ss, moving, K_back, music_note
from ep03_donde_esta_tomi import bubble
from ep09_semilla_magica import SKY, LAND, cloud, sun, srt
from ep14_bananas_papa import heart
from ep05_cumple_tomi import gift

W, H, FPS = 1920, 1080, 30
DUR = 102.0
GROUND = 880
TX = 960                      # palmera-arbolito
TOP = (TX + 30, 330)          # copa
NIGHT0, NIGHT1 = 54.0, 59.0

NARRACION = [
    (6.0, 11.0, '¡Mañana es Navidad! Coco quería un arbolito...'),
    (12.0, 17.0, 'Pero en la selva no hay pinos.'),
    (18.0, 22.0, 'Entonces Pipa tuvo una idea: ¡decorar la palmera!'),
    (23.0, 29.0, 'Tito colgó bolitas de colores con su trompa.'),
    (31.0, 37.0, 'Lola voló alrededor con una guirnalda brillante.'),
    (39.0, 45.0, 'Tomi llegó despacito... ¡con regalitos para todos!'),
    (47.0, 53.0, 'Y Pipa puso la estrella, bien arriba.'),
    (55.0, 60.0, 'Cuando llegó la noche, las luciérnagas encendieron el arbolito.'),
    (61.5, 67.0, '¡Y llegaron Mamá y Papá Coco, con gorritos para todos!'),
    (69.0, 83.0, 'Y todos juntos cantaron: ¡Feliz Navidad en la selva!'),
    (85.0, 92.0, 'Lo más lindo de la Navidad... es estar juntos.'),
    (95.0, 100.0, '¡Feliz Navidad!'),
]
LYRICS = [('¡Feliz Navidad,', 'feliz Navidad!', 69.0), ('¡En la selva', 'hay luz y amor!', 73.0),
          ('¡Feliz Navidad,', 'feliz Navidad!', 77.0), ('¡Que estemos', 'todos juntos!', 81.0)]

BALLS = [(TX - 200, 420, '#F44336'), (TX + 230, 400, '#FFEB3B'), (TX - 130, 330, '#2196F3'), (TX + 160, 300, '#E040FB'),
         (TX - 250, 480, '#FF9800'), (TX + 280, 470, '#F44336'), (TX - 60, 410, '#00E676'), (TX + 90, 430, '#FF4081')]
BALL_T = [23.5 + k * 0.85 for k in range(len(BALLS))]
GIFTS = [(TX - 120, '#E040FB', 0.7), (TX + 110, '#29B6F6', 0.6), (TX - 10, '#F44336', 0.55)]

def night(t): return ss(NIGHT0, NIGHT1, t)

def santa_hat(c, x, y, s, tilt=0.0):
    c.save(); c.translate(x, y); c.rotate(tilt); c.scale(s, s)
    c.move_to(-60, 0); c.curve_to(-40, -80, 30, -120, 90, -70); c.curve_to(40, -70, 40, -20, 60, 0); c.close_path()
    fill(c, hexc('#E53935'), OUT, 5)
    c.new_path(); r = 22
    c.arc(-60 + r, 0, r, math.pi / 2, 3 * math.pi / 2); c.arc(60 - r, 0, r, -math.pi / 2, math.pi / 2); c.close_path()
    fill(c, (1, 1, 1, 1), OUT, 5)
    ellipse(c, 92, -70, 18, 18); fill(c, (1, 1, 1, 1), OUT, 4)
    c.restore()

def xmas_palm(c, t, n):
    x, y = TX, GROUND
    sway = math.sin(t * 1.2)
    tipx, tipy = TOP
    c.set_line_cap(cairo.LINE_CAP_ROUND)
    for (col, w) in ((OUT, 60), (hexc('#8D5524'), 48)):
        c.move_to(x, y); c.curve_to(x + 5, y - 220, x + 20, y - 420, tipx, tipy)
        c.set_source_rgba(*col); c.set_line_width(w); c.stroke()
    for i, ang in enumerate((-175, -140, -105, -75, -40, -5, 200)):
        a = math.radians(ang + 4 * sway)
        c.save(); c.translate(tipx, tipy); c.rotate(a)
        c.move_to(0, 0); c.curve_to(90, -55, 210, -40, 300, 40); c.curve_to(200, 18, 90, 26, 0, 0); c.close_path()
        fill(c, hexc('#2E7D32' if i % 2 else '#43A047'), hexc('#1B5E20'), 4); c.restore()
    return n

def garland(c, t):
    q = ss(31.0, 38.0, t)
    if q <= 0: return
    pts = []
    for k in range(120):
        u = k / 119
        if u > q: break
        a = u * 3.2 * math.pi
        r = 280 - 120 * u
        pts.append((TX + 20 + r * math.cos(a), 520 - 200 * u + 40 * math.sin(a)))
    if len(pts) < 2: return
    for (col, w) in ((OUT, 14), (hexc('#FFD600'), 9)):
        c.move_to(*pts[0])
        for p in pts[1:]: c.line_to(*p)
        c.set_source_rgba(*col); c.set_line_width(w); c.stroke()
    for k in range(0, len(pts), 12):
        sparkle(c, pts[k][0], pts[k][1], 9 + 4 * math.sin(t * 5 + k), '#FFFFFF')

def ornaments(c, t, lit):
    for k, (bx, by, col) in enumerate(BALLS):
        t0 = BALL_T[k]
        if t < t0 + 0.5: continue
        s = K_back((t - t0 - 0.5) / 0.4)
        c.move_to(bx, by - 30 * s); c.line_to(bx, by - 45 * s); c.set_source_rgba(*OUT); c.set_line_width(3); c.stroke()
        if lit:
            g = cairo.RadialGradient(bx, by, 0, bx, by, 70)
            g.add_color_stop_rgba(0, *hexc(col)[:3], 0.5 * lit); g.add_color_stop_rgba(1, *hexc(col)[:3], 0)
            c.set_source(g); c.arc(bx, by, 70, 0, 2 * math.pi); c.fill()
        ellipse(c, bx, by, 26 * s, 26 * s); fill(c, hexc(col), OUT, 4)
        ellipse(c, bx - 8 * s, by - 8 * s, 7 * s, 7 * s); c.set_source_rgba(1, 1, 1, 0.8); c.fill()

def star(c, t, pos, s, glow):
    x, y = pos
    if glow > 0:
        g = cairo.RadialGradient(x, y, 0, x, y, 200 * s)
        g.add_color_stop_rgba(0, 1, 0.95, 0.5, 0.6 * glow); g.add_color_stop_rgba(1, 1, 0.95, 0.5, 0)
        c.set_source(g); c.arc(x, y, 200 * s, 0, 2 * math.pi); c.fill()
    c.save(); c.translate(x, y); c.rotate(0.1 * math.sin(t * 2)); c.scale(s, s)
    for i in range(10):
        rr = 70 if i % 2 == 0 else 32
        a = -math.pi / 2 + i * math.pi / 5
        (c.move_to if i == 0 else c.line_to)(rr * math.cos(a), rr * math.sin(a))
    c.close_path(); fill(c, hexc('#FFD600'), hexc('#F57F17'), 6)
    c.restore()

def star_pos(t):
    top = (TOP[0], TOP[1] - 70)
    if t < 46: return None
    if t < 49.0:  # en la cabeza de Pipa, sube con el cuello
        return pipa_head(t)[0] - 10, pipa_head(t)[1] - 80
    if t < 50.2:
        q = ss(49.0, 50.2, t); hx, hy = pipa_head(49.0)
        return hx - 10 + (top[0] - hx + 10) * q, hy - 80 + (top[1] - hy + 80) * q - 60 * math.sin(math.pi * q)
    return top

PIPA_X = [(0, 1650), (45.5, 1650), (47, 1240), (52.5, 1240), (54, 1500)]
def pipa_neck(t): return kf(t, [(46.5, 300), (49.0, 760), (50.5, 760), (52.5, 300)])
def pipa_lean(t): return kf(t, [(46.5, 0), (49.0, -180), (50.5, -180), (52.5, 0)])
def pipa_head(t):
    return kf(t, PIPA_X) + 0.55 * pipa_lean(t), GROUND - 0.55 * (260 + pipa_neck(t))

TITO_X = [(0, 1350), (22.5, 1350), (23.3, 1250), (31, 1250), (32, 1330)]
TOMI_X = [(0, 2100), (38.5, 2100), (45.5, 1100)]
COCO_X = [(0, 600), (8, 600), (10.5, 330), (13, 330), (16, 600)]
PAPA_X = [(0, -400), (60.5, -400), (64.5, 160)]
MAMA_X = [(0, -250), (60.5, -250), (64.5, 360)]

def lola_pos(t):
    if t < 31: return 1150 + 80 * math.sin(t * 0.6), 470 + 18 * math.sin(t * 3)
    if t < 38.2:
        q = ss(31.0, 38.0, t); a = q * 3.2 * math.pi; r = 280 - 120 * q
        return TX + 20 + r * math.cos(a), 520 - 200 * q + 40 * math.sin(a) - 60
    return kf(t, [(38.2, TX + 180), (40, 1150)]) + 60 * math.sin(t * 0.6), 470 + 18 * math.sin(t * 3)

def party(t): return 69 < t < 84

def fireflies(c, t, cam_lit):
    come = ss(NIGHT1 - 1.5, NIGHT1 + 2.0, t)
    if come <= 0: return 0.0
    for k in range(22):
        a = k * 2.3
        tx_ = TX + 30 + (260 - 9 * k) * math.cos(a + 0.2 * math.sin(t + k))
        ty_ = 560 - 12 * k + 40 * math.sin(a)
        sx_, sy_ = TX + 1100 * math.cos(k * 1.7), -100 - 50 * (k % 5)
        x = sx_ + (tx_ - sx_) * come; y = sy_ + (ty_ - sy_) * come
        kk = 0.6 + 0.4 * math.sin(t * 5 + k)
        g = cairo.RadialGradient(x, y, 0, x, y, 40)
        g.add_color_stop_rgba(0, 1, 1, 0.5, 0.8 * kk); g.add_color_stop_rgba(1, 1, 1, 0.5, 0)
        c.set_source(g); c.arc(x, y, 40, 0, 2 * math.pi); c.fill()
        ellipse(c, x, y, 7, 7); c.set_source_rgba(1, 1, 0.7, 1); c.fill()
    return come

def world(c, t):
    nt = night(t)
    c.set_source_surface(SKY, 0, 0); c.paint()
    if nt < 1:
        c.push_group(); sun(c, t)
        for (x0, y0, s, sp) in ((150, 160, 0.9, 10), (700, 110, 0.7, 7)): cloud(c, (x0 + sp * t) % 2300 - 250, y0, s)
        c.pop_group_to_source(); c.paint_with_alpha(1 - nt)
    if nt > 0:
        c.set_source_rgba(*hexc('#141048', 0.92 * nt)); c.paint()
        for k in range(40):
            sx, sy = (k * 197) % 1900, 30 + (k * 83) % 420
            ellipse(c, sx, sy, 3, 3); c.set_source_rgba(1, 1, 0.85, nt * (0.6 + 0.4 * math.sin(t * 3 + k))); c.fill()
        ellipse(c, 1600, 170, 80, 80); fill(c, (1, 0.96, 0.62, nt), (0.98, 0.75, 0.18, nt), 6)
    c.set_source_surface(LAND, 0, 0); c.paint()
    if nt > 0: c.set_source_rgba(*hexc('#141048', 0.55 * nt)); c.mask_surface(LAND, 0, 0)
    lit = fireflies_amount(t)
    xmas_palm(c, t, 0)
    garland(c, t)
    ornaments(c, t, lit)
    sp = star_pos(t)
    if sp and t >= 50.2: star(c, t, sp, 1.0, max(lit, 0.4 if t > 50.2 else 0))
    for k, (gx, col, s) in enumerate(GIFTS):
        if t > 45.5 + k * 0.4: gift(c, gx, GROUND + 10, s)
    bounce = lambda ph: -25 * abs(math.sin(t * 4.5 + ph)) if party(t) else 0
    hats = ss(65, 66, t)
    # Pipa
    px = kf(t, PIPA_X)
    pl = (-1, -0.6) if 46 < t < 52.5 else ((-1, -0.3) if 18 < t < 22 else (-0.6, 0))
    K.put(c, K.pipa, px, GROUND + bounce(0.5), 0.55, t=t, neck=pipa_neck(t), lean=pipa_lean(t), look=pl, walk=t * 7 if moving(t, PIPA_X) else 0)
    if sp and t < 50.2: star(c, t, sp, 0.7, 0.3)
    if hats > 0: hx, hy = pipa_head(t); santa_hat(c, hx + 5, hy - 75 + bounce(0.5), 0.75 * hats, 0.15)
    # Tito
    tx = kf(t, TITO_X)
    reach = None
    for k, t0 in enumerate(BALL_T):
        if t0 - 0.2 < t < t0 + 0.7: reach = 150 + 120 * math.sin(math.pi * (t - t0 + 0.2) / 0.9)
    tl = (-1, -0.6) if 23 < t < 31 else (-0.6, 0)
    K.put(c, K.tito, tx, GROUND + bounce(1.0), 0.6, flip=True, t=t, look=(1, tl[1]), reach=reach, walk=t * 6 if moving(t, TITO_X) else 0)
    for k, t0 in enumerate(BALL_T):  # bola viajando en la trompa
        q = (t - t0) / 0.5
        if 0 <= q < 1:
            sx, sy = tx - 0.6 * 200, GROUND - 60
            bx, by, col = BALLS[k]
            ellipse(c, sx + (bx - sx) * q, sy + (by - sy) * q, 22, 22); fill(c, hexc(col), OUT, 4)
    if hats > 0: santa_hat(c, tx + 10, GROUND - 0.6 * 455 + bounce(1.0), 0.95 * hats, 0.1)
    # Tomi
    tmx = kf(t, TOMI_X)
    K.put(c, K.tomi, tmx, GROUND + bounce(1.5), 0.55, t=t, look=(-1, 0), walk=t * 3 if moving(t, TOMI_X) else 0)
    if 38.5 < t < 45.5: gift(c, tmx + 10, GROUND - 0.55 * 230, 0.45)
    if hats > 0: santa_hat(c, tmx, GROUND - 0.55 * 275 + bounce(1.5), 0.7 * hats, -0.1)
    # Papá y Mamá
    pax, max_ = kf(t, PAPA_X), kf(t, MAMA_X)
    hug = 85 < t < 92
    if t > 60.5:
        K.put(c, K.papa, pax, GROUND + bounce(0.8), 0.72, t=t, look=(1, 0), walk=t * 7 if moving(t, PAPA_X) else 0,
              arm_r=math.radians(-58 + 25 * math.sin(t * 9)) if party(t) else math.radians(50), arm_l=math.radians(115), mood='closed' if hug else 'smile')
        K.put(c, K.mama, max_, GROUND + bounce(1.3), 0.72, t=t, look=(1, 0), walk=t * 7 if moving(t, MAMA_X) else 0,
              arm_r=math.radians(-58 + 25 * math.sin(t * 9 + 1)) if party(t) else math.radians(65), arm_l=math.radians(115), mood='closed' if hug else 'smile')
        if t < 66: gift(c, pax + 60, GROUND - 0.72 * 160, 0.6)
        santa_hat(c, pax, GROUND - 0.72 * 455 + bounce(0.8), 0.95, -0.1)
        santa_hat(c, max_ - 10, GROUND - 0.72 * 455 + bounce(1.3), 0.95, 0.1)
    # Coco
    cx = kf(t, COCO_X)
    mood, sad, look = 'smile', 0.0, (1, -0.3)
    ar, al = math.radians(65 + 6 * math.sin(t * 2)), math.radians(115 - 6 * math.sin(t * 2))
    if 9 < t < 17: mood, sad, look = ('o' if t < 12 else 'sad'), (1.0 if t >= 12 else 0), (-1 if t < 13 else 1, -0.2)
    if 18 < t < 22: ar, al = math.radians(-60), math.radians(-120); mood = 'o'
    if 50.2 < t < 53 or 59 < t < 61: ar, al = math.radians(-60), math.radians(-120)
    if party(t): ar, al = math.radians(-58 + 25 * math.sin(t * 9)), math.radians(-122 - 25 * math.sin(t * 9))
    if hug: mood = 'closed'; ar, al = math.radians(170), math.radians(10)
    K.put(c, K.coco, cx, GROUND + bounce(0), 0.55, t=t, mood=mood, sad=sad, look=look, arm_r=ar, arm_l=al, walk=t * 8 if moving(t, COCO_X) else 0)
    if hats > 0: santa_hat(c, cx, GROUND - 0.55 * 455 + bounce(0), 0.75 * hats, -0.15)
    # Lola
    lx, ly = lola_pos(t)
    K.put(c, K.lola, lx, ly + bounce(2.0), 0.5, t=t, flap=20, look=(-0.5, 0.4))
    if 31 < t < 38.2: ellipse(c, lx - 30, ly - 60, 10, 10); fill(c, hexc('#FFD600'), OUT, 3)
    if hats > 0: santa_hat(c, lx + 5, ly - 0.5 * 330 + bounce(2.0), 0.55 * hats, 0.2)
    fireflies(c, t, lit)
    if party(t):
        for k in range(3):
            ph = (t * 0.7 + k / 3) % 1
            music_note(c, lx + 40 + 60 * ph, ly - 150 - 160 * ph, math.sin(math.pi * ph), ['#E91E63', '#1E88E5', '#FFD600'][k])
    if hug:
        for k in range(5):
            ph = ((t - 85) * 0.5 + k / 5) % 1
            heart(c, 420 + 220 * math.sin(k * 1.7), GROUND - 420 - 250 * ph, 1.0 + 0.5 * ph, math.sin(math.pi * ph))
    # copos/brillos mágicos de noche
    if nt > 0.5:
        for k in range(14):
            ph = (t * 0.15 + k / 14) % 1
            sparkle(c, (k * 137) % 1900, -20 + 1000 * ph, 10 * nt, '#FFFFFF')
    bubble(c, cx, GROUND - 300, '¡Quiero un arbolito!', (t - 6.3) / 3.4, 46)
    bubble(c, cx, GROUND - 300, 'No hay pinos…', (t - 13.0) / 3.0, 48)
    bubble(c, pipa_head(t)[0], pipa_head(t)[1] - 110, '¡Decoremos la palmera!', (t - 18.2) / 3.6, 44)
    bubble(c, tmx, GROUND - 230, '¡Regalitos!', (t - 45.0) / 2.6, 50)
    bubble(c, (pax + max_) / 2, GROUND - 0.72 * 560, '¡Feliz Navidad!', (t - 64.5) / 3.0, 50)

def fireflies_amount(t): return ss(NIGHT1 - 1.5, NIGHT1 + 2.0, t)

def overlay(c, t):
    if t < 5.6:
        a = 1 - ss(4.8, 5.5, t)
        c.push_group(); word(c, 'Navidad en la selva', W / 2, 230, 125 * K_back((t - 0.6) / 0.6) + 0.01,
                             colors=['#E53935', '#43A047', '#FFD600'], tilt=0.05, outline=9)
        c.pop_group_to_source(); c.paint_with_alpha(a)
    for (a1, b1, t0) in LYRICS:
        if t0 <= t < t0 + 4.0:
            s = K_back((t - t0) / 0.4) * (1 - ss(t0 + 3.7, t0 + 4.0, t))
            word(c, a1, W / 2, 150, 95 * s + 0.01, colors=['#E53935', '#43A047', '#FFD600'], tilt=0.05, outline=8)
            word(c, b1, W / 2, 260, 95 * s + 0.01, colors=['#43A047', '#FFD600', '#E53935'], tilt=0.05, outline=8)
    if t > 93:
        s = K_back((t - 93) / 0.7)
        word(c, '¡Feliz Navidad!', W / 2, 220, 150 * s + 0.01, colors=['#E53935', '#43A047', '#FFD600'], tilt=0.06, outline=11)
    a = max(1 - ss(0, 0.8, t), ss(DUR - 2.0, DUR, t))
    if a > 0: c.set_source_rgba(1, 1, 1, a); c.paint()

CAM = [(0, 1.0, 960, 540), (8, 1.0, 960, 540), (9.5, 1.25, 650, 620), (16, 1.25, 650, 620), (17.5, 1.0, 960, 540),
       (45.5, 1.0, 960, 540), (46.5, 1.2, 1120, 470), (51, 1.2, 1120, 470), (52.5, 1.0, 960, 540)]
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
    args = sys.argv[1:]
    if args and args[0] == 'srt':
        print(srt(NARRACION, float(args[1]) if len(args) > 1 else 0.0)); sys.exit()
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(surf)
    if args and args[0] == 'stills':
        for t in map(float, args[1:]):
            c.save(); frame(c, t); c.restore(); surf.write_to_png(f'ep15_{t}.png')
    else:
        t0, t1 = (float(args[1]), float(args[2])) if args and args[0] == 'range' else (0, DUR)
        out = sys.stdout.buffer
        for i in range(int(round(t0 * FPS)), int(round(t1 * FPS))):
            c.save(); frame(c, i / FPS); c.restore(); surf.flush(); out.write(surf.get_data())
