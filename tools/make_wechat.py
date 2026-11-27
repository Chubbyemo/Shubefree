"""WeChat sticker album kit: 24 GIFs + cover, chat icon, banner, tipping images.

usage: python3 make_wechat.py <assets dir> <out dir>
"""
import os, sys, random
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from make_gif import frame_grids, render, to_gif

STICKERS = [  # (svg, meaning word)
    ('mouse-happy', '开心'), ('mouse-idle-cheese', '吃奶酪'), ('mouse-idle-beer', '干杯'),
    ('mouse-react-double', '嗨起来'), ('mouse-idle-swing', '荡秋千'), ('mouse-idle-ikebana', '插花'),
    ('mouse-trick-heist', '偷奶酪'), ('mouse-trick-crab', '横着走'), ('mouse-idle-pacifier', '叼奶嘴'),
    ('mouse-idle-super', '变身'), ('mouse-notification', '震惊'), ('mouse-react-left', '瞪你'),
    ('mouse-react-annoyed', '抗议'), ('mouse-react-double-angel', '升天'), ('mouse-react-drag', '被拎走'),
    ('mouse-error', '崩溃'), ('mouse-thinking', '思考'), ('mouse-working-typing', '打工'),
    ('mouse-working-building', '搬砖'), ('mouse-working-juggling', '忙不过来'), ('mouse-working-sweeping', '扫地'),
    ('mouse-yawning', '困'), ('mouse-dozing', '摸鱼'), ('mouse-sleeping', '晚安'),
]

SKY = ['#d8eefa', '#e2f2f8', '#ebf5f2', '#f3f6e8', '#fbf4dc']
GROUND, GROUND_D, GROUND_L = '#f0d9a0', '#d9b86c', '#f8e8bc'
CHEESE, HOLE, OUT = '#f8d088', '#f2a93b', '#1b1b1d'
HEART, HEART_L = '#f0647a', '#ffb3c0'
SPARK = ['#f5c518', '#3aa0f0', '#f0647a', '#8fd16a', '#b07ce8']


def rgb(h):
    h = h.lstrip('#'); return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def frame(name, assets, i=0):
    seq = frame_grids(os.path.join(assets, name + '.svg'))
    return seq[i if i >= 0 else len(seq) + i][0]


class Canvas:
    def __init__(self, w, h, bg=None):
        self.w, self.h, self.px = w, h, {}
        if bg:
            for y in range(h):
                for x in range(w):
                    self.px[(x, y)] = bg(x, y)

    def put(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h:
            self.px[(x, y)] = rgb(c) if isinstance(c, str) else c

    def sprite(self, grid, ox, oy, flip=False):
        """Paste a pixel dict so that its (0,0) lands on (ox, oy)."""
        if flip:
            xs = [x for x, y in grid]; mid = min(xs) + max(xs)
        for (x, y), c in grid.items():
            self.put(ox + ((mid - x) if flip else x), oy + y, c)

    def art(self, rows, ox, oy, pal):
        for j, row in enumerate(rows):
            for i, ch in enumerate(row):
                if ch in pal: self.put(ox + i, oy + j, pal[ch])

    def image(self, scale):
        im = Image.new('RGBA', (self.w * scale, self.h * scale), (0, 0, 0, 0))
        tile = {}
        for (x, y), c in self.px.items():
            t = tile.get(c) or tile.setdefault(c, Image.new('RGBA', (scale, scale), c + (255,)))
            im.paste(t, (x * scale, y * scale))
        return im


HEART_ART = [' oo oo ', 'oLHoHHo', 'oHHHHHo', ' oHHHo ', '  oHo  ', '   o   ']
WEDGE = ['    ooo', '  ooCCo', 'ooCCCCo', 'oCChCCo', 'oCCCChO', 'ooooooo']
CLOUD = ['   www   ', ' wwwwwww ', 'wwwwwwwww']
STAR = [' s ', 'sSs', ' s ']


def heart(cv, x, y): cv.art(HEART_ART, x, y, {'o': OUT, 'H': HEART, 'L': HEART_L})
def wedge(cv, x, y): cv.art(WEDGE, x, y, {'o': OUT, 'O': OUT, 'C': CHEESE, 'h': HOLE})
def cloud(cv, x, y): cv.art(CLOUD, x, y, {'w': '#ffffff'})
def star(cv, x, y, c): cv.art(STAR, x, y, {'s': c, 'S': '#ffffff'})


def sky(h, ground):
    bands = SKY
    def f(x, y):
        if y >= ground:
            if y == ground: return rgb(GROUND_D)
            if (x * 7 + y * 13) % 23 == 0: return rgb(GROUND_L)
            return rgb(GROUND)
        return rgb(bands[min(len(bands) - 1, y * len(bands) // ground)])
    return f


def unshadow(grid):
    """Shadows were flattened against light gray; re-flatten them onto the scene ground."""
    out = {}
    for p, c in grid.items():
        if c[0] == c[1] == c[2] and 180 <= c[0] < 237:
            out[p] = rgb(GROUND_D)
        else:
            out[p] = c
    return out


def banner(assets):
    W, H, G = 150, 80, 66
    cv = Canvas(W, H, sky(H, G))
    for x, y in [(8, 6), (52, 3), (104, 9), (136, 4)]:
        cloud(cv, x, y)
    random.seed(7)
    for _ in range(14):
        star(cv, random.randrange(2, W - 3), random.randrange(2, 30), random.choice(SPARK))
    # mouse coords: the ground line sits at y=25 in the SVGs
    cv.sprite(unshadow(frame('mouse-idle-swing', assets, 3)), 8 + 6, G - 25)
    cv.sprite(unshadow(frame('mouse-idle-ikebana', assets, -1)), 52 + 8, G - 25)
    cv.sprite(unshadow(frame('mouse-happy', assets, 4)), 104, G - 25)
    for x in (42, 94, 138):
        wedge(cv, x, G - 6)
    heart(cv, 92, 18); heart(cv, 28, 24)
    return cv.image(5)


def thanks(assets):
    W = H = 75; G = 62
    cv = Canvas(W, H, sky(H, G))
    for x, y in [(4, 5), (56, 9)]:
        cloud(cv, x, y)
    random.seed(3)
    for _ in range(10):
        star(cv, random.randrange(2, W - 3), random.randrange(2, 34), random.choice(SPARK))
    cv.sprite(unshadow(frame('mouse-happy', assets, 2)), 26, G - 25)
    for x, y in [(8, 26), (60, 30), (14, 44), (58, 46)]:
        heart(cv, x, y)
    wedge(cv, 4, G - 6); wedge(cv, 64, G - 6)
    return cv.image(10)


def guide(assets):
    W, H, G = 94, 70, 58  # 8x, cropped to 750x560
    cv = Canvas(W, H, sky(H, G))
    for x, y in [(5, 5), (70, 3)]:
        cloud(cv, x, y)
    random.seed(11)
    for _ in range(8):
        star(cv, random.randrange(2, W - 3), random.randrange(2, 26), random.choice(SPARK))
    cv.sprite(unshadow(frame('mouse-idle-cheese', assets, 0)), 33, G - 25)
    for x, y in [(8, G - 6), (17, G - 6), (12, G - 12), (74, G - 6)]:
        wedge(cv, x, y)
    heart(cv, 66, 18); heart(cv, 18, 22)
    return cv.image(8).crop((0, 0, 750, 560))


def bbox(g):
    xs = [x for x, y in g]; ys = [y for x, y in g]
    return min(xs), min(ys), max(xs), max(ys)


def cover(assets):
    g = frame('mouse-idle-cheese', assets, 0)
    x0, y0, x1, y1 = bbox(g)
    cv = Canvas(30, 30)
    cv.sprite(g, (30 - (x1 - x0 + 1)) // 2 - x0, (30 - (y1 - y0 + 1)) // 2 - y0)
    return cv.image(8)


def icon(assets):
    g = frame('mouse-idle-cheese', assets, 0)
    x0, y0, x1, y1 = bbox(g)
    row = [x for x, y in g if y == y0 + 3]
    lo, hi = min(row), max(row)
    head = {(x, y): c for (x, y), c in g.items() if y < y0 + 16 and lo <= x <= hi and c != rgb(CHEESE) and c != rgb(HOLE)}
    # keep only the piece connected to the face (drops stray tail bits)
    start = max(head, key=lambda p: -abs(p[0] - (lo + hi) / 2) - abs(p[1] - y0 - 8))
    seen, todo = {start}, [start]
    while todo:
        x, y = todo.pop()
        for q in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if q in head and q not in seen:
                seen.add(q); todo.append(q)
    head = {p: head[p] for p in seen}
    hx0, hy0, hx1, hy1 = bbox(head)
    cv = Canvas(25, 25)
    cv.sprite(head, (25 - (hx1 - hx0 + 1)) // 2 - hx0, (25 - (hy1 - hy0 + 1)) // 2 - hy0)
    return cv.image(2)


def main(assets, out):
    gd = os.path.join(out, '表情')
    os.makedirs(gd, exist_ok=True)
    lines = []
    for i, (name, word) in enumerate(STICKERS, 1):
        dst = os.path.join(gd, '%02d-%s.gif' % (i, word))
        fr = render(os.path.join(assets, name + '.svg'), 240)
        to_gif(fr, dst)
        lines.append('%02d %-6s %4dKB %5.1fs %d帧' % (i, word, os.path.getsize(dst) // 1024,
                                                     sum(m for _, m in fr) / 1000, len(fr)))
    cover(assets).save(os.path.join(out, '封面-240x240.png'))
    icon(assets).save(os.path.join(out, '聊天页图标-50x50.png'))
    banner(assets).convert('RGB').save(os.path.join(out, '横幅-750x400.png'), optimize=True)
    guide(assets).convert('RGB').save(os.path.join(out, '赞赏引导图-750x560.png'), optimize=True)
    thanks(assets).convert('RGB').save(os.path.join(out, '赞赏致谢图-750x750.png'), optimize=True)
    print('\n'.join(lines))
    for f in sorted(os.listdir(out)):
        p = os.path.join(out, f)
        if os.path.isfile(p):
            print('%-24s %s %dKB' % (f, Image.open(p).size, os.path.getsize(p) // 1024))


if __name__ == '__main__':
    main(*sys.argv[1:3])
