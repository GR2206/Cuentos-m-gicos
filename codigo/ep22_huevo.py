"""Episodio 22 — El huevo misterioso (100 s).
Tomi encuentra un huevo celeste. Lola lo abriga, Tito lo tapa de la lluvia con sus orejas-paraguas...
¡crac, crac! Nace un pichón que busca a su mamá. Pipa lo sube con su cuello largo hasta el nido
del árbol más alto y la mamá pájaro lo abraza. Invitados: el pichón Pío y su mamá (se dibujan acá).

Uso:  python3 ep22_huevo.py              -> cuadros crudos por stdout
      python3 ep22_huevo.py range 0 50   -> solo un tramo
      python3 ep22_huevo.py stills 20 70 -> PNG sueltos
      python3 ep22_huevo.py srt 5.5      -> subtítulos .srt de la narración"""
import cairo, math, random, sys
import cuerpos as K
from amigos import hexc, ellipse, fill, OUT
from logos import word, sparkle
from ep02_puente_del_rio import kf, ss, K_back, music_note
from ep03_donde_esta_tomi import bubble
from ep09_semilla_magica import SKY, LAND, cloud, sun, srt
from ep14_bananas_papa import heart
from ep20_tesoro import tall_tree

W, H, FPS = 1920, 1080, 30
DUR = 100.0
GROUND = 880
EGG = (730, 870)
TREE_X = 1560
NEST = (TREE_X - 125, 228)

NARRACION = [
    (6.0, 13.0, 'Un día, Tomi encontró algo entre las flores... ¡un huevo celeste!'),
    (14.0, 21.0, '¿De quién será? Mientras tanto, hay que cuidarlo.'),
    (22.0, 28.0, 'Lola se sentó arriba, despacito, para darle calorcito.'),
    (29.0, 36.0, 'Empezó a llover... ¡y Tito abrió sus orejas como un paraguas!'),
    (38.0, 45.0, 'Entonces el huevo se movió... ¡crac, crac, crac!'),
    (46.0, 52.0, '¡Nació un pichoncito! Se llamaba Pío.'),
    (53.0, 59.0, 'Pío buscaba a su mamá... ¡y la escucharon allá arriba, en el árbol más alto!'),
    (60.0, 69.0, 'Pipa bajó la cabeza, Pío se subió, y ella estiró el cuello bien, bien alto.'),
    (70.0, 79.0, '¡Pío llegó a su nido! Y su mamá le dio un abrazo enorme.'),
    (81.0, 92.0, 'La mamá pájaro cantó con Lola para darles las gracias.'),
    (94.0, 99.0, '¡Ayudar es lo más lindo!'),
]

# ---------------- invitados ----------------
def bird(c, x, y, s, t, flap=0.0, mood='smile', flip=False, chick=False):
    """pajarito celeste (mamá) o pichón (chick=True: más redondito, con mechón)."""
    c.save(); c.translate(x, y); c.scale(-s if flip else s, s)
    body = '#4FC3F7' if not chick else '#81D4FA'
    if not chick:
        ellipse(c, -55, 10, 30, 14); fill(c, hexc('#0288D1'), OUT, 4)          # cola
    ellipse(c, 0, 0, 52 if not chick else 46, 46); fill(c, hexc(body), OUT, 5)
    ellipse(c, 6, 14, 30, 24); fill(c, hexc('#FFF9C4'), None, 0)                  # pancita
    w = math.sin(flap) * 0.9
    c.save(); c.translate(-12, 2); c.rotate(-0.4 - w)
    ellipse(c, -18, 0, 28, 16); fill(c, hexc('#0288D1' if not chick else '#4FC3F7'), OUT, 4); c.restore()
    for ex in (8, 30):
        ellipse(c, ex, -14, 9, 11); c.set_source_rgba(1, 1, 1, 1); c.fill()
        ellipse(c, ex + 2, -12, 6, 8); c.set_source_rgba(*OUT); c.fill()
        ellipse(c, ex + 3, -15, 2.5, 2.5); c.set_source_rgba(1, 1, 1, 1); c.fill()
    for ex in (2, 38): ellipse(c, ex, 4, 7, 4); c.set_source_rgba(*hexc('#F48FB1', 0.9)); c.fill()
    op = 0.5 + 0.5 * math.sin(t * 10) if mood == 'sing' else 0
    c.move_to(36, -4); c.line_to(60, 2 - 4 * op); c.line_to(36, 8); c.close_path(); fill(c, hexc('#FFA000'), OUT, 3)
    if op > 0: c.move_to(36, 6); c.line_to(56, 10 + 6 * op); c.line_to(36, 10); c.close_path(); fill(c, hexc('#FF7043'), OUT, 2)
    if chick:
        for d in (-1, 0, 1):
            c.move_to(4 + 6 * d, -44); c.curve_to(8 + 10 * d, -64, 14 + 16 * d, -62, 16 + 18 * d, -56)
            c.set_source_rgba(*OUT); c.set_line_width(4); c.stroke()
    for d in (-1, 1):
        c.move_to(d * 12, 42); c.line_to(d * 12, 56); c.set_source_rgba(*hexc('#FFA000')); c.set_line_width(5); c.stroke()
    c.restore()

def egg_shape(c, x, y, s, rot, cracks, top_off=0.0):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    c.move_to(0, -110); c.curve_to(70, -110, 85, 0, 75, 30); c.curve_to(62, 75, -62, 75, -75, 30); c.curve_to(-85, 0, -70, -110, 0, -110); c.close_path()
    if top_off <= 0:
        fill(c, hexc('#E1F5FE'), OUT, 6)
        for (dx, dy, r) in ((-30, -50, 12), (25, -20, 9), (-10, 20, 14), (40, 30, 8), (10, -80, 7)):
            ellipse(c, dx, dy, r, r); c.set_source_rgba(*hexc('#4FC3F7', 0.8)); c.fill()
        zz = [(-70, -15), (-45, -35), (-25, -10), (0, -38), (22, -12), (45, -36), (72, -15)]
        n = int(cracks * (len(zz) - 1))
        if n >= 1:
            c.move_to(*zz[0])
            for p in zz[1:n + 1]: c.line_to(*p)
            c.set_source_rgba(*OUT); c.set_line_width(5); c.stroke()
    else:   # medio cascarón abajo
        c.new_path()
        c.move_to(-78, -10); zz = [(-78, -10), (-50, -35), (-25, -10), (0, -38), (22, -12), (45, -36), (78, -10)]
        for p in zz[1:]: c.line_to(*p)
        c.curve_to(85, 30, 62, 75, 0, 75); c.curve_to(-62, 75, -85, 30, -78, -10); c.close_path()
        fill(c, hexc('#E1F5FE'), OUT, 6)
        ellipse(c, -10, 20, 14, 14); c.set_source_rgba(*hexc('#4FC3F7', 0.8)); c.fill()
    c.restore()

def shell_top(c, t):
    if t < 46.0 or t > 48.0: return
    q = (t - 46.0) / 2.0
    x, y = EGG[0] + 220 * q, EGG[1] - 100 - 320 * math.sin(math.pi * q * 0.9)
    c.save(); c.translate(x, y); c.rotate(5 * q)
    c.move_to(-78, 0); zz = [(-78, 0), (-50, -25), (-25, 0), (0, -28), (22, -2), (45, -26), (78, 0)]
    c.move_to(-78, 0); c.curve_to(-80, -60, -40, -100, 0, -100); c.curve_to(40, -100, 80, -60, 78, 0)
    for p in reversed(zz[:-1]): c.line_to(*p)
    c.close_path(); fill(c, hexc('#E1F5FE'), OUT, 6); c.restore()

def nest(c, front):
    x, y = NEST
    if not front:
        ellipse(c, x, y, 80, 26); fill(c, hexc('#5D4037'), OUT, 5); return
    c.move_to(x - 85, y); c.curve_to(x - 80, y + 50, x + 80, y + 50, x + 85, y); c.close_path(); fill(c, hexc('#8D6E63'), OUT, 5)
    for k in range(7):
        c.move_to(x - 75 + 25 * k, y + 5); c.line_to(x - 60 + 25 * k, y + 30); c.set_source_rgba(*hexc('#5D4037')); c.set_line_width(4); c.stroke()

# ---------------- movimientos ----------------
PIPA_X = [(0, 1300), (56.0, 1300), (58.0, 960), (62.0, 960), (64.0, 1300)]
def pipa_neck(t): return kf(t, [(58.0, 300), (59.5, 180), (61.5, 180), (63.0, 300), (64.5, 300), (67.5, 760), (70.0, 760), (73.0, 300)])
def pipa_lean(t): return kf(t, [(58.0, 0), (59.5, -300), (61.5, -300), (63.0, 0), (64.5, 0), (67.5, 220), (70.0, 220), (73.0, 0)])
def pipa_head(t): return kf(t, PIPA_X) + 0.55 * pipa_lean(t), GROUND - 0.55 * (260 + pipa_neck(t))

def chick_pos(t):
    if t < 60.4: return EGG[0], EGG[1] - 75 - 10 * abs(math.sin(t * 5)) * (t > 50)
    hx, hy = pipa_head(t)
    if t < 61.2:
        q = ss(60.4, 61.2, t); return EGG[0] + (hx - EGG[0]) * q, EGG[1] - 60 + (hy - 85 - EGG[1] + 60) * q - 90 * math.sin(math.pi * q)
    if t < 69.0: return hx, hy - 85
    if t < 69.8:
        q = ss(69.0, 69.8, t); hx, hy = pipa_head(69.0)
        return hx + (NEST[0] - 25 - hx) * q, hy - 85 + (NEST[1] - 35 - hy + 85) * q - 80 * math.sin(math.pi * q)
    return NEST[0] - 25, NEST[1] - 35 - (8 * abs(math.sin(t * 6)) if t > 80 else 0)

def mama_pos(t):
    if t < 50.5: return None
    if t < 69.8:
        a = t * 1.3; return TREE_X - 60 + 220 * math.cos(a), 170 + 70 * math.sin(a * 2), math.cos(a) > 0
    if t < 71.0:
        q = ss(69.8, 71.0, t); a = 69.8 * 1.3; x0, y0 = TREE_X - 60 + 220 * math.cos(a), 170 + 70 * math.sin(a * 2)
        return x0 + (NEST[0] + 35 - x0) * q, y0 + (NEST[1] - 40 - y0) * q, True
    if t < 81.0: return NEST[0] + 35, NEST[1] - 40, True
    a = (t - 81.0) * 1.1
    return 960 + 500 * math.cos(a), 330 + 90 * math.sin(a * 2), math.sin(a) < 0

def rain(t): return ss(28.5, 29.5, t) * (1 - ss(35.5, 36.5, t))

def frame(c, t):
    c.set_source_surface(SKY, 0, 0); c.paint()
    sun(c, t)
    for (x0, y0, s, sp) in ((150, 160, 0.9, 10), (700, 110, 0.7, 7)): cloud(c, (x0 + sp * t) % 2300 - 250, y0, s)
    r = rain(t)
    if r > 0:
        c.set_source_rgba(0.35, 0.4, 0.5, 0.35 * r); c.paint()
        for k in range(4):
            c.save(); c.translate(250 + 350 * k, 120); c.scale(1.2, 1.0)
            for (cx, cy, rr) in ((0, 0, 60), (70, -30, 75), (150, 0, 60), (75, 20, 60)): ellipse(c, cx, cy, rr, rr)
            c.set_source_rgba(0.55, 0.6, 0.7, r); c.fill(); c.restore()
    c.set_source_surface(LAND, 0, 0); c.paint()
    tall_tree(c, TREE_X, t)
    nest(c, False)
    mp = mama_pos(t)
    # pichón en el nido (atrás del borde)
    chx, chy = chick_pos(t)
    hatched = t > 46.0
    if t > 69.8: bird(c, chx, chy, 1.0, t, mood='sing' if t > 81 else 'smile', chick=True)
    if mp and 70.0 < t < 81.0: bird(c, mp[0], mp[1], 1.1, t, flap=t * 2, flip=True)
    nest(c, True)
    party = t > 81.0
    bob = lambda ph: -18 * abs(math.sin(t * 4.5 + ph)) if party else 0
    # Pipa
    px = kf(t, PIPA_X)
    lk = (-1, 0.5) if 57 < t < 63 else ((1, -0.8) if 50 < t < 74 else (-0.6, 0))
    K.put(c, K.pipa, px, GROUND + bob(0.5), 0.55, t=t, neck=pipa_neck(t), lean=pipa_lean(t), look=lk,
          walk=t * 7 if 56 < t < 58 or 62 < t < 64 else 0)
    # Tito (paraguas)
    tx = 500
    K.put(c, K.tito, tx, GROUND + bob(1.0), 0.6, t=t, look=(1, 0.3), umbrella=r)
    # huevo / cascarón
    if t < 46.0:
        wob = 0.12 * math.sin(t * 14) * (ss(38.0, 39.0, t) if t > 38 else 0)
        egg_shape(c, EGG[0], EGG[1], 1.0, wob, ss(40.0, 45.5, t))
    else:
        if t < 60.4: bird(c, chx, chy, 1.0, t, mood='sing' if 48 < t < 50 or 52 < t < 54 else 'smile', chick=True)
        egg_shape(c, EGG[0], EGG[1], 1.0, 0, 1, top_off=1)
    shell_top(c, t)
    if 61.2 < t < 69.8: bird(c, chx, chy, 1.0, t, chick=True)
    if 45.6 < t < 47.0:
        for k in range(8):
            a = k * math.pi / 4; rr = 60 + 200 * (t - 45.6)
            sparkle(c, EGG[0] + rr * math.cos(a), EGG[1] - 60 + rr * math.sin(a), 18, '#FFD600')
    # Lola (empolla)
    if 21.5 < t < 37.0:
        q = ss(21.5, 23.0, t) * (1 - ss(36.0, 37.0, t))
        lx = 1150 + (EGG[0] - 1150) * q; ly = 450 + (EGG[1] - 120 - 450) * q
        K.put(c, K.lola, lx, ly + 8 * math.sin(t * 2) * (q == 1), 0.5, t=t, flap=20 if q < 1 else 0, look=(0.5, 0.5), lid=0.6 if 24 < t < 35 else 0)
    else:
        lx, ly = (1150 + 60 * math.sin(t * 0.6), 450 + 18 * math.sin(t * 3)) if t < 81 else (960 + 500 * math.cos((t - 81.0) * 1.1 + 3.14), 330 + 90 * math.sin(((t - 81.0) * 1.1 + 3.14) * 2))
        K.put(c, K.lola, lx, ly + bob(2.0), 0.5, t=t, flap=20, look=(0.5, 0.3))
    if mp and not (70.0 < t < 81.0): bird(c, mp[0], mp[1], 1.1, t, flap=t * 9, flip=mp[2], mood='sing' if 52 < t < 57 or t > 81 else 'smile')
    # Tomi
    tmx = kf(t, [(0, 1150), (5.5, 1150), (7.5, 960)])
    K.put(c, K.tomi, tmx, GROUND + bob(1.5), 0.55, t=t, look=(-1, 0.3), walk=t * 3 if 5.5 < t < 7.5 else 0)
    # Coco
    cx = kf(t, [(0, 200), (9.0, 200), (10.5, 290)])
    mood, look = 'smile', (1, 0.2)
    ar, al = math.radians(65 + 6 * math.sin(t * 2)), math.radians(115 - 6 * math.sin(t * 2))
    if 9.0 < t < 13.0: mood = 'o'
    if 38.5 < t < 46.0: mood = 'o'; ar = al = math.radians(150) if False else ar
    if 46.0 < t < 50.0: ar, al = math.radians(-60), math.radians(-120)
    if 66.0 < t < 74.0: look = (1, -1)
    if 70.0 < t < 74.0: ar, al = math.radians(-60), math.radians(-120)
    if party: ar, al = math.radians(-58 + 25 * math.sin(t * 9)), math.radians(-122 - 25 * math.sin(t * 9))
    K.put(c, K.coco, cx, GROUND + bob(0), 0.55, t=t, mood=mood, look=look, arm_r=ar, arm_l=al, walk=t * 8 if 9 < t < 10.5 else 0)
    if r > 0:   # lluvia
        for k in range(90):
            x = (k * 211 + t * 300) % 2000 - 40; y = (k * 97 + t * 1300) % 1100
            if 330 < x < 700 and y > 520: continue   # el paraguas de Tito
            c.move_to(x, y); c.line_to(x - 8, y + 34); c.set_source_rgba(0.6, 0.8, 1, 0.8 * r); c.set_line_width(4); c.stroke()
    if 71.0 < t < 80.0:
        for k in range(5):
            ph = ((t - 71.0) * 0.5 + k / 5) % 1
            heart(c, NEST[0] + 120 * math.sin(k * 1.9), NEST[1] - 60 - 200 * ph, 0.9, math.sin(math.pi * ph))
    if party:
        for k in range(3):
            ph = (t * 0.7 + k / 3) % 1
            music_note(c, lx + 40 + 60 * ph, ly - 150 - 160 * ph, math.sin(math.pi * ph), ['#E91E63', '#1E88E5', '#FFD600'][k])
            if mp: music_note(c, mp[0] + 40 + 60 * ph, mp[1] - 80 - 140 * ph, math.sin(math.pi * ph), ['#4FC3F7', '#FFD600', '#E91E63'][k])
    # globitos
    bubble(c, tmx, GROUND - 250, '¡Un huevo!', (t - 7.6) / 3.0, 54)
    bubble(c, cx, GROUND - 300, '¿De quién será?', (t - 14.0) / 3.4, 46)
    bubble(c, tx, GROUND - 420, '¡Yo lo tapo!', (t - 29.6) / 3.0, 50)
    bubble(c, cx, GROUND - 300, '¡Se mueve!', (t - 38.6) / 2.8, 50)
    bubble(c, EGG[0], EGG[1] - 170, '¡Pío, pío!', (t - 48.0) / 2.4, 54)
    if mp: bubble(c, mp[0], mp[1] - 90, '¡Pío! ¿Dónde estás?', (t - 52.0) / 4.0, 42)
    hx, hy = pipa_head(t)
    bubble(c, hx, hy - 110, '¡Subite!', (t - 59.5) / 2.2, 52)
    bubble(c, NEST[0] + 40, NEST[1] - 150, '¡Mamá!', (t - 70.0) / 2.4, 54)

def overlay(c, t):
    if t < 5.6:
        a = 1 - ss(4.8, 5.5, t)
        c.push_group(); word(c, 'El huevo misterioso', W / 2, 230, 125 * K_back((t - 0.6) / 0.6) + 0.01,
                             colors=['#29B6F6', '#FFD600', '#E91E63'], tilt=0.05, outline=9)
        c.pop_group_to_source(); c.paint_with_alpha(a)
    for (t0, txt) in ((40.2, '¡Crac!'), (42.2, '¡Crac!'), (44.2, '¡Crac!')):
        if t0 <= t < t0 + 1.2:
            q = t - t0
            word(c, txt, EGG[0] + 230, EGG[1] - 260 - 40 * q, 90 * K_back(q / 0.3) * (1 - ss(1.0, 1.2, q)) + 0.01, colors=['#FF7043'], tilt=-0.1, outline=8)
    if t > 94.0:
        s = K_back((t - 94.0) / 0.7)
        word(c, '¡Ayudar es', W / 2 - 300, 160, 110 * s + 0.01, tilt=0.05, outline=10)
        word(c, 'lo más lindo!', W / 2 - 300, 285, 110 * s + 0.01, start=3, tilt=0.05, outline=10)
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
            c.save(); full(c, t); c.restore(); surf.write_to_png(f'ep22_{t}.png')
    else:
        t0, t1 = (float(args[1]), float(args[2])) if args and args[0] == 'range' else (0, DUR)
        out = sys.stdout.buffer
        for i in range(int(round(t0 * FPS)), int(round(t1 * FPS))):
            c.save(); full(c, i / FPS); c.restore(); surf.flush(); out.write(surf.get_data())
