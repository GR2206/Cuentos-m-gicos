"""Episodio 14 — A contar bananas con Papá Coco (familia + contar del 1 al 10, 100 s).
Coco y su papá van al bananero. Coco no llega, Papá lo sube a los hombros y juntan
10 bananas contando. Después las comparten con los amigos y se dan un abrazo.

      python3 ep14_bananas_papa.py srt 5.5     -> subtítulos .srt de la narración
Uso:  python3 ep14_bananas_papa.py              -> cuadros crudos por stdout
      python3 ep14_bananas_papa.py range 0 50   -> solo un tramo
      python3 ep14_bananas_papa.py stills 12 65 -> PNG sueltos"""
import cairo, math, sys
import cuerpos as K
from amigos import hexc, ellipse, fill, OUT
from logos import word, sparkle
from ep02_puente_del_rio import kf, ss, moving, K_back, music_note
from ep03_donde_esta_tomi import bubble
from ep09_semilla_magica import SKY, LAND, cloud, sun, srt

W, H, FPS = 1920, 1080, 30
DUR = 100.0
GROUND = 880
TREE = 1420
BASKET = (930, GROUND)
PAPA_STOP = 1260
COUNT0, COUNT_DT = 21.5, 3.2
BANANAS = [(1330, 420), (1385, 455), (1440, 420), (1495, 455), (1350, 500), (1410, 530), (1470, 500), (1300, 470), (1525, 500), (1440, 570)]
FRIENDS = [('tito', 520), ('pipa', 270), ('tomi', 720), ('lola', 640)]
SHARE0 = 70.0

NARRACION = [
    (6.0, 11.0, 'Un día, Coco salió a pasear con su papá.'),
    (12.0, 17.0, '¡Querían juntar bananas! Pero Coco no llegaba...'),
    (18.0, 21.0, 'Entonces Papá lo subió a sus hombros.'),
    (22.0, 54.0, '¡Y contaron juntos! Uno, dos, tres, cuatro, cinco, seis, siete, ocho, nueve... ¡y diez!'),
    (56.0, 61.0, '¡Diez bananas! ¡Qué canasta tan llena!'),
    (62.0, 68.0, 'Entonces llegaron los amigos.'),
    (70.0, 82.0, 'Y Coco compartió: una para Tito, una para Pipa, una para Tomi y una para Lola.'),
    (84.0, 90.0, 'Coco abrazó a su papá muy fuerte.'),
    (91.0, 97.0, '¡Te quiero, papá! Contar juntos es más lindo.'),
]

def picked(k, t): return t >= COUNT0 + k * COUNT_DT + 1.1

def papa_x(t): return kf(t, [(5, -300), (12, PAPA_STOP), (56, PAPA_STOP), (58, 1180)])
def on_shoulders(t): return 19.0 <= t < 56.5

def coco_place(t):
    """(x, y_pies) de Coco."""
    px = papa_x(t)
    if t < 12: return px + 150, GROUND
    if t < 19: return PAPA_STOP + 150, GROUND
    if t < 20.2:
        q = ss(19, 20.2, t)
        return PAPA_STOP + 150 * (1 - q), GROUND - 262 * q - 120 * math.sin(math.pi * q)
    if t < 56.5: return px, GROUND - 262
    if t < 57.7:
        q = ss(56.5, 57.7, t)
        return px - 170 * q, GROUND - 262 * (1 - q) - 100 * math.sin(math.pi * q)
    return kf(t, [(57.7, px - 170), (59, 1010), (84, 1010), (85, 1060)]), GROUND

def coco_hand_target(t):
    for k in range(10):
        s = COUNT0 + k * COUNT_DT
        if s <= t < s + 1.3: return BANANAS[k]
    return None

def banana_flight(k, t):
    s = COUNT0 + k * COUNT_DT + 1.1
    q = (t - s) / 1.0
    if not 0 <= q < 1: return None
    x0, y0 = BANANAS[k]; x1, y1 = BASKET[0] + (k % 5 - 2) * 18, BASKET[1] - 95 - (k // 5) * 18
    return x0 + (x1 - x0) * q, y0 + (y1 - y0) * q - 150 * math.sin(math.pi * q)

def in_basket(t):
    n = sum(1 for k in range(10) if t >= COUNT0 + k * COUNT_DT + 2.1)
    return n - sum(1 for i in range(4) if t >= SHARE0 + i * 3.0 + 0.2)

def banana_tree(c, t):
    x = TREE
    c.set_line_cap(cairo.LINE_CAP_ROUND)
    for (col, w) in ((OUT, 62), (hexc('#9CCC65'), 50)):
        c.move_to(x, GROUND); c.curve_to(x - 10, GROUND - 150, x + 10, GROUND - 330, x, GROUND - 520)
        c.set_source_rgba(*col); c.set_line_width(w); c.stroke()
    for i, ang in enumerate((-160, -120, -80, -40, -5, 200)):
        c.save(); c.translate(x, GROUND - 520); c.rotate(math.radians(ang + 4 * math.sin(t * 1.4 + i)))
        c.move_to(0, 0); c.curve_to(70, -80, 240, -80, 320, 0); c.curve_to(240, 45, 70, 45, 0, 0); c.close_path()
        c.set_source_rgba(*hexc('#43A047' if i % 2 else '#66BB6A')); c.fill_preserve()
        c.set_source_rgba(*hexc('#2E7D32')); c.set_line_width(4); c.stroke(); c.restore()
    c.set_source_rgba(*hexc('#558B2F')); c.set_line_width(10); c.move_to(x - 5, GROUND - 500); c.curve_to(x - 60, GROUND - 470, x - 10, GROUND - 400, x, GROUND - 300); c.stroke()
    for k, (bx, by) in enumerate(BANANAS):
        if not picked(k, t):
            wob = 0.08 * math.sin(t * 6) if coco_hand_target(t) == (bx, by) else 0
            K.banana(c, bx, by, 1.0, -1.2 + 0.25 * (k % 3) + wob)

def basket(c, t, front):
    x, y = BASKET
    if not front:
        c.move_to(x - 95, y - 90); c.curve_to(x - 95, y - 210, x + 95, y - 210, x + 95, y - 90)
        c.set_source_rgba(*OUT); c.set_line_width(14); c.stroke()
        c.move_to(x - 95, y - 90); c.curve_to(x - 95, y - 210, x + 95, y - 210, x + 95, y - 90)
        c.set_source_rgba(*hexc('#A1887F')); c.set_line_width(8); c.stroke()
        n = in_basket(t)
        for k in range(n):
            K.banana(c, x + (k % 5 - 2) * 30, y - 95 - (k // 5) * 20, 0.85, -0.3 + 0.15 * (k % 3))
    else:
        c.move_to(x - 105, y - 95); c.line_to(x + 105, y - 95); c.line_to(x + 80, y); c.line_to(x - 80, y); c.close_path()
        fill(c, hexc('#D7A86E'), OUT, 5)
        c.save(); c.move_to(x - 105, y - 95); c.line_to(x + 105, y - 95); c.line_to(x + 80, y); c.line_to(x - 80, y); c.close_path(); c.clip()
        for k in range(-5, 6):
            c.move_to(x + k * 22, y - 100); c.line_to(x + k * 22 - 10, y + 5); c.set_source_rgba(*hexc('#A1887F')); c.set_line_width(4); c.stroke()
        for j in range(1, 4):
            c.move_to(x - 110, y - 95 + j * 24); c.line_to(x + 110, y - 95 + j * 24); c.stroke()
        c.restore()

def heart(c, x, y, s, a=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.move_to(0, 18); c.curve_to(-40, -10, -22, -42, 0, -22); c.curve_to(22, -42, 40, -10, 0, 18); c.close_path()
    c.set_source_rgba(*hexc('#FF4081', a)); c.fill_preserve(); c.set_source_rgba(*hexc('#3B2314', a)); c.set_line_width(3); c.stroke()
    c.restore()

def friend_pos(name, t):
    base = dict(FRIENDS)[name]
    if name == 'lola':
        return kf(t, [(60, -200), (64, base)]) + 40 * math.sin(t * 0.7), 470 + 15 * math.sin(t * 3)
    return kf(t, [(60, -400), (66, base)]), GROUND

def party(t): return 91 < t < 99

def world(c, t):
    c.set_source_surface(SKY, 0, 0); c.paint()
    sun(c, t)
    for (x0, y0, s, sp) in ((150, 160, 0.9, 10), (700, 110, 0.7, 7)):
        cloud(c, (x0 + sp * t) % 2300 - 250, y0, s)
    c.set_source_surface(LAND, 0, 0); c.paint()
    banana_tree(c, t)
    if t > 13: basket(c, t, front=False)
    bounce = lambda ph: -25 * abs(math.sin(t * 4.5 + ph)) if party(t) else 0
    # friends
    for name, _ in FRIENDS:
        if t < 60: continue
        fx, fy = friend_pos(name, t)
        got = t >= SHARE0 + [n for n, _ in FRIENDS].index(name) * 3.0 + 1.1
        lk = (1, 0)
        if name == 'tito': K.put(c, K.tito, fx, fy + bounce(1), 0.6, t=t, look=lk, walk=t * 6 if t < 66 else 0, hold='banana' if got else None)
        if name == 'pipa': K.put(c, K.pipa, fx, fy + bounce(0.5), 0.55, t=t, look=lk, walk=t * 7 if t < 66 else 0, hold='banana' if got else None)
        if name == 'tomi': K.put(c, K.tomi, fx, fy + bounce(1.5), 0.55, t=t, look=lk, walk=t * 3 if t < 66 else 0, hold='banana' if got else None)
        if name == 'lola': K.put(c, K.lola, fx, fy + bounce(2), 0.5, t=t, flap=20, look=(1, 0.5), hold='banana' if got else None)
    # Papá + Coco
    px = papa_x(t); cx, cy = coco_place(t)
    hug = 84.5 < t < 90.5
    blink = 0.0
    for bt in (3.0, 15.0, 33.0, 47.0, 64.0, 78.0, 95.0):
        if abs(t - bt) < 0.12: blink = 1 - abs(t - bt) / 0.12
    # Coco's arms & mood
    mood, look = 'smile', (0.6, -0.2)
    arm_r, arm_l = math.radians(65 + 6 * math.sin(t * 2)), math.radians(115 - 6 * math.sin(t * 2))
    if t < 12: arm_l = math.radians(160)   # holding Papá's hand
    if 13 < t < 18.5:
        look = (1, -1); arm_r, arm_l = math.radians(-70), math.radians(-110)
        jumpc = 70 * abs(math.sin((t - 13) * math.pi / 1.1)) if 14 < t < 17.5 else 0
        cy -= jumpc
        if t > 16.5: mood = 'sad'
    tgt = coco_hand_target(t)
    if on_shoulders(t):
        look = (1, -0.7)
        if tgt:
            sx, sy = cx + 0.55 * 78, cy - 0.55 * 180
            arm_r = math.atan2(tgt[1] - sy, tgt[0] - sx)
            arm_len = min(200, math.hypot(tgt[0] - sx, tgt[1] - sy) / 0.55)
        arm_l = math.radians(-120)
    if 56.5 < t < 60: mood = 'o' if t < 58 else 'smile'
    if 70 < t < 82: look = (-1, 0); arm_r = math.radians(-60) if any(SHARE0 + i * 3 <= t < SHARE0 + i * 3 + 1 for i in range(4)) else arm_r
    if party(t): arm_r, arm_l = math.radians(-58 + 25 * math.sin(t * 9)), math.radians(-122 - 25 * math.sin(t * 9))
    arm_len = 115
    if on_shoulders(t) and tgt:
        sx, sy = cx + 0.55 * 78, cy - 0.55 * 180
        arm_len = max(115, min(220, math.hypot(tgt[0] - sx, tgt[1] - sy) / 0.55 - 20))
    # Papá's arms & mood
    p_arm_r, p_arm_l = math.radians(65 + 5 * math.sin(t * 2)), math.radians(115 - 5 * math.sin(t * 2))
    if t < 12: p_arm_r = math.radians(20)
    if 18.5 < t < 56.6: p_arm_r, p_arm_l = math.radians(-75), math.radians(-105)
    if hug: p_arm_r, p_arm_l = math.radians(170), math.radians(10)
    if party(t): p_arm_r, p_arm_l = math.radians(-58 + 25 * math.sin(t * 9 + 1)), math.radians(-122 - 25 * math.sin(t * 9 + 1))
    p_look = (1, -0.5) if 13 < t < 19 else ((-0.2, -1) if on_shoulders(t) else (-0.8, 0))
    coco_kw = dict(t=t, mood='closed' if hug else mood, look=look, lid=blink, arm_r=arm_r, arm_l=arm_l, arm_len=arm_len,
                   walk=t * 8 if (moving(t, [(5, -150), (12, PAPA_STOP + 150)]) or 57.7 < t < 59 or 84 < t < 85) else 0)
    if hug: coco_kw.update(arm_r=math.radians(10), arm_l=math.radians(170))
    if on_shoulders(t) or 19 <= t < 20.2:
        K.put(c, K.coco, cx, cy + bounce(0), 0.55, **coco_kw)          # behind Papá's head
        K.put(c, K.papa, px, GROUND, 0.72, t=t, look=p_look, arm_r=p_arm_r, arm_l=p_arm_l,
              walk=t * 7 if moving(t, [(5, -300), (12, PAPA_STOP)]) else 0)
    else:
        K.put(c, K.papa, px, GROUND + bounce(0.8), 0.72, t=t, look=p_look, lid=blink, arm_r=p_arm_r, arm_l=p_arm_l, mood='closed' if hug else 'smile',
              walk=t * 7 if (moving(t, [(5, -300), (12, PAPA_STOP)]) or 56.5 < t < 58) else 0)
        K.put(c, K.coco, cx, cy + bounce(0), 0.55, **coco_kw)
    if t > 13: basket(c, t, front=True)
    for k in range(10):
        p = banana_flight(k, t)
        if p: K.banana(c, p[0], p[1], 1.0, (t - COUNT0) * 6)
    # sharing
    for i, (name, _) in enumerate(FRIENDS):
        q = (t - SHARE0 - i * 3.0 - 0.2) / 0.9
        if 0 <= q < 1:
            fx, fy = friend_pos(name, t)
            ty = {'tito': GROUND - 140, 'pipa': GROUND - 330, 'tomi': GROUND - 100, 'lola': fy - 60}[name]
            x0, y0 = BASKET[0], BASKET[1] - 110
            K.banana(c, x0 + (fx - x0) * q, y0 + (ty - y0) * q - 160 * math.sin(math.pi * q), 0.9, q * 8)
    # hearts during the hug
    if hug:
        for k in range(5):
            ph = ((t - 84.5) * 0.5 + k / 5) % 1
            heart(c, (px + cx) / 2 + 120 * math.sin(k * 1.7) , GROUND - 380 - 260 * ph, 0.9 + 0.6 * ph, math.sin(math.pi * ph))
    if party(t):
        lx, ly = friend_pos('lola', t)
        for k in range(3):
            ph = (t * 0.7 + k / 3) % 1
            music_note(c, lx + 40 + 60 * ph, ly - 150 - 160 * ph, math.sin(math.pi * ph), ['#E91E63', '#1E88E5', '#FF9800'][k])
    bubble(c, px, GROUND - 0.72 * 470, '¡Vamos, hijo!', (t - 7.0) / 3.0, 46)
    bubble(c, cx, GROUND - 300, '¡No llego!', (t - 16.0) / 2.6, 50)
    bubble(c, px, GROUND - 0.72 * 470 - 100, '¡Arriba!', (t - 18.2) / 2.4, 50)
    bubble(c, cx, GROUND - 300, '¡Para compartir!', (t - 66.2) / 3.2, 46)
    bubble(c, (px + cx) / 2, GROUND - 400, '¡Te quiero, papá!', (t - 86.0) / 4.0, 50)

def overlay(c, t):
    if t < 5.6:
        a = 1 - ss(4.8, 5.5, t)
        c.push_group()
        word(c, 'A contar bananas', W / 2, 200, 115 * K_back((t - 0.6) / 0.6) + 0.01, tilt=0.05, outline=9)
        word(c, 'con Papá Coco', W / 2, 330, 115 * K_back((t - 0.8) / 0.6) + 0.01, start=3, tilt=0.05, outline=9)
        c.pop_group_to_source(); c.paint_with_alpha(a)
    for k in range(10):
        t0 = COUNT0 + k * COUNT_DT + 1.1
        if t0 <= t < t0 + 2.1:
            s = K_back((t - t0) / 0.35) * (1 - ss(t0 + 1.8, t0 + 2.1, t))
            word(c, str(k + 1), 560, 360, 260 * s + 0.01, colors=[['#FF4081', '#FF9100', '#FFD600', '#00C853', '#00B0FF', '#AA00FF'][k % 6]], outline=14)
    # counter of bananas, top-right
    if COUNT0 < t < 60:
        n = sum(1 for k in range(10) if t >= COUNT0 + k * COUNT_DT + 2.1)
        for k in range(10):
            bx, by = 80 + (k % 5) * 70, 60 + (k // 5) * 75
            if k < n: K.banana(c, bx, by, 0.65, -0.3)
            else: ellipse(c, bx, by, 18, 18); c.set_source_rgba(1, 1, 1, 0.5); c.fill()
    if t > 91:
        s = K_back((t - 91) / 0.7)
        word(c, '¡Te quiero,', W / 2, 180, 125 * s + 0.01, tilt=0.06, outline=10)
        word(c, 'papá!', W / 2, 320, 135 * s + 0.01, start=3, tilt=0.06, outline=10)
    a = max(1 - ss(0, 0.8, t), ss(DUR - 2.0, DUR, t))
    if a > 0: c.set_source_rgba(1, 1, 1, a); c.paint()

CAM = [(0, 1.0, 960, 540), (12, 1.0, 960, 540), (14, 1.2, 1250, 600), (21, 1.2, 1300, 560), (22.5, 1.0, 960, 540),
       (56, 1.0, 960, 540), (84, 1.0, 960, 540), (85.5, 1.35, 1060, 600), (90, 1.35, 1060, 600), (91.5, 1.0, 960, 540)]
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
            c.save(); frame(c, t); c.restore(); surf.write_to_png(f'ep14_{t}.png')
    else:
        t0, t1 = (float(args[1]), float(args[2])) if args and args[0] == 'range' else (0, DUR)
        out = sys.stdout.buffer
        for i in range(int(round(t0 * FPS)), int(round(t1 * FPS))):
            c.save(); frame(c, i / FPS); c.restore(); surf.flush(); out.write(surf.get_data())
