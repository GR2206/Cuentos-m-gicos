"""Episodio 21 — La gran carrera del bosque (100 s). Aventurita de día.
Lola anuncia la gran carrera. Coco sale rapidísimo, pero vuelve a ayudar a Tomi, que se dio vuelta;
un tronco tapa el camino y Tito lo levanta con la trompa. Cerca de la meta, Coco espera a todos
y cruzan juntos: ¡ganaron todos! Medallas para cada uno y fiesta.

Uso:  python3 ep21_carrera.py              -> cuadros crudos por stdout
      python3 ep21_carrera.py range 0 50   -> solo un tramo
      python3 ep21_carrera.py stills 20 70 -> PNG sueltos
      python3 ep21_carrera.py srt 5.5      -> subtítulos .srt de la narración"""
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
DUR = 100.0
GROUND = 880
START, FINISH, LOG = 1200, 5250, 3800

NARRACION = [
    (6.0, 10.0, '¡Hoy es la gran carrera del bosque! Lola es la que da la largada.'),
    (14.5, 19.5, '¡Y salieron! Coco corría rapidísimo, ¡era el primero!'),
    (20.0, 27.0, 'Pero de pronto escuchó: ¡ay! Tomi se había dado vuelta. Coco volvió a ayudarla.'),
    (29.0, 36.0, 'Siguieron corriendo, todos juntos, por el caminito del bosque.'),
    (37.0, 46.0, '¡Un tronco enorme tapaba el camino! Pero Tito, que es muy fuerte, lo levantó con la trompa.'),
    (47.5, 56.0, 'Ya se veía la meta. Coco podía llegar primero... pero esperó a sus amigos.'),
    (56.5, 63.0, 'Se tomaron de las manos y cruzaron todos juntos. ¡Ganaron todos!'),
    (64.0, 72.0, 'Lola les dio una medalla a cada uno, y festejaron cantando y bailando.'),
    (93.0, 99.0, 'Porque lo más lindo... es llegar juntos.'),
]

COCO_X = [(0, 1200), (14.0, 1200), (21.0, 2650), (21.8, 2650), (24.0, 1860), (28.0, 1860), (36.0, 3560), (46.0, 3560),
          (51.5, 4950), (55.0, 4950), (58.5, FINISH + 300), (100, FINISH + 300)]
TOMI_X = [(0, 1380), (14.0, 1380), (19.5, 1700), (28.0, 1700), (36.0, 3380), (46.0, 3380), (52.0, 4480), (55.0, 4800),
          (58.5, FINISH + 450), (100, FINISH + 450)]
TITO_X = [(0, 960), (14.0, 960), (36.0, 3150), (38.0, 3150), (39.5, 3540), (44.0, 3540), (46.0, 3250), (52.5, 4450),
          (55.0, 4650), (58.5, FINISH + 120), (100, FINISH + 120)]
PIPA_X = [(0, 720), (14.0, 720), (36.0, 2950), (46.0, 2950), (52.5, 4250), (55.0, 4470), (58.5, FINISH - 80), (100, FINISH - 80)]
CAM = [(0, 1000), (14.0, 1000), (21.0, 2450), (24.0, 2000), (28.0, 2000), (36.0, 3450), (46.0, 3500), (51.5, 4700),
       (55.0, 4800), (58.5, FINISH + 150), (100, FINISH + 150)]

def moving(keys, t): return abs(kf(t + 0.05, keys) - kf(t, keys)) > 1.0

def tomi_flip(t):   # 0 parada, 1 patas para arriba
    return ss(19.5, 20.0, t) * (1 - ss(25.5, 26.6, t))

def log_state(t, trunk):
    """posición del tronco (mundo): en el piso, levantado por Tito, revoleado al costado."""
    if t < 40.5: return LOG, GROUND - 40, 0.0, 1.0
    if t < 43.0:
        q = ss(40.5, 41.5, t); return LOG + (trunk[0] - LOG) * q, GROUND - 40 + (trunk[1] - GROUND + 40) * q, 0.3 * q, 1.0
    q = ss(43.0, 44.5, t)
    return trunk[0] + 500 * q, trunk[1] - 300 * math.sin(math.pi * q) + 260 * q, 0.3 + 3.0 * q, 1 - ss(44.0, 44.6, t)

def big_log(c, x, y, rot, a):
    if a <= 0: return
    c.push_group(); c.save(); c.translate(x, y); c.rotate(rot)
    c.rectangle(-170, -42, 340, 84); fill(c, hexc('#8D5524'), OUT, 6)
    for dx in (-90, 0, 90):
        c.move_to(dx - 30, -20); c.line_to(dx + 30, -24); c.set_source_rgba(*hexc('#6D4C41')); c.set_line_width(5); c.stroke()
    ellipse(c, 170, 0, 26, 42); fill(c, hexc('#D7A86E'), OUT, 6)
    for r in (16, 8): ellipse(c, 170, 0, r * 0.6, r); c.set_source_rgba(*hexc('#8D5524')); c.set_line_width(3); c.stroke()
    c.restore(); c.pop_group_to_source(); c.paint_with_alpha(a)

def banner(c, sx, text, cols):
    for d in (-1, 1):
        c.rectangle(sx + d * 330 - 14, 420, 28, GROUND - 420 + 10); fill(c, hexc('#FFFFFF'), OUT, 5)
        for k in range(5): c.rectangle(sx + d * 330 - 14, 440 + 90 * k, 28, 45); c.set_source_rgba(*hexc('#E53935')); c.fill()
        c.rectangle(sx + d * 330 - 14, 420, 28, GROUND - 420 + 10); c.set_source_rgba(*OUT); c.set_line_width(5); c.stroke()
    c.move_to(sx - 330, 440); c.curve_to(sx - 100, 470, sx + 100, 470, sx + 330, 440); c.line_to(sx + 330, 540)
    c.curve_to(sx + 100, 570, sx - 100, 570, sx - 330, 540); c.close_path(); fill(c, hexc('#FFF59D'), OUT, 6)
    for k in range(10):   # cuadritos de bandera
        for j in range(2):
            if (k + j) % 2: c.rectangle(sx - 300 + 60 * k, 380 + 22 * j, 30, 22); c.set_source_rgba(*OUT); c.fill()
    word(c, text, sx, 515, 66, colors=cols, outline=7)

def medal(c, x, y, s, a):
    if a <= 0.01: return
    c.save(); c.translate(x, y); c.scale(s * a, s * a)
    for d in (-1, 1):
        c.move_to(d * 6, -70); c.line_to(d * 22, -10); c.line_to(d * 4, -10); c.close_path(); fill(c, hexc('#1E88E5' if d < 0 else '#E53935'), OUT, 3)
    ellipse(c, 0, 10, 26, 26); fill(c, hexc('#FFD600'), hexc('#F57F17'), 5)
    sparkle(c, 0, 10, 12, '#FFFFFF')
    c.restore()

def confetti(c, t, t0):
    if t < t0: return
    rnd = random.Random(5)
    for k in range(70):
        x0 = rnd.uniform(0, W); sp = rnd.uniform(120, 260); ph = rnd.uniform(0, 6)
        y = -40 + ((t - t0) * sp + rnd.uniform(0, 1100)) % 1150
        c.save(); c.translate(x0 + 30 * math.sin(t * 2 + ph), y); c.rotate(t * 3 + ph)
        c.rectangle(-9, -5, 18, 10); c.set_source_rgba(*hexc(('#E53935', '#FFD600', '#1E88E5', '#43A047', '#AB47BC')[k % 5])); c.fill()
        c.restore()

def frame(c, t):
    cam = kf(t, CAM)
    S = lambda wx: wx - cam + 960
    g = cairo.LinearGradient(0, 0, 0, H)
    for k, col in enumerate(('#29B6F6', '#81D4FA', '#B3E5FC')): g.add_color_stop_rgb(k / 2, *hexc(col)[:3])
    c.set_source(g); c.paint()
    for (x0, y0, s, sp) in ((150, 150, 0.9, 12), (820, 100, 0.7, 8), (1450, 200, 0.6, 15)):
        c.save(); c.translate((x0 - cam * 0.05 + sp * t) % 2300 - 250, y0); c.scale(s, s)
        for (cx, cy, r) in ((0, 0, 60), (70, -30, 75), (150, 0, 60), (75, 20, 60)): ellipse(c, cx, cy, r, r)
        c.set_source_rgba(1, 1, 1, 1); c.fill(); c.restore()
    far_hills(c, cam); back_trees(c, cam); ground(c, cam); path_trees(c, cam)
    banner(c, S(START), '¡LARGADA!', ['#E53935', '#1E88E5'])
    banner(c, S(FINISH), '¡LLEGADA!', ['#43A047', '#E53935', '#1E88E5'])
    race = 14.0 < t < 58.5
    party = t > 64.0
    bob = lambda ph: -22 * abs(math.sin(t * 4.5 + ph)) if party else 0
    medal_a = lambda k: K_back((t - 62.0 - 0.6 * k) / 0.4) if t > 62.0 + 0.6 * k else 0
    # Pipa
    px = S(kf(t, PIPA_X))
    K.put(c, K.pipa, px, GROUND + bob(0.5), 0.55, t=t, look=(1, 0), walk=t * 10 if moving(PIPA_X, t) else 0)
    medal(c, px + 35, GROUND - 0.55 * 300 + bob(0.5), 0.9, medal_a(0))
    # Tito
    tx = S(kf(t, TITO_X))
    lift = 40.0 < t < 43.2
    reach = (kf(t, [(40.0, 160), (40.8, 260), (41.6, 330), (43.0, 330)]) if lift else None)
    trunk = (kf(t, TITO_X) + 0.6 * 160 + 0.6 * (reach or 0) * 0.55, GROUND - 0.6 * 140 - (180 if t > 41.5 else 0) * ss(41.5, 42.5, t))
    K.put(c, K.tito, tx, GROUND + bob(1.0), 0.6, t=t, look=(1, -0.3 if lift else 0), reach=reach,
          walk=t * 8 if moving(TITO_X, t) else 0)
    medal(c, tx + 10, GROUND - 0.6 * 190 + bob(1.0), 1.0, medal_a(1))
    lx, ly, lr, la = log_state(t, trunk)
    big_log(c, S(lx), ly, lr, la)
    # Tomi
    tmx = S(kf(t, TOMI_X)); fl = tomi_flip(t)
    if fl > 0:
        K.put(c, K.tomi, tmx, GROUND - 145 * fl, 0.55, rot=math.pi * fl, t=t, look=(1, 0), walk=t * 14, mood='smile' if t > 25.5 else 'smile')
    else:
        K.put(c, K.tomi, tmx, GROUND + bob(1.5), 0.55, t=t, look=(1, 0), walk=t * 6 if moving(TOMI_X, t) else 0)
        medal(c, tmx + 20, GROUND - 0.55 * 160 + bob(1.5), 0.9, medal_a(2))
    # Coco
    cx = S(kf(t, COCO_X))
    mood, look, flip = 'smile', (1, -0.1), False
    ar, al = math.radians(65 + 6 * math.sin(t * 2)), math.radians(115 - 6 * math.sin(t * 2))
    if moving(COCO_X, t) and race: ar, al = math.radians(30 + 50 * math.sin(t * 14)), math.radians(150 - 50 * math.sin(t * 14))
    if 21.0 < t < 22.0: mood, look = 'o', (-1, 0)
    if 21.8 < t < 24.0: flip = True; look = (1, 0)
    if 24.0 < t < 26.5: flip = True; look = (1, 0.5); ar = al = math.radians(80 + 30 * math.sin(t * 8))
    if 38.0 < t < 40.0: mood = 'o'
    if 51.5 < t < 55.0: flip = True; look = (1, 0); ar = math.radians(-50 + 20 * math.sin(t * 6))
    if 55.0 < t < 58.5: ar, al = math.radians(10), math.radians(170)   # de la mano
    if 57.5 < t < 64.0: ar, al = math.radians(-60), math.radians(-120); mood = 'o' if t < 59 else 'smile'
    if party: ar, al = math.radians(-58 + 25 * math.sin(t * 9)), math.radians(-122 - 25 * math.sin(t * 9))
    K.put(c, K.coco, cx, GROUND + bob(0), 0.55, flip=flip, t=t, mood=mood, look=look, arm_r=ar, arm_l=al,
          walk=t * 12 if moving(COCO_X, t) else 0)
    medal(c, cx + 5, GROUND - 0.55 * 190 + bob(0), 0.9, medal_a(3))
    if moving(COCO_X, t) and race and not flip:   # polvito
        for k in range(4):
            ph = (t * 3 + k / 4) % 1
            ellipse(c, cx - 60 - 120 * ph, GROUND - 10 - 30 * ph, 18 * (1 - ph) + 1, 14 * (1 - ph) + 1); c.set_source_rgba(1, 1, 1, 0.7 * (1 - ph)); c.fill()
    # Lola (relatora)
    lox = 960 - 260 + 60 * math.sin(t * 0.7) if t < 14 else 960 + 260 * math.sin(t * 0.4)
    loy = 380 + 20 * math.sin(t * 3)
    K.put(c, K.lola, lox, loy + bob(2.0), 0.5, t=t, flap=20, look=(0.5, 0.4))
    fg_bushes(c, cam); flowers_front(c, cam)
    confetti(c, t, 57.5)
    if party:
        for k in range(3):
            ph = (t * 0.7 + k / 3) % 1
            music_note(c, lox + 40 + 60 * ph, loy - 150 - 160 * ph, math.sin(math.pi * ph), ['#E91E63', '#1E88E5', '#FFD600'][k])
    if 58.0 < t < 62.0:
        for k in range(5):
            ph = ((t - 58.0) * 0.5 + k / 5) % 1
            heart(c, 700 + 150 * k, 600 - 200 * ph, 1.0, math.sin(math.pi * ph))
    # globitos
    bubble(c, lox, loy - 170, '¡A sus lugares!', (t - 6.5) / 3.2, 46)
    bubble(c, tmx, GROUND - 260, '¡Ay!', (t - 19.8) / 2.4, 60)
    bubble(c, tmx, GROUND - 260, '¡Gracias, Coco!', (t - 26.5) / 2.8, 46)
    bubble(c, cx, GROUND - 300, '¡Un tronco!', (t - 37.6) / 2.6, 52)
    bubble(c, cx, GROUND - 300, '¡Esperemos a todos!', (t - 52.0) / 3.0, 44)
    bubble(c, lox, loy - 170, '¡Ganaron todos!', (t - 58.6) / 3.4, 52)

def overlay(c, t):
    if t < 5.6:
        a = 1 - ss(4.8, 5.5, t)
        c.push_group(); word(c, 'La gran carrera', W / 2, 230, 130 * K_back((t - 0.6) / 0.6) + 0.01, tilt=0.05, outline=9)
        c.pop_group_to_source(); c.paint_with_alpha(a)
    for (t0, txt, col) in ((10.2, '3', '#E53935'), (11.2, '2', '#FFB300'), (12.2, '1', '#43A047'), (13.2, '¡YA!', '#1E88E5')):
        if t0 <= t < t0 + 1.0:
            q = t - t0
            word(c, txt, W / 2, 330, 260 * K_back(q / 0.3) * (1 - ss(0.8, 1.0, q)) + 0.01, colors=[col], outline=12)
    if t > 93.0:
        s = K_back((t - 93.0) / 0.7)
        word(c, '¡Llegamos', W / 2, 160, 120 * s + 0.01, tilt=0.05, outline=10)
        word(c, 'todos juntos!', W / 2, 290, 120 * s + 0.01, start=3, tilt=0.05, outline=10)
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
            c.save(); full(c, t); c.restore(); surf.write_to_png(f'ep21_{t}.png')
    else:
        t0, t1 = (float(args[1]), float(args[2])) if args and args[0] == 'range' else (0, DUR)
        out = sys.stdout.buffer
        for i in range(int(round(t0 * FPS)), int(round(t1 * FPS))):
            c.save(); full(c, i / FPS); c.restore(); surf.flush(); out.write(surf.get_data())
