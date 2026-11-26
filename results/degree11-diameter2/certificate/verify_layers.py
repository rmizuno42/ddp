"""All-source BFS by expanding bit-set frontiers; no graph library."""
from collections import Counter
from pathlib import Path
import sys


def distance_matrix(edge_file):
    n = 108
    adj = [0] * n
    for index, row in enumerate(Path(edge_file).read_text(encoding="ascii").splitlines(), 1):
        u, v = map(int, row.split())
        if not (0 <= u < n and 0 <= v < n and u != v) or adj[u] & (1 << v):
            raise ValueError(f"Invalid or repeated edge on line {index}")
        adj[u] |= 1 << v
        adj[v] |= 1 << u
    degrees = Counter(row.bit_count() for row in adj)
    assert degrees == {11: n}, degrees
    rows = []
    for source in range(n):
        distances = bytearray([255]) * n
        frontier = visited = 1 << source
        depth = 0
        while frontier:
            following = 0
            while frontier:
                bit = frontier & -frontier
                u = bit.bit_length() - 1
                distances[u] = depth
                following |= adj[u]
                frontier ^= bit
            frontier = following & ~visited
            visited |= frontier
            depth += 1
        assert 255 not in distances
        rows.append(distances)
    pairs = Counter(rows[u][v] for u in range(n) for v in range(u + 1, n))
    assert all(rows[u][v] == rows[v][u] for u in range(n) for v in range(n))
    assert pairs == {1: 594, 2: 5184}, pairs
    print(f"vertices={n} degree=11 edges=594 diameter={max(pairs)} unordered_distances={dict(sorted(pairs.items()))}")
    return b"".join(rows)


if __name__ == "__main__":
    matrix = distance_matrix(sys.argv[1])
    if len(sys.argv) > 2:
        Path(sys.argv[2]).write_bytes(matrix)
