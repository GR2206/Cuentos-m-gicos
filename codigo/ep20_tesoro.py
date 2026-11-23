"""Episodio 20 — El tesoro del bosque (105 s). Aventurita de día.
Coco encuentra un mapa del tesoro. Siguen las pistas: la piedra con forma de corazón, el árbol más alto
(Pipa baja la llave con su cuello largo) y la X, donde cavan Tito y Coco. En el cofre hay frutas...
¡y el mejor tesoro es compartirlas con los amigos en un picnic!

Uso:  python3 ep20_tesoro.py              -> cuadros crudos por stdout
      python3 ep20_tesoro.py range 0 52   -> solo un tramo
      python3 ep20_tesoro.py stills 20 70 -> PNG sueltos
      python3 ep20_tesoro.py srt 5.5      -> subtítulos .srt de la narración"""
import cairo, math, random, sys
import cuerpos as K
from amigos import hexc, ellipse, fill, OUT
from logos import word, sparkle
from ep02_puente_del_rio import kf, ss, K_back, music_note
from ep03_donde_esta_tomi import bubble
from ep09_semilla_magica import srt, fruit
from ep14_bananas_papa import heart
from ep10_cruzando_el_bosque import far_hills, back_trees, ground, path_trees, flowers_front, fg_bushes

W, H, FPS = 1920, 1080, 30
DUR = 105.0
GROUND = 880
ROCK = 2950
TREE = 4980
XSPOT = 6680
BK = [(0, 1000), (15.0, 1000), (25.0, 2600), (35.0, 2600), (45.0, 4600), (55.0, 4600), (63.0, 6400), (105, 6400)]
FORM = {'coco': 0, 'tomi': -230, 'tito': -480, 'pipa': -760}
KEY = (TREE - 60, 300)

NARRACION = [
    (6.0, 13.0, 'Un día, Coco encontró algo escondido entre las hojas... ¡un mapa del tesoro!'),
    (16.0, 24.0, 'Primera pista: la piedra con forma de corazón.'),
    (26.0, 34.0, '¡Ahí está! Y tiene una flecha que señala el camino.'),
    (36.0, 44.0, 'Segunda pista: el árbol más alto del bosque. Allá arriba brillaba algo...'),
    (45.0, 54.0, 'Pipa estiró su cuello larguísimo... ¡y bajó una llave dorada!'),
    (56.0, 63.0, 'Y la última pista: la X.'),
    (64.0, 71.0, 'Tito y Coco cavaron, cavaron... ¡y apareció un cofre!'),
    (72.0, 79.0, 'Coco lo abrió con la llave y... ¡estaba lleno de frutas!'),
    (81.0, 92.0, 'Entonces hicieron un picnic y compartieron todo. Porque el mejor tesoro... es tener amigos.'),
    (96.0, 103.0, '¡Compartir es el mejor tesoro!'),
]

def B(t): return kf(t, BK)

PIC = {'pipa': 6060, 'tito': 6250, 'coco': 6450, 'tomi': 6900}
def x_of(name, t):
    base = B(t) + FORM[name]
    if name == 'pipa' and 35.0 < t < 55.0:
        base = kf(t, [(35.0, 4600 - 760), (38.0, TREE - 160), (52.0, TREE - 160), (55.0, 4600 - 760)])
    if name == 'tito' and 63.0 < t < 72.0:
        base = kf(t, [(63.0, 6400 - 480), (64.5, XSPOT - 300), (72.0, XSPOT - 300)])
    if name == 'coco' and 63.0 < t < 72.0:
        base = kf(t, [(63.0, 6400), (64.5, XSPOT + 170), (72.0, XSPOT + 170)])
    if t >= 72.0:
        prev = {'pipa': 6400 - 760, 'tito': XSPOT - 300, 'coco': XSPOT + 170, 'tomi': 6400 - 230}[name]
        base = kf(t, [(79.5, prev), (82.0, PIC[name])])
    return base

def walking(name, t): return abs(x_of(name, t + 0.05) - x_of(name, t)) > 1.0

# ---------------- objetos ----------------
def heart_rock(c, sx, t):
    y = GROUND + 10
    c.save(); c.translate(sx, y - 110)
    c.move_to(0, 110); c.curve_to(-170, 30, -150, -110, -70, -110); c.curve_to(-30, -110, 0, -80, 0, -55)
    c.curve_to(0, -80, 30, -110, 70, -110); c.curve_to(150, -110, 170, 30, 0, 110); c.close_path()
    fill(c, hexc('#B0BEC5'), OUT, 6)
    ellipse(c, -60, -50, 30, 16); c.set_source_rgba(1, 1, 1, 0.35); c.fill()
    a = ss(26.5, 27.5, t)
    if a > 0:   # flecha pintada
        c.move_to(-60, 10); c.line_to(30, 10); c.line_to(30, -15); c.line_to(80, 25); c.line_to(30, 65); c.line_to(30, 40); c.line_to(-60, 40); c.close_path()
        fill(c, hexc('#FF7043', a), OUT, 4)
    c.restore()

def tall_tree(c, sx, t):
    c.move_to(sx - 50, GROUND); c.curve_to(sx - 35, 600, sx - 40, 300, sx - 30, 120)
    c.line_to(sx + 30, 120); c.curve_to(sx + 40, 300, sx + 35, 600, sx + 50, GROUND); c.close_path()
    fill(c, hexc('#8D5524'), OUT, 6)
    c.move_to(sx - 20, 260); c.curve_to(sx - 60, 240, sx - 90, 240, sx - 120, 225)
    c.set_source_rgba(*OUT); c.set_line_width(22); c.stroke_preserve(); c.set_source_rgba(*hexc('#8D5524')); c.set_line_width(12); c.stroke()
    blobs = ((-140, 110, 120), (140, 110, 120), (0, 30, 150), (0, 160, 110))
    for (dx, dy, r) in blobs: ellipse(c, sx + dx, dy, r, r); c.set_source_rgba(*OUT); c.set_line_width(10); c.stroke()
    for j, (dx, dy, r) in enumerate(blobs):
        ellipse(c, sx + dx, dy, r, r); c.set_source_rgba(*hexc(['#43A047', '#43A047', '#4CAF50', '#388E3C'][j])); c.fill()

def key(c, x, y, s, t):
    c.save(); c.translate(x, y); c.scale(s, s); c.rotate(0.3 * math.sin(t * 2))
    ellipse(c, 0, 0, 22, 22); fill(c, hexc('#FFD600'), OUT, 5)
    ellipse(c, 0, 0, 9, 9); c.set_source_rgba(*hexc('#8D6E63')); c.fill()
    c.rectangle(-6, 18, 12, 55); fill(c, hexc('#FFD600'), OUT, 4)
    for dy in (50, 64): c.rectangle(6, dy, 16, 8); fill(c, hexc('#FFD600'), OUT, 3)
    c.restore()
    sparkle(c, x + 30 * s, y - 25 * s, 12 * s * (0.6 + 0.4 * math.sin(t * 6)), '#FFFFFF')

def key_pos(t, pipa_head, coco_hand):
    if t < 49.0: return KEY[0], KEY[1] + 8 * math.sin(t * 2), 1.0
    if t < 66.0: return pipa_head[0] + 20, pipa_head[1] + 55, 0.9          # en la boca de Pipa
    if t < 68.5:
        q = ss(66.0, 67.0, t); return pipa_head[0] + (coco_hand[0] - pipa_head[0]) * q, pipa_head[1] + (coco_hand[1] - pipa_head[1]) * q, 0.8
    return None

def x_mark(c, sx, t):
    a = 1 - ss(64.5, 66.0, t)
    if a <= 0: return
    for d in (-1, 1):
        c.move_to(sx - 60, GROUND + 15 - 30 * d); c.line_to(sx + 60, GROUND + 15 + 30 * d)
        c.set_source_rgba(*OUT, ) if False else None
        c.set_source_rgba(*hexc('#3B2314', a)); c.set_line_width(26); c.stroke_preserve()
        c.set_source_rgba(*hexc('#E53935', a)); c.set_line_width(16); c.stroke()

def chest(c, sx, t):
    up = ss(67.0, 68.5, t)
    if up <= 0: return
    hole = ss(64.5, 67.0, t)
    y = GROUND + 30 + 120 * (1 - up)
    c.save(); c.rectangle(sx - 200, 0, 400, GROUND + 40); c.clip()
    c.save(); c.translate(sx, y)
    c.rectangle(-110, -110, 220, 110); fill(c, hexc('#8D5524'), OUT, 6)
    for dx in (-80, 80): c.rectangle(dx - 12, -110, 24, 110); fill(c, hexc('#FFC107'), OUT, 4)
    opened = ss(71.0, 72.0, t)
    c.save(); c.translate(-110, -110); c.rotate(-1.9 * opened)
    c.move_to(0, 0); c.line_to(0, -40); c.curve_to(0, -90, 220, -90, 220, -40); c.line_to(220, 0); c.close_path(); fill(c, hexc('#A1662F'), OUT, 6)
    c.restore()
    if opened < 0.5:
        c.rectangle(-18, -40, 36, 36); fill(c, hexc('#FFC107'), OUT, 4)
    c.restore(); c.restore()
    if opened > 0:   # rayos
        a = opened * (1 - ss(77.0, 79.0, t))
        for k in range(9):
            ang = -math.pi / 2 + (k - 4) * 0.22 + 0.04 * math.sin(t * 2 + k)
            c.move_to(sx, GROUND - 90); c.line_to(sx + 600 * math.cos(ang - 0.04), GROUND - 90 + 600 * math.sin(ang - 0.04))
            c.line_to(sx + 600 * math.cos(ang + 0.04), GROUND - 90 + 600 * math.sin(ang + 0.04)); c.close_path()
            c.set_source_rgba(1, 0.92, 0.4, 0.35 * a); c.fill()

FRUITS = [('banana', 6380), ('#E53935', 6440), ('#FF9800', 6500), ('#8E24AA', 6560), ('bunch', 6620), ('#43A047', 6340)]
def fruits(c, cam, t):
    for k, (kind, wx) in enumerate(FRUITS):
        t0 = 72.3 + 0.35 * k
        if t < t0: continue
        q = ss(t0, t0 + 0.8, t)
        x0, y0 = XSPOT - cam + 960, GROUND - 120
        x1, y1 = wx - cam + 960, GROUND + 40
        x = x0 + (x1 - x0) * q; y = y0 + (y1 - y0) * q - 260 * math.sin(math.pi * q)
        if t > 84.0 + k * 0.6 and kind not in ('bunch',): continue   # se las comen
        if kind == 'banana': K.banana(c, x, y, 2.2, -0.4)
        elif kind == 'bunch': K.bunch(c, x, y, 1.6)
        else: fruit(c, x, y, kind, 1.3)

def blanket(c, cam, t):
    a = ss(76.0, 77.0, t)
    if a <= 0: return
    x = 6480 - cam + 960
    c.save(); c.translate(x, GROUND + 45); c.scale(1, 0.25 * a)
    ellipse(c, 0, 0, 330, 160); fill(c, hexc('#E53935'), OUT, 12)
    c.save(); ellipse(c, 0, 0, 330, 160); c.clip()
    for k in range(-6, 7):
        c.rectangle(k * 60, -200, 30, 400); c.set_source_rgba(1, 1, 1, 0.55); c.fill()
    c.restore(); c.restore()

def treasure_map(c, x, y, s, t, progress, a=1.0):
    """mapito con la ruta: piedra-corazón, árbol alto y X. progress 0..1 = dónde están."""
    if a <= 0 or s <= 0.01: return
    c.push_group()
    c.save(); c.translate(x, y); c.scale(s, s)
    c.move_to(-300, -170); c.line_to(300, -175); c.line_to(305, 170); c.line_to(-298, 175); c.close_path()
    fill(c, hexc('#FFE0B2'), OUT, 7)
    for d in (-1, 1):
        ellipse(c, d * 300, 0, 22, 175); fill(c, hexc('#FFCC80'), OUT, 6)
    pts = [(-240, 110), (-120, 40), (-40, 90), (60, -10), (140, -80), (240, -40)]
    c.move_to(*pts[0])
    for p in pts[1:]: c.line_to(*p)
    c.set_dash([14, 12]); c.set_source_rgba(*hexc('#8D6E63')); c.set_line_width(7); c.stroke(); c.set_dash([])
    c.save(); c.translate(-120, 30); c.scale(0.28, 0.28)
    c.move_to(0, 110); c.curve_to(-170, 30, -150, -110, -70, -110); c.curve_to(-30, -110, 0, -80, 0, -55)
    c.curve_to(0, -80, 30, -110, 70, -110); c.curve_to(150, -110, 170, 30, 0, 110); c.close_path(); fill(c, hexc('#B0BEC5'), OUT, 14); c.restore()
    c.rectangle(52, -60, 16, 50); fill(c, hexc('#8D5524'), OUT, 4)
    ellipse(c, 60, -85, 38, 38); fill(c, hexc('#43A047'), OUT, 5)
    for d in (-1, 1):
        c.move_to(240 - 26, -40 - 26 * d); c.line_to(240 + 26, -40 + 26 * d); c.set_source_rgba(*hexc('#E53935')); c.set_line_width(12); c.stroke()
    # puntito "estamos acá"
    seg = progress * (len(pts) - 1); i = min(int(seg), len(pts) - 2); f = seg - i
    px = pts[i][0] + (pts[i + 1][0] - pts[i][0]) * f; py = pts[i][1] + (pts[i + 1][1] - pts[i][1]) * f
    ellipse(c, px, py, 20 + 4 * math.sin(t * 6), 20 + 4 * math.sin(t * 6)); fill(c, hexc('#A0582C'), OUT, 5)
    c.restore()
    c.pop_group_to_source(); c.paint_with_alpha(a)

def progress(t):
    return kf(t, [(0, 0.0), (15.0, 0.0), (25.0, 0.2), (35.0, 0.2), (45.0, 0.6), (55.0, 0.6), (63.0, 1.0)])

# ---------------- cuadro ----------------
def frame(c, t):
    cam = B(t)
    g = cairo.LinearGradient(0, 0, 0, H)
    for k, col in enumerate(('#29B6F6', '#81D4FA', '#B3E5FC')): g.add_color_stop_rgb(k / 2, *hexc(col)[:3])
    c.set_source(g); c.paint()
    for (x0, y0, s, sp) in ((150, 150, 0.9, 12), (820, 100, 0.7, 8), (1450, 200, 0.6, 15)):
        c.save(); c.translate((x0 - cam * 0.05 + sp * t) % 2300 - 250, y0); c.scale(s, s)
        for (cx, cy, r) in ((0, 0, 60), (70, -30, 75), (150, 0, 60), (75, 20, 60)): ellipse(c, cx, cy, r, r)
        c.set_source_rgba(1, 1, 1, 1); c.fill(); c.restore()
    far_hills(c, cam); back_trees(c, cam); ground(c, cam); path_trees(c, cam)
    heart_rock(c, ROCK - cam + 960, t)
    tall_tree(c, TREE - cam + 960, t)
    x_mark(c, XSPOT - cam + 960, t)
    if 64.5 < t:   # pozo
        hq = ss(64.5, 67.0, t) * (1 - ss(78.0, 79.0, t))
        ellipse(c, XSPOT - cam + 960, GROUND + 30, 150 * hq + 0.1, 30 * hq + 0.1); fill(c, hexc('#5D4037'), OUT, 5)
    chest(c, XSPOT - cam + 960, t)
    blanket(c, cam, t)
    party = t > 84.0
    bob = lambda ph: -18 * abs(math.sin(t * 4.5 + ph)) if t > 95.0 else 0
    # Pipa
    px = x_of('pipa', t) - cam + 960
    neck = kf(t, [(44.5, 300), (47.0, 760), (49.5, 760), (52.0, 300)])
    lean = kf(t, [(44.5, 0), (47.0, 120), (49.5, 120), (52.0, 0)])
    hx, hy = px + 0.55 * lean, GROUND - 0.55 * (260 + neck)
    K.put(c, K.pipa, px, GROUND + bob(0.5), 0.55, t=t, neck=neck, lean=lean, look=(1, -0.8) if 38 < t < 50 else (1, 0),
          walk=t * 7 if walking('pipa', t) else 0, hold='banana' if t > 84.6 else None)
    # Tito
    tx = x_of('tito', t) - cam + 960
    dig = 64.5 < t < 67.0
    reach = 150 + 110 * abs(math.sin(t * 7)) if dig else None
    K.put(c, K.tito, tx, GROUND + bob(1.0), 0.6, t=t, look=(1, 0.5) if dig else (1, 0), reach=reach,
          walk=t * 6 if walking('tito', t) else 0, hold='banana' if t > 85.2 else None)
    # Tomi
    tmx = x_of('tomi', t) - cam + 960
    K.put(c, K.tomi, tmx, GROUND + bob(1.5), 0.55, t=t, look=(-1 if t > 82 else 1, 0), walk=t * 3 if walking('tomi', t) else 0,
          hold='banana' if t > 85.8 else None)
    # Coco
    cx = x_of('coco', t) - cam + 960
    mood, look = 'smile', (1, -0.2)
    ar, al = math.radians(65 + 6 * math.sin(t * 2)), math.radians(115 - 6 * math.sin(t * 2))
    if 6.5 < t < 10.0: mood = 'o'; ar = math.radians(-20); look = (1, 0.2)
    if 10.0 < t < 15.0: ar, al = math.radians(-60), math.radians(-120)
    if 26.0 < t < 28.5 or 49.5 < t < 52.0 or 71.0 < t < 74.0: ar, al = math.radians(-60), math.radians(-120); mood = 'o'
    if dig: ar = al = math.radians(30 + 40 * math.sin(t * 9)); look = (1, 0.6)
    if 66.0 < t < 71.0: ar = math.radians(-15); look = (1, 0.4)
    hold = None
    if t > 84.0: hold = 'banana'; mood = 'chew' if (t % 1.2) > 0.6 and t < 95 else 'smile'
    if t > 95.0: ar, al = math.radians(-58 + 25 * math.sin(t * 9)), math.radians(-122 - 25 * math.sin(t * 9))
    cflip = 63.5 < t < 79.5
    if cflip: look = (1, look[1])
    K.put(c, K.coco, cx, GROUND + bob(0), 0.55, flip=cflip, t=t, mood=mood, look=look, arm_r=ar, arm_l=al,
          walk=t * 8 if walking('coco', t) else 0, hold=hold, chew=t)
    if dig:   # tierra volando
        for k in range(10):
            ph = (t * 1.5 + k / 10) % 1
            sx = XSPOT - cam + 960 + (-1 if k % 2 else 1) * (40 + 260 * ph); sy = GROUND - 330 * ph * (1 - ph) * 2
            ellipse(c, sx, sy, 11, 9); fill(c, hexc('#6D4C41'), OUT, 2)
    # mapa en la mano de Coco al principio
    if 5.5 < t < 14.5:
        mq = K_back((t - 6.3) / 0.5) * (1 - ss(13.8, 14.5, t))
        treasure_map(c, cx + 75, GROUND - 210, 0.18 * mq, t, 0.0)
    # llave
    kp = key_pos(t, (hx, hy), (cx - 60, GROUND - 200))
    if kp: key(c, kp[0], kp[1], kp[2], t)
    fruits(c, cam, t)
    # Lola
    lox = x_of('coco', t) - 170 - cam + 960 + (0 if t < 80 else 60 * math.sin(t * 0.7)); loy = 430 + 20 * math.sin(t * 3)
    K.put(c, K.lola, lox, loy + bob(2.0), 0.5, t=t, flap=20, look=(1, 0.3), hold='banana' if t > 86.4 else None)
    fg_bushes(c, cam); flowers_front(c, cam)
    if t > 84.0:
        for k in range(3):
            ph = (t * 0.7 + k / 3) % 1
            music_note(c, lox + 40 + 60 * ph, loy - 150 - 160 * ph, math.sin(math.pi * ph), ['#E91E63', '#1E88E5', '#FFD600'][k])
        for k in range(4):
            ph = ((t - 84.0) * 0.4 + k / 4) % 1
            heart(c, 700 + 180 * k, 520 - 200 * ph, 0.9, math.sin(math.pi * ph))
    # globitos
    bubble(c, cx, GROUND - 330, '¡Un mapa del tesoro!', (t - 8.0) / 4.0, 46)
    bubble(c, tmx, GROUND - 250, '¡Vamos!', (t - 12.0) / 2.6, 52)
    bubble(c, cx, GROUND - 300, '¡La piedra corazón!', (t - 25.6) / 3.4, 46)
    bubble(c, hx, hy - 120, '¡Una llave!', (t - 46.8) / 3.0, 50)
    bubble(c, tmx, GROUND - 250, '¡La X está acá!', (t - 62.0) / 3.0, 48)
    bubble(c, cx, GROUND - 300, '¡Frutas!', (t - 73.0) / 2.6, 56)
    bubble(c, cx, GROUND - 300, '¡Compartimos!', (t - 79.5) / 3.0, 50)
    return cx

def overlay(c, t):
    if t < 5.6:
        a = 1 - ss(4.8, 5.5, t)
        c.push_group(); word(c, 'El tesoro del bosque', W / 2, 230, 125 * K_back((t - 0.6) / 0.6) + 0.01, tilt=0.05, outline=9)
        c.pop_group_to_source(); c.paint_with_alpha(a)
    if 9.0 < t < 14.5:   # mapa grande
        s = K_back((t - 9.0) / 0.5) * (1 - ss(14.0, 14.5, t))
        treasure_map(c, W / 2, 330, 1.0 * s, t, 0.0)
    if 15.0 < t < 64.0:  # mapita en la esquina
        a = ss(15.0, 15.6, t) * (1 - ss(63.4, 64.0, t))
        treasure_map(c, 1680, 140, 0.36, t, progress(t), a)
    if 88.0 < t < 94.5:
        s = K_back((t - 88.0) / 0.5) * (1 - ss(94.0, 94.5, t))
        word(c, 'El mejor tesoro:', W / 2, 160, 100 * s + 0.01, tilt=0.04, outline=9)
        word(c, '¡los amigos!', W / 2, 280, 110 * s + 0.01, start=3, tilt=0.04, outline=9)
    if t > 95.5:
        s = K_back((t - 95.5) / 0.7)
        word(c, '¡Compartir es', W / 2, 160, 110 * s + 0.01, tilt=0.05, outline=10)
        word(c, 'el mejor tesoro!', W / 2, 285, 110 * s + 0.01, start=4, tilt=0.05, outline=10)
    a = max(1 - ss(0, 0.8, t), ss(DUR - 2.0, DUR, t))
    if a > 0: c.set_source_rgba(1, 1, 1, a); c.paint()

if __name__ == '__main__':
    args = sys.argv[1:]
    if args and args[0] == 'srt':
        print(srt(NARRACION, float(args[1]) if len(args) > 1 else 0.0)); sys.exit()
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(surf)
    def full(c, t): frame(c, t); overlay(c, t)
    if args and args[0] == 'stills':
        for t in map(float, args[1:]):
            c.save(); full(c, t); c.restore(); surf.write_to_png(f'ep20_{t}.png')
    else:
        t0, t1 = (float(args[1]), float(args[2])) if args and args[0] == 'range' else (0, DUR)
        out = sys.stdout.buffer
        for i in range(int(round(t0 * FPS)), int(round(t1 * FPS))):
            c.save(); full(c, i / FPS); c.restore(); surf.flush(); out.write(surf.get_data())
