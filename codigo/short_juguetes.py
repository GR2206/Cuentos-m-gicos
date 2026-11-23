"""Short — ¡Coco no quiere guardar los juguetes! (vertical, 41 s, plantilla nueva: gancho en el cuadro 1 + tarjeta final).
El cuarto es un lío y Coco no quiere ordenar. Papá Coco lo convierte en un juego de básquet:
cada juguete que entra en la caja es un punto. ¡8 puntos y el cuarto queda ordenado!
Uso: python3 short_juguetes.py [short a b] | stills 0 12 | portada"""
import cairo, math, sys
import cuerpos as K
from amigos import hexc, ellipse, fill, OUT
from logos import word, sparkle
from ep02_puente_del_rio import kf, ss, K_back
from ep03_donde_esta_tomi import bubble
from ep17_carta import icon
from short_kit import SW, SH, FPS, END, top_title, end_card, logo_band

STORY = 38.0
DUR = STORY + END
FLOOR = 1450
BOX = (800, 1400)          # centro de la boca de la caja
COCO = (360, 1520)
PAPA = [(0, 1300), (7.0, 1300), (8.8, 890)]
# juguetes: (tipo, x, y en el piso, color, momento del tiro)
TOYS = [('pelota', 170, 1600, None, 12.5), ('bloque', 560, 1640, '#E53935', 14.6), ('tambor', 640, 1560, None, 16.7),
        ('bloque', 120, 1500, '#1E88E5', 18.8), ('libro', 300, 1650, None, 20.9), ('bloque', 470, 1520, '#FDD835', 23.0),
        ('barrilete', 690, 1600, None, 25.1), ('osito', 240, 1560, None, 27.2)]
FLY = 0.9

def block(c, x, y, s, col, letter):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.rectangle(-38, -38, 76, 76); fill(c, hexc(col), OUT, 5)
    c.select_font_face('Fredoka Light', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(52)
    e = c.text_extents(letter); c.move_to(-e.width / 2 - e.x_bearing, e.height / 2); c.set_source_rgba(1, 1, 1, 1); c.show_text(letter)
    c.restore()

def teddy(c, x, y, s):
    c.save(); c.translate(x, y); c.scale(s, s)
    for d in (-1, 1): ellipse(c, d * 30, -62, 16, 16); fill(c, hexc('#C68642'), OUT, 4)
    ellipse(c, 0, 10, 40, 36); fill(c, hexc('#C68642'), OUT, 5)
    ellipse(c, 0, -38, 34, 30); fill(c, hexc('#C68642'), OUT, 5)
    ellipse(c, 0, -28, 14, 10); fill(c, hexc('#FFE0B2'), OUT, 3)
    for d in (-1, 1): ellipse(c, d * 12, -44, 4, 5); c.set_source_rgba(*OUT); c.fill()
    c.restore()

def toy(c, k, x, y, s=1.0, rot=0.0):
    kind, _, _, col, _ = TOYS[k]
    c.save(); c.translate(x, y); c.rotate(rot)
    if kind == 'bloque': block(c, 0, 0, s, col, 'ABC'[k % 3])
    elif kind == 'osito': teddy(c, 0, 0, s)
    else: icon(c, kind, 0, 0, 0.9 * s)
    c.restore()

def toy_state(k, t):
    """posición del juguete: en el piso, volando a la caja o adentro (None)."""
    kind, x0, y0, col, t0 = TOYS[k]
    if t < t0: return x0, y0, 0.0
    if t < t0 + FLY:
        q = (t - t0) / FLY
        bx, by = BOX[0], BOX[1] - 30
        return x0 + (bx - x0) * q, y0 + (by - y0) * q - 520 * math.sin(math.pi * q), 6.0 * q
    return None

def score(t): return sum(1 for (*_, t0) in TOYS if t > t0 + FLY)

def room(c, t):
    c.set_source_rgba(*hexc('#E1F5FE')); c.paint()
    for k in range(0, SW, 120):
        c.rectangle(k, 0, 60, FLOOR); c.set_source_rgba(*hexc('#B3E5FC')); c.fill()
    c.rectangle(90, 420, 380, 330); fill(c, hexc('#8D6E63'), OUT, 7)        # ventana
    c.rectangle(108, 438, 344, 294); c.set_source_rgba(*hexc('#81D4FA')); c.fill()
    ellipse(c, 380, 520, 45, 45); fill(c, hexc('#FFEB3B'), hexc('#F9A825'), 5)
    for (x0, y0) in ((150, 640), (260, 610)):
        for (dx, dy, r) in ((0, 0, 30), (35, -15, 36), (70, 0, 30)): ellipse(c, x0 + dx, y0 + dy, r, r)
        c.set_source_rgba(1, 1, 1, 1); c.fill()
    c.move_to(280, 438); c.line_to(280, 732); c.move_to(108, 585); c.line_to(452, 585); c.set_source_rgba(*hexc('#8D6E63')); c.set_line_width(12); c.stroke()
    # cuadrito con estrellas
    c.rectangle(640, 470, 260, 200); fill(c, hexc('#FFF59D'), OUT, 7)
    for (sx, sy) in ((700, 540), (780, 600), (850, 520)): sparkle(c, sx, sy, 26, '#FF7043')
    c.rectangle(0, FLOOR, SW, SH - FLOOR); c.set_source_rgba(*hexc('#BCAAA4')); c.fill()
    c.move_to(0, FLOOR); c.line_to(SW, FLOOR); c.set_source_rgba(*OUT); c.set_line_width(6); c.stroke()
    c.save(); c.translate(430, 1600); c.scale(1, 0.32); ellipse(c, 0, 0, 380, 260); fill(c, hexc('#CE93D8'), OUT, 12); c.restore()   # alfombra

def toy_box(c, t, front):
    x, y = BOX
    if not front:
        ellipse(c, x, y, 140, 26); fill(c, hexc('#5D4037'), OUT, 5)
        return
    c.move_to(x - 140, y); c.line_to(x - 125, y + 190); c.line_to(x + 125, y + 190); c.line_to(x + 140, y); c.close_path()
    fill(c, hexc('#FF7043'), OUT, 6)
    c.rectangle(x - 140, y - 6, 280, 22); fill(c, hexc('#FFAB91'), OUT, 5)
    for k, col in enumerate(('#FFEB3B', '#29B6F6', '#66BB6A')):
        sparkle(c, x - 70 + 70 * k, y + 100, 24, col)
    n = score(t)
    if n > 0:   # juguetes que asoman
        for k in range(min(n, 5)):
            ellipse(c, x - 90 + 45 * k, y - 4, 22, 12); fill(c, hexc(('#E53935', '#1E88E5', '#FDD835', '#43A047', '#AB47BC')[k]), OUT, 3)

def frame(c, t):
    if t >= STORY:
        end_card(c, t - STORY); return
    room(c, t)
    toy_box(c, t, False)
    clean = t > 29.0
    # Papá (detrás de la caja)
    px = kf(t, PAPA)
    if t > 6.8:
        cheer = any(t0 + FLY < t < t0 + FLY + 0.8 for (*_, t0) in TOYS) or clean
        ar = math.radians(-58 + 25 * math.sin(t * 9)) if cheer else (math.radians(-40) if 9.0 < t < 12.0 else math.radians(60))
        al = math.radians(-122 - 25 * math.sin(t * 9)) if cheer else math.radians(115)
        if 30.5 < t < 32.0: ar = math.radians(-150)       # choca los cinco
        K.put(c, K.papa, px, FLOOR + 40, 0.95, flip=True, t=t, look=(1, 0.2), arm_r=ar, arm_l=al,
              walk=t * 7 if 6.8 < t < 8.8 else 0)
    toy_box(c, t, True)
    # juguetes en el piso
    for k in range(len(TOYS)):
        st = toy_state(k, t)
        if st and t < TOYS[k][4]: toy(c, k, st[0], st[1], 1.0, 0.2 * math.sin(k * 3))
    # Coco
    x, base = COCO
    mood, sad, look = 'smile', 0.0, (1, 0)
    ar, al = math.radians(65 + 6 * math.sin(t * 2)), math.radians(115 - 6 * math.sin(t * 2))
    if t < 9.0: mood, sad = 'sad', 1.0; ar, al = math.radians(150), math.radians(30)       # brazos cruzados
    if 9.0 < t < 12.0: mood = 'o'
    for (*_, t0) in TOYS:
        if t0 - 0.35 < t < t0 + 0.25:   # tira
            u = (t - t0 + 0.35) / 0.6
            ar = math.radians(110 - 220 * u); look = (1, -0.6)
    if clean: ar, al = math.radians(-58 + 25 * math.sin(t * 9)), math.radians(-122 - 25 * math.sin(t * 9))
    if 30.5 < t < 32.0: ar = math.radians(-30)
    hop = -40 * abs(math.sin(t * 5)) if t > 32.0 else 0
    K.put(c, K.coco, x, base + hop, 0.95, t=t, mood=mood, sad=sad, look=look, arm_r=ar, arm_l=al)
    # juguetes volando
    for k in range(len(TOYS)):
        st = toy_state(k, t)
        if st and t >= TOYS[k][4]: toy(c, k, st[0], st[1], 1.0, st[2])
    # +1 y marcador
    for (*_, t0) in TOYS:
        if t0 + FLY < t < t0 + FLY + 1.0:
            q = (t - t0 - FLY)
            word(c, '+1', BOX[0] - 190, BOX[1] - 140 - 120 * q, 80 * K_back(q / 0.3) + 0.01, colors=['#FFD600'], outline=8)
            for j in range(6):
                a = j * math.pi / 3; r = 50 + 120 * q
                sparkle(c, BOX[0] + r * math.cos(a), BOX[1] - 40 + r * math.sin(a), 16 * (1 - q), '#FFD600')
    if 12.0 < t < 30.5:
        n = score(t)
        c.save(); c.translate(790, 880)
        ellipse(c, 0, 0, 150, 80); fill(c, (1, 1, 1, 1), OUT, 6)
        c.restore()
        sparkle(c, 715, 880, 40, '#FFD600')
        word(c, f'{n}', 820, 905, 96, colors=['#FF7043'], outline=8)
    if clean:
        for k in range(12):
            ph = ((t - 29.0) * 0.6 + k / 12) % 1
            sparkle(c, 60 + (k * 89) % 960, 1550 - 900 * ph, 18 * math.sin(math.pi * ph), ('#FFD600', '#FF4081', '#29B6F6')[k % 3])
    # globitos
    if t < 6.5:
        bubble(c, x + 130, base - 470, '¡NO QUIERO GUARDAR!', min(0.84, 0.3 + t / 8) if t < 6.0 else 0.84 + (t - 6.0) / 0.5 * 0.16, 56)
    bubble(c, 620, FLOOR - 470, '¡Juguemos al básquet!', (t - 8.9) / 3.4, 46)
    bubble(c, x + 120, base - 470, '¡Sííí!', (t - 11.0) / 1.8, 60)
    bubble(c, 640, FLOOR - 620, '¡8 puntos!', (t - 28.5) / 2.6, 56)
    bubble(c, x + 140, base - 480, '¡Guardar es divertido!', (t - 33.2) / 4.6, 46)
    if t < 9.0: top_title(c, t, 0, '¡Coco no quiere', 'guardar los juguetes!', first=True, size=86)
    elif t < 12.0: top_title(c, t, 9.0, 'Papá tiene', 'un juego…')
    elif t < 29.0: top_title(c, t, 12.0, '¡A embocar', 'en la caja!')
    else: top_title(c, t, 29.0, '¡Cuarto', 'ordenado!')
    logo_band(c)

if __name__ == '__main__':
    args = sys.argv[1:] or ['short']
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, SW, SH); c = cairo.Context(surf)
    if args[0] == 'stills':
        for t in map(float, args[1:]):
            c.save(); frame(c, t); c.restore(); surf.write_to_png(f'juguetes_{t}.png')
    elif args[0] == 'portada':
        frame(c, 3.0); surf.write_to_png('short_juguetes_portada.png')
    else:
        a0, a1 = (float(args[1]), float(args[2])) if len(args) > 2 else (0, DUR)
        out = sys.stdout.buffer
        for i in range(int(round(a0 * FPS)), int(round(a1 * FPS))):
            c.save(); frame(c, i / FPS); c.restore(); surf.flush(); out.write(surf.get_data())
