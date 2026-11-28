"""New mouse stickers drawn from scratch (ball roll, desk slide, robot lesson) + a sunny picnic picture.

usage: python3 make_more.py <out dir> [--sheet <dir>]
"""
import math, os, sys, random
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from make_gif import frame_grids, crop, to_gif

def rgb(h):
    h = h.lstrip('#'); return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))

OUT, BODY, LIGHT, PINK = rgb('#1b1b1d'), rgb('#8d8d8d'), rgb('#b4b4b6'), rgb('#d6c4c4')
CHEEK, SHADOW, WHITE = rgb('#e6a3ad'), rgb('#000000'), rgb('#ffffff')
BAG = rgb('#7a6a9a')


def ring(fill, color=OUT, diag=False):
    """Outline pixels just outside a filled set."""
    out = {}
    nb = ((1, 0), (-1, 0), (0, 1), (0, -1)) + (((1, 1), (-1, 1), (1, -1), (-1, -1)) if diag else ())
    for (x, y) in fill:
        for dx, dy in nb:
            q = (x + dx, y + dy)
            if q not in fill:
                out[q] = color
    return out


def line(p0, p1):
    (x0, y0), (x1, y1) = p0, p1
    n = max(abs(round(x1) - round(x0)), abs(round(y1) - round(y0)), 1)
    return [(round(x0 + (x1 - x0) * i / n), round(y0 + (y1 - y0) * i / n)) for i in range(n + 1)]


def shift(g, dx, dy):
    return {(x + dx, y + dy): c for (x, y), c in g.items()}


def over(*layers):
    out = {}
    for l in layers: out.update(l)
    return out


def art(rows, ox, oy, pal):
    g = {}
    for j, row in enumerate(rows):
        for i, ch in enumerate(row):
            if ch in pal: g[(ox + i, oy + j)] = pal[ch]
    return g


# ---------------------------------------------------------------- 1. ball roll
R = 8.5


def ball(theta, cx, cy, eyes='open'):
    """Round mouse rotated by theta (radians, clockwise), centre (cx, cy). Light stays top-left."""
    c, s = math.cos(theta), math.sin(theta)
    def local(X, Y):  # screen pixel -> upright ball coords
        dx, dy = X + 0.5 - cx, Y + 0.5 - cy
        return c * dx + s * dy, -s * dx + c * dy
    def scr(u, v):
        return math.floor(cx + c * u - s * v), math.floor(cy + s * u + c * v)

    def eye(u, v, ex):
        if eyes == 'open':
            return abs(u - ex) < 0.75 and -2.3 < v < -0.1
        if eyes == 'dizzy':  # x x
            return (abs(abs(u - ex) - abs(v + 1.2)) < 0.55) and abs(u - ex) < 1.4 and abs(v + 1.2) < 1.4
        return abs(v + 1.4 + abs(u - ex) * 0.9) < 0.55 and abs(u - ex) < 1.5  # happy ^ ^

    body, extra = {}, {}
    for Y in range(int(cy - 16), int(cy + 16)):
        for X in range(int(cx - 16), int(cx + 16)):
            u, v = local(X, Y)
            r = math.hypot(u, v)
            dx, dy = X + 0.5 - cx, Y + 0.5 - cy
            if r <= R:
                if r > R - 1.05:
                    col = OUT
                elif eye(u, v, -3.4) or eye(u, v, 3.4):
                    col = OUT
                elif abs(v - 1.4) < 0.6 and abs(u) < 1.05:
                    col = PINK
                elif math.hypot(abs(u) - 5.5, v - 1.4) < 0.9:
                    col = CHEEK
                elif math.hypot(dx + 3.2, dy + 3.4) < 2.4:
                    col = LIGHT  # highlight, fixed to the screen
                else:
                    col = BODY
                body[(X, Y)] = col
                continue
            for ex in (-5.6, 5.6):  # ears
                if math.hypot(u - ex, v + 7.0) <= 3.1:
                    extra[(X, Y)] = LIGHT if math.hypot(u - ex, v + 7.4) <= 1.5 else BODY
            for ax in (-1, 1):  # stubby arms
                if math.hypot((u - ax * 9.0) / 1.6, (v - 2.0) / 1.3) <= 1:
                    extra[(X, Y)] = BODY
            for fx in (-3.4, 3.4):  # stubby feet
                if math.hypot((u - fx) / 2.2, (v - 8.9) / 1.4) <= 1:
                    extra[(X, Y)] = BODY
    g = over(ring({**body, **extra}), extra, body)
    tail = [(8.4, 5.0), (10.6, 6.2), (12.4, 5.0), (12.4, 3.0), (11.0, 2.4)]
    pts = [scr(u, v) for u, v in tail]
    for a, b in zip(pts, pts[1:]):
        for q in line(a, b):
            if q not in body and q not in extra: g[q] = OUT
    return g


def ground_shadow(cx, y, w):
    return {(x, y): SHADOW for x in range(round(cx - w / 2), round(cx + w / 2))}


def ball_body(theta, cx, cy, r=8.6):
    """Round body (belly patch, stubby arms/feet, tail) rotated by theta."""
    c, sn = math.cos(theta), math.sin(theta)
    def local(X, Y):
        dx, dy = X + 0.5 - cx, Y + 0.5 - cy
        return c * dx + sn * dy, -sn * dx + c * dy
    def scr(u, v):
        return math.floor(cx + c * u - sn * v), math.floor(cy + sn * u + c * v)
    body, extra = {}, {}
    for Y in range(int(cy - 12), int(cy + 12)):
        for X in range(int(cx - 12), int(cx + 12)):
            u, v = local(X, Y)
            d = math.hypot(u, v)
            if d <= r:
                if d > r - 1.05: body[(X, Y)] = OUT
                elif math.hypot(u, v - 2.6) <= 4.0: body[(X, Y)] = LIGHT
                else: body[(X, Y)] = BODY
                continue
            for ax in (-1, 1):
                if math.hypot((u - ax * (r + 0.7)) / 1.6, (v - 0.5) / 1.3) <= 1: extra[(X, Y)] = BODY
            for fx in (-3.4, 3.4):
                if math.hypot((u - fx) / 2.0, (v - r - 0.3) / 1.3) <= 1: extra[(X, Y)] = BODY
    g = over(ring({**body, **extra}), extra, body)
    tail = [(r - 0.8, 4.2), (r + 1.6, 5.4), (r + 3.4, 4.2), (r + 3.6, 2.0), (r + 2.4, 1.0)]
    pts = [scr(u, v) for u, v in tail]
    for p0, p1 in zip(pts, pts[1:]):
        for q in line(p0, p1):
            if q not in body and q not in extra: g[q] = OUT
    return g


def ball_roll():
    m0 = base_mouse()
    G = 32
    def head(kind):
        return {p: c for p, c in with_eyes(m0, kind).items() if p[1] <= 14}
    seq = []
    def fr(deg, ms, eyes='dot', hop=0):
        th = math.radians(deg)
        cx = 12 + 8.6 * th * 0.5
        cy = 22.6 - hop
        body = ball_body(th, cx, cy)
        hd = shift(head(eyes), round(cx - 12), -hop + (1 if abs(deg) >= 60 else 0))
        seq.append((over(ground_shadow(cx, G, 15 - hop), body, hd), ms))
    fr(0, 500)
    fr(0, 150, hop=1)
    fr(0, 120)
    for d in (30, 60, 90): fr(d, 100)
    fr(120, 450, 'wide')
    for d in (90, 60, 30, 0): fr(d, 100)
    for d in (-30, -60, -90): fr(d, 100)
    fr(-120, 450, 'wide')
    for d in (-90, -60, -30): fr(d, 100)
    fr(0, 150, hop=1)
    fr(0, 800, 'happy')
    return seq


# ---------------------------------------------------------------- shared mouse
ASSETS = '/home/lenovo/clawd-buddy/themes/chubby-mouse/assets'


def base_mouse():
    """Front-facing mouse without eyes or ground shadow (from the follow pose)."""
    g = frame_grids(os.path.join(ASSETS, 'mouse-idle-follow.svg'))[0][0]
    return {p: c for p, c in g.items() if c != SHADOW}


def with_eyes(g, kind, bags=False):
    g = dict(g)
    L, Rr = (6, 7, 8), (14, 15, 16)
    for xs in (L, Rr):
        for x in xs:
            for y in (7, 8, 9):
                if g.get((x, y)) in (OUT, LIGHT, BODY): g[(x, y)] = BODY
        m = xs[1]
        if kind == 'tired':
            for x in xs: g[(x, 7)] = OUT
            g[(m, 8)] = OUT
        elif kind == 'closed':
            for x in xs: g[(x, 8)] = OUT
        elif kind == 'dot':
            g[(m, 7)] = OUT; g[(m, 8)] = OUT
        elif kind == 'happy':
            g[(xs[0], 8)] = OUT; g[(m, 7)] = OUT; g[(xs[2], 8)] = OUT
        elif kind == 'wide':
            for x in xs:
                for y in (6, 7, 8, 9): g[(x, y)] = WHITE
            for x in (xs[0] - 1, xs[2] + 1):
                for y in (6, 7, 8, 9): g[(x, y)] = OUT
            for x in xs: g[(x, 5)] = OUT; g[(x, 10)] = OUT
            g[(m, 7)] = OUT; g[(m, 8)] = OUT
        if bags:
            for x in xs: g[(x, 10 if kind == 'wide' else 9)] = BAG
    return g


def lying_mouse():
    """The original lying-down pose (end of the collapse), without the bed."""
    here = os.path.dirname(os.path.abspath(__file__))
    g = frame_grids(os.path.join(here, 'lying.svg'))[0][0]
    return {p: c for p, c in g.items() if p[1] <= 13 and c != SHADOW}


def rot90(g, cw=True):
    """Exact quarter turn about the origin."""
    return {((-y, x) if cw else (y, -x)): c for (x, y), c in g.items()}


def window(g, x0, y0, w, h):
    return {(x, y): c for (x, y), c in g.items() if x0 <= x < x0 + w and y0 <= y < y0 + h}


# ---------------------------------------------------------------- 2. desk slide
WOOD, WOOD_D, WOOD_DD = rgb('#d39b5e'), rgb('#a8733f'), rgb('#7f5530')
SILVER, SILVER_D = rgb('#c9ccd2'), rgb('#9da2ab')
CHAIR, CHAIR_L = rgb('#3d4552'), rgb('#5b6576')
CHEESE, HOLE = rgb('#f8d088'), rgb('#f2a93b')
GLOW = rgb('#8a95ab')
COFFEE, MUG = rgb('#6b4226'), rgb('#f4f4f4')


def outlined(fill):
    return over(ring(fill), fill)


def desk_scene(steam):
    back, front = {}, {}
    # office chair back, visible once the mouse slides down
    chair = {(x, y): (CHAIR_L if y == 3 or x == 5 else CHAIR) for x in range(5, 20) for y in range(3, 18)}
    back.update(outlined(chair))
    # desk with a front panel and a drawer
    desk = {}
    for x in range(-3, 26):
        for y in range(18, 34):
            desk[(x, y)] = WOOD if y <= 19 else (WOOD_D if y == 20 else WOOD)
    for x in range(-1, 24):
        desk[(x, 33)] = WOOD_D
    for x in range(3, 20):
        desk[(x, 23)] = WOOD_D; desk[(x, 28)] = WOOD_D
    for y in range(23, 29):
        desk[(3, y)] = WOOD_D; desk[(19, y)] = WOOD_D
    for x in (10, 11, 12): desk[(x, 25)] = WOOD_DD
    front.update(outlined(desk))
    # laptop lid (back side) with a cheese logo
    lid = {(x, y): SILVER for x in range(4, 21) for y in range(12, 18)}
    for x in range(4, 21): lid[(x, 17)] = SILVER_D
    front.update(outlined(lid))
    front.update(art(['  o  ', ' oCo ', 'oChCo', 'ooooo'], 10, 12, {'o': OUT, 'C': CHEESE, 'h': HOLE}))
    # mug with steam
    mug = {(x, y): MUG for x in range(-1, 3) for y in range(14, 18)}
    for x in range(-1, 3): mug[(x, 14)] = COFFEE
    m = outlined(mug)
    for q in ((-3, 15), (-3, 16), (-2, 14), (-2, 17)): m[q] = OUT
    front.update(m)
    wisps = {0: [(-1, 12), (0, 11), (0, 10), (-1, 9), (-1, 8), (0, 7), (2, 12), (1, 11), (2, 10), (2, 9), (1, 8)],
             1: [(0, 12), (-1, 11), (-1, 10), (0, 9), (0, 8), (-1, 7), (1, 12), (2, 11), (1, 10), (1, 9), (2, 8), (2, 7)],
             2: [(-1, 12), (-1, 11), (0, 10), (0, 9), (-1, 8), (2, 12), (2, 11), (1, 10), (2, 9), (2, 8), (1, 7), (1, 6)]}
    for i, (x, y) in enumerate(wisps[steam % 3]):
        front[(x, y)] = rgb('#9aa3b0') if y >= 9 else rgb('#c3c9d2')
    floor = {(x, 34): SHADOW for x in range(-5, 32)}
    return back, front, floor


def glow(g):
    return {p: (GLOW if c == BODY else c) for p, c in g.items()}


def desk_slide():
    """Exhausted at the laptop, then slowly sinks behind the desk and is gone."""
    m0 = base_mouse()
    seq = []
    t = [0]
    def fr(mouse, ms):
        back, front, floor = desk_scene(t[0]); t[0] += 1
        seq.append((window(over(back, mouse, floor, front), -6, -5, 38, 40), ms))
    tired = glow(with_eyes(m0, 'tired', True))
    shut = glow(with_eyes(m0, 'closed', True))
    for ms in (300, 300, 300): fr(tired, ms)
    fr(shut, 140)
    for ms in (300, 300): fr(tired, ms)
    fr(shut, 140)
    fr(tired, 300)
    for dy, ms in ((1, 450), (2, 300), (3, 260), (5, 220), (7, 200), (9, 180), (11, 180), (13, 200), (15, 260), (17, 300)):
        fr(shift(shut, 0, dy), ms)
    for ms in (300, 300, 300, 300): fr({}, ms)
    return seq


# ---------------------------------------------------------------- 3. robot lesson
R_DARK, R_MID, R_SIL, R_JOINT = rgb('#33373e'), rgb('#4a5059'), rgb('#c5cad3'), rgb('#22252a')
LED, STICK, STICK_TIP = rgb('#49d6e8'), rgb('#a8733f'), rgb('#f4f4f4')
GLASS, CHECK, SWEAT, STAR = rgb('#1b1b1d'), rgb('#58c46b'), rgb('#6ab4f0'), rgb('#f5c518')


def capsule(g, p0, p1, r, col):
    (x0, y0), (x1, y1) = p0, p1
    L2 = (x1 - x0) ** 2 + (y1 - y0) ** 2 or 1e-9
    for Y in range(int(min(y0, y1) - r - 1), int(max(y0, y1) + r + 2)):
        for X in range(int(min(x0, x1) - r - 1), int(max(x0, x1) + r + 2)):
            px, py = X + 0.5, Y + 0.5
            t = max(0, min(1, ((px - x0) * (x1 - x0) + (py - y0) * (y1 - y0)) / L2))
            if math.hypot(px - x0 - t * (x1 - x0), py - y0 - t * (y1 - y0)) <= r:
                g[(X, Y)] = col


POSES = {
    #        L shoulder,elbow,hand          R shoulder,elbow,hand          L hip,knee,ankle            R hip,knee,ankle   torso dy
    'stand': ([(-5, 3), (-6, 7.5), (-6, 12)], [(5, 3), (6, 7.5), (6, 12)], [(-2, 12), (-2, 17.5), (-2, 22.5)], [(2, 12), (2, 17.5), (2, 22.5)], 0),
    'arm':   ([(-5, 3), (-6, 7.5), (-6, 12)], [(5, 3), (7, -1.5), (7.5, -6)], [(-2, 12), (-2, 17.5), (-2, 22.5)], [(2, 12), (2, 17.5), (2, 22.5)], 0),
    'leg':   ([(-5, 3), (-8, 6), (-11, 7)], [(5, 3), (8, 6), (11, 7)], [(-2, 12), (-2, 17.5), (-2, 22.5)], [(2, 12), (6, 15), (6, 19.5)], 0),
    'sit':   ([(-5, 11), (-8, 14), (-9, 18)], [(5, 11), (8, 14), (9, 18)], [(-2, 20), (-5, 21), (-8, 22.5)], [(2, 20), (5, 21), (8, 22.5)], 8),
}


def robot(pose, tilt=0.0):
    """Slim humanoid. Origin at the neck; feet rest on y=24."""
    la, ra, ll, rl, dy = POSES[pose]
    fill = {}
    # legs behind the torso
    for leg in (ll, rl):
        hip, knee, ank = leg
        capsule(fill, hip, knee, 1.4, R_MID)
        capsule(fill, knee, ank, 1.3, R_DARK)
        fill[(math.floor(knee[0]), math.floor(knee[1]))] = R_SIL
        fx = math.floor(ank[0]); fy = math.floor(ank[1]) + 1
        for x in range(fx - 2, fx + 2):
            fill[(x, fy)] = R_DARK
        if pose != 'sit' or True:
            fill[(fx - 2, fy)] = R_JOINT
    # torso
    for y in range(1 + dy, 12 + dy):
        w = 4 if y < 9 + dy else 3
        for x in range(-w, w):
            fill[(x, y)] = R_DARK
    for y in range(2 + dy, 6 + dy):
        for x in range(-3, 3):
            fill[(x, y)] = R_SIL if y < 5 + dy else R_MID
    fill[(-1, 3 + dy)] = LED; fill[(0, 3 + dy)] = LED
    for x in range(-3, 3):
        fill[(x, 9 + dy)] = R_JOINT
    # arms in front
    for arm in (la, ra):
        sh, el, ha = arm
        capsule(fill, sh, el, 1.25, R_MID)
        capsule(fill, el, ha, 1.15, R_DARK)
        fill[(math.floor(sh[0]), math.floor(sh[1]))] = R_SIL
        fill[(math.floor(sh[0]) - (1 if sh[0] < 0 else 0), math.floor(sh[1]))] = R_SIL
    # head: rounded helmet with a black visor and an LED strip
    hy = -4 + dy
    for y in range(hy - 4, hy + 4):
        for x in range(-4, 4):
            if math.hypot((x + 0.5) / 4.0, (y + 0.5 - hy) / 4.0) <= 1.0:
                fill[(x, y)] = R_SIL
    for y in range(hy - 2, hy + 2):
        for x in range(-3, 3):
            if math.hypot((x + 0.5) / 3.0, (y + 0.5 - hy + 0.2) / 2.2) <= 1.0:
                fill[(x, y)] = R_JOINT
    for x in range(-2, 2):
        fill[(x, hy - 1)] = LED
    fill[(0, hy + 4)] = R_DARK; fill[(-1, hy + 4)] = R_DARK
    g = over(ring(fill), fill)
    if tilt:
        g = rotate(g, tilt, (0, 24))
    return g


def rotate(g, th, pivot):
    """Rotate a pixel dict about pivot by th radians (inverse nearest sampling)."""
    c, s = math.cos(th), math.sin(th)
    xs = [x for x, y in g]; ys = [y for x, y in g]
    px, py = pivot
    out = {}
    for Y in range(min(ys) - 12, max(ys) + 12):
        for X in range(min(xs) - 12, max(xs) + 12):
            dx, dy = X + 0.5 - px, Y + 0.5 - py
            u, v = c * dx + s * dy + px, -s * dx + c * dy + py
            q = (math.floor(u), math.floor(v))
            if q in g:
                out[(X, Y)] = g[q]
    return out


def glasses(g, glint=False):
    g = dict(g)
    for x0 in (5, 13):
        for x in range(x0, x0 + 5):
            g[(x, 6)] = GLASS; g[(x, 10)] = GLASS
        for y in range(6, 11):
            g[(x0, y)] = GLASS; g[(x0 + 4, y)] = GLASS
        for x in range(x0 + 1, x0 + 4):
            for y in range(7, 10):
                g[(x, y)] = rgb('#a9c4d6')
        g[(x0 + 2, 8)] = OUT
        if glint:
            g[(x0 + 1, 7)] = WHITE; g[(x0 + 2, 7)] = WHITE; g[(x0 + 1, 8)] = WHITE
    for x in range(10, 13):
        g[(x, 7)] = GLASS
    g[(4, 7)] = GLASS; g[(18, 7)] = GLASS
    return g


def pointer(g, to):
    g = dict(g)
    pts = line((16, 19), to)
    for q in pts[:-1]:
        g[q] = STICK
    g[pts[-1]] = STICK_TIP
    g[(16, 19)] = OUT; g[(16, 20)] = OUT
    return g


def check(ox, oy):
    return art(['      o', '     oC', 'o   oC ', 'oC oC  ', ' oCC   ', '  o    '], ox, oy, {'o': CHECK, 'C': CHECK})


def stars(ox, oy, phase):
    pts = [(-5, 0), (0, -2), (5, 0), (0, 2)]
    out = {}
    for i, (x, y) in enumerate(pts):
        if (i + phase) % 2 == 0:
            for dx, dy in ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)):
                out[(ox + x + dx, oy + y + dy)] = STAR if (dx, dy) != (0, 0) else WHITE
    return out


def sweat(ox, oy):
    return art([' s ', 'sSs', 'sss'], ox, oy, {'s': SWEAT, 'S': WHITE})


def robot_lesson():
    m0 = base_mouse()
    RX = 32
    seq = []
    def fr(mouse, rob, ms, fx=None):
        seq.append((over(shift(rob, RX, 0), mouse, fx or {}), ms))
    teach = glasses(with_eyes(m0, 'dot'))
    glint = glasses(with_eyes(m0, 'dot'), glint=True)
    up, down = (24, 6), (28, 21)
    fr(teach, robot('stand'), 600)
    fr(glint, robot('stand'), 140)
    fr(teach, robot('stand'), 400)
    fr(pointer(teach, up), robot('stand'), 500)
    fr(pointer(teach, up), robot('arm'), 300)
    fr(pointer(teach, up), robot('arm'), 700, check(RX + 1, -15))
    fr(teach, robot('stand'), 400)
    fr(pointer(teach, down), robot('stand'), 500)
    fr(pointer(teach, down), robot('leg'), 260)
    fr(pointer(teach, down), robot('leg', math.radians(8)), 160)
    fr(pointer(teach, down), robot('leg', math.radians(-7)), 160)
    fr(pointer(teach, down), robot('leg', math.radians(12)), 160)
    fr(pointer(teach, down), robot('leg', math.radians(-12)), 140)
    fr(with_eyes(glasses(m0), 'wide'), robot('sit'), 180)
    for ph in range(4):
        fr(glasses(with_eyes(m0, 'dot')), robot('sit'), 200, stars(RX, -1, ph))
    for ph in range(3):
        fr(over(glasses(with_eyes(m0, 'closed')), sweat(22, 3)), robot('sit'), 260, stars(RX, -1, ph))
    fr(glint, robot('sit'), 500, stars(RX, -1, 1))
    return seq


# ---------------------------------------------------------------- 4. picnic picture
def picnic():
    W, H, HZ = 128, 72, 30
    rnd = random.Random(5)
    px = {}
    sky = ['#9fd3f2', '#b0dbf4', '#c2e3f5', '#d3eaf5', '#e2f0f2']
    for y in range(HZ):
        for x in range(W):
            px[(x, y)] = rgb(sky[min(4, y * 5 // HZ)])
    # sun with soft halo and rays
    SX, SY = 70, 9
    for y in range(SY - 9, SY + 10):
        for x in range(SX - 9, SX + 10):
            d = math.hypot(x - SX, y - SY)
            if d <= 4.2: px[(x, y)] = rgb('#fff3b0') if d < 3 else rgb('#ffe27a')
            elif d <= 6.5 and (x, y) in px: px[(x, y)] = rgb('#f3f4d8') if y < HZ else px[(x, y)]
    for k in range(8):
        a = k * math.pi / 4
        for r in (8, 9):
            px[(round(SX + r * math.cos(a)), round(SY + r * math.sin(a)))] = rgb('#ffe27a')
    def cloud(cx, cy, w):
        for y in range(cy - 2, cy + 2):
            for x in range(cx - w, cx + w):
                if ((x - cx) / w) ** 2 + ((y - cy) / 2.2) ** 2 <= 1 or (abs(x - cx + w / 3) < w / 2.4 and cy - 3 <= y < cy):
                    px[(x, y)] = WHITE
    cloud(44, 8, 7); cloud(96, 13, 6); cloud(20, 15, 5)
    # distant tree line
    for x in range(W):
        top = HZ - 3 - round(2.2 * abs(math.sin(x * 0.35)) + 1.5 * abs(math.sin(x * 0.13 + 1)))
        for y in range(top, HZ):
            px[(x, y)] = rgb('#5f9a5a') if y > top + 1 else rgb('#78b06a')
    # meadow
    greens = ['#8fcb6b', '#86c264', '#7db95d', '#74b056']
    for y in range(HZ, H):
        for x in range(W):
            px[(x, y)] = rgb(greens[min(3, (y - HZ) * 4 // (H - HZ))])
    for _ in range(260):
        x, y = rnd.randrange(W), rnd.randrange(HZ + 1, H)
        px[(x, y)] = rgb('#a8dc82'); 
        if y + 1 < H: px[(x, y + 1)] = rgb('#6aa64e')
    for _ in range(40):
        x, y = rnd.randrange(W), rnd.randrange(HZ + 3, H)
        c = rnd.choice(['#ffffff', '#ffe066', '#ffb3c6', '#c9a7f5'])
        for dx, dy in ((0, 0), (1, 0), (-1, 0), (0, -1), (0, 1)):
            px[(x + dx, y + dy)] = rgb(c) if (dx, dy) != (0, 0) else rgb('#f2a93b')
    # trees framing the scene (canopy shaded from the sun side)
    def tree(cx, base, r, trunk_h):
        for y in range(base - trunk_h, base + 1):
            for x in range(cx - 2, cx + 2):
                px[(x, y)] = rgb('#8a5a33') if x < cx + 1 else rgb('#6b4426')
        for y in range(base - 1, base + 3):  # soft, dithered shade under the tree
            for x in range(cx - r - 2, cx + r + 3):
                e = ((x - cx) / (r + 2)) ** 2 + ((y - base - 0.5) / 2.2) ** 2
                if (x, y) in px and (e <= 0.55 or (e <= 1 and (x + y) % 2 == 0)):
                    px[(x, y)] = rgb('#68a650')
        blobs = [(cx, base - trunk_h - r + 2, r)]
        for i in range(7):
            a = i * 2 * math.pi / 7
            blobs.append((cx + 0.7 * r * math.cos(a), base - trunk_h - r + 2 + 0.6 * r * math.sin(a), r * 0.55))
        for y in range(base - trunk_h - 2 * r - 4, base - trunk_h + 6):
            for x in range(cx - 2 * r, cx + 2 * r):
                inside = [b for b in blobs if math.hypot(x - b[0], y - b[1]) <= b[2]]
                if not inside: continue
                bx, by, br = inside[-1]
                lit = ((x - bx) * 0.5 - (y - by)) / br  # light from the upper right
                c = '#7cc35c' if lit > 0.55 else '#5aa548' if lit > -0.1 else '#3f8a3c' if lit > -0.7 else '#2f6e33'
                px[(x, y)] = rgb(c)
        for _ in range(int(r * 2)):
            x, y = cx + rnd.randint(-r, r), base - trunk_h - r + rnd.randint(-r + 2, r - 2)
            if px.get((x, y)) in (rgb('#5aa548'), rgb('#7cc35c')):
                px[(x, y)] = rgb('#f28aa0') if rnd.random() < 0.3 else rgb('#9fdc78')
    tree(10, 52, 13, 14)
    tree(118, 50, 12, 13)
    tree(30, 34, 6, 5)
    tree(103, 33, 5, 4)
    # dappled sunlight
    for _ in range(18):
        x, y = rnd.randrange(30, 100), rnd.randrange(HZ + 6, H - 2)
        for dx in range(rnd.choice((2, 3))):
            if (x + dx, y) in px: px[(x + dx, y)] = rgb('#b4e38c')
    # picnic blanket (gingham)
    MX0, MX1, MY0, MY1 = 36, 92, 48, 64
    mat = {}
    for y in range(MY0, MY1):
        skew = (MY1 - y) // 3
        for x in range(MX0 + skew, MX1 - skew // 2):
            a, b = (x // 3) % 2, (y // 2) % 2
            mat[(x, y)] = rgb('#e05a5a') if a and b else rgb('#f4f4f4') if not a and not b else rgb('#f0a6a6')
    for p, c in ring(mat).items():
        px[p] = rgb('#b84444')
    px.update(mat)
    for x in range(MX0 + 2, MX1 - 2):
        px[(x, MY1)] = rgb('#5e9a47')  # shadow under the front edge
    # the mouse, lying in the sun, with a cheese snack and a drink
    lie = lying_mouse()
    xs = [x for x, y in lie]; ys = [y for x, y in lie]
    lie = shift(lie, 52 - min(xs), 58 - max(ys))
    for x in range(53, 80):
        px[(x, 59)] = rgb('#c98a8a')
    px.update(lie)
    px.update(art(['    ooo', '  ooCCo', 'ooCCCCo', 'oChCChO', 'ooooooo'], 82, 52, {'o': OUT, 'O': OUT, 'C': CHEESE, 'h': HOLE}))
    for x in range(81, 90): px[(x, 57)] = rgb('#dfe6ee')
    glass = art(['  r ', ' r  ', 'oooo', 'oJJo', 'oJJo', 'oJJo', 'oooo'], 44, 50, {'o': OUT, 'J': rgb('#ffa94d'), 'r': rgb('#e05a5a')})
    px.update(glass)
    # a butterfly
    px.update(art(['p p', ' o ', 'p p'], 98, 40, {'p': rgb('#ffb3c6'), 'o': OUT}))
    im = Image.new('RGB', (W, H))
    for (x, y), c in px.items():
        if 0 <= x < W and 0 <= y < H: im.putpixel((x, y), c)
    return im.resize((W * 15, H * 15), Image.NEAREST)


def preview(seq, path, scale=6, cols=8):
    ims = [im for im, _ in crop(seq, 240)]
    w = ims[0].width
    rows = (len(ims) + cols - 1) // cols
    sheet = Image.new('RGB', (w * cols, w * rows), (237, 237, 237))
    for i, im in enumerate(ims):
        sheet.paste(im, ((i % cols) * w, (i // cols) * w), im)
    sheet.save(path)


def main(argv):
    out = argv[0]
    new = os.path.join(out, '新增表情')
    os.makedirs(new, exist_ok=True)
    for name, f in (('滚来滚去', ball_roll), ('溜了', desk_slide), ('教机器人', robot_lesson)):
        fr = crop(f(), 240)
        dst = os.path.join(new, name + '.gif')
        to_gif(fr, dst)
        print('%-8s %3d帧 %5.1fs %4dKB  %s' % (name, len(fr), sum(m for _, m in fr) / 1000, os.path.getsize(dst) // 1024, fr[0][0].size))
    pic = os.path.join(out, '插画-草地晒太阳-1920x1080.png')
    picnic().save(pic, optimize=True)
    print(pic, os.path.getsize(pic) // 1024, 'KB')
    if '--sheet' in argv:
        d = argv[argv.index('--sheet') + 1]
        for n, f in (('ball', ball_roll), ('desk', desk_slide), ('robot', robot_lesson)):
            preview(f(), os.path.join(d, n + '.png'))


if __name__ == '__main__':
    main(sys.argv[1:])
