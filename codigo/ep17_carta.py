"""Episodio 17 — La carta de Coco (100 s).
Coco escribe una carta de Navidad y cada amigo le cuenta su deseo: Lola un tamborcito, Tito una pelota,
Pipa un barrilete y Tomi un libro de cuentos. ¿Y Coco? Dibuja un corazón: "que estemos todos juntos".
Lola lleva la carta a la estrella, a la mañana aparecen los regalos... y el deseo de Coco se cumple con un abrazo.

Uso:  python3 ep17_carta.py              -> cuadros crudos por stdout
      python3 ep17_carta.py range 0 50   -> solo un tramo
      python3 ep17_carta.py stills 20 70 -> PNG sueltos
      python3 ep17_carta.py srt 5.5      -> subtítulos .srt de la narración"""
import cairo, math, sys
import cuerpos as K
from amigos import hexc, ellipse, fill, OUT
from logos import word, sparkle
from ep02_puente_del_rio import kf, ss, moving, K_back, music_note
from ep03_donde_esta_tomi import bubble
from ep09_semilla_magica import SKY, LAND, cloud, sun, srt
from ep14_bananas_papa import heart
import ep15_navidad as N

W, H, FPS = 1920, 1080, 30
DUR = 100.0
GROUND = 880
PAPER = (210, 380, 300, 340)            # x, y, w, h de la carta en el atril
STAR = (N.TOP[0], N.TOP[1] - 70)

NARRACION = [
    (6.0, 13.0, 'Faltaba poquito para Navidad, y Coco quiso escribir una carta.'),
    (15.0, 23.0, 'Lola le dijo: ¡yo quiero un tamborcito para cantar!'),
    (24.5, 31.5, 'Tito pidió una pelota grande, de colores.'),
    (32.5, 39.5, 'Pipa, desde arriba, pidió un barrilete para volar alto.'),
    (40.5, 47.5, 'Y Tomi, despacito, pidió un libro de cuentos.'),
    (49.0, 59.5, '¿Y Coco qué quería? Pensó, pensó... y dibujó un corazón: ¡que estemos todos juntos!'),
    (61.0, 67.0, 'Lola llevó la carta volando, bien alto, hasta la estrella.'),
    (68.0, 74.0, 'Y la estrella brilló, brilló... ¡con mucha magia!'),
    (78.0, 86.0, 'A la mañana, ¡sorpresa! Había regalos para todos.'),
    (87.0, 95.0, 'Y el deseo de Coco también se cumplió: ¡todos juntos, con un gran abrazo!'),
    (95.5, 99.5, '¡Feliz Navidad!'),
]

# deseos: (amigo, ícono, t0 del pedido, t en que Coco lo dibuja, lugar en la carta, regalo a la mañana)
WISH = [('lola', 'tambor', 15.5, 21.5, (290, 520), 740, '#29B6F6', 80.0),
        ('tito', 'pelota', 24.5, 30.0, (430, 520), 1100, '#FF7043', 81.4),
        ('pipa', 'barrilete', 32.5, 38.0, (290, 625), 1320, '#AB47BC', 82.8),
        ('tomi', 'libro', 40.5, 46.0, (430, 625), 860, '#66BB6A', 84.2)]
HEART_T = 55.0

def night(t): return ss(60.0, 65.0, t) * (1 - ss(74.0, 78.0, t))

# ---------------- íconos ----------------
def icon(c, kind, x, y, s=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    if kind == 'tambor':
        c.rectangle(-40, -28, 80, 56); fill(c, hexc('#E53935'), OUT, 5)
        ellipse(c, 0, -28, 40, 12); fill(c, (1, 1, 1, 1), OUT, 5)
        for k in range(4):
            c.move_to(-40 + 27 * k, -20); c.line_to(-27 + 27 * k, 22); c.set_source_rgba(*hexc('#FFD600')); c.set_line_width(5); c.stroke()
        for d in (-1, 1):
            c.move_to(d * 15, -40); c.line_to(d * 45, -80); c.set_source_rgba(*OUT); c.set_line_width(7); c.stroke()
            ellipse(c, d * 47, -84, 9, 9); fill(c, hexc('#FFD600'), OUT, 3)
    elif kind == 'pelota':
        ellipse(c, 0, 0, 42, 42); fill(c, (1, 1, 1, 1), OUT, 5)
        for k, col in enumerate(('#F44336', '#FFEB3B', '#2196F3')):
            c.save(); c.arc(0, 0, 40, 0, 2 * math.pi); c.clip()
            c.move_to(0, 0); c.arc(0, 0, 44, k * 2.1, k * 2.1 + 1.05); c.close_path(); c.set_source_rgba(*hexc(col)); c.fill(); c.restore()
        ellipse(c, 0, 0, 42, 42); c.set_source_rgba(*OUT); c.set_line_width(5); c.stroke()
    elif kind == 'barrilete':
        c.move_to(0, -55); c.line_to(38, 0); c.line_to(0, 55); c.line_to(-38, 0); c.close_path(); fill(c, hexc('#FFD600'), OUT, 5)
        c.move_to(0, -55); c.line_to(0, 55); c.move_to(-38, 0); c.line_to(38, 0); c.set_source_rgba(*OUT); c.set_line_width(3); c.stroke()
        c.move_to(0, 55); c.curve_to(20, 75, -20, 90, 5, 110); c.set_source_rgba(*OUT); c.set_line_width(4); c.stroke()
        for k in range(3): ellipse(c, 8 - 8 * (k % 2), 70 + 14 * k, 7, 5); fill(c, hexc(('#E53935', '#29B6F6', '#43A047')[k]), OUT, 2)
    elif kind == 'libro':
        for d in (-1, 1):
            c.move_to(0, -30); c.curve_to(d * 20, -40, d * 40, -38, d * 48, -32); c.line_to(d * 48, 32); c.curve_to(d * 40, 26, d * 20, 26, 0, 36); c.close_path()
            fill(c, hexc('#FFF8E1'), OUT, 5)
        c.move_to(0, -30); c.line_to(0, 36); c.set_source_rgba(*OUT); c.set_line_width(4); c.stroke()
        for k in range(3):
            for d in (-1, 1):
                c.move_to(d * 10, -14 + 14 * k); c.line_to(d * 38, -14 + 14 * k); c.set_source_rgba(*hexc('#90A4AE')); c.set_line_width(3); c.stroke()
        sparkle(c, 30, -45, 9, '#FFD600')
    c.restore()

def wish_cloud(c, x, y, kind, p):
    """globito de pensamiento con el ícono del deseo."""
    if p <= 0 or p >= 1: return
    s = K_back(min(1.0, p / 0.2)) * (1 - ss(0.85, 1.0, p))
    if s <= 0.01: return
    c.save(); c.translate(x, y); c.scale(s, s)
    for (dx, dy, r) in ((-20, 95, 10), (-8, 70, 15)):
        ellipse(c, dx, dy, r, r); fill(c, (1, 1, 1, 1), OUT, 4)
    for (dx, dy, r) in ((-60, -10, 55), (0, -30, 65), (60, -10, 55), (0, 15, 60)):
        ellipse(c, dx, dy, r, r * 0.85); fill(c, (1, 1, 1, 1), OUT, 5)
    for (dx, dy, r) in ((-60, -10, 55), (0, -30, 65), (60, -10, 55), (0, 15, 60)):
        ellipse(c, dx, dy, r - 5, r * 0.85 - 5); c.set_source_rgba(1, 1, 1, 1); c.fill()
    icon(c, kind, 0, -8, 0.95)
    c.restore()

# ---------------- carta y atril ----------------
def paper_on(c, x, y, w, h, t, scale=1.0):
    c.save(); c.translate(x, y); c.scale(scale, scale)
    c.rectangle(0, 0, w, h); fill(c, hexc('#FFFDE7'), OUT, 5)
    for k in range(6):
        c.move_to(20, 70 + 45 * k); c.line_to(w - 20, 70 + 45 * k); c.set_source_rgba(*hexc('#BBDEFB')); c.set_line_width(2); c.stroke()
    c.select_font_face('Fredoka Light', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    c.set_font_size(34); c.set_source_rgba(*hexc('#E53935')); c.move_to(28, 48); c.show_text('Mi carta')
    sparkle(c, w - 35, 35, 12, '#FFD600')
    for (_, kind, _, td, (ix, iy), *_r) in WISH:
        if t > td:
            icon(c, kind, ix - PAPER[0], iy - PAPER[1], 0.62 * K_back((t - td) / 0.4))
    if t > HEART_T:
        hs = K_back((t - HEART_T) / 0.5)
        heart(c, w / 2, h - 40, 1.25 * hs)
    c.restore()

def easel(c, t):
    x, y, w, h = PAPER
    for (x0, x1) in ((x + 40, x + 10), (x + w - 40, x + w - 10)):
        c.move_to(x0, y + 60); c.line_to(x1, GROUND + 5); c.set_source_rgba(*OUT); c.set_line_width(20); c.stroke()
        c.move_to(x0, y + 60); c.line_to(x1, GROUND + 5); c.set_source_rgba(*hexc('#A1887F')); c.set_line_width(12); c.stroke()
    c.rectangle(x - 15, y + h, w + 30, 22); fill(c, hexc('#8D6E63'), OUT, 5)
    if t < 61.2: paper_on(c, x, y, w, h, t)

def box(c, x, y, col, opened, kind, t, t_open):
    """regalito que se abre y deja salir el ícono."""
    c.save(); c.translate(x, y)
    c.rectangle(-55, -90, 110, 90); fill(c, hexc(col), OUT, 5)
    c.rectangle(-12, -90, 24, 90); fill(c, hexc('#FFEB3B'), OUT, 3)
    lift = 120 * K_back(opened) if opened > 0 else 0
    c.save(); c.translate(0, -lift); c.rotate(-0.5 * min(1, opened))
    c.rectangle(-62, -105, 124, 22); fill(c, hexc(col), OUT, 5)
    for sx in (-1, 1):
        ellipse(c, sx * 22, -115, 22, 14); fill(c, hexc('#FFEB3B'), OUT, 4)
    c.restore(); c.restore()
    if opened > 0:
        q = ss(t_open + 0.3, t_open + 1.1, t); d = ss(t_open + 1.8, t_open + 2.6, t)
        icon(c, kind, x, y - 100 - 90 * q + 50 * d, 0.4 + 0.6 * q - 0.15 * d)
        if t < t_open + 1.5:
            for k in range(6):
                a = k * math.pi / 3; r = 40 + 90 * (t - t_open)
                sparkle(c, x + r * math.cos(a), y - 120 + r * math.sin(a), 12, '#FFD600')

# ---------------- personajes ----------------
def aim(x, base, s, tx, ty, flip=False, side=1):
    sx = x + 78 * side * s * (-1 if flip else 1); sy = base - 180 * s
    dx, dy = tx - sx, ty - sy
    if flip: dx = -dx
    return math.atan2(dy, dx), max(90, math.hypot(dx, dy) / s)

COCO_X = [(0, 640), (86.5, 640), (87.5, 620)]
TOMI_X = [(0, 1100), (40.0, 1100), (42.5, 830), (47.5, 830), (49.5, 1050), (78.0, 950), (85.5, 950), (88.0, 760)]
TITO_X = [(0, 1330), (24.0, 1330), (25.5, 900), (31.0, 900), (32.0, 1330), (78.0, 1240), (85.5, 1240), (88.0, 980)]
PIPA_X = [(0, 1600), (78.0, 1450), (85.5, 1450), (88.0, 1180)]
MAMA_X = [(0, -300), (86.0, -300), (88.5, 410)]
PAPA_X = [(0, -480), (86.0, -480), (88.8, 220)]
def pipa_neck(t): return kf(t, [(32.0, 300), (33.5, 420), (39.0, 420), (40.5, 300)])
def pipa_lean(t): return kf(t, [(32.0, 0), (33.5, -260), (39.0, -260), (40.5, 0)])
def pipa_head(t): return kf(t, PIPA_X) + 0.55 * pipa_lean(t), GROUND - 0.55 * (260 + pipa_neck(t))

def lola_pos(t):
    if t < 15.0: return 1150 + 60 * math.sin(t * 0.6), 470 + 18 * math.sin(t * 3)
    if t < 24.0:
        q = ss(15.0, 16.2, t) * (1 - ss(23.0, 24.0, t))
        return 1150 + (800 - 1150) * q, 470 + (520 - 470) * q + 15 * math.sin(t * 3)
    if t < 60.0: return 1150 + 60 * math.sin(t * 0.6), 470 + 18 * math.sin(t * 3)
    if t < 61.2:
        q = ss(60.0, 61.2, t); x0, y0 = 1150 + 60 * math.sin(60 * 0.6), 470
        return x0 + (PAPER[0] + 150 - x0) * q, y0 + (PAPER[1] + 40 - y0) * q - 80 * math.sin(math.pi * q)
    if t < 66.0:
        q = ss(61.2, 65.5, t)
        return PAPER[0] + 150 + (STAR[0] - 60 - PAPER[0] - 150) * q, PAPER[1] + 40 + (STAR[1] + 30 - PAPER[1] - 40) * q - 120 * math.sin(math.pi * q)
    if t < 78.0:
        q = ss(66.5, 69.0, t); x0, y0 = STAR[0] - 60, STAR[1] + 30
        return x0 + (1150 - x0) * q, y0 + (470 - y0) * q
    if t < 85.5: return kf(t, [(78.0, 1150), (79.5, 780)]), kf(t, [(78.0, 470), (79.5, 640)]) + 15 * math.sin(t * 3)
    return kf(t, [(85.5, 780), (88.0, 620)]), kf(t, [(85.5, 640), (88.0, 470)]) + 15 * math.sin(t * 3)

def hugging(t): return 88.5 < t < 95.5

def draw_chars(c, t):
    hug = hugging(t)
    bob = lambda ph: -18 * abs(math.sin(t * 4 + ph)) if t > 95.5 else 0
    # Pipa
    px = kf(t, PIPA_X)
    K.put(c, K.pipa, px, GROUND + bob(0.5), 0.55, t=t, neck=pipa_neck(t), lean=pipa_lean(t), look=(-1, 0.2),
          walk=t * 7 if moving(t, PIPA_X) else 0)
    # Tito
    tx = kf(t, TITO_X)
    K.put(c, K.tito, tx, GROUND + bob(1.0), 0.6, flip=True, t=t, look=(1, 0), walk=t * 6 if moving(t, TITO_X) else 0,
          lid=0.8 if hug else 0.0, reach=160 if hug else None)
    # Tomi
    tmx = kf(t, TOMI_X)
    K.put(c, K.tomi, tmx, GROUND + bob(1.5), 0.55, t=t, look=(-1, 0), walk=t * 3 if moving(t, TOMI_X) else 0, mood='closed' if hug else 'smile')
    # Mamá y Papá
    if t > 86.0:
        for (who, xs, ph) in ((K.papa, PAPA_X, 0.8), (K.mama, MAMA_X, 1.3)):
            x = kf(t, xs)
            K.put(c, who, x, GROUND + bob(ph), 0.72, t=t, look=(1, 0), walk=t * 7 if moving(t, xs) else 0,
                  arm_r=math.radians(-15 if hug else 50), arm_l=math.radians(115), mood='closed' if hug else 'smile')
    # Coco
    cx = kf(t, COCO_X)
    flip, look, mood = False, (1, -0.2), 'smile'
    ar, al, alen = math.radians(65 + 6 * math.sin(t * 2)), math.radians(115 - 6 * math.sin(t * 2)), 115
    for (_, _, t0, td, (ix, iy), *_r) in WISH:
        if td - 1.2 < t < td + 0.4:   # dibuja en la carta
            flip, look = True, (1, 0.2)
            ar, alen = aim(cx, GROUND, 0.55, ix + 25 * math.sin(t * 12), iy + 15 * math.cos(t * 12), True); al = ar + 0.2
    if 49.0 < t < 53.5: mood = 'o'; ar = math.radians(-100); alen = 100; look = (0.3, -0.8)     # piensa
    if HEART_T - 1.3 < t < HEART_T + 0.4:
        flip, look = True, (1, 0.2)
        ar, alen = aim(cx, GROUND, 0.55, PAPER[0] + 150 + 25 * math.sin(t * 10), PAPER[1] + 300, True); al = ar + 0.2
    if 56.0 < t < 60.0: mood = 'closed'; ar, al = math.radians(-60), math.radians(-120)
    if 61.2 < t < 74: look = (0.2, -1)
    if 84.8 < t < 86.5: mood, look = 'o', (1, 0)
    if hug: mood = 'closed'; ar, al = math.radians(170), math.radians(10)
    if t > 95.5: ar, al = math.radians(-58 + 25 * math.sin(t * 9)), math.radians(-122 - 25 * math.sin(t * 9))
    K.put(c, K.coco, cx, GROUND + bob(0), 0.55, flip=flip, t=t, mood=mood, look=look, arm_r=ar, arm_l=al, arm_len=alen)
    # crayón
    for (_, _, t0, td, (ix, iy), *_r) in WISH + [(None, None, 0, HEART_T, (PAPER[0] + 150, PAPER[1] + 300))]:
        if td - 1.2 < t < td + 0.4:
            cx2 = ix + 25 * math.sin(t * 12 if td != HEART_T else t * 10); cy2 = iy + 15 * math.cos(t * 12)
            c.move_to(cx2, cy2); c.line_to(cx2 + 30, cy2 + 30); c.set_source_rgba(*OUT); c.set_line_width(16); c.stroke()
            c.move_to(cx2, cy2); c.line_to(cx2 + 30, cy2 + 30); c.set_source_rgba(*hexc('#E53935')); c.set_line_width(10); c.stroke()
    # Lola
    lx, ly = lola_pos(t)
    K.put(c, K.lola, lx, ly + bob(2.0), 0.5, t=t, flap=20, look=(-0.6, 0.3))
    if 61.2 < t < 66.0:   # carta enrollada
        c.save(); c.translate(lx - 10, ly + 40); c.rotate(0.3)
        c.rectangle(-45, -14, 90, 28); fill(c, hexc('#FFFDE7'), OUT, 4)
        c.rectangle(-6, -16, 12, 32); fill(c, hexc('#E53935'), OUT, 3); c.restore()
    return cx, tx, tmx, px, lx, ly

def world(c, t):
    nt = night(t)
    c.set_source_surface(SKY, 0, 0); c.paint()
    if nt < 1:
        c.push_group(); sun(c, t)
        for (x0, y0, s, sp) in ((150, 160, 0.9, 10), (700, 110, 0.7, 7)): cloud(c, (x0 + sp * t) % 2300 - 250, y0, s)
        c.pop_group_to_source(); c.paint_with_alpha(1 - nt)
    if nt > 0:
        c.set_source_rgba(*hexc('#141048', 0.92 * nt)); c.paint()
        for k in range(40):
            sx, sy = (k * 197) % 1900, 30 + (k * 83) % 420
            ellipse(c, sx, sy, 3, 3); c.set_source_rgba(1, 1, 0.85, nt * (0.6 + 0.4 * math.sin(t * 3 + k))); c.fill()
        ellipse(c, 1600, 170, 80, 80); fill(c, (1, 0.96, 0.62, nt), (0.98, 0.75, 0.18, nt), 6)
    c.set_source_surface(LAND, 0, 0); c.paint()
    if nt > 0: c.set_source_rgba(*hexc('#141048', 0.55 * nt)); c.mask_surface(LAND, 0, 0)
    N.xmas_palm(c, t, 0)
    N.garland(c, 100.0)
    N.ornaments(c, 100.0, nt)
    magic = ss(66.0, 68.0, t) * (1 - ss(73.0, 76.0, t))
    N.star(c, t, STAR, 1.0 + 0.5 * magic, max(0.35, nt, 1.5 * magic))
    if magic > 0:   # rayos de la estrella
        for k in range(12):
            a = k * math.pi / 6 + t * 0.6
            c.move_to(STAR[0] + 90 * math.cos(a), STAR[1] + 90 * math.sin(a)); c.line_to(STAR[0] + 260 * math.cos(a), STAR[1] + 260 * math.sin(a))
            c.set_source_rgba(1, 0.95, 0.5, 0.5 * magic); c.set_line_width(10); c.stroke()
    if 65.5 < t < 67.0:   # la carta se vuelve brillitos
        q = ss(65.5, 67.0, t)
        for k in range(14):
            a = k * 0.45; r = 30 + 200 * q
            sparkle(c, STAR[0] - 60 + r * math.cos(a), STAR[1] + 30 + r * math.sin(a), 16 * (1 - q) + 2, '#FFFFFF')
    if 69.0 < t < 74.0:   # lluvia de magia hacia la palmera
        for k in range(24):
            ph = ((t - 69) * 0.5 + k / 24) % 1
            sparkle(c, STAR[0] - 300 + (k * 53) % 600, STAR[1] + 550 * ph, 12 * math.sin(math.pi * ph), ('#FFD600', '#FFFFFF', '#FF80AB')[k % 3])
    easel(c, t)
    # regalos
    for (who, kind, t0, td, pos, gx, col, t_open) in WISH:
        if t > 71.0:
            s = K_back((t - 71.0 - 0.3 * WISH.index((who, kind, t0, td, pos, gx, col, t_open))) / 0.5)
            if s > 0.01:
                c.save(); c.translate(gx, GROUND + 10); c.scale(0.95 * s, 0.95 * s)
                box(c, 0, 0, col, ss(t_open, t_open + 0.6, t), kind, t, t_open); c.restore()
    cx, tx, tmx, px, lx, ly = draw_chars(c, t)
    if hugging(t):
        for k in range(6):
            ph = ((t - 88.5) * 0.5 + k / 6) % 1
            heart(c, 400 + 160 * k, GROUND - 450 - 250 * ph, 1.1 + 0.4 * ph, math.sin(math.pi * ph))
    if t > 95.5:
        for k in range(3):
            ph = (t * 0.7 + k / 3) % 1
            music_note(c, lx + 40 + 60 * ph, ly - 150 - 160 * ph, math.sin(math.pi * ph), ['#E91E63', '#1E88E5', '#FFD600'][k])
    # globitos
    bubble(c, cx + 40, GROUND - 300, '¡Voy a escribir una carta!', (t - 6.5) / 4.0, 44)
    wish_cloud(c, lx + 20, ly - 230, 'tambor', (t - 16.3) / 6.5)
    wish_cloud(c, tx - 60, GROUND - 430, 'pelota', (t - 25.6) / 5.6)
    hx, hy = pipa_head(t); wish_cloud(c, hx - 30, hy - 220, 'barrilete', (t - 33.6) / 5.6)
    wish_cloud(c, tmx + 10, GROUND - 330, 'libro', (t - 42.6) / 4.6)
    bubble(c, cx + 40, GROUND - 300, '¿Y yo qué quiero…?', (t - 49.0) / 4.4, 46)
    bubble(c, cx + 40, GROUND - 300, '¡Que estemos todos juntos!', (t - 56.0) / 4.0, 44)
    bubble(c, cx + 40, GROUND - 300, '¿Y mi regalo?', (t - 84.8) / 2.2, 46)
    bubble(c, 520, GROUND - 0.72 * 560, '¡Acá estamos todos!', (t - 88.8) / 3.5, 46)

def overlay(c, t):
    if t < 5.6:
        a = 1 - ss(4.8, 5.5, t)
        c.push_group(); word(c, 'La carta de Coco', W / 2, 230, 125 * K_back((t - 0.6) / 0.6) + 0.01,
                             colors=['#E53935', '#43A047', '#FFD600'], tilt=0.05, outline=9)
        c.pop_group_to_source(); c.paint_with_alpha(a)
    if t > 95.5:
        s = K_back((t - 95.5) / 0.7)
        word(c, '¡Feliz Navidad!', W / 2, 200, 150 * s + 0.01, colors=['#E53935', '#43A047', '#FFD600'], tilt=0.06, outline=11)
    if 75.5 < t < 78.5:   # pasa la noche
        a = math.sin(math.pi * (t - 75.5) / 3.0)
        c.set_source_rgba(1, 1, 1, 0.85 * a); c.paint()
    a = max(1 - ss(0, 0.8, t), ss(DUR - 2.0, DUR, t))
    if a > 0: c.set_source_rgba(1, 1, 1, a); c.paint()

CAM = [(0, 1.0, 960, 540), (14.0, 1.0, 960, 540), (15.0, 1.12, 830, 560), (59.5, 1.12, 830, 560), (60.5, 1.0, 960, 540)]
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
            c.save(); frame(c, t); c.restore(); surf.write_to_png(f'ep17_{t}.png')
    else:
        t0, t1 = (float(args[1]), float(args[2])) if args and args[0] == 'range' else (0, DUR)
        out = sys.stdout.buffer
        for i in range(int(round(t0 * FPS)), int(round(t1 * FPS))):
            c.save(); frame(c, i / FPS); c.restore(); surf.flush(); out.write(surf.get_data())
