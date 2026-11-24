"""Short familiar — El barrilete de Coco y Papá (vertical 1080x1920, 56 s).
Paso a paso para hacer un barrilete con los papás y salir a volarlo.
Uso: python3 short_barrilete.py             -> cuadros crudos 1080x1920 por stdout
     python3 short_barrilete.py stills 5 30 -> PNG sueltos
     python3 short_barrilete.py miniatura   -> short_barrilete_portada.png"""
import cairo, math, os, sys
import cuerpos as K
from amigos import hexc, ellipse, fill, OUT
from logos import word, sparkle
from ep02_puente_del_rio import kf, ss, K_back, music_note

SW, SH, FPS = 1080, 1920, 30
DUR = 56.0
STEPS = [(4.0, 'Paso 1', 'Dos palitos en cruz'), (11.0, 'Paso 2', 'Papel de colores'),
         (18.0, 'Paso 3', 'Una cola con moños'), (25.0, 'Paso 4', '¡El hilo!'), (32.0, '¡Listo!', '¡A volar!')]
FLY = 33.0
KCOLS = ['#FF4081', '#FFD600', '#00B0FF', '#00C853']

def step_k(t, i): return ss(STEPS[i][0] + 0.8, STEPS[i][0] + 3.5, t)

def kite(c, x, y, s, t, rot=0.0, flying=False):
    """Barrilete armado según el tiempo (cada parte aparece en su paso)."""
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    k1, k2, k3 = step_k(t, 0), step_k(t, 1), step_k(t, 2)
    pts = [(0, -200), (140, -40), (0, 220), (-140, -40)]
    if k2 > 0:
        for i in range(4):
            p0, p1 = pts[i], pts[(i + 1) % 4]
            q = min(1, max(0, k2 * 4 - i))
            if q <= 0: continue
            c.move_to(0, -40); c.line_to(*p0); c.line_to(p0[0] + (p1[0] - p0[0]) * q, p0[1] + (p1[1] - p0[1]) * q); c.close_path()
            c.set_source_rgba(*hexc(KCOLS[i])); c.fill()
        if k2 >= 1:
            c.move_to(*pts[0])
            for p in pts[1:]: c.line_to(*p)
            c.close_path(); c.set_source_rgba(*OUT); c.set_line_width(8); c.stroke()
            # cara feliz
            for ex in (-35, 35): ellipse(c, ex, -50, 10, 13); c.set_source_rgba(*OUT); c.fill()
            c.arc(0, -20, 34, 0.2 * math.pi, 0.8 * math.pi); c.set_line_width(7); c.stroke()
    if k1 > 0:
        c.set_line_cap(cairo.LINE_CAP_ROUND); c.set_source_rgba(*hexc('#8D6E63')); c.set_line_width(14)
        c.move_to(0, -200); c.line_to(0, -200 + 420 * min(1, k1 * 2)); c.stroke()
        if k1 > 0.5:
            q = (k1 - 0.5) * 2
            c.move_to(-140 * q, -40); c.line_to(140 * q, -40); c.stroke()
    if k3 > 0:
        n = int(1 + k3 * 5)
        wav = t * 6 if flying else t * 2
        px, py = 0, 220
        for i in range(n):
            nx, ny = 25 * math.sin(wav + i), 220 + (i + 1) * 75
            c.move_to(px, py); c.line_to(nx, ny); c.set_source_rgba(*OUT); c.set_line_width(5); c.stroke()
            c.save(); c.translate(nx, ny)
            c.move_to(0, 0); c.line_to(-30, -18); c.line_to(-30, 18); c.close_path()
            c.move_to(0, 0); c.line_to(30, -18); c.line_to(30, 18); c.close_path()
            fill(c, hexc(KCOLS[i % 4]), OUT, 4); c.restore()
            px, py = nx, ny
    c.restore()

def tip(c, text, y, a):
    if a <= 0: return
    c.push_group()
    c.new_path(); r = 50; x0, x1 = 90, SW - 90
    c.arc(x0 + r, y - r, r, math.pi, 1.5 * math.pi); c.arc(x1 - r, y - r, r, 1.5 * math.pi, 0)
    c.arc(x1 - r, y + r, r, 0, 0.5 * math.pi); c.arc(x0 + r, y + r, r, 0.5 * math.pi, math.pi); c.close_path()
    c.set_source_rgba(1, 1, 1, 0.92); c.fill_preserve(); c.set_source_rgba(*OUT); c.set_line_width(6); c.stroke()
    word(c, text, SW / 2, y + 16, 44, outline=4)
    c.pop_group_to_source(); c.paint_with_alpha(a)

LOGO = cairo.ImageSurface.create_from_png(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'imagenes', 'logo_perfil.png'))

def frame(c, t):
    outside = ss(FLY - 0.6, FLY + 0.4, t)
    # cielo: adentro (cuarto cálido) -> afuera (cielo y pasto)
    g = cairo.LinearGradient(0, 0, 0, SH)
    g.add_color_stop_rgb(0, *hexc('#FFE0B2')[:3]); g.add_color_stop_rgb(1, *hexc('#FFCC80')[:3])
    c.set_source(g); c.paint()
    if outside > 0:
        g = cairo.LinearGradient(0, 0, 0, SH)
        g.add_color_stop_rgb(0, *hexc('#29B6F6')[:3]); g.add_color_stop_rgb(0.7, *hexc('#B3E5FC')[:3]); g.add_color_stop_rgb(1, *hexc('#8BC34A')[:3])
        c.set_source(g); c.paint_with_alpha(outside)
    ground_y = 1560
    if outside < 1:  # mesa de trabajo
        c.push_group()
        c.rectangle(0, ground_y, SW, SH - ground_y); c.set_source_rgba(*hexc('#A1887F')); c.fill()
        c.rectangle(80, 940, SW - 160, 40); fill(c, hexc('#8D6E63'), OUT, 6)
        for (x, col) in ((180, '#FF4081'), (300, '#00B0FF'), (850, '#FFD600')):   # papeles y tijera
            c.rectangle(x - 40, 900, 80, 40); fill(c, hexc(col), OUT, 4)
        c.pop_group_to_source(); c.paint_with_alpha(1 - outside)
    if outside > 0:
        c.push_group()
        c.move_to(0, ground_y); c.curve_to(300, 1500, 800, 1500, SW, ground_y); c.line_to(SW, SH); c.line_to(0, SH); c.close_path()
        c.set_source_rgba(*hexc('#7CB342')); c.fill()
        for (x0, y0, s) in ((100, 260, 0.9), (650, 420, 0.7)):
            c.save(); c.translate((x0 + 15 * t) % 1300 - 200, y0); c.scale(s, s)
            for (cx, cy, r) in ((0, 0, 60), (70, -30, 75), (150, 0, 60), (75, 20, 60)): ellipse(c, cx, cy, r, r)
            c.set_source_rgba(1, 1, 1, 1); c.fill(); c.restore()
        c.pop_group_to_source(); c.paint_with_alpha(outside)
    # barrilete
    if t < FLY:
        kite(c, SW / 2, 620, 0.9, t)
    else:
        q = ss(FLY + 1.0, FLY + 7.0, t)
        kx = SW / 2 + 180 * q + 50 * math.sin(t * 1.2); ky = 1200 - 800 * q + 30 * math.sin(t * 1.7)
        ks = 0.75 - 0.25 * q
        kite(c, kx, ky, ks, t, rot=0.15 * math.sin(t * 1.5), flying=True)
    # Papá y Coco
    run = FLY < t < FLY + 6
    px = 430 if t < FLY else kf(t, [(FLY, 300), (FLY + 6, 440)])
    cxx = 720 if t < FLY else kf(t, [(FLY, 560), (FLY + 6, 720)])
    pa = (math.radians(-60 + 15 * math.sin(t * 3)), math.radians(-120)) if t < FLY else (math.radians(-55), math.radians(110))
    ca = (math.radians(-70 + 20 * math.sin(t * 5)), math.radians(-110 - 20 * math.sin(t * 5)))
    if t > FLY + 6: ca = (math.radians(-58 + 25 * math.sin(t * 9)), math.radians(-122 - 25 * math.sin(t * 9)))
    look_p = (0.4, -0.8) if t < FLY else (0.5, -1)
    K.put(c, K.papa, px, ground_y, 0.95, t=t, look=look_p, arm_r=pa[0], arm_l=pa[1], walk=t * 8 if run else 0)
    jump = 40 * abs(math.sin(t * 4.5)) if t > FLY + 6 else 0
    K.put(c, K.coco, cxx, ground_y - jump, 0.8, t=t, look=(-0.3, -0.8), arm_r=ca[0], arm_l=ca[1], walk=t * 9 if run else 0,
          mood='o' if FLY + 2 < t < FLY + 5 else 'smile')
    k4 = step_k(t, 3)
    if t < FLY and k4 > 0:  # paso 4: el hilo va del barrilete a la mano de Papá
        hx, hy = px + 0.95 * (78 + 115 * math.cos(pa[0])), ground_y - 0.95 * (180 - 115 * math.sin(pa[0]))
        kx, ky = SW / 2, 620 - 0.9 * 40
        c.move_to(kx, ky); c.line_to(kx + (hx - kx) * k4, ky + (hy - ky) * k4)
        c.set_source_rgba(*OUT); c.set_line_width(4); c.stroke()
        ellipse(c, hx, hy, 26 * k4, 18 * k4); fill(c, hexc('#FFFFFF'), OUT, 4)
    if t > FLY:  # hilo desde la mano de Papá
        q = ss(FLY + 1.0, FLY + 7.0, t)
        kx = SW / 2 + 180 * q + 50 * math.sin(t * 1.2); ky = 1200 - 800 * q + 30 * math.sin(t * 1.7)
        hx, hy = px + 0.95 * (78 + 115 * math.cos(pa[0])), ground_y - 0.95 * (180 - 115 * math.sin(pa[0]))
        c.move_to(hx, hy); c.curve_to(hx + 80, hy - 150, kx - 40, ky + 300, kx, ky + 40 * (0.75 - 0.25 * q))
        c.set_source_rgba(1, 1, 1, 0.9); c.set_line_width(3); c.stroke()
    # textos
    for i, (t0, title, text) in enumerate(STEPS):
        t1 = STEPS[i + 1][0] if i + 1 < len(STEPS) else 40.0
        if t0 <= t < t1:
            s = K_back((t - t0) / 0.4) * (1 - ss(t1 - 0.3, t1, t))
            word(c, title, SW / 2, 170, 110 * s + 0.01, tilt=0.05, outline=9)
            word(c, text, SW / 2, 290, 80 * s + 0.01, start=3, tilt=0.04, outline=7)
    if t < 4.0:
        s = K_back((t - 0.2) / 0.5)
        word(c, '¡Hagamos un', SW / 2, 170, 105 * s + 0.01, tilt=0.05, outline=9)
        word(c, 'barrilete!', SW / 2, 300, 120 * s + 0.01, start=3, tilt=0.05, outline=10)
    if 11 < t < 31:
        tip(c, 'Las tijeras, siempre con papá o mamá', 1760, ss(11.5, 12.2, t) * (1 - ss(30.3, 31, t)))
    if t > 40:
        s = K_back((t - 40) / 0.6)
        word(c, '¿Lo hacemos', SW / 2, 170, 105 * s + 0.01, tilt=0.05, outline=9)
        word(c, 'en familia?', SW / 2, 300, 110 * s + 0.01, start=3, tilt=0.05, outline=9)
        d = 170; cy = 1760
        c.save(); c.arc(170, cy, d / 2, 0, 2 * math.pi); c.clip()
        c.translate(170 - d / 2, cy - d / 2); c.scale(d / LOGO.get_width(), d / LOGO.get_height())
        c.set_source_surface(LOGO, 0, 0); c.paint(); c.restore()
        c.arc(170, cy, d / 2, 0, 2 * math.pi); c.set_source_rgba(1, 1, 1, 1); c.set_line_width(8); c.stroke()
        word(c, 'Cuentos mágicos', 620, cy - 15, 62, outline=6); word(c, 'de la selva', 620, cy + 60, 62, start=5, outline=6)
    if t > FLY + 6:
        for k in range(8):
            ph = (t * 0.5 + k / 8) % 1
            sparkle(c, 100 + k * 125, 450 + 400 * ((k * 3) % 5) / 5, 24 * math.sin(math.pi * ph), '#FFFFFF')
    a = max(1 - ss(0, 0.4, t), ss(DUR - 1.2, DUR, t))
    if a > 0: c.set_source_rgba(1, 1, 1, a); c.paint()

if __name__ == '__main__':
    args = sys.argv[1:]
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, SW, SH); c = cairo.Context(surf)
    if args and args[0] == 'stills':
        for t in map(float, args[1:]):
            c.save(); frame(c, t); c.restore(); surf.write_to_png(f'barrilete_{t}.png')
    elif args and args[0] == 'miniatura':
        c.save(); frame(c, 41.5); c.restore(); surf.write_to_png('short_barrilete_portada.png')
    else:
        a0, a1 = (float(args[1]), float(args[2])) if len(args) > 2 else (0, DUR)
        out = sys.stdout.buffer
        for i in range(int(round(a0 * FPS)), int(round(a1 * FPS))):
            c.save(); frame(c, i / FPS); c.restore(); surf.flush(); out.write(surf.get_data())
