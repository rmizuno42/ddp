#!/usr/bin/env python3
"""verify_graphs_identical.py

Verify that user-generated graphs (output of
    <package>/scripts/12_5_34992/generate_final_graph.py
    <package>/scripts/16_5_147456/generate_final_graph.py
) contain exactly the same vertices and edges as the bundled graphs in
    <package>/graphs/12_5_34992/final_graph_edges.tsv.gz
    <package>/graphs/16_5_147456/final_graph_edges.tsv.gz
where <package> is normally route_chart_clean_package, the cleaned runnable
package supplied with the paper. The script only requires that <package>
contain graphs/12_5_34992/ and graphs/16_5_147456/.

This script lives OUTSIDE the package and opens every file read-only.
The package directory is the supplementary material for the paper and is
expected to be present unchanged in the verifier's environment.

Each .tsv.gz file consists of:
    - line 1: header "n m"
    - lines 2..: one undirected edge per line as "u<TAB>v"

The script performs two complementary checks per (12,5) / (16,5) case:

    (A) Body SHA-256.  Skip line 1 of each file and SHA-256 the rest.
        Equal hashes prove the edge lines are byte-for-byte identical
        (same edges in the same order).

    (B) Parsed edge-set equality.  Read every "u<TAB>v" line, normalize each
        edge to (min(u,v), max(u,v)), collect into Python sets, and compare.
        This is independent of header format and line ordering, so it is the
        graph-theoretic equality check.

(A) implies (B), but (B) is included for human readers who want a check that
does not depend on file-format details.

Standard library only; runs on Python 3.7+.

Usage:
    python3 verify_graphs_identical.py \\
        --package /path/to/route_chart_clean_package \\
        --gen12   /path/to/generated/12/final_graph_edges.tsv.gz \\
        --gen16   /path/to/generated/16/final_graph_edges.tsv.gz

Exit code: 0 iff both cases are IDENTICAL GRAPH; otherwise 1
(2 if a path is missing or invalid).
"""
import argparse
import gzip
import hashlib
import sys
from pathlib import Path


def body_sha256(path: Path) -> str:
    """SHA-256 over every line of the gzipped TSV except the first (header)."""
    h = hashlib.sha256()
    with gzip.open(path, "rt") as f:
        f.readline()  # discard header line
        for line in f:
            h.update(line.encode("utf-8"))
    return h.hexdigest()


def parse_edges(path: Path):
    """Return (vertex_set, edge_set) parsed from the gzipped TSV.

    Edges are stored as canonical pairs (min(u,v), max(u,v)) so the set
    equality test is independent of edge orientation in the file.
    """
    verts = set()
    edges = set()
    with gzip.open(path, "rt") as f:
        f.readline()  # discard header line
        for line in f:
            a, b = line.rstrip("\n").split("\t")
            u, v = int(a), int(b)
            if u > v:
                u, v = v, u
            verts.add(u)
            verts.add(v)
            edges.add((u, v))
    return verts, edges


def check_case(name: str, n_expect: int, m_expect: int,
               bundled: Path, generated: Path) -> bool:
    print(f"=== {name}   (expected |V|={n_expect}, |E|={m_expect}) ===")
    print(f"  bundled  : {bundled}")
    print(f"  generated: {generated}")

    sha_b = body_sha256(bundled)
    sha_g = body_sha256(generated)
    sha_ok = sha_b == sha_g
    print(f"  body SHA-256 bundled    = {sha_b}")
    print(f"  body SHA-256 generated  = {sha_g}")
    print(f"  body SHA-256 match     : {'YES' if sha_ok else 'NO'}")

    vb, eb = parse_edges(bundled)
    vg, eg = parse_edges(generated)
    n_ok = len(vb) == n_expect == len(vg)
    m_ok = len(eb) == m_expect == len(eg)
    v_ok = vb == vg
    e_ok = eb == eg
    print(f"  |V| bundled / generated = {len(vb)} / {len(vg)}")
    print(f"  |E| bundled / generated = {len(eb)} / {len(eg)}")
    print(f"  vertex set equal       : {'YES' if v_ok else 'NO'}")
    print(f"  edge set equal         : {'YES' if e_ok else 'NO'}")

    ok = sha_ok and v_ok and e_ok and n_ok and m_ok
    print(f"  --> {'IDENTICAL GRAPH' if ok else 'MISMATCH'}")
    print()
    return ok


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Compare user-generated graphs against the bundled graphs "
                    "in the cleaned runnable package (read-only).")
    ap.add_argument(
        "--package", type=Path, required=True,
        help="Path to the route_chart_clean_package directory "
             "(must contain graphs/12_5_34992/ and graphs/16_5_147456/).")
    ap.add_argument(
        "--gen12", type=Path, required=True,
        help="Path to the user-generated (12,5) edge list (.tsv.gz).")
    ap.add_argument(
        "--gen16", type=Path, required=True,
        help="Path to the user-generated (16,5) edge list (.tsv.gz).")
    args = ap.parse_args()

    pkg = args.package.resolve()
    if not pkg.is_dir():
        print(f"ERROR: --package is not a directory: {pkg}", file=sys.stderr)
        return 2

    bundled12 = pkg / "graphs" / "12_5_34992" / "final_graph_edges.tsv.gz"
    bundled16 = pkg / "graphs" / "16_5_147456" / "final_graph_edges.tsv.gz"

    for label, p in [("bundled (12,5)", bundled12),
                     ("bundled (16,5)", bundled16),
                     ("generated (12,5)", args.gen12),
                     ("generated (16,5)", args.gen16)]:
        if not p.is_file():
            print(f"ERROR: {label} file not found: {p}", file=sys.stderr)
            return 2

    cases = [
        ("(12,5)",   34992,  209952, bundled12, args.gen12),
        ("(16,5)", 147456, 1179648, bundled16, args.gen16),
    ]
    all_ok = True
    for name, n, m, bundled, generated in cases:
        all_ok &= check_case(name, n, m, bundled, generated)

    print("ALL GRAPHS IDENTICAL." if all_ok else "MISMATCH DETECTED.")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
