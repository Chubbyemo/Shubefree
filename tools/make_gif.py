"""Render the pixel SVG animations to GIFs (no SVG renderer needed).

usage: python3 make_gif.py <assets dir> <out dir> [--size 240] [name.svg ...]
"""
import re, sys, os
from PIL import Image

BG = (0xed, 0xed, 0xed)  # semi-transparent bits are flattened against a light chat background


def hexrgba(c, op=1.0):
    c = c.lstrip('#')
    if len(c) in (3, 4): c = ''.join(ch * 2 for ch in c)
    r, g, b = (int(c[i:i + 2], 16) for i in (0, 2, 4))
    a = int(c[6:8], 16) / 255 if len(c) == 8 else 1.0
    return r, g, b, a * op


def timeline(svg):
    """[(frame_class, ms)] in play order, plus whether it loops."""
    segs, total, loop = [], 1000, True
    for m in re.finditer(r'@keyframes (f\d+)\{(.*?)\}\}\.\1\{animation:\1 (\d+)ms step-end (\w+)', svg):
        name, body, total, mode = m.group(1), m.group(2), int(m.group(3)), m.group(4)
        loop = mode == 'infinite'
        stops = [(float(p), float(o)) for p, o in re.findall(r'([\d.]+)%\{opacity:([\d.]+)', body)]
        for i, (p, o) in enumerate(stops):
            if o > 0:
                end = stops[i + 1][0] if i + 1 < len(stops) else 100.0
                if end > p or (p == 100 and not loop):
                    segs.append((p, end, name))
    segs.sort()
    out = [(n, max(20, round((b - a) / 100 * total))) for a, b, n in segs if b > a]
    if not loop and segs:
        out.append((segs[-1][2], 2500))  # hold the final pose before looping
    return out, loop


TOK = re.compile(r'<g([^>]*)>|</g>|<rect([^>]*)/>|<use([^>]*)/>')


def attrs_of(t):
    return dict(re.findall(r'([\w-]+)="([^"]*)"', t or ''))


def symbols(svg):
    """Reusable <g id=..> pieces inside <defs>, as raw markup."""
    defs = svg.split('<defs>', 1)[-1].split('</defs>', 1)[0]
    out = {}
    for m in re.finditer(r'<g id="([^"]+)">', defs):
        depth, i = 0, m.start()
        for t in re.finditer(r'<g[ >]|</g>', defs[i:]):
            depth += 1 if t.group(0) != '</g>' else -1
            if depth == 0:
                out[m.group(1)] = defs[m.end():i + t.start()]
                break
    clip = re.search(r'<clipPath id="ground"><rect x="(-?\d+)" y="(-?\d+)" width="(\d+)" height="(\d+)"', defs)
    return out, (tuple(map(int, clip.groups())) if clip else None)


def draw(svg):
    """{frame_class or None: [(x,y,w,h,rgba)]} in paint order."""
    syms, ground = symbols(svg)
    body = svg.split('</defs>', 1)[-1]
    layers = {}

    def walk(markup, frame, fill, op, dx, dy, clip):
        stack = [(frame, fill, op, clip)]
        for t in TOK.finditer(markup):
            if t.group(0) == '</g>':
                if len(stack) > 1: stack.pop()
                continue
            fr, fl, o, cl = stack[-1]
            if t.group(1) is not None:
                a = attrs_of(t.group(1))
                cls = a.get('class', '')
                isframe = bool(re.fullmatch(r'f\d+', cls))
                o2 = o * float(a.get('fill-opacity', 1))
                if not isframe: o2 *= float(a.get('opacity', 1))
                stack.append((cls if isframe else fr, a.get('fill', fl), o2,
                              ground if 'url(#ground)' in a.get('clip-path', '') else cl))
            elif t.group(2) is not None:
                a = attrs_of(t.group(2))
                f = a.get('fill', fl)
                if not f or not f.startswith('#'): continue
                x, y, w, h = int(a['x']) + dx, int(a['y']) + dy, int(a['width']), int(a['height'])
                if cl:
                    cx, cy, cw, ch = cl
                    x1, y1 = min(x + w, cx + cw), min(y + h, cy + ch)
                    x, y = max(x, cx), max(y, cy)
                    w, h = x1 - x, y1 - y
                    if w <= 0 or h <= 0: continue
                layers.setdefault(fr, []).append((x, y, w, h, hexrgba(f, o)))
            else:
                a = attrs_of(t.group(3))
                ref = (a.get('href') or a.get('xlink:href', '')).lstrip('#')
                m = re.search(r'translate\((-?[\d.]+)[ ,]+(-?[\d.]+)', a.get('transform', ''))
                tx, ty = (int(float(m.group(1))), int(float(m.group(2)))) if m else (0, 0)
                if ref in syms:
                    walk(syms[ref], fr, fl, o, dx + tx, dy + ty, cl)

    walk(body, None, None, 1.0, 0, 0, None)
    return layers


def paint(rects):
    px = {}
    for x, y, w, h, (r, g, b, a) in rects:
        for yy in range(y, y + h):
            for xx in range(x, x + w):
                if a >= 0.99:
                    px[(xx, yy)] = (r, g, b)
                else:
                    br, bg_, bb = px.get((xx, yy), BG)
                    px[(xx, yy)] = (round(r * a + br * (1 - a)), round(g * a + bg_ * (1 - a)), round(b * a + bb * (1 - a)))
    return px


def frame_grids(path):
    """[(pixel dict, ms)] in play order, clipped to the viewBox."""
    svg = open(path, encoding='utf8').read()
    tl, _ = timeline(svg)
    layers = draw(svg)
    static = layers.get(None, [])
    vb = [int(float(v)) for v in re.search(r'viewBox="([^"]+)"', svg).group(1).split()]
    inside = lambda g: {p: c for p, c in g.items() if vb[0] <= p[0] < vb[0] + vb[2] and vb[1] <= p[1] < vb[1] + vb[3]}
    grids = {n: inside(paint(static + layers.get(n, []))) for n in {n for n, _ in tl}}
    if not tl:
        tl, grids = [('s', 1000)], {'s': paint(static)}
    return [(grids[n], ms) for n, ms in tl]


def render(path, size=240):
    seq = frame_grids(path)
    grids = {i: g for i, (g, _) in enumerate(seq)}
    tl = [(i, ms) for i, (_, ms) in enumerate(seq)]
    xs = [x for g in grids.values() for x, y in g]
    ys = [y for g in grids.values() for x, y in g]
    w, h = max(xs) - min(xs) + 1, max(ys) - min(ys) + 1
    side = next(d for d in (30, 40, 48, 60, 80, 120, 240) if d >= max(w, h) + 2)
    k = size // side
    x0 = min(xs) - (side - w) // 2
    y0 = min(ys) - (side - h) // 2
    frames = []
    for n, ms in tl:
        im = Image.new('RGBA', (side, side), (0, 0, 0, 0))
        p = im.load()
        for (x, y), c in grids[n].items():
            if 0 <= x - x0 < side and 0 <= y - y0 < side:
                p[x - x0, y - y0] = c + (255,)
        frames.append((im.resize((side * k, side * k), Image.NEAREST), ms))
    # merge consecutive identical frames
    merged = []
    for im, ms in frames:
        if merged and merged[-1][0].tobytes() == im.tobytes():
            merged[-1][1] += ms
        else:
            merged.append([im, ms])
    return merged


def to_gif(frames, out):
    """Transparent, looping GIF; index 0 is transparent, exact colours (pixel art has few)."""
    colors = {}
    for im, _ in frames:
        for c, a in ((px[:3], px[3]) for px in im.get_flattened_data()):
            if a and c not in colors:
                colors[c] = len(colors) + 1
    if len(colors) > 255:
        raise SystemExit('too many colours in ' + out)
    pal = [0, 0, 0] + [v for c in colors for v in c]
    pal += [0] * (768 - len(pal))
    qs = []
    for im, _ in frames:
        q = Image.new('P', im.size)
        q.putpalette(pal)
        q.putdata([colors[px[:3]] if px[3] else 0 for px in im.get_flattened_data()])
        qs.append(q)
    qs[0].save(out, save_all=True, append_images=qs[1:], duration=[ms for _, ms in frames], loop=0,
               transparency=0, disposal=2, optimize=False)


def main(argv):
    assets, out = argv[0], argv[1]
    size, names = 240, []
    rest = argv[2:]
    while rest:
        a = rest.pop(0)
        if a == '--size': size = int(rest.pop(0))
        else: names.append(a)
    os.makedirs(out, exist_ok=True)
    for n in names or sorted(f for f in os.listdir(assets) if f.endswith('.svg')):
        fr = render(os.path.join(assets, n), size)
        dst = os.path.join(out, n[:-4] + '.gif')
        to_gif(fr, dst)
        print('%-32s %3d frames %6.1fs %4dKB' % (os.path.basename(dst), len(fr), sum(m for _, m in fr) / 1000, os.path.getsize(dst) // 1024))


if __name__ == '__main__':
    main(sys.argv[1:])
