"""Draw the 171-vertex (7,3) graph with D9-equivariant coordinates, and its Z9 voltage base graph.

Every edge of the published edge list is drawn exactly once. Vertex (u,x) = 9u + x is placed at
angle 90 deg + 40 deg * (x + offset[u]) and radius radius[u] (figures/layout.json), so the
translation (u,x) -> (u,x+1) is the rotation by 40 degrees.  The reflection
(u,x) -> (sigma[u], m[u] - x) is checked to be an automorphism and is drawn as the mirror in the
vertical axis.  Requires Matplotlib.
"""
import json
import math
import os
import tempfile
from pathlib import Path

os.environ.setdefault('MPLCONFIGDIR', str(Path(tempfile.gettempdir()) / 'ddp-matplotlib'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Circle, FancyArrowPatch

HERE = Path(__file__).resolve().parent.parent
FIG = HERE / 'figures'
rows = [tuple(map(int, l.split())) for l in (HERE / 'certificate/graph.edges').read_text().splitlines()]
n, m = rows[0]
assert (n, m) == (171, 594)
EDGES = rows[1:]
actual = set(EDGES)
L = json.loads((FIG / 'layout.json').read_text())
off, rad, sig, mm = L['offset'], L['radius'], L['reflection']['sigma'], L['reflection']['m']

pos = {}
for u in range(19):
    for x in range(9):
        th = math.pi / 2 + 2 * math.pi * (x + off[u]) / 9
        pos[9 * u + x] = (rad[u] * math.cos(th), rad[u] * math.sin(th))

# symmetry checks
rot = lambda p, a: (p[0] * math.cos(a) - p[1] * math.sin(a), p[0] * math.sin(a) + p[1] * math.cos(a))
tau = [9 * sig[v // 9] + (mm[v // 9] - v % 9) % 9 for v in range(n)]
assert sorted(tau) == list(range(n)) and all(tau[tau[v]] == v for v in range(n))
for a, b in EDGES:
    for p in ([9 * (a // 9) + (a % 9 + 1) % 9, 9 * (b // 9) + (b % 9 + 1) % 9], [tau[a], tau[b]]):
        assert (min(p), max(p)) in actual
for v in range(n):
    r = rot(pos[v], 2 * math.pi / 9)
    w = pos[9 * (v // 9) + (v % 9 + 1) % 9]
    assert math.hypot(r[0] - w[0], r[1] - w[1]) < 1e-5
    t = pos[tau[v]]
    assert math.hypot(t[0] + pos[v][0], t[1] - pos[v][1]) < 1e-5

DOUBLE = {(1, 10), (2, 5), (3, 9), (4, 7), (6, 12), (8, 11)}


def kind(e):
    ua, ub = e[0] // 9, e[1] // 9
    if 0 in (ua, ub):
        return 'hub'
    if ua >= 13 and ub >= 13:
        return 'loop' if ua == ub else 'pair'
    if ua >= 13 or ub >= 13:
        return 'spokecore'
    return 'coredouble' if (min(ua, ub), max(ua, ub)) in DOUBLE else 'core'


STYLE = {  # kind: (colour, width, alpha, label)
    'core': ('#3566B2', .55, .42, 'core – core'),
    'coredouble': ('#C14869', .6, .62, 'core double edges'),
    'spokecore': ('#3D8A55', .65, .72, 'spoke – core'),
    'pair': ('#C86B2B', .75, .85, 'spoke pairs (voltages 3, 6)'),
    'loop': ('#7C55A5', .75, .85, 'spoke loops'),
    'hub': ('#087E8B', .95, .9, 'hub – spoke'),
}
counts = {k: sum(1 for e in EDGES if kind(e) == k) for k in STYLE}
assert counts == {'core': 216, 'coredouble': 108, 'spokecore': 108, 'pair': 54, 'loop': 54, 'hub': 54}

# clearance: no edge passes close to a vertex it is not incident to
clear = 1e9
for a, b in EDGES:
    (ax_, ay), (bx, by) = pos[a], pos[b]
    dx, dy = bx - ax_, by - ay
    for w, (wx, wy) in pos.items():
        if w in (a, b):
            continue
        t = max(0, min(1, ((wx - ax_) * dx + (wy - ay) * dy) / (dx * dx + dy * dy)))
        clear = min(clear, math.hypot(wx - ax_ - t * dx, wy - ay - t * dy))
assert clear > 0.04, clear

plt.rcParams.update({'font.family': 'DejaVu Sans', 'svg.fonttype': 'none', 'pdf.fonttype': 42,
                     'svg.hashsalt': 'ddp-figures'})  # deterministic SVG ids
BG, INK, MUTED = '#FCFBF7', '#183747', '#536B78'


def save(fig, stem):
    for suffix in ['png', 'svg', 'pdf']:
        out = FIG / f'{stem}.{suffix}'
        meta = {'svg': {'Date': None}, 'pdf': {'CreationDate': None}}.get(suffix)  # no timestamps
        fig.savefig(out, dpi=180, facecolor=BG, metadata=meta)
        if suffix == 'svg':
            out.write_text('\n'.join(l.rstrip() for l in out.read_text().splitlines()) + '\n')
    plt.close(fig)


# ---------------------------------------------------------------- figure 1: the whole graph
fig, ax = plt.subplots(figsize=(11, 12.4), facecolor=BG)
ax.set_facecolor(BG); ax.set_aspect('equal'); ax.axis('off')
drawn = set()
for k in ['core', 'coredouble', 'spokecore', 'pair', 'loop', 'hub']:
    col, lw, al, _ = STYLE[k]
    for e in EDGES:
        if kind(e) != k:
            continue
        a, b = e
        assert e not in drawn
        drawn.add(e)
        ax.plot([pos[a][0], pos[b][0]], [pos[a][1], pos[b][1]], color=col, lw=lw, alpha=al, zorder=2,
                solid_capstyle='round')
assert drawn == actual
for v in range(n):
    u = v // 9
    big = (u == 0)
    ax.scatter(*pos[v], s=46 if big else 15, c=INK, edgecolors=BG, linewidths=.8 if big else .6, zorder=5)
for t in range(9):  # mirror axes of the D9 symmetry, faint
    a = math.pi / 2 + math.pi * t / 9
    ax.plot([-5.9 * math.cos(a), 5.9 * math.cos(a)], [-5.9 * math.sin(a), 5.9 * math.sin(a)],
            color='#C9D3D8', lw=.5, ls=(0, (2, 4)), zorder=0)
handles = [Line2D([0], [0], color=STYLE[k][0], lw=2.2, label=f'{STYLE[k][3]}  ({counts[k]})')
           for k in ['hub', 'pair', 'loop', 'spokecore', 'coredouble', 'core']]
ax.legend(handles=handles, loc='lower center', bbox_to_anchor=(.5, -.065), ncol=3, frameon=False, fontsize=9.5,
          labelcolor=INK, handlelength=2.2)
ax.set_xlim(-6.0, 6.0); ax.set_ylim(-6.0, 6.0)
fig.suptitle('171 vertices · maximum degree 7 · diameter 3', fontsize=23, fontweight='medium', color=INK, y=.975)
fig.text(.5, .937, 'dihedral symmetry D₉  /  19 fibres of 9 vertices over a 19-vertex base graph', ha='center',
         fontsize=12, color=MUTED)
fig.text(.5, .055, 'Aut(G) has order 216     •     (u, x) ↦ (u, x + 1) is the rotation by 40°', ha='center',
         fontsize=13.5, color=INK)
fig.text(.5, .03, 'All 594 edges are drawn. Crossings without dots are not vertices. The nine star tips are the '
         'hub fibre, the only vertices of degree 6.', ha='center', fontsize=9, color=MUTED)
fig.subplots_adjust(left=.03, right=.97, bottom=.12, top=.92)
save(fig, 'n73_171_symmetry')

# ---------------------------------------------------------------- figure 2: the base graph
import importlib.util
spec = importlib.util.spec_from_file_location('construct', HERE / 'certificate/construct.py')
C = importlib.util.module_from_spec(spec); spec.loader.exec_module(C)
SPOKE_ANGLE = {14: 72, 13: 108, 16: 192, 15: 228, 18: 312, 17: 348}
CORE_OF = {13: (8, 11), 14: (2, 5), 15: (6, 12), 16: (3, 9), 17: (4, 7), 18: (1, 10)}
bp = {0: (0.0, 0.0)}
for s, a in SPOKE_ANGLE.items():
    bp[s] = (1.85 * math.cos(math.radians(a)), 1.85 * math.sin(math.radians(a)))
    for i, c in enumerate(CORE_OF[s]):
        b = math.radians(a + (-8 if i == 0 else 8))
        bp[c] = (3.75 * math.cos(b), 3.75 * math.sin(b))
fig, ax = plt.subplots(figsize=(14.2, 9.4), facecolor=BG)
ax.set_facecolor(BG); ax.set_aspect('equal'); ax.axis('off')


def label(x, y, text, col):
    ax.text(x, y, text, ha='center', va='center', fontsize=10.5, color=col,
            bbox=dict(boxstyle='round,pad=.12', fc=BG, ec='none', alpha=.95), zorder=7)


def curve(p, q, bend, col, lw, txt=None, frac=.5):
    """Quadratic Bezier from p to q (arc3 connection); arrowhead at q when labelled."""
    (x1, y1), (x2, y2) = p, q
    rad = -bend
    ax.add_patch(FancyArrowPatch(posA=p, posB=q, connectionstyle=f'arc3,rad={rad}',
                                 arrowstyle='-|>' if txt is not None else '-', mutation_scale=13,
                                 color=col, lw=lw, zorder=3, shrinkA=12, shrinkB=13))
    if txt is not None:
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        cx, cy = mx + rad * (y2 - y1), my - rad * (x2 - x1)
        t = frac
        lx = (1 - t) ** 2 * x1 + 2 * (1 - t) * t * cx + t * t * x2
        ly = (1 - t) ** 2 * y1 + 2 * (1 - t) * t * cy + t * t * y2
        label(lx, ly, txt, col)


base_core = [(u, v, a) for (u, v, a) in C.CORE if (u, v) not in DOUBLE]
for (u, v, a) in base_core:
    curve(bp[u], bp[v], 0.0, '#9FB4C6', .8)
for (u, v, a) in C.HUB:
    curve(bp[u], bp[v], 0.0, STYLE['hub'][0], 2.0, f'{a}', .56)
for (u, v, a) in C.SPOKE_PAIRS:
    curve(bp[u], bp[v], .55 if a == 3 else -.55, STYLE['pair'][0], 1.8, f'{a}', .5)
for (u, v, a) in C.SPOKE_CORE:  # data orientation u < v: core -> spoke
    curve(bp[u], bp[v], 0.0, STYLE['spokecore'][0], 1.6, f'{a}', .45)
done = set()
for (u, v, a) in C.CORE:
    if (u, v) in DOUBLE:
        bend = .45 if (u, v) not in done else -.45
        done.add((u, v))
        curve(bp[u], bp[v], bend, STYLE['coredouble'][0], 1.6, f'{a}', .5)
for (u, a) in C.LOOPS:
    x, y = bp[u]
    rr = math.hypot(x, y)
    cx, cy = x / rr * (rr + .38), y / rr * (rr + .38)
    ax.add_patch(Circle((cx, cy), .27, fill=False, ec=STYLE['loop'][0], lw=1.6, zorder=3))
    label(x / rr * (rr + .72), y / rr * (rr + .72), f'±{a}', STYLE['loop'][0])
for u, (x, y) in bp.items():
    col = '#087E8B' if u == 0 else (INK if u <= 12 else '#2F5D6E')
    ax.scatter(x, y, s=560 if u == 0 else 380, c=col, edgecolors=BG, linewidths=2, zorder=5)
    ax.text(x, y, str(u), ha='center', va='center', fontsize=11 if u else 12, color='white', zorder=6,
            fontweight='bold' if u == 0 else 'normal')
ax.text(0, -.62, 'hub', ha='center', fontsize=10, color='#087E8B')
# table of the 24 remaining core edges
txt = '\n'.join(f'{u:>2} – {v:<2}  {a}' for (u, v, a) in base_core)
ax.text(5.0, 3.95, 'other core edges\n(arrow u → v, u < v; voltage)', ha='left', va='top', fontsize=10.5, color=INK)
for j, chunk in enumerate([base_core[0:8], base_core[8:16], base_core[16:24]]):
    ax.text(5.0 + 1.45 * j, 3.1, '\n'.join(f'{u:>2}→{v:<2} {a}' for (u, v, a) in chunk), ha='left', va='top',
            fontsize=10, color='#3566B2', family='DejaVu Sans Mono', linespacing=1.55)
ax.set_xlim(-4.6, 9.4); ax.set_ylim(-4.6, 4.6)
fig.suptitle('The Z₉ voltage graph behind the 171 vertices', fontsize=21, color=INK, y=.975)
fig.text(.5, .905, r'Node u stands for the fibre $\{(u,x):x\in\mathbb{Z}_9\}$. An arrow $u\to v$ with label $a$ means '
         r'$(u,x)\sim(v,x+a)$; a loop with label $\pm a$ means $(u,x)\sim(u,x\pm a)$.', ha='center', fontsize=11.5,
         color=MUTED)
fig.text(.5, .04, 'Hub 0 (degree 6), spokes 13–18, core 1–12. Each spoke meets one core double edge. '
         'All 66 base edges are shown; thin blue lines are the 24 core edges listed on the right.', ha='center',
         fontsize=10.5, color=MUTED)
fig.subplots_adjust(left=.01, right=.99, bottom=.07, top=.88)
save(fig, 'n73_171_voltage')

(FIG / 'drawing-check.json').write_text(json.dumps({
    'vertices': n, 'edges': len(drawn), 'exact_edge_set_match': drawn == actual,
    'edge_classes': counts, 'rotation': '(u,x)->(u,x+1), checked as automorphism and as rotation by 40 degrees',
    'reflection_checked_as_automorphism_and_mirror': True,
    'minimum_edge_vertex_clearance': round(clear, 6), 'coordinates': {str(v): [round(p[0], 6), round(p[1], 6)]
                                                                       for v, p in pos.items()}}, indent=1) + '\n')
print(f'Saved n73_171_symmetry and n73_171_voltage (PNG, SVG, PDF); {len(drawn)} edges, clearance {clear:.4f}.')
