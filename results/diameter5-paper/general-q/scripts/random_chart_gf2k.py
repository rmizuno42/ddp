"""Draw random route charts on GF(2^k)^5 until one is universal.

Usage: python3 random_chart_gf2k.py K SEED OUT.json
The chart is written with "q", "encoding" (GF(2^k) via the primitive modulus)
and the four A_t, b_t; check it with verify_chart.py.
"""
import json
import random
import sys

from gf2k import GF2k

SINV = {0: 1, 1: 0, 2: 3, 3: 2}


def main():
    k, seed, out = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
    F = GF2k(k)
    rng = random.Random(seed)
    from verify_chart import reduced_words, controllability_columns
    words = reduced_words()
    tries = 0
    while True:
        tries += 1
        A0 = [[rng.randrange(F.q) for _ in range(5)] for _ in range(5)]
        A2 = [[rng.randrange(F.q) for _ in range(5)] for _ in range(5)]
        A1, A3 = F.inverse(A0), F.inverse(A2)
        if A1 is None or A3 is None:
            continue
        b0 = [rng.randrange(F.q) for _ in range(5)]
        b2 = [rng.randrange(F.q) for _ in range(5)]
        A, b = [A0, A1, A2, A3], [b0, F.matvec(A1, b0), b2, F.matvec(A3, b2)]
        bad = 0
        for w in words:
            cols = controllability_columns(F, A, b, w)
            if F.rank([list(r) for r in zip(*cols)]) < 5:
                bad += 1
                break
        if not bad:
            break
    chart = {'q': F.q, 'encoding': f'GF(2^{k}) polynomial basis, modulus {F.modulus:#x} (bit i = X^i)',
             'modulus_int': F.modulus, 'seed': seed, 'tries': tries, 'A': A, 'b': b}
    json.dump(chart, open(out, 'w'))
    print(f'GF(2^{k}): universal chart after {tries} random draws -> {out}')


if __name__ == '__main__':
    main()
