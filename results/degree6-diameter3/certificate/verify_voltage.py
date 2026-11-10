#!/usr/bin/env python3
"""Second finite certificate: modular reachability in the voltage graph (standard library only).

For every ordered pair of base vertices (u, v), compute the set of voltage sums of base walks
u -> v of length at most 3 (each base edge can be traversed in either direction; the reverse
direction carries the negated voltage).  The cover vertex (v, y) is within distance 3 of
(u, 0) iff y is such a sum, so diameter <= 3 iff all 14 * 14 sets equal Z_3 x Z_3.
"""
import construct


def main():
    darts = {u: [] for u in range(construct.K)}
    for u, v, gs in construct.BASE_EDGES:
        for g in gs:
            darts[u].append((v, g))
            darts[v].append((u, ((-g[0]) % 3, (-g[1]) % 3)))
    full = set(construct.N)
    for u in range(construct.K):
        reach = {(u, (0, 0))}
        frontier = set(reach)
        for _ in range(3):
            nxt = set()
            for (w, x) in frontier:
                for (v, g) in darts[w]:
                    nxt.add((v, ((x[0] + g[0]) % 3, (x[1] + g[1]) % 3)))
            frontier = nxt - reach
            reach |= nxt
        for v in range(construct.K):
            got = {x for (w, x) in reach if w == v}
            assert got == full, f'base pair ({u},{v}) misses {sorted(full - got)}'
    print(f"PASS: all {construct.K ** 2} ordered base pairs reach every voltage within 3 steps")


if __name__ == '__main__':
    main()
