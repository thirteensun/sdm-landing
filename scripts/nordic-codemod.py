# Applies the Rollable Nordic design tokens to a lab app (see DESIGN.md, "Lab apps").
# Usage: python3 nordic_codemod.py <repo>/src  [<repo>/tailwind.config.js]
import pathlib, re, sys

COLORS = {  # old palette -> framework palette
    '#1a1a18': '#1d1d1b', '#6b6960': '#55544f', '#9b9890': '#8d8b85', '#c8c5be': '#cfccc4',
    '#f5f4f0': '#f6f5f2', '#1d9e75': '#2f7d5b', '#ef9f27': '#b9822c', '#e24b4a': '#b4483c',
    '#b8760d': '#b9822c',
}
MONO = re.compile(r"""fontFamily:\s*'ui-monospace[^']*'""")
stats = {}

def bump(k, n=1): stats[k] = stats.get(k, 0) + n

def radius(m):
    n = int(m.group(2))
    if 10 <= n <= 24: bump('radius'); return f"{m.group(1)}{6 if n <= 20 else 8}"
    return m.group(0)

for root in sys.argv[1:]:
    root = pathlib.Path(root)
    files = [root] if root.is_file() else [p for p in root.rglob('*') if p.suffix in ('.tsx', '.ts', '.css', '.js') and 'node_modules' not in p.parts]
    for p in files:
        s = o = p.read_text()
        for old, new in COLORS.items():
            s, n = re.subn(re.escape(old), new, s, flags=re.I); bump('colour', n)
        # Labels: no uppercase, no positive letter-spacing (negative tracking on headings stays).
        s, n = re.subn(r"\s*textTransform:\s*'uppercase',?", '', s); bump('uppercase', n)
        s, n = re.subn(r"\s*letterSpacing:\s*'0\.\d+em',?", '', s); bump('tracking', n)
        s, n = re.subn(r"(className=\{?[`'\"][^`'\"]*?)\s(?:uppercase|tracking-(?:wide|wider|widest))\b", r'\1', s); bump('tw-labels', n)
        while True:  # a className may hold both; repeat until none left
            s2, n = re.subn(r"(className=\{?[`'\"][^`'\"]*?)\s(?:uppercase|tracking-(?:wide|wider|widest))\b", r'\1', s)
            if not n: break
            s = s2; bump('tw-labels', n)
        s, n = MONO.subn("fontFamily: 'inherit'", s); bump('mono', n)
        # Corners: 10–24px radii become 6px (8px for the largest); pills and circles are untouched.
        s = re.sub(r"(borderRadius:\s*)(\d+)(?![\d%])", radius, s)
        s = re.sub(r"(border-radius:\s*)(\d+)(?=px)", radius, s)
        s = re.sub(r"(borderRadius:\s*['\"])(\d+)(?=px['\"])", radius, s)
        s, n = re.subn(r"\brounded-(?:xl|2xl|3xl)\b", 'rounded-md', s); bump('tw-rounded', n)
        if s != o:
            p.write_text(s); bump('files')
print(stats)
