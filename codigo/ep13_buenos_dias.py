"""Episodio 13 — ¡Buenos días, selva! (rutina de la mañana para hacer juntos, 98 s).
Sale el sol, Lola despierta a todos, y hacemos juntos: estirarse, saltar, aplaudir,
lavarse la carita, lavarse los dientes y desayunar.

      python3 ep13_buenos_dias.py srt 5.5     -> subtítulos .srt de la narración
Uso:  python3 ep13_buenos_dias.py              -> cuadros crudos por stdout
      python3 ep13_buenos_dias.py range 0 49   -> solo un tramo
      python3 ep13_buenos_dias.py stills 12 65 -> PNG sueltos"""
import cairo, math, sys
import cuerpos as K
from amigos import hexc, ellipse, fill, OUT
from logos import word, sparkle, font
from ep02_puente_del_rio import kf, ss, moving, K_back, music_note
from ep03_donde_esta_tomi import bubble
from ep09_semilla_magica import SKY, LAND, cloud, srt, fruit

W, H, FPS = 1920, 1080, 30
DUR = 98.0
GROUND = 880
PIPA_X, TITO_X, TOMI_X, COCO_STAND = 300, 620, 900, 1180
HAM = (1260, 1660)

NARRACION = [
    (6.0, 11.0, 'El sol sale despacito en la selva... ¡es de mañana!'),
    (12.0, 17.0, 'Lola canta para despertar a todos sus amigos.'),
    (18.0, 24.0, 'Pipa abre los ojos, Tito bosteza... y Tomi se asoma de su caparazón.'),
    (25.0, 30.0, '¡Y Coco se despierta de un salto!'),
    (31.0, 37.0, '¡A estirarse! Arriba los brazos, bien alto.'),
    (38.0, 44.0, '¡Ahora a saltar! Uno, dos y tres.'),
    (45.0, 51.0, '¡Y aplaudimos todos juntos!'),
    (52.0, 58.0, 'Tito nos lava la carita con su trompa.'),
    (59.0, 65.0, 'Ahora, a lavarse los dientes: arriba y abajo.'),
    (66.0, 72.0, '¡Y a desayunar! Frutas ricas para todos.'),
    (82.0, 88.0, '¡Listos para un día lleno de aventuras! ¡Buen día!'),
]
ACTIONS = [(31.0, 37.5, '¡Arriba los brazos!'), (38.0, 44.5, '¡A saltar!'), (45.0, 51.5, '¡A aplaudir!'),
           (52.0, 58.5, '¡A lavarse la carita!'), (59.0, 65.5, '¡A lavarse los dientes!'), (66.0, 72.5, '¡A desayunar!')]
JUMPS = [39.0, 40.6, 42.2]

def dawn(t): return 1 - ss(4, 13, t)     # 1 = amanecer anaranjado

def sun_pos(t): return 1450, kf(t, [(2, 760), (13, 170)])

def draw_sun(c, t):
    x, y = sun_pos(t)
    for i in range(12):
        c.save(); c.translate(x, y); c.rotate(i * math.pi / 6 + t * 0.2)
        c.move_to(-20, -110); c.line_to(0, -158); c.line_to(20, -110); c.close_path(); c.set_source_rgba(*hexc('#FFB300')); c.fill(); c.restore()
    ellipse(c, x, y, 90, 90); fill(c, hexc('#FFEB3B'), hexc('#F9A825'), 7)
    c.set_source_rgba(*OUT); c.set_line_width(7); c.set_line_cap(cairo.LINE_CAP_ROUND)
    awake = ss(9, 10, t)
    for ex in (-30, 30):
        if awake < 0.5: c.arc(x + ex, y - 8, 14, 0.15 * math.pi, 0.85 * math.pi); c.stroke()
        else:
            ellipse(c, x + ex, y - 10, 9, 12); c.set_source_rgba(*OUT); c.fill()
    c.arc(x, y + 14, 32, 0.15 * math.pi, 0.85 * math.pi); c.stroke()
    for ex in (-58, 58):
        ellipse(c, x + ex, y + 18, 14, 9); c.set_source_rgba(*hexc('#FF7043', 0.6)); c.fill()

def hammock(c, front):
    a, b = HAM
    if not front:
        for x in (a, b):
            c.rectangle(x - 12, 600, 24, GROUND - 600); fill(c, hexc('#8D5524'), OUT, 5)
        c.move_to(a, 640); c.curve_to(a + 120, 800, b - 120, 800, b, 640)
        c.set_source_rgba(*OUT); c.set_line_width(6); c.stroke()
    else:
        c.move_to(a + 30, 680); c.curve_to(a + 130, 805, b - 130, 805, b - 30, 680)
        c.line_to(b - 40, 700); c.curve_to(b - 140, 830, a + 140, 830, a + 40, 700); c.close_path()
        fill(c, hexc('#FF8A65'), OUT, 5)
        for k in range(1, 6):
            u = k / 6; x = a + 30 + (b - a - 60) * u
            c.move_to(x, 690 + 110 * math.sin(math.pi * u)); c.line_to(x, 715 + 110 * math.sin(math.pi * u))
            c.set_source_rgba(*hexc('#FFE0B2')); c.set_line_width(10); c.stroke()

def coco_pose(t):
    """(x, y, rot) de Coco: acostado en la hamaca, salto y de pie."""
    lying = (1590, 712, -1.57)
    if t < 26: return lying[0], lying[1] - 4 * math.sin(t * 1.2), lying[2]
    if t < 27.2:
        q = ss(26, 27.2, t)
        return lying[0] + (COCO_STAND - lying[0]) * q, lying[1] + (GROUND - lying[1]) * q - 180 * math.sin(math.pi * q), lying[2] * (1 - q)
    return COCO_STAND, GROUND, 0.0

def zzz(c, x, y, t, t0, t1):
    if not t0 < t < t1: return
    for k in range(3):
        p = ((t - t0) / 2.4 - k / 3.0)
        if p < 0: continue
        p %= 1.0
        a = math.sin(math.pi * p) * min(1, (t1 - t) / 0.5)
        word(c, 'z', x + 50 * p, y - 120 * p, 30 + 30 * p, colors=['#5C6BC0'], outline=3) if a > 0.05 else None

def clap(t): return math.radians(-60) + 0.35 * abs(math.sin(t * 10))

def jump(t):
    for j in JUMPS:
        if j < t < j + 0.8: return 110 * math.sin(math.pi * (t - j) / 0.8)
    return 0.0

def party(t): return 82 < t < 96

def toothbrush(c, x, y, t, s=1.0, col='#29B6F6'):
    dx = 14 * math.sin(t * 16)
    c.save(); c.translate(x + dx, y); c.rotate(-0.5); c.scale(s, s)
    c.rectangle(-8, 0, 16, 90); fill(c, hexc(col), OUT, 4)
    c.rectangle(-12, -32, 24, 34); fill(c, (1, 1, 1, 1), OUT, 4)
    c.restore()
    for k in range(5):
        ph = (t * 1.5 + k / 5) % 1
        ellipse(c, x + 30 * math.sin(k * 2.3), y - 10 - 40 * ph, 6 + 6 * ph, 6 + 6 * ph)
        c.set_source_rgba(1, 1, 1, 0.9 * (1 - ph)); c.fill_preserve(); c.set_source_rgba(*hexc('#90CAF9', 1 - ph)); c.set_line_width(2); c.stroke()

def watermelon(c, x, y, s=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.move_to(-40, 0); c.arc_negative(0, 0, 40, math.pi, 0); c.close_path()
    c.new_path(); c.arc(0, 0, 40, 0, math.pi); c.close_path(); fill(c, hexc('#43A047'), OUT, 4)
    c.arc(0, 0, 32, 0, math.pi); c.close_path(); c.set_source_rgba(*hexc('#EF5350')); c.fill()
    for k in range(4): ellipse(c, -18 + k * 12, 12 + (k % 2) * 6, 3, 5); c.set_source_rgba(*OUT); c.fill()
    c.restore()

def world(c, t):
    c.set_source_surface(SKY, 0, 0); c.paint()
    d = dawn(t)
    if d > 0:
        g = cairo.LinearGradient(0, 0, 0, H)
        g.add_color_stop_rgb(0, *hexc('#7E57C2')[:3]); g.add_color_stop_rgb(0.35, *hexc('#FF8A65')[:3]); g.add_color_stop_rgb(0.75, *hexc('#FFCC80')[:3]); g.add_color_stop_rgb(1, *hexc('#FFF3E0')[:3])
        c.set_source(g); c.paint_with_alpha(d)
    draw_sun(c, t)
    for (x0, y0, s, sp) in ((150, 160, 0.9, 10), (700, 110, 0.7, 7)):
        cloud(c, (x0 + sp * t) % 2300 - 250, y0, s, (1, 0.95 if d > 0.5 else 1, 0.92 if d > 0.5 else 1, 1))
    c.set_source_surface(LAND, 0, 0); c.paint()
    if d > 0: c.set_source_rgba(0.95, 0.45, 0.3, 0.18 * d); c.mask_surface(LAND, 0, 0)
    hammock(c, front=False)
    bounce = lambda ph: -25 * abs(math.sin(t * 4.5 + ph)) if party(t) else 0
    stretch = ss(31, 32, t) * (1 - ss(36.5, 37.5, t))
    j = jump(t)
    clapping = 45 < t < 51
    eat = 67 < t < 80
    # breakfast leaf with fruits
    if 65.5 < t < 81:
        a = ss(65.5, 66.3, t) * (1 - ss(80.3, 81, t))
        c.push_group()
        ellipse(c, 760, 975, 300, 45); fill(c, hexc('#66BB6A'), OUT, 5)
        for k, (fx, col) in enumerate(((560, '#F44336'), (660, '#FF9800'), (760, '#AB47BC'), (860, '#FFEB3B'), (960, '#29B6F6'))):
            fruit(c, fx, 950, col, 0.9)
        c.pop_group_to_source(); c.paint_with_alpha(a)
    # Pipa
    plid = 1.0 - ss(18.3, 19.0, t)
    neck = 300 + 220 * stretch
    if eat: neck = kf(t, [(67, 300), (68, 160), (79, 160), (80, 300)])
    K.put(c, K.pipa, PIPA_X, GROUND + bounce(0.5) - j, 0.55, t=t, neck=neck, look=(0.5, -0.2) if t > 19 else (0, 0))
    if plid > 0.01:  # eyelids on Pipa (drawn as closed lines)
        hx, hy = PIPA_X, GROUND - 0.55 * (260 + neck) + 0.55 * 0.85 * 0
        ey = GROUND - 0.55 * (260 + neck) + 0.55 * 0.85 * (-30)
        for ex in (-48, 48):
            ellipse(c, hx + 0.55 * 0.85 * ex, ey, 0.47 * 32, 0.47 * 40); c.set_source_rgba(*hexc('#FFCF40')); c.fill()
            c.set_source_rgba(*OUT); c.set_line_width(4); c.arc(hx + 0.55 * 0.85 * ex, ey - 2, 11, 0.15 * math.pi, 0.85 * math.pi); c.stroke()
    if eat and 68 < t < 79:
        ellipse(c, PIPA_X + 30, GROUND - 0.55 * (260 + neck) + 70, 22, 10); fill(c, hexc('#43A047'), OUT, 3)
    # Tito
    tlid = 1.0 - ss(20.3, 22.6, t) if t < 22.6 else 0.0
    if 20 < t < 22.5: tlid = 0.6
    yawn = math.sin(math.pi * (t - 20) / 2.5) if 20 < t < 22.5 else 0
    reach = None
    if stretch > 0: reach = 150 + 120 * stretch
    if 52 < t < 58.5: reach = 260
    K.put(c, K.tito, TITO_X, GROUND + bounce(1.0) - j, 0.6, t=t, lid=max(tlid, 0) if t < 23 else 0, yawn=yawn, reach=reach, look=(1, -0.3))
    if 52.5 < t < 58:  # water shower for everyone
        tip = (TITO_X + 0.6 * 260, GROUND - 36)
        for k in range(26):
            q = ((t - 52.5) * 0.9 + k / 26) % 1
            side = -1 if k % 3 == 0 else 1
            span = [320, 560, 900][k % 3]
            x = tip[0] + side * span * q * (0.6 if side < 0 else 1)
            y = tip[1] - 520 * q + 640 * q * q
            ellipse(c, x, y, 7, 10); c.set_source_rgba(*hexc('#4FC3F7', 1 - 0.5 * q)); c.fill()
    if eat: watermelon(c, TITO_X + 0.6 * 200, GROUND - 0.6 * 160, 0.9)
    # Tomi
    hide = 1.0 - ss(22.2, 23.2, t)
    K.put(c, K.tomi, TOMI_X, GROUND + bounce(1.5) - (j * 0.6 if hide < 0.1 else 0), 0.55, t=t, hide=hide, look=(0.5, -0.2))
    zzz(c, TOMI_X + 30, GROUND - 120, t, 1.0, 22.5)
    if eat: fruit(c, TOMI_X + 75, GROUND - 60, '#F44336', 0.7)
    # Coco
    cx, cy, rot = coco_pose(t)
    mood, look, lid = 'smile', (0.6, -0.3), 0.0
    arm_r, arm_l = math.radians(65 + 6 * math.sin(t * 2)), math.radians(115 - 6 * math.sin(t * 2))
    arm_len = 115
    if t < 26: lid = 1.0; mood = 'closed'; arm_r, arm_l = math.radians(100), math.radians(80)
    if 26 <= t < 28: mood = 'o'; arm_r, arm_l = math.radians(-60), math.radians(-120)
    if stretch > 0.01:
        arm_r = arm_r * (1 - stretch) + math.radians(-80) * stretch; arm_l = arm_l * (1 - stretch) + math.radians(-100) * stretch
        arm_len = 115 + 30 * stretch; look = (0, -1)
    if 38 < t < 44.5: arm_r, arm_l = math.radians(-60), math.radians(-120)
    if clapping: arm_r = clap(t); arm_l = math.pi - arm_r
    if 52.5 < t < 58: mood = 'closed'; arm_r, arm_l = math.radians(-60 + 20 * math.sin(t * 8)), math.radians(-120 - 20 * math.sin(t * 8))
    if 59 < t < 65.5: arm_r = math.radians(-132); look = (0, 0)
    hold = 'banana' if eat else None
    if eat: arm_r = math.radians(-60); mood = 'chew' if (t % 3) < 2 else 'smile'
    if party(t): arm_r, arm_l = math.radians(-58 + 25 * math.sin(t * 9)), math.radians(-122 - 25 * math.sin(t * 9))
    if t < 26: hammock_y = 0
    K.put(c, K.coco, cx, cy + (bounce(0) - j if t > 27.2 else 0), 0.55, rot=rot, t=t, mood=mood, look=look, lid=lid,
          arm_r=arm_r, arm_l=arm_l, arm_len=arm_len, hold=hold, chew=t)
    if t < 26: hammock(c, front=True); zzz(c, 1360, 640, t, 1.0, 25.8)
    else: hammock(c, front=True)
    if 59 < t < 65.5:
        toothbrush(c, cx + 18, GROUND - 0.55 * 255 + 10, t, 0.8)
    # Lola
    lx = kf(t, [(0, 2100), (11.5, 2100), (14, 1000), (66, 1000)]) + (60 * math.sin(t * 0.8) if t > 14 else 0)
    ly = kf(t, [(0, 300), (11.5, 300), (14, 430)]) + 15 * math.sin(t * 3) - j * 0.6
    K.put(c, K.lola, lx, ly + bounce(2.0), 0.5, t=t, flap=20, look=(-0.5, 0.4))
    if 12.5 < t < 26 or party(t):
        for k in range(3):
            ph = (t * 0.7 + k / 3) % 1
            music_note(c, lx + 40 + 60 * ph, ly - 150 - 160 * ph, math.sin(math.pi * ph), ['#E91E63', '#1E88E5', '#FF9800'][k])
    if eat: ellipse(c, lx + 30, ly - 60, 10, 7); fill(c, hexc('#FFE082'), OUT, 2)
    # stars of fun when everyone is awake
    if 27.2 < t < 29:
        q = (t - 27.2) / 1.8
        for k in range(8):
            a = k * math.pi / 4
            sparkle(c, COCO_STAND + 140 * q * math.cos(a), GROUND - 140 + 110 * q * math.sin(a), 26 * math.sin(math.pi * q))
    bubble(c, lx, ly - 120, '¡Buenos días!', (t - 14.2) / 3.0, 50)
    bubble(c, COCO_STAND, GROUND - 300, '¡Buen día!', (t - 27.4) / 2.6, 52)

def overlay(c, t):
    if t < 5.6:
        a = 1 - ss(4.8, 5.5, t)
        c.push_group(); word(c, '¡Buenos días, selva!', W / 2, 230, 125 * K_back((t - 0.6) / 0.6) + 0.01, tilt=0.05, outline=9)
        c.pop_group_to_source(); c.paint_with_alpha(a)
    for (a, b, txt) in ACTIONS:
        if a <= t < b:
            s = K_back((t - a) / 0.4) * (1 - ss(b - 0.3, b, t))
            word(c, txt, W / 2, 190 + 6 * math.sin(t * 5), 120 * s + 0.01, tilt=0.05, outline=10)
    for k, jt in enumerate(JUMPS):
        if jt <= t < jt + 1.3:
            s = K_back((t - jt) / 0.3)
            word(c, str(k + 1), W / 2, 380, 200 * s + 0.01, colors=[['#FF4081', '#00B0FF', '#00C853'][k]], outline=12)
    if t > 88:
        s = K_back((t - 88) / 0.7)
        word(c, '¡Buen día,', W / 2, 180, 125 * s + 0.01, tilt=0.06, outline=10)
        word(c, 'amigos!', W / 2, 320, 125 * s + 0.01, start=3, tilt=0.06, outline=10)
    a = max(1 - ss(0, 0.8, t), ss(DUR - 2.0, DUR, t))
    if a > 0: c.set_source_rgba(1, 1, 1, a); c.paint()

CAM = [(0, 1.0, 960, 540), (14, 1.0, 960, 540), (17, 1.15, 760, 600), (23.5, 1.15, 760, 600), (25, 1.25, 1350, 620),
       (29, 1.25, 1300, 620), (30.5, 1.0, 960, 540), (58.5, 1.0, 960, 540), (59.5, 1.45, 1180, 700), (65, 1.45, 1180, 700),
       (66, 1.0, 960, 540)]
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
    args = sys.argv[1:]
    if args and args[0] == 'srt':
        print(srt(NARRACION, float(args[1]) if len(args) > 1 else 0.0)); sys.exit()
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(surf)
    if args and args[0] == 'stills':
        for t in map(float, args[1:]):
            c.save(); frame(c, t); c.restore(); surf.write_to_png(f'ep13_{t}.png')
    else:
        t0, t1 = (float(args[1]), float(args[2])) if args and args[0] == 'range' else (0, DUR)
        out = sys.stdout.buffer
        for i in range(int(round(t0 * FPS)), int(round(t1 * FPS))):
            c.save(); frame(c, i / FPS); c.restore(); surf.flush(); out.write(surf.get_data())
