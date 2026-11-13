import sys, math, cairo
import escena_noche as N
from escena_noche import ellipse, fill, hexc, ss, OUT, BROWN, BEIGE, arm, W, H

DUR = 40.0
N.SHOOT = ((3.5, 250, 60), (9.0, 150, 200), (31.0, 450, 30))
LID = hexc('#E9B57E')

def eyes(c, look, lid):
    for ex in (-48, 48):
        if lid > 0.9:
            c.set_source_rgba(*OUT); c.set_line_width(7); c.set_line_cap(cairo.LINE_CAP_ROUND)
            c.arc(ex, -18, 24, 0.15 * math.pi, 0.85 * math.pi); c.stroke()
            # lashes
            for a in (0.3, 0.5, 0.7):
                x0, y0 = ex + 24 * math.cos(a * math.pi), -18 + 24 * math.sin(a * math.pi)
                c.move_to(x0, y0); c.line_to(ex + 33 * math.cos(a * math.pi), -18 + 33 * math.sin(a * math.pi)); c.stroke()
            continue
        ellipse(c, ex, -15, 34, 42); fill(c, (1, 1, 1, 1))
        ellipse(c, ex + look[0] * 10, -12 + look[1] * 10, 19, 21); fill(c, hexc('#1A1A1A'))
        ellipse(c, ex + look[0] * 10 + 7, -20 + look[1] * 10, 7, 7); c.set_source_rgba(1, 1, 1, 1); c.fill()
        if lid > 0.01:
            c.save(); ellipse(c, ex, -15, 34, 42); c.clip()
            yb = -57 + 84 * lid
            c.rectangle(ex - 40, -60, 80, yb + 60); c.set_source_rgba(*LID); c.fill()
            c.restore()
            c.save(); ellipse(c, ex, -15, 34, 42); c.clip()
            c.move_to(ex - 40, yb); c.line_to(ex + 40, yb)
            c.set_source_rgba(*OUT); c.set_line_width(6); c.stroke(); c.restore()
        ellipse(c, ex, -15, 34, 42); c.set_source_rgba(*OUT); c.set_line_width(5); c.stroke()

def mouth(c, awake, yawn):
    if yawn > 0.02:
        ry = 12 + 42 * yawn; rx = 18 + 16 * yawn
        ellipse(c, 0, 72, rx, ry); fill(c, hexc('#B71C1C'), OUT, 6)
        c.save(); ellipse(c, 0, 72, rx, ry); c.clip()
        ellipse(c, 0, 72 + ry * 0.8, rx * 0.8, ry * 0.5); c.set_source_rgba(*hexc('#FF8A80')); c.fill(); c.restore()
    elif awake > 0.5:
        c.move_to(-48, 55); c.curve_to(-40, 120, 40, 120, 48, 55); c.close_path()
        fill(c, hexc('#B71C1C'), OUT, 6)
        c.save(); c.move_to(-48, 55); c.curve_to(-40, 120, 40, 120, 48, 55); c.close_path(); c.clip()
        ellipse(c, 0, 105, 30, 20); c.set_source_rgba(*hexc('#FF8A80')); c.fill(); c.restore()
    else:
        c.set_source_rgba(*OUT); c.set_line_width(7); c.set_line_cap(cairo.LINE_CAP_ROUND)
        c.arc(0, 50, 30, 0.25 * math.pi, 0.75 * math.pi); c.stroke()

def monkey(c, x, y, t, sq, head_tilt, arm_r, arm_l, lid, look, awake, yawn, lie):
    c.save(); c.translate(x, y); c.rotate(-lie * math.radians(84)); c.scale(1 / sq, sq)
    tw = math.sin(t * 1.4) * (1 - 0.8 * lie)
    c.set_line_cap(cairo.LINE_CAP_ROUND)
    path = lambda: (c.move_to(60, -70), c.curve_to(200, -60, 230 + 20 * tw, -220, 160 + 15 * tw, -260),
                    c.curve_to(110 + 10 * tw, -290, 90, -230, 130 + 10 * tw, -215))
    path(); c.set_source_rgba(*OUT); c.set_line_width(36); c.stroke()
    path(); c.set_source_rgba(*BROWN); c.set_line_width(24); c.stroke()
    for lx in (-50, 50):
        ellipse(c, lx, -18, 44, 26); fill(c, BEIGE, OUT, 6)
    ellipse(c, 0, -120, 98, 112); fill(c, BROWN, OUT, 6)
    ellipse(c, 0, -110, 64, 78); fill(c, BEIGE)
    c.save(); c.translate(0, -245); c.rotate(head_tilt); c.translate(0, -90)
    for ex in (-1, 1):
        ellipse(c, ex * 138, -5, 52, 52); fill(c, BROWN, OUT, 6)
        ellipse(c, ex * 138, -5, 30, 30); fill(c, BEIGE)
    for i, dx in enumerate((-22, 0, 22)):
        ellipse(c, dx, -140 - (10 if i == 1 else 0), 18, 26); fill(c, BROWN, OUT, 5)
    ellipse(c, 0, 0, 138, 132); fill(c, BROWN, OUT, 6)
    for ex in (-50, 50):
        ellipse(c, ex, -10, 62, 64)
    ellipse(c, 0, 55, 98, 66)
    c.set_source_rgba(*BEIGE); c.fill()
    eyes(c, look, lid)
    for nx in (-13, 13):
        ellipse(c, nx, 32, 6, 8); fill(c, OUT)
    mouth(c, awake, yawn)
    for cx in (-98, 98):
        ellipse(c, cx, 45, 24, 17); c.set_source_rgba(*hexc('#FF5C8A', 0.6)); c.fill()
    c.restore()
    arm(c, -78, -180, arm_l)
    arm(c, 78, -180, arm_r)
    c.restore()

def zzz(c, x, y, t):
    c.select_font_face('DejaVu Sans', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    for k in range(3):
        p = ((t - 28.5) / 3.0 - k / 3.0)
        if p < 0: continue
        p = p % 1.0
        a = math.sin(math.pi * p)
        size = 50 + 50 * p
        zx = x + 140 * p + 25 * math.sin(p * 6); zy = y - 230 * p
        c.set_font_size(size)
        c.move_to(zx, zy); c.text_path('Z')
        c.set_source_rgba(1, 1, 1, a); c.fill_preserve()
        c.set_source_rgba(0.24, 0.2, 0.55, a); c.set_line_width(4); c.stroke()

def lerp(a, b, k): return a + (b - a) * k

def frame(c, t):
    N.sky(c); N.stars(c, t); N.shooting(c, t)
    for i, (x0, y0, s, sp) in enumerate(((200, 170, 1.0, 12), (900, 110, 0.8, 8), (1250, 300, 0.7, 15))):
        N.cloud(c, (x0 + sp * t) % 2300 - 250, y0 + 8 * math.sin(t * 0.6 + i), s)
    N.sun(c, t)
    N.hills(c)
    N.palm(c, 180, 900, 560, t * 0.7, 0, 1)
    N.palm(c, 1760, 900, 520, t * 0.7, 1.7, -1)
    N.bush(c, 420, 840, 0.7, '#2E7D32'); N.bush(c, 1510, 850, 0.65, '#388E3C')
    for i, (fx, col) in enumerate(((330, '#FF4081'), (560, '#FF9100'), (1380, '#E040FB'), (1600, '#FF4081'), (760, '#FFEA00'))):
        N.flower(c, fx, 900, col, t * 0.6, i * 1.3)

    pt = (t - 11.5) / 6.0
    look = (0.0, 0.0)
    if 0 <= pt <= 1:
        px, py = 2150 - 2400 * pt, 330 + 50 * math.sin(pt * 4 * math.pi)
        look = (max(-1, min(1, (px - 960) / 600)), -0.6)
    for (t0, _, _) in N.SHOOT:
        if 0 <= t - t0 <= 1.3 and t < 24: look = (-0.5 + (t - t0) / 1.3, -0.9)

    # entrance: 3 soft hops
    if t < 0.5:
        mx, hop = -300, 0
    elif t < 6.0:
        p = (t - 0.5) / 5.5
        mx = -300 + 1260 * (1 - (1 - p) ** 2)
        hop = 130 * abs(math.sin(3 * math.pi * p)) * (1 - 0.3 * p)
    else:
        mx, hop = 960, 0
    land = max(0.0, 1 - abs(t - 6.0) / 0.3) if t > 5.7 else 0
    sleepy = ss(16, 24, t)
    lie = ss(24.5, 28, t)
    idle = ss(6.2, 7.0, t) * (1 - sleepy)
    bob = idle * 12 * abs(math.sin(math.pi * t / 2.0))
    breathe = 0.025 * math.sin(2 * math.pi * t / 3.5) * ss(26, 29, t)
    sq = 1 - 0.07 * land + 0.025 * idle * math.sin(math.pi * t) + breathe
    tilt = math.radians(6) * math.sin(2 * math.pi * t / 4.0) * (1 - lie) + math.radians(14) * sleepy * (1 - lie) + math.radians(50) * lie

    wave = ss(6.5, 7.2, t) * (1 - ss(10.4, 11.0, t))
    rest_r = math.radians(65 + 6 * math.sin(t * 1.8))
    rest_l = math.radians(115 - 6 * math.sin(t * 1.8))
    if t < 6:
        rest_r = math.radians(20 + 30 * math.sin(t * 3.4)); rest_l = math.radians(160 - 30 * math.sin(t * 3.4))
    arm_r = lerp(rest_r, math.radians(-58 + 25 * math.sin(t * 2 * math.pi * 1.4)), wave)
    arm_l = rest_l
    # yawns with a stretch
    y1 = math.sin(math.pi * ss(18, 20.5, t)) if 18 < t < 20.5 else 0
    y2 = 0.75 * math.sin(math.pi * ss(22.3, 24.3, t)) if 22.3 < t < 24.3 else 0
    yawn = max(y1, y2)
    stretch = y1
    arm_r = lerp(arm_r, math.radians(-65), stretch)
    arm_l = lerp(arm_l, math.radians(-115), stretch)
    # sleeping pose: hands folded on tummy
    arm_r = lerp(arm_r, math.radians(150), lie)
    arm_l = lerp(arm_l, math.radians(40), lie)

    lid = 0.0
    lid = max(lid, 0.4 * ss(16, 18, t), 0.55 * ss(20.5, 21.5, t), 0.7 * ss(23.5, 24.5, t), ss(25.5, 27, t))
    if yawn > 0.3: lid = max(lid, 0.85)
    for bt in (3.0, 8.4, 13.0, 15.2):
        d = abs(t - bt)
        if d < 0.13: lid = max(lid, 1 - d / 0.13)
    for bt in (21.8,):  # slow sleepy blink
        d = abs(t - bt)
        if d < 0.5: lid = max(lid, 1 - d / 0.5)
    awake = 1 if t < 18 else 0

    # lying down: shift so he ends centred and resting on the ground
    lx = mx + 230 * lie
    ly = 900 - hop - bob - 92 * lie
    sh = 1 - hop / 400
    ellipse(c, lx - 200 * lie, 905, (120 + 200 * lie) * sh, 18 * sh); c.set_source_rgba(0, 0.15, 0.05, 0.3); c.fill()
    # leaf blanket under him
    if lie > 0:
        c.save(); c.translate(lx - 220, 905); c.scale(1, 1)
        ellipse(c, 0, 0, 380 * lie, 34 * lie); c.set_source_rgba(*hexc('#2E7D32', min(1, lie * 1.5))); c.fill()
        c.restore()
    monkey(c, lx, ly, t, sq, tilt, arm_r, arm_l, lid, look, awake, yawn, lie)
    if 0 <= pt <= 1:
        N.parrot(c, px, py, t * 0.8)
    if t > 28.5:
        zzz(c, lx - 520, ly - 230, t)
    N.fireflies(c, t * 0.6)
    a = max(1 - ss(0, 0.8, t), ss(DUR - 3.0, DUR, t))
    if a > 0:
        c.set_source_rgba(0.05, 0.04, 0.2, a); c.paint()

if __name__ == '__main__':
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    c = cairo.Context(surf)
    if len(sys.argv) > 1 and sys.argv[1] == 'stills':
        for t in map(float, sys.argv[2:]):
            c.save(); frame(c, t); c.restore(); surf.write_to_png(f'sleep_{t}.png')
    else:
        out = sys.stdout.buffer
        for i in range(int(DUR * 30)):
            c.save(); frame(c, i / 30); c.restore(); surf.flush()
            out.write(surf.get_data())
