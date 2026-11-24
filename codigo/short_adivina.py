"""Short — ¿Adivinás quién es? (vertical, 39 s, plantilla nueva: gancho en el cuadro 1 + tarjeta final).
Juego de siluetas: aparece la sombra de un amigo con una pista, cuenta 3, 2, 1... ¡y se revela con su nombre!
Cinco rondas (Pipa, Tito, Lola, Tomi y Coco). Termina invitando a jugar de nuevo.
Uso: python3 short_adivina.py [short a b] | stills 0 12 | portada"""
import cairo, math, sys
import cuerpos as K
from amigos import hexc, ellipse, fill, OUT
from logos import word, sparkle
from ep02_puente_del_rio import ss, K_back
from short_kit import SW, SH, FPS, END, top_title, end_card, logo_band

ROUND = 7.0
# (cuerpo, nombre, pista, colores del nombre, escala, y de los pies, kwargs)
CAST = [(K.pipa, '¡Pipa!', 'Tiene el cuello\nmuy largo…', ['#FFB300', '#FF7043'], 0.95, 1560, dict(look=(0, 0))),
        (K.tito, '¡Tito!', 'Tiene orejas\ngrandotas…', ['#42A5F5', '#7E57C2'], 1.15, 1560, dict(look=(0, 0))),
        (K.lola, '¡Lola!', '¡Le encanta\ncantar!', ['#E53935', '#43A047'], 1.25, 1250, dict(look=(0, 0), flap=20)),
        (K.tomi, '¡Tomi!', 'Lleva su casita\nen la espalda…', ['#43A047', '#8BC34A'], 1.35, 1540, dict(look=(0, 0))),
        (K.coco, '¡Coco!', '¡Le encantan\nlas bananas!', ['#A0582C', '#FFB300'], 1.25, 1560, dict(look=(0, 0)))]
STORY = ROUND * len(CAST) + 1.0
DUR = STORY + END

def bg(c, t, k):
    cols = [('#7E57C2', '#29B6F6'), ('#26A69A', '#9CCC65'), ('#EF5350', '#FFCA28'), ('#29B6F6', '#66BB6A'), ('#FF7043', '#FFD54F')][k]
    g = cairo.LinearGradient(0, 0, 0, SH)
    g.add_color_stop_rgb(0, *hexc(cols[0])[:3]); g.add_color_stop_rgb(1, *hexc(cols[1])[:3])
    c.set_source(g); c.paint()
    c.save(); c.translate(SW / 2, 1080)   # rayos que giran
    for i in range(16):
        a = i * math.pi / 8 + t * 0.15
        c.move_to(0, 0); c.arc(0, 0, 1500, a, a + math.pi / 16); c.close_path()
        c.set_source_rgba(1, 1, 1, 0.08); c.fill()
    c.restore()
    g = cairo.RadialGradient(SW / 2, 1150, 50, SW / 2, 1150, 620)   # foco
    g.add_color_stop_rgba(0, 1, 1, 1, 0.55); g.add_color_stop_rgba(1, 1, 1, 1, 0)
    c.set_source(g); c.arc(SW / 2, 1150, 620, 0, 2 * math.pi); c.fill()
    c.save(); c.translate(SW / 2, 1600); c.scale(1, 0.22); ellipse(c, 0, 0, 380, 120); c.set_source_rgba(0, 0, 0, 0.18); c.fill(); c.restore()

def character(c, k, t, reveal):
    body, name, hint, cols, sc, base, kw = CAST[k]
    bob = 14 * math.sin(t * 3)
    pop = 1 + 0.12 * math.sin(math.pi * min(1, max(0, (reveal - 0.0))) ) if 0 < reveal < 1 else 1
    c.push_group()
    K.put(c, body, SW / 2, base + bob, sc * pop, t=t, **kw)
    pat = c.pop_group()
    if reveal < 1:
        c.set_source_rgba(*hexc('#1A1033', 1 - reveal)); c.mask(pat)
    if reveal > 0:
        c.set_source(pat); c.paint_with_alpha(reveal)

def hint_text(c, txt, a, y=640):
    if a <= 0: return
    c.push_group()
    lines = txt.split('\n')
    for i, ln in enumerate(lines):
        word(c, ln, SW / 2, y + 80 * i - 40 * (len(lines) - 1), 72, colors=['#FFFFFF'], outline=7)
    c.pop_group_to_source(); c.paint_with_alpha(a)

def frame(c, t):
    if t >= STORY:
        end_card(c, t - STORY); return
    k = min(len(CAST) - 1, int(t // ROUND)); u = t - k * ROUND
    bg(c, t, k)
    reveal = ss(4.0, 4.5, u)
    character(c, k, t, reveal)
    body, name, hint, cols, *_ = CAST[k]
    if u < 4.0:
        # signo de pregunta que late
        s = 1 + 0.08 * math.sin(t * 6)
        word(c, '?', SW / 2 + 330, 960, 220 * s, colors=['#FFEB3B'], tilt=0.15, outline=12)
        word(c, '?', SW / 2 - 340, 1020, 150 * s, colors=['#FFEB3B'], tilt=-0.15, outline=10)
        hint_text(c, hint, ss(0.8, 1.2, u) if k > 0 else 1.0)
        for i, n in enumerate(('3', '2', '1')):
            t0 = 1.6 + 0.8 * i
            if t0 <= u < t0 + 0.8:
                q = (u - t0) / 0.8
                ellipse(c, SW - 150, 480, 95, 95); fill(c, (1, 1, 1, 1), OUT, 8)
                word(c, n, SW - 150, 520, 140 * K_back(q / 0.3) + 0.01, colors=['#E53935', '#FB8C00', '#43A047'][i:i + 1], outline=8)
    else:
        q = u - 4.0
        word(c, name, SW / 2, 650, 150 * K_back(q / 0.4) + 0.01, colors=cols, tilt=0.04, outline=11)
        if q < 1.2:
            for j in range(12):
                a = j * math.pi / 6; r = 120 + 520 * q
                sparkle(c, SW / 2 + r * math.cos(a), 1150 + r * math.sin(a), 30 * (1 - q / 1.2) + 2, ('#FFFFFF', '#FFEB3B', '#FF80AB')[j % 3])
    if t > STORY - 1.0 + 0.0 and k == len(CAST) - 1 and u > ROUND - 0.1:
        pass
    # títulos
    if t < ROUND:
        top_title(c, t, 0, '¿Adivinás', 'quién es?', first=True)
    elif t < ROUND * (len(CAST) - 1):
        n = k + 1
        top_title(c, t, k * ROUND, f'¿Y este amigo?', f'Ronda {n}')
    else:
        top_title(c, t, k * ROUND, '¡El último!', '¿Quién es?')
    if t > STORY - 1.6:
        word(c, '¿Cuántos adivinaste?', SW / 2, 470, 72 * K_back((t - STORY + 1.6) / 0.4) + 0.01, colors=['#FFFFFF'], outline=7)
    logo_band(c)

if __name__ == '__main__':
    args = sys.argv[1:] or ['short']
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, SW, SH); c = cairo.Context(surf)
    if args[0] == 'stills':
        for t in map(float, args[1:]):
            c.save(); frame(c, t); c.restore(); surf.write_to_png(f'adivina_{t}.png')
    elif args[0] == 'portada':
        frame(c, 2.0); surf.write_to_png('short_adivina_portada.png')
    else:
        a0, a1 = (float(args[1]), float(args[2])) if len(args) > 2 else (0, DUR)
        out = sys.stdout.buffer
        for i in range(int(round(a0 * FPS)), int(round(a1 * FPS))):
            c.save(); frame(c, i / FPS); c.restore(); surf.flush(); out.write(surf.get_data())
