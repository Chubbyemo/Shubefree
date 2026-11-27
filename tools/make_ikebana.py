"""Idle animation: the mouse arranges rare flowers in a vase, one stem at a time.

usage: python3 make_ikebana.py <assets dir>                 writes mouse-idle-ikebana.svg
       python3 make_ikebana.py <assets dir> --sheet <dir>   also writes flower/frame previews there
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pixsvg


def rects_svg(rects):
    # keep paint order (later rects on top), grouping runs of one colour
    out, cur, run = [], None, []
    for x, y, w, h, f in list(rects) + [(0, 0, 0, 0, None)]:
        if f != cur and run:
            out.append(f'<g fill="{cur}">{"".join(run)}</g>')
            run = []
        cur = f
        if f: run.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}"/>')
    return ''.join(out)

A = sys.argv[1]
OUT_DIR = A
DARK = '#1b1b1d'
GREY, GREY_L = '#8d8d8d', '#b4b4b6'
PINK = '#d6c4c4'
BLUSH = '#f0a0a8'
GOLD = '#f5c518'
HEAD = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="-12 -24 52 52" width="500" height="500" shape-rendering="crispEdges">'

# ---------------------------------------------------------------- flowers
# Each flower: ASCII art + palette + anchor (where the stem meets the head, in art coords).
# '.' is transparent. Art is drawn with its anchor placed on the end of the stem.

FLOWERS = {}


def flower(name, art, pal, anchor, stem='#4e8a3c', leaves=()):
    rows = [r for r in art.strip('\n').split('\n')]
    rows = [r.strip() for r in rows]
    FLOWERS[name] = dict(rows=rows, pal=pal, anchor=anchor, stem=stem, leaves=leaves)


# 飞燕草 Delphinium — a tall spike of cobalt florets with white "bee" eyes, buds at the tip
flower('delphinium', """
..g..
..b..
..B..
.bBb.
..B..
.BwB.
.bBb.
BBwBb
.BBB.
bBwBB
.BBB.
BBwBb
.BBB.
..g..
""", {'g': '#6fa35a', 'b': '#8fa9f2', 'B': '#3f5fcf', 'w': '#f4f4f4'}, anchor=(2, 13))

# 石蒜 Lycoris radiata — red spider lily: curled petals, very long stamens arcing up, no leaves
flower('lycoris', """
L...........L
.L....L....L.
..L...L...L..
..L...L...L..
...L..L..L...
R...L.L.L...R
.RR.RRLRR.RR.
..RRDRRRDRR..
.R.DRDRDRD.R.
......D......
""", {'L': '#ff6f6f', 'R': '#d8283a', 'D': '#8e1424'}, anchor=(6, 9))

# 嘉兰百合 Gloriosa — flame lily: wavy petals swept upward, red with golden edges, stamens out sideways
flower('gloriosa', """
.R...R...R.
.RY..R..YR.
R.RY.R.YR.R
.R.RYRYR.R.
..RRYYYRR..
...RYYYR...
s---.Y.---s
.....g.....
""", {'R': '#e0342a', 'Y': '#f6c431', '-': '#b7b04a', 's': '#8a5a1e', 'g': '#4e8a3c'}, anchor=(5, 7),
    leaves=('tendril',))

# 亚百合 Asiatic lily — upward-facing six-petalled star, orange to gold tips, brown freckles, rust anthers
flower('asiatic', """
.....o.....
....oOo....
o...OsO...o
.oO.OOO.Oo.
.OOOsasOOO.
..OOaca00..
.OOOsasOOO.
.oO.OOO.Oo.
o...OsO...o
....oOo....
.....o.....
""", {'O': '#f28c28', 'o': '#f8b84e', '0': '#f28c28', 's': '#7a3b12', 'a': '#a5421a', 'c': '#b5cc5a'},
    anchor=(5, 7), leaves=('lance',))

# 帝王花 King protea — a big cup of pointed pink bracts around a silky, striated cone
flower('protea', """
.P...P...P.
.Pp.PpP.pP.
PpP.PWP.PpP
PpWWWWWWWpP
PpwWwWwWwpP
.PWWWWWWWP.
.PpWwWwWpP.
..PpPpPpP..
...PPPPP...
....ppp....
""", {'P': '#e98aa6', 'p': '#b8577a', 'W': '#f4ede2', 'w': '#ddd0c0'}, anchor=(5, 9), stem='#5d6b3a',
)

# 尤加利 silver-dollar eucalyptus — a sprig of round dusty-blue leaves cascading over the vase
flower('eucalyptus', """
ss.........
..ss..ee...
....seEEe..
..ee.s.ee..
.eEEe.s....
..ee..s....
.......s...
....ee.s...
...eEEes...
....ee.s...
........s..
.......eEe.
........e..
""", {'e': '#a9c2b6', 'E': '#7f9c90', 's': '#6b7f5a'}, anchor=(0, 0), stem='#6b7f5a')


def art_cells(name):
    f = FLOWERS[name]
    ax, ay = f['anchor']
    out = []
    for y, row in enumerate(f['rows']):
        for x, ch in enumerate(row):
            if ch != '.':
                out.append((x - ax, y - ay, f['pal'][ch]))
    return out


# ---------------------------------------------------------------- vase & arrangement
# A narrow-necked celadon bottle to the right of the mouse; neck mouth at y 15.
CEL, CEL_D, CEL_L = '#9cc5b0', '#6f9e88', '#cfe5d8'
MOUTH = 13  # stems enter the vase here


def vase():
    """A celadon bottle with a flared lip, a crackle band and a highlight."""
    rows = {13: (22, 26), 14: (23, 25), 15: (23, 25), 16: (21, 27), 17: (20, 28), 18: (19, 29), 19: (19, 29),
            20: (19, 29), 21: (19, 29), 22: (19, 29), 23: (19, 29), 24: (20, 28), 25: (21, 27)}
    cells = {}
    for y, (a, b) in rows.items():
        for x in range(a, b + 1):
            cells[(x, y)] = CEL
    for (x, y) in list(cells):
        if any(n not in cells for n in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1))):
            cells[(x, y)] = DARK
    for (x, y), c in list(cells.items()):
        if c == CEL and x >= 26:
            cells[(x, y)] = CEL_D
    for y in (18, 19, 20, 21):
        cells[(21, y)] = CEL_L
    for x in (22, 24, 26):  # crackle band
        cells[(x, 22)] = CEL_D
    for x in (23, 25):
        cells[(x, 23)] = CEL_D
    return [(x, y, 1, 1, c) for (x, y), c in cells.items()]


# where each stem enters the neck (bx) and where its head sits (hx, hy) — order = insertion order
ARRANGEMENT = [
    ('delphinium', 24, (21, 1)),    # the tall line first
    ('lycoris', 23, (12, -2)),      # sweeps out over the mouse's head
    ('gloriosa', 25, (29, -4)),     # flames up to the right
    ('asiatic', 25, (29, 4)),       # middle right
    ('protea', 24, (21, 8)),        # the big focal flower, low on the neck
    ('eucalyptus', 25, (25, 12)),   # a trailing sprig to finish, cascading over the vase
]
TOP = -14  # top of the visible window


def line(x0, y0, x1, y1):
    pts = []
    dx, dy = abs(x1 - x0), -abs(y1 - y0)
    sx, sy = (1 if x0 < x1 else -1), (1 if y0 < y1 else -1)
    err = dx + dy
    while True:
        pts.append((x0, y0))
        if x0 == x1 and y0 == y1: break
        e2 = 2 * err
        if e2 >= dy: err += dy; x0 += sx
        if e2 <= dx: err += dx; y0 += sy
    return pts


def leaf_cells(kind, stem_pts):
    """Small accents along the stem."""
    out = []
    if not stem_pts: return out
    mid = stem_pts[len(stem_pts) // 2]
    x, y = mid
    if kind == 'lance':      # narrow lily leaves
        out += [(x + 1, y, '#5f9a48'), (x + 2, y - 1, '#5f9a48'), (x - 1, y + 2, '#5f9a48'), (x - 2, y + 1, '#5f9a48')]
    elif kind == 'tendril':  # gloriosa leaf ending in a curl
        out += [(x + 1, y + 1, '#5f9a48'), (x + 2, y + 1, '#5f9a48'), (x + 3, y, '#5f9a48'), (x + 3, y - 1, '#7fb35e'),
                (x + 2, y - 1, '#7fb35e')]
    elif kind == 'leather':  # protea's dark leathery leaf
        out += [(x - 1, y, '#3f5a2e'), (x - 2, y, '#3f5a2e'), (x - 2, y - 1, '#3f5a2e'), (x - 3, y - 1, '#53703c')]
    return out


def stem_and_head(name, bx, hx, hy, lift=0):
    """All cells of one flower; lift raises it (for the held / lowering phases)."""
    f = FLOWERS[name]
    pts = line(bx, MOUTH, hx, hy)
    pts = [p for p in pts if p != (hx, hy)]
    cells = []
    cells += [(x, y, f['stem']) for x, y in pts]
    for k in f['leaves']:
        cells += leaf_cells(k, pts)
    cells += [(hx + x, hy + y, c) for x, y, c in art_cells(name)]
    return [(x, y - lift, c) for x, y, c in cells]


# ---------------------------------------------------------------- the mouse
A_SVG = open(os.path.join(A, 'mouse-idle-follow.svg')).read()
F = pixsvg.frames(A_SVG)
MDX = -6  # the mouse steps left to make room for the vase


def mouse(eyes='look', blush=False):
    body = [(x + MDX, y, w, h, c) for x, y, w, h, c in F['f0'] if not (c == DARK and (x, y) in
            ((8, 7), (16, 7), (7, 8), (17, 8)))]
    e = {'look': [(9, 7), (9, 8), (17, 7), (17, 8)],          # glancing right at the vase
         'happy': [(7, 8), (8, 7), (9, 8), (15, 8), (16, 7), (17, 8)],
         'up': [(9, 6), (9, 7), (17, 6), (17, 7)],                # watching the sky
         'wow': [(8, 7), (9, 7), (8, 8), (9, 8), (16, 7), (17, 7), (16, 8), (17, 8)]}[eyes]  # round eyes
    out = body + [(x + MDX, y, 1, 1, DARK) for x, y in e]
    if blush:
        out += [(x + MDX, 10, 2, 1, BLUSH) for x in (6, 17)]
    return out


SHADOW = [(1 + MDX, 25, 12, 1, '#00000033')]


def cells_to_rects(cells):
    return [(x, y, 1, 1, c) for x, y, c in cells]


def frames():
    out = []  # (rects, ms)
    placed = []
    base = lambda: vase() + [r for n in placed for r in cells_to_rects(stem_and_head(*n))]

    def add(rects, ms, k=1):
        for _ in range(k): out.append((rects, ms))

    add(SHADOW + mouse('look') + vase(), 900)
    for i, (name, bx, (hx, hy)) in enumerate(ARRANGEMENT):
        # it looks up, the flower drops in from above the window, lands in the neck with a bounce and a sparkle
        spark = [(bx - 3, MOUTH - 1, 1, 1, GOLD), (bx + 3, MOUTH - 1, 1, 1, GOLD), (bx - 2, MOUTH - 3, 1, 1, GOLD),
                 (bx + 2, MOUTH - 3, 1, 1, GOLD)]
        add(SHADOW + mouse('up') + base(), 450)
        fall = MOUTH - TOP + 2  # stem bottom just above the window
        for lift, ms in ((fall, 60), (fall * 3 // 5, 60), (fall * 3 // 10, 60), (fall // 10, 60), (0, 110), (-1, 90), (0, 160)):
            fx = spark if lift <= 0 else []
            add(SHADOW + mouse('up' if lift > 0 else 'wow') + base() + cells_to_rects(stem_and_head(name, bx, hx, hy, lift)) + fx, ms)
        placed.append((name, bx, hx, hy))
        add(SHADOW + mouse('look') + base(), 500)
        add(SHADOW + mouse('happy', blush=(i == len(ARRANGEMENT) - 1)) + base(), 700 if i < len(ARRANGEMENT) - 1 else 2600)
    return out


def build(fr):
    total = sum(ms for _, ms in fr)
    css, body, t = [], [], 0
    for i, (rects, ms) in enumerate(fr):
        a, b = 100 * t / total, 100 * (t + ms) / total
        t += ms
        if i == 0:
            css.append(f'@keyframes f{i}{{0%{{opacity:1}}{b:.3f}%{{opacity:0}}100%{{opacity:0}}}}')
        elif i == len(fr) - 1:
            css.append(f'@keyframes f{i}{{0%{{opacity:0}}{a:.3f}%{{opacity:1}}100%{{opacity:1}}}}')
        else:
            css.append(f'@keyframes f{i}{{0%{{opacity:0}}{a:.3f}%{{opacity:1}}{b:.3f}%{{opacity:0}}100%{{opacity:0}}}}')
        css.append(f'.f{i}{{animation:f{i} {total}ms step-end forwards}}')
        body.append(f'<g class="f{i}" opacity="0">{rects_svg(rects)}</g>')
    return HEAD + '<defs><style>' + ''.join(css) + '</style></defs>' + ''.join(body) + '</svg>', total


if __name__ == '__main__':
    fr = frames()
    svg, total = build(fr)
    open(os.path.join(OUT_DIR, 'mouse-idle-ikebana.svg'), 'w').write(svg)
    print('frames', len(fr), 'total ms', total)
    if '--sheet' in sys.argv:
        tmp = sys.argv[sys.argv.index('--sheet') + 1]
        prev = lambda r: [(x, y, w, h, c[:7]) for x, y, w, h, c in r]
        pixsvg.sheet([prev(r) for r, _ in fr], cols=8, scale=4).save(os.path.join(tmp, 'ikebana_frames.png'))
        pixsvg.sheet([prev(fr[-1][0])], cols=1, scale=12).save(os.path.join(tmp, 'ikebana_final.png'))
        fl = []
        for n in FLOWERS:
            fl.append([(x + 12, y + 0, 1, 1, c) for x, y, c in art_cells(n)])
        pixsvg.sheet(fl, cols=6, scale=10, box=(0, -14, 24, 20)).save(os.path.join(tmp, 'ikebana_flowers.png'))
