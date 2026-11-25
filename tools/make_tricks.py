"""Generate the cheese-heist and crab-walk animations from the existing Chubby Mouse frames.
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
    # keep paint order (later rects on top, e.g. eyes over the face), grouping runs of one colour
    out, cur, run = [], None, []
    for x, y, w, h, f in list(rects) + [(0, 0, 0, 0, None)]:
        if f != cur and run:
            out.append(f'<g fill="{cur}">{"".join(run)}</g>')
            run = []
        cur = f
        if f: run.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}"/>')
    return ''.join(out)

def hole(cx, size):
    """Pixel hole on the ground (rows 23-25, the bottom of the visible window), size 0..3."""
    if size <= 0: return []
    rows = {1: [(25, 4)], 2: [(24, 6), (25, 8)], 3: [(23, 6), (24, 10), (25, 12)]}[size]
    out = []
    for y, w in rows:
        out.append((cx - w // 2, y, w, 1, DARK))
    y0, w0 = rows[-1]
    out.append((cx - w0 // 2 - 1, y0, 1, 1, GREY))
    out.append((cx - w0 // 2 + w0, y0, 1, 1, GREY))
    return out

WEDGE = [(27, 22, 3, 1, DARK), (26, 23, 1, 1, DARK), (30, 23, 2, 1, DARK), (25, 24, 1, 1, DARK),
         (32, 24, 1, 1, DARK), (25, 25, 8, 1, DARK),
         (27, 23, 3, 1, CH1), (26, 24, 6, 1, CH1), (28, 24, 1, 1, CH2)]

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
            use = f'<use href="#{spr[0]}" transform="translate({dx} {dy})"/>'
            inner += f'<g clip-path="url(#ground)">{use}</g>' if dy > 0 else use
        body.append(f'<g class="f{i}" opacity="0">{inner}</g>')
    d = ''.join(f'<g id="{k}">{rects_svg(v)}</g>' for k, v in defs.items())
    return (HEAD + '<defs><clipPath id="ground"><rect x="-40" y="-60" width="140" height="85"/></clipPath>'
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
    for s in (1, 2, 3): add(None, 0, 0, WEDGE + hole(4, s), 2)
    for dy in (22, 18, 14): add(M, -8, dy, WEDGE + hole(4, 3), 2)
    add(M, -8, 14, WEDGE + hole(4, 3), 4)
    add(MB, -8, 14, WEDGE + hole(4, 3), 4)
    for dy in (9, 4, 0): add(M, -8, dy, WEDGE + hole(4, 3))
    # 4. 踮脚走过去
    for i, dx in enumerate(range(-8, 9)):
        add(M if i % 2 == 0 else MB, dx, -1 if i % 2 else 0, WEDGE + hole(4, 3))
    # 5. 拿起奶酪
    add(M, 8, 0, WEDGE + hole(4, 3), 3)
    add(H, 8, -2, hole(4, 3), 2)
    add(H, 8, 0, hole(4, 3), 3)
    # 6. 飞快跑回去
    for i, dx in enumerate(range(8, -9, -2)):
        add(H if i % 2 == 0 else HB, dx, -1 if i % 2 else 0, hole(4, 3))
    # 7. 钻回洞里，洞消失
    for dy in (4, 10, 17, 25): add(H, -8, dy, hole(4, 3))
    for s in (2, 1, 0): add(None, 0, 0, hole(4, s), 2)
    add(None, 0, 0, [], 6)
    # 8. 回到原位，抱着奶酪冒出来
    for s in (1, 2, 3): add(None, 0, 0, hole(12, s))
    for dy in (20, 12, 5, 0): add(H, 0, dy, hole(12, 3))
    for s in (2, 1): add(H, 0, 0, hole(12, s))
    add(H, 0, 0, shadow(0), 4)
    add(HB, 0, 0, shadow(0), 4)
    add(H, 0, 0, shadow(0), 4)
    return build(F, 110, 'forwards')

def crab_frames():
    """Sideways crab scuttle: body lifted, big flat feet stepping in and out, claws snapping."""
    body = [(x, y - 3, w, h, f) for x, y, w, h, f in MOUSE if y <= 23 or x >= 18]
    LIGHT = '#b4b4b6'

    def foot(cx):
        x0 = cx - 4
        return [(x0 + 1, 23, 7, 1, DARK), (x0, 24, 1, 1, DARK), (x0 + 1, 24, 7, 1, GREY), (x0 + 8, 24, 1, 1, DARK),
                (x0, 25, 9, 1, DARK), (x0 + 2, 24, 2, 1, LIGHT), (x0 + 3, 23, 1, 1, GREY), (x0 + 5, 23, 1, 1, GREY)]

    def leg(x_top, x_bot):
        # leg from body bottom (y=20) to foot top (y=23)
        return [(x_top, 21, 1, 1, DARK), (x_bot, 22, 1, 1, DARK)]

    def claw(cx, open_):
        if open_:
            return [(cx - 1, 12, 1, 2, DARK), (cx + 1, 12, 1, 2, DARK), (cx, 14, 1, 1, DARK),
                    (cx, 15, 1, 1, DARK), (cx - 1, 14, 1, 1, '#d6c4c4'), (cx + 1, 14, 1, 1, '#d6c4c4')]
        return [(cx - 1, 13, 3, 1, DARK), (cx - 1, 14, 1, 1, DARK), (cx + 1, 14, 1, 1, DARK),
                (cx, 14, 1, 1, '#d6c4c4'), (cx, 15, 1, 1, DARK)]

    wide = foot(5) + foot(19) + leg(10, 9) + leg(15, 16) + claw(4, True) + claw(19, True)
    narrow = foot(8) + foot(17) + leg(10, 10) + leg(15, 15) + claw(5, False) + claw(18, False)
    shadow = []
    return [(body + wide, 0), (body + narrow, -1)], shadow

def crab():
    poses, shadow = crab_frames()
    F = []
    for i in range(4):
        rects, bob = poses[i % 2]
        F.append((('c%d' % (i % 2), rects), 0, bob, shadow))
    return build(F, 130, 'infinite')

open(os.path.join(A, 'mouse-trick-heist.svg'), 'w').write(heist())
open(os.path.join(A, 'mouse-trick-crab.svg'), 'w').write(crab())
print('ok')
