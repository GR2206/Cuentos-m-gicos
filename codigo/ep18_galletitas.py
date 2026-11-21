"""Episodio 18 — Galletitas navideñas con Papá Coco (112 s). Receta real, paso a paso:
lavarse las manos; 250 g de manteca blanda, 200 g de azúcar impalpable, ralladura de 1 limón, 1 huevo,
400 g de harina 0000, 1 cdita de polvo de hornear y 1 pizca de sal; batir, formar la masa, estirarla,
enfriarla un ratito, cortar con moldes y al horno a 180 °C unos 12 minutos (¡siempre con un adulto!).
Después se decoran y se regalan.

Uso:  python3 ep18_galletitas.py              -> cuadros crudos por stdout
      python3 ep18_galletitas.py range 0 56   -> solo un tramo
      python3 ep18_galletitas.py stills 18 40 -> PNG sueltos
      python3 ep18_galletitas.py srt 5.5      -> subtítulos .srt de la narración"""
import cairo, math, sys
import cuerpos as K
from amigos import hexc, ellipse, fill, OUT
from logos import word, sparkle
from ep02_puente_del_rio import kf, ss, moving, K_back
from ep03_donde_esta_tomi import bubble
from ep09_semilla_magica import srt
from ep12_burbujas_magicas import soap_bubble
from ep14_bananas_papa import heart
from ep15_navidad import santa_hat
from ep16_chipa import kitchen_back, counter_front, mix, aim, item as item16, TOP_Y, SINK_X, OVEN

W, H, FPS = 1920, 1080, 30
DUR = 112.0
BOWL = (900, 690)
TRAY_X = 1110          # bandeja (centro) a la derecha de la tablita

NARRACION = [
    (6.0, 12.5, '¡Se viene Navidad! Coco y Papá Coco van a hacer galletitas.'),
    (14.5, 21.5, 'Primero, como siempre: ¡manos bien limpias con agua y jabón!'),
    (23.0, 33.0, 'Necesitamos manteca, azúcar impalpable, un limón, un huevo, harina, polvo de hornear y una pizca de sal.'),
    (35.0, 43.5, 'Batimos la manteca con el azúcar y la ralladura de limón, hasta que quede una crema.'),
    (45.0, 49.5, 'Sumamos el huevo.'),
    (51.0, 59.5, 'Y después la harina, el polvo de hornear y la sal, hasta formar una masa.'),
    (61.0, 69.5, 'Estiramos la masa con el palote, y la enfriamos un ratito.'),
    (71.0, 79.5, 'Con los moldes cortamos estrellas, arbolitos y corazones.'),
    (81.0, 91.5, 'Al horno, a ciento ochenta grados, unos doce minutos... ¡siempre con un adulto!'),
    (93.0, 99.5, 'Cuando se enfrían, ¡las decoramos de colores!'),
    (101.0, 106.0, 'Y las guardamos en una cajita... ¡para regalar a los amigos!'),
    (107.0, 111.0, '¡Feliz Navidad!'),
]
STEPS = [(14, 22, 'Paso 1: ¡a lavarse las manos!'), (22, 34, 'Los ingredientes'), (34, 44, 'Paso 2: manteca, azúcar y limón'),
         (44, 50, 'Paso 3: el huevo'), (50, 60, 'Paso 4: harina, polvo de hornear y sal'),
         (60, 70, 'Paso 5: estirar y enfriar'), (70, 80, 'Paso 6: ¡cortar con moldes!'),
         (80, 92, 'Paso 7: al horno, ¡con un adulto!'), (92, 100, 'Paso 8: ¡a decorar!')]
INGR = [('manteca', '250 g de manteca blanda', 23.0, 35.0), ('azucar', '200 g de azúcar impalpable', 24.4, 36.5),
        ('limon', 'ralladura de 1 limón', 25.8, 38.0), ('huevo', '1 huevo', 27.2, 45.0),
        ('harina', '400 g de harina 0000', 28.6, 51.0), ('polvo', '1 cdita de polvo de hornear', 30.0, 52.5),
        ('sal', '1 pizca de sal', 31.4, 54.0)]
SPOT = [1170, 1240, 1310, 1375, 1440, 1510, 1570]
SHAPES = ['estrella', 'arbolito', 'corazon', 'estrella', 'arbolito', 'corazon']
CUT_T = [71.0 + k * 1.4 for k in range(6)]
DECO_T = [93.0 + k * 1.0 for k in range(6)]
COOK_POS = [(TRAY_X - 100 + 100 * (k % 3), TOP_Y - 30 - 8 * (k // 3)) for k in range(6)]

# ---------------- ingredientes ----------------
def item(c, kind, x, y, s=1.0, tilt=0.0):
    if kind in ('sal',): return item16(c, kind, x, y, s, tilt)
    c.save(); c.translate(x, y); c.rotate(tilt); c.scale(s, s)
    if kind in ('harina', 'azucar'):
        col = '#FFFFFF' if kind == 'harina' else '#FCE4EC'
        c.move_to(-34, 0); c.line_to(-30, -80); c.line_to(30, -80); c.line_to(34, 0); c.close_path(); fill(c, hexc(col), OUT, 4)
        c.move_to(-30, -80); c.line_to(-20, -96); c.line_to(20, -96); c.line_to(30, -80); fill(c, hexc('#E3F2FD'), OUT, 4)
        ellipse(c, 0, -42, 18, 18); fill(c, hexc('#FFB300' if kind == 'harina' else '#EC407A'), OUT, 3)
    elif kind == 'manteca':
        c.rectangle(-36, -34, 72, 34); fill(c, hexc('#FFF59D'), OUT, 4)
        c.rectangle(-36, -34, 30, 34); fill(c, hexc('#90CAF9'), OUT, 4)
    elif kind == 'limon':
        ellipse(c, 0, -26, 32, 24); fill(c, hexc('#FFEB3B'), OUT, 4)
        ellipse(c, 30, -30, 6, 5); fill(c, hexc('#FFEB3B'), OUT, 3)
        c.move_to(-6, -48); c.curve_to(4, -66, 22, -62, 24, -52); c.curve_to(10, -50, 2, -48, -6, -48); fill(c, hexc('#66BB6A'), OUT, 3)
    elif kind == 'huevo':
        ellipse(c, 0, -26, 18, 25); fill(c, hexc('#FFF8E1'), OUT, 4)
    elif kind == 'polvo':
        c.rectangle(-20, -56, 40, 56); fill(c, hexc('#E53935'), OUT, 4)
        ellipse(c, 0, -56, 20, 6); fill(c, hexc('#FFCDD2'), OUT, 3)
        ellipse(c, 0, -28, 11, 11); fill(c, (1, 1, 1, 1), OUT, 3)
    c.restore()

def fly(t, k):
    kind, _, t_in, t_bowl = INGR[k]
    if t < t_in: return None
    x0, y0 = SPOT[k], TOP_Y
    if t < t_bowl: return x0, y0, K_back((t - t_in) / 0.4), 0.0
    if t < t_bowl + 1.0:
        q = ss(t_bowl, t_bowl + 1.0, t)
        return x0 + (BOWL[0] + 40 - x0) * q, y0 + (BOWL[1] - 100 - y0) * q - 160 * math.sin(math.pi * q), 1.0, -1.9 * q
    return None

# ---------------- masa, moldes y galletitas ----------------
def shape_path(c, shape, r):
    if shape == 'estrella':
        for i in range(10):
            rr = r if i % 2 == 0 else r * 0.48; a = -math.pi / 2 + i * math.pi / 5
            (c.move_to if i == 0 else c.line_to)(rr * math.cos(a), rr * math.sin(a))
        c.close_path()
    elif shape == 'arbolito':
        c.move_to(0, -r); c.line_to(r * 0.55, -r * 0.2); c.line_to(r * 0.3, -r * 0.2); c.line_to(r * 0.8, r * 0.55)
        c.line_to(r * 0.15, r * 0.55); c.line_to(r * 0.15, r); c.line_to(-r * 0.15, r); c.line_to(-r * 0.15, r * 0.55)
        c.line_to(-r * 0.8, r * 0.55); c.line_to(-r * 0.3, -r * 0.2); c.line_to(-r * 0.55, -r * 0.2); c.close_path()
    else:
        c.move_to(0, r * 0.85); c.curve_to(-r * 1.25, -r * 0.1, -r * 0.6, -r * 1.05, 0, -r * 0.45)
        c.curve_to(r * 0.6, -r * 1.05, r * 1.25, -r * 0.1, 0, r * 0.85); c.close_path()

DECO_COL = {'estrella': '#FFD600', 'arbolito': '#43A047', 'corazon': '#FF4081'}
def cookie(c, shape, x, y, s, golden, deco):
    c.save(); c.translate(x, y); c.scale(s, s)
    shape_path(c, shape, 36); fill(c, mix('#FFF3C4', '#E9B45A', golden), OUT, 4)
    if deco > 0:
        c.save(); c.scale(0.72, 0.72); shape_path(c, shape, 36); c.restore()
        c.set_source_rgba(*hexc(DECO_COL[shape], deco)); c.fill()
        for k in range(4):
            a = k * 1.7
            ellipse(c, 12 * math.cos(a), 12 * math.sin(a), 3.5, 3.5)
            c.set_source_rgba(*hexc(('#FFFFFF', '#E53935', '#29B6F6', '#FFFFFF')[k], deco)); c.fill()
    c.restore()

def bowl(c, t):
    if t > 60.2: return
    x, y = BOWL
    a = 1 - ss(59.8, 60.2, t)
    n = sum(1 for (_, _, _, tb) in INGR if t > tb + 0.9)
    c.push_group()
    ellipse(c, x, y - 70, 120, 26); fill(c, hexc('#EF5350'), OUT, 5)
    if n > 0:
        ellipse(c, x, y - 66 + 3 * (7 - n), 104, 20); fill(c, mix('#FFF59D', '#FFF3E0', min(1, n / 7)), None, 0)
    if t > 56.5:
        ellipse(c, x, y - 82, 70, 34 * ss(56.5, 58.0, t) + 1); fill(c, hexc('#FFF3C4'), OUT, 4)
    if 39.5 < t < 44.0 or 46.5 < t < 50.0 or 55.0 < t < 59.5:   # batidor que gira
        a2 = t * 7
        sx, sy = x + 45 * math.cos(a2), y - 70 + 10 * math.sin(a2)
        c.move_to(sx, sy); c.line_to(sx - 40, sy - 110); c.set_source_rgba(*OUT); c.set_line_width(14); c.stroke()
        c.move_to(sx, sy); c.line_to(sx - 40, sy - 110); c.set_source_rgba(*hexc('#BCAAA4'), ); c.set_line_width(8); c.stroke()
        for d in (-1, 1):
            c.save(); c.translate(sx, sy - 5); c.scale(1, 1.4); c.arc(0, 0, 18 + 6 * d, math.pi, 2 * math.pi); c.restore()
            c.set_source_rgba(*hexc('#90A4AE')); c.set_line_width(4); c.stroke()
    c.move_to(x - 120, y - 70); c.curve_to(x - 115, y + 5, x + 115, y + 5, x + 120, y - 70); c.close_path(); fill(c, hexc('#E53935'), OUT, 5)
    c.pop_group_to_source(); c.paint_with_alpha(a)

def whisk_tip(t):
    a2 = t * 7
    return BOWL[0] + 45 * math.cos(a2) - 40, BOWL[1] - 180 + 10 * math.sin(a2)

def dough(c, t):
    if not 59.8 < t < 80.5: return
    x, y = BOWL
    c.rectangle(x - 190, y - 18, 380, 18); fill(c, hexc('#D7A86E'), OUT, 4)    # tablita
    flat = ss(61.0, 66.0, t)
    left = 1 - sum(1 for tc in CUT_T if t > tc) / 7
    w = (70 + 100 * flat) * K_back((t - 59.8) / 0.4); h = 55 - 40 * flat
    c.rectangle(x - w, y - 18 - h, 2 * w, h)
    fill(c, hexc('#FFF3C4'), OUT, 5)
    for k, tc in enumerate(CUT_T):   # huecos de los moldes
        if t > tc + 0.5:
            c.save(); c.translate(x - 110 + 44 * k, y - 18 - h / 2); c.scale(0.45, 0.25 + 0.0 * left); shape_path(c, SHAPES[k], 36); c.restore()
            c.set_source_rgba(*hexc('#D7A86E')); c.fill()
    if 61.0 < t < 66.2:   # palote
        px = x - 120 + 240 * (0.5 + 0.5 * math.sin((t - 61.0) * 2.4))
        c.rectangle(px - 25, y - 18 - h - 46, 50, 46); fill(c, hexc('#BCAAA4'), OUT, 5)
        for d in (-1, 1):
            c.rectangle(px - 9 + d * 0, y - 18 - h - 46 - 0, 18, 0)
        c.save(); c.translate(px, y - 18 - h - 23)
        c.rectangle(-110, -14, 220, 28); fill(c, hexc('#D7A86E'), OUT, 5)
        for d in (-1, 1):
            c.rectangle(d * 110 - (30 if d < 0 else 0), -8, 30, 16); fill(c, hexc('#8D6E63'), OUT, 4)
        c.restore()
    if 66.2 < t < 70.0:   # a enfriar un ratito
        a = ss(66.2, 66.6, t) * (1 - ss(69.6, 70.0, t))
        for k in range(7):
            ph = (t * 0.5 + k / 7) % 1
            sparkle(c, x - 150 + 50 * k, y - 60 - 120 * ph, 14 * a * math.sin(math.pi * ph), '#81D4FA')
        cx, cy = x + 220, y - 120
        ellipse(c, cx, cy, 38 * a + 0.1, 38 * a + 0.1); fill(c, (1, 1, 1, 1), OUT, 5)
        an = -math.pi / 2 + (t - 66.2) / 3.4 * 2 * math.pi
        c.move_to(cx, cy); c.line_to(cx + 28 * a * math.cos(an), cy + 28 * a * math.sin(an))
        c.set_source_rgba(*hexc('#1E88E5')); c.set_line_width(5); c.stroke()

def cutter(c, t):
    for k, tc in enumerate(CUT_T):
        if tc - 0.5 < t < tc + 0.7:
            x = BOWL[0] - 110 + 44 * k
            down = math.sin(math.pi * ss(tc - 0.5, tc + 0.7, t))
            y = BOWL[1] - 60 - 70 * (1 - down)
            c.save(); c.translate(x, y); c.scale(0.6, 0.6); shape_path(c, SHAPES[k], 36); c.restore()
            c.set_source_rgba(*hexc('#B0BEC5')); c.set_line_width(7); c.stroke_preserve()
            c.set_source_rgba(*OUT); c.set_line_width(2); c.stroke()
            return x, y
    return None

def tray_offset(t):
    if t < 80.3 or t > 91.8: return 0, 0
    if t < 82.8:
        q = ss(80.3, 82.8, t); return (1720 - TRAY_X) * q, 60 * q - 140 * math.sin(math.pi * q)
    if t < 89.3: return None
    q = ss(89.3, 91.8, t); return (1720 - TRAY_X) * (1 - q), 60 * (1 - q) - 140 * math.sin(math.pi * q)

def tray(c, t):
    if t < 70.5 or t > 104.0: return
    off = tray_offset(t)
    if off is None: return
    ox, oy = off; golden = ss(84.0, 88.5, t)
    c.save(); c.translate(ox, oy)
    c.rectangle(TRAY_X - 160, TOP_Y - 12, 320, 14); fill(c, hexc('#90A4AE'), OUT, 4)
    for k, (bx, by) in enumerate(COOK_POS):
        if t < CUT_T[k] + 0.7: continue
        if t > 101.0 + 0.35 * k: continue   # se guardan en la cajita
        cookie(c, SHAPES[k], bx, by, 1.15 * K_back((t - CUT_T[k] - 0.7) / 0.3), golden, ss(DECO_T[k], DECO_T[k] + 0.5, t))
    c.restore()
    if 89.3 < t < 95:
        for k in range(3):
            ph = (t * 0.6 + k / 3) % 1
            x = TRAY_X - 80 + 80 * k + ox + 20 * math.sin(t * 3 + k)
            c.move_to(x, TOP_Y - 70 - 80 * ph); c.curve_to(x + 20, TOP_Y - 90 - 80 * ph, x - 20, TOP_Y - 120 - 80 * ph, x, TOP_Y - 140 - 80 * ph)
            c.set_source_rgba(1, 1, 1, 0.8 * math.sin(math.pi * ph)); c.set_line_width(8); c.stroke()

def icing(c, t):
    for k, td in enumerate(DECO_T):
        if td - 0.6 < t < td + 0.5:
            bx, by = COOK_POS[k]
            x, y = bx + 10, by - 70 + 20 * math.sin(t * 8)
            c.save(); c.translate(x, y); c.rotate(0.5)
            c.move_to(-12, 30); c.line_to(-24, -40); c.line_to(24, -40); c.line_to(12, 30); c.close_path()
            fill(c, hexc(DECO_COL[SHAPES[k]]), OUT, 4)
            c.restore()
            return x, y
    return None

def gift_box(c, t):
    if t < 100.5: return
    x, y = 640, TOP_Y
    s = K_back((t - 100.5) / 0.5)
    c.save(); c.translate(x, y); c.scale(s, s)
    c.rectangle(-80, -90, 160, 90); fill(c, hexc('#43A047'), OUT, 5)
    c.rectangle(-14, -90, 28, 90); fill(c, hexc('#E53935'), OUT, 3)
    closed = ss(103.6, 104.2, t)
    if closed > 0:
        c.save(); c.translate(0, -110 * (1 - closed))
        c.rectangle(-88, -108, 176, 24); fill(c, hexc('#66BB6A'), OUT, 5)
        for sx in (-1, 1):
            ellipse(c, sx * 26, -118, 26, 16); fill(c, hexc('#E53935'), OUT, 4)
        c.restore()
    c.restore()
    for k in range(6):   # galletitas volando a la caja
        t0 = 101.0 + 0.35 * k
        if t0 < t < t0 + 0.6:
            q = (t - t0) / 0.6; bx, by = COOK_POS[k]
            cookie(c, SHAPES[k], bx + (x - bx) * q, by + (y - 60 - by) * q - 120 * math.sin(math.pi * q), 0.85, 1, 1)

def oven(c, t):
    x0, x1 = OVEN
    c.rectangle(x0, 450, x1 - x0, 560); fill(c, hexc('#ECEFF1'), OUT, 7)
    c.rectangle(x0, 450, x1 - x0, 90); fill(c, hexc('#B0BEC5'), OUT, 6)
    on = ss(82.0, 82.6, t) * (1 - ss(91.0, 92.0, t))
    for k in range(3):
        ellipse(c, x0 + 50 + 70 * k, 495, 22, 22); fill(c, hexc('#FFFFFF'), OUT, 4)
        a = -math.pi / 2 + (1.6 * on if k == 1 else 0)
        c.move_to(x0 + 50 + 70 * k, 495); c.line_to(x0 + 50 + 70 * k + 16 * math.cos(a), 495 + 16 * math.sin(a))
        c.set_source_rgba(*OUT); c.set_line_width(4); c.stroke()
    c.rectangle(x0 + 30, 590, x1 - x0 - 60, 300); fill(c, hexc('#CFD8DC'), OUT, 6)
    c.rectangle(x0 + 55, 615, x1 - x0 - 110, 200); fill(c, hexc('#37474F'), OUT, 5)
    if on > 0:
        c.rectangle(x0 + 55, 615, x1 - x0 - 110, 200)
        c.set_source_rgba(1, 0.6, 0.15, 0.55 * on * (0.85 + 0.15 * math.sin(t * 6))); c.fill()
    if 83.0 < t < 89.3:
        c.rectangle(x0 + 75, 760, x1 - x0 - 150, 14); fill(c, hexc('#90A4AE'), OUT, 3)
        q = ss(84.0, 88.5, t)
        for k in range(3): cookie(c, SHAPES[k], x0 + 105 + 60 * k, 735, 0.5, q, 0)
    c.rectangle(x0 + 70, 590 - 22, x1 - x0 - 140, 16); fill(c, hexc('#90A4AE'), OUT, 4)
    c.rectangle(x0, 1010, x1 - x0, 70); c.set_source_rgba(*hexc('#B0BEC5')); c.fill()
    if on > 0:
        word(c, '180°', (x0 + x1) / 2, 410, 64 * K_back((t - 82.0) / 0.4) + 0.01, colors=['#FF5722'], outline=6)
    if 84.0 < t < 89.0:
        cx, cy = (x0 + x1) / 2, 950
        ellipse(c, cx, cy, 40, 40); fill(c, (1, 1, 1, 1), OUT, 5)
        a = -math.pi / 2 + (t - 84) / 5 * 2 * math.pi
        c.move_to(cx, cy); c.line_to(cx + 30 * math.cos(a), cy + 30 * math.sin(a)); c.set_source_rgba(*hexc('#E53935')); c.set_line_width(5); c.stroke()
        c.select_font_face('Fredoka Light', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(30)
        c.set_source_rgba(*OUT); c.move_to(cx + 52, cy + 10); c.show_text('12 min')

def board_text(c, t):
    if t < 22.5: return
    c.select_font_face('Fredoka Light', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    c.set_font_size(42); c.set_source_rgba(1, 0.95, 0.6, 1); c.move_to(120, 150); c.show_text('Galletitas')
    c.set_font_size(25)
    for k, (kind, txt, t_in, t_bowl) in enumerate(INGR):
        if t < t_in: continue
        a = ss(t_in, t_in + 0.4, t); y = 200 + 46 * k
        c.set_source_rgba(1, 1, 1, a); c.move_to(160, y); c.show_text(txt)
        item(c, kind, 128, y + 6, 0.3)
        done = t_bowl + 1.0
        if t > done:
            q = ss(done, done + 0.3, t)
            c.move_to(98, y - 8); c.line_to(108, y + 2); c.line_to(98 + 32 * q, y - 22 * q)
            c.set_source_rgba(*hexc('#76FF03')); c.set_line_width(6); c.stroke()

# ---------------- personajes ----------------
COCO_X = [(0, 720), (13.5, 720), (14.5, SINK_X + 140), (21.5, SINK_X + 140), (22.5, 720), (99.0, 720), (100.5, 800)]
PAPA_X = [(0, 1300), (13.5, 1300), (14.5, SINK_X + 330), (21.5, SINK_X + 330), (22.5, 1300), (80.0, 1300), (82.8, 1500),
          (89.5, 1500), (91.8, 1300)]
MAMA_X = [(0, -300), (99.0, -300), (101.0, 570)]

def draw_chars(c, t):
    s_c, base_c = 0.75, 830
    s_p, base_p = 0.92, 880
    hats = 1.0
    # Mamá
    if t > 99.0:
        mx = kf(t, MAMA_X)
        K.put(c, K.mama, mx, base_p, 0.92, t=t, look=(1, 0.3), walk=t * 7 if moving(t, MAMA_X) else 0,
              mood='closed' if 104.5 < t < 107 else 'smile', arm_r=math.radians(-55 + 20 * math.sin(t * 6)) if t > 106.5 else math.radians(60), arm_l=math.radians(115))
        santa_hat(c, mx - 10, base_p - 0.92 * 455, 1.1, 0.1)
    # Papá
    px = kf(t, PAPA_X)
    p_r, p_l, p_len, look_p = math.radians(65), math.radians(115), 115, (-1, 0.3)
    if 15.0 < t < 21.0:
        p_r, p_len = aim(px, base_p, s_p, SINK_X + 40 + 20 * math.sin(t * 9), TOP_Y - 30, True); p_l = p_r + 0.25
    if 34.5 < t < 39.0 or 50.5 < t < 55.0: p_r = math.radians(-10 + 25 * math.sin(t * 2))
    if 61.0 < t < 66.2:   # estira con el palote
        x = BOWL[0] - 120 + 240 * (0.5 + 0.5 * math.sin((t - 61.0) * 2.4))
        p_r, p_len = aim(px, base_p, s_p, x + 60, TOP_Y - 70, True); p_l = p_r + 0.2
    if 80.3 < t < 83.0 or 89.3 < t < 91.8: p_r = p_l = math.radians(10); look_p = (1, 0.3)
    if 83.0 <= t <= 89.3: look_p = (1, 0.4); p_r = math.radians(-20) if t < 84 or t > 88.6 else math.radians(65)
    flip_p = not (80.3 < t < 91.8 and look_p[0] > 0)
    K.put(c, K.papa, px, base_p, s_p, flip=flip_p, t=t, look=(1, look_p[1]), arm_r=p_r, arm_l=p_l, arm_len=p_len,
          walk=t * 7 if moving(t, PAPA_X) else 0, mood='closed' if 104.5 < t < 107 else 'smile')
    santa_hat(c, px + (10 if flip_p else -10), base_p - s_p * 455, 1.1, -0.1 if flip_p else 0.1)
    if 80.3 < t < 91.8 and not (83.0 <= t <= 89.3) or 83.0 < t < 84.0 or 88.6 < t < 89.3:   # guantes de cocina
        for d in (-1, 1):
            ellipse(c, px + d * 70 + (60 if not flip_p else -60), base_p - 170, 26, 22); fill(c, hexc('#E53935'), OUT, 4)
    # Coco
    cx = kf(t, COCO_X)
    mood, look = 'smile', (1, 0.4)
    ar, al, alen = math.radians(65 + 6 * math.sin(t * 2)), math.radians(115 - 6 * math.sin(t * 2)), 115
    if 8.5 < t < 11: ar, al = math.radians(-60), math.radians(-120); mood = 'o'
    if 15.0 < t < 21.0:
        ar, alen = aim(cx, base_c, s_c, SINK_X + 10 + 20 * math.sin(t * 9 + 1), TOP_Y - 30, False, 1)
        al, _ = aim(cx, base_c, s_c, SINK_X + 10 + 20 * math.sin(t * 9 + 1), TOP_Y - 30, False, -1)
    if 39.5 < t < 44.0 or 46.5 < t < 50.0 or 55.0 < t < 59.5:
        ar, alen = aim(cx, base_c, s_c, *whisk_tip(t)); al = ar + 0.3
        mood = 'closed' if (t % 2) > 1.4 else 'smile'
    cp = cutter(c, t) if False else None
    for k, tc in enumerate(CUT_T):
        if tc - 0.5 < t < tc + 0.7:
            x = BOWL[0] - 110 + 44 * k; down = math.sin(math.pi * ss(tc - 0.5, tc + 0.7, t))
            ar, alen = aim(cx, base_c, s_c, x, BOWL[1] - 90 - 70 * (1 - down)); al = ar + 0.25
    for k, td in enumerate(DECO_T):
        if td - 0.6 < t < td + 0.5:
            bx, by = COOK_POS[k]
            ar, alen = aim(cx, base_c, s_c, bx + 10, by - 100 + 20 * math.sin(t * 8)); al = ar + 0.25
    if 80.3 < t < 92.0: look = (1, 0.1)
    if 83.0 < t < 89.0: mood = 'o' if t < 85 else 'smile'
    if 96.5 < t < 99.0: mood = 'chew' if (t % 1.1) > 0.5 else 'smile'
    if t > 106.5: ar, al = math.radians(-58 + 25 * math.sin(t * 9)), math.radians(-122 - 25 * math.sin(t * 9))
    hop = -25 * abs(math.sin(t * 6)) if 8.5 < t < 11 or t > 106.5 else 0
    K.put(c, K.coco, cx, base_c + hop, s_c, t=t, mood=mood, look=look, arm_r=ar, arm_l=al, arm_len=alen, chew=t)
    santa_hat(c, cx, base_c + hop - s_c * 455, 0.9 * hats, -0.15)

def washing(c, t):
    if not 14.8 < t < 21.5: return
    a = ss(14.8, 15.3, t) * (1 - ss(21.0, 21.5, t))
    for k in range(5):
        c.move_to(SINK_X + 30 + 3 * math.sin(t * 20 + k), TOP_Y - 120); c.line_to(SINK_X + 30 + 4 * math.sin(t * 17 + k), TOP_Y - 10)
    c.set_source_rgba(0.5, 0.8, 1, 0.7 * a); c.set_line_width(12); c.stroke()
    for k in range(12):
        ph = (t * 0.5 + k / 12) % 1
        x = SINK_X - 120 + (k * 53) % 300 + 30 * math.sin(t + k)
        soap_bubble(c, x, TOP_Y - 30 - 260 * ph, (16 + 10 * (k % 3)) * math.sin(math.pi * ph) * a, t + k, a)

def world(c, t):
    kitchen_back(c)
    board_text(c, t)
    oven(c, t)
    draw_chars(c, t)
    counter_front(c, t)
    washing(c, t)
    for k in range(len(INGR)):
        p = fly(t, k)
        if p: item(c, INGR[k][0], p[0], p[1], 1.0 * p[2] + 0.001, p[3])
    bowl(c, t)
    for k in range(len(INGR)):   # nubecita de harina al caer
        tb = INGR[k][3]
        if tb + 0.9 < t < tb + 1.6:
            q = (t - tb - 0.9) / 0.7
            for j in range(6):
                ellipse(c, BOWL[0] + 90 * math.cos(j) * q, BOWL[1] - 90 - 50 * q * abs(math.sin(j * 2)), 18 * (1 - q), 18 * (1 - q))
                c.set_source_rgba(1, 1, 1, 0.8 * (1 - q)); c.fill()
    dough(c, t)
    cutter(c, t)
    tray(c, t)
    icing(c, t)
    gift_box(c, t)
    if t > 106.5:
        for k in range(10):
            ph = (t * 0.6 + k / 10) % 1
            heart(c, 300 + 150 * k, TOP_Y - 450 - 200 * ph, 0.9, math.sin(math.pi * ph))
    px = kf(t, PAPA_X); cx = kf(t, COCO_X)
    bubble(c, px, 380, '¿Hacemos galletitas?', (t - 5.8) / 3.0, 48)
    bubble(c, cx, 480, '¡Sííí!', (t - 8.6) / 2.6, 60)
    bubble(c, cx, 480, '¡Con jabón!', (t - 16.0) / 3.5, 50)
    bubble(c, cx, 480, '¡Una estrella!', (t - 71.3) / 2.6, 50)
    bubble(c, cx, 480, '¡Con un adulto!', (t - 81.0) / 3.4, 50)
    bubble(c, 1500, 380, '¡Doraditas!', (t - 89.4) / 2.6, 50)
    bubble(c, cx, 480, '¡Para los amigos!', (t - 101.2) / 3.2, 48)
    bubble(c, kf(t, MAMA_X), 400, '¡Qué lindas!', (t - 101.5) / 2.8, 48)

def overlay(c, t):
    if t < 5.6:
        a = 1 - ss(4.8, 5.5, t)
        c.push_group()
        c.set_source_rgba(1, 1, 1, 0.55); c.paint()
        word(c, 'Galletitas navideñas', W / 2, 400, 120 * K_back((t - 0.6) / 0.6) + 0.01, colors=['#E53935', '#43A047', '#FFD600'], tilt=0.05, outline=10)
        word(c, 'con Papá Coco', W / 2, 560, 120 * K_back((t - 1.0) / 0.6) + 0.01, start=3, tilt=0.05, outline=10)
        c.pop_group_to_source(); c.paint_with_alpha(a)
    for (a1, b1, txt) in STEPS:
        if a1 <= t < b1:
            s = K_back((t - a1) / 0.4) * (1 - ss(b1 - 0.3, b1, t))
            word(c, txt, 1230, 115, 62 * s + 0.01, tilt=0.03, outline=8)
    if t > 106.5:
        s = K_back((t - 106.5) / 0.6)
        word(c, '¡Feliz Navidad!', 1230, 140, 110 * s + 0.01, colors=['#E53935', '#43A047', '#FFD600'], tilt=0.05, outline=10)
    a = max(1 - ss(0, 0.8, t), ss(DUR - 2.0, DUR, t))
    if a > 0: c.set_source_rgba(1, 1, 1, a); c.paint()

CAM = [(0, 1.0, 960, 540), (34.0, 1.0, 960, 540), (35.0, 1.12, 960, 580), (79.5, 1.12, 960, 580), (80.5, 1.0, 960, 540),
       (92.0, 1.0, 960, 540), (93.0, 1.12, 960, 580), (99.5, 1.12, 960, 580), (100.5, 1.0, 960, 540)]
def camera(t):
    z = kf(t, [(a, b) for a, b, _, _ in CAM]); x = kf(t, [(a, d) for a, _, d, _ in CAM]); y = kf(t, [(a, e) for a, _, _, e in CAM])
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
            c.save(); frame(c, t); c.restore(); surf.write_to_png(f'ep18_{t}.png')
    else:
        t0, t1 = (float(args[1]), float(args[2])) if args and args[0] == 'range' else (0, DUR)
        out = sys.stdout.buffer
        for i in range(int(round(t0 * FPS)), int(round(t1 * FPS))):
            c.save(); frame(c, i / FPS); c.restore(); surf.flush(); out.write(surf.get_data())
