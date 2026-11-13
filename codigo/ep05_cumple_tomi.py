"""Episodio 5 — El cumpleaños de Tomi (aventurita, 110 s).
Es el cumple de Tomi y los amigos preparan una sorpresa: Tito infla globos, Pipa cuelga banderines,
Coco trae una torta de bananas y Lola ensaya la canción. Se esconden, Tomi llega despacito... ¡sorpresa!

Uso:  python3 ep05_cumple_tomi.py                -> cuadros crudos por stdout
      python3 ep05_cumple_tomi.py range 0 55     -> solo un tramo
      python3 ep05_cumple_tomi.py stills 12 65   -> PNG sueltos"""
import cairo, math, random, sys
import amigos as A, cuerpos as K
from amigos import hexc, ellipse, fill, OUT
from logos import word, sparkle, font
from ep02_puente_del_rio import kf, ss, moving, K_back, music_note, palm
from ep03_donde_esta_tomi import bubble, bush

W, H, FPS = 1920, 1080, 30
DUR = 110.0
GROUND = 880
TABLE_X = 1010
PALM_L, PALM_R = 110, 1810
COLS = ['#FF4081', '#FFD600', '#00B0FF', '#00C853', '#AA00FF', '#FF9100']

# ---------------- escenario ----------------
def make_bg():
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(s)
    g = cairo.LinearGradient(0, 0, 0, H)
    for k, col in enumerate(('#29B6F6', '#81D4FA', '#B3E5FC')): g.add_color_stop_rgb(k / 2, *hexc(col)[:3])
    c.set_source(g); c.paint()
    c.move_to(0, 640); c.curve_to(350, 520, 700, 540, 980, 650); c.curve_to(1250, 560, 1600, 520, 1920, 620)
    c.line_to(1920, H); c.line_to(0, H); c.close_path(); c.set_source_rgba(*hexc('#66BB6A')); c.fill()
    c.move_to(0, 750); c.curve_to(450, 690, 900, 710, 1920, 740); c.line_to(1920, H); c.line_to(0, H); c.close_path()
    c.set_source_rgba(*hexc('#43A047')); c.fill()
    c.rectangle(0, 805, W, H - 805); c.set_source_rgba(*hexc('#8BC34A')); c.fill()
    c.move_to(0, 810); c.curve_to(600, 785, 1300, 785, 1920, 810); c.line_to(1920, 830); c.line_to(0, 830); c.close_path(); c.fill()
    for (fx, col) in ((260, '#FF4081'), (1500, '#E040FB'), (1690, '#FFEA00'), (60, '#FF9100')):
        c.set_line_width(7); c.set_source_rgba(*hexc('#2E7D32')); c.move_to(fx, 975); c.line_to(fx, 930); c.stroke()
        for i in range(6):
            a = i * math.pi / 3; ellipse(c, fx + 20 * math.cos(a), 925 + 20 * math.sin(a), 15, 15)
            c.set_source_rgba(*hexc(col)); c.fill()
        ellipse(c, fx, 925, 12, 12); c.set_source_rgba(*hexc('#FFEB3B')); c.fill()
    return s

BG = make_bg()

def sun(c, t):
    x, y = 1560, 150
    for i in range(12):
        c.save(); c.translate(x, y); c.rotate(i * math.pi / 6 + t * 0.2)
        c.move_to(-20, -115); c.line_to(0, -160); c.line_to(20, -115); c.close_path()
        c.set_source_rgba(*hexc('#FFB300')); c.fill(); c.restore()
    ellipse(c, x, y, 92, 92); fill(c, hexc('#FFEB3B'), hexc('#F9A825'), 7)
    c.set_source_rgba(*OUT); c.set_line_width(7); c.set_line_cap(cairo.LINE_CAP_ROUND)
    for ex in (-32, 32): c.arc(x + ex, y - 12, 15, math.pi * 1.1, math.pi * 1.9); c.stroke()
    c.arc(x, y + 12, 34, 0.15 * math.pi, 0.85 * math.pi); c.stroke()

def clouds(c, t):
    for (x0, y0, s, sp) in ((250, 170, 0.9, 12), (900, 110, 0.7, 8), (1250, 250, 0.55, 15)):
        c.save(); c.translate((x0 + sp * t) % 2300 - 250, y0); c.scale(s, s)
        for (cx, cy, r) in ((0, 0, 60), (70, -30, 75), (150, 0, 60), (75, 20, 60)): ellipse(c, cx, cy, r, r)
        c.set_source_rgba(1, 1, 1, 1); c.fill(); c.restore()

def garland(c, t, upto):
    """Banderines entre las dos palmeras, visibles hasta x = upto."""
    if upto <= PALM_L: return
    y0 = 300
    sag = lambda x: y0 + 110 * math.sin(math.pi * (x - PALM_L) / (PALM_R - PALM_L))
    c.set_source_rgba(*OUT); c.set_line_width(5)
    x = PALM_L; c.move_to(x, sag(x))
    while x < min(upto, PALM_R): x += 20; c.line_to(x, sag(x))
    c.stroke()
    k = 0; x = PALM_L + 50
    while x < min(upto, PALM_R) - 30:
        y = sag(x); sw = 0.08 * math.sin(t * 2.5 + k)
        c.save(); c.translate(x, y); c.rotate(sw)
        c.move_to(-30, 0); c.line_to(30, 0); c.line_to(0, 62); c.close_path(); fill(c, hexc(COLS[k % 6]), OUT, 4)
        c.restore(); x += 90; k += 1

def stump(c):
    x = TABLE_X
    c.rectangle(x - 110, GROUND - 120, 220, 120); fill(c, hexc('#8D6E63'), OUT, 6)
    ellipse(c, x, GROUND - 120, 110, 26); fill(c, hexc('#D7B899'), OUT, 6)
    for r in (70, 40): ellipse(c, x, GROUND - 120, r, r * 0.24); c.set_source_rgba(*hexc('#A1887F')); c.set_line_width(4); c.stroke()

def cake(c, x, y, t, lit=True, s=1.0):
    """Torta de bananas, (x, y) = centro de la base."""
    c.save(); c.translate(x, y); c.scale(s, s)
    c.rectangle(-95, -70, 190, 70); fill(c, hexc('#FFE082'), OUT, 6)
    c.rectangle(-95, -38, 190, 14); c.set_source_rgba(*hexc('#FFFFFF')); c.fill()
    c.rectangle(-95, -38, 190, 14); c.set_source_rgba(*OUT); c.set_line_width(3); c.stroke()
    ellipse(c, 0, -70, 95, 20); fill(c, hexc('#FFF8E1'), OUT, 5)
    for k in range(6):  # cream drips
        ellipse(c, -80 + k * 32, -58, 12, 14); c.set_source_rgba(*hexc('#FFF8E1')); c.fill()
    for (bx, by) in ((-50, -74), (0, -78), (50, -74), (-25, -66), (25, -66)):
        ellipse(c, bx, by, 13, 8); fill(c, hexc('#FFF59D'), hexc('#C9A227'), 3)
    c.rectangle(-7, -150, 14, 72); fill(c, hexc('#4FC3F7'), OUT, 4)
    for k in range(3):
        c.move_to(-7, -142 + k * 22); c.line_to(7, -132 + k * 22); c.set_source_rgba(1, 1, 1, 1); c.set_line_width(4); c.stroke()
    if lit:
        fl = 1 + 0.15 * math.sin(t * 18) + 0.08 * math.sin(t * 31)
        c.save(); c.translate(0, -158); c.scale(1, fl)
        c.move_to(0, -40); c.curve_to(22, -12, 14, 8, 0, 8); c.curve_to(-14, 8, -22, -12, 0, -40); c.close_path()
        fill(c, hexc('#FFB300'), hexc('#E65100'), 3)
        c.move_to(0, -22); c.curve_to(9, -6, 6, 4, 0, 4); c.curve_to(-6, 4, -9, -6, 0, -22); c.close_path()
        c.set_source_rgba(*hexc('#FFF59D')); c.fill(); c.restore()
    c.restore()

def balloon(c, x, y, col, t, ph, string_to=None, size=1.0):
    bx = x + 8 * math.sin(t * 1.3 + ph); by = y + 6 * math.sin(t * 1.7 + ph)
    if string_to:
        c.set_source_rgba(*OUT); c.set_line_width(3)
        c.move_to(bx, by + 62 * size); c.curve_to(bx + 15, by + 120, string_to[0] - 15, string_to[1] - 60, *string_to); c.stroke()
    ellipse(c, bx, by, 48 * size, 60 * size); fill(c, hexc(col), OUT, 5)
    ellipse(c, bx - 16 * size, by - 22 * size, 10 * size, 16 * size); c.set_source_rgba(1, 1, 1, 0.6); c.fill()
    c.move_to(bx - 8 * size, by + 66 * size); c.line_to(bx + 8 * size, by + 66 * size); c.line_to(bx, by + 56 * size); c.close_path()
    fill(c, hexc(col), OUT, 3)

def hat(c, x, y, col, s=1.0, tilt=0.0):
    c.save(); c.translate(x, y); c.rotate(tilt); c.scale(s, s)
    c.move_to(-34, 0); c.line_to(0, -90); c.line_to(34, 0); c.close_path(); fill(c, hexc(col), OUT, 5)
    c.save(); c.move_to(-34, 0); c.line_to(0, -90); c.line_to(34, 0); c.close_path(); c.clip()
    for k in range(4):
        c.move_to(-40, -10 - k * 24); c.line_to(40, -30 - k * 24); c.set_source_rgba(1, 1, 1, 0.8); c.set_line_width(8); c.stroke()
    c.restore()
    ellipse(c, 0, -92, 14, 14); fill(c, hexc('#FFEB3B'), OUT, 4)
    c.restore()

def gift(c, x, y, s=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.rectangle(-55, -90, 110, 90); fill(c, hexc('#E040FB'), OUT, 5)
    c.rectangle(-12, -90, 24, 90); fill(c, hexc('#FFEB3B'), OUT, 3)
    c.rectangle(-62, -105, 124, 22); fill(c, hexc('#CE93D8'), OUT, 5)
    for sx in (-1, 1):
        ellipse(c, sx * 22, -115, 22, 14); fill(c, hexc('#FFEB3B'), OUT, 4)
    c.restore()

CONF = [(random.Random(i).uniform(-1, 1), random.Random(i + 99).uniform(0.4, 1.0), COLS[i % 6], random.Random(i + 7).uniform(0, 6)) for i in range(120)]
def confetti(c, t, t0, x, y, spread=900, dur=3.0):
    p = (t - t0) / dur
    if not 0 <= p <= 1: return
    for (dx, sp, col, ph) in CONF:
        vx, vy = dx * spread, -900 * sp
        tt = p * dur
        px = x + vx * tt * 0.6 + 30 * math.sin(tt * 4 + ph)
        py = y + vy * tt + 500 * tt * tt
        if py > GROUND + 60: continue
        c.save(); c.translate(px, py); c.rotate(tt * 6 + ph)
        c.rectangle(-9, -5, 18, 10); c.set_source_rgba(*hexc(col, 1 - max(0, p - 0.7) / 0.3)); c.fill(); c.restore()

# ---------------- historia ----------------
COCO_X = [(0, 820), (12, 820), (13.5, 560), (24, 560), (25.5, -250), (27, -250), (33.5, TABLE_X - 30),
          (34.5, TABLE_X - 150), (37, TABLE_X - 150), (39.5, 430), (55, 430), (56, 800)]
TITO_X = [(0, 1150), (11, 1150), (13, 1350), (36.5, 1350), (39.5, 640), (55, 640), (56, 620)]
PIPA_X = [(0, 480), (17.5, 480), (18.5, 200), (19, 200), (26.5, 1700), (36.5, 1700), (39.5, 290), (55, 290), (56, 420)]
TOMI_X = [(0, 2100), (40.5, 2100), (55, 1170)]
BALLOONS = [(14.5, '#FF4081', (1120, 560)), (16.5, '#FFD600', (1210, 500)), (18.5, '#00B0FF', (1170, 430)),
            (20.5, '#00C853', (880, 520)), (22.5, '#AA00FF', (820, 450))]
SURPRISE = 55.2
HATS = 57.8
SONG = (63.5, 79.5)
BLOW = 81.0

def umbrella(t): return 0.0

def lola_pos(t):
    if t < 12: return kf(t, [(0, 2050), (5, 1000)]), kf(t, [(0, 300), (5, 520)]) + 15 * math.sin(t * 3)
    if t < 36: return 1000 + 220 * math.sin(t * 0.5), 430 + 30 * math.sin(t * 1.3)
    if t < 37.5: return kf(t, [(36, 1000 + 220 * math.sin(18)), (37, 1650)]), kf(t, [(36, 430), (37, 360)])
    if t < 39.8: return kf(t, [(37.5, 1650), (39.8, 520)]), kf(t, [(37.5, 360), (39.8, 700)])
    if t < SURPRISE: return 520, 700 + 8 * math.sin(t * 3)
    return kf(t, [(SURPRISE, 520), (SURPRISE + 1, 1010)]), kf(t, [(SURPRISE, 700), (SURPRISE + 1, 470)]) + 15 * math.sin(t * 3)

def party(t): return SURPRISE < t < SURPRISE + 2.5 or SONG[0] < t < SONG[1] or 84 < t < 106

def world(c, t):
    c.set_source_surface(BG, 0, 0); c.paint()
    sun(c, t); clouds(c, t)
    palm(c, PALM_L, GROUND, 560, 1, t); palm(c, PALM_R, GROUND, 560, -1, t)
    # garland
    px = kf(t, PIPA_X)
    upto = PALM_L if t < 19 else (px + 40 if t < 26.5 else PALM_R)
    garland(c, t, upto)
    # balloons (tied to the stump)
    tie = (TABLE_X + 90, GROUND - 120)
    for (bt, col, (bx, by)) in BALLOONS:
        if t < bt: continue
        if t < bt + 2.0:  # being inflated on Tito's trunk tip, then floats to its place
            tip = (1350 + 0.6 * 180, GROUND - 0.6 * 115)
            p = (t - bt) / 1.2
            if p < 1:
                balloon(c, tip[0] + 10, tip[1] - 60 * p, col, t, bt, None, 0.3 + 0.7 * p)
                continue
            q = (t - bt - 1.2) / 0.8
            balloon(c, tip[0] + (bx - tip[0]) * q, tip[1] - 60 + (by - tip[1] + 60) * q, col, t, bt, tie)
            continue
        balloon(c, bx, by, col, t, bt, tie)
    stump(c)
    if t >= 34.5:
        if t < BLOW + 0.4: cake(c, TABLE_X, GROUND - 126, t, lit=t > 35.5)
        else: cake(c, TABLE_X, GROUND - 126, t, lit=False)
    # smoke after blowing
    if BLOW + 0.4 < t < BLOW + 2.5:
        q = (t - BLOW - 0.4) / 2.1
        for k in range(3):
            ellipse(c, TABLE_X + 10 * math.sin(q * 6 + k), GROUND - 126 - 170 - 120 * q - k * 25, 12 + 18 * q, 12 + 18 * q)
            c.set_source_rgba(0.85, 0.85, 0.85, 0.6 * (1 - q)); c.fill()
    hiding = 39.5 < t < SURPRISE
    # Pipa
    neck = kf(t, [(18.5, 300), (19.3, 520), (26.5, 520), (27.5, 300), (39.0, 300), (39.8, 110), (SURPRISE, 110), (SURPRISE + 0.5, 300)])
    pb = -25 * abs(math.sin(t * 4.5 + 0.5)) if party(t) else 0
    pl = (1, -0.6) if 19 < t < 26.5 else ((1, 0.2) if hiding else ((0.5, 0) if t > SURPRISE else (0, 0)))
    if 47.5 < t < 50: pb -= 60 * math.sin(math.pi * (t - 47.5) / 2.5)  # peeks
    # Tito
    tx = kf(t, TITO_X)
    tb = -25 * abs(math.sin(t * 4.5 + 1.0)) if party(t) else 0
    reach = 180 if 13.5 < t < 25 else None
    tl = (1, -0.3) if 13 < t < 25 else ((1, 0.2) if hiding or t > SURPRISE else (0, 0))
    # Coco
    cx = kf(t, COCO_X)
    cb = -25 * abs(math.sin(t * 4.5)) if party(t) else 0
    if SURPRISE < t < SURPRISE + 0.8: cb -= 120 * math.sin(math.pi * (t - SURPRISE) / 0.8)
    mood, look = 'smile', (0, 0)
    arm_r, arm_l = math.radians(65 + 6 * math.sin(t * 2)), math.radians(115 - 6 * math.sin(t * 2))
    if 5 < t < 12: look = (1, -0.6)
    if 7.5 < t < 9.5: mood = 'o'
    if 9.5 < t < 12:
        arm_r, arm_l = math.radians(-58 + 25 * math.sin(t * 9)), math.radians(-122 - 25 * math.sin(t * 9)); cb -= 25 * abs(math.sin(t * 5))
    if 13.5 < t < 24: look = (1, -0.4)
    hold = None
    if 27 < t < 34.5: arm_r, arm_l = math.radians(-70), math.radians(-110); look = (1, 0)
    if hiding:
        look = (1, 0); mood = 'closed'
        if 44 < t < 47: arm_l = math.radians(-100 + 15 * math.sin(t * 10)); mood = 'o'   # "shhh"
        if 50 < t < 53: mood = 'o'
    if SURPRISE < t < SURPRISE + 2.5:
        arm_r, arm_l = math.radians(-60), math.radians(-120)
    if party(t) and t > SURPRISE + 2.5:
        arm_r, arm_l = math.radians(-58 + 25 * math.sin(t * 9)), math.radians(-122 - 25 * math.sin(t * 9))
    if 84 < t < 88: arm_r = arm_l = None  # clap
    cpeek = -50 * math.sin(math.pi * (t - 47.5) / 2.5) if 47.5 < t < 50 else 0
    blink = 0.0
    for bt in (3.0, 15.0, 30.0, 42.0, 60.0, 72.0, 90.0, 101.0):
        if abs(t - bt) < 0.12: blink = 1 - abs(t - bt) / 0.12
    # draw hidden ones, then the bush, then visible ones
    def draw_pipa():
        K.put(c, K.pipa, px, GROUND + pb, 0.55, t=t, neck=neck, look=pl, walk=t * 7 if moving(t, PIPA_X) else 0)
    def draw_tito():
        K.put(c, K.tito, tx, GROUND + tb, 0.6, t=t, look=tl, reach=reach, walk=t * 6 if moving(t, TITO_X) else 0)
    def draw_coco():
        if arm_r is None:
            clap = math.radians(-60) + 0.35 * abs(math.sin(t * 10)); ar, al = clap, math.pi - clap
        else: ar, al = arm_r, arm_l
        K.put(c, K.coco, cx, GROUND + cb + cpeek, 0.55, t=t, mood=mood, look=look, lid=blink, arm_r=ar, arm_l=al,
              walk=t * 9 if moving(t, COCO_X) else 0)
    draw_tito() if t < 39 or not hiding else None
    draw_pipa() if not hiding else None
    if hiding:
        draw_pipa(); draw_tito()
        lx, ly = lola_pos(t); K.put(c, K.lola, lx, ly, 0.5, t=t, flap=18, look=(1, 0.3))
        draw_coco()
        bush(c, 330, 795, 200, 120, t); bush(c, 640, 800, 210, 125, t, shake=0.5 if 50 < t < 53 else 0)
    # Tomi
    tmx = kf(t, TOMI_X)
    if t > 40:
        tmb = -20 * abs(math.sin(t * 4.5 + 1.5)) if party(t) and t > SURPRISE + 2.5 else 0
        tlook = (-1, 0) if t < SURPRISE else (-0.8, 0.1)
        K.put(c, K.tomi, tmx, GROUND + tmb, 0.55, t=t, look=tlook, walk=t * 3 if moving(t, TOMI_X) else 0)
        if SURPRISE < t < SURPRISE + 2.5:  # surprised: big O mouth
            ellipse(c, tmx, GROUND - 0.55 * 105, 16, 20); fill(c, hexc('#B71C1C'), OUT, 4)
        if BLOW - 0.2 < t < BLOW + 0.6:  # blowing
            ellipse(c, tmx, GROUND - 0.55 * 105, 10, 10); fill(c, hexc('#B71C1C'), OUT, 4)
            q = (t - BLOW + 0.2) / 0.8
            for k in range(5):
                wx = tmx - 60 - 150 * q - k * 20; wy = GROUND - 80 - 15 * math.sin(k + q * 8)
                c.set_source_rgba(1, 1, 1, 0.8 * (1 - q)); c.set_line_width(6); c.set_line_cap(cairo.LINE_CAP_ROUND)
                c.move_to(wx, wy); c.line_to(wx - 40, wy); c.stroke()
    if not hiding:
        if t >= 39: draw_tito()
        draw_coco()
        if 27 < t < 34.5:  # carrying the cake over his head
            cake(c, cx, GROUND - 0.55 * 480 - 10 + cb, t, lit=False, s=0.8)
        lx, ly = lola_pos(t)
        K.put(c, K.lola, lx, ly - (25 * abs(math.sin(t * 4.5)) if party(t) else 0), 0.5, t=t, flap=20,
              look=(1, 0.3) if 36 < t < 38 else (0.2, 0.6))
        if SONG[0] < t < SONG[1] or 95 < t < 106:
            for k in range(3):
                ph = (t * 0.7 + k / 3) % 1
                music_note(c, lx + 40 + 60 * ph, ly - 150 - 160 * ph, math.sin(math.pi * ph), ['#E91E63', '#1E88E5', '#FF9800'][k])
        # party hats
        if t > HATS:
            s = K_back((t - HATS) / 0.5)
            hat(c, cx, GROUND + cb - 0.55 * 455, '#FF4081', s, 0.1)
            hat(c, tx, GROUND + tb - 0.6 * 455, '#00B0FF', s * 1.1, -0.05)
            hat(c, px, GROUND + pb - 0.55 * (260 + neck + 120), '#00C853', s * 0.9, 0.0)
            hat(c, lx + 4, ly - 0.5 * 330 - (25 * abs(math.sin(t * 4.5)) if party(t) else 0), '#FFD600', s * 0.75, 0.15)
        if t > HATS + 1.2:
            tmb = -20 * abs(math.sin(t * 4.5 + 1.5)) if party(t) and t > SURPRISE + 2.5 else 0
            s = K_back((t - HATS - 1.2) / 0.5)
            hat(c, tmx, GROUND + tmb - 0.55 * 275, '#AA00FF', s * 1.0, -0.1)
    # gift from Tito to Tomi
    if 88 < t < 110:
        gx = kf(t, [(88, tx + 60), (90, tmx - 40)]); gy = GROUND - 10
        if t < 94: gift(c, gx, gy, 0.8)
        else:
            gift(c, gx, gy, 0.8 * (1 - ss(94, 94.3, t)) + 0.0001)
            if t > 94.1:
                c.save(); ball_y = GROUND - 120 - 160 * K_back((t - 94.1) / 0.6)
                from ep04_lluvia_magica import ball
                ball(c, gx, min(GROUND - 40, ball_y) if t < 97 else GROUND - 40, t * 2); c.restore()
    confetti(c, t, SURPRISE, 700, GROUND - 200, 900, 3.2)
    confetti(c, t, BLOW + 0.5, TABLE_X, GROUND - 300, 700, 3.0)
    # bubbles
    lx, ly = lola_pos(t)
    bubble(c, lx, ly - 120, '¡Hoy es el cumple de Tomi!', (t - 5.5) / 3.5, 44)
    bubble(c, cx, GROUND - 300, '¡Hagamos una sorpresa!', (t - 9.3) / 3.0, 44)
    bubble(c, lx, ly - 120, '¡Ahí viene!', (t - 36.4) / 2.2, 48)
    bubble(c, cx, GROUND - 300 + cpeek, '¡Shhh!', (t - 44) / 2.5, 52)
    bubble(c, 760, GROUND - 330, '¡SORPRESA!', (t - SURPRISE) / 2.6, 80)
    bubble(c, tmx, GROUND - 230, '¡Gracias, amigos!', (t - 59.5) / 3.0, 44)

LYRICS = [('¡Feliz cumple, Tomi!', 63.5), ('¡Feliz cumple, Tomi!', 67.5), ('¡Que lo pases muy lindo!', 71.5), ('¡Feliz cumple a vos!', 75.5)]

def overlay(c, t):
    if t < 5.5:
        a = 1 - ss(4.6, 5.4, t)
        c.push_group(); word(c, 'El cumpleaños de Tomi', W / 2, 230, 115 * K_back((t - 0.6) / 0.6) + 0.01, tilt=0.05, outline=9)
        c.pop_group_to_source(); c.paint_with_alpha(a)
    for (txt, t0) in LYRICS:
        if t0 <= t < t0 + 4.0:
            s = K_back((t - t0) / 0.4) * (1 - ss(t0 + 3.7, t0 + 4.0, t))
            word(c, txt, W / 2, 170 + 8 * math.sin(t * 6), 95 * s + 0.01, tilt=0.06, outline=8)
    if t > 99:
        s = K_back((t - 99) / 0.7)
        word(c, '¡Feliz cumpleaños,', W / 2, 170, 105 * s + 0.01, tilt=0.06, outline=9)
        word(c, 'Tomi!', W / 2, 310, 130 * s + 0.01, start=3, tilt=0.06, outline=10)
    a = max(1 - ss(0, 0.8, t), ss(DUR - 2.0, DUR, t))
    if a > 0: c.set_source_rgba(1, 1, 1, a); c.paint()

CAM = [(0, 1.1, 900, 600), (11.5, 1.1, 900, 600), (13.5, 1.3, 1200, 600), (19, 1.3, 1200, 600), (20.5, 1.0, 960, 540),
       (26.5, 1.0, 960, 540), (28, 1.2, 700, 620), (35, 1.2, 900, 620), (36.5, 1.0, 960, 540), (46.5, 1.0, 960, 540),
       (47.5, 1.35, 520, 650), (50.5, 1.35, 520, 650), (51.5, 1.0, 960, 540), (55, 1.0, 960, 540), (56, 1.15, 850, 600),
       (63, 1.1, 900, 600), (79.5, 1.1, 900, 600), (80.5, 1.45, 1080, 700), (83.5, 1.45, 1080, 700), (85, 1.0, 960, 540)]
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
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(surf)
    args = sys.argv[1:]
    if args and args[0] == 'stills':
        for t in map(float, args[1:]):
            c.save(); frame(c, t); c.restore(); surf.write_to_png(f'ep05_{t}.png')
    else:
        t0, t1 = (float(args[1]), float(args[2])) if args and args[0] == 'range' else (0, DUR)
        out = sys.stdout.buffer
        for i in range(int(round(t0 * FPS)), int(round(t1 * FPS))):
            c.save(); frame(c, i / FPS); c.restore(); surf.flush(); out.write(surf.get_data())
