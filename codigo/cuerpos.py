"""Cuerpos completos de los personajes (estilo oficial del canal).
Cada función dibuja al personaje con el origen en el centro de los pies, mirando de frente.
Las cabezas salen de amigos.py, así todo se ve igual en cada video."""
import math, cairo
import amigos as A
from amigos import hexc, ellipse, fill, OUT

BROWN, BEIGE = hexc('#A0582C'), hexc('#FFD9A8')
YEL_BANANA = hexc('#FFE135')

# ---------------- objetos ----------------
def banana(c, x, y, s=1.0, rot=0.0):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    c.move_to(-40, -10); c.curve_to(-20, 30, 30, 30, 45, -15)
    c.curve_to(30, 8, -15, 10, -40, -10); c.close_path()
    fill(c, YEL_BANANA, OUT, 4)
    ellipse(c, -41, -11, 5, 5); fill(c, hexc('#5D4037'))
    ellipse(c, 46, -16, 4, 4); fill(c, hexc('#5D4037'))
    c.restore()

def bunch(c, x, y, s=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    for k, a in enumerate((-0.9, -0.45, 0.0, 0.45, 0.9)):
        c.save(); c.rotate(a); banana(c, 0, 55, 1.0, -1.57 + 0.35); c.restore()
    ellipse(c, 0, 0, 14, 14); fill(c, hexc('#7CB342'), OUT, 4)
    c.restore()

# ---------------- Coco ----------------
def _arm(c, sx, sy, ang, L=115):
    hx, hy = sx + L * math.cos(ang), sy + L * math.sin(ang)
    c.set_line_cap(cairo.LINE_CAP_ROUND)
    c.move_to(sx, sy); c.line_to(hx, hy); c.set_source_rgba(*OUT); c.set_line_width(46); c.stroke()
    c.move_to(sx, sy); c.line_to(hx, hy); c.set_source_rgba(*BROWN); c.set_line_width(34); c.stroke()
    ellipse(c, hx, hy, 26, 26); fill(c, BEIGE, OUT, 6)
    return hx, hy

def _coco_eyes(c, look, lid, sad):
    for ex in (-48, 48):
        if lid > 0.9:
            c.set_source_rgba(*OUT); c.set_line_width(7); c.set_line_cap(cairo.LINE_CAP_ROUND)
            c.arc(ex, -18, 24, 0.15 * math.pi, 0.85 * math.pi); c.stroke(); continue
        ellipse(c, ex, -15, 34, 42); fill(c, (1, 1, 1, 1))
        ellipse(c, ex + look[0] * 10, -12 + look[1] * 10, 19, 21); fill(c, hexc('#1A1A1A'))
        ellipse(c, ex + look[0] * 10 + 7, -20 + look[1] * 10, 7, 7); c.set_source_rgba(1, 1, 1, 1); c.fill()
        if lid > 0.01:
            c.save(); ellipse(c, ex, -15, 34, 42); c.clip()
            c.rectangle(ex - 40, -60, 80, 84 * lid + 3); c.set_source_rgba(*hexc('#E9B57E')); c.fill(); c.restore()
        ellipse(c, ex, -15, 34, 42); c.set_source_rgba(*OUT); c.set_line_width(5); c.stroke()
    if sad > 0:
        c.set_source_rgba(*OUT); c.set_line_width(7); c.set_line_cap(cairo.LINE_CAP_ROUND)
        for sx in (-1, 1):
            c.move_to(sx * 25, -72 - 6 * sad); c.line_to(sx * 70, -62 + 6 * sad); c.stroke()

def _coco_mouth(c, mood, chew=0.0):
    if mood == 'smile':
        A.open_smile(c)
    elif mood == 'sad':
        c.set_source_rgba(*OUT); c.set_line_width(7); c.set_line_cap(cairo.LINE_CAP_ROUND)
        c.arc(0, 100, 30, 1.25 * math.pi, 1.75 * math.pi); c.stroke()
    elif mood == 'o':
        ellipse(c, 0, 75, 20, 26); fill(c, hexc('#B71C1C'), OUT, 6)
    elif mood == 'chew':
        w = 30 + 8 * math.sin(chew * 12)
        c.set_source_rgba(*OUT); c.set_line_width(7); c.set_line_cap(cairo.LINE_CAP_ROUND)
        c.move_to(-w, 62); c.curve_to(-w / 2, 80, w / 2, 80, w, 62); c.stroke()
        ellipse(c, 70, 60, 18 + 4 * math.sin(chew * 12), 14); c.set_source_rgba(*hexc('#E9B57E')); c.fill()
    else:  # 'closed'
        c.set_source_rgba(*OUT); c.set_line_width(7); c.set_line_cap(cairo.LINE_CAP_ROUND)
        c.arc(0, 50, 30, 0.25 * math.pi, 0.75 * math.pi); c.stroke()

def coco(c, t=0.0, look=(0, 0), lid=0.0, mood='smile', sad=0.0, arm_r=1.13, arm_l=2.0,
         walk=0.0, head_tilt=0.0, hold=None, chew=0.0, arm_len=115):
    """walk: fase de caminata (0 = quieto). arm_r / arm_l: ángulo en radianes desde el hombro.
    hold: None | 'banana' | 'bunch' (en la mano derecha)."""
    tw = math.sin(t * 2.2)
    c.set_line_cap(cairo.LINE_CAP_ROUND)
    path = lambda: (c.move_to(60, -70), c.curve_to(200, -60, 230 + 20 * tw, -220, 160 + 15 * tw, -260),
                    c.curve_to(110 + 10 * tw, -290, 90, -230, 130 + 10 * tw, -215))
    path(); c.set_source_rgba(*OUT); c.set_line_width(36); c.stroke()
    path(); c.set_source_rgba(*BROWN); c.set_line_width(24); c.stroke()
    for k, lx in enumerate((-50, 50)):
        lift = max(0.0, math.sin(walk + k * math.pi)) * 22 if walk else 0
        ellipse(c, lx, -18 - lift, 44, 26); fill(c, BEIGE, OUT, 6)
    ellipse(c, 0, -120, 98, 112); fill(c, BROWN, OUT, 6)
    ellipse(c, 0, -110, 64, 78); fill(c, BEIGE)
    c.save(); c.translate(0, -245); c.rotate(head_tilt); c.translate(0, -90)
    for ex in (-1, 1):
        ellipse(c, ex * 138, -5, 52, 52); fill(c, BROWN, OUT, 6)
        ellipse(c, ex * 138, -5, 30, 30); fill(c, BEIGE)
    for i, dx in enumerate((-22, 0, 22)):
        ellipse(c, dx, -140 - (10 if i == 1 else 0), 18, 26); fill(c, BROWN, OUT, 5)
    ellipse(c, 0, 0, 138, 132); fill(c, BROWN, OUT, 6)
    for ex in (-50, 50): ellipse(c, ex, -10, 62, 64)
    ellipse(c, 0, 55, 98, 66); c.set_source_rgba(*BEIGE); c.fill()
    _coco_eyes(c, look, lid, sad)
    for nx in (-13, 13): ellipse(c, nx, 32, 6, 8); fill(c, OUT)
    _coco_mouth(c, mood, chew)
    A.cheeks(c)
    c.restore()
    _arm(c, -78, -180, arm_l, arm_len)
    hx, hy = _arm(c, 78, -180, arm_r, arm_len)
    if hold == 'banana': banana(c, hx + 15, hy - 30, 1.7, -0.6)
    elif hold == 'bunch': bunch(c, hx, hy - 10, 1.4)

# ---------------- Tito ----------------
TITO_BLUE = hexc('#8FB8E8')
def tito_trunk_tip(reach):
    return (reach, -60)

def tito_big_ears(c, u, t=0.0):
    """Orejas abiertas como paraguas (u de 0 a 1), en coordenadas de la cabeza."""
    PINK = hexc('#F8BBD0')
    flap = 0.03 * math.sin(t * 3)
    for s in (-1, 1):
        c.save(); c.scale(s, 1); c.rotate(-flap)
        ox, oy = 90, -60
        c.move_to(ox, oy - 30)
        c.curve_to(ox + 120 + 120 * u, oy - 150 - 120 * u, ox + 330 + 260 * u, oy - 140 - 120 * u, ox + 330 + 330 * u, oy + 60 - 140 * u)
        c.curve_to(ox + 260 + 220 * u, oy + 140 - 120 * u, ox + 100, oy + 150 - 30 * u, ox + 10, oy + 120)
        c.close_path(); fill(c, TITO_BLUE, OUT, 6)
        c.move_to(ox + 25, oy - 5)
        c.curve_to(ox + 120 + 100 * u, oy - 110 - 100 * u, ox + 290 + 220 * u, oy - 100 - 100 * u, ox + 290 + 280 * u, oy + 50 - 120 * u)
        c.curve_to(ox + 230 + 180 * u, oy + 110 - 100 * u, ox + 100, oy + 115 - 30 * u, ox + 30, oy + 95)
        c.close_path(); fill(c, PINK)
        c.restore()

def tito(c, t=0.0, look=(0, 0), reach=None, walk=0.0, hold=None, umbrella=0.0):
    """reach: largo de la trompa hacia la derecha en unidades locales (None = trompa normal)."""
    for k, lx in enumerate((-75, 75)):
        lift = max(0.0, math.sin(walk + k * math.pi)) * 18 if walk else 0
        c.rectangle(lx - 38, -130 - lift, 76, 125); fill(c, TITO_BLUE, OUT, 6)
        ellipse(c, lx, -8 - lift, 40, 14); fill(c, TITO_BLUE, OUT, 6)
        for nx in (-18, 0, 18):
            ellipse(c, lx + nx, -12 - lift, 8, 6); fill(c, (1, 1, 1, 1))
    ellipse(c, 0, -175, 160, 115); fill(c, TITO_BLUE, OUT, 6)
    c.save(); c.translate(0, -340)
    if umbrella > 0: tito_big_ears(c, umbrella, t)
    A.tito(c, look, trunk=False, ears=umbrella <= 0); c.restore()
    # trunk
    end = 150 if reach is None else max(150, reach)
    c.set_line_cap(cairo.LINE_CAP_ROUND)
    def tr():
        c.move_to(0, -320); c.curve_to(0, -200, 50, -70, 140, -60); c.line_to(end, -60)
        if reach is None:
            c.curve_to(end + 30, -60, end + 45, -90, end + 30, -115)
    tr(); c.set_source_rgba(*OUT); c.set_line_width(60); c.stroke()
    tr(); c.set_source_rgba(*TITO_BLUE); c.set_line_width(46); c.stroke()
    c.set_source_rgba(*OUT); c.set_line_width(4)
    x = 170
    while x < end - 20:
        c.move_to(x, -80); c.line_to(x + 4, -42); c.stroke(); x += 70
    tip = (end + 30, -115) if reach is None else (end, -60)
    if hold == 'banana': banana(c, tip[0] + 15, tip[1] - 40, 1.7, -0.9)
    return tip

# ---------------- Pipa ----------------
P_YEL, P_SPOT = hexc('#FFCF40'), hexc('#F08A24')
def pipa(c, t=0.0, look=(0, 0), neck=300, lean=0.0, walk=0.0, hold=None):
    for k, (lx, front) in enumerate(((-80, 0), (80, 0), (-35, 1), (35, 1))):
        lift = max(0.0, math.sin(walk + k * math.pi / 2)) * 14 if walk else 0
        c.set_line_cap(cairo.LINE_CAP_ROUND)
        c.move_to(lx, -190); c.line_to(lx, -20 - lift); c.set_source_rgba(*OUT); c.set_line_width(36); c.stroke()
        c.move_to(lx, -190); c.line_to(lx, -20 - lift); c.set_source_rgba(*P_YEL); c.set_line_width(24); c.stroke()
        ellipse(c, lx, -14 - lift, 18, 12); fill(c, hexc('#8D5524'), OUT, 4)
    ellipse(c, 0, -215, 125, 80); fill(c, P_YEL, OUT, 6)
    c.save(); ellipse(c, 0, -215, 125, 80); c.clip()
    for (sx, sy, r) in ((-70, -240, 22), (40, -200, 26), (-20, -260, 15), (85, -250, 15)):
        ellipse(c, sx, sy, r, r * 0.8); c.set_source_rgba(*P_SPOT); c.fill()
    c.restore()
    hx, hy = lean, -260 - neck
    def nk():
        c.move_to(0, -250); c.curve_to(0, -250 - neck * 0.5, hx * 0.7, hy + neck * 0.3, hx, hy + 60)
    c.set_line_cap(cairo.LINE_CAP_ROUND)
    nk(); c.set_source_rgba(*OUT); c.set_line_width(74); c.stroke()
    nk(); c.set_source_rgba(*P_YEL); c.set_line_width(60); c.stroke()
    for k in range(1, 4):
        u = k / 4
        px = 3 * (1 - u) * u * u * hx * 0.7 + u ** 3 * hx
        py = (1 - u) ** 3 * -250 + 3 * (1 - u) ** 2 * u * (-250 - neck * 0.5) + 3 * (1 - u) * u * u * (hy + neck * 0.3) + u ** 3 * (hy + 60)
        ellipse(c, px + (8 if k % 2 else -8), py, 12, 10); c.set_source_rgba(*P_SPOT); c.fill()
    c.save(); c.translate(hx, hy); c.scale(0.85, 0.85); A.pipa(c, look); c.restore()
    if hold == 'banana': banana(c, hx + 30, hy + 120, 1.6, 0.3)
    return hx, hy

# ---------------- Tomi ----------------
def tomi_shell(c):
    """Tomi escondido: solo se ve el caparazón (parece una piedra)."""
    c.move_to(-200, -20); c.curve_to(-200, -250, 200, -250, 200, -20); c.close_path()
    fill(c, hexc('#8D6E63'), OUT, 6)
    c.save(); c.move_to(-200, -20); c.curve_to(-200, -250, 200, -250, 200, -20); c.close_path(); c.clip()
    for (hx, hy) in ((-110, -60), (0, -140), (110, -60), (0, -40), (-70, -150), (70, -150)):
        ellipse(c, hx, hy, 46, 34); c.set_source_rgba(*hexc('#BCAAA4')); c.fill()
    c.restore()
    c.rectangle(-205, -30, 410, 26); fill(c, hexc('#6D4C41'), OUT, 5)

def tomi(c, t=0.0, look=(0, 0), walk=0.0, hold=None, hide=0.0, lid=0.0, mood='smile'):
    """hide: 0 = afuera, 1 = escondido en el caparazón. lid/mood sirven al despertarse."""
    G = hexc('#7CCB5B')
    if hide > 0:
        tomi_shell(c)
        c.save(); c.rectangle(-300, -600, 600, 590); c.clip()
        c.translate(0, -165 + 300 * hide); A.tomi(c, look, shell=False)
        if lid > 0:
            for ex in (-48, 48):
                c.save(); ellipse(c, ex, -25, 32, 40); c.clip()
                c.rectangle(ex - 40, -70, 80, 84 * lid); c.set_source_rgba(*hexc('#6DB84E')); c.fill(); c.restore()
                c.move_to(ex - 32, -67 + 84 * lid); c.line_to(ex + 32, -67 + 84 * lid)
                c.set_source_rgba(*OUT); c.set_line_width(5); c.stroke()
        if mood == 'o':
            ellipse(c, 0, 70, 26, 34); fill(c, hexc('#B71C1C'), OUT, 5)
        c.restore()
        return
    for k, (fx, fy) in enumerate(((-150, -12), (150, -12), (-70, -6), (70, -6))):
        lift = max(0.0, math.sin(walk + k * math.pi / 2)) * 10 if walk else 0
        ellipse(c, fx, fy - lift, 34, 20); fill(c, G, OUT, 5)
    c.save(); c.translate(0, -150); A.tomi(c, look); c.restore()
    if hold == 'banana': banana(c, 110, -100, 1.5, -0.3)

# ---------------- Lola ----------------
def lola(c, t=0.0, look=(0, 0), flap=None, hold=None):
    """flap: velocidad de aleteo (None = alas quietas)."""
    RED = hexc('#E53935')
    for k, (col, a) in enumerate((('#1E88E5', -0.3), ('#FDD835', 0.0), ('#E53935', 0.3))):
        c.save(); c.translate(0, -60); c.rotate(a)
        ellipse(c, 0, 60, 18, 55); fill(c, hexc(col), OUT, 5); c.restore()
    w = 0.5 + 0.5 * math.sin(t * flap) if flap else 0.15
    for side in (-1, 1):
        c.save(); c.translate(side * 55, -140); c.rotate(side * (0.4 - 1.3 * w)); c.scale(side, 1)
        c.move_to(0, 0); c.curve_to(60, -30, 150, 0, 150, 60); c.curve_to(90, 60, 30, 70, 0, 40); c.close_path()
        fill(c, hexc('#1E88E5'), OUT, 5)
        c.move_to(20, 20); c.curve_to(60, 0, 120, 20, 130, 52); c.curve_to(80, 52, 40, 55, 20, 40); c.close_path()
        c.set_source_rgba(*hexc('#FDD835')); c.fill()
        c.restore()
    ellipse(c, 0, -105, 70, 85); fill(c, RED, OUT, 6)
    for fx in (-22, 22):
        c.set_source_rgba(*hexc('#FF9800')); c.set_line_width(10); c.set_line_cap(cairo.LINE_CAP_ROUND)
        c.move_to(fx, -25); c.line_to(fx, -5); c.stroke()
    c.save(); c.translate(0, -230); c.scale(0.7, 0.7); A.lola(c, look); c.restore()
    if hold == 'banana': banana(c, 90, -115, 1.6, -0.4)

# ---------------- dibujar con posición y escala ----------------
SCALE = {'coco': 0.55, 'tito': 0.6, 'pipa': 0.55, 'tomi': 0.55, 'lola': 0.5}
def put(c, fn, x, y, s, flip=False, rot=0.0, sq=1.0, **kw):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s * (-1 if flip else 1) / sq, s * sq)
    r = fn(c, **kw); c.restore(); return r
