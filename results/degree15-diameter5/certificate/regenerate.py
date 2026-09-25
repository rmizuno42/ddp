"""Regenerate the 100,000-vertex edge list using only Python's standard library.

Vertices are u*5**5 + x0 + 5*x1 + 25*x2 + 125*x3 + 625*x4.
Output: header 'n m', then each undirected edge once, u < v, in sorted order.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT / 'regenerated.edges')
    args = parser.parse_args()
    d = json.loads((ROOT / 'chart.json').read_text())
    q, dim = int(d['q']), int(d['s'])
    A, vectors = d['matrices'], d['vectors']
    C = [list(map(int, line.split())) for line in (ROOT / 'controller.adj').read_text().splitlines() if line.strip()]
    if (q, dim, len(C)) != (5, 5, 32):
        raise ValueError('This generator is for the certified q=5, s=5, nC=32 instance.')
    inv = (1, 0, 2)
    for u, row in enumerate(C):
        if len(row) != 3 or len(set(row)) != 3 or u in row:
            raise ValueError('The controller must be simple and cubic.')
        for t, v in enumerate(row):
            if not 0 <= v < len(C) or C[v][inv[t]] != u:
                raise ValueError('Invalid inverse-labeled controller.')
    size = q ** dim
    powers = [q ** i for i in range(dim)]
    relations = [[None] * size for _ in range(3)]
    for xcode in range(size):
        x = [(xcode // p) % q for p in powers]
        for t in range(3):
            ax = [sum(A[t][i][j] * x[j] for j in range(dim)) % q for i in range(dim)]
            relations[t][xcode] = [sum(((ax[i] + lam * vectors[t][i]) % q) * powers[i] for i in range(dim)) for lam in range(q)]
    n, expected_edges = len(C) * size, len(C) * size * 15 // 2
    written = 0
    with args.output.open('w', buffering=1024 * 1024) as out:
        out.write(f'{n} {expected_edges}\n')
        for u, row in enumerate(C):
            for xcode in range(size):
                ucode = u * size + xcode
                neighbors = sorted(row[t] * size + y for t in range(3) for y in relations[t][xcode])
                if len(set(neighbors)) != 15 or ucode in neighbors:
                    raise ValueError('Unexpected duplicate neighbor or loop.')
                upper = [v for v in neighbors if v > ucode]
                out.write(''.join(f'{ucode} {v}\n' for v in upper))
                written += len(upper)
    if written != expected_edges:
        raise ValueError(f'Wrote {written} edges, expected {expected_edges}.')
    digest = hashlib.sha256(args.output.read_bytes()).hexdigest()
    expected = json.loads((ROOT / 'graph_metadata.json').read_text())['sha256']
    result = {'vertices': n, 'edges': written, 'sha256': digest, 'matches_reference': digest == expected}
    print(json.dumps(result, indent=2))
    if digest != expected:
        raise ValueError('The regenerated edge file does not match the reference hash.')

if __name__ == '__main__':
    main()
