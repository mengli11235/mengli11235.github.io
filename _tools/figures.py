"""Figures for meng.science, drawn in one visual language.

Ink lines for raw signals, teal for learned structure, amber for the event of
interest and what the model finds from it. Writes Jekyll includes.

Usage (from the repository root):
    python3 _tools/figures.py _includes

Colors and strokes come from the fg-* classes in assets/css/main.css,
so the SVGs carry no colors of their own. Seeds are fixed, so the output
is identical on every run.
"""
import math, random, os, sys

OUT = sys.argv[1] if len(sys.argv) > 1 else "."


def f(v):
    return f"{v:.1f}"


def P(pts):
    return "M" + " L".join(f"{f(x)} {f(y)}" for x, y in pts)


def ricker(d):
    return (1 - d * d) * math.exp(-d * d / 2)


def make_trace(rng, x0, x1, cy, amp, n, events=()):
    f1, f2, f3 = rng.uniform(.9, 1.6), rng.uniform(2.2, 3.4), rng.uniform(5, 8)
    p1, p2, p3 = [rng.uniform(0, 6.283) for _ in range(3)]
    pts = []
    for s in range(n):
        t = s / (n - 1)
        x = x0 + (x1 - x0) * t
        y = (math.sin(t * 6.283 * f1 + p1) + .55 * math.sin(t * 6.283 * f2 + p2) + .25 * math.sin(t * 6.283 * f3 + p3)) * amp * .62
        y += rng.uniform(-.2, .2) * amp * .55
        for tc, h, w in events:
            y -= h * ricker((t - tc) / w)
        pts.append((t, x, cy + y))
    return pts


def fade_defs(uid, x_end, width_total):
    stop = f"{x_end / width_total:.3f}"
    return (f'<defs><linearGradient id="fade-{uid}" x1="0" y1="0" x2="1" y2="0">'
            f'<stop offset="0" stop-color="#fff"/><stop offset="{stop}" stop-color="#fff"/>'
            f'<stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>'
            f'<mask id="mask-{uid}" maskUnits="userSpaceOnUse"><rect x="0" y="0" width="{width_total}" height="1000" fill="url(#fade-{uid})"/></mask></defs>')


# --------------------------------------------------------------------------
# Hero: signal to structure
# --------------------------------------------------------------------------
def hero():
    rng = random.Random(20261008)
    W, H = 600, 440
    x0, x1, n = 20, 300, 230
    ta, tb = .60, .70
    events = {1: (.648, 22, .011), 2: (.653, -15, .012), 4: (.645, 26, .010), 5: (.656, 13, .012)}
    bx0, bx1 = x0 + (x1 - x0) * ta - 3, x0 + (x1 - x0) * tb + 3
    bxm = (bx0 + bx1) / 2
    o = [f'<svg class="fig-signal" viewBox="0 0 {W} {H}" role="img" aria-labelledby="fig-signal-title">',
         '<title id="fig-signal-title">Seven channels of neural recordings with an amber event window. An arc maps the event to an amber cluster in the curved latent grid that a model learns.</title>',
         fade_defs("hero", x1 * .80, x1 + 4)]
    o.append(f'<rect class="fg-band" x="{f(bx0)}" y="34" width="{f(bx1 - bx0)}" height="362" rx="3"/>')
    traces, overlays = [], []
    for i in range(7):
        cy = 64 + i * 50
        amp = rng.uniform(10.5, 15)
        ev = [events[i]] if i in events else []
        pts = make_trace(rng, x0, x1, cy, amp, n, ev)
        traces.append(f'<path class="fg-trace" style="--i:{i}" d="{P([(x, y) for _, x, y in pts])}"/>')
        if ev:
            seg = [(x, y) for t, x, y in pts if ta <= t <= tb]
            overlays.append(f'<path class="fg-event" d="{P(seg)}"/>')
    o.append('<g mask="url(#mask-hero)">' + "".join(traces) + '</g>')
    o.append('<g>' + "".join(overlays) + '</g>')

    def warp(u, v):
        x = 352 + 226 * u + 16 * math.sin(math.pi * v) * (1 - u) - 10 * (1 - v) * u
        y = 58 + 322 * v + 24 * math.sin(math.pi * u) * (0.55 + 0.45 * v) - 10 * u * (1 - v)
        return x, y
    grid = []
    for k in range(8):
        a = k / 7
        grid.append(f'<path d="{P([warp(a, t / 40) for t in range(41)])}"/>')
        grid.append(f'<path d="{P([warp(t / 40, a) for t in range(41)])}"/>')
    o.append('<g class="latent-grid fg-grid">' + "".join(grid) + '</g>')
    pts_t = []
    for _ in range(62):
        u, v = rng.random(), rng.random()
        x, y = warp(u, v)
        pts_t.append(f'<circle class="fg-pt" cx="{f(x + rng.uniform(-2, 2))}" cy="{f(y + rng.uniform(-2, 2))}" r="2.6"/>')
    cu, cv = .64, .36
    pts_a = []
    for _ in range(11):
        u = min(1, max(0, rng.gauss(cu, .06)))
        v = min(1, max(0, rng.gauss(cv, .07)))
        x, y = warp(u, v)
        pts_a.append(f'<circle class="fg-pt-a" cx="{f(x)}" cy="{f(y)}" r="3.1"/>')
    cxa, cya = warp(cu, cv)
    o.append('<g class="latent-pts">' + "".join(pts_t) + "".join(pts_a)
             + f'<ellipse class="fg-chart-a" cx="{f(cxa)}" cy="{f(cya)}" rx="36" ry="27" transform="rotate(-16 {f(cxa)} {f(cya)})"/></g>')
    ey = cya - 27
    o.append(f'<path class="fg-link" d="M{f(bxm)} 32 C{f(bxm)} 2, {f(cxa)} 2, {f(cxa)} {f(ey - 2)}"/>')
    o.append(f'<circle class="fg-link-start" cx="{f(bxm)}" cy="32" r="2.6"/>')
    o.append('</svg>')
    return "\n".join(o) + "\n"


# --------------------------------------------------------------------------
# Small glyphs for the home page (120 x 72)
# --------------------------------------------------------------------------
def glyph_algorithms():
    rng = random.Random(11)

    def w(u, v):
        return 6 + 108 * u + 6 * math.sin(math.pi * v) * (1 - u), 7 + 58 * v + 7 * math.sin(math.pi * u) * (.5 + .5 * v) - 3 * u * (1 - v)
    o = ['<svg class="glyph" viewBox="0 0 120 72" aria-hidden="true">', '<g class="fg-grid">']
    for k in range(6):
        a = k / 5
        o.append(f'<path d="{P([w(a, t / 16) for t in range(17)])}"/>')
        o.append(f'<path d="{P([w(t / 16, a) for t in range(17)])}"/>')
    o.append('</g>')
    c1, c2 = w(.34, .52), w(.74, .4)
    o.append(f'<ellipse class="fg-chart" cx="{f(c1[0])}" cy="{f(c1[1])}" rx="25" ry="17" transform="rotate(-10 {f(c1[0])} {f(c1[1])})"/>')
    o.append(f'<ellipse class="fg-chart-a" cx="{f(c2[0])}" cy="{f(c2[1])}" rx="12" ry="9" transform="rotate(8 {f(c2[0])} {f(c2[1])})"/>')
    for _ in range(9):
        x, y = w(rng.uniform(.12, .58), rng.uniform(.2, .85))
        o.append(f'<circle class="fg-pt" cx="{f(x)}" cy="{f(y)}" r="1.9"/>')
    for du, dv in [(-.03, -.04), (.03, .02), (-.01, .07), (.04, -.06)]:
        x, y = w(.74 + du, .4 + dv)
        o.append(f'<circle class="fg-pt-a" cx="{f(x)}" cy="{f(y)}" r="2.1"/>')
    o.append('</svg>')
    return "\n".join(o) + "\n"


def glyph_bci():
    rng = random.Random(7)
    o = ['<svg class="glyph" viewBox="0 0 120 72" aria-hidden="true">']
    x0, x1, ta, tb = 4, 62, .56, .76
    bx0, bx1 = x0 + (x1 - x0) * ta, x0 + (x1 - x0) * tb
    o.append(f'<rect class="fg-band" x="{f(bx0)}" y="4" width="{f(bx1 - bx0)}" height="64" rx="2"/>')
    ev = {0: (.66, 7, .035), 2: (.67, -6, .035)}
    tr, ovl = [], []
    for i, cy in enumerate([17, 36, 55]):
        pts = make_trace(rng, x0, x1, cy, 3.4, 80, [ev[i]] if i in ev else [])
        tr.append(f'<path class="fg-trace" d="{P([(x, y) for _, x, y in pts])}"/>')
        if i in ev:
            ovl.append(f'<path class="fg-event" d="{P([(x, y) for t, x, y in pts if ta <= t <= tb])}"/>')
    o += tr + ovl
    for (y, wd, amber) in [(19, 38, False), (31.5, 28, True), (44, 33, False)]:
        cls = "fg-word fg-word-a" if amber else "fg-word"
        o.append(f'<rect class="{cls}" x="76" y="{f(y)}" width="{wd}" height="9" rx="4.5"/>')
    o.append('</svg>')
    return "\n".join(o) + "\n"


def glyph_embryo():
    rng = random.Random(5)
    cx, cy = 30, 36
    o = ['<svg class="glyph" viewBox="0 0 120 72" aria-hidden="true">',
         f'<circle class="fg-zona" cx="{cx}" cy="{cy}" r="24"/>']
    o.append(f'<circle class="fg-cell-back" cx="{cx}" cy="{cy}" r="6"/>')
    for a in (45, 135, 225, 315):
        x, y = cx + 13 * math.cos(math.radians(a)), cy + 13 * math.sin(math.radians(a))
        o.append(f'<circle class="fg-cell-back" cx="{f(x)}" cy="{f(y)}" r="6.5"/>')
    front = [(a, cx + 11.5 * math.cos(math.radians(a)), cy + 11.5 * math.sin(math.radians(a))) for a in (270, 0, 90, 180)]
    amber = {270, 0}
    for a, x, y in front:
        o.append(f'<circle class="fg-cell{" fg-cell-a" if a in amber else ""}" cx="{f(x)}" cy="{f(y)}" r="8.1"/>')
    for a, x, y in front:
        o.append(f'<circle class="{"fg-nuc-a" if a in amber else "fg-nuc"}" cx="{f(x)}" cy="{f(y)}" r="1.7"/>')
    cw, ch, g = 7, 8.5, 2
    xs, ys = 66, 17.5
    for r in range(4):
        for c in range(6):
            mod = (r in (0, 1) and c in (3, 4))
            val = rng.uniform(.75, 1) if mod else rng.uniform(.1, .5)
            cls = "fg-heat-a" if mod else "fg-heat"
            o.append(f'<rect class="{cls}" x="{f(xs + c * (cw + g))}" y="{f(ys + r * (ch + g))}" width="{cw}" height="{ch}" rx="1" fill-opacity="{val:.2f}"/>')
    o.append('</svg>')
    return "\n".join(o) + "\n"


# --------------------------------------------------------------------------
# Plates for the research page (360 x 240)
# --------------------------------------------------------------------------
def plate_algorithms():
    rng = random.Random(23)

    def w(u, v):
        x = 22 + 316 * u + 18 * math.sin(math.pi * v) * (1 - u) - 6 * u * v
        y = 26 + 186 * v + 26 * math.sin(math.pi * u) * (.5 + .5 * v) - 9 * u * (1 - v)
        return x, y
    o = ['<svg class="plate" viewBox="0 0 360 240" aria-hidden="true">', '<g class="fg-grid">']
    for k in range(10):
        a = k / 9
        o.append(f'<path d="{P([w(a, t / 40) for t in range(41)])}"/>')
        o.append(f'<path d="{P([w(t / 40, a) for t in range(41)])}"/>')
    o.append('</g>')
    charts = [((.30, .52), 74, 54, -12, "fg-chart"), ((.60, .38), 50, 36, 8, "fg-chart"), ((.80, .68), 26, 20, -6, "fg-chart-a")]
    for (u, v), rx, ry, rot, cls in charts:
        x, y = w(u, v)
        o.append(f'<ellipse class="{cls}" cx="{f(x)}" cy="{f(y)}" rx="{rx}" ry="{ry}" transform="rotate({rot} {f(x)} {f(y)})"/>')
    for _ in range(26):
        x, y = w(rng.uniform(.1, .5), rng.uniform(.25, .82))
        o.append(f'<circle class="fg-pt" cx="{f(x)}" cy="{f(y)}" r="2.5"/>')
    for _ in range(12):
        x, y = w(rng.uniform(.5, .7), rng.uniform(.22, .55))
        o.append(f'<circle class="fg-pt" cx="{f(x)}" cy="{f(y)}" r="2.5"/>')
    for _ in range(7):
        x, y = w(rng.gauss(.8, .03), rng.gauss(.68, .045))
        o.append(f'<circle class="fg-pt-a" cx="{f(x)}" cy="{f(y)}" r="2.8"/>')
    o.append('</svg>')
    return "\n".join(o) + "\n"


def plate_bci():
    rng = random.Random(31)
    o = ['<svg class="plate" viewBox="0 0 360 240" aria-hidden="true">', fade_defs("bci", 172, 204)]
    x0, x1, ta, tb = 10, 200, .60, .74
    bx0, bx1 = x0 + (x1 - x0) * ta - 2, x0 + (x1 - x0) * tb + 2
    bxm = (bx0 + bx1) / 2
    o.append(f'<rect class="fg-band" x="{f(bx0)}" y="22" width="{f(bx1 - bx0)}" height="208" rx="3"/>')
    ev = {1: (.668, 15, .012), 2: (.672, -11, .013), 3: (.664, 17, .011), 5: (.675, 10, .013)}
    tr, ovl = [], []
    for i in range(6):
        cy = 40 + i * 34
        pts = make_trace(rng, x0, x1, cy, 8, 170, [ev[i]] if i in ev else [])
        tr.append(f'<path class="fg-trace" d="{P([(x, y) for _, x, y in pts])}"/>')
        if i in ev:
            ovl.append(f'<path class="fg-event" d="{P([(x, y) for t, x, y in pts if ta <= t <= tb])}"/>')
    o.append('<g mask="url(#mask-bci)">' + "".join(tr) + '</g>')
    o += ovl
    bx = [222 + k * 20 for k in range(6)]
    by, bs = 96, 14
    w1 = (226, 54)
    w2 = (290, 50)
    wy, wh = 150, 18
    for k, x in enumerate(bx):
        tx, ty = x + bs / 2, by + bs
        wx = w1[0] + w1[1] / 2 if k < 3 else w2[0] + w2[1] / 2
        o.append(f'<path class="fg-wire" d="M{f(tx)} {f(ty)} C{f(tx)} {f(ty + 18)}, {f(wx)} {f(wy - 18)}, {f(wx)} {f(wy)}"/>')
    for x in bx:
        o.append(f'<rect class="fg-token" x="{x}" y="{by}" width="{bs}" height="{bs}" rx="3"/>')
    o.append(f'<rect class="fg-word" x="{w1[0]}" y="{wy}" width="{w1[1]}" height="{wh}" rx="9"/>')
    o.append(f'<rect class="fg-word fg-word-a" x="{w2[0]}" y="{wy}" width="{w2[1]}" height="{wh}" rx="9"/>')
    o.append(f'<path class="fg-link" d="M{f(bxm)} 20 C{f(bxm)} 0, {f(bx[0] + 7)} 2, {f(bx[0] + 7)} {by - 4}"/>')
    o.append(f'<circle class="fg-link-start" cx="{f(bxm)}" cy="20" r="2.4"/>')
    o.append('</svg>')
    return "\n".join(o) + "\n"


def plate_embryo():
    rng = random.Random(41)
    o = ['<svg class="plate" viewBox="0 0 360 240" aria-hidden="true">']
    cx, cy = 96, 120
    d, r = 38, 26.8
    o.append(f'<circle class="fg-zona" cx="{cx}" cy="{cy}" r="76"/>')
    o.append(f'<circle class="fg-cell-back" cx="{cx}" cy="{cy}" r="20"/>')
    for a in (45, 135, 225, 315):
        x, y = cx + 42 * math.cos(math.radians(a)), cy + 42 * math.sin(math.radians(a))
        o.append(f'<circle class="fg-cell-back" cx="{f(x)}" cy="{f(y)}" r="21"/>')
    front = [(a, cx + d * math.cos(math.radians(a)), cy + d * math.sin(math.radians(a))) for a in (270, 0, 90, 180)]
    amber = {270, 0}
    for a, x, y in front:
        o.append(f'<circle class="fg-cell{" fg-cell-a" if a in amber else ""}" cx="{f(x)}" cy="{f(y)}" r="{r}"/>')
    for a, x, y in front:
        o.append(f'<circle class="{"fg-nuc-a" if a in amber else "fg-nuc"}" cx="{f(x)}" cy="{f(y)}" r="3.2"/>')
    cw, ch, g = 10, 15, 2.5
    xs, ys = 212, 44
    rows, cols = 8, 11
    mod_rows, mod_cols = (0, 1), (6, 7, 8)
    for rr in range(rows):
        for c in range(cols):
            mod = rr in mod_rows and c in mod_cols
            val = rng.uniform(.72, 1) if mod else rng.uniform(.08, .52)
            cls = "fg-heat-a" if mod else "fg-heat"
            o.append(f'<rect class="{cls}" x="{f(xs + c * (cw + g))}" y="{f(ys + rr * (ch + g))}" width="{cw}" height="{ch}" rx="1.5" fill-opacity="{val:.2f}"/>')
    mx = xs + mod_cols[0] * (cw + g) - 3
    my = ys + mod_rows[0] * (ch + g) - 3
    mw = len(mod_cols) * cw + (len(mod_cols) - 1) * g + 6
    mh = len(mod_rows) * ch + (len(mod_rows) - 1) * g + 6
    o.append(f'<rect class="fg-module" x="{f(mx)}" y="{f(my)}" width="{f(mw)}" height="{f(mh)}" rx="3"/>')
    for rr in mod_rows:
        yy = ys + rr * (ch + g) + ch / 2
        o.append(f'<path class="fg-tick" d="M{xs - 9} {f(yy)} L{xs - 4} {f(yy)}"/>')
    o.append('</svg>')
    return "\n".join(o) + "\n"


files = {
    "fig-signal.html": hero(),
    "glyph-algorithms.html": glyph_algorithms(),
    "glyph-bci.html": glyph_bci(),
    "glyph-embryo.html": glyph_embryo(),
    "plate-algorithms.html": plate_algorithms(),
    "plate-bci.html": plate_bci(),
    "plate-embryo.html": plate_embryo(),
}
for name, svg in files.items():
    with open(os.path.join(OUT, name), "w") as fh:
        fh.write(svg)
print({k: len(v) for k, v in files.items()})
