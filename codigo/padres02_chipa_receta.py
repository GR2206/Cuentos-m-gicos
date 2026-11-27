"""Para papás 02 — Receta de chipá para hacer con tus hijos (112 s).
Tutorial de cocina dirigido al ADULTO: cantidades, temperatura y tiempo de horno, y qué parte hace
cada uno ("Ellos" / "Vos"). La cocina animada de ep16 queda como ilustración a la izquierda; a la
derecha, la ficha de la receta en tipografía de adulto (Inter).

Uso:  python3 padres02_chipa_receta.py [range a b] | stills 3 20 | miniatura | srt 0"""
import cairo, math, sys
import ep16_chipa as E
from amigos import hexc, ellipse, fill
from logos import sparkle
from ep02_puente_del_rio import ss, K_back
from ep09_semilla_magica import srt
from padres01_dormir import text, rrect, LOGO, INK, CREAM

W, H, FPS = 1920, 1080, 30
DUR = E.DUR
ACC = hexc('#E0607E'); OK = hexc('#2E9E6A'); SUB = hexc('#4A4F6E'); PANEL = hexc('#FFFDF8')
SC, SX, SY = 0.64, 40, 175          # escena de cocina reducida

INGR = [('500 g de almidón de mandioca', 35.5), ('250 g de queso semiduro rallado', 38.0), ('1 cucharadita de sal', 40.5),
        ('100 g de manteca derretida', 47.5), ('2 huevos', 49.5), ('100 ml de leche (de a poco)', 57.0)]

PASOS = [  # (desde, hasta, título, ellos, vos)
    (14, 22, '1 · Manos limpias', 'Se lavan con agua y jabón.', 'Prepará los ingredientes\nen la mesa.'),
    (22, 34, '2 · Los ingredientes', 'Te ayudan a encontrarlos\ny ponerlos en fila.', 'Medí las cantidades.'),
    (34, 46, '3 · Almidón, queso y sal', 'Vuelcan y mezclan\ncon la cuchara.', 'Sostené el bol.'),
    (46, 56, '4 · Manteca y huevos', 'Rompen los huevos\n(con tu ayuda).', 'Derretí la manteca\n(tibia, no caliente).'),
    (56, 68, '5 · Leche y amasar', 'Amasan con las manos.', 'Agregá la leche de a poco\nhasta que no se pegue.'),
    (68, 80, '6 · Bolitas', 'Hacen bolitas del tamaño\nde una nuez.', 'Precalentá el horno a 180 °C\ny enmantecá la placa.'),
    (80, 92, '7 · Al horno', 'Miran desde lejos.', 'Ponés y sacás la placa.\n20 a 25 min, hasta dorar.'),
    (92, 104, '8 · A disfrutar', 'Comparten con la familia.', 'Dejá enfriar 5 minutos:\nel queso quema.'),
]

NARRACION = [
    (0.6, 7.0, 'Una receta de chipá fácil, para hacer con tus hijos. Te digo qué parte hacen ellos y cuál te toca a vos.'),
    (14.5, 21.5, 'Primero, manos limpias. Mientras ellos se lavan, vos prepará todo en la mesa.'),
    (23.0, 33.0, 'Vas a necesitar quinientos gramos de almidón de mandioca, doscientos cincuenta de queso, sal, cien de manteca, dos huevos y cien de leche.'),
    (35.0, 45.0, 'Ellos vuelcan el almidón, el queso y la sal, y mezclan. Vos sostené el bol.'),
    (47.0, 55.5, 'La manteca la derretís vos, que quede tibia. Los huevos los pueden romper ellos, con ayuda.'),
    (57.0, 67.0, 'Agregá la leche de a poco, mientras ellos amasan, hasta que la masa no se pegue.'),
    (69.0, 79.0, 'Ellos hacen las bolitas. Vos prendé el horno a ciento ochenta grados.'),
    (81.0, 91.5, 'El horno es cosa de grandes: vos ponés y sacás la placa. Veinte a veinticinco minutos, hasta que estén doraditos.'),
    (93.5, 103.0, 'Dejalos enfriar cinco minutos antes de comer: el queso adentro quema.'),
    (104.5, 110.5, 'Guardá la receta y compartila con otra familia.'),
]

def scene(c, t):
    cx, cy, z = E.camera(t)
    c.save(); c.translate(SX, SY)
    rrect(c, 0, 0, W * SC, H * SC, 36); c.clip()
    c.scale(SC, SC)
    c.translate(W / 2, H / 2); c.scale(z, z); c.translate(-cx, -cy)
    E.world(c, t)
    c.restore()
    rrect(c, SX, SY, W * SC, H * SC, 36); c.set_source_rgba(*INK); c.set_line_width(5); c.stroke()

def header(c, t):
    text(c, 'Chipá para hacer con tus hijos', SX, 110, 70, INK, True, 'Inter')
    text(c, '6 ingredientes · 45 minutos · rinde unos 30', SX, 158, 34, SUB, False, 'Inter')

def panel(c, t):
    x0, y0, w = 1310, 70, 570
    rrect(c, x0, y0, w, 870, 32); c.set_source_rgba(*PANEL); c.fill_preserve(); c.set_source_rgba(*INK); c.set_line_width(4); c.stroke()
    text(c, 'Ingredientes', x0 + 36, y0 + 70, 40, ACC, True, 'Inter')
    for k, (s, ta) in enumerate(INGR):
        y = y0 + 125 + 52 * k
        done = ss(ta - 0.2, ta + 0.3, t)
        ellipse(c, x0 + 50, y - 11, 15, 15)
        if done > 0:
            c.set_source_rgba(*OK[:3], done); c.fill_preserve()
        c.set_source_rgba(*INK); c.set_line_width(3); c.stroke()
        if done > 0.5:
            c.move_to(x0 + 42, y - 11); c.line_to(x0 + 48, y - 4); c.line_to(x0 + 59, y - 19)
            c.set_source_rgba(1, 1, 1, 1); c.set_line_width(4); c.stroke()
        text(c, s, x0 + 80, y, 28, INK if done < 0.5 else SUB, done < 0.5, 'Inter')
    c.move_to(x0 + 36, y0 + 450); c.line_to(x0 + w - 36, y0 + 450); c.set_source_rgba(*hexc('#E6DCC8')); c.set_line_width(3); c.stroke()
    cur = None
    for p in PASOS:
        if p[0] <= t < p[1]: cur = p
    if t < 14:
        a = ss(0.3, 1.0, t)
        text(c, 'Cada paso dice qué hacen\nellos y qué hacés vos.', x0 + 36, y0 + 530, 34, INK, True, 'Inter', a=a, lh=1.3)
        text(c, 'El horno, siempre un adulto.', x0 + 36, y0 + 680, 32, ACC, True, 'Inter', a=ss(1.5, 2.2, t))
    elif cur:
        a1, b1, tit, ellos, vos = cur
        u = t - a1
        a = ss(0, 0.4, u) * (1 - ss(b1 - a1 - 0.3, b1 - a1, u))
        text(c, tit, x0 + 36, y0 + 515, 40, INK, True, 'Inter', a=a)
        for j, (lab, s, col) in enumerate((('Ellos', ellos, hexc('#5C6BC0')), ('Vos', vos, ACC))):
            q = a * ss(0.4 + 0.5 * j, 0.9 + 0.5 * j, u)
            yy = y0 + 570 + 140 * j
            rrect(c, x0 + 36, yy, 110, 46, 23); c.set_source_rgba(*col[:3], q); c.fill()
            text(c, lab, x0 + 91, yy + 33, 28, (1, 1, 1, 1), True, 'Inter', 'center', a=q)
            text(c, s, x0 + 165, yy + 33, 29, INK, False, 'Inter', a=q, lh=1.3)
    else:
        a = ss(104, 104.6, t)
        text(c, 'Guardá la receta\ny compartila', x0 + 36, y0 + 540, 46, INK, True, 'Inter', a=a, lh=1.2)
        pulse = 1 + 0.04 * math.sin(t * 5)
        c.save(); c.translate(x0 + w / 2, y0 + 760); c.scale(pulse, pulse)
        rrect(c, -230, -45, 460, 90, 45); c.set_source_rgba(*ACC[:3], a); c.fill()
        text(c, 'con otra familia 💛'.replace(' 💛', ''), 0, 12, 36, (1, 1, 1, 1), True, 'Inter', 'center', a=a)
        c.restore()

def footer(c):
    c.save(); c.translate(SX, 1060); c.scale(0.11, 0.11); c.set_source_surface(LOGO, 0, -LOGO.get_height()); c.paint(); c.restore()
    text(c, 'Cuentos mágicos de la selva · Para papás', SX + 130, 1018, 28, hexc('#6B6F8A'), True, 'Inter')
    text(c, 'Si tu hijo tiene alergia al huevo o a la leche,\nconsultá con tu pediatra.', 1310, 990, 22, hexc('#8A8FA8'), False, 'Inter')

def frame(c, t):
    c.set_source_rgba(*CREAM); c.paint()
    header(c, t); scene(c, t); panel(c, t); footer(c)
    a = ss(DUR - 1.5, DUR, t)
    if a > 0: c.set_source_rgba(*CREAM[:3], a); c.paint()

def miniatura(path):
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, 1280, 720); c = cairo.Context(s)
    c.scale(1280 / W, 720 / H)
    c.set_source_rgba(*CREAM); c.paint()
    fx, fy, fw, fh = 960, 160, 900, 760
    c.save(); rrect(c, fx, fy, fw, fh, 40); c.clip()
    c.translate(fx + fw / 2, fy + fh / 2); c.scale(1.25, 1.25); c.translate(-760, -470)
    E.world(c, 100.0); c.restore()
    rrect(c, fx, fy, fw, fh, 40); c.set_source_rgba(*INK); c.set_line_width(8); c.stroke()
    text(c, 'Chipá', 80, 400, 190, INK, True, 'Fredoka Light')
    text(c, 'con tus hijos', 80, 540, 100, hexc('#5C6BC0'), True, 'Fredoka Light')
    rrect(c, 80, 640, 820, 120, 60); c.set_source_rgba(*ACC); c.fill()
    text(c, 'Receta fácil, paso a paso', 125, 720, 56, (1, 1, 1, 1), True, 'Inter')
    s.write_to_png(path)

if __name__ == '__main__':
    args = sys.argv[1:]
    if args and args[0] == 'srt':
        print(srt(NARRACION, float(args[1]) if len(args) > 1 else 0.0)); sys.exit()
    if args and args[0] == 'miniatura':
        miniatura('padres02_miniatura.png'); sys.exit()
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(surf)
    if args and args[0] == 'stills':
        for t in map(float, args[1:]):
            c.save(); frame(c, t); c.restore(); surf.write_to_png(f'padres02_{t}.png')
    else:
        t0, t1 = (float(args[1]), float(args[2])) if args and args[0] == 'range' else (0, DUR)
        out = sys.stdout.buffer
        for i in range(int(round(t0 * FPS)), int(round(t1 * FPS))):
            c.save(); frame(c, i / FPS); c.restore(); surf.flush(); out.write(surf.get_data())
