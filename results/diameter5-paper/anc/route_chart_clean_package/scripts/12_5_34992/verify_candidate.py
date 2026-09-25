"""(12,5) construction-certificate verifier.

Re-checks, from scratch and with no external input, the two facts the (12,5)
route-chart construction relies on:

  * Controller -- the 144-vertex voltage lift of a 6-vertex 4-regular base
    multigraph over the group H = C4 x C6 is a simple, 4-regular, connected
    graph in which every ordered pair of vertices is joined by an exact
    length-5 nonbacktracking (NB) walk.
  * Fiber chart -- over GF(3)^5, for every reduced word of length 5 in the
    symbols {a, a^-1, b, b^-1} the associated 5x5 controllability matrix is
    nonsingular (full rank 5).

Together these give the lifted graph V(controller) x GF(3)^5 degree 4*3 = 12
and diameter <= 5.

Run as a script to print the OK report. The helper functions and chart data
(build_controller, euler_2factor_coloring, orient_two_factors, A, B, mv, Q)
are imported by generate_final_graph.py, so their behavior must not change.
"""
from collections import deque, defaultdict
import json
import os

# --- base multigraph and voltage group ---
MOD4, MOD6 = 4, 6        # the two cyclic factors of the voltage group H = C4 x C6
NBASE = 6                # number of base vertices
S = 5                    # target walk length (= target diameter)
HSIZE = MOD4 * MOD6      # |H| = 24
Q = 3                    # the fiber field is GF(Q) = GF(3)

# Base edges as (u, v, voltage mod 4, voltage mod 6). Parallel edges are allowed
# and are distinguished by their position (edge id) in this list. Reference copy;
# checked at load time against certificates/<param>/certificate.json (see below).
EDGE_DATA_HARDCODED = [(0, 2, 1, 0), (0, 3, 2, 4), (0, 4, 2, 0), (0, 4, 2, 5),
                       (1, 2, 1, 2), (1, 3, 3, 5), (1, 5, 1, 1), (1, 5, 1, 0),
                       (2, 4, 2, 2), (2, 5, 1, 5), (3, 4, 1, 5), (3, 5, 3, 1)]


def gid(x, y):
    """Index in 0..HSIZE-1 of the group element (x mod 4, y mod 6)."""
    return (x % MOD4) * MOD6 + (y % MOD6)


# ---------- controller ----------

def verify_base_voltage_coverage():
    """Assert that, on the base graph, the length-5 NB walks between every
    ordered pair (i, j) realize *every* voltage in H.

    If they do, then in the lift every (i, h) reaches every (j, h') by a
    length-5 NB walk: pick a base walk whose accumulated voltage equals
    h' - h. This is exactly the coverage the controller needs.
    """
    # Directed base adjacency: each base edge contributes its voltage in the
    # forward direction and the negated voltage in the reverse direction.
    adj = [[] for _ in range(NBASE)]
    for eid, (u, v, x, y) in enumerate(EDGE_DATA):
        adj[u].append((v, eid, x % MOD4, y % MOD6))
        adj[v].append((u, eid, (-x) % MOD4, (-y) % MOD6))

    # sums[i][j] = set of voltage-sum indices reached by length-5 NB walks i -> j.
    sums = [[set() for _ in range(NBASE)] for __ in range(NBASE)]

    def rec(start, u, last_edge, depth, x, y):
        # Walk forward accumulating the voltage sum (x, y); record it at depth S.
        if depth == S:
            sums[start][u].add(gid(x, y))
            return
        for v, eid, dx, dy in adj[u]:
            if eid != last_edge:                 # nonbacktracking: don't reuse the last edge
                rec(start, v, eid, depth + 1, x + dx, y + dy)

    for s in range(NBASE):
        rec(s, s, -1, 0, 0, 0)

    # Every ordered pair must cover all HSIZE group elements.
    bad = []
    for i in range(NBASE):
        for j in range(NBASE):
            missing = set(range(HSIZE)) - sums[i][j]
            if missing:
                bad.append((i, j, sorted(missing), len(sums[i][j])))
    assert not bad, f'base voltage coverage failed: {bad[:5]}'


def build_controller():
    """Build the voltage lift of the base graph over H = C4 x C6.

    Vertex (base u, group element g) is encoded as the integer u*HSIZE + g.
    For each base edge (u, v) with voltage gamma and each h in H, add the
    lifted edge (u, h) -- (v, h + gamma).

    Returns (adj, edges):
      edges[i] = (a, b, base_edge_id) with a < b,
      adj[w]   = list of (neighbor, edge_index).
    Asserts the lift is simple, 4-regular and connected.
    """
    edges = []
    seen = set()
    for beid, (u, v, xv, yv) in enumerate(EDGE_DATA):
        for x in range(MOD4):
            for y in range(MOD6):
                a = u * HSIZE + gid(x, y)
                b = v * HSIZE + gid(x + xv, y + yv)
                key = (a, b) if a < b else (b, a)
                if key in seen:                  # simple graph: no repeated edge
                    raise AssertionError(f'duplicate controller edge {key}')
                seen.add(key)
                edges.append((key[0], key[1], beid))

    n = NBASE * HSIZE                            # 144 controller vertices
    adj = [[] for _ in range(n)]
    for eid, (u, v, beid) in enumerate(edges):
        adj[u].append((v, eid))
        adj[v].append((u, eid))

    # 4-regular?
    assert all(len(a) == 4 for a in adj), sorted(set(len(a) for a in adj))

    # connected? (BFS from vertex 0)
    q = deque([0])
    reached = {0}
    while q:
        u = q.popleft()
        for v, eid in adj[u]:
            if v not in reached:
                reached.add(v)
                q.append(v)
    assert len(reached) == n, f'disconnected controller {len(reached)}/{n}'
    return adj, edges


def euler_2factor_coloring(adj, edges):
    """2-color the controller edges so each color class is a 2-factor.

    The controller is 4-regular and connected, hence Eulerian. We walk one
    Euler circuit (Hierholzer's algorithm) and color edges by their parity
    along the circuit. Consecutive edges at any vertex alternate colors, so
    each vertex ends with exactly two edges of each color -- i.e. two 2-factors.

    Returns color: edge_index -> 0/1.
    """
    n = len(adj)
    m = len(edges)
    used = [False] * m
    next_ptr = [0] * n        # next_ptr[u] = next index into adj[u] still to try
    stack = [(0, -1)]         # (vertex, edge arrived by); -1 marks the start
    circuit = []              # vertices in Hierholzer post-order

    while stack:
        u, _arrived_by = stack[-1]
        # Advance past edges out of u that are already used.
        while next_ptr[u] < len(adj[u]) and used[adj[u][next_ptr[u]][1]]:
            next_ptr[u] += 1
        if next_ptr[u] == len(adj[u]):
            circuit.append(stack.pop())          # u exhausted -> commit it
        else:
            v, eid = adj[u][next_ptr[u]]
            used[eid] = True
            stack.append((v, eid))

    # Edge ids in Euler-circuit order (drop the start sentinel's edge).
    order = [e for _, e in reversed(circuit)][1:]
    assert len(order) == m and all(used)

    color = {eid: (k & 1) for k, eid in enumerate(order)}

    # Each vertex must carry two edges of each color.
    deg = [[0, 0] for _ in range(n)]
    for eid, (u, v, _) in enumerate(edges):
        c = color[eid]
        deg[u][c] += 1
        deg[v][c] += 1
    assert all(d == [2, 2] for d in deg)
    return color


def orient_two_factors(adj, edges, color):
    """Orient the cycles of each 2-factor, labeling every arc with a symbol.

    Color 0 becomes symbol a (0 = forward, 1 = a^-1 backward); color 1 becomes
    symbol b (2 = forward, 3 = b^-1 backward). Each color class is a disjoint
    union of cycles; orienting each cycle consistently leaves every vertex with
    exactly one outgoing arc of each of the 4 symbols.

    Returns arc: (u, v) -> symbol in {0, 1, 2, 3}.
    """
    n = len(adj)
    arc = {}
    for c in (0, 1):
        # Adjacency restricted to color-c edges (every vertex has degree 2 here).
        color_adj = [[] for _ in range(n)]
        for eid, (u, v, _) in enumerate(edges):
            if color[eid] == c:
                color_adj[u].append((v, eid))
                color_adj[v].append((u, eid))

        forward, backward = (0, 1) if c == 0 else (2, 3)
        used = set()
        for st in range(n):
            for nxt, e0 in color_adj[st]:
                if e0 in used:
                    continue
                # Walk the cycle st -> nxt -> ..., always leaving each vertex by
                # the edge we did NOT arrive on (degree 2 => the choice is unique).
                cyc = [st]
                u, e = nxt, e0
                while True:
                    used.add(e)
                    cyc.append(u)
                    opts = color_adj[u]
                    v, ne = opts[1] if opts[0][1] == e else opts[0]
                    if v == st:                  # cycle closes back to the start
                        used.add(ne)
                        arc[(u, st)] = forward
                        arc[(st, u)] = backward
                        break
                    u, e = v, ne
                # Orient every edge along the cycle the same way.
                for a, b in zip(cyc[:-1], cyc[1:]):
                    arc[(a, b)] = forward
                    arc[(b, a)] = backward

    # Each vertex has exactly one arc per symbol, and (v,u) is the inverse of (u,v).
    invsym = {0: 1, 1: 0, 2: 3, 3: 2}
    cnt = [defaultdict(int) for _ in range(n)]
    for (u, v), s in arc.items():
        cnt[u][s] += 1
        assert arc[(v, u)] == invsym[s]
    assert all(all(cnt[u][s] == 1 for s in range(4)) for u in range(n))
    return arc


def verify_labeled_nb5(adj, arc):
    """Assert that, using the arc symbols, every ordered pair of controller
    vertices is still joined by an exact length-5 NB walk.

    NB walks correspond to reduced words (no symbol immediately followed by its
    inverse). This re-checks coverage at the labeled level, which is what the
    fiber chart consumes.
    """
    inv = {0: 1, 1: 0, 2: 3, 3: 2}
    n = len(adj)
    bad = []
    for s in range(n):
        reach = set()

        def rec(u, prev, depth, last_sym):
            if depth == S:
                reach.add(u)
                return
            for v, eid in adj[u]:
                if v == prev:
                    continue
                sym = arc[(u, v)]
                assert last_sym is None or sym != inv[last_sym]   # word stays reduced
                rec(v, u, depth + 1, sym)

        rec(s, -1, 0, None)
        if len(reach) != n:
            bad.append((s, n - len(reach)))
    assert not bad, f'NB5 labeled coverage failed: {bad[:5]}'


# ---------- GF(3)^5 fiber chart ----------
# A[s] is the transition matrix and B[s] the control vector for symbol s
# (0 = a, 1 = a^-1, 2 = b, 3 = b^-1). Reference copy; checked at load time against
# certificates/<param>/certificate.json (see below).
A_HARDCODED = [
    [[1, 2, 0, 2, 0], [1, 2, 1, 2, 0], [1, 2, 1, 1, 0], [2, 0, 0, 0, 0], [1, 2, 2, 0, 1]],  # a
    [[0, 0, 0, 2, 0], [2, 2, 1, 2, 0], [2, 1, 0, 0, 0], [0, 1, 2, 0, 0], [1, 0, 1, 0, 1]],  # a^-1
    [[2, 1, 0, 0, 0], [0, 1, 1, 0, 0], [2, 2, 0, 1, 0], [2, 0, 1, 0, 0], [2, 2, 1, 1, 1]],  # b
    [[1, 2, 0, 1, 0], [2, 2, 0, 1, 0], [1, 2, 0, 2, 0], [0, 1, 1, 2, 0], [2, 1, 2, 1, 1]],  # b^-1
]
B_HARDCODED = [[2, 2, 2, 0, 0], [0, 1, 0, 0, 1], [2, 1, 2, 0, 2], [1, 0, 1, 0, 2]]
SINV = {0: 1, 1: 0, 2: 3, 3: 2}   # symbol -> its inverse


# --- Load the construction data from the certificate -------------------------
# verify_candidate.py and generate_final_graph.py operate on the data read here
# from certificates/<param>/certificate.json. The *_HARDCODED reference copies
# above are retained only as a guard: the assertions below fail loudly if the
# certificate is ever edited to disagree with them, so the checked construction
# cannot silently change. Because the equality is asserted, the values used
# downstream are identical to the reference copies.
def load_certificate(path=None):
    """Read (edge_data, A, b) from the JSON certificate for this parameter set.

    edge_data is a list of (u, v, voltage_mod_4, voltage_mod_6) tuples; A is the
    list of per-symbol 5x5 transition matrices and b the list of control vectors.
    """
    if path is None:
        here = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(here, os.pardir, os.pardir,
                            'certificates', os.path.basename(here), 'certificate.json')
    with open(path) as fh:
        cert = json.load(fh)
    edge_data = [tuple(e) for e in cert['base_multigraph']['edges']]
    A = cert['chart']['A']
    b = cert['chart']['b']
    return edge_data, A, b


EDGE_DATA, A, B = load_certificate()
assert EDGE_DATA == EDGE_DATA_HARDCODED, 'certificate base data disagrees with the reference copy'
assert A == A_HARDCODED, 'certificate chart matrices disagree with the reference copy'
assert B == B_HARDCODED, 'certificate chart vectors disagree with the reference copy'


def mm(X, Y):
    """Matrix product over GF(3)."""
    return [[sum(X[i][k] * Y[k][j] for k in range(len(Y))) % Q
             for j in range(len(Y[0]))] for i in range(len(X))]


def mv(M, v):
    """Matrix-times-vector over GF(3)."""
    return [sum(M[i][j] * v[j] for j in range(len(v))) % Q for i in range(len(M))]


def rank_cols(cols):
    """Rank over GF(3) of the matrix whose columns are the vectors in `cols`,
    via Gaussian elimination."""
    n = len(cols[0])                          # number of rows
    m = len(cols)                             # number of columns
    M = [list(row) for row in zip(*cols)]     # transpose: column list -> row list
    r = 0
    for c in range(m):
        # Find a pivot in column c at or below the current row r.
        piv = None
        for i in range(r, n):
            if M[i][c] % Q:
                piv = i
                break
        if piv is None:
            continue
        M[r], M[piv] = M[piv], M[r]
        inv = 1 if M[r][c] == 1 else 2        # inverse of the pivot in GF(3) (2*2 = 1)
        M[r] = [(inv * x) % Q for x in M[r]]
        # Eliminate column c from every other row.
        for i in range(n):
            if i != r and M[i][c]:
                f = M[i][c]
                M[i] = [(M[i][j] - f * M[r][j]) % Q for j in range(m)]
        r += 1
        if r == n:
            return r
    return r


def verify_chart():
    """Assert the chart is a valid universal route chart over GF(3)^5:

      * inverse relations A[a^-1] = A[a]^-1 and B[a^-1] = A[a]^-1 B[a]
        (checked via A[p]A[q] = I and A[q]B[p] = B[q] for the inverse pairs);
      * for every length-5 reduced word, the 5 controllability columns are
        linearly independent (rank 5), so the length-5 route reaches all 3^5
        fiber targets.

    Returns (number_of_words, min_rank).
    """
    I = [[1 if i == j else 0 for j in range(5)] for i in range(5)]
    # inverse-pair consistency for (a, a^-1) = (0, 1) and (b, b^-1) = (2, 3)
    for p, q in [(0, 1), (2, 3)]:
        assert mm(A[p], A[q]) == I and mm(A[q], A[p]) == I
        assert mv(A[q], B[p]) == B[q] and mv(A[p], B[q]) == B[p]

    # Enumerate all reduced words of length 5 (no symbol next to its inverse).
    words = []

    def gen(w):
        if len(w) == 5:
            words.append(tuple(w))
            return
        for s in range(4):
            if not w or s != SINV[w[-1]]:
                w.append(s)
                gen(w)
                w.pop()

    gen([])

    min_rank = 99
    for w in words:
        # Build the controllability columns for word w and check full rank.
        suff = I
        cols = []
        for s in reversed(w):
            cols.append(mv(suff, B[s]))
            suff = mm(suff, A[s])
        r = rank_cols(cols)
        min_rank = min(min_rank, r)
        assert r == 5, (w, r)
    return len(words), min_rank


if __name__ == '__main__':
    verify_base_voltage_coverage()
    adj, edges = build_controller()
    color = euler_2factor_coloring(adj, edges)
    arc = orient_two_factors(adj, edges, color)
    verify_labeled_nb5(adj, arc)
    nwords, min_rank = verify_chart()
    print('Base voltage coverage over C4 x C6: OK')
    print('Controller: OK; 144 vertices, simple 4-regular, exact labeled NB length-5 coverage')
    print(f'GF(3)^5 universal chart: OK; {nwords} reduced words checked, min rank {min_rank}; inverse-symbol data verified')
    print('Certificate complete: degree 12, diameter <=5, vertices = 144*3^5 = 34992')
