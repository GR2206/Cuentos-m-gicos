"""Episodio 26 — El concierto de la selva (100 s). Aventurita musical (para narrar con la voz de Malena).
Lola quiere hacer un concierto, pero nadie tiene instrumentos. Coco encuentra dos cocos (¡maracas!), Tito toca
la trompeta con la trompa, Tomi descubre un tronco hueco que suena como tambor y Pipa hace sonar las flores-campanita
de lo alto de un árbol. Al principio tocan todos a la vez y es un lío... hasta que se escuchan y suenan juntos.

Uso:  python3 ep26_concierto.py              -> cuadros crudos por stdout
      python3 ep26_concierto.py range 0 50   -> solo un tramo
      python3 ep26_concierto.py stills 20 70 -> PNG sueltos
      python3 ep26_concierto.py srt 5.5      -> subtítulos .srt de la narración"""
import cairo, math, sys
import cuerpos as K
from amigos import hexc, ellipse, fill, OUT
from logos import word, sparkle
from ep02_puente_del_rio import kf, ss, K_back, music_note
from ep03_donde_esta_tomi import bubble
from ep09_semilla_magica import SKY, LAND, cloud, sun, srt
from ep14_bananas_papa import heart

W, H, FPS = 1920, 1080, 30
DUR = 100.0
GROUND = 880
STAGE = (960, GROUND - 10)
LOG = (1260, GROUND + 5)
BELL_TREE = 1760

NARRACION = [
    (6.0, 13.0, 'Un día, Lola tuvo una idea: ¡hagamos un concierto! Pero... nadie tenía instrumentos.'),
    (15.0, 23.0, 'Coco encontró dos cocos... y al sacudirlos, ¡sonaban como maracas!'),
    (25.0, 33.0, 'Tito levantó la trompa y sopló bien fuerte: ¡prrrú! ¡Una trompeta!'),
    (35.0, 43.0, 'Tomi encontró un tronco hueco. Toc, toc, toc... ¡era un tambor!'),
    (45.0, 53.0, 'Y Pipa estiró el cuello hasta las flores campanita. ¡Tilín, tilín!'),
    (55.0, 61.5, 'Pero cuando tocaron todos a la vez... ¡qué lío! ¡Así no se entendía nada!'),
    (63.0, 70.0, 'Lola les dijo: escuchémonos. Primero uno, después el otro... y después, ¡todos juntos!'),
    (71.0, 88.0, '¡Y así sonaba hermoso! Hasta los pajaritos vinieron a escuchar.'),
    (93.0, 99.0, '¡Juntos sonamos mejor!'),
]

def chaos(t): return 55.0 < t < 62.0
def concert(t): return 71.0 < t < 91.0
ENTRY = {'tomi': 71.0, 'coco': 73.5, 'tito': 76.0, 'pipa': 78.5}   # entran de a uno en el concierto
def playing(name, t, solo):
    a, b = solo
    return a < t < b or chaos(t) or (concert(t) and t > ENTRY[name])

# ---------------- escenario e instrumentos ----------------
def stage(c, t):
    x, y = STAGE
    c.save(); c.translate(x, y + 20); c.scale(1, 0.22)
    ellipse(c, 0, 0, 760, 200); fill(c, hexc('#A1887F'), OUT, 14)
    ellipse(c, 0, -30, 700, 170); c.set_source_rgba(*hexc('#BCAAA4')); c.fill()
    c.restore()
    # guirnalda de flores entre dos palos
    for px in (x - 700, x + 700):
        c.rectangle(px - 12, 420, 24, GROUND - 420); fill(c, hexc('#8D6E63'), OUT, 5)
    pts = [(x - 700 + 1400 * k / 20, 430 + 70 * math.sin(math.pi * k / 20)) for k in range(21)]
    c.move_to(*pts[0])
    for p in pts[1:]: c.line_to(*p)
    c.set_source_rgba(*hexc('#43A047')); c.set_line_width(6); c.stroke()
    for k, (px, py) in enumerate(pts[1:-1]):
        col = ('#FF4081', '#FFD600', '#40C4FF', '#B388FF')[k % 4]
        for i in range(5):
            a = i * 2 * math.pi / 5 + 0.3 * math.sin(t + k)
            ellipse(c, px + 12 * math.cos(a), py + 12 + 12 * math.sin(a), 9, 9); c.set_source_rgba(*hexc(col)); c.fill()
        ellipse(c, px, py + 12, 6, 6); c.set_source_rgba(*hexc('#FFF59D')); c.fill()

def log_drum(c, t, hit):
    x, y = LOG
    c.save(); c.translate(x, y)
    sq = 1 + 0.06 * hit
    c.scale(sq, 1 / sq)
    c.rectangle(-110, -110, 220, 110); fill(c, hexc('#8D5524'), OUT, 6)
    ellipse(c, 0, -110, 110, 30); fill(c, hexc('#D7A86E'), OUT, 6)
    for r in (70, 40): ellipse(c, 0, -110, r, r * 0.27); c.set_source_rgba(*hexc('#8D5524')); c.set_line_width(4); c.stroke()
    for dx in (-60, 0, 60):
        c.move_to(dx, -80); c.line_to(dx + 10, -20); c.set_source_rgba(*hexc('#6D4C41')); c.set_line_width(5); c.stroke()
    c.restore()
    if hit > 0.3:
        for k in range(3):
            a = -math.pi / 2 + (k - 1) * 0.6
            c.move_to(x + 130 * math.cos(a), y - 120 + 130 * math.sin(a)); c.line_to(x + 170 * math.cos(a), y - 120 + 170 * math.sin(a))
            c.set_source_rgba(*OUT); c.set_line_width(6); c.stroke()

BELLS = [(BELL_TREE - 120, 330), (BELL_TREE - 40, 290), (BELL_TREE + 50, 320), (BELL_TREE + 130, 360)]
def bell_tree(c, t, ring):
    x = BELL_TREE
    c.move_to(x - 40, GROUND + 5); c.curve_to(x - 30, 700, x - 25, 450, x - 15, 300)
    c.line_to(x + 15, 300); c.curve_to(x + 25, 450, x + 30, 700, x + 40, GROUND + 5); c.close_path()
    fill(c, hexc('#8D5524'), OUT, 6)
    for (dx, dy, r) in ((-150, 230, 110), (150, 230, 110), (0, 160, 140)):
        ellipse(c, x + dx, dy, r, r * 0.8); c.set_source_rgba(*OUT); c.set_line_width(10); c.stroke()
    for j, (dx, dy, r) in enumerate(((-150, 230, 110), (150, 230, 110), (0, 160, 140))):
        ellipse(c, x + dx, dy, r, r * 0.8); c.set_source_rgba(*hexc(('#43A047', '#43A047', '#4CAF50')[j])); c.fill()
    for k, (bx, by) in enumerate(BELLS):
        sw = 0.5 * ring * math.sin(t * 14 + k)
        c.save(); c.translate(bx, by - 40); c.rotate(sw)
        c.move_to(0, 0); c.line_to(0, 40); c.set_source_rgba(*hexc('#2E7D32')); c.set_line_width(5); c.stroke()
        c.move_to(-26, 80); c.curve_to(-24, 40, -16, 36, 0, 36); c.curve_to(16, 36, 24, 40, 26, 80)
        c.curve_to(14, 72, -14, 72, -26, 80); c.close_path(); fill(c, hexc(('#B388FF', '#FF80AB', '#80D8FF', '#FFD180')[k]), OUT, 4)
        ellipse(c, 0, 80, 7, 7); fill(c, hexc('#FFD600'), OUT, 2)
        c.restore()
        if ring > 0.3: sparkle(c, bx + 30, by + 10, 12 * ring * (0.5 + 0.5 * math.sin(t * 10 + k)), '#FFFFFF')

def coconut(c, x, y, s=1.0):
    ellipse(c, x, y, 26 * s, 24 * s); fill(c, hexc('#A1662F'), OUT, 4); ellipse(c, x - 8 * s, y - 8 * s, 7 * s, 5 * s); c.set_source_rgba(1, 1, 1, 0.45); c.fill()
    for d in (-8, 0, 8): ellipse(c, x + d * s, y - 8 * s, 3 * s, 3 * s); c.set_source_rgba(*OUT); c.fill()

# ---------------- público ----------------
def birds(c, t):
    come = ss(78.0, 82.0, t)
    if come <= 0: return
    for k, (bx, by, col) in enumerate(((240, 300, '#4FC3F7'), (380, 250, '#FFB74D'), (520, 310, '#F06292'), (180, 420, '#AED581'))):
        x = bx - (1 - come) * 600; y = by - 30 * abs(math.sin(t * 3 + k)) * (1 if concert(t) else 0)
        ellipse(c, x, y, 34, 30); fill(c, hexc(col), OUT, 4)
        ellipse(c, x + 14, y - 8, 6, 7); c.set_source_rgba(*OUT); c.fill()
        c.move_to(x + 30, y - 2); c.line_to(x + 48, y + 3); c.line_to(x + 30, y + 8); c.close_path(); fill(c, hexc('#FFA000'), OUT, 2)
        c.save(); c.translate(x - 12, y); c.rotate(-0.4 - 0.6 * math.sin(t * 12 + k))
        ellipse(c, -10, 0, 20, 11); fill(c, hexc(col), OUT, 3); c.restore()

def note_burst(c, x, y, t, k0, cols):
    for k in range(3):
        ph = (t * 0.8 + k / 3 + k0) % 1
        music_note(c, x + 50 * math.sin(ph * 6 + k), y - 200 * ph, math.sin(math.pi * ph), cols[k % len(cols)])

def scribble(c, x, y, t):
    c.save(); c.translate(x, y)
    for k in range(3):
        a = t * 4 + k * 2
        c.move_to(-40, 0)
        for i in range(12):
            c.line_to(-40 + 7 * i, 18 * math.sin(i * 1.8 + a))
        c.set_source_rgba(*OUT); c.set_line_width(5); c.stroke()
        c.translate(0, -30)
    c.restore()

# ---------------- cuadro ----------------
def frame(c, t):
    c.set_source_surface(SKY, 0, 0); c.paint()
    sun(c, t)
    for (x0, y0, s, sp) in ((150, 160, 0.9, 10), (700, 110, 0.7, 7)): cloud(c, (x0 + sp * t) % 2300 - 250, y0, s)
    c.set_source_surface(LAND, 0, 0); c.paint()
    stage(c, t)
    birds(c, t)
    # Pipa y las campanitas
    pipa_ring = playing('pipa', t, (46.0, 53.5))
    ring = 1.0 if pipa_ring else 0.0
    px = kf(t, [(0, 1560), (44.0, 1560), (45.5, BELL_TREE - 330)])
    neck = 300 if not pipa_ring else 560 + 30 * math.sin(t * 6)
    neck = kf(t, [(45.5, 300), (46.8, 560)]) if 45.5 < t < 46.8 else neck
    lean = 230 if pipa_ring or 45.5 < t < 46.8 else 0
    bell_tree(c, t, ring)
    K.put(c, K.pipa, px, GROUND, 0.6, t=t, neck=neck, lean=lean * (ss(45.5, 46.8, t) if t < 47 else 1), look=(1, -0.5) if pipa_ring else (-1, 0),
          walk=t * 7 if 44.0 < t < 45.5 else 0)
    # Tito trompeta
    tito_play = playing('tito', t, (26.0, 33.0))
    tx = 440
    reach = 200 + 60 * abs(math.sin(t * 7)) if tito_play else None
    K.put(c, K.tito, tx, GROUND, 0.68, flip=True, t=t, look=(1, -0.3), reach=reach, lid=0.7 if tito_play else 0.0)
    if tito_play:
        note_burst(c, tx - 360, GROUND - 380, t, 0.1, ['#1E88E5', '#00ACC1', '#3949AB'])
    # Tomi y el tambor-tronco
    tomi_play = playing('tomi', t, (37.0, 43.5))
    hit = abs(math.sin(t * 7)) if tomi_play else 0.0
    log_drum(c, t, hit)
    tmx = kf(t, [(0, 1130), (35.0, 1130), (36.5, LOG[0] - 175)])
    K.put(c, K.tomi, tmx, GROUND, 0.62, t=t, look=(1, 0.2), walk=t * 4 if 35.0 < t < 36.5 else 0)
    if tomi_play:   # palito
        ang = -0.9 + 0.7 * hit
        c.move_to(tmx + 50, GROUND - 120); c.line_to(tmx + 50 + 110 * math.cos(ang), GROUND - 120 - 110 * math.sin(ang) * -1)
        c.set_source_rgba(*OUT); c.set_line_width(14); c.stroke()
        c.move_to(tmx + 50, GROUND - 120); c.line_to(tmx + 50 + 110 * math.cos(ang), GROUND - 120 - 110 * math.sin(ang) * -1)
        c.set_source_rgba(*hexc('#D7A86E')); c.set_line_width(8); c.stroke()
        note_burst(c, LOG[0], LOG[1] - 200, t, 0.4, ['#E53935', '#FF7043', '#8D6E63'])
    # Coco maracas
    coco_play = playing('coco', t, (17.0, 23.5))
    cx = kf(t, [(0, 380), (15.0, 380), (16.0, 800)])
    mood = 'smile'
    if 8.5 < t < 13.0: mood = 'o'
    if chaos(t): mood = 'o'
    if coco_play:
        sh = math.sin(t * 16)
        ar, al = math.radians(-20 + 30 * sh), math.radians(-160 - 30 * sh)
    else:
        ar, al = math.radians(65 + 6 * math.sin(t * 2)), math.radians(115 - 6 * math.sin(t * 2))
    bow = ss(91.0, 92.0, t) * (1 - ss(93.0, 94.0, t))
    for (who, x0, sc) in ((K.coco, cx, 0.55),):
        K.put(who, None, 0, 0, 0) if False else None
    K.put(c, K.coco, cx, GROUND, 0.64, rot=0.25 * bow, t=t, mood=mood, look=(1, -0.2), arm_r=ar, arm_l=al)
    if 15.0 < t < 17.0:   # encuentra los cocos
        coconut(c, cx + 60, GROUND - 20, 1.2); coconut(c, cx + 120, GROUND - 25, 1.2)
    if coco_play or (t > 17.0 and not coco_play):
        for side, a in ((1, ar), (-1, al)):
            hx = cx + side * 0.64 * 78 + 0.64 * 115 * math.cos(a) * (1 if side > 0 else 1)
            hy = GROUND - 0.64 * 180 + 0.64 * 115 * math.sin(a)
            coconut(c, hx, hy, 1.5)
        if coco_play: note_burst(c, cx, GROUND - 330, t, 0.7, ['#8D6E63', '#FFB300', '#43A047'])
    # Lola
    if chaos(t):
        lx, ly = 960 + 30 * math.sin(t * 9), 430
    elif concert(t):
        lx, ly = 960, 380 + 15 * math.sin(t * 3)
    else:
        lx, ly = 960 + 300 * math.sin(t * 0.5), 400 + 20 * math.sin(t * 3)
    K.put(c, K.lola, lx, ly, 0.5, t=t, flap=20, look=(0, 0.4), lid=0.8 if chaos(t) else 0.0)
    if concert(t) or 6.5 < t < 9.0:
        note_burst(c, lx + 40, ly - 160, t, 0.2, ['#E91E63', '#FFD600', '#7C4DFF'])
    if chaos(t):
        for (sx, sy) in ((lx - 200, ly - 100), (cx - 100, GROUND - 400), (tx - 200, GROUND - 450), (LOG[0] + 120, GROUND - 330)):
            scribble(c, sx, sy, t)
    if 63.0 < t < 70.5:   # silencio: todos escuchan
        for k in range(3):
            ph = ((t - 63.0) * 0.5 + k / 3) % 1
            sparkle(c, 960 + 400 * math.cos(k * 2.1), 300 + 60 * k, 14 * math.sin(math.pi * ph), '#FFFFFF')
    if t > 91.0:
        for k in range(8):
            ph = ((t - 91.0) * 0.5 + k / 8) % 1
            heart(c, 300 + 200 * k, 600 - 260 * ph, 1.0, math.sin(math.pi * ph))
    # globitos
    bubble(c, lx, ly - 170, '¡Hagamos un concierto!', (t - 6.6) / 3.2, 44)
    bubble(c, cx, GROUND - 350, '¡No tenemos instrumentos!', (t - 10.0) / 3.0, 42)
    bubble(c, cx, GROUND - 350, '¡Maracas!', (t - 18.0) / 2.6, 54)
    bubble(c, tx - 160, GROUND - 500, '¡Prrrú!', (t - 27.0) / 2.6, 58)
    bubble(c, tmx, GROUND - 250, '¡Toc, toc!', (t - 38.0) / 2.6, 54)
    bubble(c, BELL_TREE - 330, 120, '¡Tilín, tilín!', (t - 48.0) / 2.8, 50)
    bubble(c, lx, ly - 170, '¡Qué lío!', (t - 57.5) / 2.6, 56)
    bubble(c, lx, ly - 170, '¡Escuchémonos!', (t - 63.4) / 3.2, 50)

def overlay(c, t):
    if t < 5.6:
        a = 1 - ss(4.8, 5.5, t)
        c.push_group(); word(c, 'El concierto de la selva', W / 2, 230, 115 * K_back((t - 0.6) / 0.6) + 0.01,
                             colors=['#E91E63', '#FFD600', '#1E88E5', '#43A047'], tilt=0.05, outline=9)
        c.pop_group_to_source(); c.paint_with_alpha(a)
    for name, t0, txt in (('tomi', 71.0, '¡Tambor!'), ('coco', 73.5, '¡Maracas!'), ('tito', 76.0, '¡Trompeta!'), ('pipa', 78.5, '¡Campanitas!')):
        if t0 < t < t0 + 2.2:
            s = K_back((t - t0) / 0.3) * (1 - ss(t0 + 1.9, t0 + 2.2, t))
            word(c, txt, W / 2, 140, 100 * s + 0.01, tilt=0.04, outline=9)
    if t > 93.0:
        s = K_back((t - 93.0) / 0.7)
        word(c, '¡Juntos sonamos', W / 2, 150, 115 * s + 0.01, colors=['#E91E63', '#FFD600', '#1E88E5', '#43A047'], tilt=0.05, outline=10)
        word(c, 'mejor!', W / 2, 270, 125 * s + 0.01, colors=['#43A047', '#E91E63', '#FFD600'], tilt=0.05, outline=10)
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
            c.save(); full(c, t); c.restore(); surf.write_to_png(f'ep26_{t}.png')
    else:
        t0, t1 = (float(args[1]), float(args[2])) if args and args[0] == 'range' else (0, DUR)
        out = sys.stdout.buffer
        for i in range(int(round(t0 * FPS)), int(round(t1 * FPS))):
            c.save(); full(c, i / FPS); c.restore(); surf.flush(); out.write(surf.get_data())
