#!/usr/bin/env python3
"""Second finite certificate: modular reachability in the Z_9 voltage graph (standard library only).

For every ordered pair of base vertices (u, v), compute the set of voltage sums of base walks
u -> v of length at most 3 (edges in either direction, the reverse carrying -a; a loop with
voltage a gives the darts +a and -a).  The cover vertex (v, y) is within distance 3 of (u, 0)
iff y is such a sum, so diameter <= 3 iff all 19 * 19 sets equal Z_9.
"""
import construct


def main():
    M = construct.M
    darts = {u: [] for u in range(construct.K)}
    for u, v, a in construct.BASE_EDGES:
        darts[u].append((v, a % M))
        darts[v].append((u, (-a) % M))
    for u, a in construct.LOOPS:
        darts[u].append((u, a % M))
        darts[u].append((u, (-a) % M))
    full = set(range(M))
    for u in range(construct.K):
        reach = {(u, 0)}
        frontier = set(reach)
        for _ in range(3):
            nxt = set()
            for (w, x) in frontier:
                for (v, a) in darts[w]:
                    nxt.add((v, (x + a) % M))
            frontier = nxt - reach
            reach |= nxt
        for v in range(construct.K):
            got = {x for (w, x) in reach if w == v}
            assert got == full, f'base pair ({u},{v}) misses {sorted(full - got)}'
    print(f"PASS: all {construct.K ** 2} ordered base pairs reach every voltage within 3 steps")


if __name__ == '__main__':
    main()
