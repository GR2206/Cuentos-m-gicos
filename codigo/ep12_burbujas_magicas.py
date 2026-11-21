"""Episodio 12 — Las burbujas mágicas (aventurita, 110 s, pensada para voz en off).
Coco encuentra una flor que hace burbujas mágicas. Cada burbuja hace un truco:
Tito queda rosado, Pipa azul, a Tomi le salen alitas, Lola cambia de colores
y una burbuja gigante se lleva a Coco por el aire. La última burbuja deja todo como antes.

      python3 ep12_burbujas_magicas.py srt 5.5     -> subtítulos .srt de la narración
Uso:  python3 ep12_burbujas_magicas.py              -> cuadros crudos por stdout
      python3 ep12_burbujas_magicas.py range 0 55   -> solo un tramo
      python3 ep12_burbujas_magicas.py stills 12 65 -> PNG sueltos"""
import cairo, math, sys
import cuerpos as K
from amigos import hexc, ellipse, fill, OUT
from logos import word, sparkle
from ep02_puente_del_rio import kf, ss, moving, K_back, music_note
from ep03_donde_esta_tomi import bubble as speech
from ep09_semilla_magica import SKY, LAND, sun, cloud, srt

W, H, FPS = 1920, 1080, 30
DUR = 110.0
GROUND = 880
FLOWER = (1580, GROUND)
PIPA_X, TITO_X, TOMI_X = 330, 640, 1150
RESTORE = 86.0

NARRACION = [
    (6.0, 10.5, 'Un día, Coco encontró una flor muy especial.'),
    (11.5, 16.0, '¡Cuando la soplaba, hacía burbujas mágicas!'),
    (18.0, 23.5, 'La primera burbuja voló hasta Tito y... ¡plop! ¡Tito se puso rosado!'),
    (28.0, 33.5, 'La segunda llegó a Pipa y... ¡plop! ¡Pipa se puso azul!'),
    (38.0, 44.5, 'Con la tercera, a Tomi le salieron alitas... ¡y voló!'),
    (50.0, 55.5, 'Y Lola... ¡cambió de todos los colores!'),
    (60.0, 66.0, 'Entonces salió una burbuja gigante... ¡y se llevó a Coco por el aire!'),
    (70.5, 76.0, 'Lola voló, la pinchó con el pico, y...'),
    (77.0, 82.0, 'Coco bajó suavecito, como una plumita.'),
    (84.5, 90.0, 'La última burbuja hizo que todo volviera a ser como antes.'),
    (93.0, 99.0, 'Y Coco compartió su flor para que todos hicieran burbujas.'),
    (103.0, 108.0, 'Compartir... ¡es lo más mágico de todo!'),
]

# ---------------- burbujas ----------------
RAINBOW = ['#F44336', '#FF9800', '#FFEB3B', '#4CAF50', '#2196F3', '#9C27B0']
def soap_bubble(c, x, y, r, t, a=1.0):
    if r <= 1: return
    c.save()
    g = cairo.RadialGradient(x - r * 0.3, y - r * 0.3, r * 0.1, x, y, r)
    g.add_color_stop_rgba(0, 1, 1, 1, 0.05 * a); g.add_color_stop_rgba(0.8, 0.8, 0.95, 1, 0.12 * a); g.add_color_stop_rgba(1, 1, 1, 1, 0.35 * a)
    c.set_source(g); c.arc(x, y, r, 0, 2 * math.pi); c.fill()
    for k, col in enumerate(RAINBOW):
        a0 = t * 0.8 + k * math.pi / 3
        c.set_source_rgba(*hexc(col, 0.55 * a)); c.set_line_width(max(2, r * 0.06))
        c.arc(x, y, r * 0.96, a0, a0 + math.pi / 3); c.stroke()
    c.set_source_rgba(1, 1, 1, 0.9 * a); c.set_line_width(max(2, r * 0.05))
    c.arc(x, y, r * 0.7, math.pi * 1.1, math.pi * 1.45); c.stroke()
    ellipse(c, x - r * 0.45, y - r * 0.45, r * 0.12, r * 0.08); c.set_source_rgba(1, 1, 1, 0.9 * a); c.fill()
    c.restore()

def pop(c, x, y, t, t0, col='#FFFFFF'):
    q = (t - t0) / 0.9
    if not 0 <= q <= 1: return
    for k in range(10):
        a = k * math.pi / 5
        sparkle(c, x + 150 * q * math.cos(a), y + 120 * q * math.sin(a), 26 * math.sin(math.pi * q), RAINBOW[k % 6] if k % 2 else col)
    word(c, '¡plop!', x, y - 90 - 40 * q, 60 * K_back(q / 0.3) + 0.01, outline=6)

def head_of(name, t):
    if name == 'tito': return TITO_X, GROUND - 0.6 * 340
    if name == 'pipa': return PIPA_X, GROUND - 0.55 * 560
    if name == 'tomi': return TOMI_X, GROUND - 0.55 * 150
    if name == 'lola': lx, ly = lola_pos(t); return lx, ly - 0.5 * 230
    return 0, 0

MAGIC = [(17.0, 'tito'), (27.0, 'pipa'), (37.0, 'tomi'), (49.0, 'lola')]
TRAVEL = 4.0
def flower_mouth(): return FLOWER[0], FLOWER[1] - 190

def magic_bubble(c, t, t0, who):
    q = (t - t0) / TRAVEL
    if not 0 <= q < 1: return
    x0, y0 = flower_mouth(); x1, y1 = head_of(who, t)
    x = x0 + (x1 - x0) * q + 40 * math.sin(q * 9); y = y0 + (y1 - y0) * q - 160 * math.sin(math.pi * q)
    soap_bubble(c, x, y, 34 + 20 * min(1, q * 3), t)

def popped(who, t):
    for (t0, w) in MAGIC:
        if w == who: return t >= t0 + TRAVEL and t < RESTORE
    return False

def magic_k(who, t):
    for (t0, w) in MAGIC:
        if w == who: return ss(t0 + TRAVEL, t0 + TRAVEL + 0.6, t) * (1 - ss(RESTORE, RESTORE + 0.8, t))
    return 0.0

def tinted(c, draw, rgb, k):
    if k <= 0.01: draw(); return
    c.push_group(); draw(); pat = c.pop_group()
    c.push_group()
    c.set_source(pat); c.paint()
    c.set_operator(cairo.OPERATOR_HSL_HUE); c.set_source_rgba(*rgb, k); c.mask(pat)
    c.set_operator(cairo.OPERATOR_HSL_SATURATION); c.set_source_rgba(*rgb, k * 0.6); c.mask(pat)
    c.set_operator(cairo.OPERATOR_DEST_IN); c.set_source(pat); c.paint()   # pixman deja color con alfa 0: limpiar
    c.set_operator(cairo.OPERATOR_OVER)
    c.pop_group_to_source(); c.paint()

def hsv(h):
    import colorsys
    return colorsys.hsv_to_rgb(h % 1.0, 0.85, 1.0)

# ---------------- flor ----------------
def magic_flower(c, t, blow=0.0):
    x, y = FLOWER
    c.set_line_width(14); c.set_source_rgba(*hexc('#2E7D32')); c.set_line_cap(cairo.LINE_CAP_ROUND)
    c.move_to(x, y); c.curve_to(x - 20, y - 80, x + 20, y - 120, x, y - 160); c.stroke()
    for side in (-1, 1):
        c.save(); c.translate(x, y - 60); c.rotate(side * 0.7 + 0.1 * math.sin(t * 2))
        ellipse(c, side * 40, 0, 45, 18); fill(c, hexc('#43A047'), OUT, 4); c.restore()
    c.save(); c.translate(x, y - 190); c.rotate(0.1 * math.sin(t * 1.5)); s = 1 + 0.06 * blow
    c.scale(s, s)
    for i in range(8):
        a = i * math.pi / 4
        ellipse(c, 55 * math.cos(a), 55 * math.sin(a), 38, 38); fill(c, hexc(['#F06292', '#BA68C8'][i % 2]), OUT, 4)
    ellipse(c, 0, 0, 40, 40); fill(c, hexc('#FFF59D'), OUT, 4)
    ellipse(c, 0, 0, 24, 24); c.set_source_rgba(*hexc('#B3E5FC', 0.8)); c.fill()
    c.restore()
    for k in range(3):
        ph = (t * 0.7 + k / 3) % 1
        sparkle(c, x + 80 * math.cos(k * 2.1 + t), y - 190 + 70 * math.sin(k * 2.1 + t), 14 * math.sin(math.pi * ph))

# ---------------- posiciones ----------------
COCO_X = [(0, 900), (6, 900), (9.5, 1380), (59, 1380), (60.5, 1380), (72, 920), (92, 920), (94, 1380), (110, 1380)]
def coco_float(t):
    """Altura extra de Coco cuando lo lleva la burbuja gigante."""
    if t < 60: return 0.0
    if t < 75.6: return 330 * ss(60, 64, t) + 20 * math.sin(t * 2)
    if t < 81: return (330 + 20 * math.sin(75.6 * 2)) * (1 - ss(75.6, 81, t))
    return 0.0

def lola_pos(t):
    x = kf(t, [(0, 1250), (72, 1250), (74.5, 1000), (75.7, 960), (77.5, 1250)]) + 30 * math.sin(t * 0.6)
    y = kf(t, [(0, 470), (72, 470), (74.5, 300), (75.7, 330), (77.5, 470)]) + 15 * math.sin(t * 3)
    return x, y

def tomi_fly(t):
    return 170 * ss(42, 43.5, t) * (1 - ss(46.5, 48, t)) + (12 * math.sin(t * 4) if 43.5 < t < 46.5 else 0)

BLOWS = [m[0] - 0.8 for m in MAGIC] + [12.0, 13.2, 59.2, 84.0, 95.5, 97.0, 98.5]
def coco_blow(t):
    for b in BLOWS:
        if b <= t < b + 0.8: return math.sin(math.pi * (t - b) / 0.8)
    return 0.0

def party(t): return t < 1.2 or (23.5 < t < 25.5) or (33.5 < t < 35.5) or (101.5 < t < 108)

def world(c, t):
    c.set_source_surface(SKY, 0, 0); c.paint()
    sun(c, t)
    for (x0, y0, s, sp) in ((150, 160, 0.9, 10), (700, 110, 0.7, 7)):
        cloud(c, (x0 + sp * t) % 2300 - 250, y0, s)
    c.set_source_surface(LAND, 0, 0); c.paint()
    blow = coco_blow(t)
    magic_flower(c, t, blow)
    bounce = lambda ph: -25 * abs(math.sin(t * 4.5 + ph)) if party(t) else 0
    look_coco = lambda x, y: (max(-1, min(1, (kf(t, COCO_X) - x) / 300)), max(-1, min(1, (GROUND - 300 - coco_float(t) - y) / 250)))
    # Pipa
    neck = kf(t, [(66, 300), (68, 560), (78, 560), (80, 300)])
    pl = look_coco(PIPA_X, GROUND - 0.55 * 560) if 60 < t < 82 else (1, 0)
    tinted(c, lambda: K.put(c, K.pipa, PIPA_X, GROUND + bounce(0.5), 0.55, t=t, neck=neck, look=pl),
           (0.26, 0.62, 0.96), magic_k('pipa', t))
    # Tito
    tl = look_coco(TITO_X, GROUND - 200) if 60 < t < 82 else (1, 0)
    tinted(c, lambda: K.put(c, K.tito, TITO_X, GROUND + bounce(1.0), 0.6, t=t, look=tl),
           (1.0, 0.43, 0.78), magic_k('tito', t))
    # Tomi (with little wings)
    def draw_tomi():
        k = magic_k('tomi', t)
        ty = GROUND + bounce(1.5) - tomi_fly(t)
        if k > 0.01:
            flap = math.sin(t * 22) if 42 < t < 48 else 0.3 * math.sin(t * 4)
            for side in (-1, 1):
                c.save(); c.translate(TOMI_X + side * 70, ty - 0.55 * 120); c.rotate(side * (-0.5 - 0.5 * flap)); c.scale(side * k, k)
                c.move_to(0, 0); c.curve_to(40, -70, 130, -60, 120, 0); c.curve_to(90, 20, 40, 20, 0, 0); c.close_path()
                fill(c, (1, 1, 1, 0.95), OUT, 4)
                for j in range(2):
                    c.move_to(30 + j * 35, -5); c.curve_to(45 + j * 35, -30, 55 + j * 35, -30, 70 + j * 35, -10)
                    c.set_source_rgba(*hexc('#B3E5FC')); c.set_line_width(4); c.stroke()
                c.restore()
        K.put(c, K.tomi, TOMI_X, ty, 0.55, t=t, look=look_coco(TOMI_X, GROUND - 100) if 60 < t < 82 else (1, -0.3 if 42 < t < 48 else 0))
        if tomi_fly(t) > 20:
            ellipse(c, TOMI_X, GROUND + 5, 100 * (1 - tomi_fly(t) / 400), 12); c.set_source_rgba(0, 0.2, 0, 0.25); c.fill()
    draw_tomi()
    # Coco
    cx = kf(t, COCO_X); fl = coco_float(t)
    mood, look = 'smile', (1, -0.3)
    arm_r, arm_l = math.radians(65 + 6 * math.sin(t * 2)), math.radians(115 - 6 * math.sin(t * 2))
    if party(t): arm_r, arm_l = math.radians(-58 + 25 * math.sin(t * 9)), math.radians(-122 - 25 * math.sin(t * 9))
    if blow > 0: mood = 'o'; arm_r, arm_l = math.radians(-20), math.radians(-160); look = (1, -0.4)
    for (t0, who) in MAGIC:
        if t0 < t < t0 + TRAVEL:
            hx, hy = head_of(who, t); look = (max(-1, min(1, (hx - cx) / 300)), -0.4)
    if 60 < t < 75.6:
        mood = 'o' if t < 66 else 'smile'; arm_r, arm_l = math.radians(-50 + 20 * math.sin(t * 3)), math.radians(-130 - 20 * math.sin(t * 3))
        look = (math.sin(t * 1.3), 0.5)
    if 75.6 < t < 81: arm_r, arm_l = math.radians(-80 + 30 * math.sin(t * 6)), math.radians(-100 - 30 * math.sin(t * 6)); mood = 'o'
    if 93 < t < 100: look = (-1, 0)
    blink = 0.0
    for bt in (3.0, 16.0, 31.0, 46.0, 57.0, 69.0, 89.0, 100.0):
        if abs(t - bt) < 0.12: blink = 1 - abs(t - bt) / 0.12
    K.put(c, K.coco, cx, GROUND + bounce(0) - fl, 0.55, t=t, mood=mood, look=look, lid=blink, arm_r=arm_r, arm_l=arm_l,
          walk=t * 8 if moving(t, COCO_X) and fl == 0 else 0)
    if 59.8 < t < 75.6:  # the giant bubble around Coco
        r = 200 * K_back((t - 59.8) / 0.8)
        soap_bubble(c, cx, GROUND - 150 - fl, r, t)
    if fl > 0 and t > 75.6:  # floating like a feather: little sparkles
        for k in range(3):
            ph = (t * 1.2 + k / 3) % 1
            sparkle(c, cx + 120 * math.sin(k * 2 + t * 2), GROUND - 150 - fl + 80 * math.cos(k * 2 + t * 2), 16 * math.sin(math.pi * ph))
    # Lola (rainbow when magic)
    lx, ly = lola_pos(t)
    k = magic_k('lola', t)
    def draw_lola():
        K.put(c, K.lola, lx, ly + bounce(2.0), 0.5, t=t, flap=20, look=look_coco(lx, ly) if 60 < t < 82 else (-0.3, 0.3))
    tinted(c, draw_lola, hsv(t * 0.35), k)
    if 101.5 < t < 108:
        for j in range(3):
            ph = (t * 0.7 + j / 3) % 1
            music_note(c, lx + 40 + 60 * ph, ly - 150 - 160 * ph, math.sin(math.pi * ph), ['#E91E63', '#1E88E5', '#FF9800'][j])
    # bubbles in flight and pops
    for (t0, who) in MAGIC:
        magic_bubble(c, t, t0, who)
        hx, hy = head_of(who, t0 + TRAVEL)
        pop(c, hx, hy, t, t0 + TRAVEL)
    pop(c, 920, GROUND - 150 - 330, t, 75.6)
    # free play bubbles at the start and the end
    for (a, b) in ((12.0, 16.5), (93.0, 110.0)):
        if a < t < b:
            for j in range(10):
                q = ((t - a) * 0.25 + j / 10) % 1
                bx = FLOWER[0] - 900 * q + 60 * math.sin(q * 8 + j); by = FLOWER[1] - 190 - 500 * q - 40 * math.sin(j)
                soap_bubble(c, bx, by, 18 + 22 * ((j * 7) % 5) / 5, t, 1 - q)
    # the restoring rainbow bubble
    if 84.0 < t < RESTORE + 1.2:
        if t < RESTORE:
            q = (t - 84.0) / (RESTORE - 84.0)
            x0, y0 = flower_mouth()
            soap_bubble(c, x0 + (900 - x0) * q, y0 + (380 - y0) * q, 40 + 90 * q, t)
        else:
            q = (t - RESTORE) / 1.2
            for j in range(16):
                a = j * math.pi / 8
                sparkle(c, 900 + 700 * q * math.cos(a), 380 + 420 * q * math.sin(a), 30 * math.sin(math.pi * q), RAINBOW[j % 6])
    # speech
    speech(c, cx, GROUND - 300, '¡Una flor mágica!', (t - 9.8) / 2.4, 46)
    speech(c, TITO_X, GROUND - 0.6 * 470, '¡Estoy rosado!', (t - 21.6) / 2.6, 46)
    speech(c, PIPA_X + 40, GROUND - 0.55 * 700, '¡Estoy azul!', (t - 31.6) / 2.6, 46)
    speech(c, TOMI_X, GROUND - 260 - tomi_fly(t), '¡Estoy volando!', (t - 43.6) / 3.0, 46)
    speech(c, cx, GROUND - 300 - coco_float(t) - 120, '¡Ayuda!', (t - 65.0) / 3.0, 52)
    speech(c, cx, GROUND - 300, '¡Para todos!', (t - 93.3) / 2.8, 52)

def overlay(c, t):
    if t < 5.6:
        a = 1 - ss(4.8, 5.5, t)
        c.push_group(); word(c, 'Las burbujas mágicas', W / 2, 230, 115 * K_back((t - 0.6) / 0.6) + 0.01, tilt=0.05, outline=9)
        c.pop_group_to_source(); c.paint_with_alpha(a)
    if t > 102:
        s = K_back((t - 102) / 0.7)
        word(c, '¡Compartir es', W / 2, 180, 115 * s + 0.01, tilt=0.06, outline=10)
        word(c, 'lo más mágico!', W / 2, 320, 115 * s + 0.01, start=3, tilt=0.06, outline=10)
    a = max(1 - ss(0, 0.8, t), ss(DUR - 2.0, DUR, t))
    if a > 0: c.set_source_rgba(1, 1, 1, a); c.paint()

FOCUS = [(17.0, 900, 620), (27.0, 700, 600), (37.0, 1150, 620), (49.0, 1250, 560)]
def camera(t):
    z, x, y = 1.0, 960.0, 540.0
    for (t0, fx, fy) in FOCUS:
        w = ss(t0 + TRAVEL - 1.2, t0 + TRAVEL, t) * (1 - ss(t0 + TRAVEL + 3.5, t0 + TRAVEL + 4.8, t))
        z += 0.25 * w; x += (fx - 960) * w; y += (fy - 540) * w
    w = ss(6, 8, t) * (1 - ss(15, 16.5, t)); z += 0.25 * w; x += (1350 - 960) * w; y += (620 - 540) * w
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
            c.save(); frame(c, t); c.restore(); surf.write_to_png(f'ep12_{t}.png')
    else:
        t0, t1 = (float(args[1]), float(args[2])) if args and args[0] == 'range' else (0, DUR)
        out = sys.stdout.buffer
        for i in range(int(round(t0 * FPS)), int(round(t1 * FPS))):
            c.save(); frame(c, i / FPS); c.restore(); surf.flush(); out.write(surf.get_data())
