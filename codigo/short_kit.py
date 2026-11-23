"""Plantilla de shorts del canal (desde nov 2026, según las métricas):
- SIN fundido de entrada: el conflicto y el título se ven completos desde el cuadro 1.
- 35–45 s en total.
- Tarjeta final de 3 s: Coco saluda + botón ¡Suscribite! que se toca + campanita que suena.
Uso desde otro script:
    from short_kit import SW, SH, top_title, end_card, logo_band, END
"""
import cairo, math, os
import cuerpos as K
from amigos import hexc, ellipse, fill, OUT
from logos import word, sparkle
from ep02_puente_del_rio import ss, K_back

SW, SH, FPS = 1080, 1920, 30
END = 3.0      # duración de la tarjeta final
LOGO = cairo.ImageSurface.create_from_png(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'imagenes', 'logo_perfil.png'))

def top_title(c, t, t0, a, b=None, first=False, size=100):
    """Título de la banda de arriba. Si first=True aparece entero desde el cuadro 1 (gancho)."""
    sc = 1.0 + 0.04 * math.sin(t * 5) if first else K_back((t - t0) / 0.4)
    if b is None:
        word(c, a, SW / 2, 230, size * 1.15 * sc + 0.01, tilt=0.05, outline=10)
    else:
        word(c, a, SW / 2, 170, size * sc + 0.01, tilt=0.05, outline=9)
        word(c, b, SW / 2, 295, size * 1.05 * sc + 0.01, start=3, tilt=0.05, outline=9)

def logo_band(c, cy=1770):
    d = 170
    c.save(); c.arc(170, cy, d / 2, 0, 2 * math.pi); c.clip()
    c.translate(170 - d / 2, cy - d / 2); c.scale(d / LOGO.get_width(), d / LOGO.get_height())
    c.set_source_surface(LOGO, 0, 0); c.paint(); c.restore()
    c.arc(170, cy, d / 2, 0, 2 * math.pi); c.set_source_rgba(1, 1, 1, 1); c.set_line_width(8); c.stroke()
    word(c, 'Cuentos mágicos', 620, cy - 15, 62, outline=6); word(c, 'de la selva', 620, cy + 60, 62, start=5, outline=6)

def bell(c, x, y, s, ring):
    c.save(); c.translate(x, y); c.rotate(0.35 * math.sin(ring * 18) * max(0, 1 - ring * 0.6)); c.scale(s, s)
    c.move_to(-70, 60); c.curve_to(-70, -10, -55, -80, 0, -85); c.curve_to(55, -80, 70, -10, 70, 60); c.line_to(90, 80); c.line_to(-90, 80); c.close_path()
    fill(c, hexc('#FFD600'), OUT, 7)
    ellipse(c, 0, 92, 20, 16); fill(c, hexc('#FFB300'), OUT, 5)
    ellipse(c, 0, -92, 12, 12); fill(c, hexc('#FFD600'), OUT, 5)
    c.restore()
    if ring > 0:
        for side in (-1, 1):
            for k in range(2):
                r = 120 + 30 * k + 20 * math.sin(ring * 10)
                c.arc(x, y, r * s, -math.pi / 2 + side * 0.5 - 0.25, -math.pi / 2 + side * 0.5 + 0.25)
                c.set_source_rgba(*OUT); c.set_line_width(7); c.stroke()

def end_card(c, u):
    """Tarjeta final. u = segundos desde que empieza (0..END)."""
    g = cairo.LinearGradient(0, 0, 0, SH)
    g.add_color_stop_rgb(0, *hexc('#29B6F6')[:3]); g.add_color_stop_rgb(1, *hexc('#8BC34A')[:3])
    c.set_source(g); c.paint()
    for k in range(10):
        ph = (u * 0.7 + k / 10) % 1
        sparkle(c, 80 + k * 100, 350 + 900 * ((k * 3) % 7) / 7, 26 * math.sin(math.pi * ph), '#FFFFFF')
    K.put(c, K.coco, 330, 1250, 1.0, t=u, arm_r=math.radians(-58 + 25 * math.sin(u * 9)), arm_l=math.radians(115),
          look=(0.6, 0))
    word(c, '¡Seguinos para', SW / 2, 230, 92, tilt=0.05, outline=9)
    word(c, 'más cuentos!', SW / 2, 345, 100, start=3, tilt=0.05, outline=9)
    # botón suscribirse
    press = 0.92 if 0.9 < u < 1.2 else 1.0
    sub = u > 1.15
    c.save(); c.translate(720, 1000); c.scale(press * K_back(u / 0.4), press * K_back(u / 0.4))
    r = 60; w = 520
    c.new_path(); c.arc(-w / 2 + r, 0, r, math.pi / 2, 3 * math.pi / 2); c.arc(w / 2 - r, 0, r, -math.pi / 2, math.pi / 2); c.close_path()
    fill(c, hexc('#9E9E9E') if sub else hexc('#E53935'), OUT, 7)
    word(c, '¡Suscripto!' if sub else '¡Suscribite!', 0, 26, 68, colors=['#FFFFFF'], outline=4)
    c.restore()
    # manito que toca el botón
    if 0.5 < u < 1.6:
        q = ss(0.5, 0.95, u) * (1 - ss(1.3, 1.6, u))
        hx, hy = 860 + 160 * (1 - q), 1060 + 160 * (1 - q)
        ellipse(c, hx, hy, 40, 34); fill(c, hexc('#FFD9A8'), OUT, 5)
        c.set_line_cap(cairo.LINE_CAP_ROUND)
        c.move_to(hx - 18, hy - 20); c.line_to(hx - 38, hy - 70); c.set_source_rgba(*OUT); c.set_line_width(26); c.stroke()
        c.move_to(hx - 18, hy - 20); c.line_to(hx - 38, hy - 70); c.set_source_rgba(*hexc('#FFD9A8')); c.set_line_width(16); c.stroke()
    # campanita
    if u > 1.3:
        bell(c, 720, 1320, 1.0 * K_back((u - 1.3) / 0.35), max(0, u - 1.5))
        word(c, '¡Activá la campanita!', SW / 2, 1560, 66 * K_back((u - 1.5) / 0.35) + 0.01, outline=6)
    logo_band(c)
