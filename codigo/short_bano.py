"""Short familiar — ¡Hora del baño! (vertical 1080x1920, 56 s).
Coco está embarrado y no se quiere bañar. Mamá Coco llena la bañera de burbujas
y un patito... ¡y Coco se tira de cabeza! Sombrero de espuma, toalla y abrazo.
Uso: python3 short_bano.py               -> cuadros crudos 1080x1920 por stdout
     python3 short_bano.py short 0 28    -> tramo
     python3 short_bano.py stills 5 30   -> PNG sueltos
     python3 short_bano.py portada       -> short_bano_portada.png"""
import cairo, math, os, sys
import cuerpos as K
from amigos import hexc, ellipse, fill, OUT
from logos import word, sparkle
from ep02_puente_del_rio import kf, ss, K_back, music_note
from ep03_donde_esta_tomi import bubble
from ep12_burbujas_magicas import soap_bubble
from ep14_bananas_papa import heart

SW, SH, FPS = 1080, 1920, 30
DUR = 56.0
FLOOR = 1520
TUB = (540, 1150)          # centro del borde de la bañera
PLANT = 960
JUMP = (21.0, 22.2)
CLEAN = (28.0, 36.0)

# ---------------- escenario ----------------
def room(c, t):
    c.set_source_rgba(*hexc('#B3E5FC')); c.paint()
    for i in range(0, SW, 90):          # azulejos
        for j in range(0, FLOOR, 90):
            c.rectangle(i + 3, j + 3, 84, 84); c.set_source_rgba(*hexc('#E1F5FE' if (i // 90 + j // 90) % 2 else '#B3E5FC')); c.fill()
    # ventana con atardecer y luna
    c.rectangle(110, 420, 300, 300); fill(c, hexc('#8D6E63'), OUT, 6)
    g = cairo.LinearGradient(0, 430, 0, 710)
    g.add_color_stop_rgb(0, *hexc('#5E35B1')[:3]); g.add_color_stop_rgb(1, *hexc('#FF8A65')[:3])
    c.rectangle(125, 435, 270, 270); c.set_source(g); c.fill()
    ellipse(c, 320, 510, 40, 40); fill(c, hexc('#FFF59D'), hexc('#FBC02D'), 4)
    for (sx, sy) in ((180, 480), (240, 560), (200, 620)):
        sparkle(c, sx, sy, 10 + 3 * math.sin(t * 3 + sx), '#FFFFFF')
    c.move_to(260, 435); c.line_to(260, 705); c.move_to(125, 570); c.line_to(395, 570)
    c.set_source_rgba(*hexc('#8D6E63')); c.set_line_width(10); c.stroke()
    # piso de madera
    c.rectangle(0, FLOOR - 20, SW, SH - FLOOR + 20); c.set_source_rgba(*hexc('#D7A86E')); c.fill()
    for k in range(0, SW, 160):
        c.move_to(k, FLOOR - 20); c.line_to(k, SH); c.set_source_rgba(*hexc('#BC8F5A')); c.set_line_width(4); c.stroke()
    c.rectangle(0, FLOOR - 26, SW, 12); c.set_source_rgba(*hexc('#8D6E63')); c.fill()
    # toallero
    c.rectangle(700, 640, 280, 14); fill(c, hexc('#B0BEC5'), OUT, 4)
    if t < 40.5:
        c.rectangle(740, 652, 160, 230); fill(c, hexc('#F48FB1'), OUT, 5)
        for k in range(6): ellipse(c, 770 + (k % 3) * 50, 700 + (k // 3) * 90, 9, 9); c.set_source_rgba(1, 1, 1, 0.8); c.fill()

def plant(c, t, shake=0.0):
    x = PLANT + shake * 6 * math.sin(t * 25)
    c.move_to(x - 80, FLOOR); c.line_to(x - 95, FLOOR - 170); c.line_to(x + 95, FLOOR - 170); c.line_to(x + 80, FLOOR); c.close_path()
    fill(c, hexc('#FF8A65'), OUT, 6)
    for i, ang in enumerate((-150, -120, -95, -70, -45, -20, -165)):
        c.save(); c.translate(x, FLOOR - 170); c.rotate(math.radians(ang + 4 * math.sin(t * 1.5 + i)))
        L = 300 if i % 2 else 260
        c.move_to(0, 0); c.curve_to(L * 0.3, -L * 0.25, L * 0.8, -L * 0.2, L, 0); c.curve_to(L * 0.8, L * 0.2, L * 0.3, L * 0.25, 0, 0)
        c.close_path(); fill(c, hexc('#43A047' if i % 2 else '#66BB6A'), OUT, 4); c.restore()

def foam_level(t): return ss(11.5, 17.5, t) * (1 - ss(40.5, 44, t))

def tub_back(c, t):
    x, y = TUB
    ellipse(c, x, y, 300, 60); fill(c, hexc('#ECEFF1'), OUT, 6)
    ellipse(c, x, y + 6, 270, 46); c.set_source_rgba(*hexc('#81D4FA')); c.fill()
    # grifo
    c.rectangle(x + 250, y - 160, 30, 150); fill(c, hexc('#B0BEC5'), OUT, 5)
    c.move_to(x + 265, y - 160); c.curve_to(x + 265, y - 200, x + 200, y - 200, x + 200, y - 150)
    c.set_source_rgba(*OUT); c.set_line_width(26); c.stroke()
    c.move_to(x + 265, y - 160); c.curve_to(x + 265, y - 200, x + 200, y - 200, x + 200, y - 150)
    c.set_source_rgba(*hexc('#B0BEC5')); c.set_line_width(16); c.stroke()
    if 11.0 < t < 17.0:  # chorro
        for k in range(10):
            q = (t * 2.0 + k / 10) % 1
            ellipse(c, x + 200 + 4 * math.sin(k), y - 140 + 140 * q, 8, 12); c.set_source_rgba(*hexc('#4FC3F7', 0.9)); c.fill()

def tub_front(c, t):
    x, y = TUB
    f = foam_level(t)
    if f > 0:  # espuma desbordando
        for k in range(11):
            bx = x - 250 + k * 50; r = (30 + 14 * math.sin(k * 1.7 + t)) * f
            ellipse(c, bx, y - 10 * f + 4 * math.sin(t * 2 + k), r, r * 0.8); fill(c, (1, 1, 1, 1), hexc('#B3E5FC'), 3)
    c.move_to(x - 300, y); c.curve_to(x - 300, y + 210, x - 200, y + 230, x, y + 230)
    c.curve_to(x + 200, y + 230, x + 300, y + 210, x + 300, y); c.close_path()
    fill(c, hexc('#FFFFFF'), OUT, 7)
    c.move_to(x - 240, y + 70); c.curve_to(x - 100, y + 110, x + 100, y + 110, x + 240, y + 70)
    c.set_source_rgba(*hexc('#B3E5FC')); c.set_line_width(10); c.stroke()
    for side in (-1, 1):  # patas
        ellipse(c, x + side * 200, y + 240, 34, 22); fill(c, hexc('#FFD54F'), OUT, 5)

def duck(c, x, y, t, s=1.0):
    c.save(); c.translate(x, y + 5 * math.sin(t * 3)); c.rotate(0.08 * math.sin(t * 2.3)); c.scale(s, s)
    ellipse(c, 0, 0, 55, 36); fill(c, hexc('#FFEB3B'), OUT, 5)
    ellipse(c, -40, -42, 30, 30); fill(c, hexc('#FFEB3B'), OUT, 5)
    c.move_to(-68, -40); c.line_to(-92, -32); c.line_to(-68, -26); c.close_path(); fill(c, hexc('#FF9800'), OUT, 4)
    ellipse(c, -46, -48, 6, 7); c.set_source_rgba(*OUT); c.fill()
    c.move_to(10, -5); c.curve_to(30, -25, 50, -15, 40, 5); c.set_source_rgba(*hexc('#FBC02D')); c.set_line_width(5); c.stroke()
    c.restore()

def mud(c, x, y, s, a):
    if a <= 0: return
    for (dx, dy, r) in ((-30, -120, 22), (40, -90, 16), (-10, -60, 18), (55, -300, 15), (-60, -330, 13), (20, -250, 10)):
        ellipse(c, x + dx * s / 0.8, y + dy * s / 0.8, r * s / 0.8, r * 0.8 * s / 0.8); c.set_source_rgba(*hexc('#6D4C41', 0.85 * a)); c.fill()

def foam_hat(c, x, y, k):
    if k <= 0: return
    for (dx, dy, r) in ((-60, 0, 40), (0, -25, 50), (60, 0, 40), (-25, -70, 36), (25, -70, 36), (0, -120, 34)):
        ellipse(c, x + dx * k, y + dy * k, r * k, r * k); fill(c, (1, 1, 1, 1), hexc('#B3E5FC'), 3)

# ---------------- Coco ----------------
def coco_place(t):
    """(x, y_pies, en_bañera)."""
    if t < 8.0: return 760, FLOOR, False
    if t < 9.5: return kf(t, [(8.0, 760), (9.5, PLANT)]), FLOOR, False
    if t < 19.5: return PLANT - 130 * (kf(t, [(14.5, 0), (15.5, 1), (18.5, 1), (19.5, 1.3)]) if t > 14 else 0), FLOOR, False
    if t < JUMP[0]: return PLANT - 170, FLOOR, False
    if t < JUMP[1]:
        q = (t - JUMP[0]) / (JUMP[1] - JUMP[0])
        return PLANT - 170 + (TUB[0] + 10 - PLANT + 170) * q, FLOOR + (TUB[1] + 150 - FLOOR) * q - 380 * math.sin(math.pi * q), q > 0.6
    if t < 40.5: return TUB[0] + 10, TUB[1] + 150 + 8 * math.sin(t * 2.5), True
    if t < 41.7:
        q = ss(40.5, 41.7, t)
        return TUB[0] + 10 + 300 * q, TUB[1] + 150 + (FLOOR - TUB[1] - 150) * q - 200 * math.sin(math.pi * q), q < 0.4
    return kf(t, [(41.7, 850), (43, 700)]), FLOOR, False

def mama_x(t): return kf(t, [(0, -250), (3.5, 200), (24, 200), (26, 260), (40, 260), (43, 400)])

def frame(c, t):
    room(c, t)
    tub_back(c, t)
    cx, cy, in_tub = coco_place(t)
    # Mamá
    mx = mama_x(t)
    m_arm_r, m_arm_l = math.radians(65 + 5 * math.sin(t * 2)), math.radians(115 - 5 * math.sin(t * 2))
    m_look = (1, 0)
    if 3.5 < t < 8: m_arm_r = math.radians(-50 + 20 * math.sin(t * 6))
    if 11 < t < 18: m_arm_r = math.radians(-20); m_look = (1, 0.4)
    if 26 < t < 40: m_arm_r, m_arm_l = math.radians(-30 + 15 * math.sin(t * 4)), math.radians(-10); m_look = (1, 0.2)
    hug = 43.5 < t < 48.5
    if hug: m_arm_r, m_arm_l = math.radians(10), math.radians(170)
    blink = 1.0 if (abs(t - 6) < 0.12 or abs(t - 30) < 0.12) else 0.0
    hidden = 9.5 <= t < 19.5
    peek = kf(t, [(14.5, 0), (15.5, 1), (18.5, 1), (19.5, 0)]) if 14 < t < 19.5 else 0
    if 37 < t < 40.5:  # jarra de agua para enjuagar
        jx, jy = TUB[0] - 80, TUB[1] - 340
        c.save(); c.translate(jx, jy); c.rotate(0.9)
        c.rectangle(-40, -50, 80, 100); fill(c, hexc('#4FC3F7'), OUT, 5); c.restore()
        for k in range(12):
            q = (t * 2 + k / 12) % 1
            ellipse(c, jx + 60 + 30 * math.sin(k), jy + 40 + 140 * q, 7, 11); c.set_source_rgba(*hexc('#81D4FA', 0.9)); c.fill()
    # Coco
    s = 0.8
    mood, look, sad = 'smile', (-0.6, 0), 0.0
    arm_r, arm_l = math.radians(65 + 6 * math.sin(t * 2)), math.radians(115 - 6 * math.sin(t * 2))
    if t < 4: arm_r, arm_l = math.radians(-60 + 25 * math.sin(t * 8)), math.radians(-120)   # jugando
    if 5.5 < t < 9.5: mood, sad = 'sad', 1.0; arm_r, arm_l = math.radians(155), math.radians(25)   # brazos cruzados
    if hidden: mood, sad, look = ('o', 0.0, (-1, 0)) if t > 15.5 else ('sad', 1.0, (-1, 0))
    if 19.5 < t < JUMP[1]: arm_r, arm_l = math.radians(-60), math.radians(-120); mood = 'o'
    if in_tub:
        arm_r, arm_l = math.radians(-60 + 25 * math.sin(t * 6)), math.radians(-120 - 25 * math.sin(t * 6))
        look = (0.5, 0.3)
        if 26 < t < 30: look = (-0.8, -0.6)
        if 37 < t < 40.5: mood = 'closed'
    if hug: mood = 'closed'; arm_r, arm_l = math.radians(170), math.radians(10)
    if t > 48.5: arm_r, arm_l = math.radians(-58 + 25 * math.sin(t * 9)), math.radians(-122 - 25 * math.sin(t * 9))
    dirt = 1 - ss(CLEAN[0], CLEAN[1], t)
    def draw_coco():
        K.put(c, K.coco, cx, cy, s, t=t, mood=mood, sad=sad, look=look, arm_r=arm_r, arm_l=arm_l,
              walk=t * 9 if (8 < t < 9.5 or 41.7 < t < 43) else 0)
        mud(c, cx, cy, s, dirt)
    if in_tub: draw_coco()
    if 14 < t < 44:
        duck(c, TUB[0] - 170 + 30 * math.sin(t * 0.8), TUB[1] - 15, t, 0.9 * ss(14, 15, t))
    tub_front(c, t)
    pass
    K.put(c, K.mama, mx, FLOOR, 0.95, t=t, look=m_look, arm_r=m_arm_r, arm_l=m_arm_l, lid=blink,
          mood='closed' if hug else 'smile', walk=t * 7 if (t < 3.5 or 24 < t < 26 or 40 < t < 43) else 0)
    if not hidden: plant(c, t)
    if not in_tub:
        draw_coco()
        if t > 41.7:
            c.move_to(cx - 95, cy - 280); c.curve_to(cx - 120, cy - 120, cx - 100, cy - 20, cx - 70, cy - 10)
            c.line_to(cx + 70, cy - 10); c.curve_to(cx + 100, cy - 20, cx + 120, cy - 120, cx + 95, cy - 280); c.close_path()
            fill(c, hexc('#F48FB1'), OUT, 5)
            for k in range(6): ellipse(c, cx - 50 + (k % 3) * 50, cy - 220 + (k // 3) * 110, 9, 9); c.set_source_rgba(1, 1, 1, 0.8); c.fill()
    if hidden: plant(c, t, shake=1.0 if 9.4 < t < 10.3 else 0.0)
    if in_tub:
        foam_hat(c, cx, cy - s * 470 - 40, ss(28.5, 30, t) * (1 - ss(37.5, 39, t)))
    # burbujas
    f = foam_level(t)
    if f > 0.2:
        for k in range(8):
            q = (t * 0.22 + k / 8) % 1
            bx = TUB[0] - 250 + (k * 71) % 500 + 40 * math.sin(q * 6 + k); by = TUB[1] - 40 - 900 * q
            soap_bubble(c, bx, by, (18 + (k * 7) % 22) * f, t, 1 - q)
    # salpicón al tirarse
    q = (t - JUMP[1]) / 1.0
    if 0 <= q <= 1:
        for k in range(12):
            a = math.pi * (0.1 + 0.8 * k / 11)
            ellipse(c, TUB[0] + 300 * q * math.cos(a), TUB[1] - 30 - 340 * q * math.sin(a) + 400 * q * q, 13 * (1 - q) + 3, 16 * (1 - q) + 3)
            c.set_source_rgba(*hexc('#81D4FA', 1 - q)); c.fill()
    # limpito y abrazo
    if 41.7 < t < 46:
        for k in range(6):
            ph = (t * 1.0 + k / 6) % 1
            sparkle(c, cx + 150 * math.cos(k + t), cy - 220 + 200 * math.sin(k * 1.3 + t), 22 * math.sin(math.pi * ph))
    if hug:
        for k in range(5):
            ph = ((t - 43.5) * 0.5 + k / 5) % 1
            heart(c, (mx + cx) / 2 + 120 * math.sin(k * 1.7), FLOOR - 520 - 330 * ph, 1.0 + 0.7 * ph, math.sin(math.pi * ph))
    if 27 < t < 36:
        for k in range(3):
            ph = (t * 0.8 + k / 3) % 1
            music_note(c, cx + 100 + 50 * ph, cy - 420 - 160 * ph, math.sin(math.pi * ph), ['#E91E63', '#1E88E5', '#FF9800'][k])
    # globitos
    bubble(c, mx + 30, FLOOR - 0.95 * 480, '¡Coco, a bañarse!', (t - 4.0) / 2.8, 50)
    bubble(c, cx, FLOOR - 0.8 * 480, '¡No quiero!', (t - 6.6) / 2.6, 56)
    bubble(c, mx + 30, FLOOR - 0.95 * 480, '¡Burbujas y un patito!', (t - 14.0) / 3.4, 46)
    bubble(c, cx, FLOOR - 0.8 * 480, '¿Burbujas?', (t - 17.6) / 2.2, 52)
    bubble(c, mx + 40, FLOOR - 0.95 * 480, '¡Sombrero de espuma!', (t - 29.0) / 3.0, 46)
    bubble(c, cx, FLOOR - 0.8 * 480 - 60, '¡Qué rico olor!', (t - 42.0) / 2.4, 50)
    bubble(c, cx, FLOOR - 0.8 * 480 - 60, '¡Gracias, mamá!', (t - 45.0) / 3.0, 50)
    overlay(c, t)

LOGO = cairo.ImageSurface.create_from_png(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'imagenes', 'logo_perfil.png'))

def overlay(c, t):
    tops = [(0.0, '¡Hora del baño!', None), (5.5, '¡Coco no se quiere', 'bañar!'), (11.0, 'Mamá tiene', 'una idea…'),
            (20.5, '¡Al agua!', None), (28.0, '¡A jugar con', 'la espuma!'), (41.0, '¡Limpito y', 'perfumado!'), (48.5, '¡Bañarse es', 'divertido!')]
    for i, (t0, a, b) in enumerate(tops):
        t1 = tops[i + 1][0] if i + 1 < len(tops) else DUR + 1
        if t0 <= t < t1:
            sc = K_back((t - t0) / 0.45) * (1 - ss(t1 - 0.25, t1, t))
            if b is None: word(c, a, SW / 2, 230, 120 * sc + 0.01, tilt=0.05, outline=10)
            else:
                word(c, a, SW / 2, 170, 95 * sc + 0.01, tilt=0.05, outline=8)
                word(c, b, SW / 2, 290, 100 * sc + 0.01, start=3, tilt=0.05, outline=8)
    if t > 48.5:
        d = 170; cy = 1770
        c.save(); c.arc(170, cy, d / 2, 0, 2 * math.pi); c.clip()
        c.translate(170 - d / 2, cy - d / 2); c.scale(d / LOGO.get_width(), d / LOGO.get_height())
        c.set_source_surface(LOGO, 0, 0); c.paint(); c.restore()
        c.arc(170, cy, d / 2, 0, 2 * math.pi); c.set_source_rgba(1, 1, 1, 1); c.set_line_width(8); c.stroke()
        word(c, 'Cuentos mágicos', 620, cy - 15, 62, outline=6); word(c, 'de la selva', 620, cy + 60, 62, start=5, outline=6)
    a = max(1 - ss(0, 0.4, t), ss(DUR - 1.2, DUR, t))
    if a > 0: c.set_source_rgba(1, 1, 1, a); c.paint()

if __name__ == '__main__':
    args = sys.argv[1:]
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, SW, SH); c = cairo.Context(surf)
    if args and args[0] == 'stills':
        for t in map(float, args[1:]):
            c.save(); frame(c, t); c.restore(); surf.write_to_png(f'bano_{t}.png')
    elif args and args[0] == 'portada':
        c.save(); frame(c, 31.0); c.restore(); surf.write_to_png('short_bano_portada.png')
    else:
        a0, a1 = (float(args[1]), float(args[2])) if len(args) > 2 else (0, DUR)
        out = sys.stdout.buffer
        for i in range(int(round(a0 * FPS)), int(round(a1 * FPS))):
            c.save(); frame(c, i / FPS); c.restore(); surf.flush(); out.write(surf.get_data())
