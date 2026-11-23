"""Episodio 3 — ¿Dónde está Tomi? (aventurita, 2 min).
Los amigos juegan a las escondidas. Coco cuenta hasta 10 y encuentra a Lola, Pipa y Tito,
pero Tomi no aparece: se escondió en su caparazón entre las piedras y se quedó dormido.
Pipa estira el cuello, lo ve desde arriba y todos lo despiertan.

Uso:  python3 ep03_donde_esta_tomi.py                -> cuadros crudos por stdout
      python3 ep03_donde_esta_tomi.py range 0 60     -> solo un tramo
      python3 ep03_donde_esta_tomi.py stills 12 65   -> PNG sueltos"""
import cairo, math, random, sys
import amigos as A, cuerpos as K
from amigos import hexc, ellipse, fill, OUT
from logos import word, sparkle, font
from ep02_puente_del_rio import kf, ss, moving, K_back, music_note, palm

W, H, FPS = 1920, 1080, 30
DUR = 120.0
GROUND = 880
TREE_X = 300
PIPA_BUSH = 720
TITO_BUSH = 1640
ROCK_A, TOMI_X, ROCK_B = 1050, 1265, 1430

# ---------------- escenario ----------------
def make_bg():
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(s)
    g = cairo.LinearGradient(0, 0, 0, H)
    g.add_color_stop_rgb(0, *hexc('#29B6F6')[:3]); g.add_color_stop_rgb(0.55, *hexc('#81D4FA')[:3]); g.add_color_stop_rgb(1, *hexc('#B3E5FC')[:3])
    c.set_source(g); c.paint()
    for i in range(12):
        c.save(); c.translate(1720, 140); c.rotate(i * math.pi / 6 + 0.1)
        c.move_to(-20, -115); c.line_to(0, -165); c.line_to(20, -115); c.close_path()
        c.set_source_rgba(*hexc('#FFB300')); c.fill(); c.restore()
    ellipse(c, 1720, 140, 95, 95); fill(c, hexc('#FFEB3B'), hexc('#F9A825'), 7)
    c.move_to(0, 650); c.curve_to(350, 520, 700, 540, 980, 650); c.curve_to(1250, 560, 1600, 520, 1920, 620)
    c.line_to(1920, H); c.line_to(0, H); c.close_path(); c.set_source_rgba(*hexc('#66BB6A')); c.fill()
    c.move_to(0, 750); c.curve_to(450, 690, 900, 710, 1920, 740); c.line_to(1920, H); c.line_to(0, H); c.close_path()
    c.set_source_rgba(*hexc('#43A047')); c.fill()
    c.rectangle(0, 805, W, H - 805); c.set_source_rgba(*hexc('#8BC34A')); c.fill()
    c.move_to(0, 810); c.curve_to(600, 785, 1300, 785, 1920, 810); c.line_to(1920, 830); c.line_to(0, 830); c.close_path()
    c.fill()
    palm(c, 1890, GROUND, 520, -1)
    # tree trunk + back crown
    c.move_to(TREE_X - 45, GROUND); c.curve_to(TREE_X - 30, 700, TREE_X - 40, 560, TREE_X - 25, 430)
    c.line_to(TREE_X + 25, 430); c.curve_to(TREE_X + 40, 560, TREE_X + 30, 700, TREE_X + 45, GROUND); c.close_path()
    fill(c, hexc('#8D5524'), OUT, 6)
    for (cx, cy, r) in ((TREE_X - 150, 330, 95), (TREE_X + 150, 330, 95), (TREE_X, 230, 130), (TREE_X - 90, 250, 100), (TREE_X + 90, 250, 100)):
        ellipse(c, cx, cy, r, r); c.set_source_rgba(*hexc('#2E7D32')); c.fill()
    return s

def crown_front(c, t):
    sw = 3 * math.sin(t * 1.3)
    for (cx, cy, r, col) in ((TREE_X - 120, 380, 85, '#43A047'), (TREE_X + 120, 380, 85, '#43A047'),
                             (TREE_X, 360, 92, '#388E3C'), (TREE_X - 60, 300, 90, '#4CAF50'), (TREE_X + 60, 300, 90, '#4CAF50')):
        ellipse(c, cx + sw, cy, r, r); fill(c, hexc(col), hexc('#1B5E20'), 4)
    for (fx, fy) in ((TREE_X - 120, 340), (TREE_X + 80, 280), (TREE_X + 140, 390)):
        ellipse(c, fx + sw, fy, 13, 13); fill(c, hexc('#FF7043'), OUT, 3)

def bush(c, x, y, rx, ry, t, shake=0.0):
    dx = shake * 6 * math.sin(t * 30)
    blobs = ((-rx * 0.55, 0, ry * 0.75), (rx * 0.55, 0, ry * 0.75), (0, -ry * 0.35, ry * 0.85), (0, ry * 0.25, ry * 0.8))
    for (bx, by, r) in blobs:
        ellipse(c, x + bx + dx, y + by, r * rx / ry if False else r, r)
        c.set_source_rgba(*OUT); c.set_line_width(10); c.stroke()
    for k, (bx, by, r) in enumerate(blobs):
        ellipse(c, x + bx + dx, y + by, r, r); c.set_source_rgba(*hexc(['#2E7D32', '#388E3C', '#43A047', '#2E7D32'][k])); c.fill()
    for (fx, fy) in ((-0.4, -0.3), (0.35, -0.5), (0.1, 0.1)):
        ellipse(c, x + fx * rx + dx, y + fy * ry, 12, 12); fill(c, hexc('#F06292'), OUT, 3)

def rock(c, x, s):
    c.save(); c.translate(x, GROUND); c.scale(s, s)
    c.move_to(-200, -20); c.curve_to(-200, -230, 200, -230, 200, -20); c.close_path()
    fill(c, hexc('#9E9E9E'), OUT, 6)
    for (hx, hy, r) in ((-80, -110, 30), (60, -80, 22), (20, -150, 16)):
        ellipse(c, hx, hy, r, r * 0.7); c.set_source_rgba(*hexc('#BDBDBD')); c.fill()
    c.rectangle(-205, -30, 410, 26); fill(c, hexc('#757575'), OUT, 5)
    c.restore()

BG = make_bg()

def clouds(c, t):
    for (x0, y0, s, sp) in ((150, 150, 0.9, 12), (820, 100, 0.7, 8), (1300, 230, 0.6, 15)):
        c.save(); c.translate((x0 + sp * t) % 2300 - 250, y0); c.scale(s, s)
        for (cx, cy, r) in ((0, 0, 60), (70, -30, 75), (150, 0, 60), (75, 20, 60)): ellipse(c, cx, cy, r, r)
        c.set_source_rgba(1, 1, 1, 1); c.fill(); c.restore()

def bubble(c, x, y, text, p, size=48):
    """Globito de diálogo con la punta hacia abajo, centrado en x, apoyado en y."""
    if p <= 0: return
    s = K_back(min(1.0, p / 0.25)) * (1 - ss(0.85, 1.0, p))
    if s <= 0.01: return
    font(c, size); w = c.text_extents(text).x_advance + 50; h = size * 1.5
    c.save(); c.translate(x, y); c.scale(s, s)
    r = h / 2
    c.new_path(); c.arc(-w / 2 + r, -h - 20 + r, r, math.pi / 2, 3 * math.pi / 2); c.arc(w / 2 - r, -h - 20 + r, r, -math.pi / 2, math.pi / 2)
    c.close_path(); c.move_to(-18, -22); c.line_to(0, 8); c.line_to(18, -22)
    c.set_source_rgba(*OUT); c.set_line_width(10); c.stroke_preserve(); c.set_source_rgba(1, 1, 1, 1); c.fill()
    c.new_path(); c.arc(-w / 2 + r, -h - 20 + r, r, math.pi / 2, 3 * math.pi / 2); c.arc(w / 2 - r, -h - 20 + r, r, -math.pi / 2, math.pi / 2)
    c.close_path(); c.fill()
    c.move_to(-18, -24); c.line_to(0, 6); c.line_to(18, -24); c.fill()
    word(c, text, 0, -20 - h * 0.3, size, outline=3)
    c.restore()

def qmark(c, x, y, t, ph=0.0, ch='?'):
    bob = 10 * math.sin(t * 4 + ph)
    font(c, 90)
    c.save(); c.translate(x, y + bob); c.rotate(0.15 * math.sin(t * 3 + ph))
    word(c, ch, 0, 0, 90, colors=['#FF9100' if ch == '?' else '#FF1744'], outline=6)
    c.restore()

def zzz(c, x, y, t, t0, t1, big=1.0):
    if not t0 < t < t1: return
    font(c, 50)
    for k in range(3):
        p = ((t - t0) / 2.4 - k / 3.0)
        if p < 0: continue
        p %= 1.0
        a = math.sin(math.pi * p) * min(1, (t1 - t) / 0.5)
        c.save(); c.translate(x + 90 * p + 15 * math.sin(p * 7), y - 170 * p * big)
        c.set_font_size((34 + 40 * p) * big); c.move_to(0, 0); c.text_path('Z')
        c.set_source_rgba(1, 1, 1, a); c.fill_preserve(); c.set_source_rgba(0.24, 0.2, 0.55, a); c.set_line_width(4); c.stroke()
        c.restore()

# ---------------- historia ----------------
COUNT_T0, COUNT_DT = 8.5, 1.1
COCO_X = [(0, 960), (22.5, 960), (27.0, 430), (32.5, 430), (36.5, 600), (43.0, 600), (51.0, 1500),
          (57.5, 1500), (60.0, 1450), (65.5, 470), (68.5, 470), (74.0, 1050), (88.0, 1050), (89.5, 1110)]
PIPA_X = [(0, 470), (9.5, 470), (13.0, PIPA_BUSH), (40.6, PIPA_BUSH), (42.5, 920), (74.0, 920), (76.0, 960)]
TITO_X = [(0, 1250), (10.0, 1250), (15.0, TITO_BUSH), (55.6, TITO_BUSH), (57.5, 1800), (76.0, 1800), (82.0, 1540)]
TOMI_W = [(0, 770), (10.5, 770), (19.0, TOMI_X)]
FOUND = {'lola': 30.0, 'pipa': 40.0, 'tito': 55.0, 'tomi': 95.0}

def coco_state(t):
    x = kf(t, COCO_X); y = GROUND
    st = dict(mood='smile', look=(0, 0), lid=0.0, arm_r=math.radians(65 + 6 * math.sin(t * 2)),
              arm_l=math.radians(115 - 6 * math.sin(t * 2)), arm_len=115, walk=t * 8 if moving(t, COCO_X) else 0, tilt=0.0, sad=0.0)
    if 1 < t < 6:
        y -= 30 * abs(math.sin(t * 4.5))
        st['arm_r'], st['arm_l'] = math.radians(-58 + 25 * math.sin(t * 9)), math.radians(-122 - 25 * math.sin(t * 9))
    if 6 <= t < 20.2:  # covers his eyes and counts
        k = ss(6, 6.8, t) * (1 - ss(19.7, 20.2, t))
        st['arm_r'] = st['arm_r'] * (1 - k) + math.radians(-100) * k
        st['arm_l'] = st['arm_l'] * (1 - k) + math.radians(-80) * k
        st['arm_len'] = 115 + 50 * k
        st['tilt'] = math.radians(4) * math.sin(t * 2.5) * k
    if 20.2 <= t < 23: st['look'] = (math.sin(t * 2.5), -0.2)
    if 23 <= t < 27: st['look'] = (-1, -0.3)
    if 27 <= t < 30:
        st['look'] = (-0.3, -1); st['mood'] = 'closed' if t < 28.5 else 'o'
        if t > 28.5: st['arm_l'] = math.radians(-115)
    if 30 <= t < 32.5: st['look'] = (-0.3, -1); y -= 30 * abs(math.sin(t * 6))
    if 32.5 <= t < 43: st['look'] = (1, -0.6)
    if 38 <= t < 40: st['mood'] = 'o'; st['arm_r'] = math.radians(-60)
    if 40 <= t < 42: y -= 30 * abs(math.sin(t * 6))
    if 43 <= t < 51: st['look'] = (1, 0)
    if 51 <= t < 55: st['look'] = (1, -0.4); st['mood'] = 'closed'
    if 54 <= t < 55: st['mood'] = 'o'; st['arm_r'] = math.radians(-50)
    if 55 <= t < 57: y -= 30 * abs(math.sin(t * 6))
    if 57.5 <= t < 76:  # where is Tomi?
        st['mood'] = 'closed'; st['look'] = (math.sin(t * 1.7), -0.2)
        if 58 < t < 62 or 66 < t < 68.5:
            st['arm_r'], st['arm_l'] = math.radians(-30), math.radians(-150)
            st['mood'] = 'o'
        if 74 <= t: st['look'] = (0, -1)
    if 76 <= t < 88: st['look'] = (-0.6, -1) if t < 81 else (1, 0.5); st['mood'] = 'closed' if t < 81 else 'o'
    if 89.5 <= t < 92.5:  # knock knock
        st['look'] = (1, 0.6); st['mood'] = 'closed'
        st['arm_r'] = math.radians(20 + 25 * max(0, math.sin((t - 90.3) * math.pi * 1.6)))
    if 92.5 <= t < 95: st['look'] = (1, 0.6); st['mood'] = 'o'
    if 95 <= t < 98: y -= 30 * abs(math.sin(t * 6)); st['look'] = (1, 0.4)
    if 98 <= t < 110:
        y -= 30 * abs(math.sin(t * 4.5))
        st['arm_r'], st['arm_l'] = math.radians(-58 + 25 * math.sin(t * 9)), math.radians(-122 - 25 * math.sin(t * 9))
    if t >= 110:
        st['arm_r'], st['arm_l'] = math.radians(-58 + 25 * math.sin(t * 9)), math.radians(65)
    for bt in (3.5, 23.5, 34.0, 46.0, 63.0, 71.0, 86.0, 100.0, 113.0):
        if abs(t - bt) < 0.12: st['lid'] = 1 - abs(t - bt) / 0.12
    st['x'], st['y'] = x, y
    return st

def lola_pos(t):
    if t < 9: return 1460, 560 - (25 * abs(math.sin(t * 4.5)) if 1 < t < 6 else 0) + 12 * math.sin(t * 3), 'out'
    if t < 12: return kf(t, [(9, 1460), (12, TREE_X)]), kf(t, [(9, 560), (10.5, 300), (12, 445)]), 'out'
    if t < 30: return TREE_X + (6 * math.sin(t * 20) if 26 < t < 30 else 0), 445, 'tree'
    if t < 32.5: return kf(t, [(30, TREE_X), (31, 430)]), kf(t, [(30, 445), (31, 300), (32.5, 330)]), 'out'
    cx = kf(t - 0.8, COCO_X)
    if t < 88: return kf(t, [(32.5, 430), (34, cx - 150)]) if t < 34 else cx - 150, 520 + 15 * math.sin(t * 3), 'out'
    return kf(t, [(88, kf(88 - 0.8, COCO_X) - 150), (90, TOMI_X)]), kf(t, [(88, 520), (90, 450)]) + 15 * math.sin(t * 3) - (30 * abs(math.sin(t * 4.5)) if 98 < t < 110 else 0), 'out'

def tomi_state(t):
    hide = 0.0; lid = 0.0; mood = 'smile'
    x = kf(t, TOMI_W)
    if 19.0 <= t < 96.0:
        hide = 1.0 if t > 19.4 else ss(19.0, 19.4, t)
        if 92.0 < t < 96.0:
            hide = kf(t, [(92.0, 1.0), (92.6, 0.35), (95.4, 0.35), (96.0, 0.0)])
            lid = 0.6 if t < 94.6 else 0.0
            mood = 'o' if 93.0 < t < 94.4 else 'smile'
    return x, hide, lid, mood

CAM = [  # (t, zoom, x, y)   x=None -> sigue a Coco
    (0, 1.0, 960, 540), (20, 1.0, 960, 540), (22.5, 1.25, 900, 620), (24.5, 1.35, 520, 600), (32, 1.35, 520, 600),
    (34, 1.3, 700, 620), (42, 1.3, 760, 620), (44, 1.25, None, 620), (56, 1.25, None, 620), (58, 1.0, 960, 540),
    (75, 1.0, 960, 540), (77, 1.15, 1080, 500), (87, 1.15, 1080, 500), (89, 1.4, 1200, 640), (97, 1.4, 1200, 640),
    (99.5, 1.0, 960, 540)]

def camera(t):
    z = kf(t, [(a, b) for a, b, _, _ in CAM]); y = kf(t, [(a, d) for a, _, _, d in CAM])
    keys = [(a, (c_ if c_ is not None else kf(a, COCO_X))) for a, _, c_, _ in CAM]
    x = kf(t, keys)
    if 44 <= t <= 56: x = kf(t, COCO_X)
    x = max(W / (2 * z), min(W - W / (2 * z), x)); y = max(H / (2 * z), min(H - H / (2 * z), y))
    return x, y, z

def world(c, t):
    c.set_source_surface(BG, 0, 0); c.paint()
    clouds(c, t)
    lx, ly, lmode = lola_pos(t)
    cs = coco_state(t)
    if lmode == 'tree':
        K.put(c, K.lola, lx, ly, 0.5, t=t, flap=None, look=(1, 0.3))
    crown_front(c, t)
    rock(c, ROCK_A, 0.6); rock(c, ROCK_B, 0.5)
    # Pipa + her bush
    px = kf(t, PIPA_X)
    neck = kf(t, [(76, 300), (78, 620), (85, 620), (87, 300)])
    lean = kf(t, [(81.5, 0), (83, 300), (85.5, 300), (87, 0)])
    plook = (1, 0.8) if 79 < t < 87 else ((-0.8, 0.2) if 33 < t < 40 else (0.3, 0))
    pbob = -25 * abs(math.sin(t * 4.5)) if (1 < t < 6 or 98 < t < 110) else 0
    if 38.5 < t < 40.5: neck += 12 * math.sin(t * 12)
    pipa_hidden = 9.5 < t < 41.5
    if not pipa_hidden: bush(c, PIPA_BUSH, 790, 170, 105, t)
    K.put(c, K.pipa, px, GROUND + pbob, 0.55, t=t, neck=neck, lean=lean, look=plook, walk=t * 7 if moving(t, PIPA_X) else 0)
    if pipa_hidden: bush(c, PIPA_BUSH, 790, 170, 105, t, shake=1.0 if 38.5 < t < 40.2 else 0.0)
    # Tito + his bush
    tx = kf(t, TITO_X)
    tbob = -25 * abs(math.sin(t * 4.5)) if (1 < t < 6 or 98 < t < 110) else 0
    if 55 < t < 56.2: tbob = -60 * math.sin(math.pi * (t - 55) / 1.2)
    tlook = (-1, 0) if 52 < t < 56 else ((-1, -0.6) if 79 < t < 90 else (-0.4, 0))
    tito_hidden = 11.0 < t < 56.6
    if not tito_hidden: bush(c, TITO_BUSH, 790, 125, 150, t)
    K.put(c, K.tito, tx + (5 * math.sin(t * 18) if 50 < t < 55 else 0), GROUND + tbob, 0.6, t=t, look=tlook,
          walk=t * 6 if moving(t, TITO_X) else 0)
    if tito_hidden: bush(c, TITO_BUSH, 790, 125, 150, t, shake=1.0 if 53.5 < t < 55 else 0.0)
    # Tomi
    tmx, hide, lid, mood = tomi_state(t)
    tbob2 = -20 * abs(math.sin(t * 4.5)) if (1 < t < 6 or 98 < t < 110) else 0
    K.put(c, K.tomi, tmx, GROUND + (tbob2 if hide == 0 else 0), 0.55, t=t, look=(-0.6, -0.2) if t > 96 else (0.4, 0),
          walk=t * 3 if moving(t, TOMI_W) else 0, hide=hide, lid=lid, mood=mood)
    zzz(c, TOMI_X + 30, GROUND - 120, t, 46.5, 51.5, 0.8)
    zzz(c, TOMI_X + 30, GROUND - 120, t, 78.5, 91.5, 1.2)
    for (t0, dx) in ((90.3, 40), (90.95, 110)):
        q = (t - t0) / 0.6
        if 0 <= q <= 1:
            word(c, 'toc', TOMI_X + dx, GROUND - 190 - 40 * q, 50 * K_back(q / 0.3) + 0.01, colors=['#8D6E63'], outline=5)
    # Coco
    K.put(c, K.coco, cs['x'], cs['y'], 0.55, t=t, look=cs['look'], lid=cs['lid'], mood=cs['mood'], sad=cs['sad'],
          arm_r=cs['arm_r'], arm_l=cs['arm_l'], arm_len=cs['arm_len'], walk=cs['walk'], head_tilt=cs['tilt'])
    # Lola flying
    if lmode == 'out':
        K.put(c, K.lola, lx, ly, 0.5, t=t, flap=20, look=(1, 0.4) if t < 88 else (0.3, 0.8))
        if 98 < t < 112:
            for k in range(3):
                ph = (t * 0.7 + k / 3) % 1
                music_note(c, lx + 40 + 60 * ph + 20 * math.sin(ph * 8), ly - 150 - 160 * ph, math.sin(math.pi * ph), ['#E91E63', '#1E88E5', '#FF9800'][k])
    # question marks & exclamation
    if 58.5 < t < 76:
        a = ss(58.5, 59, t)
        qmark(c, cs['x'] + 40, cs['y'] - 300, t, 0)
        qmark(c, lx + 40, ly - 160, t, 1.3)
        qmark(c, px + 30, GROUND - 0.55 * 640 - 70, t, 2.1)
        qmark(c, tx, GROUND - 330, t, 3.0)
    if 80.5 < t < 84.5:
        hx = px + lean * 0.55; hy = GROUND - 0.55 * (260 + neck) - 110
        qmark(c, hx + 30, hy - 10, t, 0.4, '!')
    # speech bubbles
    bubble(c, cs['x'], cs['y'] - 290, '¡Allá voy!', (t - 20.3) / 2.3)
    bubble(c, cs['x'], cs['y'] - 290, '¡Te encontré!', (t - 30.2) / 2.2)
    bubble(c, cs['x'], cs['y'] - 290, '¡Te encontré!', (t - 40.2) / 2.2)
    bubble(c, cs['x'], cs['y'] - 290, '¡Te encontré!', (t - 55.2) / 2.2)
    bubble(c, cs['x'] + 40, cs['y'] - 400, '¿Dónde está Tomi?', (t - 58.6) / 3.4, 52)
    bubble(c, px + lean * 0.55 - 40, GROUND - 0.55 * (260 + neck) - 150, '¡Ahí está!', (t - 83.2) / 2.6)
    bubble(c, cs['x'], cs['y'] - 290, '¡Te encontramos!', (t - 95.2) / 2.6)
    # sparkles when someone is found
    for who, t0 in FOUND.items():
        q = (t - t0) / 1.0
        if 0 <= q <= 1:
            fx, fy = {'lola': (430, 330), 'pipa': (PIPA_BUSH, 560), 'tito': (TITO_BUSH, 640), 'tomi': (TOMI_X, 780)}[who]
            for k in range(8):
                a = k * math.pi / 4
                sparkle(c, fx + 140 * q * math.cos(a), fy + 110 * q * math.sin(a), 28 * math.sin(math.pi * q), '#FFF59D' if k % 2 else '#FFFFFF')

def hud(c, t):
    """Arriba a la izquierda: a quién ya encontró Coco."""
    if t < 20.5: return
    a = ss(20.5, 21.2, t) * (1 - ss(108, 109, t))
    if a <= 0: return
    c.push_group()
    x0, y0 = 30, 30
    c.new_path(); r = 50
    c.arc(x0 + r, y0 + r, r, math.pi, 1.5 * math.pi); c.arc(x0 + 470 - r, y0 + r, r, 1.5 * math.pi, 0)
    c.arc(x0 + 470 - r, y0 + 130 - r, r, 0, 0.5 * math.pi); c.arc(x0 + r, y0 + 130 - r, r, 0.5 * math.pi, math.pi); c.close_path()
    c.set_source_rgba(1, 1, 1, 0.85); c.fill_preserve(); c.set_source_rgba(*OUT); c.set_line_width(6); c.stroke()
    for k, who in enumerate(('lola', 'pipa', 'tito', 'tomi')):
        cx, cy = x0 + 70 + k * 110, y0 + 68
        if t >= FOUND[who]:
            s = 0.3 * K_back((t - FOUND[who]) / 0.5)
            if who == 'pipa': A.draw(c, who, cx, cy + 10, s * 0.85)
            elif who == 'tito': A.draw(c, who, cx, cy, s * 0.75)
            else: A.draw(c, who, cx, cy, s)
        else:
            ellipse(c, cx, cy, 42, 42); fill(c, hexc('#CFD8DC'), hexc('#90A4AE'), 5)
            word(c, '?', cx, cy + 22, 60, colors=['#78909C'], outline=3)
    c.pop_group_to_source(); c.paint_with_alpha(a)

def overlay(c, t):
    if t < 5.5:
        a = 1 - ss(4.6, 5.4, t)
        c.push_group(); word(c, '¿Dónde está Tomi?', W / 2, 230, 120 * K_back((t - 0.6) / 0.6) + 0.01, tilt=0.05, outline=9)
        c.pop_group_to_source(); c.paint_with_alpha(a)
    # counting 1..10
    for k in range(10):
        t0 = COUNT_T0 + k * COUNT_DT
        if t0 <= t < t0 + COUNT_DT:
            s = K_back((t - t0) / 0.35)
            word(c, str(k + 1), W / 2, 260, 230 * s + 0.01, colors=[['#FF4081', '#FF9100', '#FFD600', '#00C853', '#00B0FF', '#AA00FF'][k % 6]], outline=12)
    hud(c, t)
    if t > 109.5:
        s = K_back((t - 109.5) / 0.7)
        word(c, '¡Los amigos', W / 2, 200, 120 * s + 0.01, tilt=0.06, outline=10)
        word(c, 'se cuidan!', W / 2, 340, 120 * s + 0.01, start=3, tilt=0.06, outline=10)
    a = max(1 - ss(0, 0.8, t), ss(DUR - 2.0, DUR, t))
    if a > 0: c.set_source_rgba(1, 1, 1, a); c.paint()

def frame(c, t):
    cx, cy, z = camera(t)
    c.save(); c.translate(W / 2, H / 2); c.scale(z, z); c.translate(-cx, -cy)
    world(c, t)
    c.restore()
    overlay(c, t)

if __name__ == '__main__':
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(surf)
    args = sys.argv[1:]
    if args and args[0] == 'stills':
        for t in map(float, args[1:]):
            c.save(); frame(c, t); c.restore(); surf.write_to_png(f'ep03_{t}.png')
    else:
        t0, t1 = (float(args[1]), float(args[2])) if args and args[0] == 'range' else (0, DUR)
        out = sys.stdout.buffer
        for i in range(int(round(t0 * FPS)), int(round(t1 * FPS))):
            c.save(); frame(c, i / FPS); c.restore(); surf.flush(); out.write(surf.get_data())
