"""Generate the cheese-heist and rolling animations from the existing Chubby Mouse frames.
Usage: python3 make_tricks.py <theme assets dir>"""
import math, sys, os
sys.path.insert(0, os.path.dirname(__file__))
import pixsvg

A = sys.argv[1]
follow = pixsvg.frames(open(os.path.join(A, 'mouse-idle-follow.svg')).read())
cheese = pixsvg.frames(open(os.path.join(A, 'mouse-idle-cheese.svg')).read())
MOUSE = follow['f0'] + follow['eyes']
MOUSE_B = follow['f1'] + follow['eyes']
HOLD = cheese['f2']
HOLD_B = cheese['f3']
DARK, GREY, CH1, CH2 = '#1b1b1d', '#8d8d8d', '#f8d088', '#f2a93b'
GROUND = 26
HEAD = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="-12 -24 52 52" width="500" height="500" shape-rendering="crispEdges">'

def rects_svg(rects):
    by = {}
    for x, y, w, h, f in rects:
        by.setdefault(f, []).append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}"/>')
    return ''.join(f'<g fill="{f}">{"".join(v)}</g>' for f, v in by.items())

def hole(cx, size):
    """Pixel hole on the ground, size 0..3."""
    if size <= 0: return []
    widths = {1: [4], 2: [8, 6], 3: [12, 10, 6]}[size]
    out = []
    for i, w in enumerate(widths):
        y = GROUND - 1 + i
        out.append((cx - w // 2, y, w, 1, DARK))
    w0 = widths[0] + 2
    out.append((cx - w0 // 2, GROUND - 1, 1, 1, GREY))
    out.append((cx - w0 // 2 + w0 - 1, GROUND - 1, 1, 1, GREY))
    return out

WEDGE = [(32, 23, 2, 1, DARK), (31, 24, 1, 1, DARK), (34, 23, 2, 1, DARK), (36, 24, 1, 1, DARK),
         (30, 25, 8, 1, DARK), (32, 24, 4, 1, CH1), (31, 24, 1, 1, DARK), (33, 24, 1, 1, CH2),
         (29, 25, 1, 1, DARK), (38, 25, 1, 1, DARK)]
WEDGE = [(32, 22, 3, 1, DARK), (31, 23, 1, 1, DARK), (35, 23, 2, 1, DARK), (30, 24, 1, 1, DARK),
         (37, 24, 1, 1, DARK), (30, 25, 8, 1, DARK),
         (32, 23, 3, 1, CH1), (31, 24, 6, 1, CH1), (33, 24, 1, 1, CH2), (35, 23, 0, 0, CH2)]

def build(frames, ms, name, extra_css=''):
    """frames: list of (defs-id or None, dx, dy, extra_rects); one <g> per frame."""
    n = len(frames)
    total = n * ms
    css, body, defs = [], [], {}
    for i, (spr, dx, dy, extra) in enumerate(frames):
        a = 100 * i / n
        b = 100 * (i + 1) / n
        if i == 0:
            css.append(f'@keyframes f{i}{{0%{{opacity:1}}{b:.3f}%{{opacity:0}}100%{{opacity:0}}}}')
        elif i == n - 1:
            css.append(f'@keyframes f{i}{{0%{{opacity:0}}{a:.3f}%{{opacity:1}}100%{{opacity:1}}}}')
        else:
            css.append(f'@keyframes f{i}{{0%{{opacity:0}}{a:.3f}%{{opacity:1}}{b:.3f}%{{opacity:0}}100%{{opacity:0}}}}')
        css.append(f'.f{i}{{animation:f{i} {total}ms step-end {name}}}')
        inner = rects_svg(extra) if extra else ''
        if spr:
            defs[spr[0]] = spr[1]
            inner += f'<g clip-path="url(#ground)"><use href="#{spr[0]}" transform="translate({dx} {dy})"/></g>'
        body.append(f'<g class="f{i}" opacity="0">{inner}</g>')
    d = ''.join(f'<g id="{k}">{rects_svg(v)}</g>' for k, v in defs.items())
    return (HEAD + '<defs><clipPath id="ground"><rect x="-40" y="-60" width="140" height="86"/></clipPath>'
            + d + '<style>' + ''.join(css) + extra_css + '</style></defs>' + ''.join(body) + '</svg>')

def heist():
    M, MB, H, HB = ('m', MOUSE), ('mb', MOUSE_B), ('h', HOLD), ('hb', HOLD_B)
    F = []
    add = lambda spr, dx, dy, extra=(), k=1: F.extend([(spr, dx, dy, list(extra))] * k)
    shadow = lambda dx: [(7 + dx, 25, 10, 1, '#4a4a4a')]
    # 1. 站在原地，脚下开个洞
    add(M, 0, 0, WEDGE + shadow(0), 5)
    for s in (1, 2, 3): add(M, 0, 0, WEDGE + hole(12, s), 2)
    # 2. 钻下去
    for dy in (3, 7, 12, 18, 25): add(M, 0, dy, WEDGE + hole(12, 3))
    for s in (2, 1, 0): add(None, 0, 0, WEDGE + hole(12, s))
    # 3. 左边冒出洞，探头
    for s in (1, 2, 3): add(None, 0, 0, WEDGE + hole(2, s), 2)
    for dy in (22, 18, 14): add(M, -10, dy, WEDGE + hole(2, 3), 2)
    add(M, -10, 14, WEDGE + hole(2, 3), 4)
    add(MB, -10, 14, WEDGE + hole(2, 3), 4)
    for dy in (9, 4, 0): add(M, -10, dy, WEDGE + hole(2, 3))
    # 4. 踮脚走过去
    for i, dx in enumerate(range(-10, 11)):
        add(M if i % 2 == 0 else MB, dx, -1 if i % 2 else 0, WEDGE + hole(2, 3))
    # 5. 拿起奶酪
    add(M, 10, 0, WEDGE + hole(2, 3), 3)
    add(H, 10, -2, hole(2, 3), 2)
    add(H, 10, 0, hole(2, 3), 3)
    # 6. 飞快跑回去
    for i, dx in enumerate(range(10, -11, -2)):
        add(H if i % 2 == 0 else HB, dx, -1 if i % 2 else 0, hole(2, 3))
    # 7. 钻回洞里，洞消失
    for dy in (4, 10, 17, 25): add(H, -10, dy, hole(2, 3))
    for s in (2, 1, 0): add(None, 0, 0, hole(2, s), 2)
    add(None, 0, 0, [], 6)
    # 8. 回到原位，抱着奶酪冒出来
    for s in (1, 2, 3): add(None, 0, 0, hole(12, s))
    for dy in (20, 12, 5, 0): add(H, 0, dy, hole(12, 3))
    for s in (2, 1): add(H, 0, 0, hole(12, s))
    add(H, 0, 0, shadow(0), 4)
    add(HB, 0, 0, shadow(0), 4)
    add(H, 0, 0, shadow(0), 4)
    return build(F, 110, 'forwards')

def rotate(rects, deg, cx=12, cy=13):
    """Rotate pixel sprite around (cx, cy), snapping to the grid."""
    r = math.radians(deg)
    c, s = math.cos(r), math.sin(r)
    px = {}
    for x, y, w, h, f in rects:
        for yy in range(y, y + h):
            for xx in range(x, x + w):
                X, Y = xx + .5 - cx, yy + .5 - cy
                nx, ny = cx + X * c - Y * s, cy + X * s + Y * c
                px[(math.floor(nx), math.floor(ny))] = f
    # fill pinholes from 45° rotation
    if deg % 90:
        for (x, y), f in list(px.items()):
            for dx, dy in ((1, 0), (0, 1)):
                q = (x + dx, y + dy)
                if q not in px:
                    nb = [px.get((q[0] + a, q[1] + b)) for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1))]
                    if sum(1 for v in nb if v) >= 3: px[q] = f
    return [(x, y, 1, 1, f) for (x, y), f in px.items()]

def roll(direction):
    F = []
    steps = 8
    for i in range(steps):
        deg = direction * 360 * i / steps
        spr = (f'r{i}', rotate(MOUSE, deg))
        bob = -1 if i % 2 else 0
        dust = []
        if i % 2 == 0:
            x0 = 2 if direction > 0 else 21
            dust = [(x0, 24, 1, 1, '#b4b4b6'), (x0 - direction * 2, 23, 1, 1, '#d6c4c4')]
        F.append((spr, 0, bob, [(6, 25, 12, 1, '#4a4a4a')] + dust))
    return build(F, 125, 'infinite')

open(os.path.join(A, 'mouse-trick-heist.svg'), 'w').write(heist())
open(os.path.join(A, 'mouse-trick-roll-right.svg'), 'w').write(roll(1))
open(os.path.join(A, 'mouse-trick-roll-left.svg'), 'w').write(roll(-1))
print('ok')
