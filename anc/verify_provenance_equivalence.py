#!/usr/bin/env python3
"""Check 0 (provenance equivalence).

Confirm that the cleaned, runnable package verifies *exactly* the construction
recorded in the verified (provenance) package, even though the two packages use
different file formats and different verifier code.

For each parameter set this checks two things:

  * Certificate equivalence (semantic). The construction data recovered from the
    clean JSON certificate (base voltages and the GF(q)^5 chart matrices/vectors)
    is compared, as data structures, against the same data recovered from the
    original provenance certificate text files. The comparison is semantic, not
    byte-for-byte, because the clean package deliberately uses a single unified
    JSON format whereas the provenance files preserve the original text layout.

  * Graph equivalence (content). The bundled edge list in the clean package has
    the same *uncompressed* content (SHA-256) as the one in the provenance
    package. This is independent of gzip metadata.

Usage:
    python3 verify_provenance_equivalence.py [--clean DIR] [--provenance DIR]

Defaults assume both package directories sit next to this script.
Exit status is 0 on success and 1 on any mismatch.
"""
import argparse
import gzip
import hashlib
import json
import os
import re
import sys

PARAMS = ["12_5_34992", "16_5_147456"]


# --- parsers for the original provenance certificate text formats -----------
def parse_controller_txt(path):
    """Provenance base file: 'edge_id u v voltage_mod_4 voltage_mod_6' per line."""
    rows = []
    with open(path) as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            eid, u, v, m4, m6 = map(int, line.split())
            rows.append((eid, (u, v, m4, m6)))
    rows.sort()
    return [edge for _, edge in rows]


def parse_gf3_txt(path):
    """Provenance GF(3) chart: 'SYMBOL k' / 'A' + 5 rows / 'b' + 1 row, repeated."""
    A, B, cur, mode = {}, {}, None, None
    with open(path) as fh:
        for line in fh:
            s = line.rstrip("\n")
            if s.startswith("SYMBOL"):
                cur = int(s.split()[1])
            elif s == "A":
                mode, A[cur] = "A", []
            elif s == "b":
                mode = "b"
            elif s.strip() and re.fullmatch(r"[0-9 ]+", s):
                row = list(map(int, s.split()))
                if mode == "A":
                    A[cur].append(row)
                else:
                    B[cur] = row
    return [A[k] for k in sorted(A)], [B[k] for k in sorted(B)]


def parse_gf4_txt(path):
    """Provenance GF(4) chart: 'A_list:' + one matrix per line, 'b_list:' + one vector per line."""
    A, b, mode = [], [], None
    with open(path) as fh:
        for line in fh:
            s = line.strip()
            if s.startswith("A_list"):
                mode = "A"
                continue
            if s.startswith("b_list"):
                mode = "b"
                continue
            if s.startswith("["):
                val = json.loads(s)
                (A if mode == "A" else b).append(val)
    return A, b


def provenance_certificate(prov_pkg, param):
    base = parse_controller_txt(
        os.path.join(prov_pkg, "certificates", param, "controller_c4xc6_multibase.txt"))
    if param.startswith("12_5"):
        A, B = parse_gf3_txt(os.path.join(prov_pkg, "certificates", param, "gf3_s5_universal.txt"))
    else:
        A, B = parse_gf4_txt(os.path.join(prov_pkg, "certificates", param, "gf4_s5_universal.txt"))
    return list(base), A, B


def clean_certificate(clean_pkg, param):
    with open(os.path.join(clean_pkg, "certificates", param, "certificate.json")) as fh:
        cert = json.load(fh)
    base = [tuple(e) for e in cert["base_multigraph"]["edges"]]
    return base, cert["chart"]["A"], cert["chart"]["b"]


def content_sha256(path):
    """SHA-256 of the uncompressed bytes of a .gz file (gzip metadata ignored)."""
    with gzip.open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    ap = argparse.ArgumentParser(description="Check that the clean package matches the provenance construction.")
    ap.add_argument("--clean", default=os.path.join(here, "route_chart_clean_package"),
                    help="Path to the cleaned, runnable package.")
    ap.add_argument("--provenance", default=os.path.join(here, "route_chart_verified_graphs_package"),
                    help="Path to the verified (provenance) package.")
    args = ap.parse_args()

    all_ok = True
    for param in PARAMS:
        prov_base, prov_A, prov_B = provenance_certificate(args.provenance, param)
        clean_base, clean_A, clean_B = clean_certificate(args.clean, param)
        cert_ok = (list(prov_base) == list(clean_base)) and (prov_A == clean_A) and (prov_B == clean_B)

        clean_graph = os.path.join(args.clean, "graphs", param, "final_graph_edges.tsv.gz")
        prov_graph = os.path.join(args.provenance, "graphs", param, "final_graph_edges.tsv.gz")
        h_clean, h_prov = content_sha256(clean_graph), content_sha256(prov_graph)
        graph_ok = (h_clean == h_prov)

        all_ok = all_ok and cert_ok and graph_ok
        print(f"[{param}] certificate (semantic): {'OK' if cert_ok else 'MISMATCH'}")
        print(f"[{param}] graph content SHA-256 : {'OK' if graph_ok else 'MISMATCH'}  ({h_clean[:16]}...)")

    print()
    if all_ok:
        print("PASS: the clean package verifies the same construction as the provenance package.")
        sys.exit(0)
    print("FAIL: clean and provenance disagree.")
    sys.exit(1)


if __name__ == "__main__":
    main()
