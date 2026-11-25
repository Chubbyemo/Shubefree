"""Tiny helpers for the Chubby Mouse pixel SVGs: parse frames, rasterize previews."""
import re
from PIL import Image

def frames(svg):
    """Return {frame_class: [(x,y,w,h,fill), ...]} plus the eyes group as 'eyes'."""
    out = {}
    # split on top-level frame groups <g class="fN">
    for m in re.finditer(r'<g class="(f\d+)">(.*?)</g></g>(?=<g class="f\d+">|<g id="eyes-js">|</g>)', svg, re.S):
        out[m.group(1)] = parse_rects(m.group(2) + '</g>')
    m = re.search(r'<g id="eyes-js">(.*?)</g></g></g>', svg, re.S)
    if m: out['eyes'] = parse_rects(m.group(1) + '</g>')
    return out

def parse_rects(chunk):
    rects = []
    for g in re.finditer(r'<g fill="(#[0-9a-fA-F]+)"[^>]*>(.*?)</g>', chunk, re.S):
        fill = g.group(1)
        for r in re.finditer(r'<rect x="(-?\d+)" y="(-?\d+)" width="(\d+)" height="(\d+)"', g.group(2)):
            x, y, w, h = map(int, r.groups())
            rects.append((x, y, w, h, fill))
    return rects

def raster(rects, box=(-12, -24, 52, 52), scale=8, bg=(255, 255, 255)):
    bx, by, bw, bh = box
    im = Image.new('RGB', (bw * scale, bh * scale), bg)
    px = im.load()
    for x, y, w, h, fill in rects:
        c = tuple(int(fill[i:i + 2], 16) for i in (1, 3, 5))
        for yy in range(y, y + h):
            for xx in range(x, x + w):
                X, Y = xx - bx, yy - by
                if 0 <= X < bw and 0 <= Y < bh:
                    for sy in range(scale):
                        for sx in range(scale):
                            px[X * scale + sx, Y * scale + sy] = c
    return im

def sheet(list_of_rects, cols=6, **kw):
    ims = [raster(r, **kw) for r in list_of_rects]
    w, h = ims[0].size
    rows = (len(ims) + cols - 1) // cols
    out = Image.new('RGB', (w * cols, h * rows), (200, 200, 200))
    for i, im in enumerate(ims):
        out.paste(im, ((i % cols) * w, (i // cols) * h))
    return out
