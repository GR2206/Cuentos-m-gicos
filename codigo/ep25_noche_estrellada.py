"""Episodio 25 — Una noche estrellada en la selva (110 s). "A dormir con…": lento y suave.
Los amigos, acostados sobre una mantita, miran el cielo. Las estrellas dibujan una banana, un corazón y una
tortuguita; pasan estrellas fugaces y piden un deseo; llegan las luciérnagas, Lola canta bajito
y uno por uno se van durmiendo. Hasta la luna cierra los ojitos.

Uso:  python3 ep25_noche_estrellada.py              -> cuadros crudos por stdout
      python3 ep25_noche_estrellada.py range 0 55   -> solo un tramo
      python3 ep25_noche_estrellada.py stills 20 70 -> PNG sueltos
      python3 ep25_noche_estrellada.py srt 5.5      -> subtítulos .srt de la narración"""
import cairo, math, random, sys
import cuerpos as K
from amigos import hexc, ellipse, fill, OUT
from logos import word, sparkle
from ep02_puente_del_rio import kf, ss, K_back, music_note
from ep03_donde_esta_tomi import bubble
from ep09_semilla_magica import srt
from ep19_luciernaga import luz, glow, tiny

W, H, FPS = 1920, 1080, 30
DUR = 110.0
GROUND = 905
LIE = -math.pi / 2          # acostado: cabeza a la izquierda, mirando al cielo

NARRACION = [
    (6.5, 14.0, 'Era una noche tranquila en la selva. Los amigos se acostaron en la mantita a mirar el cielo.'),
    (16.0, 21.0, 'Había muchísimas estrellas... ¡y algunas formaban dibujos!'),
    (22.0, 30.0, 'Pipa, que ve todo desde arriba, encontró una banana. ¡A Coco le encantó!'),
    (33.0, 41.0, 'Después, un corazón de estrellas.'),
    (44.0, 52.0, 'Y una tortuguita... ¡igualita a Tomi!'),
    (54.0, 61.0, 'Pasaron estrellas fugaces, y cada uno cerró los ojos para pedir un deseo.'),
    (63.0, 73.0, 'Llegaron Luz y las luciérnagas, y Lola cantó una canción bajito, bajito.'),
    (76.0, 86.0, 'Tomi se acurrucó en su caparazón. Tito bostezó. Pipa cerró los ojitos...'),
    (88.0, 95.0, 'Coco miró las estrellas una vez más, y dijo despacito: buenas noches, estrellas.'),
    (98.0, 106.0, 'Y hasta la luna cerró los ojos. Buenas noches, amigos.'),
]

rnd = random.Random(7)
STARS = [(rnd.uniform(0, W), rnd.uniform(0, 640), rnd.uniform(1.5, 4.0), rnd.uniform(0, 6.28)) for _ in range(160)]

def path_pts(fn, n): return [fn(k / (n - 1)) for k in range(n)]
BANANA = path_pts(lambda u: (760 + 330 * math.cos(math.pi * (0.15 + 0.7 * u)), 360 - 230 * math.sin(math.pi * (0.15 + 0.7 * u)) + 120), 8)
def heart_pt(u):
    a = 2 * math.pi * u
    return 960 + 13 * 16 * math.sin(a) ** 3, 300 - 13 * (13 * math.cos(a) - 5 * math.cos(2 * a) - 2 * math.cos(3 * a) - math.cos(4 * a))
HEART = path_pts(heart_pt, 13)
TURTLE = [(820, 360), (900, 290), (1020, 290), (1100, 360), (1020, 410), (900, 410), (820, 360), (760, 340), (720, 320),
          (1100, 360), (1150, 390), (880, 410), (860, 450), (1040, 410), (1060, 450)]
TURTLE_EDGES = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 0), (0, 7), (7, 8), (3, 10), (5, 12), (4, 14)]
CONST = [(22.0, 32.5, BANANA, None, '#FFF59D'), (33.0, 43.5, HEART, None, '#FF80AB'), (44.0, 53.5, TURTLE, TURTLE_EDGES, '#B9F6CA')]

def const_draw(c, t):
    for (a, b, pts, edges, col) in CONST:
        if not (a < t < b): continue
        fade = ss(a, a + 0.6, t) * (1 - ss(b - 1.2, b, t))
        n = len(pts)
        es = edges or [(k, k + 1) for k in range(n - 1)]
        prog = ss(a + 0.8, a + 5.5, t) * len(es)
        c.set_line_cap(cairo.LINE_CAP_ROUND)
        for k, (i, j) in enumerate(es):
            q = max(0.0, min(1.0, prog - k))
            if q <= 0: continue
            (x0, y0), (x1, y1) = pts[i], pts[j]
            c.move_to(x0, y0); c.line_to(x0 + (x1 - x0) * q, y0 + (y1 - y0) * q)
            c.set_source_rgba(*hexc(col)[:3], 0.75 * fade); c.set_line_width(5); c.stroke()
        for k, (x, y) in enumerate(pts):
            on = ss(a + 0.3 * k / n * 4, a + 0.3 * k / n * 4 + 0.5, t) * fade
            glow(c, x, y, 50, on, (1, 1, 0.85))
            sparkle(c, x, y, (14 + 4 * math.sin(t * 4 + k)) * on, '#FFFFFF')

def shooting(c, t):
    for (t0, x0, y0) in ((54.5, 300, 80), (56.2, 1100, 40), (58.0, 700, 120)):
        q = (t - t0) / 1.4
        if 0 < q < 1:
            x = x0 + 700 * q; y = y0 + 260 * q
            g = cairo.LinearGradient(x - 260, y - 97, x, y)
            g.add_color_stop_rgba(0, 1, 1, 1, 0); g.add_color_stop_rgba(1, 1, 1, 0.8, 0.95 * math.sin(math.pi * q))
            c.move_to(x - 260, y - 97); c.line_to(x, y); c.set_source(g); c.set_line_width(7); c.stroke()
            sparkle(c, x, y, 20 * math.sin(math.pi * q), '#FFFFFF')

def moon(c, t):
    x, y = 1640, 170
    glow(c, x, y, 260, 0.55, (1, 1, 0.8))
    ellipse(c, x, y, 95, 95); fill(c, hexc('#FFF9C4'), hexc('#F9A825'), 6)
    for (dx, dy, r) in ((-40, -40, 14), (35, -50, 9), (45, 30, 12)): ellipse(c, x + dx, y + dy, r, r); c.set_source_rgba(*hexc('#F0E68C', 0.8)); c.fill()
    closed = ss(98.0, 100.0, t)
    c.set_source_rgba(*OUT); c.set_line_width(6); c.set_line_cap(cairo.LINE_CAP_ROUND)
    for ex in (-30, 30):
        if closed > 0.5:
            c.arc(x + ex, y - 5, 14, 0.15 * math.pi, 0.85 * math.pi); c.stroke()
        else:
            ellipse(c, x + ex, y - 8, 8, 10); c.fill()
    c.arc(x, y + 22, 22, 0.2 * math.pi, 0.8 * math.pi); c.stroke()
    for ex in (-55, 55): ellipse(c, x + ex, y + 18, 14, 8); c.set_source_rgba(*hexc('#FF8A80', 0.7)); c.fill()

def landscape(c, t):
    g = cairo.LinearGradient(0, 0, 0, H)
    g.add_color_stop_rgb(0, *hexc('#0B0930')[:3]); g.add_color_stop_rgb(0.55, *hexc('#24207A')[:3]); g.add_color_stop_rgb(0.85, *hexc('#4A3B8F')[:3])
    c.set_source(g); c.paint()
    c.save(); c.translate(960, 300); c.rotate(-0.25)   # vía láctea suave
    gg = cairo.LinearGradient(0, -120, 0, 120)
    gg.add_color_stop_rgba(0, 1, 1, 1, 0); gg.add_color_stop_rgba(0.5, 0.85, 0.8, 1, 0.12); gg.add_color_stop_rgba(1, 1, 1, 1, 0)
    c.rectangle(-1300, -120, 2600, 240); c.set_source(gg); c.fill(); c.restore()
    for (x, y, r, ph) in STARS:
        ellipse(c, x, y, r, r); c.set_source_rgba(1, 1, 0.85, 0.45 + 0.55 * (0.5 + 0.5 * math.sin(t * 1.5 + ph))); c.fill()
    moon(c, t)
    for (cx_, cy_, rx, col) in ((300, 1000, 900, '#1E3A2F'), (1600, 1020, 1000, '#183126')):
        ellipse(c, cx_, cy_, rx, 260); c.set_source_rgba(*hexc(col)); c.fill()
    for k in range(7):   # siluetas de palmeras
        x = 80 + 300 * k + (60 if k % 2 else 0)
        if 500 < x < 1500: continue
        c.move_to(x, 880); c.curve_to(x + 5, 760, x + 15, 640, x + 25, 560); c.set_source_rgba(*hexc('#0F2019')); c.set_line_width(26); c.stroke()
        for a in (-160, -120, -80, -40, -5):
            c.save(); c.translate(x + 25, 560); c.rotate(math.radians(a + 4 * math.sin(t * 0.6 + k)))
            c.move_to(0, 0); c.curve_to(60, -40, 150, -30, 210, 30); c.curve_to(140, 12, 60, 18, 0, 0); c.close_path()
            c.set_source_rgba(*hexc('#0F2019')); c.fill(); c.restore()
    c.rectangle(0, 880, W, H - 880); c.set_source_rgba(*hexc('#244A39')); c.fill()
    # mantita
    c.save(); c.translate(1000, GROUND + 30); c.scale(1, 0.22)
    ellipse(c, 0, 0, 820, 260); fill(c, hexc('#7E57C2'), OUT, 14)
    c.save(); ellipse(c, 0, 0, 820, 260); c.clip()
    for k in range(-12, 13): c.rectangle(k * 70, -300, 30, 600); c.set_source_rgba(1, 1, 1, 0.18); c.fill()
    c.restore(); c.restore()

def frame(c, t):
    pan = 180 * ss(97.0, 106.0, t)   # al final la cámara sube hacia el cielo
    c.save(); c.translate(0, pan)
    landscape(c, t)
    const_draw(c, t)
    shooting(c, t)
    wish = 56.0 < t < 60.5
    sleep = lambda t0: ss(t0, t0 + 2.0, t)
    look_up = (1, 0)
    # Pipa (acostada, la más larga)
    K.put(c, K.pipa, 1830, GROUND - 70, 0.56, rot=LIE, t=t, look=look_up, lid=1.0 if wish else sleep(82.0))
    # Tito
    K.put(c, K.tito, 930, GROUND - 90, 0.7, rot=LIE, t=t, look=look_up, lid=1.0 if wish else sleep(79.0),
          yawn=math.sin(math.pi * ss(77.0, 79.5, t)))
    # Coco
    yawn = 88.0 < t < 89.6
    mood = 'o' if yawn else ('closed' if wish else 'smile')
    clid = sleep(94.5) if not wish else 0.0
    if t > 96.5: mood = 'closed'
    K.put(c, K.coco, 1390, GROUND - 75, 0.75, rot=LIE, t=t, look=look_up, mood=mood, lid=clid,
          arm_r=math.radians(150), arm_l=math.radians(30))
    # Tomi (sentadita al costado)
    K.put(c, K.tomi, 400, GROUND + 10, 0.65, t=t, look=(0.6, -0.8), hide=sleep(75.5), lid=1.0 if wish else 0.0)
    # Lola (sobre una piedrita)
    ellipse(c, 150, GROUND + 5, 70, 26); fill(c, hexc('#5D4037'), OUT, 5)
    llid = 1.0 if wish else sleep(85.5)
    K.put(c, K.lola, 150, GROUND - 5, 0.5, t=t, flap=0, look=(-0.3, -0.8), lid=llid)
    # luciérnagas
    come = ss(62.0, 66.0, t)
    if come > 0:
        for k in range(18):
            a = k * 2.1 + t * 0.25
            x = 960 + (500 + 300 * math.sin(k)) * math.cos(a) * come + (1 - come) * 1100
            y = 600 + 160 * math.sin(a * 1.3 + k) - (1 - come) * 400
            tiny(c, x, y, t, k, come * (1 - 0.5 * ss(100, 106, t)))
        lx, ly = 1150 + 220 * math.cos(t * 0.4), 560 + 60 * math.sin(t * 0.8)
        luz(c, lx + (1 - come) * 800, ly - (1 - come) * 300, 0.45, t, 1.0)
    if 64.0 < t < 82.0:
        for k in range(3):
            ph = (t * 0.45 + k / 3) % 1
            music_note(c, 190 + 50 * ph, GROUND - 160 - 220 * ph, 0.8 * math.sin(math.pi * ph), ['#F48FB1', '#90CAF9', '#FFF59D'][k])
    if t > 90.0:   # zzz
        for (zx, zy, t0) in ((760, GROUND - 280, 81.0), (1180, GROUND - 280, 96.5), (1560, GROUND - 240, 84.0), (460, GROUND - 190, 77.5)):
            if t < t0: continue
            for k in range(3):
                ph = ((t - t0) * 0.35 + k / 3) % 1
                c.select_font_face('Fredoka Light', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
                c.set_font_size(36 + 26 * ph); c.set_source_rgba(1, 1, 1, 0.8 * math.sin(math.pi * ph))
                c.move_to(zx + 50 * ph, zy - 140 * ph); c.show_text('z')
    # globitos
    bubble(c, 1560, GROUND - 330, '¡Miren, una banana!', (t - 23.0) / 4.0, 42)
    bubble(c, 1150, GROUND - 360, '¡Mi preferida!', (t - 27.2) / 3.2, 44)
    bubble(c, 1150, GROUND - 360, '¡Un corazón!', (t - 37.0) / 3.4, 46)
    bubble(c, 400, GROUND - 300, '¡Soy yo!', (t - 48.0) / 3.2, 48)
    bubble(c, 1150, GROUND - 360, '¡Pidan un deseo!', (t - 54.0) / 2.4, 44)
    bubble(c, 1150, GROUND - 360, 'Buenas noches, estrellas…', (t - 90.0) / 4.2, 38)
    c.restore()

def overlay(c, t):
    if t < 6.5:
        a = 1 - ss(5.6, 6.4, t)
        c.push_group()
        word(c, 'Una noche estrellada', W / 2, 200, 115 * K_back((t - 0.8) / 0.8) + 0.01, colors=['#FFF59D', '#80D8FF', '#FF80AB'], tilt=0.04, outline=9)
        word(c, 'en la selva', W / 2, 320, 110 * K_back((t - 1.3) / 0.8) + 0.01, colors=['#B9F6CA', '#FFF59D', '#80D8FF'], tilt=0.04, outline=9)
        c.pop_group_to_source(); c.paint_with_alpha(a)
    if t > 101.0:
        s = ss(101.0, 102.5, t)
        c.push_group(); word(c, 'Buenas noches', W / 2, 330, 140, colors=['#FFF59D', '#80D8FF', '#FF80AB'], tilt=0.03, outline=10)
        c.pop_group_to_source(); c.paint_with_alpha(s)
    a = max(1 - ss(0, 1.5, t), ss(DUR - 3.5, DUR, t))
    if a > 0: c.set_source_rgba(0.02, 0.02, 0.08, a); c.paint()

if __name__ == '__main__':
    args = sys.argv[1:]
    if args and args[0] == 'srt':
        print(srt(NARRACION, float(args[1]) if len(args) > 1 else 0.0)); sys.exit()
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(surf)
    def full(c, t): frame(c, t); overlay(c, t)
    if args and args[0] == 'stills':
        for t in map(float, args[1:]):
            c.save(); full(c, t); c.restore(); surf.write_to_png(f'ep25_{t}.png')
    else:
        t0, t1 = (float(args[1]), float(args[2])) if args and args[0] == 'range' else (0, DUR)
        out = sys.stdout.buffer
        for i in range(int(round(t0 * FPS)), int(round(t1 * FPS))):
            c.save(); full(c, i / FPS); c.restore(); surf.flush(); out.write(surf.get_data())
