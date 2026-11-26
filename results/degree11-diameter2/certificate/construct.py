"""Generate the 108-vertex undirected graph. Python 3, standard library."""
from pathlib import Path
import sys

# For each fixed vertex, list only its higher-numbered fixed neighbors.
FIXED_FORWARD = (
    (1, 2, 3, 4), (5, 10, 12), (6, 13, 15), (7, 9, 16), (8, 11, 14),
    (6, 7, 8), (7, 11), (14,), (9, 16), (10, 13), (11, 15), (12,),
    (13, 16), (14,), (15,), (16,), (),
)
# Fixed vertices attached to every point of each successive center fibre.
ANCHORS = ((5, 13, 15), (6, 9, 16), (7, 10, 12), (1, 14), (2, 8), (3, 11), (0, 4))
CENTER_EDGES = ((0, 5), (0, 6), (1, 3), (1, 6), (2, 4), (2, 6), (3, 4), (3, 5), (4, 5))
# Base shifts from center i into the two members of an outer pair.
COLUMNS = ((0, 1), (3, 5), (2, 6), (1, 0), (5, 3), (6, 2), (4, 4))


def vertex(fibre, x):
    return 17 + 7 * fibre + x % 7


def graph():
    edges = [(u, v) for u, neighbors in enumerate(FIXED_FORWARD) for v in neighbors]
    for x in range(7):
        for i, anchors in enumerate(ANCHORS):
            edges.extend((p, vertex(i, x)) for p in anchors)
        edges.extend((vertex(i, x), vertex(j, x)) for i, j in CENTER_EDGES)
        for r, scale in enumerate((1, 2, 4)):
            a = 7 + 2 * r
            for i, (first, second) in enumerate(COLUMNS):
                edges.append((vertex(i, x), vertex(a, x + scale * first)))
                edges.append((vertex(i, x), vertex(a + 1, x + scale * second)))
            edges.extend((vertex(a, x), vertex(a + 1, x + d)) for d in (0, 3, 5, 6))
    assert all(0 <= u < v < 108 for u, v in edges)
    assert len(edges) == len(set(edges)) == 594
    return sorted(edges)


if __name__ == "__main__":
    output = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("regenerated.edges")
    output.write_bytes(b"108 594\n" + "".join(f"{u} {v}\n" for u, v in graph()).encode("ascii"))
