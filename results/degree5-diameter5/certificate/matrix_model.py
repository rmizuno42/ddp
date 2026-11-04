#!/usr/bin/env python3
"""Construct a 660-vertex (5,5)-graph directly from projective matrices.

No input graph, search, third-party library, or network access is required.
Projective matrices are normalized by their first nonzero entry.
"""
from __future__ import annotations

P = 11
Matrix = tuple[int, int, int, int]
I: Matrix = (1, 0, 0, 1)
H: Matrix = (1, 0, 0, 10)
T: Matrix = (0, 1, 10, 0)
S: tuple[Matrix, ...] = (H, (1, 1, 4, 10), (1, 5, 3, 10),
                         (0, 1, 3, 8), (1, 4, 1, 0))
NAMES = "habrR"
SQUARES = {1, 3, 4, 5, 9}
NONSQUARES = {2, 6, 7, 8, 10}


def normalize(m: Matrix) -> Matrix:
    v = tuple(z % P for z in m)
    first = next((z for z in v if z), None)
    if first is None:
        raise ValueError("The zero matrix has no projective class.")
    scale = pow(first, -1, P)
    return tuple(z * scale % P for z in v)  # type: ignore[return-value]


def mul(x: Matrix, y: Matrix) -> Matrix:
    a, b, c, d = x
    e, f, g, h = y
    return normalize((a * e + b * g, a * f + b * h,
                      c * e + d * g, c * f + d * h))


def det(x: Matrix) -> int:
    a, b, c, d = x
    return (a * d - b * c) % P


def inv(x: Matrix) -> Matrix:
    a, b, c, d = x
    if det(x) == 0:
        raise ValueError("A singular matrix is not a group element.")
    return normalize((d, -b, -c, a))


def projective_group() -> list[Matrix]:
    # First nonzero entry is 1. Invertibility excludes the other possible forms.
    first = [(1, b, c, d) for b in range(P) for c in range(P)
             for d in range(P) if (d - b * c) % P]
    second = [(0, 1, c, d) for c in range(1, P) for d in range(P)]
    return sorted(first + second)
