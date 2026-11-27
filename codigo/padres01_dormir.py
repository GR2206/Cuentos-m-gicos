"""Para papás 01 — 5 claves para que tus hijos se duerman sin pelear (95 s).
Video PARA ADULTOS (todo público, no "para niños"): habla a los padres, estilo infografía cálida,
sin personajes protagonistas (Coco aparece solo como logo del canal). Consejos basados en la AAP
(healthychildren.org), KidsHealth y Child Mind Institute.

Uso:  python3 padres01_dormir.py [range a b] | stills 3 20 | miniatura | srt 5.5"""
import cairo, math, sys, os
from amigos import hexc, ellipse, fill, OUT
from logos import sparkle
from ep02_puente_del_rio import kf, ss, K_back
from ep09_semilla_magica import srt

W, H, FPS = 1920, 1080, 30
DUR = 95.0
INK = hexc('#1F2440'); CREAM = hexc('#FBF5EA'); SAND = hexc('#F1E4CC')
ACC = ['#5C6BC0', '#26A69A', '#EF8A4F', '#8E7CC3', '#E0607E']
LOGO = cairo.ImageSurface.create_from_png(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'imagenes', 'logo_perfil.png'))

TIPS = [
    ('Mismo horario,\ntodos los días', 'Acostarse y levantarse a la misma hora\nordena el reloj interno del cuerpo.', 'clock'),
    ('Pantallas apagadas\n1 hora antes', 'La luz de celulares y tablets\nles quita el sueño. Mejor fuera del cuarto.', 'phone'),
    ('La misma rutina,\nen el mismo orden', 'Baño, dientes, cuento y a la cama.\nRepetirla les avisa que llega la hora.', 'book'),
    ('Cuarto oscuro,\nfresco y tranquilo', 'Luces bajas, nada de juguetes que entusiasmen.\nLa cama es para dormir.', 'moon'),
    ('Calma antes\nde acostarse', 'Juegos movidos, no. Y resolvé antes\nel agua, el baño y la lucecita.', 'cup'),
]
T0, TL = 7.0, 14.0
def tip_at(t):
    k = int((t - T0) // TL)
    return k if 0 <= k < 5 else None

NARRACION = [
    (0.6, 6.5, '¿A tu hijo le cuesta dormirse? Estas son cinco claves que recomiendan los pediatras.'),
    (7.5, 19.5, 'Uno: mismo horario, todos los días. Acostarse y levantarse a la misma hora ordena el reloj interno del cuerpo.'),
    (21.5, 33.5, 'Dos: pantallas apagadas una hora antes de dormir. La luz del celular y la tablet les quita el sueño.'),
    (35.5, 47.5, 'Tres: la misma rutina, en el mismo orden. Baño, dientes, cuento y a la cama.'),
    (49.5, 61.5, 'Cuatro: un cuarto oscuro, fresco y tranquilo. La cama es para dormir.'),
    (63.5, 75.5, 'Cinco: calma antes de acostarse. Nada de juegos movidos, y resolvé antes el agua y la lucecita.'),
    (78.0, 92.0, 'Si el problema sigue, consultá con tu pediatra. Guardá este video y compartilo con otra familia.'),
]

def font(c, size, bold=True, fam='Inter'):
    c.select_font_face(fam, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD if bold else cairo.FONT_WEIGHT_NORMAL); c.set_font_size(size)

def text(c, s, x, y, size, col=INK, bold=True, fam='Inter', align='left', a=1.0, lh=1.25):
    font(c, size, bold, fam)
    for i, ln in enumerate(s.split('\n')):
        e = c.text_extents(ln)
        xx = x - e.width / 2 - e.x_bearing if align == 'center' else x
        c.move_to(xx, y + i * size * lh); c.set_source_rgba(col[0], col[1], col[2], a); c.show_text(ln)
    c.new_path()

def rrect(c, x, y, w, h, r):
    c.new_sub_path(); c.arc(x + w - r, y + r, r, -math.pi / 2, 0); c.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
    c.arc(x + r, y + h - r, r, math.pi / 2, math.pi); c.arc(x + r, y + r, r, math.pi, 1.5 * math.pi); c.close_path()

# ---------------- íconos (dibujados, estilo plano) ----------------
def icon(c, kind, x, y, s, t, col):
    c.save(); c.translate(x, y); c.scale(s, s)
    C = hexc(col)
    if kind == 'clock':
        ellipse(c, 0, 0, 150, 150); fill(c, (1, 1, 1, 1), INK, 10)
        for k in range(12):
            a = k * math.pi / 6
            c.move_to(120 * math.cos(a), 120 * math.sin(a)); c.line_to(135 * math.cos(a), 135 * math.sin(a))
            c.set_source_rgba(*INK); c.set_line_width(8); c.stroke()
        a1 = -math.pi / 2 + t * 0.6; a2 = -math.pi / 2 + t * 0.05
        for (a, L, w) in ((a1, 105, 9), (a2, 70, 14)):
            c.move_to(0, 0); c.line_to(L * math.cos(a), L * math.sin(a)); c.set_source_rgba(*C); c.set_line_width(w); c.set_line_cap(cairo.LINE_CAP_ROUND); c.stroke()
        ellipse(c, 0, 0, 14, 14); fill(c, INK, None, 0)
        ellipse(c, 105, -105, 40, 40); fill(c, hexc('#FFF3C4'), INK, 6)    # lunita
        c.arc(118, -112, 30, 0, 2 * math.pi); c.set_source_rgba(1, 1, 1, 1); c.fill()
    elif kind == 'phone':
        rrect(c, -85, -150, 170, 300, 30); fill(c, (1, 1, 1, 1), INK, 10)
        rrect(c, -65, -120, 130, 220, 12); c.set_source_rgba(*hexc('#3A3F63')); c.fill()
        ellipse(c, 0, 125, 12, 12); fill(c, INK, None, 0)
        q = 0.5 + 0.5 * math.sin(t * 3)
        font(c, 70, True, 'Fredoka Light'); c.set_source_rgba(1, 1, 1, 0.3 + 0.5 * q); c.move_to(-30, 20); c.show_text('z'); c.new_path()
        c.set_source_rgba(*C); c.set_line_width(22); c.set_line_cap(cairo.LINE_CAP_ROUND)
        c.move_to(-150, -150); c.line_to(150, 150); c.stroke()
        ellipse(c, 0, 0, 205, 205); c.set_source_rgba(*C); c.set_line_width(22); c.stroke()
    elif kind == 'book':
        for d in (-1, 1):
            c.move_to(0, -90); c.curve_to(d * 60, -120, d * 130, -115, d * 160, -100); c.line_to(d * 160, 100)
            c.curve_to(d * 130, 85, d * 60, 90, 0, 115); c.close_path(); fill(c, (1, 1, 1, 1), INK, 10)
            for k in range(4):
                c.move_to(d * 35, -50 + 35 * k); c.line_to(d * 130, -55 + 35 * k); c.set_source_rgba(*C); c.set_line_width(8); c.stroke()
        c.move_to(0, -90); c.line_to(0, 115); c.set_source_rgba(*INK); c.set_line_width(10); c.stroke()
        for k in range(3):
            ph = (t * 0.5 + k / 3) % 1
            sparkle(c, -90 + 90 * k, -160 - 60 * ph, 22 * math.sin(math.pi * ph), col)
    elif kind == 'moon':
        rrect(c, -160, -140, 320, 260, 20); fill(c, hexc('#2C3366'), INK, 10)
        c.move_to(0, -140); c.line_to(0, 120); c.move_to(-160, -10); c.line_to(160, -10); c.set_source_rgba(*INK); c.set_line_width(10); c.stroke()
        ellipse(c, 60, -75, 38, 38); fill(c, hexc('#FFF3C4'), None, 0)
        c.arc(78, -85, 32, 0, 2 * math.pi); c.set_source_rgba(*hexc('#2C3366')); c.fill()
        for k, (sx, sy) in enumerate(((-100, -90), (-60, 50), (90, 60), (-120, 20))):
            sparkle(c, sx, sy, 12 + 5 * math.sin(t * 3 + k), '#FFF3C4')
    elif kind == 'cup':
        c.move_to(-90, -100); c.line_to(-70, 120); c.line_to(70, 120); c.line_to(90, -100); c.close_path(); fill(c, (1, 1, 1, 1), INK, 10)
        c.move_to(-82, -40); c.line_to(-75, 110); c.line_to(75, 110); c.line_to(82, -40); c.close_path(); c.set_source_rgba(*hexc('#90CAF9')); c.fill()
        c.arc(100, 10, 45, -math.pi / 2, math.pi / 2); c.set_source_rgba(*INK); c.set_line_width(10); c.stroke()
        for k in range(3):
            ph = (t * 0.4 + k / 3) % 1
            x0 = -40 + 40 * k
            c.move_to(x0, -120 - 60 * ph); c.curve_to(x0 + 15, -140 - 60 * ph, x0 - 15, -160 - 60 * ph, x0, -180 - 60 * ph)
            c.set_source_rgba(C[0], C[1], C[2], math.sin(math.pi * ph)); c.set_line_width(8); c.stroke()
    c.restore()

# ---------------- cuadro ----------------
def bg(c, t):
    c.set_source_rgba(*CREAM); c.paint()
    for k in range(7):   # puntos suaves de fondo
        x = (k * 331 + 40 * math.sin(t * 0.2 + k)) % W; y = 120 + (k * 197) % 900
        ellipse(c, x, y, 90, 90); c.set_source_rgba(*SAND, ); c.fill()
    c.save(); c.translate(80, 980); c.scale(0.18, 0.18); c.set_source_surface(LOGO, 0, -LOGO.get_height()); c.paint(); c.restore()
    text(c, 'Cuentos mágicos de la selva · Para papás', 290, 960, 30, hexc('#6B6F8A'), True)

def hook(c, t):
    a = 1 - ss(6.4, 7.0, t)
    s = K_back(min(1.0, (t + 0.4) / 0.6))   # visible desde el cuadro 0
    c.push_group()
    text(c, '¿A tu hijo le cuesta', W / 2, 360, 104 * s + 0.01, INK, True, 'Fredoka Light', 'center')
    text(c, 'dormirse?', W / 2, 490, 130 * s + 0.01, hexc(ACC[0]), True, 'Fredoka Light', 'center')
    q = 1.0
    rrect(c, W / 2 - 420, 600, 840, 120, 60); c.set_source_rgba(*hexc(ACC[4]), ); c.fill()
    text(c, '5 claves de pediatras', W / 2, 680, 62, (1, 1, 1, 1), True, 'Inter', 'center', a=q)
    for k in range(5):
        ph = (t * 0.4 + k / 5) % 1
        sparkle(c, 300 + 330 * k, 230 + 40 * math.sin(k), 22 * math.sin(math.pi * ph), ACC[k])
    c.pop_group_to_source(); c.paint_with_alpha(a)

def tip(c, t, k):
    u = t - (T0 + k * TL)
    title, body, kind = TIPS[k]
    col = ACC[k]
    a = ss(0, 0.5, u) * (1 - ss(TL - 0.5, TL, u))
    c.push_group()
    # tarjeta del ícono
    cx, cy = 560, 520
    sc = K_back(u / 0.6)
    ellipse(c, cx, cy, 300 * sc + 0.1, 300 * sc + 0.1); c.set_source_rgba(*hexc(col)[:3], 0.18); c.fill()
    icon(c, kind, cx, cy, 1.15 * sc + 0.01, t, col)
    # número
    ellipse(c, 330, 250, 78, 78); fill(c, hexc(col), INK, 0)
    text(c, str(k + 1), 330, 285, 100, (1, 1, 1, 1), True, 'Fredoka Light', 'center')
    # texto
    x = 1000
    q1 = ss(0.4, 1.1, u); q2 = ss(1.4, 2.2, u)
    c.save(); c.rectangle(x - 10, 300, 900, 260); c.clip()
    text(c, title, x, 380 + 40 * (1 - Easing(q1)), 72, INK, True, 'Inter', a=q1, lh=1.15)
    c.restore()
    text(c, body, x, 620, 40, hexc('#4A4F6E'), False, 'Inter', a=q2, lh=1.35)
    c.move_to(x, 560); c.line_to(x + 220 * ss(1.0, 1.8, u), 560); c.set_source_rgba(*hexc(col)); c.set_line_width(10); c.set_line_cap(cairo.LINE_CAP_ROUND); c.stroke()
    # progreso
    for j in range(5):
        ellipse(c, W / 2 - 100 + 50 * j, 1020, 12, 12)
        c.set_source_rgba(*hexc(ACC[j] if j <= k else '#D6CCB8')); c.fill()
    c.pop_group_to_source(); c.paint_with_alpha(a)

def Easing(q): return 1 - (1 - q) ** 3

def outro(c, t):
    u = t - 77.0
    if u < 0: return
    a = ss(0, 0.6, u)
    c.push_group()
    text(c, 'Resumen', 200, 210, 64, hexc(ACC[0]), True, 'Fredoka Light')
    for k, (title, _, kind) in enumerate(TIPS):
        q = ss(0.3 + 0.35 * k, 0.9 + 0.35 * k, u)
        y = 300 + 110 * k
        ellipse(c, 230, y - 18, 34, 34); c.set_source_rgba(*hexc(ACC[k]), ); c.fill()
        text(c, str(k + 1), 230, y + 2, 44, (1, 1, 1, 1), True, 'Fredoka Light', 'center', a=q)
        text(c, title.replace('\n', ' '), 300, y + 2, 44, INK, True, 'Inter', a=q)
    q = ss(4.0, 4.8, u)
    rrect(c, 1180, 330, 600, 300, 40); c.set_source_rgba(1, 1, 1, q); c.fill_preserve(); c.set_source_rgba(*INK[:3], q); c.set_line_width(6); c.stroke()
    text(c, '¿Sigue costando?', 1480, 420, 46, INK, True, 'Inter', 'center', a=q)
    text(c, 'Consultá con\ntu pediatra.', 1480, 490, 42, hexc('#4A4F6E'), False, 'Inter', 'center', a=q)
    q2 = ss(7.0, 7.8, u)
    pulse = 1 + 0.04 * math.sin(t * 5)
    c.save(); c.translate(1480, 760); c.scale(pulse, pulse)
    rrect(c, -330, -60, 660, 120, 60); c.set_source_rgba(*hexc(ACC[4])[:3], q2); c.fill()
    text(c, 'Guardalo y compartilo', 0, 18, 46, (1, 1, 1, 1), True, 'Inter', 'center', a=q2)
    c.restore()
    text(c, 'Fuentes: Academia Americana de Pediatría (healthychildren.org), KidsHealth, Child Mind Institute.', 290, 905, 24, hexc('#8A8FA8'), False, 'Inter', a=ss(1.0, 1.6, u))
    c.pop_group_to_source(); c.paint_with_alpha(a)

def frame(c, t):
    bg(c, t)
    if t < 7.0: hook(c, t)
    k = tip_at(t)
    if k is not None: tip(c, t, k)
    outro(c, t)
    a = ss(DUR - 1.5, DUR, t)
    if a > 0: c.set_source_rgba(*CREAM[:3], a); c.paint()

def miniatura(path):
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, 1280, 720); c = cairo.Context(s)
    c.scale(1280 / W, 720 / H)
    c.set_source_rgba(*CREAM); c.paint()
    icon(c, 'moon', 1450, 470, 1.6, 2.0, ACC[3])
    text(c, '¿No se quiere', 110, 300, 120, INK, True, 'Fredoka Light')
    text(c, 'dormir?', 110, 440, 150, hexc(ACC[0]), True, 'Fredoka Light')
    rrect(c, 110, 540, 720, 120, 60); c.set_source_rgba(*hexc(ACC[4])); c.fill()
    text(c, '5 claves de pediatras', 150, 620, 58, (1, 1, 1, 1), True, 'Inter')
    s.write_to_png(path)

if __name__ == '__main__':
    args = sys.argv[1:]
    if args and args[0] == 'srt':
        print(srt(NARRACION, float(args[1]) if len(args) > 1 else 0.0)); sys.exit()
    if args and args[0] == 'miniatura':
        miniatura('padres01_miniatura.png'); sys.exit()
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(surf)
    if args and args[0] == 'stills':
        for t in map(float, args[1:]):
            c.save(); frame(c, t); c.restore(); surf.write_to_png(f'padres01_{t}.png')
    else:
        t0, t1 = (float(args[1]), float(args[2])) if args and args[0] == 'range' else (0, DUR)
        out = sys.stdout.buffer
        for i in range(int(round(t0 * FPS)), int(round(t1 * FPS))):
            c.save(); frame(c, i / FPS); c.restore(); surf.flush(); out.write(surf.get_data())
