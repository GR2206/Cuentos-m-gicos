"""Episodio 11 — La pelota perdida (aventurita, 110 s, pensada para voz en off).
Tito patea la pelota muy fuerte y se va por el bosque. Para recuperarla: Tomi hace de piedrita
en el arroyo, Pipa la baja de un árbol con el cuello y Tito la saca de la laguna con un chorro de agua.
Mismo motor de escenario que se desplaza que el episodio 10.

      python3 ep11_pelota_perdida.py srt 5.5     -> subtítulos .srt de la narración
Uso:  python3 ep11_pelota_perdida.py              -> cuadros crudos por stdout
      python3 ep11_pelota_perdida.py range 0 55   -> solo un tramo
      python3 ep11_pelota_perdida.py stills 12 65 -> PNG sueltos"""
import cairo, math, sys
import cuerpos as K
from amigos import hexc, ellipse, fill, OUT
from logos import word, sparkle
from ep02_puente_del_rio import kf, ss, K_back, music_note
from ep03_donde_esta_tomi import bubble
from ep04_lluvia_magica import ball
from ep09_semilla_magica import srt
from ep10_cruzando_el_bosque import far_hills, back_trees, ground, path_trees, flowers_front, fg_bushes

W, H, FPS = 1920, 1080, 30
DUR = 110.0
GROUND = 880
STREAM = (2700, 2980)
TREE_X = 5500
BALL_TREE = (5470, 430)
POND = (7950, 380)

NARRACION = [
    (6.0, 10.5, 'Los amigos jugaban a la pelota, cuando Tito... ¡la pateó muy fuerte!'),
    (11.5, 16.5, '¡La pelota se fue rodando por el bosque!'),
    (22.0, 26.5, 'Para seguirla había que cruzar un arroyo.'),
    (27.5, 33.5, 'Tomi se metió en el agua y su caparazón fue una piedrita para saltar.'),
    (39.0, 44.0, 'Siguieron buscando entre los árboles...'),
    (46.5, 50.5, '¡La pelota estaba trabada en un árbol!'),
    (51.5, 56.5, 'Pipa estiró el cuello y... ¡la bajó!'),
    (57.0, 61.0, 'Pero la pelota siguió rodando...'),
    (62.0, 66.5, 'Lola voló bien alto y gritó: ¡allá está!'),
    (71.0, 75.0, 'La pelota había caído en la laguna.'),
    (76.0, 81.5, 'Tito tomó agua con la trompa y... ¡un chorro gigante la trajo de vuelta!'),
    (84.0, 90.0, 'Y todos volvieron a jugar, pasándose la pelota.'),
    (103.0, 108.0, 'Jugar juntos... ¡es mucho más divertido!'),
]

FORM = {'coco': 0, 'tomi': -230, 'tito': -480, 'pipa': -760}
BK = [(0, 900), (11, 900), (22, 2450), (38, 3800), (46, 5000), (58, 5000), (70, 7300), (110, 7300)]
def B(t): return kf(t, BK)

def x_of(name, t):
    if 22 <= t < 38:
        keys = {'coco': [(22, 2450), (29, 2450), (30, 2840), (30.5, 2840), (31.5, 3150), (33, 3150), (37, 3800)],
                'tomi': [(22, 2220), (24, 2220), (27.5, 2840), (36, 2840), (38, 3570)],
                'tito': [(22, 1970), (31, 1970), (35.5, 3320)],
                'pipa': [(22, 1690), (32, 1690), (36.5, 3040)]}[name]
        return kf(t, keys)
    if name == 'pipa' and 49 <= t < 58.5:
        return kf(t, [(49, 4240), (51, 5150), (56, 5150), (58.5, B(58.5) - 760)])
    if name == 'tito' and 74 <= t < 82:
        return kf(t, [(74, 6820), (76, 7420), (80.5, 7420), (82, 6820)])
    return B(t) + FORM[name]

def walking(name, t): return abs(x_of(name, t + 0.05) - x_of(name, t)) > 1.0

def coco_hop(t):
    if 29 < t < 30: return 130 * math.sin(math.pi * (t - 29)) + 115 * (t - 29) if t > 29.5 else 130 * math.sin(math.pi * (t - 29))
    if 30.5 < t < 31.5: return 130 * math.sin(math.pi * (t - 30.5)) + 115 * (31.5 - t) * (1 if t < 31 else 1)
    if 48 < t < 50: return 110 * abs(math.sin(math.pi * (t - 48) / 1.0))
    return 0.0

def tomi_hide(t): return ss(27.5, 28.5, t) * (1 - ss(35.5, 36.2, t))

def lola_world(t):
    if 58.5 < t < 68:
        x = kf(t, [(58.5, x_of('coco', 58.5) - 150), (62, x_of('coco', 62) + 480), (65, x_of('coco', 65) + 480), (68, x_of('coco', 68) - 150)])
        y = kf(t, [(58.5, 430), (62, 400), (65, 400), (68, 430)])
        return x, y + 15 * math.sin(t * 3)
    return x_of('coco', t - 0.6) - 150 + 40 * math.sin(t * 0.7), 430 + 18 * math.sin(t * 3)

def cam_x(t):
    xs = [x_of(n, t) for n in ('coco', 'tomi', 'tito', 'pipa')]
    pan = kf(t, [(45, 0), (47, 260), (57, 260), (58.5, 0), (69, 0), (71, 300), (82, 300), (84, 120)])
    return sum(xs) / 4 + 60 + pan

# ---------------- la pelota ----------------
PASS = [(1.5, 'coco', 'tito'), (3.3, 'tito', 'coco'), (5.0, 'coco', 'tito')]
PLAY = [(84.0, 'coco', 'tomi'), (86.0, 'tomi', 'tito'), (88.0, 'tito', 'pipa'), (90.0, 'pipa', 'coco'),
        (92.0, 'coco', 'tito'), (94.0, 'tito', 'tomi'), (96.0, 'tomi', 'pipa'), (98.0, 'pipa', 'coco'), (100.0, 'coco', 'tito')]

def holder_point(name, t):
    x = x_of(name, t)
    return {'coco': (x + 40, GROUND - 300), 'tomi': (x, GROUND - 200), 'tito': (x + 120, GROUND - 120),
            'pipa': (x + 20, GROUND - 0.55 * 735 + 40)}[name]

def ball_world(t):
    """(x, y) de la pelota en el mundo, o None."""
    for (t0, a, b) in PASS + PLAY:
        if t0 <= t < t0 + 1.7:
            q = (t - t0) / 1.7
            (x0, y0), (x1, y1) = holder_point(a, t), holder_point(b, t)
            return x0 + (x1 - x0) * q, y0 + (y1 - y0) * q - 220 * math.sin(math.pi * q)
    if t < 1.5: return holder_point('coco', t)
    if t < 6.5: return holder_point('tito', t)
    if t < 9.0:  # the big kick
        q = (t - 6.5) / 2.5
        x0, y0 = holder_point('tito', 6.5)
        return x0 + 1900 * q, y0 - 420 * math.sin(math.pi * min(1, q * 1.3)) + (0 if q < 0.77 else -80 * abs(math.sin(q * 12)))
    if t < 55.2: return BALL_TREE[0] + 4 * math.sin(t * 3), BALL_TREE[1]
    if t < 56.4:
        q = (t - 55.2) / 1.2
        return BALL_TREE[0] + 120 * q, BALL_TREE[1] + (GROUND - 40 - BALL_TREE[1]) * q * q
    if t < 58.5:
        q = (t - 56.4) / 2.1
        return BALL_TREE[0] + 120 + 1100 * q, GROUND - 40 - 90 * abs(math.sin(q * 3 * math.pi)) * (1 - q)
    if t < 78.6: return POND[0], GROUND + 5 + 6 * math.sin(t * 2)
    if t < 80.4:
        q = (t - 78.6) / 1.8
        x1, y1 = holder_point('coco', t)
        return POND[0] + (x1 - POND[0]) * q, GROUND + 5 + (y1 - GROUND - 5) * q - 380 * math.sin(math.pi * q)
    if t < 84.0 or t >= 101.7: return holder_point('coco', t)
    for (t0, a, b) in PLAY:
        if t0 + 1.7 <= t < t0 + 2.0: return holder_point(b, t)
    return holder_point('coco', t)

# ---------------- escenario extra ----------------
def stream(c, cam, t, front=False):
    x0, x1 = STREAM[0] - cam + 960, STREAM[1] - cam + 960
    if x1 < -200 or x0 > W + 200: return
    if not front:
        c.move_to(x0 + 60, 805); c.curve_to(x0 + 20, 900, x0 - 30, 980, x0 - 60, H)
        c.line_to(x1 + 60, H); c.curve_to(x1 + 30, 980, x1 - 20, 900, x1 - 60, 805); c.close_path()
        g = cairo.LinearGradient(0, 805, 0, H)
        g.add_color_stop_rgb(0, *hexc('#4FC3F7')[:3]); g.add_color_stop_rgb(1, *hexc('#0288D1')[:3])
        c.set_source(g); c.fill_preserve(); c.set_source_rgba(*hexc('#6D4C41')); c.set_line_width(8); c.stroke()
        c.set_line_cap(cairo.LINE_CAP_ROUND)
        for k in range(8):
            q = (t * 0.4 + k / 8) % 1
            y = 820 + q * 250; xm = (x0 + x1) / 2 + 60 * math.sin(k * 2.1)
            c.move_to(xm - 30, y); c.curve_to(xm - 10, y - 6, xm + 10, y + 6, xm + 30, y)
            c.set_source_rgba(1, 1, 1, 0.6 * math.sin(math.pi * q)); c.set_line_width(5); c.stroke()
    else:
        c.save()
        c.move_to(x0 + 60, 805); c.curve_to(x0 + 20, 900, x0 - 30, 980, x0 - 60, H)
        c.line_to(x1 + 60, H); c.curve_to(x1 + 30, 980, x1 - 20, 900, x1 - 60, 805); c.close_path(); c.clip()
        c.rectangle(x0 - 100, GROUND - 25, x1 - x0 + 200, 300); c.set_source_rgba(*hexc('#4FC3F7', 0.75)); c.fill()
        c.restore()

def big_tree(c, cam, t):
    x = TREE_X - cam + 960
    if x < -500 or x > W + 500: return
    c.move_to(x - 55, GROUND - 40); c.curve_to(x - 40, 700, x - 45, 560, x - 30, 470)
    c.line_to(x + 30, 470); c.curve_to(x + 45, 560, x + 40, 700, x + 55, GROUND - 40); c.close_path()
    fill(c, hexc('#8D5524'), OUT, 6)
    c.set_line_cap(cairo.LINE_CAP_ROUND)
    c.move_to(x, 520); c.line_to(x - 90, 450); c.set_source_rgba(*OUT); c.set_line_width(30); c.stroke()
    c.move_to(x, 520); c.line_to(x - 90, 450); c.set_source_rgba(*hexc('#8D5524')); c.set_line_width(20); c.stroke()
    blobs = ((-170, 380, 120), (170, 380, 120), (0, 280, 170), (-100, 230, 120), (100, 230, 120))
    for (dx, y, r) in blobs: ellipse(c, x + dx, y, r, r); c.set_source_rgba(*OUT); c.set_line_width(12); c.stroke()
    for k, (dx, y, r) in enumerate(blobs):
        ellipse(c, x + dx, y, r, r); c.set_source_rgba(*hexc(['#43A047', '#43A047', '#4CAF50', '#388E3C', '#388E3C'][k])); c.fill()

def big_tree_front(c, cam, t):  # leaves in front of the stuck ball
    x = TREE_X - cam + 960
    if x < -500 or x > W + 500: return
    shake = 6 * math.sin(t * 30) if 54.5 < t < 55.4 else 0
    for (dx, y, r) in ((-150, 485, 45), (60, 480, 40)):
        ellipse(c, x + dx + shake, y, r, r * 0.7); fill(c, hexc('#66BB6A'), OUT, 5)

def pond(c, cam, t, front=False):
    x = POND[0] - cam + 960
    if x < -600 or x > W + 600: return
    if not front:
        ellipse(c, x, GROUND + 25, POND[1], 60); fill(c, hexc('#4FC3F7'), hexc('#0277BD'), 6)
        for (dx, s) in ((-250, 1), (240, 0.8)):
            ellipse(c, x + dx, GROUND + 15, 50 * s, 16 * s); fill(c, hexc('#66BB6A'), OUT, 3)
        for k in range(3):
            q = (t * 0.6 + k / 3) % 1
            ellipse(c, x, GROUND + 15, 50 + 120 * q, 10 + 18 * q); c.set_source_rgba(1, 1, 1, 0.6 * (1 - q)); c.set_line_width(4); c.stroke()
    else:
        c.save(); ellipse(c, x, GROUND + 25, POND[1], 60); c.clip()
        c.rectangle(x - POND[1], GROUND + 18, 2 * POND[1], 120); c.set_source_rgba(*hexc('#4FC3F7', 0.85)); c.fill()
        c.restore()

def party(t): return t < 1.2 or 101.7 < t < 108

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
    stream(c, cam, t); pond(c, cam, t); big_tree(c, cam, t)
    bw = ball_world(t)
    if bw and 9 <= t < 55.2:
        ball(c, bw[0] - cam + 960, bw[1], 0)
    big_tree_front(c, cam, t)
    bounce = lambda ph: -25 * abs(math.sin(t * 4.5 + ph)) if party(t) else 0
    # Pipa
    sx = x_of('pipa', t) - cam + 960
    neck = kf(t, [(51, 300), (52.5, 410), (56, 410), (57.5, 300)])
    lean = kf(t, [(51, 0), (52.5, 450), (56, 450), (57.5, 0)])
    if 54.5 < t < 55.3: lean += 25 * math.sin((t - 54.5) * 20)
    pl = (1, -1) if 46 < t < 56 else (1, 0)
    K.put(c, K.pipa, sx, GROUND + bounce(0.5), 0.55, t=t, neck=neck, lean=lean, look=pl, walk=t * 8 if walking('pipa', t) else 0)
    # Tito
    sx = x_of('tito', t) - cam + 960
    reach = 260 if 5.8 < t < 6.8 else None
    if 76.5 < t < 80: reach = kf(t, [(76.5, 150), (77.3, 330), (79.5, 330), (80, 150)])
    tl = (1, 0.4) if 76 < t < 80 else (1, 0)
    K.put(c, K.tito, sx, GROUND + bounce(1.0), 0.6, t=t, look=tl, reach=reach, walk=t * 7 if walking('tito', t) else 0)
    if 78.4 < t < 79.4:  # big water jet
        q = (t - 78.4) / 1.0
        tip = sx + 0.6 * 330
        for k in range(16):
            u = (q * 1.4 - k * 0.05)
            if 0 < u < 1:
                ellipse(c, tip + 40 * k * 0.2 + 30 * math.sin(k), GROUND - 40 - 420 * u + 120 * u * u, 12, 16)
                c.set_source_rgba(*hexc('#81D4FA', 1 - u * 0.6)); c.fill()
    # Tomi
    sx = x_of('tomi', t) - cam + 960
    stream(c, cam, t, front=True)
    K.put(c, K.tomi, sx, GROUND + bounce(1.5) + (12 if tomi_hide(t) > 0.5 else 0), 0.55, t=t, look=(1, 0),
          walk=t * 4 if walking('tomi', t) else 0, hide=tomi_hide(t))
    if tomi_hide(t) > 0.5:  # little ripples around the shell
        for k in range(2):
            q = (t * 0.8 + k / 2) % 1
            ellipse(c, sx, GROUND + 5, 120 + 60 * q, 14 + 6 * q); c.set_source_rgba(1, 1, 1, 0.7 * (1 - q)); c.set_line_width(4); c.stroke()
    # Coco
    sx = x_of('coco', t) - cam + 960
    mood, look = 'smile', (1, 0)
    arm_r, arm_l = math.radians(65 + 6 * math.sin(t * 2)), math.radians(115 - 6 * math.sin(t * 2))
    if party(t): arm_r, arm_l = math.radians(-58 + 25 * math.sin(t * 9)), math.radians(-122 - 25 * math.sin(t * 9))
    if 6.8 < t < 11: mood = 'o'; look = (1, -0.6)
    if 46 < t < 51: look = (1, -1); mood = 'o' if t < 48 else 'smile'
    if 48 < t < 50: arm_r, arm_l = math.radians(-70), math.radians(-110)
    if 70 < t < 76: mood = 'o'; look = (1, 0.4)
    held = (bw is not None and abs(bw[0] - holder_point('coco', t)[0]) < 5 and abs(bw[1] - holder_point('coco', t)[1]) < 5)
    if held or 80 < t < 84: arm_r, arm_l = math.radians(-70), math.radians(-110)
    cy = GROUND + bounce(0) - coco_hop(t) - (115 if 29.9 < t < 30.6 else 0)
    blink = 0.0
    for bt in (3.0, 15.0, 35.0, 44.0, 62.0, 75.0, 88.0, 100.0):
        if abs(t - bt) < 0.12: blink = 1 - abs(t - bt) / 0.12
    K.put(c, K.coco, sx, cy, 0.55, t=t, mood=mood, look=look, lid=blink, arm_r=arm_r, arm_l=arm_l,
          walk=t * 9 if walking('coco', t) and coco_hop(t) == 0 else 0)
    pond(c, cam, t, front=True)
    # ball in play (in front)
    if bw and not (9 <= t < 55.2):
        ball(c, bw[0] - cam + 960, bw[1], t * 5)
    if 55.2 <= t < 55.6:
        for k in range(6):
            a = k * math.pi / 3; q = (t - 55.2) / 0.4
            ellipse(c, BALL_TREE[0] - cam + 960 + 80 * q * math.cos(a), BALL_TREE[1] + 60 * q * math.sin(a), 14, 7)
            c.set_source_rgba(*hexc('#43A047', 1 - q)); c.fill()
    # sparkles when the ball comes back
    q = (t - 80.4) / 1.0
    if 0 <= q <= 1:
        hx, hy = holder_point('coco', t)
        for k in range(8):
            a = k * math.pi / 4
            sparkle(c, hx - cam + 960 + 120 * q * math.cos(a), hy + 90 * q * math.sin(a), 26 * math.sin(math.pi * q))
    # Lola
    lwx, ly = lola_world(t)
    lx_ = lwx - cam + 960
    K.put(c, K.lola, lx_, ly + bounce(2.0), 0.5, t=t, flap=20, look=(1, 0.5))
    if 101.7 < t < 108:
        for k in range(3):
            ph = (t * 0.7 + k / 3) % 1
            music_note(c, lx_ + 40 + 60 * ph, ly - 150 - 160 * ph, math.sin(math.pi * ph), ['#E91E63', '#1E88E5', '#FF9800'][k])
    flowers_front(c, cam); fg_bushes(c, cam)
    cx_ = x_of('coco', t) - cam + 960
    bubble(c, cx_, GROUND - 300, '¡Mi pelota!', (t - 7.5) / 2.5, 52)
    bubble(c, cx_, GROUND - 300, '¡Un arroyo!', (t - 22.3) / 2.4, 52)
    bubble(c, x_of('tomi', t) - cam + 960, GROUND - 170, '¡Salten sobre mí!', (t - 27.7) / 2.0, 44)
    bubble(c, cx_, GROUND - 300, '¡Está en el árbol!', (t - 46.3) / 2.6, 46)
    bubble(c, lx_, ly - 120, '¡Allá está!', (t - 62.2) / 2.6, 52)
    bubble(c, cx_, GROUND - 300, '¡Gracias, Tito!', (t - 80.6) / 2.6, 48)

def overlay(c, t):
    if t < 5.6:
        a = 1 - ss(4.8, 5.5, t)
        c.push_group(); word(c, 'La pelota perdida', W / 2, 230, 120 * K_back((t - 0.6) / 0.6) + 0.01, tilt=0.05, outline=9)
        c.pop_group_to_source(); c.paint_with_alpha(a)
    if t > 102:
        s = K_back((t - 102) / 0.7)
        word(c, '¡Jugar juntos es', W / 2, 180, 110 * s + 0.01, tilt=0.06, outline=10)
        word(c, 'más divertido!', W / 2, 320, 115 * s + 0.01, start=3, tilt=0.06, outline=10)
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
            c.save(); full(c, t); c.restore(); surf.write_to_png(f'ep11_{t}.png')
    else:
        t0, t1 = (float(args[1]), float(args[2])) if args and args[0] == 'range' else (0, DUR)
        out = sys.stdout.buffer
        for i in range(int(round(t0 * FPS)), int(round(t1 * FPS))):
            c.save(); full(c, i / FPS); c.restore(); surf.flush(); out.write(surf.get_data())
