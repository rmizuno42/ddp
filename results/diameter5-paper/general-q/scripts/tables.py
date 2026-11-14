"""Write the GF(q) tables read by chartsearch.c.

Usage: python3 tables.py q OUTFILE
"""
import sys
from gfq import GF


def main():
    q, out = int(sys.argv[1]), sys.argv[2]
    F = GF(q)
    with open(out, 'w') as fh:
        fh.write(f'{q}\n')
        for row in F.add:
            fh.write(' '.join(map(str, row)) + '\n')
        for row in F.mul:
            fh.write(' '.join(map(str, row)) + '\n')
        fh.write(' '.join(map(str, F.neg)) + '\n')
        fh.write(' '.join(str(x if x is not None else 0) for x in F.inv) + '\n')


if __name__ == '__main__':
    main()
