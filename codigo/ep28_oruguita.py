"""Episodio 28 — La oruguita Mari (100 s). Aventurita (estándar Estudio de video GR, perfil Cuentos).
Coco encuentra a Mari, una oruguita que come hojas y crece. Le da sueño, sube a una rama y se envuelve en su
capullo. Los amigos esperan días y noches cuidándola... ¡y sale una mariposa enorme de colores! Mari vuela por
primera vez, se posa en cada amigo y las flores se abren donde pasa. Enseñanza: cada uno a su tiempo.
(Mari es personaje invitado y se dibuja acá: `oruga()` y `mariposa()`.)

Uso:  python3 ep28_oruguita.py              -> cuadros crudos por stdout
      python3 ep28_oruguita.py range 0 50   -> solo un tramo
      python3 ep28_oruguita.py stills 20 70 -> PNG sueltos
      python3 ep28_oruguita.py srt 5.5      -> subtítulos .srt de la narración"""
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
BUSH = (930, 790)
BRANCH_Y = 400
COCOON = (1190, BRANCH_Y + 20)

NARRACION = [
    (6.0, 13.5, 'Un día, Coco encontró a alguien chiquito en una hoja... ¡era Mari, una oruguita!'),
    (15.0, 23.5, 'Mari comía y comía hojas, ¡ñam, ñam! Y crecía cada vez más.'),
    (25.0, 34.0, 'Hasta que le dio sueño. Subió a una rama y se envolvió en un capullo.'),
    (36.0, 45.0, '¿Cuándo va a salir? Pasó un día, y una noche... y los amigos la cuidaban con paciencia.'),
    (46.5, 53.5, 'Hasta que una mañana, el capullo se movió... ¡crac, crac!'),
    (55.0, 63.0, 'Y salió Mari... ¡convertida en una mariposa de colores!'),
    (65.0, 77.0, 'Mari voló por primera vez, y saludó a cada uno de sus amigos.'),
    (79.0, 90.0, 'Y por donde pasaba, se abrían las flores. ¡Gracias por esperarme, amigos!'),
    (92.0, 99.0, 'Porque cada uno crece... a su tiempo.'),
]

# ---------------- Mari ----------------
def oruga(c, x, y, s, t, chew=False, sleepy=0.0, mood='smile'):
    c.save(); c.translate(x, y); c.scale(s, s)
    for i in range(5, 0, -1):   # segmentos (de la cola a la cabeza)
        bx = -34 * i; by = -8 * math.sin(t * 4 - i * 0.9)
        ellipse(c, bx, by, 26, 24); fill(c, hexc('#8BC34A' if i % 2 else '#7CB342'), OUT, 4)
        ellipse(c, bx, by + 22, 6, 5); fill(c, hexc('#558B2F'), OUT, 2)
        ellipse(c, bx - 6, by - 10, 5, 5); c.set_source_rgba(*hexc('#FFEB3B')); c.fill()
    hy = -10 - 6 * math.sin(t * 4)
    for d in (-1, 1):   # antenitas
        c.move_to(8 + 10 * d, hy - 26); c.curve_to(10 + 14 * d, hy - 50, 20 + 18 * d, hy - 56, 26 + 18 * d, hy - 52)
        c.set_source_rgba(*OUT); c.set_line_width(4); c.stroke()
        ellipse(c, 26 + 18 * d, hy - 52, 6, 6); fill(c, hexc('#FF7043'), OUT, 2)
    ellipse(c, 10, hy, 34, 32); fill(c, hexc('#9CCC65'), OUT, 5)
    lid = sleepy
    for ex in (-2, 24):
        if lid > 0.6:
            c.arc(ex, hy - 6, 7, 0.15 * math.pi, 0.85 * math.pi); c.set_source_rgba(*OUT); c.set_line_width(4); c.stroke()
        else:
            ellipse(c, ex, hy - 8, 8, 10); c.set_source_rgba(1, 1, 1, 1); c.fill()
            ellipse(c, ex + 2, hy - 6, 5, 7); c.set_source_rgba(*OUT); c.fill()
            ellipse(c, ex + 3, hy - 9, 2, 2); c.set_source_rgba(1, 1, 1, 1); c.fill()
    for ex in (-10, 34): ellipse(c, ex, hy + 8, 7, 4); c.set_source_rgba(*hexc('#F48FB1')); c.fill()
    if chew:
        o = abs(math.sin(t * 10))
        ellipse(c, 12, hy + 14, 7, 3 + 5 * o); c.set_source_rgba(*hexc('#C62828')); c.fill()
    else:
        c.arc(12, hy + 8, 9, 0.15 * math.pi, 0.85 * math.pi); c.set_source_rgba(*OUT); c.set_line_width(4); c.stroke()
    c.restore()

WING = [('#FF4081', '#FFD600'), ('#7C4DFF', '#40C4FF')]
def mariposa(c, x, y, s, t, open_=1.0, flap=0.0):
    """open_ 0..1 despliega las alas; flap = fase del aleteo."""
    c.save(); c.translate(x, y); c.scale(s, s)
    f = 0.25 + 0.75 * abs(math.cos(flap)) if flap else 1.0
    for side in (-1, 1):
        c.save(); c.scale(side * f * open_ + 0.001, 1)
        for (dy, rx, ry, cols, rot) in ((-35, 95, 70, WING[0], -0.35), (40, 70, 55, WING[1], 0.35)):
            c.save(); c.translate(70, dy); c.rotate(rot)
            ellipse(c, 0, 0, rx, ry); fill(c, hexc(cols[0]), OUT, 5)
            ellipse(c, 10, 0, rx * 0.55, ry * 0.55); c.set_source_rgba(*hexc(cols[1])); c.fill()
            for k in range(3): ellipse(c, -rx * 0.55 + 20 * k, -ry * 0.6 + 10 * k, 8, 8); c.set_source_rgba(1, 1, 1, 0.9); c.fill()
            c.restore()
        c.restore()
    ellipse(c, 0, 10, 16, 60); fill(c, hexc('#6D4C41'), OUT, 4)
    for d in (-1, 1):
        c.move_to(4 * d, -55); c.curve_to(12 * d, -85, 26 * d, -95, 34 * d, -92); c.set_source_rgba(*OUT); c.set_line_width(4); c.stroke()
        ellipse(c, 34 * d, -92, 6, 6); fill(c, hexc('#FFD600'), OUT, 2)
    ellipse(c, 0, -48, 24, 22); fill(c, hexc('#8D6E63'), OUT, 4)
    for ex in (-9, 9):
        ellipse(c, ex, -52, 6, 8); c.set_source_rgba(1, 1, 1, 1); c.fill()
        ellipse(c, ex + 1, -51, 4, 5); c.set_source_rgba(*OUT); c.fill()
    for ex in (-15, 15): ellipse(c, ex, -40, 5, 3); c.set_source_rgba(*hexc('#F48FB1')); c.fill()
    c.arc(0, -42, 7, 0.15 * math.pi, 0.85 * math.pi); c.set_source_rgba(*OUT); c.set_line_width(3); c.stroke()
    c.restore()

def cocoon(c, t, wrap, crack):
    x, y = COCOON
    if wrap <= 0: return
    wig = 0.12 * math.sin(t * 14) * ss(46.5, 47.0, t) * (1 - ss(53.0, 53.5, t))
    c.save(); c.translate(x, y); c.rotate(wig)
    c.move_to(0, 0); c.line_to(0, 30); c.set_source_rgba(*hexc('#A1887F')); c.set_line_width(5); c.stroke()
    h = 170 * wrap
    c.move_to(0, 30); c.curve_to(70, 40, 70, 30 + h, 0, 40 + h); c.curve_to(-70, 30 + h, -70, 40, 0, 30); c.close_path()
    fill(c, hexc('#C5E1A5'), OUT, 5)
    for k in range(int(6 * wrap)):
        yy = 50 + 26 * k
        c.move_to(-48, yy); c.curve_to(-20, yy + 14, 20, yy - 6, 48, yy + 8); c.set_source_rgba(*hexc('#9CCC65')); c.set_line_width(4); c.stroke()
    if crack > 0:
        zz = [(-30, 70), (-12, 90), (-22, 112), (0, 130), (-8, 150)]
        n = int(crack * (len(zz) - 1))
        if n >= 1:
            c.move_to(*zz[0])
            for p in zz[1:n + 1]: c.line_to(*p)
            c.set_source_rgba(*OUT); c.set_line_width(5); c.stroke()
    c.restore()

def bush(c, t):
    x, y = BUSH
    for (dx, dy, r, col) in ((-110, 30, 90, '#388E3C'), (110, 30, 90, '#388E3C'), (0, -20, 110, '#43A047'), (-40, 50, 80, '#4CAF50'), (60, 55, 80, '#4CAF50')):
        ellipse(c, x + dx, y + dy, r, r * 0.8); fill(c, hexc(col), OUT, 6)
    eaten = ss(15.5, 23.0, t)
    for k in range(6):   # hojas que Mari se come
        if k / 6 < eaten: continue
        a = -2.6 + k * 0.55
        lx, ly = x + 120 * math.cos(a), y - 30 + 90 * math.sin(a)
        c.save(); c.translate(lx, ly); c.rotate(a + 1.57)
        c.move_to(0, -34); c.curve_to(26, -16, 26, 16, 0, 34); c.curve_to(-26, 16, -26, -16, 0, -34); c.close_path()
        fill(c, hexc('#8BC34A'), OUT, 4); c.restore()

def tree(c, t):
    x = 1700
    c.move_to(x - 60, GROUND + 5); c.curve_to(x - 50, 700, x - 45, 300, x - 30, 80)
    c.line_to(x + 30, 80); c.curve_to(x + 45, 300, x + 50, 700, x + 60, GROUND + 5); c.close_path()
    fill(c, hexc('#8D5524'), OUT, 6)
    c.move_to(x - 40, BRANCH_Y + 20); c.curve_to(x - 250, BRANCH_Y + 10, x - 450, BRANCH_Y, x - 620, BRANCH_Y + 5)
    c.set_source_rgba(*OUT); c.set_line_width(36); c.stroke_preserve(); c.set_source_rgba(*hexc('#8D5524')); c.set_line_width(24); c.stroke()
    for (dx, dy, r) in ((-120, 90, 150), (120, 60, 150), (0, -10, 170), (-560, BRANCH_Y - 40, 70), (-420, BRANCH_Y - 55, 60)):
        yy = dy if dy < 200 else dy
        ellipse(c, x + dx, yy, r, r * 0.75); c.set_source_rgba(*OUT); c.set_line_width(10); c.stroke()
    for (dx, dy, r) in ((-120, 90, 150), (120, 60, 150), (0, -10, 170), (-560, BRANCH_Y - 40, 70), (-420, BRANCH_Y - 55, 60)):
        ellipse(c, x + dx, dy, r, r * 0.75); c.set_source_rgba(*hexc('#43A047')); c.fill()

def flowers(c, t):
    spots = [(150, 900, 72.5), (420, 930, 74.0), (700, 910, 75.5), (1010, 935, 77.0), (1290, 905, 79.0), (1560, 930, 80.5),
             (260, 960, 83.0), (880, 965, 84.5), (1440, 970, 86.0)]
    for k, (x, y, t0) in enumerate(spots):
        s = K_back((t - t0) / 0.6) if t > t0 else 0
        if s <= 0.01: continue
        col = ('#FF4081', '#FFD600', '#7C4DFF', '#40C4FF', '#FF7043')[k % 5]
        c.move_to(x, y); c.line_to(x, y - 40 * s); c.set_source_rgba(*hexc('#388E3C')); c.set_line_width(6); c.stroke()
        for i in range(6):
            a = i * math.pi / 3 + 0.3 * math.sin(t + k)
            ellipse(c, x + 20 * s * math.cos(a), y - 40 * s + 20 * s * math.sin(a), 14 * s, 14 * s); fill(c, hexc(col), OUT, 3)
        ellipse(c, x, y - 40 * s, 10 * s, 10 * s); fill(c, hexc('#FFF59D'), OUT, 3)
        if t - t0 < 1.0: sparkle(c, x + 30, y - 70, 16 * (1 - (t - t0)), '#FFFFFF')

# ---------------- dónde está Mari ----------------
def mari_state(t):
    """('oruga'|'capullo'|'mariposa', x, y, escala)"""
    if t < 25.0:
        g = 0.75 + 0.45 * ss(15.5, 23.5, t)
        a = -2.6 + 0.55 * min(5, int(ss(15.5, 23.0, t) * 6))
        if t < 15.5: return 'oruga', BUSH[0] - 60, BUSH[1] - 120, g
        return 'oruga', BUSH[0] + 110 * math.cos(a) - 20, BUSH[1] - 40 + 90 * math.sin(a) - 30, g
    if t < 30.0:   # sube por el tronco y la rama
        q = ss(25.5, 29.5, t)
        pts = [(BUSH[0] - 60, BUSH[1] - 130), (1300, 700), (1640, 560), (1620, BRANCH_Y - 10), (COCOON[0], BRANCH_Y - 10)]
        seg = q * (len(pts) - 1); i = min(int(seg), len(pts) - 2); f = seg - i
        return 'oruga', pts[i][0] + (pts[i + 1][0] - pts[i][0]) * f, pts[i][1] + (pts[i + 1][1] - pts[i][1]) * f, 1.2
    if t < 53.5: return 'capullo', COCOON[0], COCOON[1], 1.0
    if t < 64.5: return 'mariposa', COCOON[0], COCOON[1] + 120 - 60 * ss(55.0, 58.0, t), 1.0
    # vuelo: se posa en Pipa, Tito y Coco
    path = [(64.5, COCOON[0], COCOON[1] + 60), (67.0, 1480, 500), (69.5, 1480, 500), (72.0, 470, 480), (74.0, 470, 480),
            (76.5, 640, 560), (78.0, 640, 560), (82.0, 1100, 300), (86.0, 400, 330), (90.0, 960, 280), (100, 960, 280)]
    x = kf(t, [(a, b) for a, b, _ in path]); y = kf(t, [(a, cc) for a, _, cc in path])
    return 'mariposa', x + 30 * math.sin(t * 2.3), y + 20 * math.sin(t * 3.1), 0.95

def darkness(t):
    return 0.6 * (ss(37.0, 38.0, t) * (1 - ss(39.5, 40.5, t)) + ss(42.0, 43.0, t) * (1 - ss(45.0, 46.0, t)))

def frame(c, t):
    c.set_source_surface(SKY, 0, 0); c.paint()
    if 35.5 < t < 46.5:   # el sol cruza rápido (pasan los días)
        ph = ((t - 35.5) / 5.5) % 1
        sx, sy = 200 + 1500 * ph, 600 - 450 * math.sin(math.pi * ph)
        ellipse(c, sx, sy, 70, 70); fill(c, hexc('#FFD54F'), hexc('#F9A825'), 6)
    else: sun(c, t)
    for (x0, y0, s, sp) in ((150, 160, 0.9, 10), (700, 110, 0.7, 7)): cloud(c, (x0 + sp * t) % 2300 - 250, y0, s)
    c.set_source_surface(LAND, 0, 0); c.paint()
    tree(c, t)
    bush(c, t)
    flowers(c, t)
    kind, mx, my, ms = mari_state(t)
    wrap = ss(29.5, 33.5, t)
    if kind == 'capullo' or (kind == 'mariposa' and t < 56.0) or (kind == 'oruga' and t > 29.5):
        cocoon(c, t, wrap if t < 53.5 else 1 - ss(53.5, 55.5, t), ss(47.5, 52.0, t))
    party = t > 79.0
    bob = lambda ph: -14 * abs(math.sin(t * 4 + ph)) if party else 0
    watch = 35.5 < t < 53.5
    # Pipa
    px = 1480
    K.put(c, K.pipa, px, GROUND + bob(0.5), 0.6, t=t, look=(-1, -0.6) if watch else (-1, 0), lid=0.7 if darkness(t) > 0.3 else 0.0)
    # Tito
    tx = 300
    K.put(c, K.tito, tx, GROUND + bob(1.0), 0.66, t=t, look=(1, -0.2), lid=0.8 if darkness(t) > 0.3 else 0.0,
          reach=200 if 71.5 < t < 74.5 else None)
    # Tomi
    tmx = kf(t, [(0, 1200), (100, 1200)])
    K.put(c, K.tomi, tmx, GROUND + bob(1.5), 0.6, t=t, look=(-0.3, -0.6) if watch else (-1, 0))
    # Coco
    cx = kf(t, [(0, 380), (6.0, 380), (8.5, 680)])
    mood, look = 'smile', (1, -0.2)
    ar, al = math.radians(65 + 6 * math.sin(t * 2)), math.radians(115 - 6 * math.sin(t * 2))
    if 8.5 < t < 12.0: mood = 'o'
    if 26.0 < t < 34.0: look = (1, -0.8)
    if watch: look = (1, -0.9)
    if 46.5 < t < 56.0: mood = 'o'
    if 56.0 < t < 60.0: ar, al = math.radians(-60), math.radians(-120)
    if party: ar, al = math.radians(-58 + 25 * math.sin(t * 9)), math.radians(-122 - 25 * math.sin(t * 9))
    K.put(c, K.coco, cx, GROUND + bob(0), 0.62, t=t, mood=mood, look=look, arm_r=ar, arm_l=al, lid=0.6 if darkness(t) > 0.3 else 0.0,
          walk=t * 8 if 6.0 < t < 8.5 else 0)
    # Lola
    lx, ly = 780 + 160 * math.sin(t * 0.4), 360 + 18 * math.sin(t * 3)
    K.put(c, K.lola, lx, ly + bob(2.0), 0.5, t=t, flap=20, look=(0.6, 0.3))
    # Mari
    if kind == 'oruga':
        chew = 15.5 < t < 23.5
        oruga(c, mx, my, ms * (0.9 if t < 25 else 1.0), t, chew=chew, sleepy=ss(23.5, 25.0, t) * (1 if t > 23.5 else 0))
    elif kind == 'mariposa':
        o = ss(55.0, 60.0, t)
        fl = t * 10 if t > 64.5 else (t * 2 if t > 60 else 0)
        mariposa(c, mx, my, ms if t > 64.5 else 1.15, t, open_=o, flap=fl)
        if 55.0 < t < 61.5:   # destello del gran momento
            q = ss(55.0, 61.5, t)
            for k in range(14):
                a = k * math.pi / 7 + t * 0.5; r = 90 + 360 * q
                sparkle(c, mx + r * math.cos(a), my + r * math.sin(a), 26 * (1 - q) + 4, ('#FF4081', '#FFD600', '#7C4DFF', '#40C4FF', '#FFFFFF')[k % 5])
        if t > 64.5:
            for k in range(5):   # estela de brillitos
                ph = (t * 1.2 + k / 5) % 1
                sparkle(c, mx - 60 * ph * (1 if math.cos(t) > 0 else -1), my + 40 * ph, 10 * (1 - ph), ('#FFD600', '#FF80AB', '#B388FF')[k % 3])
    d = darkness(t)
    if d > 0:
        c.set_source_rgba(0.05, 0.05, 0.25, d); c.paint()
        for k in range(30):
            ellipse(c, (k * 197) % 1900, 30 + (k * 83) % 380, 3, 3); c.set_source_rgba(1, 1, 0.85, d * 1.5 * (0.5 + 0.5 * math.sin(t * 3 + k))); c.fill()
        ellipse(c, 1500, 160, 60, 60); c.set_source_rgba(1, 0.97, 0.7, d * 1.6); c.fill()
        for k in range(3):
            ph = (t * 0.6 + k / 3) % 1
            music_note(c, lx + 40 + 60 * ph, ly - 150 - 160 * ph, math.sin(math.pi * ph) * d * 1.6, ['#F48FB1', '#90CAF9', '#FFF59D'][k])
    if party:
        for k in range(3):
            ph = (t * 0.7 + k / 3) % 1
            music_note(c, lx + 40 + 60 * ph, ly - 150 - 160 * ph, math.sin(math.pi * ph), ['#E91E63', '#1E88E5', '#FFD600'][k])
    for (t0, x, y) in ((68.0, 1500, 420), (72.5, 470, 420), (76.8, 660, 480)):   # corazoncitos al posarse
        if t0 < t < t0 + 2.0:
            q = (t - t0) / 2.0; heart(c, x + 40, y - 80 - 100 * q, 0.9, math.sin(math.pi * q))
    # globitos
    bubble(c, cx, GROUND - 330, '¿Quién está ahí?', (t - 7.5) / 2.6, 46)
    bubble(c, BUSH[0] - 40, BUSH[1] - 230, '¡Hola, soy Mari!', (t - 10.2) / 3.0, 46)
    bubble(c, mx, my - 90, '¡Ñam, ñam!', (t - 16.5) / 3.0, 52)
    bubble(c, mx + 20, my - 90, 'Tengo sueño…', (t - 23.4) / 2.2, 46)
    bubble(c, tmx, GROUND - 270, 'Hay que esperar…', (t - 36.2) / 3.2, 44)
    bubble(c, cx, GROUND - 330, '¡Se mueve!', (t - 46.8) / 2.4, 52)
    bubble(c, cx, GROUND - 330, '¡Una mariposa!', (t - 60.2) / 3.2, 48)
    bubble(c, mx, my - 150, '¡Gracias por esperarme!', (t - 86.2) / 3.6, 44)

def overlay(c, t):
    if t < 5.6:
        a = 1 - ss(4.8, 5.5, t)
        c.push_group(); word(c, 'La oruguita Mari', W / 2, 230, 130 * K_back((t - 0.6) / 0.6) + 0.01,
                             colors=['#8BC34A', '#FF4081', '#FFD600', '#7C4DFF'], tilt=0.05, outline=9)
        c.pop_group_to_source(); c.paint_with_alpha(a)
    for (t0, txt) in ((48.0, '¡Crac!'), (49.6, '¡Crac!'), (51.2, '¡Crac!')):
        if t0 <= t < t0 + 1.2:
            q = t - t0
            word(c, txt, COCOON[0] - 260, COCOON[1] + 60 - 40 * q, 90 * K_back(q / 0.3) * (1 - ss(1.0, 1.2, q)) + 0.01, colors=['#FF7043'], tilt=-0.1, outline=8)
    if t > 92.0:
        s = K_back((t - 92.0) / 0.7)
        word(c, '¡Cada uno crece', W / 2, 160, 105 * s + 0.01, colors=['#8BC34A', '#FF4081', '#FFD600'], tilt=0.04, outline=10)
        word(c, 'a su tiempo!', W / 2, 280, 115 * s + 0.01, colors=['#7C4DFF', '#40C4FF', '#FF4081'], tilt=0.04, outline=10)
    a = max(1 - ss(0, 0.8, t), ss(DUR - 2.0, DUR, t))
    if a > 0: c.set_source_rgba(1, 1, 1, a); c.paint()

CAM = [(0, 1.0, 960, 540), (7.0, 1.0, 960, 540), (9.5, 1.55, 860, 640), (24.5, 1.55, 860, 640), (26.5, 1.0, 960, 540),
       (28.5, 1.0, 960, 540), (30.0, 1.6, 1220, 470), (34.5, 1.6, 1220, 470), (36.0, 1.0, 960, 540),
       (46.0, 1.0, 960, 540), (47.5, 1.6, 1120, 520), (63.0, 1.6, 1120, 520), (65.0, 1.0, 960, 540)]
def camera(t):
    z = kf(t, [(a, b) for a, b, _, _ in CAM]); x = kf(t, [(a, d) for a, _, d, _ in CAM]); y = kf(t, [(a, e) for a, _, _, e in CAM])
    return z, max(W / (2 * z), min(W - W / (2 * z), x)), max(H / (2 * z), min(H - H / (2 * z), y))

if __name__ == '__main__':
    args = sys.argv[1:]
    if args and args[0] == 'srt':
        print(srt(NARRACION, float(args[1]) if len(args) > 1 else 0.0)); sys.exit()
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(surf)
    def full(c, t):
        z, cx, cy = camera(t)
        c.save(); c.translate(W / 2, H / 2); c.scale(z, z); c.translate(-cx, -cy); frame(c, t); c.restore(); overlay(c, t)
    if args and args[0] == 'stills':
        for t in map(float, args[1:]):
            c.save(); full(c, t); c.restore(); surf.write_to_png(f'ep28_{t}.png')
    else:
        t0, t1 = (float(args[1]), float(args[2])) if args and args[0] == 'range' else (0, DUR)
        out = sys.stdout.buffer
        for i in range(int(round(t0 * FPS)), int(round(t1 * FPS))):
            c.save(); full(c, i / FPS); c.restore(); surf.flush(); out.write(surf.get_data())
