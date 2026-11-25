"""Short — ¡La travesura de Coco! (vertical, 40 s, plantilla nueva: gancho en el cuadro 1 + tarjeta final).
Tito duerme la siesta al lado de su canasta de bananas. Coco, de puntitas, se las lleva una por una y las esconde
detrás de un arbusto. Tito se despierta: "¿Y mis bananas?". Coco se ríe... y sale con una torta de bananas
de sorpresa: ¡era para el cumple de Tito! Abrazo y "¡Feliz cumple, Tito!".
Uso: python3 short_travesura.py [short a b] | stills 0 12 | portada"""
import cairo, math, sys
import cuerpos as K
from amigos import hexc, ellipse, fill, OUT
from logos import word, sparkle
from ep02_puente_del_rio import kf, ss, K_back, music_note
from ep03_donde_esta_tomi import bubble
from ep14_bananas_papa import heart
from short_kit import SW, SH, FPS, END, top_title, end_card, logo_band

STORY = 37.0
DUR = STORY + END
FLOOR = 1480
TITO = (320, FLOOR)
BASKET = (560, FLOOR - 10)
BUSH = (830, FLOOR - 40)
TRIPS = [(1.0, 3.6), (4.2, 6.8), (7.4, 10.0)]        # viajes de Coco: (sale, vuelve)

def bg(c, t):
    g = cairo.LinearGradient(0, 0, 0, SH)
    g.add_color_stop_rgb(0, *hexc('#4FC3F7')[:3]); g.add_color_stop_rgb(0.55, *hexc('#B3E5FC')[:3]); g.add_color_stop_rgb(0.56, *hexc('#8BC34A')[:3]); g.add_color_stop_rgb(1, *hexc('#689F38')[:3])
    c.set_source(g); c.paint()
    for (x0, y0, s) in ((150, 560, 1.0), (720, 480, 0.8)):
        c.save(); c.translate(x0 + 8 * t, y0); c.scale(s, s)
        for (cx, cy, r) in ((0, 0, 60), (70, -30, 75), (150, 0, 60), (75, 20, 60)): ellipse(c, cx, cy, r, r)
        c.set_source_rgba(1, 1, 1, 1); c.fill(); c.restore()
    for (x, y, r) in ((100, 1030, 260), (980, 1000, 300)):
        ellipse(c, x, y, r, r * 0.45); c.set_source_rgba(*hexc('#7CB342')); c.fill()
    # palmera de fondo
    c.move_to(120, FLOOR - 120); c.curve_to(130, 1100, 160, 900, 190, 800); c.set_source_rgba(*OUT); c.set_line_width(40); c.stroke_preserve()
    c.set_source_rgba(*hexc('#8D5524')); c.set_line_width(28); c.stroke()
    for a in (-160, -120, -80, -40, -5):
        c.save(); c.translate(190, 800); c.rotate(math.radians(a + 4 * math.sin(t)))
        c.move_to(0, 0); c.curve_to(70, -45, 180, -35, 250, 30); c.curve_to(170, 14, 70, 20, 0, 0); c.close_path()
        fill(c, hexc('#43A047'), hexc('#1B5E20'), 4); c.restore()

def basket(c, n_left, front):
    x, y = BASKET
    if not front:
        ellipse(c, x, y - 90, 110, 26); fill(c, hexc('#8D6E63'), OUT, 5)
        for k in range(n_left):
            K.banana(c, x - 50 + 45 * k, y - 105 - 10 * (k % 2), 1.9, -0.5 + 0.4 * k)
        return
    c.move_to(x - 110, y - 90); c.curve_to(x - 100, y, x + 100, y, x + 110, y - 90); c.close_path(); fill(c, hexc('#D7A86E'), OUT, 6)
    for k in range(4):
        c.move_to(x - 95 + 10 * k, y - 70 + 18 * k); c.line_to(x + 95 - 10 * k, y - 70 + 18 * k); c.set_source_rgba(*hexc('#A1887F')); c.set_line_width(5); c.stroke()

def bush(c, t):
    x, y = BUSH
    shake = 6 * math.sin(t * 25) if any(b - 0.6 < t < b + 0.2 for (_, b) in [(a, a + 1.3) for a, _ in TRIPS]) else 0
    for (dx, dy, r, col) in ((-90, 20, 95, '#388E3C'), (90, 20, 95, '#388E3C'), (0, -40, 115, '#43A047')):
        ellipse(c, x + dx + shake, y + dy, r, r * 0.85); fill(c, hexc(col), OUT, 6)

def cake(c, x, y, s):
    c.save(); c.translate(x, y); c.scale(s, s)
    ellipse(c, 0, 10, 150, 30); fill(c, hexc('#FFFFFF'), OUT, 5)
    c.rectangle(-120, -90, 240, 95); fill(c, hexc('#FFE082'), OUT, 6)
    c.move_to(-120, -90)
    for k in range(9): c.curve_to(-120 + 30 * k + 10, -60, -120 + 30 * k + 20, -60, -120 + 30 * (k + 1), -90)
    c.line_to(120, -110); c.line_to(-120, -110); c.close_path(); fill(c, hexc('#FFF8E1'), OUT, 5)
    for k in range(5): K.banana(c, -95 + 48 * k, -112, 1.3, -0.4 + 0.2 * k)
    for k, col in enumerate(('#E53935', '#1E88E5', '#43A047')):
        x0 = -50 + 50 * k
        c.rectangle(x0 - 7, -175, 14, 55); fill(c, hexc(col), OUT, 3)
        ellipse(c, x0, -186, 9, 14); c.set_source_rgba(1, 0.7 + 0.2 * math.sin(k + 9), 0.2, 1); c.fill()
    c.restore()

def tiptoe(t):
    """posición de Coco y si lleva banana."""
    home = 720
    for (a, b) in TRIPS:
        if a <= t < b:
            q = (t - a) / (b - a)
            if q < 0.4: return home + (BASKET[0] + 90 - home) * ss(0, 0.4, q), q > 0.3, -1
            if q < 0.5: return BASKET[0] + 90, True, -1
            return BASKET[0] + 90 + (BUSH[0] + 40 - BASKET[0] - 90) * ss(0.5, 1.0, q), True, 1
    if t < 10.0: return home if t < TRIPS[0][0] else BUSH[0] + 40, False, 1
    return kf(t, [(10.0, BUSH[0] + 40), (11.0, 720), (19.5, 720), (20.3, BUSH[0] + 60), (21.4, BUSH[0] + 60), (22.6, 620)]), False, 1

def frame(c, t):
    if t >= STORY:
        end_card(c, t - STORY); return
    bg(c, t)
    c.save(); c.translate(540, FLOOR + 20); c.scale(1.25, 1.25); c.translate(-540, -(FLOOR + 20))
    stolen = sum(1 for (a, b) in TRIPS if t > a + (b - a) * 0.45)
    left = 3 - stolen
    awake = t > 12.0
    party = t > 24.0
    # Tito
    tx, ty = TITO
    bob = -18 * abs(math.sin(t * 4.5)) if party else 0
    lid = 0.0 if awake else 1.0
    look = (1, 0.4) if 13.0 < t < 19.5 else (1, 0)
    mood_sad = 15.0 < t < 21.0
    K.put(c, K.tito, tx, ty + bob, 0.85, t=t, look=look, lid=lid, yawn=math.sin(math.pi * ss(12.0, 13.4, t)),
          reach=150 + 30 * math.sin(t * 6) if 26.0 < t < 30.0 else None)
    if not awake:
        for k in range(3):
            ph = (t * 0.45 + k / 3) % 1
            c.select_font_face('Fredoka Light', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
            c.set_font_size(50 + 30 * ph); c.set_source_rgba(1, 1, 1, math.sin(math.pi * ph))
            c.move_to(tx + 60 + 50 * ph, ty - 520 - 160 * ph); c.show_text('z'); c.new_path()
    basket(c, left, False); basket(c, left, True)
    # Coco
    cx, carry, d = tiptoe(t)
    flip = d < 0
    sneaking = t < 11.0
    mood = 'smile'
    ar, al = math.radians(65 + 6 * math.sin(t * 2)), math.radians(115 - 6 * math.sin(t * 2))
    hop = 0.0
    if sneaking:
        hop = -30 * abs(math.sin(t * 7))
        ar, al = math.radians(-100), math.radians(-80)     # dedo en la boca: shhh
        if carry: ar = math.radians(-35)
    if 13.0 < t < 19.5: mood = 'closed' if (t % 1.0) > 0.5 else 'smile'; ar, al = math.radians(-120), math.radians(-60)   # se tapa la risa
    if party: ar, al = math.radians(-58 + 25 * math.sin(t * 9)), math.radians(-122 - 25 * math.sin(t * 9))
    if 22.6 < t < 24.0 or 26.0 < t < 30.0: ar, al = math.radians(10), math.radians(170)
    if 26.0 < t < 30.0: mood = 'closed'
    show = cx < BUSH[0] - 10 or not (19.5 < t < 22.6 and 20.3 < t < 21.4)
    if not (20.4 < t < 21.3):
        K.put(c, K.coco, cx, FLOOR + hop + (bob if party else 0), 0.78, flip=flip, t=t, mood=mood, look=(1, 0), arm_r=ar, arm_l=al,
              walk=t * 7 if sneaking else 0, hold='banana' if carry and sneaking else None)
    if 22.0 < t < 26.0:   # trae la torta
        q = ss(21.4, 22.6, t)
        cake(c, cx + 150 if t < 24 else cx + 150, FLOOR - 140, 0.85 * q)
    elif t >= 26.0:
        cake(c, 520, FLOOR - 120, 0.85)
    bush(c, t)
    # efectos
    if sneaking:
        for k in range(2):
            ph = (t * 1.4 + k / 2) % 1
            c.select_font_face('Fredoka Light', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
            c.set_font_size(46); c.set_source_rgba(*hexc('#3B2314', math.sin(math.pi * ph)))
            c.move_to(cx - 40 + 30 * k, FLOOR - 470 - 60 * ph); c.show_text('…'); c.new_path()
    if party:
        for k in range(12):
            ph = ((t - 24.0) * 0.5 + k / 12) % 1
            x = 60 + (k * 89) % 960; y = 300 + 1100 * ph
            c.save(); c.translate(x + 20 * math.sin(t * 2 + k), y); c.rotate(t * 3 + k)
            c.rectangle(-12, -7, 24, 14); c.set_source_rgba(*hexc(('#E53935', '#FFD600', '#1E88E5', '#43A047')[k % 4])); c.fill(); c.restore()
        for k in range(3):
            ph = (t * 0.7 + k / 3) % 1
            music_note(c, 860 + 60 * ph, 1000 - 200 * ph, math.sin(math.pi * ph), ['#E91E63', '#1E88E5', '#FFD600'][k])
    if 26.0 < t < 31.0:
        for k in range(4):
            ph = ((t - 26.0) * 0.5 + k / 4) % 1
            heart(c, 300 + 160 * k, FLOOR - 650 - 220 * ph, 1.2, math.sin(math.pi * ph))
    # globitos
    if t < 1.0:
        bubble(c, cx + 60, FLOOR - 520, '¡Shhh!', 0.84 + t / 1.0 * 0.16, 70)
    bubble(c, cx + 60, FLOOR - 520, '¡Shhh!', (t - 1.0) / 9.5 if t > 1.0 else 0, 70)
    bubble(c, tx + 40, FLOOR - 690, '¿Y mis bananas?', (t - 14.0) / 4.4, 52)
    bubble(c, cx + 40, FLOOR - 520, '¡Jijiji!', (t - 16.0) / 2.6, 60)
    bubble(c, cx + 60, FLOOR - 520, '¡Sorpresa!', (t - 22.7) / 2.5, 60)
    bubble(c, tx + 40, FLOOR - 690, '¡Una torta de bananas!', (t - 24.4) / 2.0, 44)
    c.restore()
    # títulos
    if t < 11.0: top_title(c, t, 0, '¡La travesura', 'de Coco!', first=True)
    elif t < 22.0: top_title(c, t, 11.0, '¿Dónde están', 'las bananas?')
    elif t < 31.0: top_title(c, t, 22.0, '¡Era una', 'sorpresa!')
    else: top_title(c, t, 31.0, '¡Feliz cumple,', 'Tito!')
    logo_band(c)

if __name__ == '__main__':
    args = sys.argv[1:] or ['short']
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, SW, SH); c = cairo.Context(surf)
    if args[0] == 'stills':
        for t in map(float, args[1:]):
            c.save(); frame(c, t); c.restore(); surf.write_to_png(f'travesura_{t}.png')
    elif args[0] == 'portada':
        frame(c, 5.4); surf.write_to_png('short_travesura_portada.png')
    else:
        a0, a1 = (float(args[1]), float(args[2])) if len(args) > 2 else (0, DUR)
        out = sys.stdout.buffer
        for i in range(int(round(a0 * FPS)), int(round(a1 * FPS))):
            c.save(); frame(c, i / FPS); c.restore(); surf.flush(); out.write(surf.get_data())
