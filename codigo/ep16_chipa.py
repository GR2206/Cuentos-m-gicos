"""Episodio 16 — Chipá con Mamá Coco (112 s). Receta real, paso a paso:
lavarse las manos; 500 g de almidón de mandioca, 250 g de queso semiduro rallado, 1 cdita de sal,
100 g de manteca derretida, 2 huevos, 100 ml de leche; mezclar, amasar, bolitas y al horno a 180 °C
(¡siempre con un adulto!) hasta que estén doraditos. Llega Papá y comparten.

Uso:  python3 ep16_chipa.py              -> cuadros crudos por stdout
      python3 ep16_chipa.py range 0 56   -> solo un tramo
      python3 ep16_chipa.py stills 18 40 -> PNG sueltos
      python3 ep16_chipa.py srt 5.5      -> subtítulos .srt de la narración"""
import cairo, math, sys
import cuerpos as K
from amigos import hexc, ellipse, fill, OUT
from logos import word, sparkle
from ep02_puente_del_rio import kf, ss, moving, K_back
from ep03_donde_esta_tomi import bubble
from ep09_semilla_magica import srt
from ep12_burbujas_magicas import soap_bubble
from ep14_bananas_papa import heart

W, H, FPS = 1920, 1080, 30
DUR = 112.0
TOP_Y = 700                 # mesada
BOWL = (900, 690)
SINK_X = 330
OVEN = (1620, 1890)

NARRACION = [
    (6.0, 12.5, 'Hoy Coco y Mamá Coco van a cocinar... ¡chipá!'),
    (14.5, 21.5, 'Primero, lo más importante: ¡lavarse bien las manos con agua y jabón!'),
    (23.0, 33.0, 'Necesitamos almidón de mandioca, queso rallado, sal, manteca derretida, dos huevos y un poquito de leche.'),
    (35.0, 45.0, 'En un bol ponemos el almidón, el queso y la sal. ¡Y mezclamos!'),
    (47.0, 55.5, 'Agregamos la manteca derretida y los huevos.'),
    (57.0, 67.0, 'La leche va de a poquito, mientras amasamos hasta tener una masa suave.'),
    (69.0, 79.0, 'Ahora hacemos bolitas, ¡como pelotitas chiquitas!'),
    (81.0, 91.5, 'Y al horno, a ciento ochenta grados, siempre con un adulto, hasta que estén doraditos.'),
    (93.5, 103.0, '¡Mmm, qué rico olor! Papá Coco llegó justo a tiempo para compartir.'),
    (104.5, 110.0, '¡Cocinar juntos es lo más rico!'),
]
STEPS = [(14, 22, 'Paso 1: ¡a lavarse las manos!'), (22, 34, 'Los ingredientes'), (34, 46, 'Paso 2: almidón, queso y sal'),
         (46, 56, 'Paso 3: manteca y huevos'), (56, 68, 'Paso 4: leche de a poquito y amasar'),
         (68, 80, 'Paso 5: ¡hacer bolitas!'), (80, 92, 'Paso 6: al horno, ¡con un adulto!')]
# (tipo, texto de la pizarra, aparece, entra al bol)
INGR = [('almidon', '500 g de almidón de mandioca', 23.0, 35.5), ('queso', '250 g de queso rallado', 24.6, 38.0),
        ('sal', '1 cucharadita de sal', 26.2, 40.5), ('manteca', '100 g de manteca derretida', 27.8, 47.5),
        ('huevo', '2 huevos', 29.4, 49.5), ('leche', '100 ml de leche', 31.0, 57.0)]
SPOT = [1180, 1265, 1345, 1420, 1495, 1570]

BALLS = [(820 + 55 * (k % 4) - 0, 668 + 34 * (k // 4) - 0) for k in range(12)]
BALL_T = [69.0 + k * 0.75 for k in range(12)]
EAT_T = [97.5 + k * 0.45 for k in range(12)]

# ---------------- cocina ----------------
def kitchen_back(c):
    c.set_source_rgba(*hexc('#FFF3E0')); c.paint()
    for k in range(0, W, 120):
        c.rectangle(k, 0, 60, TOP_Y); c.set_source_rgba(*hexc('#FFE0B2')); c.fill()
    # pizarra
    c.rectangle(60, 70, 560, 470); fill(c, hexc('#8D6E63'), OUT, 7)
    c.rectangle(84, 94, 512, 422); fill(c, hexc('#2E5E4E'), OUT, 4)
    # ventana
    c.rectangle(1050, 230, 300, 220); fill(c, hexc('#81D4FA'), OUT, 7)
    c.move_to(1200, 230); c.line_to(1200, 450); c.move_to(1050, 340); c.line_to(1350, 340); c.set_source_rgba(*OUT); c.set_line_width(7); c.stroke()
    ellipse(c, 1290, 290, 32, 32); fill(c, hexc('#FFD600'), hexc('#F9A825'), 4)
    # estante con frascos
    c.rectangle(700, 300, 260, 18); fill(c, hexc('#A1887F'), OUT, 5)
    for k, col in enumerate(('#E57373', '#64B5F6', '#81C784')):
        c.rectangle(722 + 82 * k, 230, 56, 70); fill(c, hexc(col), OUT, 5)
        c.rectangle(716 + 82 * k, 220, 68, 16); fill(c, hexc('#8D6E63'), OUT, 4)

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
    if 83.0 < t < 89.3:   # bandeja adentro
        c.rectangle(x0 + 75, 760, x1 - x0 - 150, 14); fill(c, hexc('#90A4AE'), OUT, 3)
        q = ss(84.0, 88.5, t)
        for k in range(4):
            ellipse(c, x0 + 105 + 50 * k, 748, 20, 15); fill(c, mix('#FFF3C4', '#F2B640', q), OUT, 3)
    c.rectangle(x0 + 70, 590 - 22, x1 - x0 - 140, 16); fill(c, hexc('#90A4AE'), OUT, 4)
    c.rectangle(x0, 1010, x1 - x0, 70); c.set_source_rgba(*hexc('#B0BEC5')); c.fill()
    if on > 0:   # cartelito de temperatura
        word(c, '180°', (x0 + x1) / 2, 410, 64 * K_back((t - 82.0) / 0.4) + 0.01, colors=['#FF5722'], outline=6)
    if 84.0 < t < 89.0:  # relojito
        cx, cy = (x0 + x1) / 2, 950
        ellipse(c, cx, cy, 40, 40); fill(c, (1, 1, 1, 1), OUT, 5)
        a = -math.pi / 2 + (t - 84) / 5 * 2 * math.pi
        c.move_to(cx, cy); c.line_to(cx + 30 * math.cos(a), cy + 30 * math.sin(a)); c.set_source_rgba(*hexc('#E53935')); c.set_line_width(5); c.stroke()

def counter_front(c, t):
    c.rectangle(0, TOP_Y, OVEN[0] - 10, 30); fill(c, hexc('#BCAAA4'), OUT, 6)
    c.rectangle(0, TOP_Y + 30, OVEN[0] - 10, H - TOP_Y); fill(c, hexc('#FFCC80'), OUT, 6)
    for k in range(5):
        x = 30 + k * 318
        c.rectangle(x, TOP_Y + 70, 290, 250); fill(c, hexc('#FFB74D'), OUT, 5)
        ellipse(c, x + 145, TOP_Y + 100, 30, 8); fill(c, hexc('#8D6E63'), OUT, 3)
    # pileta y canilla
    ellipse(c, SINK_X, TOP_Y + 8, 150, 26); fill(c, hexc('#90A4AE'), OUT, 5)
    c.move_to(SINK_X + 110, TOP_Y); c.line_to(SINK_X + 110, TOP_Y - 120); c.curve_to(SINK_X + 110, TOP_Y - 170, SINK_X + 30, TOP_Y - 170, SINK_X + 30, TOP_Y - 120)
    c.set_source_rgba(*OUT); c.set_line_width(26); c.stroke_preserve(); c.set_source_rgba(*hexc('#CFD8DC')); c.set_line_width(16); c.stroke()

def mix(a, b, q):
    A, B = hexc(a), hexc(b)
    return tuple(A[i] + (B[i] - A[i]) * q for i in range(4))

# ---------------- ingredientes ----------------
def item(c, kind, x, y, s=1.0, tilt=0.0):
    c.save(); c.translate(x, y); c.rotate(tilt); c.scale(s, s)
    if kind == 'almidon':
        c.move_to(-34, 0); c.line_to(-30, -80); c.line_to(30, -80); c.line_to(34, 0); c.close_path(); fill(c, (1, 1, 1, 1), OUT, 4)
        c.move_to(-30, -80); c.line_to(-20, -96); c.line_to(20, -96); c.line_to(30, -80); fill(c, hexc('#E3F2FD'), OUT, 4)
        ellipse(c, 0, -42, 18, 18); fill(c, hexc('#8D6E63'), OUT, 3)
    elif kind == 'queso':
        ellipse(c, 0, -10, 40, 14); fill(c, hexc('#FFE082'), OUT, 4)
        for k in range(7):
            c.move_to(-26 + 9 * k, -16); c.line_to(-20 + 9 * k, -30 - 6 * (k % 2)); c.set_source_rgba(*hexc('#FFC107')); c.set_line_width(6); c.stroke()
        c.move_to(-40, -10); c.curve_to(-38, 18, 38, 18, 40, -10); fill(c, hexc('#4FC3F7'), OUT, 4)
    elif kind == 'sal':
        c.rectangle(-17, -60, 34, 60); fill(c, (1, 1, 1, 1), OUT, 4)
        c.move_to(-17, -60); c.curve_to(-17, -84, 17, -84, 17, -60); fill(c, hexc('#B0BEC5'), OUT, 4)
        for d in (-6, 6): ellipse(c, d, -70, 2.5, 2.5); c.set_source_rgba(*OUT); c.fill()
    elif kind == 'manteca':
        c.move_to(-32, -50); c.line_to(-28, 0); c.line_to(28, 0); c.line_to(32, -50); c.close_path(); fill(c, hexc('#E57373'), OUT, 4)
        ellipse(c, 0, -50, 32, 9); fill(c, hexc('#FFEB3B'), OUT, 3)
        c.move_to(30, -40); c.line_to(62, -46); c.set_source_rgba(*OUT); c.set_line_width(9); c.stroke()
    elif kind == 'huevo':
        for d in (-18, 18):
            ellipse(c, d, -26, 17, 24); fill(c, hexc('#FFF8E1'), OUT, 4)
    elif kind == 'leche':
        c.move_to(-26, 0); c.line_to(-26, -70); c.line_to(0, -92); c.line_to(26, -70); c.line_to(26, 0); c.close_path(); fill(c, (1, 1, 1, 1), OUT, 4)
        c.rectangle(-26, -50, 52, 26); c.set_source_rgba(*hexc('#42A5F5')); c.fill()
    c.restore()

def fly(t, k):
    """posición de un ingrediente: en la mesada, volando al bol, o None si ya entró."""
    kind, _, t_in, t_bowl = INGR[k]
    if t < t_in: return None
    x0, y0 = SPOT[k], TOP_Y
    if kind == 'leche':
        if t < 56.0: return x0, y0, K_back((t - t_in) / 0.4), 0.0
        if t < 61.5:
            q = ss(56.0, 57.0, t) * (1 - ss(61.0, 61.5, t))
            return x0 + (BOWL[0] + 50 - x0) * q, y0 + (BOWL[1] - 120 - y0) * q, 1.0, -1.6 * q
        return x0, y0, 1.0, 0.0
    if t < t_bowl: return x0, y0, K_back((t - t_in) / 0.4), 0.0
    if t < t_bowl + 1.0:
        q = ss(t_bowl, t_bowl + 1.0, t)
        return x0 + (BOWL[0] + 40 - x0) * q, y0 + (BOWL[1] - 100 - y0) * q - 160 * math.sin(math.pi * q), 1.0, -1.9 * q
    return None

def bowl(c, t):
    if t > 62.0: return
    x, y = BOWL
    a = 1 - ss(61.6, 62.0, t)
    n = sum(1 for (_, _, _, tb) in INGR if t > tb + 0.9) + ss(57.0, 61.0, t)
    c.push_group()
    ellipse(c, x, y - 70, 120, 26); fill(c, hexc('#4FC3F7'), OUT, 5)
    if n > 0:
        ellipse(c, x, y - 66 + 4 * (5 - n), 104, 20); fill(c, mix('#FFFFFF', '#FFE082', min(1, n / 5)), None, 0)
    if t > 60.0:
        ellipse(c, x, y - 82, 70, 34 * ss(60.0, 61.0, t) + 1); fill(c, hexc('#FFF3C4'), OUT, 4)
    if 42.0 < t < 46.0 or 52.0 < t < 56.0:   # cuchara que gira
        a2 = t * 6
        sx, sy = x + 50 * math.cos(a2), y - 70 + 10 * math.sin(a2)
        c.move_to(sx, sy); c.line_to(sx - 40, sy - 110); c.set_source_rgba(*OUT); c.set_line_width(14); c.stroke()
        c.move_to(sx, sy); c.line_to(sx - 40, sy - 110); c.set_source_rgba(*hexc('#BCAAA4')); c.set_line_width(8); c.stroke()
    c.move_to(x - 120, y - 70); c.curve_to(x - 115, y + 5, x + 115, y + 5, x + 120, y - 70); c.close_path(); fill(c, hexc('#29B6F6'), OUT, 5)
    c.pop_group_to_source(); c.paint_with_alpha(a)

def spoon_tip(t):
    a2 = t * 6
    return BOWL[0] + 50 * math.cos(a2) - 40, BOWL[1] - 180 + 10 * math.sin(a2)

def dough(c, t):
    if not 61.6 < t < 79.0: return
    x, y = BOWL
    c.rectangle(x - 170, y - 18, 340, 18); fill(c, hexc('#D7A86E'), OUT, 4)    # tablita
    left = 1 - sum(1 for tb in BALL_T if t > tb) / 12
    if left <= 0: return
    knead = 62.5 < t < 68.0
    sq = 1 + (0.25 * abs(math.sin((t - 62.5) * 3)) if knead else 0)
    r = 80 * math.sqrt(left) * K_back((t - 61.6) / 0.4)
    c.save(); c.translate(x - 30, y - 18); c.scale(sq, 1 / sq)
    ellipse(c, 0, -r * 0.7, r, r * 0.7); fill(c, hexc('#FFF3C4'), OUT, 5); c.restore()

def tray(c, t):
    """bandeja con bolitas: en la mesada (68-80), la lleva Mamá (80-83 y 89.3-92), de nuevo en la mesada después."""
    if t < 68.0 or 83.0 <= t <= 89.3: return
    golden = ss(84.0, 88.5, t)
    if t < 80.0 or t > 92.0: ox, oy = 0, 0
    elif t < 83.0:
        q = ss(80.3, 82.8, t); ox, oy = (1720 - 900) * q, (760 - 700) * q - 140 * math.sin(math.pi * q)
    else:
        q = ss(89.3, 91.8, t); ox, oy = (1720 - 900) * (1 - q), (760 - 700) * (1 - q) - 140 * math.sin(math.pi * q)
    c.save(); c.translate(ox + (180 if t >= 68 else 0), oy)
    c.rectangle(BOWL[0] + 20, TOP_Y - 12, 280, 14); fill(c, hexc('#90A4AE'), OUT, 4)
    for k, (bx, by) in enumerate(BALLS):
        if t < BALL_T[k] or t > EAT_T[k]: continue
        s = K_back((t - BALL_T[k]) / 0.3)
        bx2, by2 = bx + 230, TOP_Y - 28 - 0 * by + (k // 4) * 0 - (k // 4) * 18
        bx2 = BOWL[0] + 55 + 55 * (k % 4) + 20 * (k // 4)
        ellipse(c, bx2, by2, 22 * s, 17 * s); fill(c, mix('#FFF3C4', '#F2B640', golden), OUT, 3)
        if golden > 0.5:
            for d in (-7, 6): ellipse(c, bx2 + d, by2 - 6, 3, 2); c.set_source_rgba(*hexc('#C77F1A', golden)); c.fill()
    c.restore()
    if t > 89.3 and t < 96:
        for k in range(3):   # vapor
            ph = (t * 0.6 + k / 3) % 1
            x = BOWL[0] + 180 + 60 * k + ox + 20 * math.sin(t * 3 + k)
            c.move_to(x, TOP_Y - 60 - 80 * ph); c.curve_to(x + 20, TOP_Y - 80 - 80 * ph, x - 20, TOP_Y - 110 - 80 * ph, x, TOP_Y - 130 - 80 * ph)
            c.set_source_rgba(1, 1, 1, 0.8 * math.sin(math.pi * ph)); c.set_line_width(8); c.stroke()

def board_text(c, t):
    if t < 22.5: return
    c.select_font_face('Fredoka Light', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    c.set_font_size(46); c.set_source_rgba(1, 0.95, 0.6, 1); c.move_to(120, 155); c.show_text('Chipá')
    c.set_font_size(27)
    for k, (kind, txt, t_in, t_bowl) in enumerate(INGR):
        if t < t_in: continue
        a = ss(t_in, t_in + 0.4, t); y = 210 + 52 * k
        c.set_source_rgba(1, 1, 1, a); c.move_to(160, y); c.show_text(txt)
        item(c, kind, 128, y + 6, 0.32)
        done = t_bowl + 1.0 if kind != 'leche' else 61.0
        if t > done:
            q = ss(done, done + 0.3, t)
            c.move_to(98, y - 8); c.line_to(108, y + 2); c.line_to(98 + 32 * q, y - 22 * q)
            c.set_source_rgba(*hexc('#76FF03')); c.set_line_width(6); c.stroke()

# ---------------- personajes ----------------
def aim(x, base, s, tx, ty, flip=False, side=1):
    sx = x + 78 * side * s * (-1 if flip else 1); sy = base - 180 * s
    dx, dy = tx - sx, ty - sy
    if flip: dx = -dx
    return math.atan2(dy, dx), max(90, math.hypot(dx, dy) / s)

COCO_X = [(0, 720), (13.5, 720), (14.5, SINK_X + 140), (21.5, SINK_X + 140), (22.5, 720), (92.0, 720), (94.0, 810)]
MAMA_X = [(0, 1080), (13.5, 1080), (14.5, SINK_X + 330), (21.5, SINK_X + 330), (22.5, 1080), (80.0, 1080), (82.8, 1500),
          (89.5, 1500), (91.8, 1080)]
PAPA_X = [(0, -300), (92.5, -300), (95.0, 620)]

def draw_chars(c, t):
    s_c, base_c = 0.75, 830
    s_m, base_m = 0.95, 880
    # Papá
    if t > 92.5:
        px = kf(t, PAPA_X)
        eat_p = any(EAT_T[k] - 0.3 < t < EAT_T[k] + 0.3 for k in (2, 5, 8, 11))
        K.put(c, K.papa, px, base_m, 0.92, t=t, look=(1, 0.3), walk=t * 7 if moving(t, PAPA_X) else 0,
              mood='chew' if 97 < t < 104 and (t % 1.2) > 0.5 else ('closed' if 95 < t < 97 else 'smile'), chew=t,
              arm_r=math.radians(-20 if eat_p else 60), arm_l=math.radians(115))
        if 95.0 < t < 97.5:  # olfatea
            for k in range(3):
                ph = (t * 0.8 + k / 3) % 1
                x = px + 80 + 120 * ph
                c.move_to(x, base_m - 330 - 20 * k); c.curve_to(x + 20, base_m - 350 - 20 * k, x + 40, base_m - 310 - 20 * k, x + 60, base_m - 330 - 20 * k)
                c.set_source_rgba(*hexc('#FF8A65', math.sin(math.pi * ph))); c.set_line_width(6); c.stroke()
    # Mamá
    mx = kf(t, MAMA_X)
    m_r, m_l, m_len, mood_m, look_m = math.radians(65), math.radians(115), 115, 'smile', (-1, 0.3)
    if 15.0 < t < 21.0:   # se lava las manos
        m_r, m_len = aim(mx, base_m, s_m, SINK_X + 40 + 20 * math.sin(t * 9), TOP_Y - 30, True)
        m_l = m_r + 0.25
    if 34.5 < t < 41.5 or 46.5 < t < 52.0:  # alcanza ingredientes
        m_r = math.radians(-10 + 25 * math.sin(t * 2))
    if 56.0 < t < 61.5:   # sirve la leche
        m_r, m_len = aim(mx, base_m, s_m, *fly(t, 5)[:2], True)
    if 62.5 < t < 68.0 or 69.0 < t < 78.5:   # amasa / bolitas
        m_r, m_len = aim(mx, base_m, s_m, BOWL[0] + 60 + 30 * math.sin(t * 6), TOP_Y - 40, True)
    if 80.3 < t < 83.0 or 89.3 < t < 91.8:   # lleva la bandeja
        m_r = m_l = math.radians(10); look_m = (1, 0.3)
    if 83.0 <= t <= 89.3: look_m = (1, 0.4); m_r = math.radians(-20) if t < 84 or t > 88.6 else math.radians(65)
    if 97 < t < 104: mood_m = 'chew' if (t % 1.3) > 0.6 else 'smile'
    flip_m = not (80.3 < t < 91.8 and look_m[0] > 0)
    K.put(c, K.mama, mx, base_m, s_m, flip=flip_m, t=t, look=(1, look_m[1]), mood=mood_m, chew=t,
          arm_r=m_r, arm_l=m_l, arm_len=m_len, walk=t * 7 if moving(t, MAMA_X) else 0)
    if 80.3 < t < 91.8 and not (83.0 <= t <= 89.3) or 83.0 < t < 84.0 or 88.6 < t < 89.3:   # guantes de cocina
        for d in (-1, 1):
            ellipse(c, mx + d * 70 + (60 if not flip_m else -60), base_m - 170, 26, 22); fill(c, hexc('#E53935'), OUT, 4)
    # Coco
    cx = kf(t, COCO_X)
    mood, look = 'smile', (1, 0.4)
    ar, al, alen = math.radians(65 + 6 * math.sin(t * 2)), math.radians(115 - 6 * math.sin(t * 2)), 115
    if 8.5 < t < 11: ar, al = math.radians(-60), math.radians(-120); mood = 'o'      # ¡sí!
    if 15.0 < t < 21.0:
        ar, alen = aim(cx, base_c, s_c, SINK_X + 10 + 20 * math.sin(t * 9 + 1), TOP_Y - 30, False, 1); al = ar
        al_, _ = aim(cx, base_c, s_c, SINK_X + 10 + 20 * math.sin(t * 9 + 1), TOP_Y - 30, False, -1); al = al_
    if 42.0 < t < 46.0 or 52.0 < t < 56.0:  # revuelve
        ar, alen = aim(cx, base_c, s_c, *spoon_tip(t))
        mood = 'closed' if (t % 2) > 1.4 else 'smile'
    if 62.5 < t < 68.0 or 69.0 < t < 78.5:
        ar, alen = aim(cx, base_c, s_c, BOWL[0] - 60 + 30 * math.sin(t * 6 + 2), TOP_Y - 40)
    if 80.3 < t < 92.0: look = (1, 0.1)
    if 83.0 < t < 89.0: mood = 'o' if t < 85 else 'smile'
    if 97 < t < 104:
        mood = 'chew' if (t % 1.1) > 0.5 else 'smile'
        ar = math.radians(-30 if (t % 1.1) < 0.5 else 40)
    if 104 < t: ar, al = math.radians(-58 + 25 * math.sin(t * 9)), math.radians(-122 - 25 * math.sin(t * 9))
    hop = -25 * abs(math.sin(t * 6)) if 8.5 < t < 11 or t > 104 else 0
    K.put(c, K.coco, cx, base_c + hop, s_c, t=t, mood=mood, look=look, arm_r=ar, arm_l=al, arm_len=alen, chew=t,
          walk=t * 8 if moving(t, COCO_X) else 0)

def washing(c, t):
    if not 14.8 < t < 21.5: return
    a = ss(14.8, 15.3, t) * (1 - ss(21.0, 21.5, t))
    for k in range(5):   # chorro de agua
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
    for k in range(6):
        p = fly(t, k)
        if p:
            item(c, INGR[k][0], p[0], p[1], 1.0 * p[2] + 0.001, p[3])
            if INGR[k][0] == 'leche' and 57.0 < t < 61.0:   # chorrito de leche
                c.move_to(p[0] - 50, p[1] - 70); c.line_to(BOWL[0] - 10, BOWL[1] - 70)
                c.set_source_rgba(1, 1, 1, 0.95); c.set_line_width(7); c.stroke()
    bowl(c, t)
    for k in range(6):   # nubecita de harina al caer
        tb = INGR[k][3]
        if INGR[k][0] != 'leche' and tb + 0.9 < t < tb + 1.6:
            q = (t - tb - 0.9) / 0.7
            for j in range(6):
                ellipse(c, BOWL[0] + 90 * math.cos(j) * q, BOWL[1] - 90 - 50 * q * abs(math.sin(j * 2)), 18 * (1 - q), 18 * (1 - q))
                c.set_source_rgba(1, 1, 1, 0.8 * (1 - q)); c.fill()
    dough(c, t)
    tray(c, t)
    if t > 104:
        for k in range(10):
            ph = (t * 0.6 + k / 10) % 1
            heart(c, 300 + 150 * k, TOP_Y - 450 - 200 * ph, 0.9, math.sin(math.pi * ph))
    # globitos
    mx = kf(t, MAMA_X); cx = kf(t, COCO_X)
    bubble(c, mx, 380, '¿Hacemos chipá?', (t - 5.8) / 3.0, 50)
    bubble(c, cx, 480, '¡Sííí!', (t - 8.6) / 2.6, 60)
    bubble(c, cx, 480, '¡Con jabón!', (t - 16.0) / 3.5, 50)
    bubble(c, cx, 480, '¡Qué masa suave!', (t - 64.0) / 3.2, 48)
    bubble(c, cx, 480, '¡Con un adulto!', (t - 81.0) / 3.4, 50)
    bubble(c, 1500, 380, '¡Doraditos!', (t - 89.4) / 2.6, 50)
    bubble(c, kf(t, PAPA_X), 400, '¡Qué rico olor!', (t - 95.0) / 3.0, 50)
    bubble(c, cx, 480, '¡Mmm!', (t - 99.5) / 2.4, 60)

def overlay(c, t):
    if t < 5.6:
        a = 1 - ss(4.8, 5.5, t)
        c.push_group()
        c.set_source_rgba(1, 1, 1, 0.55); c.paint()
        word(c, 'Chipá con', W / 2, 400, 130 * K_back((t - 0.6) / 0.6) + 0.01, tilt=0.05, outline=10)
        word(c, 'Mamá Coco', W / 2, 560, 140 * K_back((t - 1.0) / 0.6) + 0.01, start=3, tilt=0.05, outline=10)
        c.pop_group_to_source(); c.paint_with_alpha(a)
    for (a1, b1, txt) in STEPS:
        if a1 <= t < b1:
            s = K_back((t - a1) / 0.4) * (1 - ss(b1 - 0.3, b1, t))
            word(c, txt, 1230, 115, 66 * s + 0.01, tilt=0.03, outline=8)
    if t > 104.5:
        s = K_back((t - 104.5) / 0.6)
        word(c, '¡Cocinar juntos', 1230, 110, 84 * s + 0.01, tilt=0.05, outline=9)
        word(c, 'es lo más rico!', 1230, 210, 84 * s + 0.01, start=4, tilt=0.05, outline=9)
    a = max(1 - ss(0, 0.8, t), ss(DUR - 2.0, DUR, t))
    if a > 0: c.set_source_rgba(1, 1, 1, a); c.paint()

CAM = [(0, 1.0, 960, 540), (34.0, 1.0, 960, 540), (35.0, 1.12, 960, 580), (79.5, 1.12, 960, 580), (80.5, 1.0, 960, 540)]
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
            c.save(); frame(c, t); c.restore(); surf.write_to_png(f'ep16_{t}.png')
    else:
        t0, t1 = (float(args[1]), float(args[2])) if args and args[0] == 'range' else (0, DUR)
        out = sys.stdout.buffer
        for i in range(int(round(t0 * FPS)), int(round(t1 * FPS))):
            c.save(); frame(c, i / FPS); c.restore(); surf.flush(); out.write(surf.get_data())
