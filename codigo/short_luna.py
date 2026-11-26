"""Short — ¡Se apagó la luna! (vertical, 40 s, plantilla nueva: gancho en el cuadro 1 + tarjeta final).
Fórmula ganadora del canal (nov 2026): noche + luz que brilla + un problema + una pregunta.
La luna se apagó y está todo oscuro. Los amigos se asustan... Luz, la luciérnaga, trae a sus amigas
y entre todas llenan la luna de lucecitas: ¡la luna se vuelve a encender y les sonríe!
Uso: python3 short_luna.py [short a b] | stills 0 12 | portada"""
import cairo, math, sys, random
import cuerpos as K
from amigos import hexc, ellipse, fill, OUT
from logos import word, sparkle
from ep02_puente_del_rio import kf, ss, K_back, music_note
from ep03_donde_esta_tomi import bubble
from ep19_luciernaga import luz, glow, tiny
from short_kit import SW, SH, FPS, END, top_title, end_card, logo_band

STORY = 37.0
DUR = STORY + END
FLOOR = 1540
MOON = (540, 760)
MR = 190
rnd = random.Random(4)
STARS = [(rnd.uniform(0, SW), rnd.uniform(380, 1250), rnd.uniform(2, 4.5), rnd.uniform(0, 6)) for _ in range(70)]
N = 30
FF = [(rnd.uniform(-1, 1), rnd.uniform(-1, 1), rnd.uniform(0, 6.28)) for _ in range(N)]

def moon_on(t): return ss(24.0, 27.5, t)
def dark(t): return 0.55 * (1 - moon_on(t))

def moon(c, t, on):
    x, y = MOON
    if on > 0: glow(c, x, y, 520, on * 0.8, (1, 1, 0.75))
    col = tuple(a + (b - a) * on for a, b in zip((0.35, 0.36, 0.5), (1.0, 0.97, 0.7)))
    ellipse(c, x, y, MR, MR); fill(c, col + (1,), hexc('#3B2314'), 7)
    for (dx, dy, r) in ((-70, -60, 30), (60, -80, 18), (80, 50, 26), (-40, 90, 16)):
        ellipse(c, x + dx, y + dy, r, r); c.set_source_rgba(0.85 * col[0], 0.85 * col[1], 0.6 * col[2] + 0.1, 0.8); c.fill()
    # cara
    c.set_source_rgba(*OUT); c.set_line_width(9); c.set_line_cap(cairo.LINE_CAP_ROUND)
    if on < 0.5:
        for ex in (-60, 60):
            c.arc(x + ex, y - 10, 24, 0.15 * math.pi, 0.85 * math.pi); c.stroke()
        c.arc(x, y + 80, 30, 1.2 * math.pi, 1.8 * math.pi); c.stroke()          # triste
    else:
        for ex in (-60, 60):
            ellipse(c, x + ex, y - 20, 16, 22); c.fill()
            ellipse(c, x + ex + 5, y - 28, 6, 6); c.set_source_rgba(1, 1, 1, 1); c.fill(); c.set_source_rgba(*OUT)
        c.arc(x, y + 30, 55, 0.15 * math.pi, 0.85 * math.pi); c.stroke()
        for ex in (-105, 105): ellipse(c, x + ex, y + 40, 26, 15); c.set_source_rgba(*hexc('#FF8A80', 0.75 * on)); c.fill()

def ff_pos(k, t):
    """luciérnagas: vienen de lejos (14–20), forman un anillo en la luna (20–25) y después revolotean."""
    u, v, ph = FF[k]
    sx, sy = SW / 2 + 900 * u, 1500 + 400 * v
    a = 2 * math.pi * k / N + 0.25 * t
    rx, ry = MOON[0] + (MR - 30) * math.cos(a), MOON[1] + (MR - 30) * math.sin(a)
    q1 = ss(14.0 + 0.12 * k, 19.0 + 0.12 * k, t)
    q2 = ss(28.0, 31.0, t)
    fx, fy = MOON[0] + 420 * math.cos(a * 1.7 + ph), MOON[1] + 380 * math.sin(a * 1.3 + ph)
    x = sx + (rx - sx) * q1; y = sy + (ry - sy) * q1
    return x + (fx - x) * q2, y + (fy - y) * q2, q1

def frame(c, t):
    if t >= STORY:
        end_card(c, t - STORY); return
    on = moon_on(t)
    g = cairo.LinearGradient(0, 0, 0, SH)
    top = tuple(a + (b - a) * on for a, b in zip((0.03, 0.03, 0.1), (0.07, 0.06, 0.28)))
    bot = tuple(a + (b - a) * on for a, b in zip((0.08, 0.07, 0.2), (0.24, 0.2, 0.52)))
    g.add_color_stop_rgb(0, *top); g.add_color_stop_rgb(0.85, *bot); c.set_source(g); c.paint()
    for (x, y, r, ph) in STARS:
        a = (0.15 + 0.85 * on) * (0.5 + 0.5 * math.sin(t * 2 + ph))
        ellipse(c, x, y, r, r); c.set_source_rgba(1, 1, 0.85, a); c.fill()
    moon(c, t, on)
    # siluetas de selva
    for (x, s) in ((60, 1.0), (1010, 1.1)):
        c.move_to(x, FLOOR); c.curve_to(x + 5, FLOOR - 200, x + 20, FLOOR - 380, x + 40, FLOOR - 470)
        c.set_source_rgba(*hexc('#0E1E17')); c.set_line_width(34); c.stroke()
        for a in (-165, -125, -85, -45, -10):
            c.save(); c.translate(x + 40, FLOOR - 470); c.rotate(math.radians(a + 4 * math.sin(t * 0.7)))
            c.move_to(0, 0); c.curve_to(70, -45, 180, -35, 250, 30); c.curve_to(170, 14, 70, 20, 0, 0); c.close_path()
            c.set_source_rgba(*hexc('#0E1E17')); c.fill(); c.restore()
    c.rectangle(0, FLOOR - 10, SW, SH); c.set_source_rgba(*hexc('#1F4030')); c.fill()
    # amigos
    scared = 3.0 < t < 13.5
    party = t > 28.0
    bob = lambda ph: -20 * abs(math.sin(t * 4.5 + ph)) if party else (-6 * abs(math.sin(t * 20 + ph)) if scared else 0)
    K.put(c, K.tito, 230, FLOOR + bob(1.0), 0.78, t=t, look=(1, -0.6), lid=0.0, umbrella=0.0)
    K.put(c, K.tomi, 820, FLOOR + bob(1.5), 0.72, t=t, look=(-1, -0.6), hide=0.8 * ss(4.0, 5.0, t) * (1 - ss(20.0, 21.0, t)))
    ar, al = math.radians(65), math.radians(115); mood = 'o'
    if scared: ar, al = math.radians(-100), math.radians(-80)       # se tapa la cara
    if 20.0 < t < 28.0: mood = 'o'; ar, al = math.radians(-60), math.radians(-120)
    if party: mood = 'smile'; ar, al = math.radians(-58 + 25 * math.sin(t * 9)), math.radians(-122 - 25 * math.sin(t * 9))
    K.put(c, K.coco, 540, FLOOR + 20 + bob(0), 0.85, t=t, mood=mood, look=(0, -1), arm_r=ar, arm_l=al)
    # oscuridad con huecos de luz
    d = dark(t)
    if d > 0:
        c.push_group(); c.set_source_rgba(0.01, 0.01, 0.06, d); c.paint()
        c.set_operator(cairo.OPERATOR_DEST_OUT)
        lx, ly = kf(t, [(0, 1300), (8.5, 1300), (11.0, 760)]), kf(t, [(0, 900), (8.5, 900), (11.0, 1150)]) + 20 * math.sin(t * 3)
        holes = [(lx, ly, 330 * ss(8.5, 10.0, t))]
        for k in range(N):
            x, y, q = ff_pos(k, t); holes.append((x, y, 120 * q))
        for (hx, hy, r) in holes:
            if r <= 1: continue
            gg = cairo.RadialGradient(hx, hy, 0, hx, hy, r); gg.add_color_stop_rgba(0, 0, 0, 0, 0.9); gg.add_color_stop_rgba(1, 0, 0, 0, 0)
            c.set_source(gg); c.arc(hx, hy, r, 0, 2 * math.pi); c.fill()
        c.set_operator(cairo.OPERATOR_OVER); c.pop_group_to_source(); c.paint()
    # luciérnagas
    for k in range(N):
        x, y, q = ff_pos(k, t)
        if q > 0: tiny(c, x, y, t, k, q)
    if t > 8.5:
        if t < 24.0: lx, ly = kf(t, [(8.5, 1300), (11.0, 760), (13.5, 760), (15.0, 900)]), kf(t, [(8.5, 900), (11.0, 1150), (13.5, 1150), (15.0, 1000)]) + 20 * math.sin(t * 3)
        else: lx, ly = MOON[0] + 260 * math.cos(t * 0.8), MOON[1] + 300 + 60 * math.sin(t * 1.6)
        luz(c, lx, ly, 0.75, t, 1.2, 'smile')
    if 24.0 < t < 28.5:   # la luna se enciende: rayos y brillos
        q = ss(24.0, 28.5, t)
        for k in range(16):
            a = k * math.pi / 8; r = MR + 40 + 380 * q
            sparkle(c, MOON[0] + r * math.cos(a), MOON[1] + r * math.sin(a), 34 * (1 - q) + 4, ('#FFF59D', '#FFFFFF', '#FF80AB', '#80D8FF')[k % 4])
    if party:
        for k in range(3):
            ph = (t * 0.7 + k / 3) % 1
            music_note(c, 860 + 60 * ph, 1100 - 200 * ph, math.sin(math.pi * ph), ['#FFF59D', '#80D8FF', '#FF80AB'][k])
    # globitos
    if t < 3.0:
        bubble(c, 540, FLOOR - 560, '¡Se apagó la luna!', 0.84 + t / 3.0 * 0.16 if t < 2.6 else 1.0 - (t - 2.6) / 0.4 * 0.0, 54)
    bubble(c, 540, FLOOR - 560, '¡Qué oscuro!', (t - 3.2) / 4.0, 56)
    bubble(c, 760, 1010, '¡Yo los ayudo!', (t - 10.6) / 3.2, 50)
    bubble(c, 540, FLOOR - 560, '¡Las luciérnagas!', (t - 17.0) / 3.0, 50)
    bubble(c, 540, FLOOR - 560, '¡Gracias, Luz!', (t - 29.0) / 3.4, 54)
    if t < 8.5: top_title(c, t, 0, '¡Se apagó', 'la luna!', first=True)
    elif t < 14.0: top_title(c, t, 8.5, '¿Quién nos', 'ayuda?')
    elif t < 24.0: top_title(c, t, 14.0, '¡Muchas', 'lucecitas!')
    elif t < 32.0: top_title(c, t, 24.0, '¡Se encendió', 'la luna!')
    else: top_title(c, t, 32.0, '¡Buenas noches,', 'luna!')
    logo_band(c)

if __name__ == '__main__':
    args = sys.argv[1:] or ['short']
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, SW, SH); c = cairo.Context(surf)
    if args[0] == 'stills':
        for t in map(float, args[1:]):
            c.save(); frame(c, t); c.restore(); surf.write_to_png(f'luna_{t}.png')
    elif args[0] == 'portada':
        frame(c, 1.5); surf.write_to_png('short_luna_portada.png')
    else:
        a0, a1 = (float(args[1]), float(args[2])) if len(args) > 2 else (0, DUR)
        out = sys.stdout.buffer
        for i in range(int(round(a0 * FPS)), int(round(a1 * FPS))):
            c.save(); frame(c, i / FPS); c.restore(); surf.flush(); out.write(surf.get_data())
