"""Episodio 24 — El barrilete perdido (105 s). Aventurita (pensada para narrar con la voz de Gino).
Pipa remonta su barrilete, una ráfaga de viento se lo lleva y los amigos lo persiguen por el bosque.
Queda enganchado arriba de una palmera altísima: Pipa no llega y Lola no puede desenredarlo,
hasta que Tomi propone una torre: ¡Coco se sube a la cabeza de Pipa y lo baja! Al final lo remontan todos juntos.

Uso:  python3 ep24_barrilete.py              -> cuadros crudos por stdout
      python3 ep24_barrilete.py range 0 52   -> solo un tramo
      python3 ep24_barrilete.py stills 20 70 -> PNG sueltos
      python3 ep24_barrilete.py srt 5.5      -> subtítulos .srt de la narración"""
import cairo, math, random, sys
import cuerpos as K
from amigos import hexc, ellipse, fill, OUT
from logos import word, sparkle
from ep02_puente_del_rio import kf, ss, K_back, music_note
from ep03_donde_esta_tomi import bubble
from ep09_semilla_magica import srt
from ep14_bananas_papa import heart
from ep10_cruzando_el_bosque import far_hills, back_trees, ground, path_trees, flowers_front, fg_bushes

W, H, FPS = 1920, 1080, 30
DUR = 105.0
GROUND = 880
PALM = 6000
STUCK = (PALM + 10, 150)
KCOLS = ['#FF4081', '#FFD600', '#00B0FF', '#00C853']
CAM = [(0, 1000), (22.0, 1000), (46.0, 5600), (70.0, 5600), (76.0, 6700), (105, 6700)]

NARRACION = [
    (6.0, 12.0, 'Era un día de mucho viento, y Pipa remontaba su barrilete. ¡Qué alto volaba!'),
    (17.0, 22.0, 'Pero de pronto, una ráfaga fuerte... ¡se llevó el barrilete!'),
    (23.5, 30.0, '¡Hay que alcanzarlo! Y todos salieron corriendo por el bosque.'),
    (31.0, 37.0, 'Coco saltó bien alto... ¡pero no llegó!'),
    (38.0, 45.0, 'Lola voló detrás, pero el viento soplaba muy fuerte.'),
    (47.0, 52.5, 'El barrilete quedó enganchado arriba de una palmera altísima.'),
    (53.0, 59.5, 'Pipa estiró el cuello todo lo que pudo... pero no llegaba.'),
    (60.0, 66.0, 'Entonces Tomi tuvo una idea: ¡hagamos una torre! Coco se subió a la cabeza de Pipa...'),
    (66.5, 71.0, '¡Y lo alcanzó! ¡Lo tenemos!'),
    (77.0, 88.0, 'Después, subieron a la loma y remontaron el barrilete todos juntos. ¡Volaba más alto que nunca!'),
    (96.0, 103.0, 'Porque juntos, ¡llegamos más alto!'),
]

def cam(t): return kf(t, CAM)

# ---------------- posiciones ----------------
FORM = {'coco': 0, 'tomi': -230, 'tito': -480, 'pipa': -760}
def x_of(name, t):
    base = cam(t) + FORM[name]
    if 46.0 <= t < 76.0:
        stop = {'pipa': PALM - 140, 'coco': PALM - 330, 'tito': PALM - 620, 'tomi': PALM - 860}[name]
        base = kf(t, [(46.0, 5600 + FORM[name]), (50.0, stop), (70.0, stop), (76.0, 6700 + {'pipa': -520, 'coco': -150, 'tito': -330, 'tomi': 120}[name])])
    if t >= 76.0:
        base = 6700 + {'pipa': -520, 'coco': -150, 'tito': -330, 'tomi': 120}[name]
    return base

def moving(name, t): return abs(x_of(name, t + 0.05) - x_of(name, t)) > 1.0

def pipa_neck(t): return kf(t, [(52.0, 300), (54.5, 760), (58.5, 760), (60.5, 300), (61.5, 160), (62.8, 160), (64.6, 760), (67.4, 760), (69.0, 300)])
def pipa_lean(t): return kf(t, [(52.0, 0), (54.5, 120), (58.5, 120), (60.5, 0), (61.5, -330), (62.8, -330), (64.6, 140), (67.4, 140), (69.0, 0)])
def pipa_head(t): return x_of('pipa', t) + 0.55 * pipa_lean(t), GROUND - 0.55 * (260 + pipa_neck(t))

def coco_base(t):
    """dónde se paran los pies de Coco (mundo) y su escala."""
    x = x_of('coco', t)
    if 61.8 < t < 68.2:
        hx, hy = pipa_head(t)
        if t < 62.6:   # salta a la cabeza de Pipa
            q = ss(61.8, 62.6, t); return x + (hx - x) * q, GROUND + (hy - 55 - GROUND) * q - 120 * math.sin(math.pi * q)
        if t < 67.6: return hx, hy - 55
        q = ss(67.6, 68.2, t); return hx + (x - hx) * q, hy - 55 + (GROUND - hy + 55) * q - 100 * math.sin(math.pi * q)
    return x, GROUND

def kite_pos(t):
    """barrilete (mundo): x, y, inclinación."""
    if t < 16.5:
        px = x_of('pipa', t); return px + 420 + 60 * math.sin(t * 0.9), 230 + 40 * math.sin(t * 1.3), 0.15 * math.sin(t * 2)
    if t < 46.0:
        c0 = cam(t)
        x = kf(t, [(16.5, x_of('pipa', 16.5) + 420), (19.5, 1000 + 760), (22.0, 1000 + 820)]) if t < 22.0 else c0 + 820 - 300 * math.sin((t - 22) * 0.35) ** 2
        y = 240 + 70 * math.sin(t * 1.7)
        y += 360 * math.sin(math.pi * ss(31.0, 34.0, t)) + 220 * math.sin(math.pi * ss(38.0, 43.0, t))
        if t < 22.0: y = kf(t, [(16.5, 260), (18.0, 120), (22.0, 240)])
        return x, y, 0.4 * math.sin(t * 3)
    if t < 50.0:
        q = ss(46.0, 50.0, t); x0 = cam(46.0) + 820
        return x0 + (STUCK[0] - x0) * q, 240 + (STUCK[1] - 240) * q - 60 * math.sin(math.pi * q), 0.4 * (1 - q)
    if t < 66.4: return STUCK[0], STUCK[1] + 6 * math.sin(t * 3), -0.3 + 0.08 * math.sin(t * 4)
    if t < 70.0:   # en las manos de Coco
        bx, by = coco_base(t); return bx + 70, by - 0.45 * 300 - 80, -0.2
    if t < 76.0:
        bx, by = coco_base(t); return bx + 60, by - 210, -0.2
    q = ss(76.5, 80.0, t)
    bx = x_of('coco', t)
    return bx + 60 + (bx + 820 - bx - 60) * q, GROUND - 210 + (230 - GROUND + 210) * q + 40 * math.sin(t * 1.2) * q, 0.15 * math.sin(t * 2) * q

def string_from(t):
    """de dónde sale el hilo (mundo), o None si no hay hilo."""
    if t < 17.0:
        hx, hy = pipa_head(t); return hx + 30, hy + 10
    if t > 76.5:
        bx = x_of('coco', t); return bx + 70, GROUND - 0.55 * 300
    return None

# ---------------- dibujos ----------------
def kite(c, x, y, s, t, rot=0.0, tail=True, tangled=False):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    pts = [(0, -200), (140, -40), (0, 220), (-140, -40)]
    for i in range(4):
        p0, p1 = pts[i], pts[(i + 1) % 4]
        c.move_to(0, -40); c.line_to(*p0); c.line_to(*p1); c.close_path(); c.set_source_rgba(*hexc(KCOLS[i])); c.fill()
    c.move_to(*pts[0])
    for p in pts[1:]: c.line_to(*p)
    c.close_path(); c.set_source_rgba(*OUT); c.set_line_width(8); c.stroke()
    for ex in (-35, 35): ellipse(c, ex, -50, 10, 13); c.set_source_rgba(*OUT); c.fill()
    if tangled: c.arc(0, -5, 26, 1.2 * math.pi, 1.8 * math.pi)
    else: c.arc(0, -20, 34, 0.2 * math.pi, 0.8 * math.pi)
    c.set_line_width(7); c.stroke()
    if tail:
        px, py = 0, 220
        for i in range(6):
            nx, ny = 30 * math.sin(t * 6 + i) + (i * 20 if tangled else 0), 220 + (i + 1) * 70
            c.move_to(px, py); c.line_to(nx, ny); c.set_source_rgba(*OUT); c.set_line_width(5); c.stroke()
            c.save(); c.translate(nx, ny); c.rotate(0.8)
            c.rectangle(-16, -9, 32, 18); fill(c, hexc(KCOLS[i % 4]), OUT, 4); c.restore()
            px, py = nx, ny
    c.restore()

def tall_palm(c, sx, t):
    tipx, tipy = sx + 30, 200
    c.set_line_cap(cairo.LINE_CAP_ROUND)
    for (col, w) in ((OUT, 64), (hexc('#8D5524'), 52)):
        c.move_to(sx, GROUND + 5); c.curve_to(sx + 5, 700, sx + 30, 400, tipx, tipy)
        c.set_source_rgba(*col); c.set_line_width(w); c.stroke()
    for k in range(9):   # anillos
        y = GROUND - 80 - 75 * k
        c.move_to(sx - 24 + 0.04 * (GROUND - y), y); c.line_to(sx + 22 + 0.04 * (GROUND - y), y - 8); c.set_source_rgba(*OUT); c.set_line_width(4); c.stroke()
    sway = math.sin(t * 1.5)
    for i, ang in enumerate((-175, -140, -105, -75, -40, -5, 200)):
        a = math.radians(ang + 5 * sway)
        c.save(); c.translate(tipx, tipy); c.rotate(a)
        c.move_to(0, 0); c.curve_to(90, -55, 230, -40, 320, 40); c.curve_to(220, 18, 90, 26, 0, 0); c.close_path()
        fill(c, hexc('#2E7D32' if i % 2 else '#43A047'), hexc('#1B5E20'), 4); c.restore()
    for d in (-30, 10, 45): ellipse(c, tipx + d, tipy + 30, 22, 22); fill(c, hexc('#8D6E63'), OUT, 4)

def wind(c, t, a):
    if a <= 0: return
    for k in range(9):
        ph = (t * 0.9 + k / 9) % 1
        x = -200 + 2300 * ph; y = 180 + 80 * k
        c.move_to(x, y); c.curve_to(x + 80, y - 30, x + 160, y + 30, x + 260, y)
        c.set_source_rgba(1, 1, 1, 0.7 * a * math.sin(math.pi * ph)); c.set_line_width(7); c.stroke()
    for k in range(10):   # hojitas volando
        ph = (t * 0.7 + k / 10) % 1
        x = -100 + 2100 * ph; y = 300 + 60 * k + 50 * math.sin(t * 4 + k)
        c.save(); c.translate(x, y); c.rotate(t * 5 + k)
        c.move_to(0, -14); c.curve_to(12, -6, 12, 6, 0, 14); c.curve_to(-12, 6, -12, -6, 0, -14); c.close_path()
        fill(c, hexc(('#66BB6A', '#FFB300', '#8BC34A')[k % 3], a), OUT, 2); c.restore()

def windy(t): return ss(16.0, 17.0, t) * (1 - ss(46.0, 48.0, t)) + 0.35 * ss(76.0, 78.0, t)

def frame(c, t):
    cm = cam(t)
    S = lambda wx: wx - cm + 960
    g = cairo.LinearGradient(0, 0, 0, H)
    for k, col in enumerate(('#29B6F6', '#81D4FA', '#B3E5FC')): g.add_color_stop_rgb(k / 2, *hexc(col)[:3])
    c.set_source(g); c.paint()
    for (x0, y0, s, sp) in ((150, 150, 0.9, 30), (820, 100, 0.7, 25), (1450, 200, 0.6, 35)):
        c.save(); c.translate((x0 - cm * 0.05 + sp * t) % 2300 - 250, y0); c.scale(s, s)
        for (cx, cy, r) in ((0, 0, 60), (70, -30, 75), (150, 0, 60), (75, 20, 60)): ellipse(c, cx, cy, r, r)
        c.set_source_rgba(1, 1, 1, 1); c.fill(); c.restore()
    far_hills(c, cm); back_trees(c, cm); ground(c, cm); path_trees(c, cm)
    tall_palm(c, S(PALM), t)
    party = t > 78.0
    bob = lambda ph: -16 * abs(math.sin(t * 4.5 + ph)) if party and t > 84 else 0
    # hilo
    kx, ky, kr = kite_pos(t)
    sf = string_from(t)
    if sf:
        c.move_to(S(sf[0]), sf[1]); c.curve_to(S(sf[0]) + 200, sf[1] - 60, S(kx) - 150, ky + 260, S(kx), ky + 40)
        c.set_source_rgba(1, 1, 1, 0.95); c.set_line_width(3); c.stroke()
    big = 0.45 if t < 66.4 or t > 76.0 else 0.3
    kite(c, S(kx), ky, big, t, kr, tangled=50.0 < t < 66.4)
    # Pipa
    px = S(x_of('pipa', t)); hx, hy = pipa_head(t)
    look_p = (1, -0.9) if 52 < t < 59 or 64 < t < 67.4 else ((-1, 0.5) if 60.5 < t < 63 else (1, -0.6))
    K.put(c, K.pipa, px, GROUND + bob(0.5), 0.55, t=t, neck=pipa_neck(t), lean=pipa_lean(t), look=look_p,
          walk=t * 9 if moving('pipa', t) else 0)
    # Tito
    tx = S(x_of('tito', t))
    K.put(c, K.tito, tx, GROUND + bob(1.0), 0.6, t=t, look=(1, -0.5), walk=t * 8 if moving('tito', t) else 0,
          reach=140 if party else None)
    # Tomi
    tmx = S(x_of('tomi', t))
    K.put(c, K.tomi, tmx, GROUND + bob(1.5), 0.55, t=t, look=(1, -0.3), walk=t * 5 if moving('tomi', t) else 0)
    # Coco
    bx, by = coco_base(t); cx = S(bx)
    mood, look = 'smile', (1, -0.3)
    ar, al = math.radians(65 + 6 * math.sin(t * 2)), math.radians(115 - 6 * math.sin(t * 2))
    running = moving('coco', t) and 22.0 < t < 50.0
    if running: ar, al = math.radians(30 + 50 * math.sin(t * 14)), math.radians(150 - 50 * math.sin(t * 14))
    if 17.5 < t < 22.0: mood = 'o'
    hop = 0.0
    if 31.6 < t < 33.4:   # salto
        hop = -260 * math.sin(math.pi * (t - 31.6) / 1.8); ar, al = math.radians(-70), math.radians(-110); look = (1, -1)
    if 33.4 < t < 35.5: mood = 'sad'
    if 62.6 < t < 67.6: ar, al = math.radians(-70), math.radians(-110); look = (1, -1); mood = 'o' if t < 66.4 else 'smile'
    if 66.4 < t < 76.0: ar = math.radians(-35)
    if party: ar = math.radians(-40 + 8 * math.sin(t * 2)); al = math.radians(-122 - 25 * math.sin(t * 9)) if t > 84 else al
    sc = 0.45 if 62.0 < t < 67.9 else 0.55
    K.put(c, K.coco, cx, by + hop + bob(0), sc, t=t, mood=mood, look=look, arm_r=ar, arm_l=al,
          walk=t * 11 if running or moving('coco', t) else 0, sad=0.7 if mood == 'sad' else 0.0)
    # Lola
    if 37.5 < t < 46.0:   # persigue el barrilete
        q = ss(37.5, 39.0, t)
        lx = S(kx) - 260 * q + (cx - 150) * (1 - q) - 60 * math.sin(t * 3) * q; ly = ky + 120 * q + (430) * (1 - q)
    elif 55.5 < t < 59.5:   # tira de la cola
        lx, ly = S(kx) + 60 + 20 * math.sin(t * 8), ky + 330
    elif party:
        lx, ly = S(kx) - 220 + 40 * math.sin(t * 1.3), ky + 140 + 30 * math.sin(t * 2.1)
    else:
        lx, ly = cx - 150 + 50 * math.sin(t * 0.7), 430 + 20 * math.sin(t * 3)
    K.put(c, K.lola, lx, ly, 0.5, t=t, flap=20, look=(1, -0.3))
    fg_bushes(c, cm); flowers_front(c, cm)
    wind(c, t, windy(t))
    if party:
        for k in range(3):
            ph = (t * 0.7 + k / 3) % 1
            music_note(c, lx + 40 + 60 * ph, ly - 150 - 160 * ph, math.sin(math.pi * ph), ['#E91E63', '#1E88E5', '#FFD600'][k])
    if 68.5 < t < 72.0:
        for k in range(5):
            ph = ((t - 68.5) * 0.6 + k / 5) % 1
            heart(c, cx - 200 + 100 * k, GROUND - 330 - 200 * ph, 0.9, math.sin(math.pi * ph))
    # globitos
    bubble(c, cx, GROUND - 300, '¡Qué alto vuela!', (t - 9.0) / 3.4, 48)
    bubble(c, S(hx), hy - 110, '¡Mi barrilete!', (t - 18.0) / 3.0, 48) if t < 22 else None
    bubble(c, cx, GROUND - 300, '¡Vamos a buscarlo!', (t - 22.2) / 2.8, 46)
    bubble(c, S(hx) if 52 < t < 60 else px, hy - 110, '¡No llego!', (t - 55.0) / 3.0, 52)
    bubble(c, lx, ly - 170, '¡Está enredado!', (t - 56.4) / 3.0, 46)
    bubble(c, tmx, GROUND - 250, '¡Hagamos una torre!', (t - 59.4) / 2.6, 44)
    bubble(c, cx, by - 300, '¡Lo tengo!', (t - 66.5) / 2.4, 52)

def overlay(c, t):
    if t < 5.6:
        a = 1 - ss(4.8, 5.5, t)
        c.push_group(); word(c, 'El barrilete perdido', W / 2, 230, 125 * K_back((t - 0.6) / 0.6) + 0.01, tilt=0.05, outline=9)
        c.pop_group_to_source(); c.paint_with_alpha(a)
    if t > 96.0:
        s = K_back((t - 96.0) / 0.7)
        word(c, '¡Juntos llegamos', W / 2 - 250, 170, 100 * s + 0.01, tilt=0.05, outline=10)
        word(c, 'más alto!', W / 2 - 250, 290, 115 * s + 0.01, start=3, tilt=0.05, outline=10)
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
            c.save(); full(c, t); c.restore(); surf.write_to_png(f'ep24_{t}.png')
    else:
        t0, t1 = (float(args[1]), float(args[2])) if args and args[0] == 'range' else (0, DUR)
        out = sys.stdout.buffer
        for i in range(int(round(t0 * FPS)), int(round(t1 * FPS))):
            c.save(); full(c, i / FPS); c.restore(); surf.flush(); out.write(surf.get_data())
