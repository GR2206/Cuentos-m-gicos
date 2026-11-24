"""Episodio 23 — La cueva del eco (100 s). Aventurita.
Los amigos encuentran una cueva. Coco grita "¡Hola!" y la cueva contesta... ¡es el eco! Juegan con el eco,
Tomi se anima a hablar, y Luz (la luciérnaga del ep. 19) los acompaña adentro: cuando cantan, los cristales
de la cueva se encienden de colores. Al salir, el atardecer: "¡Chau, cueva!".

Uso:  python3 ep23_cueva.py              -> cuadros crudos por stdout
      python3 ep23_cueva.py range 0 50   -> solo un tramo
      python3 ep23_cueva.py stills 20 70 -> PNG sueltos
      python3 ep23_cueva.py srt 5.5      -> subtítulos .srt de la narración"""
import cairo, math, random, sys
import cuerpos as K
from amigos import hexc, ellipse, fill, OUT
from logos import word, sparkle
from ep02_puente_del_rio import kf, ss, K_back, music_note
from ep03_donde_esta_tomi import bubble
from ep09_semilla_magica import SKY, LAND, cloud, sun, srt
from ep14_bananas_papa import heart
from ep19_luciernaga import luz, glow

W, H, FPS = 1920, 1080, 30
DUR = 100.0
GROUND = 880
MOUTH = (1480, 690)            # boca de la cueva (de donde sale el eco)
IN0, IN1 = 50.0, 84.0          # escena de adentro

NARRACION = [
    (6.0, 13.0, 'Caminando por la selva, los amigos encontraron una cueva enorme.'),
    (14.0, 21.5, 'Tomi tenía un poquito de miedo. Coco gritó: ¡Hola!... ¡y la cueva contestó!'),
    (23.0, 30.0, '¿Quién está ahí? Pipa se rió: ¡es el eco! La cueva repite todo lo que decimos.'),
    (31.0, 47.0, 'Jugaron con el eco: Lola cantó, Tito hizo sonar su trompa, y Tomi se animó a decir hola.'),
    (51.0, 58.0, 'Luz, la luciérnaga, llegó para iluminar el camino, y entraron todos juntos.'),
    (60.0, 70.0, 'Adentro había cristales... ¡y cuando cantaban, se encendían de colores!'),
    (72.0, 82.0, 'Era la cueva más linda del mundo, porque la exploraron juntos.'),
    (86.0, 94.0, 'Ya era el atardecer. ¡Chau, cueva! Y la cueva contestó: chau... chau...'),
    (95.0, 99.0, 'Con amigos, ¡somos más valientes!'),
]
# ecos: (momento, texto, tamaño)
ECHOS = [(16.2, '¡Hola!', 125), (24.0, '¿...ahí?', 100), (32.0, '¡La la la!', 110), (37.5, '¡Prrrú!', 110), (43.0, 'hola...', 75),
         (88.5, '¡Chau!', 125)]

def outside(t): return t < IN0 or t >= IN1
def dusk(t): return ss(84.0, 88.0, t)

# ---------------- afuera ----------------
def rock_hill(c, t):
    c.move_to(1020, GROUND + 20); c.curve_to(1060, 420, 1250, 250, 1500, 260); c.curve_to(1760, 270, 1900, 380, 1960, 520)
    c.line_to(1960, GROUND + 20); c.close_path(); fill(c, hexc('#A1887F'), OUT, 7)
    for (x, y, rx, ry) in ((1250, 450, 70, 40), (1700, 400, 90, 45), (1820, 640, 60, 35), (1180, 700, 55, 30)):
        ellipse(c, x, y, rx, ry); c.set_source_rgba(*hexc('#8D6E63')); c.fill()
    for (x, y) in ((1330, 300), (1620, 290)):
        for k in range(5):
            c.move_to(x + 12 * k, y + 10); c.curve_to(x + 12 * k - 10, y - 30, x + 12 * k + 10, y - 50, x + 12 * k + 5, y - 70)
            c.set_source_rgba(*hexc('#43A047')); c.set_line_width(8); c.stroke()
    # boca de la cueva
    c.move_to(1300, GROUND + 10); c.curve_to(1300, 560, 1660, 560, 1660, GROUND + 10); c.close_path()
    g = cairo.RadialGradient(1480, 800, 20, 1480, 760, 260)
    g.add_color_stop_rgb(0, *hexc('#120A08')[:3]); g.add_color_stop_rgb(1, *hexc('#3E2723')[:3])
    c.set_source(g); c.fill_preserve(); c.set_source_rgba(*OUT); c.set_line_width(8); c.stroke()
    for k, x in enumerate((1330, 1390, 1450, 1510, 1570, 1630)):   # estalactitas de la entrada
        y0 = 600 + 40 * abs(math.sin(k * 1.3)) + (30 if k in (0, 5) else 0)
        c.move_to(x - 18, y0); c.line_to(x, y0 + 45); c.line_to(x + 18, y0); c.close_path(); fill(c, hexc('#8D6E63'), OUT, 4)

def echo_text(c, t):
    for (t0, txt, size) in ECHOS:
        for j in range(3):
            tj = t0 + 0.55 * j
            if tj <= t < tj + 1.6:
                q = (t - tj) / 1.6
                a = min(1.0, 2.2 * (1 - q)) * (1.0 - 0.25 * j)
                c.push_group()
                word(c, txt, MOUTH[0] - 170 + 190 * j, MOUTH[1] - 190 - 120 * j - 80 * q, size * (1 - 0.25 * j) * K_back(q / 0.15) + 0.01,
                     colors=['#00B0FF', '#D500F9', '#FFD600'], tilt=0.05 * (j - 1), outline=9)
                c.pop_group_to_source(); c.paint_with_alpha(max(0, a))

def outside_scene(c, t):
    d = dusk(t)
    c.set_source_surface(SKY, 0, 0); c.paint()
    if d > 0:
        g = cairo.LinearGradient(0, 0, 0, H)
        g.add_color_stop_rgba(0, *hexc('#7E57C2')[:3], 0.85 * d); g.add_color_stop_rgba(0.6, *hexc('#FF8A65')[:3], 0.8 * d); g.add_color_stop_rgba(1, *hexc('#FFCC80')[:3], 0.7 * d)
        c.set_source(g); c.paint()
    c.push_group(); sun(c, t); c.pop_group_to_source(); c.paint_with_alpha(1 - d)
    if d > 0:
        sy = 520 + 120 * d
        glow(c, 300, sy, 260, d, (1, 0.6, 0.3)); ellipse(c, 300, sy, 80, 80); fill(c, hexc('#FF7043'), hexc('#E64A19'), 6)
    for (x0, y0, s, sp) in ((150, 160, 0.9, 10), (700, 110, 0.7, 7)): cloud(c, (x0 + sp * t) % 2300 - 250, y0, s)
    c.set_source_surface(LAND, 0, 0); c.paint()
    if d > 0: c.set_source_rgba(*hexc('#FF7043', 0.18 * d)); c.mask_surface(LAND, 0, 0)
    rock_hill(c, t)
    party = 30.0 < t < 47.0
    bob = lambda ph: -16 * abs(math.sin(t * 4 + ph)) if t > 95.0 else 0
    walk_in = lambda x0, x1: kf(t, [(0, x0 - 900), (6.0, x0 - 900), (11.0, x0)]) if t < IN0 else x0
    back = t >= IN1
    # Pipa
    px = walk_in(260, 260) if not back else kf(t, [(IN1, 1300), (86.5, 260)])
    K.put(c, K.pipa, px, GROUND + bob(0.5), 0.55, t=t, look=(1, 0) if 23 < t < 30 else (1, -0.2),
          walk=t * 7 if (6 < t < 11 or IN1 < t < 86.5) else 0)
    # Tito
    tx = walk_in(500, 500) if not back else kf(t, [(IN1, 1400), (86.5, 500)])
    trump = 36.8 < t < 38.2
    K.put(c, K.tito, tx, GROUND + bob(1.0), 0.6, t=t, look=(1, -0.2), reach=200 + 60 * math.sin(t * 20) if trump else None,
          walk=t * 6 if (6 < t < 11 or IN1 < t < 86.5) else 0, lid=0.8 if trump else 0.0)
    # Tomi
    tmx = walk_in(1000, 1000) if not back else kf(t, [(IN1, 1500), (86.5, 1000)])
    hide = ss(14.0, 14.6, t) * (1 - ss(41.5, 42.5, t)) if not back else 0
    peek = 0.5 * ss(26.0, 27.0, t) * (1 - ss(41.5, 42.5, t))
    K.put(c, K.tomi, tmx, GROUND + bob(1.5), 0.55, t=t, look=(1, 0), hide=max(0, hide - peek), walk=t * 4 if (6 < t < 11 or IN1 < t < 86.5) else 0)
    # Coco
    cx = walk_in(760, 760) if not back else kf(t, [(IN1, 1600), (86.5, 760)])
    mood, look = 'smile', (1, -0.1)
    ar, al = math.radians(65 + 6 * math.sin(t * 2)), math.radians(115 - 6 * math.sin(t * 2))
    if 11.0 < t < 14.0: mood = 'o'; ar = math.radians(-20)
    if 15.5 < t < 16.5 or 87.5 < t < 88.6: mood = 'o'; ar, al = math.radians(-100), math.radians(-80)    # manos en la boca
    if 16.5 < t < 22.5: mood = 'o'; look = (1, -0.4)
    if 43.0 < t < 47.0 or 47.0 < t < 50.0: ar, al = math.radians(-58 + 25 * math.sin(t * 9)), math.radians(-122 - 25 * math.sin(t * 9))
    if t > 88.6: ar = math.radians(-50 + 25 * math.sin(t * 8))
    if t > 95.0: ar, al = math.radians(-58 + 25 * math.sin(t * 9)), math.radians(-122 - 25 * math.sin(t * 9))
    K.put(c, K.coco, cx, GROUND + bob(0), 0.55, t=t, mood=mood, look=look, arm_r=ar, arm_l=al, walk=t * 8 if (6 < t < 11 or IN1 < t < 86.5) else 0)
    # Lola
    lx, ly = (640 + 60 * math.sin(t * 0.6), 430 + 18 * math.sin(t * 3))
    if t < 11.0: lx -= kf(t, [(0, 900), (6.0, 900), (11.0, 0)])
    K.put(c, K.lola, lx, ly + bob(2.0), 0.5, t=t, flap=20, look=(1, 0.3))
    if 31.5 < t < 34.0 or t > 95.0:
        for k in range(3):
            ph = (t * 0.7 + k / 3) % 1
            music_note(c, lx + 40 + 60 * ph, ly - 150 - 160 * ph, math.sin(math.pi * ph), ['#E91E63', '#1E88E5', '#FFD600'][k])
    # Luz llega
    if 47.0 < t < IN0:
        q = ss(47.0, 49.5, t)
        luz(c, 2100 - 600 * q, 300 + 200 * q, 0.55, t, 1.0)
    echo_text(c, t)
    # globitos
    bubble(c, cx, GROUND - 300, '¡Una cueva!', (t - 11.2) / 2.8, 52)
    bubble(c, tmx, GROUND - 230, 'Está oscura…', (t - 14.4) / 1.6, 44)
    bubble(c, cx, GROUND - 300, '¡HOLA!', (t - 15.6) / 1.4, 64)
    bubble(c, cx, GROUND - 300, '¿Quién está ahí?', (t - 22.6) / 2.0, 46)
    bubble(c, px + 30, GROUND - 0.55 * 560 - 110, '¡Es el eco!', (t - 26.0) / 3.6, 50)
    bubble(c, lx, ly - 170, '¡La la la!', (t - 31.3) / 1.8, 52)
    bubble(c, tmx, GROUND - 230, 'hola…', (t - 42.4) / 1.6, 40)
    bubble(c, cx, GROUND - 300, '¡Bravo, Tomi!', (t - 44.2) / 2.6, 48)
    bubble(c, cx, GROUND - 300, '¡CHAU, CUEVA!', (t - 87.4) / 1.6, 56)
    if 45.0 < t < 48.0:
        for k in range(4):
            ph = ((t - 45.0) * 0.6 + k / 4) % 1
            heart(c, tmx - 100 + 70 * k, GROUND - 260 - 160 * ph, 0.8, math.sin(math.pi * ph))

# ---------------- adentro ----------------
CRYSTALS = [(300, 560, '#E040FB', 1.0), (520, 330, '#00E5FF', 0.8), (830, 250, '#FFD600', 0.9), (1150, 300, '#76FF03', 0.8),
            (1440, 260, '#FF4081', 1.0), (1700, 420, '#448AFF', 0.9), (1600, 760, '#FFAB40', 1.1), (180, 820, '#64FFDA', 0.9),
            (1050, 620, '#E040FB', 0.7), (700, 700, '#00E5FF', 0.7)]
def song(t): return 60.0 < t < 72.0
def crystal_light(k, t):
    on = ss(60.5 + 0.9 * k, 61.2 + 0.9 * k, t)
    return on * (0.75 + 0.25 * math.sin(t * 4 + k))

def crystal(c, x, y, col, s, light, t, k):
    if light > 0: glow(c, x, y - 40 * s, 230 * s, light, hexc(col)[:3])
    c.save(); c.translate(x, y); c.scale(s, s)
    for (dx, h, w, rot) in ((-34, 110, 26, -0.35), (0, 150, 32, 0.0), (34, 100, 24, 0.35)):
        c.save(); c.translate(dx * 0.6, 0); c.rotate(rot)
        c.move_to(-w, 0); c.line_to(-w, -h * 0.7); c.line_to(0, -h); c.line_to(w, -h * 0.7); c.line_to(w, 0); c.close_path()
        base = hexc(col)
        dark = tuple(v * (0.45 + 0.55 * light) for v in base[:3]) + (1,)
        fill(c, dark, OUT, 5)
        c.move_to(0, -h); c.line_to(-w * 0.4, -h * 0.6); c.line_to(-w * 0.4, -10); c.set_source_rgba(1, 1, 1, 0.35 + 0.3 * light); c.set_line_width(4); c.stroke()
        c.restore()
    c.restore()
    if light > 0.6: sparkle(c, x + 30 * s, y - 130 * s, 14 * (0.5 + 0.5 * math.sin(t * 5 + k)), '#FFFFFF')

def luz_in(t):
    return 760 + 520 * math.sin((t - IN0) * 0.35), 420 + 120 * math.sin((t - IN0) * 0.7)

def inside_scene(c, t):
    g = cairo.LinearGradient(0, 0, 0, H)
    g.add_color_stop_rgb(0, *hexc('#2A1B3D')[:3]); g.add_color_stop_rgb(1, *hexc('#4E342E')[:3])
    c.set_source(g); c.paint()
    for (x, y, rx, ry, col) in ((200, 200, 320, 220, '#3E2A4F'), (900, 120, 420, 200, '#352545'), (1650, 220, 360, 260, '#3E2A4F'),
                                (400, 1000, 600, 220, '#5D4037'), (1500, 1020, 700, 240, '#5D4037')):
        ellipse(c, x, y, rx, ry); c.set_source_rgba(*hexc(col)); c.fill()
    for k in range(14):   # estalactitas
        x = 70 + k * 140; h = 60 + 70 * abs(math.sin(k * 1.7))
        c.move_to(x - 30, -5); c.line_to(x, h); c.line_to(x + 30, -5); c.close_path(); fill(c, hexc('#5D4037'), OUT, 4)
    c.rectangle(0, GROUND, W, H - GROUND); c.set_source_rgba(*hexc('#6D4C41')); c.fill()
    c.move_to(0, GROUND); c.line_to(W, GROUND); c.set_source_rgba(*OUT); c.set_line_width(6); c.stroke()
    for k, (x, y, col, s) in enumerate(CRYSTALS):
        crystal(c, x, y, col, s, crystal_light(k, t), t, k)
    # personajes entrando
    ent = lambda x: kf(t, [(IN0, x - 1100), (IN0 + 5.5, x)])
    wk = lambda sp: t * sp if t < IN0 + 5.5 else 0
    party = song(t)
    bob = lambda ph: -16 * abs(math.sin(t * 4 + ph)) if party else 0
    lk = (1, -0.6) if t > 61 else (1, -0.2)
    K.put(c, K.pipa, ent(330), GROUND + bob(0.5), 0.55, t=t, look=lk, walk=wk(7))
    K.put(c, K.tito, ent(560), GROUND + bob(1.0), 0.6, t=t, look=lk, walk=wk(6))
    K.put(c, K.tomi, ent(1070), GROUND + bob(1.5), 0.55, t=t, look=lk, walk=wk(4))
    cx = ent(820)
    ar, al = math.radians(65), math.radians(115)
    mood = 'o' if IN0 + 6 < t < 60.5 or 61 < t < 63 else 'smile'
    if party: ar, al = math.radians(-58 + 25 * math.sin(t * 9)), math.radians(-122 - 25 * math.sin(t * 9))
    K.put(c, K.coco, cx, GROUND + bob(0), 0.55, t=t, mood=mood, look=lk, arm_r=ar, arm_l=al, walk=wk(8))
    lx, ly = kf(t, [(IN0, -400), (IN0 + 5.5, 640)]), 430 + 18 * math.sin(t * 3)
    K.put(c, K.lola, lx, ly + bob(2.0), 0.5, t=t, flap=20, look=(1, 0.3))
    # oscuridad con luz alrededor de Luz y de los cristales encendidos
    zx, zy = luz_in(t)
    c.push_group()
    c.set_source_rgba(0.02, 0.01, 0.06, 0.6); c.paint()
    c.set_operator(cairo.OPERATOR_DEST_OUT)
    holes = [(zx, zy + 60, 680, 0.95)] + [(x, y - 60 * s, 380 * s, 0.85 * crystal_light(k, t)) for k, (x, y, col, s) in enumerate(CRYSTALS)]
    for (hx, hy, r, a) in holes:
        if a <= 0: continue
        gg = cairo.RadialGradient(hx, hy, 0, hx, hy, r)
        gg.add_color_stop_rgba(0, 0, 0, 0, a); gg.add_color_stop_rgba(1, 0, 0, 0, 0)
        c.set_source(gg); c.arc(hx, hy, r, 0, 2 * math.pi); c.fill()
    c.set_operator(cairo.OPERATOR_OVER)
    c.pop_group_to_source(); c.paint()
    luz(c, zx, zy, 0.55, t, 1.3)
    if party:
        for k in range(3):
            ph = (t * 0.7 + k / 3) % 1
            music_note(c, lx + 40 + 60 * ph, ly - 150 - 160 * ph, math.sin(math.pi * ph), ['#E91E63', '#1E88E5', '#FFD600'][k])
    if t > 72.0:
        for k in range(16):
            ph = ((t - 72.0) * 0.4 + k / 16) % 1
            x, y, col, s = CRYSTALS[k % len(CRYSTALS)]
            sparkle(c, x + 80 * math.sin(k + t), y - 150 - 300 * ph, 14 * math.sin(math.pi * ph), col)
    bubble(c, cx, GROUND - 300, '¡Qué oscuro!', (t - 56.0) / 2.6, 50)
    bubble(c, lx, ly - 170, '¡Cantemos!', (t - 58.6) / 2.2, 52)
    bubble(c, cx, GROUND - 300, '¡Se encienden!', (t - 62.5) / 3.0, 48)
    bubble(c, cx, GROUND - 300, '¡Qué lindo!', (t - 73.0) / 3.0, 52)

def frame(c, t):
    if outside(t): outside_scene(c, t)
    else: inside_scene(c, t)

def overlay(c, t):
    if t < 5.6:
        a = 1 - ss(4.8, 5.5, t)
        c.push_group(); word(c, 'La cueva del eco', W / 2, 230, 130 * K_back((t - 0.6) / 0.6) + 0.01,
                             colors=['#80D8FF', '#B388FF', '#FFD600'], tilt=0.05, outline=9)
        c.pop_group_to_source(); c.paint_with_alpha(a)
    if t > 95.0:
        s = K_back((t - 95.0) / 0.7)
        word(c, '¡Con amigos somos', W / 2, 160, 105 * s + 0.01, tilt=0.05, outline=10)
        word(c, 'más valientes!', W / 2, 285, 115 * s + 0.01, start=3, tilt=0.05, outline=10)
    for tc in (IN0, IN1):   # destello al entrar y salir
        if tc - 0.6 < t < tc + 0.6:
            c.set_source_rgba(1, 1, 1, 0.95 * (1 - abs(t - tc) / 0.6)); c.paint()
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
            c.save(); full(c, t); c.restore(); surf.write_to_png(f'ep23_{t}.png')
    else:
        t0, t1 = (float(args[1]), float(args[2])) if args and args[0] == 'range' else (0, DUR)
        out = sys.stdout.buffer
        for i in range(int(round(t0 * FPS)), int(round(t1 * FPS))):
            c.save(); full(c, i / FPS); c.restore(); surf.flush(); out.write(surf.get_data())
