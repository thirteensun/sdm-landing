# Regenerates the ink-brush Go board drawing in index.html: python3 scripts/go-board.py index.html
#
# A whole goban seen slightly from above, drawn in black ink as with a Chinese brush (maobi):
# every line is a filled stroke that presses at the start, thins and tapers, with dry-brush streaks.
import math, pathlib, random, re, sys

random.seed(11)
path = pathlib.Path(sys.argv[1])
s = path.read_text()

INK = "#141413"
W, H = 260, 340
N = 12          # a 13×13 board: 13 lines = 12 intervals, legible at this size
M = 0.75        # board margin beyond the outer lines, in cells

# --- Perspective: map board coordinates (u across, v from front to back) onto the screen ---
def solve(A, b):
    n = len(A)
    for i in range(n):
        piv = max(range(i, n), key=lambda r: abs(A[r][i]))
        A[i], A[piv], b[i], b[piv] = A[piv], A[i], b[piv], b[i]
        for r in range(i + 1, n):
            f = A[r][i] / A[i][i]
            for c in range(i, n): A[r][c] -= f * A[i][c]
            b[r] -= f * b[i]
    x = [0] * n
    for i in reversed(range(n)):
        x[i] = (b[i] - sum(A[i][c] * x[c] for c in range(i + 1, n))) / A[i][i]
    return x

lo, hi = -M, N + M
src = [(lo, lo), (hi, lo), (hi, hi), (lo, hi)]                  # front-left, front-right, back-right, back-left
dst = [(14, 236), (246, 236), (216, 96), (44, 96)]
A, b = [], []
for (u, v), (x, y) in zip(src, dst):
    A.append([u, v, 1, 0, 0, 0, -u * x, -v * x]); b.append(x)
    A.append([0, 0, 0, u, v, 1, -u * y, -v * y]); b.append(y)
h = solve(A, b)
def P(u, v):
    d = h[6] * u + h[7] * v + 1
    return ((h[0] * u + h[1] * v + h[2]) / d, (h[3] * u + h[4] * v + h[5]) / d)

# --- Brush stroke: a filled outline whose width follows a press, thin, taper profile ---
def brush(p0, p1, w, press=1.6, taper=0.15, jitter=0.25, dry="dryH"):
    (x0, y0), (x1, y1) = p0, p1
    L = math.hypot(x1 - x0, y1 - y0)
    nx, ny = -(y1 - y0) / L, (x1 - x0) / L
    steps = max(8, int(L / 3))
    left, right = [], []
    for i in range(steps + 1):
        t = i / steps
        prof = (press if t < 0.06 else 1) * (0.75 + 0.35 * math.sin(math.pi * t)) * (1 - (1 - taper) * max(0, (t - 0.8) / 0.2))
        hw = w * prof / 2 + random.uniform(-jitter, jitter) * w * 0.15
        x, y = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t
        left.append((x + nx * hw, y + ny * hw)); right.append((x - nx * hw, y - ny * hw))
    pts = left + right[::-1]
    d = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts) + "Z"
    return f'<path d="{d}" fill="{INK}" filter="url(#{dry})" />'

def ring_path(cx, cy, rx, ry, w):
    # A brushed circle drawn as one stroke that leaves a gap where the brush lifts.
    start = random.uniform(0, 2 * math.pi); span = 2 * math.pi * 0.88
    steps = 40; outer, inner = [], []
    for i in range(steps + 1):
        t = i / steps; a = start + span * t
        hw = w * (1.5 if t < 0.08 else 1) * (1 - 0.7 * max(0, (t - 0.85) / 0.15)) / 2
        outer.append((cx + (rx + hw) * math.cos(a), cy + (ry + hw * ry / rx) * math.sin(a)))
        inner.append((cx + (rx - hw) * math.cos(a), cy + (ry - hw * ry / rx) * math.sin(a)))
    pts = outer + inner[::-1]
    return "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts) + "Z"

defs = f'''<defs>
<filter id="dryH" x="-5%" y="-30%" width="110%" height="160%"><feTurbulence type="fractalNoise" baseFrequency="0.035 0.9" numOctaves="2" seed="3" result="n" /><feColorMatrix in="n" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 -1.3 1.55" result="m" /><feComposite in="SourceGraphic" in2="m" operator="in" result="c" /><feTurbulence type="fractalNoise" baseFrequency="0.05" numOctaves="2" seed="6" result="w" /><feDisplacementMap in="c" in2="w" scale="1.6" /></filter>
<filter id="dryV" x="-30%" y="-5%" width="160%" height="110%"><feTurbulence type="fractalNoise" baseFrequency="0.9 0.035" numOctaves="2" seed="8" result="n" /><feColorMatrix in="n" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 -1.3 1.55" result="m" /><feComposite in="SourceGraphic" in2="m" operator="in" result="c" /><feTurbulence type="fractalNoise" baseFrequency="0.05" numOctaves="2" seed="2" result="w" /><feDisplacementMap in="c" in2="w" scale="1.6" /></filter>
<filter id="bleed" x="-30%" y="-30%" width="160%" height="160%"><feTurbulence type="fractalNoise" baseFrequency="0.8" numOctaves="2" seed="9" result="n" /><feDisplacementMap in="SourceGraphic" in2="n" scale="2.4" result="d" /><feGaussianBlur in="d" stdDeviation="0.35" /></filter>
</defs>'''

parts = []

# Board body: the top outline, the front face (thickness) and four short legs, in bold strokes.
FL, FR, BR, BL = P(lo, lo), P(hi, lo), P(hi, hi), P(lo, hi)
T = 30   # thickness of the board in screen pixels
parts.append(f'<path d="M{FL[0]:.1f} {FL[1]:.1f} L{FR[0]:.1f} {FR[1]:.1f} L{BR[0]:.1f} {BR[1]:.1f} L{BL[0]:.1f} {BL[1]:.1f}Z" fill="#ffffff" />')
parts.append(f'<rect x="{FL[0]:.1f}" y="{FL[1]:.1f}" width="{FR[0] - FL[0]:.1f}" height="{T}" fill="#ffffff" />')
parts.append(brush(BL, BR, 2.2, dry="dryH"))
parts.append(brush(BL, FL, 2.6, dry="dryV"))
parts.append(brush(BR, FR, 2.6, dry="dryV"))
parts.append(brush(FL, FR, 3.2, dry="dryH"))
parts.append(brush((FL[0], FL[1] - 1), (FL[0] + 1, FL[1] + T), 3.4, dry="dryV"))
parts.append(brush((FR[0], FR[1] - 1), (FR[0] - 1, FR[1] + T), 3.4, dry="dryV"))
parts.append(brush((FL[0] - 1, FL[1] + T), (FR[0] + 1, FR[1] + T), 4.2, press=1.3, dry="dryH"))
# Legs: short, rounded blocks under the front corners, and a hint of the back ones.
for lx in (FL[0] + 22, FR[0] - 22):
    parts.append(brush((lx - 7, FL[1] + T + 2), (lx - 6, FL[1] + T + 22), 3.6, dry="dryV"))
    parts.append(brush((lx + 7, FL[1] + T + 2), (lx + 6, FL[1] + T + 22), 3.6, dry="dryV"))
    parts.append(brush((lx - 7, FL[1] + T + 22), (lx + 7, FL[1] + T + 22), 3.0, dry="dryH"))
for lx in (FL[0] + 48, FR[0] - 48):
    parts.append(brush((lx, FL[1] + T + 3), (lx, FL[1] + T + 14), 2.4, dry="dryV"))

# Grid: thin strokes, each pressed at its start and tapering away.
grid = []
for i in range(N + 1):
    grid.append(brush(P(i, -0.05), P(i, N + 0.05), 1.15, press=1.6, taper=0.4, dry="dryV"))
    grid.append(brush(P(-0.05, i), P(N + 0.05, i), 1.15, press=1.6, taper=0.4, dry="dryH"))
parts.append("".join(grid))
for a, c in [(3, 3), (9, 3), (6, 6), (3, 9), (9, 9)]:
    x, y = P(a, c)
    parts.append(f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="2.4" ry="1.7" fill="{INK}" filter="url(#bleed)" />')

# Stones in the front-left corner: a 4-4 point with a 3-3 invasion, placed one by one.
moves = [(3, 3), (2, 2), (2, 3), (3, 2), (4, 2), (4, 1), (5, 2), (5, 1), (6, 2)]
for k, (a, c) in enumerate(moves):
    x, y = P(a, c)
    cell_w = P(a + 0.5, c)[0] - P(a - 0.5, c)[0]
    cell_h = P(a, c - 0.5)[1] - P(a, c + 0.5)[1]
    rx, ry = cell_w * 0.48, cell_h * 0.48
    delay = 0.3 + 0.5 * k
    if k % 2 == 0:
        body = (f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" fill="#ffffff" />'
                f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" fill="{INK}" filter="url(#bleed)" />')
    else:
        body = (f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" fill="#ffffff" />'
                f'<path d="{ring_path(x, y, rx, ry, 1.7)}" fill="{INK}" filter="url(#bleed)" />')
    parts.append(f'<g class="stone" style="animation-delay:{delay:.2f}s">{body}</g>')
x, y = P(2, 5)
rx = (P(2.5, 5)[0] - P(1.5, 5)[0]) * 0.45; ry = (P(2, 4.5)[1] - P(2, 5.5)[1]) * 0.45
parts.append(f'<ellipse class="next" cx="{x:.1f}" cy="{y:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" fill="none" stroke="{INK}" '
             f'stroke-width=".8" stroke-dasharray="2 2.5" style="animation-delay:{0.3 + 0.5 * len(moves) + 0.3:.2f}s" />')

SVG = (f'<div class="board" aria-hidden="true"><svg viewBox="0 84 {W} 222">' + defs + "".join(parts) + '</svg></div>')
s, n = re.subn(r'<div class="board" aria-hidden="true">.*?</svg></div>', lambda m: SVG, s, flags=re.S)
assert n == 1
path.write_text(s)
print('board written', len(SVG))
