"""Episodio 27 — El desayuno de los amigos (100 s). Para la mañana (narrar con la voz de Malena).
Amanece en la selva y Lola despierta a todos cantando. Se estiran, Tito los moja jugando para lavarse
la carita, y cada uno trae una fruta: Pipa baja mangos del árbol más alto, Tomi trae frutillas,
Lola un racimo de uvas y Coco bananas. Arman juntos una gran ensalada de frutas y desayunan.

Uso:  python3 ep27_desayuno.py              -> cuadros crudos por stdout
      python3 ep27_desayuno.py range 0 50   -> solo un tramo
      python3 ep27_desayuno.py stills 20 70 -> PNG sueltos
      python3 ep27_desayuno.py srt 5.5      -> subtítulos .srt de la narración"""
import cairo, math, sys
import cuerpos as K
from amigos import hexc, ellipse, fill, OUT
from logos import word, sparkle
from ep02_puente_del_rio import kf, ss, K_back, music_note
from ep03_donde_esta_tomi import bubble
from ep09_semilla_magica import LAND, cloud, srt, fruit
from ep14_bananas_papa import heart
from ep20_tesoro import tall_tree

W, H, FPS = 1920, 1080, 30
DUR = 100.0
GROUND = 880
TREE = 1730
BOWL = (930, GROUND + 40)
CLOTH = (930, GROUND + 50)

NARRACION = [
    (6.0, 12.5, 'El sol empezó a salir en la selva. Todos dormían... hasta que Lola cantó: ¡buen día!'),
    (14.0, 21.5, 'Uno por uno se despertaron. Coco se estiró, Tito bostezó y Tomi salió de su caparazón.'),
    (23.0, 31.0, 'Tito llenó su trompa de agua y ¡fshhh! Los mojó a todos para lavarse la carita.'),
    (32.5, 39.5, 'Coco tuvo una idea: ¡hagamos un desayuno todos juntos! Cada uno trae una fruta.'),
    (41.0, 48.5, 'Pipa estiró su cuello larguísimo y bajó unos mangos del árbol más alto.'),
    (50.0, 57.0, 'Tomi llegó despacito con frutillas, y Lola trajo un racimo de uvas.'),
    (58.0, 65.0, 'Y Coco, por supuesto, ¡trajo bananas!'),
    (67.0, 76.0, 'Pusieron todo en un bol grande, mezclaron... ¡y armaron una ensalada de frutas!'),
    (78.0, 89.0, 'Y desayunaron todos juntos. ¡Qué rico empezar el día con amigos!'),
    (93.0, 99.0, '¡Buen día, amigos!'),
]

# ---------------- cielo del amanecer ----------------
def dawn(t): return ss(0.0, 18.0, t)
def sky(c, t):
    d = dawn(t)
    night = [('#1A1A4E', 0), ('#3E2A6E', 0.6), ('#7A4B8C', 1)]
    rise = [('#FF8A65', 0), ('#FFCC80', 0.55), ('#FFF3E0', 1)]
    day = [('#29B6F6', 0), ('#81D4FA', 0.6), ('#B3E5FC', 1)]
    def lerp(a, b, q):
        A, Bc = hexc(a), hexc(b); return [A[i] + (Bc[i] - A[i]) * q for i in range(3)]
    g = cairo.LinearGradient(0, 0, 0, H)
    for k in range(3):
        if d < 0.5: col = lerp(night[k][0], rise[k][0], d / 0.5)
        else: col = lerp(rise[k][0], day[k][0], (d - 0.5) / 0.5)
        g.add_color_stop_rgb(night[k][1], *col)
    c.set_source(g); c.paint()
    if d < 0.6:   # estrellitas que se apagan
        for k in range(30):
            ellipse(c, (k * 197) % 1900, 30 + (k * 83) % 380, 2.5, 2.5); c.set_source_rgba(1, 1, 0.85, (1 - d / 0.6) * (0.5 + 0.5 * math.sin(t * 2 + k))); c.fill()
    sy = kf(t, [(0, 820), (16.0, 300), (40.0, 170)])
    sx = 360
    g2 = cairo.RadialGradient(sx, sy, 20, sx, sy, 420)
    g2.add_color_stop_rgba(0, 1, 0.9, 0.5, 0.6); g2.add_color_stop_rgba(1, 1, 0.8, 0.4, 0)
    c.set_source(g2); c.arc(sx, sy, 420, 0, 2 * math.pi); c.fill()
    c.save(); c.translate(sx, sy)
    for k in range(12):
        a = k * math.pi / 6 + t * 0.2
        c.move_to(105 * math.cos(a), 105 * math.sin(a)); c.line_to(150 * math.cos(a), 150 * math.sin(a))
        c.set_source_rgba(*hexc('#FFB300')); c.set_line_width(12); c.set_line_cap(cairo.LINE_CAP_ROUND); c.stroke()
    ellipse(c, 0, 0, 90, 90); fill(c, hexc('#FFD54F'), hexc('#F9A825'), 6)
    awake = ss(6.0, 8.0, t)
    c.set_source_rgba(*OUT); c.set_line_width(6)
    for ex in (-30, 30):
        if awake < 0.5: c.arc(ex, -8, 13, 0.15 * math.pi, 0.85 * math.pi); c.stroke()
        else: ellipse(c, ex, -12, 8, 11); c.fill()
    c.arc(0, 18, 26, 0.15 * math.pi, 0.85 * math.pi); c.stroke()
    for ex in (-55, 55): ellipse(c, ex, 15, 14, 8); c.set_source_rgba(*hexc('#FF8A80', 0.7)); c.fill()
    c.restore()
    for (x0, y0, s, sp) in ((700, 150, 0.8, 8), (1200, 110, 0.7, 6)):
        c.push_group(); cloud(c, (x0 + sp * t) % 2300 - 250, y0, s); c.pop_group_to_source(); c.paint_with_alpha(0.5 + 0.5 * d)

def zzz(c, x, y, t, a):
    if a <= 0: return
    for k in range(3):
        ph = (t * 0.4 + k / 3) % 1
        c.select_font_face('Fredoka Light', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        c.set_font_size(34 + 24 * ph); c.set_source_rgba(1, 1, 1, a * math.sin(math.pi * ph))
        c.move_to(x + 40 * ph, y - 120 * ph); c.show_text('z')

# ---------------- comida ----------------
def mango(c, x, y, s=1.0, rot=0.0):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    c.move_to(0, -34); c.curve_to(34, -34, 40, 20, 8, 34); c.curve_to(-26, 40, -34, -10, 0, -34); c.close_path()
    g = cairo.LinearGradient(-30, -30, 30, 30); g.add_color_stop_rgb(0, *hexc('#FFB300')[:3]); g.add_color_stop_rgb(1, *hexc('#FF7043')[:3])
    c.set_source(g); c.fill_preserve(); c.set_source_rgba(*OUT); c.set_line_width(4); c.stroke()
    c.move_to(2, -32); c.curve_to(16, -52, 34, -48, 36, -40); c.curve_to(22, -38, 12, -36, 2, -32); fill(c, hexc('#43A047'), OUT, 3)
    c.restore()

def strawberry(c, x, y, s=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.move_to(0, 26); c.curve_to(-28, 6, -24, -20, 0, -18); c.curve_to(24, -20, 28, 6, 0, 26); c.close_path(); fill(c, hexc('#E53935'), OUT, 3)
    for (dx, dy) in ((-8, -4), (6, -6), (-2, 8), (9, 6)): ellipse(c, dx, dy, 2, 3); c.set_source_rgba(1, 0.95, 0.6, 1); c.fill()
    for a in (-0.8, 0, 0.8):
        c.save(); c.translate(0, -18); c.rotate(a); ellipse(c, 0, -6, 6, 10); fill(c, hexc('#43A047'), OUT, 2); c.restore()
    c.restore()

def grapes(c, x, y, s=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    for r, row in enumerate((4, 3, 2, 1)):
        for i in range(row):
            ellipse(c, (i - (row - 1) / 2) * 22, r * 19, 12, 12); fill(c, hexc('#8E24AA'), OUT, 3)
    c.move_to(0, -10); c.line_to(4, -28); c.set_source_rgba(*hexc('#5D4037')); c.set_line_width(4); c.stroke()
    c.restore()

def cloth(c, t):
    a = ss(37.0, 38.5, t)
    if a <= 0: return
    c.save(); c.translate(*CLOTH); c.scale(a, 0.25 * a)
    ellipse(c, 0, 0, 520, 220); fill(c, hexc('#E53935'), OUT, 14)
    c.save(); ellipse(c, 0, 0, 520, 220); c.clip()
    for k in range(-9, 10):
        c.rectangle(k * 60, -260, 28, 520); c.set_source_rgba(1, 1, 1, 0.5); c.fill()
        c.rectangle(-560, k * 60, 1120, 28); c.set_source_rgba(1, 1, 1, 0.35); c.fill()
    c.restore(); c.restore()

def bowl(c, t, front):
    a = K_back((t - 66.5) / 0.6) if t > 66.5 else 0
    if a <= 0.01: return
    x, y = BOWL
    c.save(); c.translate(x, y); c.scale(a, a)
    if not front:
        ellipse(c, 0, -110, 150, 32); fill(c, hexc('#FFF3E0'), OUT, 6)
        full = ss(67.5, 74.0, t)
        if full > 0:
            for k in range(16):
                ang = k * 2.4 + (t - 70) * 2.5 * (1 if 71.5 < t < 75 else 0)
                r = 100 * math.sqrt((k + 0.5) / 16)
                fx, fy = r * math.cos(ang), -118 + 22 * math.sin(ang) - 8 * full
                if k / 16 > full: continue
                kind = k % 4
                if kind == 0: mango(c, fx, fy, 0.45, ang)
                elif kind == 1: strawberry(c, fx, fy, 0.65)
                elif kind == 2: ellipse(c, fx, fy, 11, 11); fill(c, hexc('#8E24AA'), OUT, 3)
                else: ellipse(c, fx, fy, 16, 10); fill(c, hexc('#FFF59D'), OUT, 3)
        return c.restore()
    c.move_to(-150, -110); c.curve_to(-140, 0, 140, 0, 150, -110); c.curve_to(100, -80, -100, -80, -150, -110); c.close_path()
    fill(c, hexc('#29B6F6'), OUT, 6)
    for k in range(5): ellipse(c, -100 + 50 * k, -55, 10, 10); c.set_source_rgba(1, 1, 1, 0.8); c.fill()
    c.restore()

def spoon(c, t):
    if not 71.5 < t < 75.5: return
    x, y = BOWL; a = (t - 71.5) * 6
    sx, sy = x + 60 * math.cos(a), y - 130 + 12 * math.sin(a)
    c.move_to(sx, sy); c.line_to(sx - 50, sy - 140); c.set_source_rgba(*OUT); c.set_line_width(16); c.stroke()
    c.move_to(sx, sy); c.line_to(sx - 50, sy - 140); c.set_source_rgba(*hexc('#BCAAA4')); c.set_line_width(9); c.stroke()

# frutas sobre el mantel: (tipo, x, y, aparece, entra al bol)
PILE = [('mango', 1190, GROUND + 30, 46.5, 67.6), ('mango', 1260, GROUND + 45, 47.3, 68.2),
        ('fresa', 1090, GROUND + 50, 52.5, 68.8), ('fresa', 1130, GROUND + 60, 52.7, 69.2),
        ('uvas', 700, GROUND + 15, 55.5, 69.8), ('banana', 790, GROUND + 50, 61.0, 70.4)]
def pile(c, t):
    for (kind, x, y, t0, t1) in PILE:
        if t < t0: continue
        if t < t1:
            s = K_back((t - t0) / 0.4); X, Y = x, y
        elif t < t1 + 0.7:
            q = (t - t1) / 0.7; s = 1 - 0.4 * q
            X = x + (BOWL[0] - x) * q; Y = y + (BOWL[1] - 120 - y) * q - 160 * math.sin(math.pi * q)
        else: continue
        if kind == 'mango': mango(c, X, Y, 1.3 * s)
        elif kind == 'fresa': strawberry(c, X, Y, 1.2 * s)
        elif kind == 'uvas': grapes(c, X, Y - 30, 1.1 * s)
        else: K.banana(c, X, Y, 2.0 * s, -0.3)

# ---------------- personajes ----------------
def aim(x, base, s, tx, ty, side=1):
    sx = x + 78 * side * s; sy = base - 180 * s
    dx, dy = tx - sx, ty - sy
    return math.atan2(dy, dx), max(90, math.hypot(dx, dy) / s)

PIPA_X = [(0, 1500), (41.5, 1500), (43.0, TREE - 330), (47.5, TREE - 330), (49.0, 1450)]
def pipa_neck(t): return kf(t, [(42.5, 300), (44.5, 700), (46.5, 700), (48.5, 300)])
def pipa_lean(t): return kf(t, [(42.5, 0), (44.5, 170), (46.5, 170), (48.5, 0)])
TOMI_X = [(0, 1150), (49.5, 1150), (50.0, 1950), (50.1, 1950), (53.0, 1180)]

def frame(c, t):
    sky(c, t)
    c.set_source_surface(LAND, 0, 0); c.paint()
    d = dawn(t)
    if d < 1: c.set_source_rgba(0.2, 0.1, 0.3, 0.45 * (1 - d)); c.mask_surface(LAND, 0, 0)
    tall_tree(c, TREE, t)
    for (mx, my) in ((TREE - 120, 160), (TREE + 60, 120), (TREE - 30, 210)):   # mangos en el árbol
        if t < 44.8 or (mx, my) == (TREE + 60, 120): mango(c, mx, my, 0.9)
    cloth(c, t)
    bowl(c, t, False)
    sleep = lambda t0: 1 - ss(t0, t0 + 1.2, t)
    eat = 78.0 < t < 90.0
    party = t > 91.0
    bob = lambda ph: -16 * abs(math.sin(t * 4.5 + ph)) if party else 0
    wet = 26.0 < t < 31.5
    # Pipa
    px = kf(t, PIPA_X)
    lk = (1, -0.9) if 43 < t < 47 else (-1, 0.3)
    K.put(c, K.pipa, px, GROUND + bob(0.5), 0.6, t=t, neck=pipa_neck(t), lean=pipa_lean(t), look=lk, lid=sleep(16.5),
          walk=t * 7 if 41.5 < t < 43 or 47.5 < t < 49 else 0)
    if 45.0 < t < 47.5:   # mango en la boca
        hx = px + 0.6 * pipa_lean(t); hy = GROUND - 0.6 * (260 + pipa_neck(t))
        mango(c, hx + 25, hy + 50, 0.8)
    # Tito
    tx = 360
    spray = 25.5 < t < 29.5
    reach = 250 + 30 * math.sin(t * 5) if spray else (180 if 24.0 < t < 25.5 else None)
    K.put(c, K.tito, tx, GROUND + bob(1.0), 0.66, flip=True, t=t, look=(1, -0.2), lid=sleep(15.5), yawn=math.sin(math.pi * ss(15.2, 17.4, t)), reach=reach)
    if spray:   # chorro de agua en arco
        for k in range(45):
            q = ((t * 1.6) + k / 45) % 1
            x = tx + 220 + 820 * q + 25 * math.sin(k * 3.1); y = GROUND - 330 - 260 * math.sin(math.pi * q) + 200 * q + 20 * math.cos(k * 1.7)
            ellipse(c, x, y, 16, 20); fill(c, (0.55, 0.85, 1, 0.95), (0.1, 0.45, 0.8, 1), 3)
            ellipse(c, x - 5, y - 7, 5, 6); c.set_source_rgba(1, 1, 1, 0.9); c.fill()
    # Tomi
    tmx = kf(t, TOMI_X)
    hide = 1 - ss(17.0, 18.5, t)
    K.put(c, K.tomi, tmx, GROUND + bob(1.5), 0.6, t=t, look=(-1, 0.2), hide=hide if t < 49.5 else 0.0, mood='chew' if eat and (t % 1.3) > 0.6 else 'smile',
          walk=t * 4 if 50.1 < t < 53 else 0)
    if 50.1 < t < 53.0:
        for k in range(3): strawberry(c, tmx - 20 + 25 * k, GROUND - 0.6 * 230, 1.0)
    # Coco
    cx = 760
    mood, look = 'smile', (1, 0)
    ar, al, alen = math.radians(65 + 6 * math.sin(t * 2)), math.radians(115 - 6 * math.sin(t * 2)), 115
    lid = sleep(14.2)
    if 14.2 < t < 16.5: ar, al = math.radians(-80), math.radians(-100); mood = 'o'     # se estira
    if wet: mood = 'closed' if (t % 1.4) > 0.5 else 'o'; ar, al = math.radians(-60 + 20 * math.sin(t * 8)), math.radians(-120 - 20 * math.sin(t * 8))
    if 32.5 < t < 36.5: ar = math.radians(-60); mood = 'o'
    if 58.5 < t < 61.5: ar, al = math.radians(-50), math.radians(-130)
    if 71.5 < t < 75.5:
        a2 = (t - 71.5) * 6
        ar, alen = aim(cx, GROUND, 0.62, BOWL[0] + 60 * math.cos(a2) - 50, BOWL[1] - 270 + 12 * math.sin(a2))
    if eat:
        mood = 'chew' if (t % 1.1) > 0.5 else 'smile'; ar = math.radians(-30 if (t % 1.1) < 0.5 else 40)
    if party: ar, al = math.radians(-58 + 25 * math.sin(t * 9)), math.radians(-122 - 25 * math.sin(t * 9))
    K.put(c, K.coco, cx, GROUND + bob(0), 0.62, t=t, mood=mood, look=look, lid=lid, arm_r=ar, arm_l=al, arm_len=alen, chew=t,
          hold='bunch' if 58.5 < t < 61.0 else ('banana' if eat else None))
    spoon(c, t)
    bowl(c, t, True)
    pile(c, t)
    # Lola
    if t < 6.0: lx, ly = 1180, 520
    elif 55.0 < t < 56.0:
        q = ss(55.0, 56.0, t); lx, ly = 1100 + (720 - 1100) * q, 430 + 300 * math.sin(math.pi * q) * 0.3
    else: lx, ly = 1100 + 120 * math.sin(t * 0.5), 430 + 18 * math.sin(t * 3)
    K.put(c, K.lola, lx, ly + bob(2.0), 0.5, t=t, flap=20 if t > 6.5 else 0, look=(-0.5, 0.4), lid=sleep(6.0))
    if 53.5 < t < 55.2: grapes(c, lx - 10, ly + 30, 0.8)
    if 6.5 < t < 13.5 or party:
        for k in range(3):
            ph = (t * 0.7 + k / 3) % 1
            music_note(c, lx + 40 + 60 * ph, ly - 150 - 160 * ph, math.sin(math.pi * ph), ['#E91E63', '#1E88E5', '#FFD600'][k])
    zzz(c, cx + 60, GROUND - 330, t, sleep(14.2))
    zzz(c, tx - 60, GROUND - 420, t, sleep(15.5))
    zzz(c, px + 40, GROUND - 560, t, sleep(16.5))
    if wet:
        for k in range(10):
            ph = ((t - 26.0) * 0.8 + k / 10) % 1
            sparkle(c, 600 + 90 * k, GROUND - 350 + 120 * math.sin(k), 14 * math.sin(math.pi * ph), '#B3E5FC')
    if eat:
        for k in range(5):
            ph = ((t - 78.0) * 0.4 + k / 5) % 1
            heart(c, 600 + 170 * k, GROUND - 420 - 200 * ph, 0.9, math.sin(math.pi * ph))
    # globitos
    bubble(c, lx, ly - 170, '¡Buen día!', (t - 7.5) / 3.6, 56)
    bubble(c, cx, GROUND - 330, '¡Aaaah!', (t - 14.4) / 2.0, 52)
    bubble(c, tx - 100, GROUND - 470, '¡Fshhh!', (t - 25.6) / 2.4, 56)
    bubble(c, cx, GROUND - 330, '¡Jajaja!', (t - 28.0) / 2.6, 52)
    bubble(c, cx, GROUND - 330, '¡Hagamos un desayuno!', (t - 32.8) / 3.6, 44)
    bubble(c, tmx, GROUND - 260, '¡Frutillas!', (t - 52.5) / 2.6, 50)
    bubble(c, lx, ly - 170, '¡Uvas!', (t - 55.3) / 2.2, 56)
    bubble(c, cx, GROUND - 330, '¡Bananas!', (t - 59.0) / 2.6, 54)
    bubble(c, cx, GROUND - 330, '¡Mmm!', (t - 80.0) / 2.4, 60)

def overlay(c, t):
    if t < 5.6:
        a = 1 - ss(4.8, 5.5, t)
        c.push_group(); word(c, 'El desayuno de los amigos', W / 2, 230, 110 * K_back((t - 0.6) / 0.6) + 0.01,
                             colors=['#FFB300', '#E53935', '#43A047', '#8E24AA'], tilt=0.05, outline=9)
        c.pop_group_to_source(); c.paint_with_alpha(a)
    if 67.5 < t < 76.0:
        s = K_back((t - 67.5) / 0.5) * (1 - ss(75.6, 76.0, t))
        word(c, '¡Ensalada de frutas!', W / 2 + 160, 150, 100 * s + 0.01, colors=['#FFB300', '#E53935', '#43A047', '#8E24AA'], tilt=0.04, outline=9)
    if t > 92.5:
        s = K_back((t - 92.5) / 0.7)
        word(c, '¡Buen día,', W / 2 + 160, 160, 125 * s + 0.01, colors=['#FFB300', '#E53935', '#43A047'], tilt=0.05, outline=10)
        word(c, 'amigos!', W / 2 + 160, 290, 125 * s + 0.01, colors=['#43A047', '#8E24AA', '#FFB300'], tilt=0.05, outline=10)
    a = max(1 - ss(0, 0.8, t), ss(DUR - 2.0, DUR, t))
    if a > 0: c.set_source_rgba(1, 1, 1, a); c.paint()

if __name__ == '__main__':
    args = sys.argv[1:]
    if args and args[0] == 'srt':
        print(srt(NARRACION, float(args[1]) if len(args) > 1 else 0.0)); sys.exit()
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(surf)
    def full(c, t):
        z = 1 + 0.15 * ss(32.0, 34.0, t) * (1 - ss(90.0, 92.0, t))
        c.save(); c.translate(W / 2, H / 2); c.scale(z, z); c.translate(-(W / 2 - 60 * (z - 1) / 0.15), -(H / 2 + 60 * (z - 1) / 0.15))
        frame(c, t); c.restore(); overlay(c, t)
    if args and args[0] == 'stills':
        for t in map(float, args[1:]):
            c.save(); full(c, t); c.restore(); surf.write_to_png(f'ep27_{t}.png')
    else:
        t0, t1 = (float(args[1]), float(args[2])) if args and args[0] == 'range' else (0, DUR)
        out = sys.stdout.buffer
        for i in range(int(round(t0 * FPS)), int(round(t1 * FPS))):
            c.save(); full(c, i / FPS); c.restore(); surf.flush(); out.write(surf.get_data())
