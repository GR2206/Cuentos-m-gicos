"""Episodio 19 — La luciérnaga perdida (100 s). Aventurita de noche en el bosque.
Luz, una luciérnaga chiquita, se perdió y apenas brilla. Pipa ve luces lejos, todos la acompañan por el bosque
oscuro y cuando cantan, Luz brilla más fuerte. En el prado la espera su familia; las luciérnagas dibujan un
corazón y una estrella en el cielo para dar las gracias... y todos se van a dormir.
(Luz es un personaje invitado: `luz()` se puede importar de este archivo.)

Uso:  python3 ep19_luciernaga.py              -> cuadros crudos por stdout
      python3 ep19_luciernaga.py range 0 50   -> solo un tramo
      python3 ep19_luciernaga.py stills 20 70 -> PNG sueltos
      python3 ep19_luciernaga.py srt 5.5      -> subtítulos .srt de la narración"""
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
MEADOW = 5200
BK = [(0, 1000), (22.0, 1000), (55.0, MEADOW), (100, MEADOW)]
FORM = {'coco': 0, 'tomi': -230, 'tito': -480, 'pipa': -760}
MOM = (MEADOW + 480, 470)        # mamá luciérnaga (mundo)

NARRACION = [
    (6.0, 13.5, 'Una noche, los amigos encontraron a una luciérnaga chiquita que lloraba. Se llamaba Luz.'),
    (14.0, 21.5, '¡Se había perdido! Pipa miró desde arriba y vio lucecitas, lejos, del otro lado del bosque.'),
    (23.0, 29.5, 'Entonces todos juntos la acompañaron por el caminito.'),
    (30.5, 35.0, 'El bosque estaba muy oscuro...'),
    (35.5, 44.0, 'Pero Lola empezó a cantar, ¡y cuando cantaban, Luz brillaba cada vez más!'),
    (45.0, 54.0, 'Cantando y cantando, cruzaron todo el bosque.'),
    (56.0, 66.0, 'En el prado estaba la familia de Luz. ¡Mamá! ¡Qué abrazo tan lindo!'),
    (68.0, 83.0, 'Para dar las gracias, las luciérnagas dibujaron en el cielo un corazón... y una estrella.'),
    (85.0, 93.0, 'Y con sus lucecitas iluminaron el camino de vuelta. Los amigos tenían mucho sueño.'),
    (94.0, 99.0, 'Buenas noches, amigos. Buenas noches, Luz.'),
]

def B(t): return kf(t, BK)
def x_of(name, t): return B(t) + FORM[name]
def walking(t): return 22.0 < t < 55.0

# ---------------- Luz, la luciérnaga ----------------
def glow(c, x, y, r, a, col=(1, 0.95, 0.4)):
    if r <= 1 or a <= 0: return
    g = cairo.RadialGradient(x, y, 0, x, y, r)
    g.add_color_stop_rgba(0, *col, 0.75 * a); g.add_color_stop_rgba(0.35, *col, 0.3 * a); g.add_color_stop_rgba(1, *col, 0)
    c.set_source(g); c.arc(x, y, r, 0, 2 * math.pi); c.fill()

def luz(c, x, y, s, t, shine=1.0, mood='smile', flip=False):
    """Luciérnaga con cara: cabecita marrón, ojos grandes y colita que brilla (shine 0..1+)."""
    c.save(); c.translate(x, y); c.scale(-s if flip else s, s)
    glow(c, -40, 20, 170 * (0.4 + 0.6 * shine), min(1.0, 0.3 + 0.7 * shine))
    fl = math.sin(t * 30) * 0.5
    for d in (-1, 1):   # alitas
        c.save(); c.translate(-5, -20); c.rotate(d * (0.5 + fl * 0.4) - 0.3)
        ellipse(c, 0, -40, 22, 42); c.set_source_rgba(1, 1, 1, 0.75); c.fill_preserve(); c.set_source_rgba(*OUT); c.set_line_width(3); c.stroke()
        c.restore()
    ellipse(c, -42, 18, 40, 32); fill(c, mix_glow(shine), OUT, 5)                   # colita
    ellipse(c, 0, 0, 34, 30); fill(c, hexc('#6D4C41'), OUT, 5)                       # cuerpito
    for d in (-1, 1):   # antenitas
        c.move_to(20 + 8 * d, -45); c.curve_to(30 + 8 * d, -80, 45 + 20 * d, -90, 55 + 20 * d, -85)
        c.set_source_rgba(*OUT); c.set_line_width(4); c.stroke()
        ellipse(c, 55 + 20 * d, -85, 7, 7); fill(c, hexc('#FFEB3B'), OUT, 3)
    ellipse(c, 28, -30, 42, 38); fill(c, hexc('#8D6E63'), OUT, 5)                    # cabeza
    for ex in (14, 44):
        ellipse(c, ex, -36, 11, 14); c.set_source_rgba(1, 1, 1, 1); c.fill()
        ellipse(c, ex + 3, -34, 7, 9); c.set_source_rgba(*OUT); c.fill()
        ellipse(c, ex + 5, -38, 3, 3); c.set_source_rgba(1, 1, 1, 1); c.fill()
    for ex in (8, 52): ellipse(c, ex, -16, 8, 5); c.set_source_rgba(*hexc('#F48FB1', 0.9)); c.fill()
    if mood == 'sad':
        c.arc(30, -6, 10, math.pi * 1.15, math.pi * 1.85); c.set_source_rgba(*OUT); c.set_line_width(4); c.stroke()
        ellipse(c, 8, -18 + 10 * ((t * 0.8) % 1), 4, 6); c.set_source_rgba(0.5, 0.8, 1, 0.9); c.fill()      # lagrimita
    else:
        c.arc(30, -18, 11, 0.15 * math.pi, 0.85 * math.pi); c.set_source_rgba(*OUT); c.set_line_width(4); c.stroke()
    c.restore()

def mix_glow(shine):
    q = max(0.0, min(1.0, shine))
    return (0.75 + 0.25 * q, 0.85 + 0.15 * q, 0.35 + 0.15 * q, 1)

def tiny(c, x, y, t, k, a=1.0):
    """luciérnaga chiquita de la familia (un puntito que brilla)."""
    b = 0.6 + 0.4 * math.sin(t * 5 + k)
    glow(c, x, y, 70, a * b)
    ellipse(c, x, y, 10, 10); c.set_source_rgba(1, 1, 0.7, a); c.fill()

# ---------------- dónde está cada cosa ----------------
def luz_pos(t):
    """posición de Luz en el mundo."""
    cx = x_of('coco', t)
    if t < 6.0: return cx + 420 + 200 * (1 - ss(1.0, 6.0, t)), 620 - 150 * (1 - ss(1.0, 6.0, t))
    if t < 56.0: return cx + 170 + 25 * math.sin(t * 1.3), 560 + 25 * math.sin(t * 2.1)
    if t < 58.5:
        q = ss(56.0, 58.5, t); x0, y0 = cx + 170, 560
        return x0 + (MOM[0] - 120 - x0) * q, y0 + (MOM[1] + 20 - y0) * q - 80 * math.sin(math.pi * q)
    if t < 68.0: return MOM[0] - 120 + 10 * math.sin(t * 2), MOM[1] + 20 + 8 * math.sin(t * 3)
    return MOM[0] - 120 + 40 * math.sin(t * 0.8), MOM[1] + 20 + 30 * math.sin(t * 1.3) - 60 * ss(68, 70, t)

def luz_shine(t):
    return kf(t, [(0, 0.15), (30.0, 0.25), (34.5, 0.25), (37.5, 1.3), (55.0, 1.3), (58.0, 1.0)])

def light_radius(t):
    return kf(t, [(0, 260), (28.0, 240), (32.0, 150), (34.5, 150), (38.0, 650), (55.0, 650), (60.0, 500)])

def darkness(t):
    return kf(t, [(0, 0.45), (24.0, 0.45), (30.0, 0.82), (55.0, 0.82), (60.0, 0.55), (100, 0.55)])

FAM = [(random.Random(i).uniform(-1, 1), random.Random(i + 7).uniform(-1, 1), random.Random(i + 31).uniform(0, 6.28)) for i in range(40)]
def family_points(t, cam):
    """luciérnagas de la familia en pantalla; forman corazón (68–76) y estrella (76–84), luego alumbran el camino."""
    pts = []
    n = len(FAM)
    for k, (u, v, ph) in enumerate(FAM):
        fx = MOM[0] - cam + 960 + 380 * u + 50 * math.sin(t * 1.2 + ph)
        fy = MOM[1] + 260 * v + 40 * math.sin(t * 1.6 + ph) - 100
        # corazón
        a = 2 * math.pi * k / n
        hx = 16 * math.sin(a) ** 3; hy = -(13 * math.cos(a) - 5 * math.cos(2 * a) - 2 * math.cos(3 * a) - math.cos(4 * a))
        hx, hy = 960 + 300 + 17 * hx, 330 + 17 * hy
        # estrella
        j = k % 10; u2 = (k // 10) / 4
        r0 = 230 if j % 2 == 0 else 95; r1 = 95 if j % 2 == 0 else 230
        a0 = -math.pi / 2 + j * math.pi / 5; a1 = -math.pi / 2 + (j + 1) * math.pi / 5
        sx = 960 + 300 + (r0 * math.cos(a0)) * (1 - u2) + (r1 * math.cos(a1)) * u2
        sy = 330 + (r0 * math.sin(a0)) * (1 - u2) + (r1 * math.sin(a1)) * u2
        # camino de vuelta
        px, py = 200 + 1600 * k / n + 30 * math.sin(t * 2 + ph), 760 + 40 * math.sin(k * 1.3 + t)
        q1 = ss(68.0, 70.5, t) * (1 - ss(76.0, 77.5, t)); q2 = ss(76.0, 77.5, t) * (1 - ss(84.0, 86.0, t)); q3 = ss(84.0, 86.5, t)
        x = fx + (hx - fx) * q1 + (sx - fx) * q2 + (px - fx) * q3
        y = fy + (hy - fy) * q1 + (sy - fy) * q2 + (py - fy) * q3
        come = ss(52.0 + 0.1 * k, 56.0 + 0.1 * k, t)
        pts.append((x, y + (1 - come) * 0, come))
    return pts

# ---------------- dibujo ----------------
def sky(c, t):
    g = cairo.LinearGradient(0, 0, 0, H)
    g.add_color_stop_rgb(0, *hexc('#0D0B3B')[:3]); g.add_color_stop_rgb(0.6, *hexc('#2B2370')[:3]); g.add_color_stop_rgb(1, *hexc('#4A3B8F')[:3])
    c.set_source(g); c.paint()
    for k in range(60):
        sx, sy = (k * 197) % 1920, 20 + (k * 83) % 520
        ellipse(c, sx, sy, 2.5 + (k % 3), 2.5 + (k % 3)); c.set_source_rgba(1, 1, 0.85, 0.5 + 0.5 * math.sin(t * 2 + k)); c.fill()
    my = kf(t, [(0, 260), (100, 170)])
    glow(c, 1650, my, 220, 0.5, (1, 1, 0.8))
    ellipse(c, 1650, my, 80, 80); fill(c, hexc('#FFF9C4'), hexc('#F9A825'), 6)
    for (dx, dy, r) in ((-25, -15, 14), (20, 20, 10), (-10, 30, 7)):
        ellipse(c, 1650 + dx, my + dy, r, r); c.set_source_rgba(*hexc('#F0E68C', 0.8)); c.fill()

def frame(c, t):
    cam = B(t)
    sky(c, t)
    # bosque (se dibuja con colores de día y después se oscurece)
    c.push_group()
    far_hills(c, cam); back_trees(c, cam); ground(c, cam); path_trees(c, cam)
    if cam > MEADOW - 1500:   # flores del prado
        for k in range(14):
            x = MEADOW + 120 + 120 * k - cam + 960; y = 860 + 50 * ((k * 7) % 3)
            for i in range(5):
                a = i * 2 * math.pi / 5; ellipse(c, x + 14 * math.cos(a), y + 14 * math.sin(a), 10, 10); c.set_source_rgba(*hexc(('#FF80AB', '#B39DDB', '#FFF59D')[k % 3])); c.fill()
    c.pop_group_to_source(); c.paint()
    lx, ly = luz_pos(t); lsx = lx - cam + 960
    # personajes
    scared = 30.0 < t < 35.5
    sleepy = t > 86.0
    song = 35.5 < t < 55.0
    wk = lambda sp: t * sp if walking(t) else 0
    bob = lambda ph: -14 * abs(math.sin(t * 4 + ph)) if song else 0
    px = x_of('pipa', t) - cam + 960
    neck = kf(t, [(14.0, 300), (15.5, 760), (20.5, 760), (22.0, 300)])
    K.put(c, K.pipa, px, GROUND + bob(0.5), 0.55, t=t, neck=neck, look=(1, -0.8) if 14 < t < 21 else ((0.5, -0.5) if scared else (1, 0)), walk=wk(7))
    tx = x_of('tito', t) - cam + 960
    K.put(c, K.tito, tx, GROUND + bob(1.0), 0.6, t=t, look=(0.6, -0.4) if scared else (1, 0), walk=wk(6),
          lid=0.6 if sleepy and t < 96 else (1.0 if t > 96 else 0.0), yawn=math.sin(math.pi * ss(87.0, 90.0, t)))
    tmx = x_of('tomi', t) - cam + 960
    K.put(c, K.tomi, tmx, GROUND + bob(1.5), 0.55, t=t, look=(1, -0.3), walk=wk(4), hide=0.6 if scared else 0.0,
          lid=0.7 if sleepy else 0.0)
    cx = x_of('coco', t) - cam + 960
    mood, look, sad = 'smile', (1, -0.3), 0.0
    ar, al = math.radians(65 + 6 * math.sin(t * 2)), math.radians(115 - 6 * math.sin(t * 2))
    if 7.0 < t < 13.0: mood, look, sad = 'sad', (1, -0.4), 0.6
    if scared: mood, look = 'o', (math.sin(t * 2), -0.3)
    if song: ar, al = math.radians(-58 + 20 * math.sin(t * 6)), math.radians(-122 - 20 * math.sin(t * 6))
    if 59.0 < t < 66.0: mood = 'closed'
    if 68.0 < t < 84.0: look = (1, -1); mood = 'o' if t < 70 else 'smile'
    lid = 0.0
    if sleepy: mood = 'o' if 88.5 < t < 91.0 else ('closed' if t > 95 else 'smile'); lid = 0.5 if t < 95 else 0
    K.put(c, K.coco, cx, GROUND + bob(0), 0.55, t=t, mood=mood, look=look, sad=sad, arm_r=ar, arm_l=al, lid=lid, walk=wk(8))
    lox = x_of('coco', t) - 150 - cam + 960; loy = 420 + 20 * math.sin(t * 3)
    K.put(c, K.lola, lox, loy + bob(2.0), 0.5, t=t, flap=20, look=(1, 0.3), lid=0.6 if sleepy else 0.0)
    fg_bushes(c, cam); flowers_front(c, cam)
    # oscuridad con un hueco de luz alrededor de Luz y de la familia
    c.push_group()
    c.set_source_rgba(0.02, 0.02, 0.12, darkness(t)); c.paint()
    c.set_operator(cairo.OPERATOR_DEST_OUT)
    for (hx, hy, r, a) in [(lsx - 30, ly + 30, light_radius(t), 0.95)] + [(x, y, 170, 0.6 * a) for (x, y, a) in family_points(t, cam)]:
        if r <= 0 or a <= 0: continue
        g = cairo.RadialGradient(hx, hy, 0, hx, hy, r)
        g.add_color_stop_rgba(0, 0, 0, 0, a); g.add_color_stop_rgba(1, 0, 0, 0, 0)
        c.set_source(g); c.arc(hx, hy, r, 0, 2 * math.pi); c.fill()
    c.set_operator(cairo.OPERATOR_OVER)
    c.pop_group_to_source(); c.paint()
    # luces
    for k, (x, y, a) in enumerate(family_points(t, cam)):
        if a > 0: tiny(c, x, y, t, k, a)
    if t > 50.0:
        mx, my = MOM[0] - cam + 960, MOM[1] + 10 * math.sin(t * 2)
        if -200 < mx < W + 200: luz(c, mx, my, 0.85, t, 1.2, 'smile', flip=True)
    luz(c, lsx, ly, 0.55, t, luz_shine(t), 'sad' if t < 14.0 else 'smile')
    if song:
        for k in range(3):
            ph = (t * 0.7 + k / 3) % 1
            music_note(c, lox + 40 + 60 * ph, loy - 150 - 160 * ph, math.sin(math.pi * ph), ['#F48FB1', '#90CAF9', '#FFF59D'][k])
    if 59.0 < t < 66.0:
        for k in range(4):
            ph = ((t - 59.0) * 0.5 + k / 4) % 1
            heart(c, lsx + 60 + 60 * math.sin(k * 2), ly - 80 - 200 * ph, 0.9, math.sin(math.pi * ph))
    if sleepy:
        for k in range(3):
            ph = ((t - 86.0) * 0.4 + k / 3) % 1
            c.select_font_face('Fredoka Light', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
            c.set_font_size(40 + 30 * ph); c.set_source_rgba(1, 1, 1, math.sin(math.pi * ph) * ss(92, 94, t))
            c.move_to(cx + 80 + 60 * ph, GROUND - 300 - 150 * ph); c.show_text('z')
    # globitos
    bubble(c, lsx, ly - 120, '¡Me perdí!', (t - 7.0) / 3.0, 50)
    bubble(c, cx, GROUND - 300, '¡Te ayudamos!', (t - 10.6) / 3.0, 48)
    py_ = GROUND - 0.55 * (260 + neck)
    bubble(c, px + 60, py_ - 120, '¡Veo lucecitas allá!', (t - 15.6) / 4.6, 44)
    bubble(c, cx, GROUND - 300, '¡Qué oscuro!', (t - 30.6) / 3.0, 50)
    bubble(c, lox, loy - 180, '¡Cantemos!', (t - 33.5) / 2.6, 52)
    bubble(c, lsx, ly - 120, '¡Mamá!', (t - 56.0) / 2.6, 56)
    bubble(c, lsx, ly - 120, '¡Gracias, amigos!', (t - 84.0) / 3.4, 46)

def flowers_front_dark(c, cam):
    c.push_group(); flowers_front(c, cam); c.pop_group_to_source(); c.paint_with_alpha(0.55)

def overlay(c, t):
    if t < 5.6:
        a = 1 - ss(4.8, 5.5, t)
        c.push_group(); word(c, 'La luciérnaga perdida', W / 2, 230, 120 * K_back((t - 0.6) / 0.6) + 0.01,
                             colors=['#FFEB3B', '#FFF59D', '#B2FF59'], tilt=0.05, outline=9)
        c.pop_group_to_source(); c.paint_with_alpha(a)
    if t > 94.0:
        s = K_back((t - 94.0) / 0.7)
        word(c, '¡Buenas noches!', W / 2, 200, 140 * s + 0.01, colors=['#FFEB3B', '#B2FF59', '#80D8FF'], tilt=0.05, outline=10)
    a = max(1 - ss(0, 0.8, t), ss(DUR - 2.0, DUR, t))
    if a > 0: c.set_source_rgba(0, 0, 0.1, a); c.paint()

if __name__ == '__main__':
    args = sys.argv[1:]
    if args and args[0] == 'srt':
        print(srt(NARRACION, float(args[1]) if len(args) > 1 else 0.0)); sys.exit()
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(surf)
    def full(c, t): frame(c, t); overlay(c, t)
    if args and args[0] == 'stills':
        for t in map(float, args[1:]):
            c.save(); full(c, t); c.restore(); surf.write_to_png(f'ep19_{t}.png')
    else:
        t0, t1 = (float(args[1]), float(args[2])) if args and args[0] == 'range' else (0, DUR)
        out = sys.stdout.buffer
        for i in range(int(round(t0 * FPS)), int(round(t1 * FPS))):
            c.save(); full(c, i / FPS); c.restore(); surf.flush(); out.write(surf.get_data())
