"""Short — ¡Coco no quiere comer verdura! (vertical, 40 s, plantilla nueva: gancho en el cuadro 1 + tarjeta final).
Papá Coco arma una carita con las verduras en el plato y Coco se la come toda.
Uso: python3 short_verdura.py [short a b] | stills 0 12 | portada"""
import cairo, math, sys
import cuerpos as K
from amigos import hexc, ellipse, fill, OUT
from logos import word, sparkle
from ep02_puente_del_rio import kf, ss, K_back
from ep03_donde_esta_tomi import bubble
from short_kit import SW, SH, FPS, END, top_title, end_card, logo_band

STORY = 37.0
DUR = STORY + END
TABLE_Y = 1240
PLATE = (600, 1215)

def kitchen(c, t):
    c.set_source_rgba(*hexc('#FFF3E0')); c.paint()
    for k in range(0, SW, 120):            # papel de pared a rayas
        c.rectangle(k, 0, 60, TABLE_Y); c.set_source_rgba(*hexc('#FFE0B2')); c.fill()
    c.rectangle(130, 430, 320, 280); fill(c, hexc('#8D6E63'), OUT, 6)       # ventana
    c.rectangle(145, 445, 290, 250); c.set_source_rgba(*hexc('#81D4FA')); c.fill()
    ellipse(c, 360, 520, 40, 40); fill(c, hexc('#FFEB3B'), hexc('#F9A825'), 4)
    c.move_to(290, 445); c.line_to(290, 695); c.set_source_rgba(*hexc('#8D6E63')); c.set_line_width(10); c.stroke()
    for (x, col) in ((640, '#E57373'), (760, '#64B5F6'), (880, '#81C784')):   # frascos
        c.rectangle(x - 40, 560, 80, 110); fill(c, hexc(col), OUT, 5)
        c.rectangle(x - 46, 540, 92, 26); fill(c, hexc('#A1887F'), OUT, 4)
    c.rectangle(580, 670, 380, 18); fill(c, hexc('#8D6E63'), OUT, 4)
    c.rectangle(0, 1500, SW, SH - 1500); c.set_source_rgba(*hexc('#BCAAA4')); c.fill()

def table(c):
    c.rectangle(60, TABLE_Y, SW - 120, 46); fill(c, hexc('#A1887F'), OUT, 7)
    for x in (140, SW - 140):
        c.rectangle(x - 20, TABLE_Y + 46, 40, 330); fill(c, hexc('#8D6E63'), OUT, 6)
    c.rectangle(60, TABLE_Y + 46, SW - 120, 18); c.set_source_rgba(*hexc('#E57373')); c.fill()     # mantel
    for k in range(12): ellipse(c, 100 + k * 80, TABLE_Y + 55, 8, 8); c.set_source_rgba(1, 1, 1, 1); c.fill()

def broccoli(c, x, y, s):
    c.rectangle(x - 9 * s, y, 18 * s, 34 * s); fill(c, hexc('#AED581'), OUT, 3)
    for (dx, dy, r) in ((-16, -4, 17), (16, -4, 17), (0, -18, 20), (0, 2, 16)):
        ellipse(c, x + dx * s, y + dy * s, r * s, r * s); fill(c, hexc('#43A047'), OUT, 3)

def carrot_slice(c, x, y, s):
    ellipse(c, x, y, 18 * s, 18 * s); fill(c, hexc('#FF9800'), OUT, 3)
    ellipse(c, x, y, 8 * s, 8 * s); c.set_source_rgba(*hexc('#FFB74D')); c.fill()

def carrot_stick(c, x, y, s, rot=0.0):
    c.save(); c.translate(x, y); c.rotate(rot)
    c.move_to(-60 * s, -9 * s); c.curve_to(-20 * s, -14 * s, 20 * s, -14 * s, 60 * s, -4 * s); c.line_to(60 * s, 4 * s)
    c.curve_to(20 * s, 14 * s, -20 * s, 14 * s, -60 * s, 9 * s); c.close_path(); fill(c, hexc('#FF9800'), OUT, 3)
    c.restore()

def pea(c, x, y, s): ellipse(c, x, y, 11 * s, 11 * s); fill(c, hexc('#8BC34A'), OUT, 3)

# piezas: (tipo, pila_x, pila_y, carita_x, carita_y, t_armado, t_comida)
PIECES = [('b', -60, -10, -70, -50, 11.0, 22.0), ('b', -10, -20, -25, -66, 11.6, 23.4), ('b', 40, -10, 25, -66, 12.2, 24.8),
          ('b', 75, -5, 70, -50, 12.8, 26.2), ('c', -40, 10, -36, -8, 13.6, 27.6), ('c', 20, 12, 36, -8, 14.2, 29.0),
          ('p', 50, 15, 0, 10, 14.8, 30.0), ('s', 0, 18, 0, 38, 15.5, 31.0)]

def plate(c, t):
    x, y = PLATE
    ellipse(c, x, y, 230, 60); fill(c, (1, 1, 1, 1), OUT, 6)
    ellipse(c, x, y - 6, 180, 44); c.set_source_rgba(*hexc('#E3F2FD')); c.fill()
    for (kind, px, py, fx, fy, ta, te) in PIECES:
        if t >= te: continue
        q = ss(ta, ta + 0.6, t)
        dx, dy = px + (fx - px) * q, (py + (fy - py) * q) * (0.5 + 0.9 * q) - 40 * math.sin(math.pi * q)
        X, Y = x + dx * 1.9, y + dy - 20 * q
        if kind == 'b': broccoli(c, X, Y - 18, 1.5)
        elif kind == 'c': carrot_slice(c, X, Y, 1.5)
        elif kind == 'p': pea(c, X, Y, 1.5)
        elif q < 0.5: carrot_stick(c, X, Y, 1.3, 0.5)
        else:
            c.arc(X, Y - 40, 60, 0.2 * math.pi, 0.8 * math.pi); c.set_source_rgba(*OUT); c.set_line_width(24); c.stroke()
            c.arc(X, Y - 40, 60, 0.2 * math.pi, 0.8 * math.pi); c.set_source_rgba(*hexc('#FF9800')); c.set_line_width(16); c.stroke()

def frame(c, t):
    if t >= STORY:
        end_card(c, t - STORY); return
    kitchen(c, t)
    # Papá (atrás, a la derecha de la mesa)
    px = kf(t, [(0, 1250), (5.5, 1250), (7.5, 840)])
    pa_r, pa_l = math.radians(65), math.radians(115)
    if 8 < t < 10: pa_r = math.radians(-70)                                # ¡idea!
    if 10.5 < t < 16.5: pa_r, pa_l = math.radians(150 + 15 * math.sin(t * 8)), math.radians(30)   # arma la carita
    if 33 < t < 37: pa_r = math.radians(-60 + 20 * math.sin(t * 8))
    K.put(c, K.papa, px, TABLE_Y + 30, 0.85, t=t, look=(-0.8, 0.5) if t > 10 else (-1, 0), arm_r=pa_r, arm_l=pa_l,
          walk=t * 8 if 5.5 < t < 7.5 else 0)
    # Coco (sentado del otro lado de la mesa: lo tapa la mesa)
    eat = 21.5 < t < 31.5
    mood, sad, look = 'smile', 0.0, (0.5, 0.6)
    ar, al = math.radians(65), math.radians(115)
    if t < 8: mood, sad, ar, al, look = 'sad', 1.0, math.radians(155), math.radians(25), (-0.3, 0)    # brazos cruzados
    if 8 <= t < 17: mood, sad, look = 'closed', 0.6, (0.6, 0.4)
    if 17 <= t < 21.5: mood, look = 'o' if t < 18.5 else 'smile', (0.3, 0.8)
    if eat:
        mood = 'chew' if (t % 1.4) > 0.5 else 'o'
        ar = math.radians(-20 - 70 * abs(math.sin(math.pi * (t - 21.5) / 1.4)))
    if 31.5 < t < 37: ar, al = math.radians(-35), math.radians(-145)       # "¡fuerte!"
    bob = -20 * abs(math.sin(t * 4.5)) if 31.5 < t < 37 else 0
    K.put(c, K.coco, 330, TABLE_Y + 150 + bob, 0.9, t=t, mood=mood, sad=sad, look=look, arm_r=ar, arm_l=al, chew=t, arm_len=125 if eat else 115)
    if t < 6.0:   # sacudida de enojo y plato empujado
        pass
    table(c)
    plate(c, t)
    if eat:  # tenedor con un pedacito que va a la boca
        q = abs(math.sin(math.pi * (t - 21.5) / 1.4))
        fx, fy = 420 + (360 - 420) * q, 1180 - 180 * q
        c.move_to(fx + 70, fy + 60); c.line_to(fx, fy); c.set_source_rgba(*hexc('#90A4AE')); c.set_line_width(10); c.stroke()
        broccoli(c, fx, fy - 10, 0.6) if int((t - 21.5) / 1.4) % 2 == 0 else carrot_slice(c, fx, fy, 0.8)
    if 9.0 < t < 10.4:   # lamparita
        q = K_back((t - 9.0) / 0.3)
        cx, cy = px, TABLE_Y - 520
        ellipse(c, cx, cy, 40 * q, 44 * q); fill(c, hexc('#FFF176'), OUT, 5)
        for i in range(8):
            a = i * math.pi / 4 + t
            c.move_to(cx + 60 * q * math.cos(a), cy + 60 * q * math.sin(a)); c.line_to(cx + 85 * q * math.cos(a), cy + 85 * q * math.sin(a))
            c.set_source_rgba(*hexc('#FFD600')); c.set_line_width(7); c.stroke()
    if 31.5 < t < 37:
        for k in range(8):
            ph = (t * 0.9 + k / 8) % 1
            sparkle(c, 330 + 220 * math.cos(k + t), TABLE_Y - 250 + 200 * math.sin(k * 1.3 + t), 24 * math.sin(math.pi * ph))
    # globitos
    if t < 6.5: bubble(c, 330, TABLE_Y - 330, '¡NO QUIERO!', min(0.84, 0.3 + t / 8) if t < 6.0 else 0.84 + (t - 6.0) / 0.5 * 0.16, 64)
    bubble(c, px, TABLE_Y - 420, '¡Tengo una idea!', (t - 7.6) / 2.8, 50)
    bubble(c, 330, TABLE_Y - 330, '¡Una carita!', (t - 17.2) / 2.8, 56)
    bubble(c, 330, TABLE_Y - 330, '¡Mmm, qué rico!', (t - 27.5) / 3.0, 54)
    bubble(c, 330, TABLE_Y - 330, '¡Soy fuerte!', (t - 32.0) / 2.6, 56)
    # textos de arriba (el primero está desde el cuadro 1)
    if t < 8: top_title(c, t, 0, '¡Coco no quiere', 'comer verdura!', first=True)
    elif t < 17: top_title(c, t, 8, 'Papá tiene', 'una idea…')
    elif t < 31.5: top_title(c, t, 17, '¡Una carita', 'de verduras!')
    else: top_title(c, t, 31.5, '¡Comer verdura', 'es divertido!')
    logo_band(c)

if __name__ == '__main__':
    args = sys.argv[1:]
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, SW, SH); c = cairo.Context(surf)
    if args and args[0] == 'stills':
        for t in map(float, args[1:]):
            c.save(); frame(c, t); c.restore(); surf.write_to_png(f'verdura_{t}.png')
    elif args and args[0] == 'portada':
        c.save(); frame(c, 18.0); c.restore(); surf.write_to_png('short_verdura_portada.png')
    else:
        a0, a1 = (float(args[1]), float(args[2])) if len(args) > 2 else (0, DUR)
        out = sys.stdout.buffer
        for i in range(int(round(a0 * FPS)), int(round(a1 * FPS))):
            c.save(); frame(c, i / FPS); c.restore(); surf.flush(); out.write(surf.get_data())
