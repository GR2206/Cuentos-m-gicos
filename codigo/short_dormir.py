"""Short — ¡Coco no se quiere ir a dormir! (vertical, 41 s, plantilla nueva: gancho en el cuadro 1 + tarjeta final).
Es Nochebuena y Coco salta en la cama porque quiere esperar la Navidad despierto. Mamá Coco le cuenta un
secreto: "si dormís, la Navidad llega más rápido". Canción de cuna, Coco se duerme... ¡y a la mañana llegó la Navidad!
Uso: python3 short_dormir.py [short a b] | stills 0 12 | portada"""
import cairo, math, sys
import cuerpos as K
from amigos import hexc, ellipse, fill, OUT
from logos import word, sparkle
from ep02_puente_del_rio import kf, ss, K_back, music_note
from ep03_donde_esta_tomi import bubble
from ep05_cumple_tomi import gift
from ep14_bananas_papa import heart
from ep15_navidad import santa_hat, star
from short_kit import SW, SH, FPS, END, top_title, end_card, logo_band

STORY = 38.0
DUR = STORY + END
FLOOR = 1500
MATT = 1250            # arriba del colchón
COCO_X = 390
MAMA = [(0, 1300), (7.0, 1300), (9.0, 800), (31.5, 800), (33.0, 1300), (34.0, 700), (34.5, 700)]
MORNING = 34.0

def day(t): return ss(MORNING, MORNING + 0.8, t)

def room(c, t):
    d = day(t)
    c.set_source_rgba(*hexc('#3F3A7A')); c.paint()
    if d > 0: c.set_source_rgba(*hexc('#FFF3E0', d)); c.paint()
    for k in range(0, SW, 120):
        c.rectangle(k, 0, 60, FLOOR); c.set_source_rgba(*hexc('#4B4590' if d < 0.5 else '#FFE0B2', 1)); c.fill()
    # ventana
    c.rectangle(110, 380, 400, 360); fill(c, hexc('#8D6E63'), OUT, 7)
    c.rectangle(128, 398, 364, 324)
    g = cairo.LinearGradient(0, 398, 0, 722)
    if d < 0.5: g.add_color_stop_rgb(0, *hexc('#141048')[:3]); g.add_color_stop_rgb(1, *hexc('#3949AB')[:3])
    else: g.add_color_stop_rgb(0, *hexc('#29B6F6')[:3]); g.add_color_stop_rgb(1, *hexc('#B3E5FC')[:3])
    c.set_source(g); c.fill()
    if d < 0.5:
        for k in range(12):
            sparkle(c, 150 + (k * 97) % 320, 420 + (k * 61) % 280, 7 + 4 * math.sin(t * 3 + k), '#FFF59D')
        ellipse(c, 420, 470, 45, 45); fill(c, hexc('#FFF59D'), hexc('#F9A825'), 5)
    else:
        ellipse(c, 420, 480, 50, 50); fill(c, hexc('#FFEB3B'), hexc('#F9A825'), 5)
    c.move_to(310, 398); c.line_to(310, 722); c.move_to(128, 560); c.line_to(492, 560)
    c.set_source_rgba(*hexc('#8D6E63')); c.set_line_width(12); c.stroke()
    # piso
    c.rectangle(0, FLOOR, SW, SH - FLOOR); c.set_source_rgba(*hexc('#A1887F')); c.fill()
    c.move_to(0, FLOOR); c.line_to(SW, FLOOR); c.set_source_rgba(*OUT); c.set_line_width(6); c.stroke()
    # arbolito
    x, y = 960, FLOOR
    c.rectangle(x - 22, y - 70, 44, 70); fill(c, hexc('#8D5524'), OUT, 5)
    for k, (w, h) in enumerate(((170, 170), (135, 150), (95, 130))):
        yy = y - 60 - 110 * k
        c.move_to(x - w, yy); c.line_to(x, yy - h - 40); c.line_to(x + w, yy); c.close_path(); fill(c, hexc('#2E7D32'), hexc('#1B5E20'), 5)
    for k, (bx, by, col) in enumerate(((-90, -90, '#F44336'), (70, -120, '#FFEB3B'), (-40, -230, '#2196F3'), (50, -300, '#E040FB'), (-10, -160, '#FF9800'))):
        glow = 0.5 + 0.5 * math.sin(t * 4 + k)
        ellipse(c, x + bx, y + by, 16, 16); fill(c, hexc(col), OUT, 3)
        sparkle(c, x + bx + 14, y + by - 14, 6 * glow, '#FFFFFF')
    star(c, t, (x, y - 470), 0.6, 0.4)
    if d > 0:
        for k, gx in enumerate((880, 1040, 960)):
            s = K_back((t - MORNING - 0.3 * k) / 0.5)
            if s > 0.01: gift(c, gx, FLOOR + 20, 0.7 * s)
    if d < 1:   # oscuridad de la noche encima
        c.set_source_rgba(0.05, 0.04, 0.2, 0.25 * (1 - d)); c.paint()

def bed_back(c):
    c.rectangle(60, 1020, 70, 480); fill(c, hexc('#8D6E63'), OUT, 6)
    c.move_to(60, 1040); c.curve_to(60, 900, 130, 880, 130, 1040); fill(c, hexc('#8D6E63'), OUT, 6)
    ellipse(c, 250, MATT - 40, 130, 60); fill(c, (1, 1, 1, 1), OUT, 6)        # almohada

def bed_front(c, t, blanket_top):
    c.rectangle(70, MATT, 680, 110); fill(c, hexc('#E3F2FD'), OUT, 6)       # colchón
    c.rectangle(70, MATT + 110, 680, 60); fill(c, hexc('#8D6E63'), OUT, 6)
    for x in (90, 730): c.rectangle(x - 20, MATT + 170, 40, FLOOR - MATT - 170); fill(c, hexc('#6D4C41'), OUT, 5)
    if blanket_top < MATT + 100:   # frazada
        c.move_to(90, MATT + 120); c.line_to(90, blanket_top + 40); c.curve_to(90, blanket_top, 160, blanket_top - 10, 260, blanket_top)
        c.line_to(720, blanket_top + 30); c.line_to(740, MATT + 120); c.close_path()
        fill(c, hexc('#EF5350'), OUT, 6)
        for k in range(5):
            sx = 170 + 120 * k; sy = blanket_top + 70 + 30 * (k % 2) + 0.06 * (sx - 260)
            if sy < MATT + 100: sparkle(c, sx, sy, 16, '#FFFFFF')

def frame(c, t):
    if t >= STORY:
        end_card(c, t - STORY); return
    room(c, t)
    bed_back(c)
    # --- Coco ---
    jumping = t < 7.0 or t > MORNING + 0.3
    if jumping:
        hop = abs(math.sin(t * 4.2)) * 170
        base = MATT + 40 - hop; sq = 1.0
        mood = 'sad' if t < 7.0 else 'o' if t < MORNING + 1.4 else 'smile'
        ar, al = math.radians(-60 + 20 * math.sin(t * 8)), math.radians(-120 - 20 * math.sin(t * 8))
        blanket = 2000
        look = (0, -0.2)
    else:
        base = MATT + 120; hop = 0
        blanket = kf(t, [(15.5, MATT + 160), (18.0, 1090), (30.0, 1090), (31.0, 1060)])
        mood, look = 'smile', (1, -0.1)
        ar, al = math.radians(65), math.radians(115)
        if t < 15.5: base = MATT + 40; mood = 'sad'; ar, al = math.radians(150), math.radians(30)      # brazos cruzados, sentado
        if 12.5 < t < 15.5: mood = 'o'
        if 22.0 < t < 30.0:
            mood = 'o' if (t - 22.0) % 3.0 < 0.9 else 'smile'                # bosteza
        if t > 27.0: mood = 'closed'
    lid = ss(24.0, 28.0, t) if not jumping else 0.0
    K.put(c, K.coco, COCO_X, base, 1.0, t=t, mood=mood, look=look, arm_r=ar, arm_l=al, lid=lid,
          sad=1.0 if mood == 'sad' else 0.0)
    if t > MORNING + 0.3 or t < 7.0:
        pass
    if t > MORNING: santa_hat(c, COCO_X, base - 455, 1.1, -0.15)
    bed_front(c, t, blanket)
    # --- Mamá ---
    mx = kf(t, MAMA)
    if 6.5 < t:
        reading = 20.0 < t < 27.5
        mar = math.radians(-35) if reading else (math.radians(-160) if 28.0 < t < 30.5 else math.radians(60))
        mal = math.radians(-145) if reading else math.radians(115)
        if t > MORNING + 0.3: mar, mal = math.radians(-58 + 25 * math.sin(t * 9)), math.radians(-122 - 25 * math.sin(t * 9))
        if 16.0 < t < 18.5: mar = mal = math.radians(170)        # arropa
        K.put(c, K.mama, mx, FLOOR + 10, 1.0, flip=True, t=t, look=(1, 0.4), arm_r=mar, arm_l=mal, walk=t * 7 if 7.0 < t < 9.0 or 31.5 < t < 34.5 else 0,
              mood='closed' if 28.0 < t < 31.0 else 'smile')
        if reading:   # librito
            c.save(); c.translate(mx - 10, FLOOR - 330); c.rotate(-0.15)
            for d in (-1, 1):
                c.move_to(0, -40); c.line_to(d * 70, -50); c.line_to(d * 70, 40); c.line_to(0, 50); c.close_path(); fill(c, hexc('#29B6F6'), OUT, 5)
            c.restore()
        if t > MORNING: santa_hat(c, mx + 10, FLOOR + 10 - 455, 1.1, 0.1)
    # --- efectos ---
    if 20.0 < t < 30.0:   # canción de cuna
        for k in range(3):
            ph = (t * 0.45 + k / 3) % 1
            music_note(c, mx - 120 - 200 * ph, FLOOR - 560 - 260 * ph, math.sin(math.pi * ph), ['#F48FB1', '#90CAF9', '#FFF59D'][k])
    if 28.5 < t < MORNING:   # zzz
        for k in range(3):
            ph = ((t - 28.5) * 0.5 + k / 3) % 1
            c.select_font_face('Fredoka Light', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
            c.set_font_size(60 + 40 * ph); c.set_source_rgba(1, 1, 1, math.sin(math.pi * ph))
            c.move_to(COCO_X + 150 + 90 * ph, base - 450 - 220 * ph); c.show_text('z')
    if 29.0 < t < 32.0:
        q = ss(29.0, 32.0, t)
        heart(c, COCO_X + 80, base - 420 - 120 * q, 1.6, math.sin(math.pi * q))
    if MORNING - 0.6 < t < MORNING + 0.6:   # destello de la mañana
        a = 1 - abs(t - MORNING) / 0.6
        c.set_source_rgba(1, 1, 1, 0.9 * a); c.paint()
    if t > MORNING + 0.5:
        for k in range(10):
            ph = ((t - MORNING) * 0.8 + k / 10) % 1
            sparkle(c, 80 + (k * 113) % 950, 300 + 1100 * ph, 14, ('#FFD600', '#FF4081', '#29B6F6')[k % 3])
    # --- globitos ---
    if t < 6.5:
        bubble(c, COCO_X + 120, base - 480, '¡NO ME QUIERO DORMIR!', min(0.84, 0.3 + t / 8) if t < 6.0 else 0.84 + (t - 6.0) / 0.5 * 0.16, 56)
    bubble(c, COCO_X + 80, MATT - 460, '¡Quiero esperar la Navidad!', (t - 6.8) / 3.0, 48)
    bubble(c, mx - 40, FLOOR - 560, 'Si dormís, la Navidad', (t - 10.0) / 3.4, 46)
    bubble(c, mx - 40, FLOOR - 480, 'llega más rápido…', (t - 10.3) / 3.1, 46)
    bubble(c, COCO_X + 80, MATT - 460, '¿En serio?', (t - 13.0) / 2.5, 54)
    bubble(c, COCO_X + 180, base - 480, '¡Llegó la Navidad!', (t - (MORNING + 1.2)) / 2.8, 52)
    # --- títulos ---
    if t < 7.0: top_title(c, t, 0, '¡Coco no se quiere', 'ir a dormir!', first=True, size=92)
    elif t < 15.5: top_title(c, t, 7.0, 'Mamá tiene', 'un secreto…')
    elif t < 22.0: top_title(c, t, 15.5, '¡A la camita!')
    elif t < MORNING: top_title(c, t, 22.0, 'Shhh…', 'Coco se duerme')
    else: top_title(c, t, MORNING, '¡Llegó la', 'Navidad!')
    logo_band(c)

if __name__ == '__main__':
    args = sys.argv[1:] or ['short']
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, SW, SH); c = cairo.Context(surf)
    if args[0] == 'stills':
        for t in map(float, args[1:]):
            c.save(); frame(c, t); c.restore(); surf.write_to_png(f'dormir_{t}.png')
    elif args[0] == 'portada':
        frame(c, 3.0); surf.write_to_png('short_dormir_portada.png')
    else:
        a0, a1 = (float(args[1]), float(args[2])) if len(args) > 2 else (0, DUR)
        out = sys.stdout.buffer
        for i in range(int(round(a0 * FPS)), int(round(a1 * FPS))):
            c.save(); frame(c, i / FPS); c.restore(); surf.flush(); out.write(surf.get_data())
