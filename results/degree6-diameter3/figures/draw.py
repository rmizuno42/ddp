"""Draw the 126-vertex (6,3) graph with D3-equivariant coordinates, and its Z3 x Z3 voltage base graph.

Every edge of the published edge list is drawn exactly once. figures/layout.json gives two
automorphisms, r of order 3 and an involution t with t r t = r^-1; they generate a dihedral group
D3 that acts freely on the vertices (21 orbits of 6). For each orbit it gives a base vertex v, an
angle theta measured from the vertical axis and a radius: r^k v is drawn at angle
90 deg + theta + 120 deg * k and r^k t v at angle 90 deg - theta + 120 deg * k, so r is the rotation
by 120 degrees and t is the mirror in the vertical axis. The script checks both automorphisms, the
equivariance of the drawing, and that no edge passes close to a vertex it is not incident to.
Requires Matplotlib.
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
from matplotlib.patches import FancyArrowPatch

HERE = Path(__file__).resolve().parent.parent
FIG = HERE / 'figures'
rows = [tuple(map(int, l.split())) for l in (HERE / 'certificate/graph.edges').read_text().splitlines()]
n, m = rows[0]
assert (n, m) == (126, 378)
EDGES = rows[1:]
actual = set(EDGES)
L = json.loads((FIG / 'layout.json').read_text())
rot, ref = L['rotation'], L['reflection']
for perm in (rot, ref):
    assert sorted(perm) == list(range(n))
    for a, b in EDGES:
        assert (min(perm[a], perm[b]), max(perm[a], perm[b])) in actual, 'not an automorphism'
assert all(rot[v] != v and rot[rot[rot[v]]] == v for v in range(n)), 'rotation: fixed-point-free, order 3'
assert all(ref[v] != v and ref[ref[v]] == v for v in range(n)), 'reflection: fixed-point-free involution'
assert all(ref[rot[ref[v]]] == rot[rot[v]] for v in range(n)), 't r t = r^-1'

pos = {}
for v0, th, rad in zip(L['orbit_base_points'], L['theta'], L['radius']):
    for mirrored in (False, True):
        v = ref[v0] if mirrored else v0
        for k in range(3):
            a = math.pi / 2 + (-th if mirrored else th) + 2 * math.pi * k / 3
            assert v not in pos
            pos[v] = (rad * math.cos(a), rad * math.sin(a))
            v = rot[v]
assert len(pos) == n
c3, s3 = math.cos(2 * math.pi / 3), math.sin(2 * math.pi / 3)
for v in range(n):
    x, y = pos[v]
    rx, ry = pos[rot[v]]
    tx, ty = pos[ref[v]]
    assert math.hypot(c3 * x - s3 * y - rx, s3 * x + c3 * y - ry) < 1e-6  # rotation by 120 degrees
    assert math.hypot(-x - tx, y - ty) < 1e-6                              # mirror in the vertical axis

# vertex roles = the three Aut(G)-orbits: fibres of h, h', b0, b2, b'0, b'2 (H), triangle fibres (T), b1, b'1 (S)
ROLE = {0: 'H', 1: 'H', 5: 'H', 7: 'H', 11: 'H', 13: 'H', 2: 'T', 3: 'T', 4: 'T', 8: 'T', 9: 'T', 10: 'T',
        6: 'S', 12: 'S'}


def kind(e):
    t = tuple(sorted((ROLE[e[0] // 9], ROLE[e[1] // 9])))
    return {('H', 'H'): 'HH', ('H', 'T'): 'HT', ('T', 'T'): 'TT', ('S', 'T'): 'ST', ('S', 'S'): 'SS'}[t]


STYLE = {  # kind: (colour, width, alpha, legend)
    'HT': ('#3566B2', .6, .5, 'inner ring – triangle fibres'),
    'HH': ('#C86B2B', .75, .75, 'bundles h–h′, b₀–b′₀, b₂–b′₂'),
    'TT': ('#3D8A55', .85, .85, 'triangle edges'),
    'ST': ('#7C55A5', .85, .85, 'b₁, b′₁ – triangle fibres'),
    'SS': ('#C14869', 1.0, .9, 'bundle b₁–b′₁'),
}
counts = {k: sum(1 for e in EDGES if kind(e) == k) for k in STYLE}
assert counts == {'HT': 162, 'HH': 81, 'TT': 54, 'ST': 54, 'SS': 27}

clear = {'small': 1e9, 'large': 1e9}  # large dots: b1 and b'1 fibres
for a, b in EDGES:
    (ax_, ay), (bx, by) = pos[a], pos[b]
    dx, dy = bx - ax_, by - ay
    for w, (wx, wy) in pos.items():
        if w in (a, b):
            continue
        t = max(0, min(1, ((wx - ax_) * dx + (wy - ay) * dy) / (dx * dx + dy * dy)))
        key = 'large' if ROLE[w // 9] == 'S' else 'small'
        clear[key] = min(clear[key], math.hypot(wx - ax_ - t * dx, wy - ay - t * dy))
assert clear['small'] > 0.03 and clear['large'] > 0.05, clear

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
fig, ax = plt.subplots(figsize=(11, 12.2), facecolor=BG)
ax.set_facecolor(BG); ax.set_aspect('equal'); ax.axis('off')
drawn = set()
for k in ['HT', 'HH', 'TT', 'ST', 'SS']:
    col, lw, al, _ = STYLE[k]
    for e in EDGES:
        if kind(e) != k:
            continue
        assert e not in drawn
        drawn.add(e)
        a, b = e
        ax.plot([pos[a][0], pos[b][0]], [pos[a][1], pos[b][1]], color=col, lw=lw, alpha=al, zorder=2,
                solid_capstyle='round')
assert drawn == actual
for v in range(n):
    big = ROLE[v // 9] == 'S'
    ax.scatter(*pos[v], s=42 if big else 15, c=INK, edgecolors=BG, linewidths=.8 if big else .6, zorder=5)
RR = max(math.hypot(*p) for p in pos.values()) + .25
for k in range(3):  # mirror axes of the D3 symmetry, faint
    a = math.pi / 2 + math.pi * k / 3
    ax.plot([-RR * math.cos(a), RR * math.cos(a)], [-RR * math.sin(a), RR * math.sin(a)],
            color='#C9D3D8', lw=.5, ls=(0, (2, 4)), zorder=0)
handles = [Line2D([0], [0], color=STYLE[k][0], lw=2.2, label=f'{STYLE[k][3]}  ({counts[k]})')
           for k in ['HH', 'HT', 'TT', 'ST', 'SS']]
ax.legend(handles=handles, loc='lower center', bbox_to_anchor=(.5, -.07), ncol=3, frameon=False, fontsize=9.5,
          labelcolor=INK, handlelength=2.2)
ax.set_xlim(-RR, RR); ax.set_ylim(-RR, RR)
fig.suptitle('126 vertices · degree 6 · diameter 3', fontsize=23, fontweight='medium', color=INK, y=.975)
fig.text(.5, .937, 'dihedral symmetry D₃  /  21 orbits of 6 vertices on three rings', ha='center', fontsize=12,
         color=MUTED)
fig.text(.5, .055, 'Aut(G) has order 162     •     rings: h, h′, b₀, b₂, b′₀, b′₂ fibres (inner), '
         'triangle fibres, b₁ and b′₁ (outer)', ha='center', fontsize=12.5, color=INK)
fig.text(.5, .03, 'All 378 edges are drawn. Crossings without dots are not vertices. The rotation by 120° and '
         'the reflections in the three faint axes are automorphisms.', ha='center', fontsize=9, color=MUTED)
fig.subplots_adjust(left=.03, right=.97, bottom=.12, top=.92)
save(fig, 'n63_126_symmetry')

# ---------------------------------------------------------------- figure 2: the base graph
import importlib.util
spec = importlib.util.spec_from_file_location('construct', HERE / 'certificate/construct.py')
C = importlib.util.module_from_spec(spec); spec.loader.exec_module(C)
NAME = {0: 'h', 1: "h′", 2: 'a₀', 3: 'a₁', 4: 'a₂', 5: 'b₀', 6: 'b₁', 7: 'b₂', 8: "a′₀", 9: "a′₁", 10: "a′₂",
        11: "b′₀", 12: "b′₁", 13: "b′₂"}
bp = {0: (-5.7, 0.0), 2: (-3.3, 1.3), 3: (-4.05, 0.0), 4: (-3.3, -1.3), 5: (-1.1, 2.25), 6: (-1.1, 0.0),
      7: (-1.1, -2.25)}
for u, (x, y) in list(bp.items()):
    bp[{0: 1, 2: 8, 3: 9, 4: 10, 5: 11, 6: 12, 7: 13}[u]] = (-x, y)
fig, ax = plt.subplots(figsize=(15.5, 10.6), facecolor=BG)
ax.set_facecolor(BG); ax.set_aspect('equal'); ax.axis('off')


def fmt(gv):
    return '0' if gv == (0, 0) else f'({gv[0]},{gv[1]})'


def label(x, y, text, col, fs=9.5):
    ax.text(x, y, text, ha='center', va='center', fontsize=fs, color=col,
            bbox=dict(boxstyle='round,pad=.1', fc=BG, ec='none', alpha=.95), zorder=7)


def curve(p, q, bend, col, lw, txt, frac=.5, arrow=True, fs=9.5):
    (x1, y1), (x2, y2) = p, q
    ax.add_patch(FancyArrowPatch(posA=p, posB=q, connectionstyle=f'arc3,rad={bend}',
                                 arrowstyle='-|>' if arrow else '-', mutation_scale=12, color=col, lw=lw, zorder=3,
                                 shrinkA=14, shrinkB=15))
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    cx, cy = mx + bend * (y2 - y1), my - bend * (x2 - x1)
    t = frac
    label((1 - t) ** 2 * x1 + 2 * (1 - t) * t * cx + t * t * x2, (1 - t) ** 2 * y1 + 2 * (1 - t) * t * cy + t * t * y2,
          txt, col, fs)


COL = {'hub': '#C86B2B', 'tri': '#3D8A55', 'ab': '#3566B2', 'bund': '#C14869', 'zero': '#8A9AA5'}
assert sum(len(gs) for _, _, gs in C.BASE_EDGES) == 42  # 14 base vertices of degree 6
for (u, v, gs) in C.BASE_EDGES:
    p, q = bp[u], bp[v]
    if (u, v) != (0, 1) and ((u in (0, 1)) or (u in (2, 8) and v not in (3, 4, 9, 10))):
        assert gs == [(0, 0)], (u, v, gs)  # drawn grey without a label
    if (u, v) == (0, 1):
        for gv, bend in zip(gs, [-.68, -.61, -.54]):
            curve(p, q, bend, COL['hub'], 1.5, fmt(gv), .5)
    elif u in (5, 6, 7) and v in (11, 12, 13):
        for gv, bend in zip(gs, [.32, 0.0, -.32]):
            curve(p, q, bend, COL['bund'], 1.5, fmt(gv), .5)
    elif (u in (0, 1)) or (u in (2, 8) and v not in (3, 4, 9, 10)):
        curve(p, q, 0.0, COL['zero'], 1.1, '', .5, arrow=False)
    elif v in (3, 4, 9, 10) and u in (2, 3, 8, 9):
        bend = (-.22 if (u, v) == (2, 4) else .0) if u < 8 else (.22 if (u, v) == (8, 10) else .0)
        curve(p, q, bend, COL['tri'], 1.5, fmt(gs[0]), .5)
    else:
        curve(p, q, 0.0, COL['ab'], 1.2, fmt(gs[0]), .62)
for u, (x, y) in bp.items():
    col = {'H': '#183747', 'T': '#3D8A55', 'S': '#7C55A5'}[ROLE[u]]
    ax.scatter(x, y, s=720, c=col, edgecolors=BG, linewidths=2, zorder=5)
    ax.text(x, y, NAME[u], ha='center', va='center', fontsize=12, color='white', zorder=6)

# AG(2,3) insets: the four bundles are relative difference sets avoiding one direction
insets = [('h → h′', [(0, 0), (1, 1), (2, 1)], (0, 1)),
          ('b₀ → b′₀', [(2, 2), (0, 2), (0, 1)], (1, 1)),
          ('b₁ → b′₁', [(2, 0), (2, 1), (1, 2)], (1, 0)),
          ('b₂ → b′₂', [(1, 0), (0, 0), (0, 2)], (1, 2))]
for k, (title, S, d) in enumerate(insets):
    ox, oy, sc = -5.4 + 3.05 * k, -4.95, .42
    pts = [(a, b) for a in range(3) for b in range(3)]
    for (a, b) in pts:
        ax.scatter(ox + a * sc, oy + b * sc, s=22, c='#C7D0D6', zorder=4)
    line = {((t * d[0]) % 3, (t * d[1]) % 3) for t in range(3)}
    diffs = {((x[0] - y[0]) % 3, (x[1] - y[1]) % 3) for x in S for y in S if x != y}
    assert len(diffs) == 6 and not diffs & line  # a (3,3,3,1) relative difference set avoiding <d>
    for (a, b) in line:
        ax.scatter(ox + a * sc, oy + b * sc, s=290, facecolors='none', edgecolors='#8A9AA5', linewidths=1.1,
                   linestyle=(0, (2.2, 1.6)), zorder=4)
    for (a, b) in S:
        ax.scatter(ox + a * sc, oy + b * sc, s=58, c=COL['bund'] if k else COL['hub'], zorder=5)
    ax.text(ox + sc, oy + 3.05 * sc, title, ha='center', fontsize=10.5, color=INK)
    ax.text(ox + sc, oy - .62, f'avoids ⟨({d[0]},{d[1]})⟩', ha='center', fontsize=9.5, color=MUTED)
    for t in range(3):
        ax.text(ox + t * sc, oy - .25, str(t), ha='center', va='top', fontsize=7.5, color='#9AA7B0')
        ax.text(ox - .22, oy + t * sc, str(t), ha='right', va='center', fontsize=7.5, color='#9AA7B0')
ax.text(7.0, -3.55, 'Each triple of parallel voltages is a\n(3,3,3,1) relative difference set in\n'
        'AG(2,3): its six differences are\ndistinct and miss one line through 0\n(dashed rings). The four directions\n'
        'of AG(2,3) each occur once.', ha='left', va='top', fontsize=10, color=MUTED, linespacing=1.4)
for i, (col, txt) in enumerate([('#183747', 'h, h′, b₀, b₂, b′₀, b′₂  (54 vertices)'), ('#3D8A55', 'triangle fibres  (54)'),
                                ('#7C55A5', 'b₁, b′₁  (18)')]):
    ax.scatter(7.15, 3.2 - .42 * i, s=110, c=col, zorder=5)
    ax.text(7.45, 3.2 - .42 * i, txt, ha='left', va='center', fontsize=10, color=INK)
ax.text(7.0, 3.62, 'Node colours: the orbits of Aut(G)', ha='left', va='center', fontsize=10, color=MUTED)
ax.set_xlim(-6.6, 10.2); ax.set_ylim(-5.95, 4.55)
fig.suptitle('The Z₃ × Z₃ voltage graph behind the 126 vertices', fontsize=21, color=INK, y=.975)
fig.text(.5, .905, r'Node u stands for the fibre $\{(u,x):x\in\mathbb{Z}_3^2\}$. An arrow $u\to v$ with label $g$ means '
         r'$(u,x)\sim(v,x+g)$; grey edges have voltage 0.', ha='center', fontsize=11.5, color=MUTED)
fig.text(.5, .035, r'Triangles $a_l\to a_m$ carry $(m-l)(0,2)$; edges $a_l\to b_j$ carry $l\,w_j$ with '
         r'$w=(2,0),(1,1),(1,0)$. The right half repeats the voltages of the left half.', ha='center', fontsize=10.5,
         color=MUTED)
fig.subplots_adjust(left=.01, right=.99, bottom=.06, top=.88)
save(fig, 'n63_126_voltage')

(FIG / 'drawing-check.json').write_text(json.dumps({
    'vertices': n, 'edges': len(drawn), 'exact_edge_set_match': drawn == actual, 'edge_classes': counts,
    'rotation_checked_as_automorphism_of_order_3_and_as_rotation_by_120_degrees': True,
    'reflection_checked_as_automorphism_and_mirror': True,
    'minimum_edge_vertex_clearance': {k: round(c, 6) for k, c in clear.items()},
    'coordinates': {str(v): [round(p[0], 6), round(p[1], 6)] for v, p in pos.items()}}, indent=1) + '\n')
print(f'Saved n63_126_symmetry and n63_126_voltage (PNG, SVG, PDF); {len(drawn)} edges, '
      f'clearance {clear["small"]:.4f} (small dots), {clear["large"]:.4f} (large dots).')
