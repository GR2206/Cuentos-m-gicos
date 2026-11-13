import cairo, math, sys

W, H, FPS, DUR = 1920, 1080, 30, 20.0

def hexc(h, a=1.0):
    h = h.lstrip('#')
    return (int(h[0:2], 16)/255, int(h[2:4], 16)/255, int(h[4:6], 16)/255, a)

OUT = hexc('#3B2314')

def ss(e0, e1, x):
    t = max(0.0, min(1.0, (x - e0) / (e1 - e0)))
    return t * t * (3 - 2 * t)

def ellipse(c, x, y, rx, ry):
    c.save(); c.translate(x, y); c.scale(rx, ry)
    c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()

def fill(c, col, outline=None, lw=6):
    c.set_source_rgba(*col)
    if outline:
        c.fill_preserve(); c.set_source_rgba(*outline); c.set_line_width(lw); c.stroke()
    else:
        c.fill()

# ---------------- background ----------------
def sky(c):
    g = cairo.LinearGradient(0, 0, 0, H)
    g.add_color_stop_rgb(0, *hexc('#120F4A')[:3])
    g.add_color_stop_rgb(0.55, *hexc('#2D2A8C')[:3])
    g.add_color_stop_rgb(1, *hexc('#6A4FC4')[:3])
    c.set_source(g); c.paint()

import random
random.seed(7)
STARS = [(random.uniform(20, 1900), random.uniform(20, 560), random.uniform(5, 13), random.uniform(0, 6.28), random.uniform(1.5, 3.5)) for _ in range(60)]

def star_shape(c, x, y, r, rot=0):
    c.save(); c.translate(x, y); c.rotate(rot)
    for i in range(10):
        rr = r if i % 2 == 0 else r * 0.45
        a = -math.pi / 2 + i * math.pi / 5
        (c.move_to if i == 0 else c.line_to)(rr * math.cos(a), rr * math.sin(a))
    c.close_path(); c.restore()

def stars(c, t):
    for (x, y, r, ph, sp) in STARS:
        if 1150 < x < 1650 and y < 470: continue  # keep clear of the moon
        k = 0.6 + 0.4 * math.sin(t * sp + ph)
        if r > 10:
            g2 = cairo.RadialGradient(x, y, 0, x, y, r * 2.6); g2.add_color_stop_rgba(0, 1, 0.95, 0.6, 0.35 * k); g2.add_color_stop_rgba(1, 1, 0.95, 0.6, 0); c.set_source(g2); c.arc(x, y, r * 2.6, 0, 2 * math.pi); c.fill()
            star_shape(c, x, y, r * (0.85 + 0.25 * k), 0.1 * math.sin(t + ph)); c.set_source_rgba(1, 0.93, 0.45, 0.6 + 0.4 * k); c.fill()
        else:
            rr = r * 0.35 * (0.7 + 0.5 * k)
            ellipse(c, x, y, rr, rr); c.set_source_rgba(1, 1, 0.9, 0.5 + 0.5 * k); c.fill()

SHOOT = ((2.6, 250, 60), (9.2, 150, 200), (15.4, 450, 30))
def shooting(c, t):
    for (t0, x0, y0) in SHOOT:
        p = (t - t0) / 1.1
        if not 0 <= p <= 1: continue
        e = 1 - (1 - p) ** 2
        hx, hy = x0 + 800 * e, y0 + 340 * e
        a = math.sin(math.pi * p) ** 0.5
        tl = 340
        g = cairo.LinearGradient(hx, hy, hx - tl * 0.92, hy - tl * 0.39)
        g.add_color_stop_rgba(0, 1, 1, 0.85, a); g.add_color_stop_rgba(1, 1, 1, 0.85, 0)
        c.set_line_cap(cairo.LINE_CAP_ROUND); c.set_line_width(10)
        c.move_to(hx, hy); c.line_to(hx - tl * 0.92, hy - tl * 0.39); c.set_source(g); c.stroke()
        g2 = cairo.RadialGradient(hx, hy, 0, hx, hy, 60); g2.add_color_stop_rgba(0, 1, 0.95, 0.6, 0.6 * a); g2.add_color_stop_rgba(1, 1, 0.95, 0.6, 0); c.set_source(g2); c.arc(hx, hy, 60, 0, 2 * math.pi); c.fill()
        star_shape(c, hx, hy, 24, t * 6); c.set_source_rgba(1, 0.95, 0.5, a); c.fill()

def fireflies(c, t):
    for i in range(9):
        x = 200 + i * 190 + 70 * math.sin(t * 0.7 + i * 1.7); y = 640 + 110 * math.sin(t * 0.9 + i * 2.3)
        k = 0.5 + 0.5 * math.sin(t * 3 + i * 1.1)
        g2 = cairo.RadialGradient(x, y, 0, x, y, 34); g2.add_color_stop_rgba(0, 1, 1, 0.4, 0.5 * k); g2.add_color_stop_rgba(1, 1, 1, 0.4, 0); c.set_source(g2); c.arc(x, y, 34, 0, 2 * math.pi); c.fill()
        ellipse(c, x, y, 8, 8); c.set_source_rgba(1, 1, 0.6, 0.5 + 0.5 * k); c.fill()

def sun(c, t):  # the moon
    x, y = 1400, 230
    s = 1 + 0.02 * math.sin(t * 1.5)
    rg = cairo.RadialGradient(x, y, 160, x, y, 360)
    rg.add_color_stop_rgba(0, 1, 0.97, 0.75, 0.35); rg.add_color_stop_rgba(1, 1, 0.97, 0.75, 0)
    c.set_source(rg); c.arc(x, y, 360, 0, 2 * math.pi); c.fill()
    c.save(); c.translate(x, y); c.scale(s, s)
    ellipse(c, 0, 0, 175, 175); fill(c, hexc('#FFF59D'), hexc('#FBC02D'), 8)
    for (cx, cy, r) in ((-75, -90, 24), (95, -60, 17), (70, 100, 26), (-110, 70, 15)):
        ellipse(c, cx, cy, r, r); c.set_source_rgba(*hexc('#FFE082')); c.fill()
    c.set_source_rgba(*OUT); c.set_line_width(8); c.set_line_cap(cairo.LINE_CAP_ROUND)
    for ex in (-52, 52):
        c.arc(ex, -10, 22, math.pi * 0.15, math.pi * 0.85); c.stroke()
    c.arc(0, 30, 40, 0.2 * math.pi, 0.8 * math.pi); c.stroke()
    for ex in (-95, 95):
        ellipse(c, ex, 35, 22, 15); c.set_source_rgba(*hexc('#FF8A80', 0.6)); c.fill()
    c.restore()

def _old_sun(c, t):
    x, y = 1380, 175
    c.save(); c.translate(x, y); c.rotate(t * 0.25)
    for i in range(12):
        c.save(); c.rotate(i * math.pi / 6)
        c.move_to(-22, -150); c.line_to(0, -205 - 12 * math.sin(t * 3 + i)); c.line_to(22, -150); c.close_path()
        c.set_source_rgba(*hexc('#FFB300')); c.fill(); c.restore()
    c.restore()
    s = 1 + 0.03 * math.sin(t * 2)
    c.save(); c.translate(x, y); c.scale(s, s)
    ellipse(c, 0, 0, 125, 125); fill(c, hexc('#FFEB3B'), hexc('#F9A825'), 8)
    # happy closed eyes
    c.set_source_rgba(*OUT); c.set_line_width(8); c.set_line_cap(cairo.LINE_CAP_ROUND)
    for ex in (-42, 42):
        c.arc(ex, -15, 20, math.pi * 1.1, math.pi * 1.9); c.stroke()
    c.arc(0, 15, 45, 0.15 * math.pi, 0.85 * math.pi); c.stroke()
    for ex in (-75, 75):
        ellipse(c, ex, 30, 20, 14); c.set_source_rgba(*hexc('#FF7043', 0.55)); c.fill()
    c.restore()

def cloud(c, x, y, s):
    c.save(); c.translate(x, y); c.scale(s, s)
    for (cx, cy, r) in ((0, 0, 60), (70, -30, 75), (150, 0, 60), (75, 20, 60)):
        ellipse(c, cx, cy, r, r)
    c.set_source_rgba(*hexc('#8C8FD6', 0.8)); c.fill(); c.restore()

def hills(c):
    c.move_to(0, 640)
    c.curve_to(300, 480, 600, 500, 900, 620)
    c.curve_to(1150, 520, 1500, 470, 1920, 600)
    c.line_to(1920, H); c.line_to(0, H); c.close_path()
    c.set_source_rgba(*hexc('#2E8B57')); c.fill()
    c.move_to(0, 760)
    c.curve_to(400, 660, 800, 700, 1100, 740)
    c.curve_to(1400, 690, 1700, 680, 1920, 730)
    c.line_to(1920, H); c.line_to(0, H); c.close_path()
    c.set_source_rgba(*hexc('#1F7A4A')); c.fill()
    # bright ground the monkey stands on
    c.move_to(0, 860)
    c.curve_to(500, 820, 1400, 820, 1920, 860)
    c.line_to(1920, H); c.line_to(0, H); c.close_path()
    c.set_source_rgba(*hexc('#4CAF50')); c.fill()

def palm(c, x, y, h, t, ph, flip=1):
    sway = math.sin(t * 2 * math.pi / 3.2 + ph)
    tipx, tipy = x + flip * (60 + 10 * sway), y - h
    c.set_line_cap(cairo.LINE_CAP_ROUND)
    c.move_to(x, y); c.curve_to(x + flip * 10, y - h * 0.4, x + flip * 50, y - h * 0.8, tipx, tipy)
    c.set_line_width(46); c.set_source_rgba(*hexc('#8D5524')); c.stroke()
    for k in range(1, 9):  # trunk rings
        u = k / 9
        px = (1-u)**3*x + 3*(1-u)**2*u*(x+flip*10) + 3*(1-u)*u*u*(x+flip*50) + u**3*tipx
        py = (1-u)**3*y + 3*(1-u)**2*u*(y-h*0.4) + 3*(1-u)*u*u*(y-h*0.8) + u**3*tipy
        c.move_to(px - 20, py); c.line_to(px + 20, py - 6)
        c.set_line_width(6); c.set_source_rgba(*hexc('#6D3F17')); c.stroke()
    for i, ang in enumerate((-160, -125, -90, -55, -20, -195, 15)):
        a = math.radians(ang + 5 * sway + 3 * math.sin(t * 2.4 + i))
        c.save(); c.translate(tipx, tipy); c.rotate(a)
        c.move_to(0, 0); c.curve_to(80, -45, 170, -30, 240, 30)
        c.curve_to(160, 10, 80, 20, 0, 0); c.close_path()
        c.set_source_rgba(*hexc('#2E7D32' if i % 2 else '#43A047')); c.fill()
        c.restore()
    for dx in (-18, 18, 0):  # coconuts
        ellipse(c, tipx + dx, tipy + 22 + (8 if dx == 0 else 0), 20, 20); fill(c, hexc('#6D4C41'))

def flower(c, x, y, col, t, ph):
    bob = 6 * math.sin(t * 2.5 + ph)
    c.set_line_width(8); c.set_source_rgba(*hexc('#2E7D32'))
    c.move_to(x, y + 70); c.line_to(x, y + bob); c.stroke()
    c.save(); c.translate(x, y + bob); c.rotate(0.2 * math.sin(t * 1.5 + ph))
    for i in range(6):
        a = i * math.pi / 3
        ellipse(c, 26 * math.cos(a), 26 * math.sin(a), 20, 20)
        c.set_source_rgba(*hexc(col)); c.fill()
    ellipse(c, 0, 0, 17, 17); c.set_source_rgba(*hexc('#FFEB3B')); c.fill()
    c.restore()

def bush(c, x, y, s, col):
    c.save(); c.translate(x, y); c.scale(s, s)
    for (cx, cy, r) in ((-110, 0, 90), (0, -50, 120), (110, 0, 95), (0, 30, 100)):
        ellipse(c, cx, cy, r, r)
    c.set_source_rgba(*hexc(col)); c.fill(); c.restore()

def butterfly(c, x, y, t, col):
    flap = 0.25 + 0.75 * abs(math.sin(t * 9))
    c.save(); c.translate(x, y); c.rotate(0.2 * math.sin(t * 2))
    for side in (-1, 1):
        c.save(); c.scale(side * flap, 1)
        ellipse(c, 26, -14, 28, 24); fill(c, hexc(col), OUT, 3)
        ellipse(c, 20, 18, 18, 16); fill(c, hexc(col), OUT, 3)
        ellipse(c, 28, -16, 9, 9); c.set_source_rgba(1, 1, 1, 0.8); c.fill()
        c.restore()
    ellipse(c, 0, 0, 7, 26); fill(c, OUT)
    c.restore()

# ---------------- characters ----------------
BROWN, BEIGE = hexc('#A0582C'), hexc('#FFD9A8')

def arm(c, sx, sy, ang):
    hx, hy = sx + 115 * math.cos(ang), sy + 115 * math.sin(ang)
    c.set_line_cap(cairo.LINE_CAP_ROUND)
    c.move_to(sx, sy); c.line_to(hx, hy); c.set_source_rgba(*OUT); c.set_line_width(46); c.stroke()
    c.move_to(sx, sy); c.line_to(hx, hy); c.set_source_rgba(*BROWN); c.set_line_width(34); c.stroke()
    ellipse(c, hx, hy, 26, 26); fill(c, BEIGE, OUT, 6)

def monkey(c, x, y, t, sq, head_tilt, arm_r, arm_l, blink, look):
    c.save(); c.translate(x, y); c.scale(1 / sq, sq)
    # tail
    tw = math.sin(t * 2.2)
    c.set_line_cap(cairo.LINE_CAP_ROUND)
    path = lambda: (c.move_to(60, -70), c.curve_to(200, -60, 230 + 20 * tw, -220, 160 + 15 * tw, -260),
                    c.curve_to(110 + 10 * tw, -290, 90, -230, 130 + 10 * tw, -215))
    path(); c.set_source_rgba(*OUT); c.set_line_width(36); c.stroke()
    path(); c.set_source_rgba(*BROWN); c.set_line_width(24); c.stroke()
    # legs / feet
    for lx in (-50, 50):
        ellipse(c, lx, -18, 44, 26); fill(c, BEIGE, OUT, 6)
    ellipse(c, 0, -120, 98, 112); fill(c, BROWN, OUT, 6)
    ellipse(c, 0, -110, 64, 78); fill(c, BEIGE)
    # head
    c.save(); c.translate(0, -245); c.rotate(head_tilt); c.translate(0, -90)
    for ex in (-1, 1):
        ellipse(c, ex * 138, -5, 52, 52); fill(c, BROWN, OUT, 6)
        ellipse(c, ex * 138, -5, 30, 30); fill(c, BEIGE)
    # tuft
    for i, dx in enumerate((-22, 0, 22)):
        ellipse(c, dx, -140 - (10 if i == 1 else 0), 18, 26); fill(c, BROWN, OUT, 5)
    ellipse(c, 0, 0, 138, 132); fill(c, BROWN, OUT, 6)
    for ex in (-50, 50):
        ellipse(c, ex, -10, 62, 64)
    ellipse(c, 0, 55, 98, 66)
    c.set_source_rgba(*BEIGE); c.fill()
    # eyes
    for ex in (-48, 48):
        if blink > 0.15:
            ellipse(c, ex, -15, 34, 42 * blink); fill(c, (1, 1, 1, 1), OUT, 5)
            ellipse(c, ex + look[0] * 10, -12 + look[1] * 10, 19, 21 * min(1, blink * 1.2)); fill(c, hexc('#1A1A1A'))
            ellipse(c, ex + look[0] * 10 + 7, -20 + look[1] * 10, 7, 7); c.set_source_rgba(1, 1, 1, 1); c.fill()
        else:
            c.set_source_rgba(*OUT); c.set_line_width(7)
            c.arc(ex, -18, 24, 0.15 * math.pi, 0.85 * math.pi); c.stroke()
    # nose
    for nx in (-13, 13):
        ellipse(c, nx, 32, 6, 8); fill(c, OUT)
    # open smile
    c.move_to(-48, 55); c.curve_to(-40, 120, 40, 120, 48, 55); c.close_path()
    fill(c, hexc('#B71C1C'), OUT, 6)
    c.save(); c.move_to(-48, 55); c.curve_to(-40, 120, 40, 120, 48, 55); c.close_path(); c.clip()
    ellipse(c, 0, 105, 30, 20); c.set_source_rgba(*hexc('#FF8A80')); c.fill(); c.restore()
    for cx in (-98, 98):
        ellipse(c, cx, 45, 24, 17); c.set_source_rgba(*hexc('#FF5C8A', 0.6)); c.fill()
    c.restore()
    arm(c, -78, -180, arm_l)
    arm(c, 78, -180, arm_r)
    c.restore()

def parrot(c, x, y, t):
    flap = math.sin(t * 14)
    c.save(); c.translate(x, y)
    for i, col in enumerate(('#1E88E5', '#FDD835', '#E53935')):  # tail
        c.save(); c.rotate(math.radians(-10 + i * 10))
        c.move_to(60, 0); c.line_to(190, -12); c.line_to(190, 14); c.close_path(); fill(c, hexc(col), OUT, 4)
        c.restore()
    ellipse(c, 0, 0, 85, 52); fill(c, hexc('#E53935'), OUT, 5)
    ellipse(c, -75, -30, 48, 46); fill(c, hexc('#E53935'), OUT, 5)
    ellipse(c, -82, -38, 20, 20); fill(c, (1, 1, 1, 1), OUT, 4)
    ellipse(c, -88, -38, 10, 10); fill(c, hexc('#1A1A1A'))
    c.move_to(-112, -38); c.curve_to(-160, -30, -150, 5, -118, 0); c.close_path(); fill(c, hexc('#FFC107'), OUT, 4)
    c.save(); c.translate(10, -20); c.scale(1, flap)
    c.move_to(-40, 0); c.curve_to(-20, -150, 60, -150, 70, 0); c.close_path(); fill(c, hexc('#1E88E5'), OUT, 5)
    c.move_to(-25, -40); c.curve_to(-10, -110, 45, -110, 55, -40); c.close_path(); c.set_source_rgba(*hexc('#FDD835')); c.fill()
    c.restore()
    c.restore()

# ---------------- timeline ----------------
def frame(c, t):
    sky(c)
    stars(c, t)
    shooting(c, t)
    for i, (x0, y0, s, sp) in enumerate(((200, 170, 1.0, 22), (900, 110, 0.8, 15), (1250, 300, 0.7, 28))):
        cloud(c, (x0 + sp * t) % 2300 - 250, y0 + 8 * math.sin(t + i), s)
    sun(c, t)
    hills(c)
    palm(c, 180, 900, 560, t, 0, 1)
    palm(c, 1760, 900, 520, t, 1.7, -1)
    bush(c, 420, 840, 0.7, '#2E7D32'); bush(c, 1510, 850, 0.65, '#388E3C')
    for i, (fx, col) in enumerate(((330, '#FF4081'), (560, '#FF9100'), (1380, '#E040FB'), (1600, '#FF4081'), (760, '#FFEA00'))):
        flower(c, fx, 900, col, t, i * 1.3)
    # parrot crosses 8s..14s
    pt = (t - 8.0) / 6.0
    look = (0.0, 0.0)
    for (t0, _, _) in SHOOT:
        if 0 <= t - t0 <= 1.3: look = (-0.5 + 1.0 * (t - t0) / 1.3, -0.9)
    if 0 <= pt <= 1:
        px, py = 2150 - 2400 * pt, 330 + 50 * math.sin(pt * 6 * math.pi)
        lx = max(-1, min(1, (px - 960) / 600)); look = (lx, -0.6)
    # monkey
    if t < 0.4:
        mx, hop = -300, 0
    elif t < 4.0:
        p = (t - 0.4) / 3.6
        mx = -300 + 1260 * (1 - (1 - p) ** 2)
        hop = 160 * abs(math.sin(3 * math.pi * p)) * (1 - 0.3 * p)
    else:
        mx, hop = 960, 0
    land = max(0.0, 1 - abs(t - 4.0) / 0.25) if t > 3.7 else 0
    idle = ss(4.2, 5.0, t)
    bob = idle * 14 * abs(math.sin(math.pi * t / 1.0))
    sq = 1 - 0.08 * land + 0.03 * idle * math.sin(2 * math.pi * t)
    tilt = math.radians(6) * math.sin(2 * math.pi * t / 2.0) * (0.4 + 0.6 * idle)
    wave = ss(5, 5.6, t) * (1 - ss(8.6, 9.2, t)) + ss(13.5, 14.1, t) * (1 - ss(17, 17.6, t))
    rest_r = math.radians(65 + 8 * math.sin(t * 3))
    if t < 4: rest_r = math.radians(20 + 30 * math.sin(t * 6))
    arm_r = (1 - wave) * rest_r + wave * math.radians(-58 + 25 * math.sin(t * 2 * math.pi * 2))
    arm_l = math.radians(115 - 8 * math.sin(t * 3))
    if t < 4: arm_l = math.radians(160 - 30 * math.sin(t * 6))
    if 9.5 < t < 12.5:  # both arms up, cheering the parrot
        k = ss(9.5, 10, t) * (1 - ss(12, 12.5, t))
        arm_l = (1 - k) * arm_l + k * math.radians(-120 + 15 * math.sin(t * 12))
    blink = 1.0
    for bt in (2.6, 6.3, 10.2, 15.4, 18.3):
        d = abs(t - bt)
        if d < 0.12: blink = d / 0.12
    # shadow
    sh = 1 - hop / 400
    ellipse(c, mx, 905, 120 * sh, 18 * sh); c.set_source_rgba(0, 0.25, 0, 0.25); c.fill()
    monkey(c, mx, 900 - hop - bob, t, sq, tilt, arm_r, arm_l, blink, look)
    if 0 <= pt <= 1:
        parrot(c, px, py, t)
    # butterflies in front
    fireflies(c, t)
    # fades
    a = max(1 - ss(0, 0.6, t), ss(DUR - 0.8, DUR, t))
    if a > 0:
        c.set_source_rgba(0.05, 0.04, 0.2, a); c.paint()

if __name__ == '__main__':
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    c = cairo.Context(surf)
    if len(sys.argv) > 1 and sys.argv[1] == 'stills':
        for t in map(float, sys.argv[2:]):
            c.save(); frame(c, t); c.restore(); surf.write_to_png(f'night_{t}.png')
    else:
        out = sys.stdout.buffer
        for i in range(int(DUR * FPS)):
            c.save(); frame(c, i / FPS); c.restore(); surf.flush()
            out.write(surf.get_data())
