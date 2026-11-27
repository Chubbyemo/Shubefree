"""Sleeping mouse: cheese blanket, blue nightcap, shadow instead of the bed (idempotent).

usage: python3 make_sleep.py <assets dir>
"""
import re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pixsvg import parse_rects

OUT = '#1b1b1d'
CHEESE, HOLE = '#f8d088', '#f2a93b'
BLUE, BLUE_D, WHITE = '#4a8fe7', '#2f6cc0', '#f4f4f4'
ZZZ = '#f5c518'
SHADOW = 'shadow'
LIGHT = '#fbe6b0'


def cells(rects):
    g = {}
    for x, y, w, h, c in rects:
        for yy in range(y, y + h):
            for xx in range(x, x + w):
                g[(xx, yy)] = c
    return g


def blanket(g):
    """Cheese blanket draped over the back half, wavy hem."""
    add = {}
    x0, x1 = 15, 27
    hem = {x: 14 for x in range(x0, x1 + 1)}
    tops = {}
    for x in range(x0, x1 + 1):
        top = min((y for (xx, y), c in g.items() if xx == x and c != ZZZ and 0 <= y <= 13), default=7)
        tops[x] = min(top, 8) + (1 if x in (x0, x1) else 0)
    for x in range(x0, x1 + 1):
        for y in range(tops[x], hem[x] + 1):
            add[(x, y)] = CHEESE
    for (x, y) in list(add):
        nb = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
        if any(q not in add for q in nb):
            add[(x, y)] = OUT
    for x in range(x0 + 1, x1):
        if add.get((x, tops[x] + 1)) == CHEESE:
            add[(x, tops[x] + 1)] = LIGHT
    for p in [(17, 10), (17, 11), (20, 9), (21, 9), (22, 12), (23, 12), (22, 13), (18, 13), (25, 10), (26, 12)]:
        if add.get(p) == CHEESE:
            add[p] = HOLE
    return add


def nightcap():
    add = {}
    cone = {3: (7, 14), 2: (7, 13), 1: (7, 12), 0: (6, 11), -1: (5, 9), -2: (4, 7)}
    for y, (a, b) in cone.items():
        for x in range(a, b + 1):
            add[(x, y)] = BLUE_D if (x - y) % 4 == 0 else BLUE
    for (x, y) in [(3, -1), (3, 0), (2, 0), (2, 1)]:  # floppy tip
        add[(x, y)] = BLUE
    for y in (4, 5):
        for x in range(6, 16):
            add[(x, y)] = WHITE
    for p in [(0, 2), (1, 2), (0, 3), (1, 3)]:  # pompom
        add[p] = WHITE
    ring = {}
    for (x, y) in add:
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            q = (x + dx, y + dy)
            if q not in add and (q[1] <= 5 or q[0] <= 2):
                ring[q] = OUT
    ring.update(add)
    return ring


def emit(add):
    by = {}
    for (x, y), c in sorted(add.items(), key=lambda t: (t[0][1], t[0][0])):
        by.setdefault(c, []).append((x, y))
    out = []
    for c, pts in by.items():
        rs, run = [], None
        for x, y in pts:
            if run and run[1] == y and run[0] + run[2] == x:
                run[2] += 1
            else:
                if run: rs.append(run)
                run = [x, y, 1]
        rs.append(run)
        head = '<g fill="#1b1b1d" fill-opacity="0.22">' if c == SHADOW else '<g fill="%s">' % c
        out.append(head + ''.join('<rect x="%d" y="%d" width="%d" height="1"/>' % tuple(r) for r in rs) + '</g>')
    return ''.join(out)


DY = 9  # no bed: drop the mouse to the ground line, soft shadow underneath


def has_bed(g):
    return any(c == CHEESE and y >= 18 for (x, y), c in g.items())


def lying(g):
    """Bed-less lying pose floating at the old height (mid-collapse)."""
    pts = [p for p, c in g.items() if c != ZZZ]
    xs = [x for x, y in pts]; ys = [y for x, y in pts]
    return bool(pts) and max(ys) < 23 and max(xs) - min(xs) > 20 and max(ys) - min(ys) < 15


def ground(g):
    """Set a bed-less lying frame on the same ground line, with the same shadow."""
    dy = 23 - max(y for (x, y), c in g.items() if c != ZZZ)
    final = {}
    for y, (a, b) in {24: (1, 28), 25: (4, 25)}.items():
        for x in range(a, b + 1):
            final[(x, y)] = SHADOW
    final.update({(x, y + dy): c for (x, y), c in g.items()})
    return final


def cozy(g):
    mouse = {p: c for p, c in g.items() if p[1] <= 14}  # drop the cheese bed and tail bits under the blanket
    mouse.update(blanket(mouse))
    mouse.update(nightcap())
    final = {}
    for y, (a, b) in {15: (1, 28), 16: (4, 25)}.items():
        for x in range(a, b + 1):
            final[(x, y + DY)] = SHADOW
    final.update({(x, y + DY): c for (x, y), c in mouse.items()})
    return final


def process(path):
    """Rewrite every lying-on-the-bed frame of an animation in the cozy style."""
    s = open(path, encoding='utf8').read()
    if '<!--cozy-->' in s:
        print('already cozy:', os.path.basename(path))
        return
    heads = list(re.finditer(r'<g class="f\d+">', s))
    pieces, last = [], 0
    for i, m in enumerate(heads):
        end = heads[i + 1].start() if i + 1 < len(heads) else s.rindex('</svg>')
        g = cells(parse_rects(s[m.end():end]))
        if has_bed(g) or lying(g):
            pieces.append(s[last:m.end()] + emit(cozy(g) if has_bed(g) else ground(g)) + '</g>')
            last = end
    pieces.append(s[last:].replace('</svg>', '<!--cozy--></svg>'))
    open(path, 'w', encoding='utf8').write(''.join(pieces))


def main(assets):
    # sleeping is the loop; the last collapse frame and first wake frame are the same pose
    for name in ('mouse-sleeping.svg', 'mouse-collapsing.svg', 'mouse-wake.svg'):
        process(os.path.join(assets, name))


if __name__ == '__main__':
    main(sys.argv[1])
