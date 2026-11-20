"""Short — ¡Coco no se quiere lavar los dientes! (vertical, 41 s, plantilla nueva: gancho en el cuadro 1 + tarjeta final).
Es de noche y Coco no quiere lavarse los dientes. Mamá Coco le dice que los dientes quieren brillar como estrellas:
cepillado cantando (arriba, abajo y los costados), enjuague... ¡y una sonrisa que brilla! Ahora sí, a dormir.
Uso: python3 short_dientes.py [short a b] | stills 0 12 | portada"""
import cairo, math, sys
import cuerpos as K
from amigos import hexc, ellipse, fill, OUT
from logos import word, sparkle
from ep02_puente_del_rio import kf, ss, K_back, music_note
from ep03_donde_esta_tomi import bubble
from ep12_burbujas_magicas import soap_bubble
from ep14_bananas_papa import heart
from short_kit import SW, SH, FPS, END, top_title, end_card, logo_band

STORY = 38.0
DUR = STORY + END
FLOOR = 1500
TOP = 1330                       # mesada del lavatorio
COCO = (380, 1395)
S = 1.0
MAMA = [(0, 1350), (7.0, 1350), (8.6, 830)]
MOUTH = (COCO[0] + 18, COCO[1] - 262)

def room(c, t):
    c.set_source_rgba(*hexc('#E0F7FA')); c.paint()
    for y in range(0, FLOOR, 90):
        for x in range(0, SW, 90):
            c.rectangle(x + 3, y + 3, 84, 84); c.set_source_rgba(*hexc('#B2EBF2' if (x // 90 + y // 90) % 2 else '#C5F1F7')); c.fill()
    c.rectangle(640, 380, 360, 300); fill(c, hexc('#8D6E63'), OUT, 7)       # ventana de noche
    c.rectangle(658, 398, 324, 264)
    g = cairo.LinearGradient(0, 398, 0, 662); g.add_color_stop_rgb(0, *hexc('#141048')[:3]); g.add_color_stop_rgb(1, *hexc('#3949AB')[:3])
    c.set_source(g); c.fill()
    for k in range(9): sparkle(c, 680 + (k * 97) % 280, 420 + (k * 61) % 220, 7 + 4 * math.sin(t * 3 + k), '#FFF59D')
    ellipse(c, 920, 450, 36, 36); fill(c, hexc('#FFF59D'), hexc('#F9A825'), 5)
    c.move_to(820, 398); c.line_to(820, 662); c.set_source_rgba(*hexc('#8D6E63')); c.set_line_width(12); c.stroke()
    ellipse(c, 230, 720, 150, 190); fill(c, hexc('#CFD8DC'), OUT, 8)        # espejo
    ellipse(c, 230, 720, 125, 165); c.set_source_rgba(*hexc('#E1F5FE')); c.fill()
    for k in range(2):
        c.move_to(170 + 40 * k, 620); c.line_to(130 + 40 * k, 700); c.set_source_rgba(1, 1, 1, 0.9); c.set_line_width(12); c.stroke()
    c.rectangle(0, FLOOR, SW, SH - FLOOR); c.set_source_rgba(*hexc('#90A4AE')); c.fill()
    c.move_to(0, FLOOR); c.line_to(SW, FLOOR); c.set_source_rgba(*OUT); c.set_line_width(6); c.stroke()

def sink(c, t, rinse):
    c.rectangle(80, TOP, 600, 40); fill(c, hexc('#FFFFFF'), OUT, 6)
    c.rectangle(110, TOP + 40, 540, FLOOR - TOP - 30); fill(c, hexc('#F8BBD0'), OUT, 6)
    for x in (230, 530): ellipse(c, x, TOP + 140, 14, 14); fill(c, hexc('#FFFFFF'), OUT, 4)
    c.move_to(110, TOP + 100); c.line_to(650, TOP + 100); c.set_source_rgba(*OUT); c.set_line_width(5); c.stroke()
    ellipse(c, 380, TOP + 6, 150, 22); fill(c, hexc('#B0BEC5'), OUT, 5)
    c.move_to(560, TOP); c.line_to(560, TOP - 90); c.curve_to(560, TOP - 130, 500, TOP - 130, 495, TOP - 90)
    c.set_source_rgba(*OUT); c.set_line_width(24); c.stroke_preserve(); c.set_source_rgba(*hexc('#CFD8DC')); c.set_line_width(14); c.stroke()
    if rinse > 0:
        for k in range(4):
            c.move_to(495 + 3 * math.sin(t * 20 + k), TOP - 85); c.line_to(495 + 4 * math.sin(t * 17 + k), TOP)
        c.set_source_rgba(0.5, 0.8, 1, 0.8 * rinse); c.set_line_width(10); c.stroke()
    # vaso con cepillo y pasta
    c.rectangle(130, TOP - 90, 70, 90); fill(c, hexc('#81D4FA'), OUT, 5)
    c.rectangle(210, TOP - 30, 90, 30); fill(c, hexc('#FFFFFF'), OUT, 4)
    c.rectangle(210, TOP - 30, 34, 30); fill(c, hexc('#29B6F6'), OUT, 4)

def brush(c, x, y, ang, s=1.0):
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s)
    c.rectangle(0, -9, 150, 18); fill(c, hexc('#E53935'), OUT, 4)
    c.rectangle(-30, -16, 40, 16); fill(c, hexc('#FFFFFF'), OUT, 3)
    for k in range(4):
        c.move_to(-26 + 10 * k, -16); c.line_to(-26 + 10 * k, -30); c.set_source_rgba(*hexc('#29B6F6')); c.set_line_width(5); c.stroke()
    ellipse(c, -10, -34, 22, 10); fill(c, hexc('#FFFFFF'), OUT, 3)
    c.restore()

def aim(x, base, s, tx, ty, side=1):
    sx = x + 78 * side * s; sy = base - 180 * s
    dx, dy = tx - sx, ty - sy
    return math.atan2(dy, dx), max(90, math.hypot(dx, dy) / s)

PHASES = [(16.0, 20.5, 'Arriba…', -14), (20.5, 25.0, 'Abajo…', 14), (25.0, 29.5, '¡Y los costados!', 0)]

def frame(c, t):
    if t >= STORY:
        end_card(c, t - STORY); return
    room(c, t)
    x, base = COCO
    brushing = 16.0 < t < 29.5
    rinse = ss(29.8, 30.2, t) * (1 - ss(31.8, 32.2, t))
    mood, sad, look = 'smile', 0.0, (0.2, 0)
    ar, al, alen = math.radians(65 + 6 * math.sin(t * 2)), math.radians(115 - 6 * math.sin(t * 2)), 115
    if t < 9.0: mood, sad = 'sad', 1.0; ar, al = math.radians(150), math.radians(30); look = (-0.6, 0)
    if 9.0 < t < 16.0: mood = 'o'; look = (1, -0.2)
    bx = by = None
    if brushing:
        ph = next(p for p in PHASES if p[0] <= t < p[1])
        wig = 22 * math.sin(t * 16)
        bx, by = MOUTH[0] + (wig if ph[3] != 0 else 0), MOUTH[1] + ph[3] + (wig * 0.6 if ph[3] == 0 else 0)
        ar, alen = aim(x, base, S, bx + 90, by + 30)
        mood = 'smile'; look = (0.3, 0)
    if 29.8 < t < 32.0: mood = 'o'
    if t > 32.0: mood = 'smile'
    if t > 34.5: ar, al = math.radians(-58 + 25 * math.sin(t * 9)), math.radians(-122 - 25 * math.sin(t * 9))
    lid = ss(35.5, 37.5, t) * 0.5
    K.put(c, K.coco, x, base, S, t=t, mood=mood, sad=sad, look=look, arm_r=ar, arm_l=al, arm_len=alen, lid=lid)
    if brushing:
        brush(c, bx + 6, by + 22, 0.25)
        for k in range(8):   # espuma
            q = (t * 0.9 + k / 8) % 1
            soap_bubble(c, MOUTH[0] - 40 + 90 * math.sin(k * 2.1) * q + 20, MOUTH[1] + 20 - 170 * q, (10 + 6 * (k % 3)) * math.sin(math.pi * q), t + k, 1)
    sink(c, t, rinse)
    if not brushing and 9.0 < t < 16.0:   # Mamá trae el cepillo
        pass
    # Mamá
    mx = kf(t, MAMA)
    if t > 6.8:
        mar = math.radians(-35) if 9.0 < t < 15.5 else math.radians(60)
        if 16.0 < t < 29.5: mar = math.radians(-58 + 25 * math.sin(t * 6))
        if 34.0 < t < 36.5: mar = math.radians(-150)
        K.put(c, K.mama, mx, FLOOR + 10, 1.0, flip=True, t=t, look=(1, 0.3), arm_r=mar, arm_l=math.radians(115),
              walk=t * 7 if 6.8 < t < 8.6 else 0, mood='closed' if 34.0 < t < 37.0 else 'smile')
        if 9.0 < t < 15.5:   # cepillo en la mano de Mamá
            hx = mx - 78 - 115 * math.cos(mar) * 1.0; hy = FLOOR + 10 - 180 + 115 * math.sin(mar)
            brush(c, hx - 10, hy - 20, -0.6)
            sparkle(c, hx - 40, hy - 60, 18 * (0.6 + 0.4 * math.sin(t * 8)), '#FFFFFF')
    if brushing:
        for k in range(3):
            ph = (t * 0.7 + k / 3) % 1
            music_note(c, mx - 120 - 160 * ph, FLOOR - 560 - 220 * ph, math.sin(math.pi * ph), ['#F48FB1', '#29B6F6', '#FFD600'][k])
    if t > 31.8:   # sonrisa que brilla
        q = K_back((t - 31.8) / 0.4)
        for k, (dx, dy) in enumerate(((-30, 10), (40, 0), (5, 40))):
            sparkle(c, MOUTH[0] + dx, MOUTH[1] + dy, (26 + 10 * math.sin(t * 6 + k)) * q, '#FFFFFF')
        for k in range(10):
            ph = ((t - 31.8) * 0.6 + k / 10) % 1
            sparkle(c, 60 + (k * 113) % 960, 1250 - 700 * ph, 14 * math.sin(math.pi * ph), ('#FFD600', '#FFFFFF', '#80D8FF')[k % 3])
    if 34.2 < t < 37.5:
        q = ss(34.2, 37.5, t)
        heart(c, x + 90, base - 470 - 140 * q, 1.6, math.sin(math.pi * q))
    # globitos
    if t < 6.5:
        bubble(c, x + 150, base - 500, '¡NO ME QUIERO LAVAR!', min(0.84, 0.3 + t / 8) if t < 6.0 else 0.84 + (t - 6.0) / 0.5 * 0.16, 54)
    bubble(c, mx - 60, FLOOR - 520, 'Tus dientes quieren', (t - 9.0) / 4.0, 44)
    bubble(c, mx - 60, FLOOR - 440, 'brillar como estrellas', (t - 9.3) / 3.7, 44)
    bubble(c, x + 120, base - 500, '¿Brillar?', (t - 13.2) / 2.6, 56)
    for (a, b, txt, _) in PHASES:
        bubble(c, mx - 40, FLOOR - 560, txt, (t - a - 0.2) / (b - a - 0.3), 52)
    bubble(c, x + 150, base - 500, '¡Mirá cómo brillan!', (t - 32.0) / 2.8, 48)
    # títulos
    if t < 9.0: top_title(c, t, 0, '¡Coco no se quiere', 'lavar los dientes!', first=True, size=86)
    elif t < 16.0: top_title(c, t, 9.0, 'Mamá tiene', 'una idea…')
    elif t < 29.5: top_title(c, t, 16.0, '¡A cepillar', 'cantando!')
    elif t < 34.5: top_title(c, t, 29.5, '¡Dientes', 'brillantes!')
    else: top_title(c, t, 34.5, '¡Ahora sí,', 'a dormir!')
    logo_band(c)

if __name__ == '__main__':
    args = sys.argv[1:] or ['short']
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, SW, SH); c = cairo.Context(surf)
    if args[0] == 'stills':
        for t in map(float, args[1:]):
            c.save(); frame(c, t); c.restore(); surf.write_to_png(f'dientes_{t}.png')
    elif args[0] == 'portada':
        frame(c, 3.0); surf.write_to_png('short_dientes_portada.png')
    else:
        a0, a1 = (float(args[1]), float(args[2])) if len(args) > 2 else (0, DUR)
        out = sys.stdout.buffer
        for i in range(int(round(a0 * FPS)), int(round(a1 * FPS))):
            c.save(); frame(c, i / FPS); c.restore(); surf.flush(); out.write(surf.get_data())
