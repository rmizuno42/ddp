#!/usr/bin/env python3
"""Check the edge files linked by the 2026-10-23 table snapshot."""

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
from urllib.request import urlopen


ROOT = Path(__file__).resolve().parents[2]
BASE = "https://web.mat.upc.edu/francesc.comellas/delta-d/desc_g/"
CASES = [
    {
        "degree": 14,
        "repository_order": 88452,
        "record_order": 94186,
        "record_sha256": "7e9d7e71438d787241d3ea741e7c5593332bfe0dc56200d08554558f90a88438",
        "former_sha256": "1930eb09c2513db2b20c03d47af2ced0e59a654bba10c977481ffbf3e3c1910c",
    },
    {
        "degree": 15,
        "repository_order": 100000,
        "record_order": 100132,
        "record_sha256": "d325c23b85a13c8e887331a9c3cd3b4f93bde15643cfb0ec295cda1a48e1cbbc",
        "former_sha256": "87cba117abdf2a464a8af51d65e03ec2ee8963bfeeb08769381cf9800ccf3c2f",
    },
]


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def read_graph(data):
    lines = iter(data.decode("ascii").splitlines())
    n, expected_m = map(int, next(lines).lstrip("#").split())
    if n <= 0 or expected_m < 0:
        raise ValueError("Invalid graph header")
    edges = set()
    degrees = [0] * n
    for line in lines:
        if not line.strip() or line.startswith("#"):
            continue
        u, v = sorted(map(int, line.split()))
        if not 0 <= u < v < n or (u, v) in edges:
            raise ValueError("Invalid, repeated, or loop edge")
        edges.add((u, v))
        degrees[u] += 1
        degrees[v] += 1
    if len(edges) != expected_m or any(d == 0 for d in degrees):
        raise ValueError("Edge count or vertex support differs from the header")
    normalized = hashlib.sha256(f"{n} {len(edges)}\n".encode("ascii"))
    for u, v in sorted(edges):
        normalized.update(f"{u} {v}\n".encode("ascii"))
    return edges, {
        "vertices": n,
        "edges": len(edges),
        "simple": True,
        "degree_histogram": dict(sorted(Counter(degrees).items())),
        "maximum_degree": max(degrees),
        "file_sha256": sha256(data),
        "normalized_edge_sha256": normalized.hexdigest(),
    }


def get_file(filename, expected_sha256, input_dir):
    url = BASE + "adjacencies/adjD5/" + filename
    if input_dir is None:
        with urlopen(url, timeout=60) as response:
            data = response.read()
    else:
        data = (input_dir / filename).read_bytes()
    if sha256(data) != expected_sha256:
        raise ValueError(f"File differs from the dated snapshot: {url}")
    return data, url


def compare(case, input_dir):
    degree = case["degree"]
    n = case["repository_order"]
    filename = f"graph_d{degree}_D5_n{n}.edges"
    repository_path = f"results/degree{degree}-diameter5/certificate/{filename}"
    original, original_info = read_graph((ROOT / repository_path).read_bytes())
    former_data, former_url = get_file(filename, case["former_sha256"], input_dir)
    former, former_info = read_graph(former_data)
    if original_info["vertices"] != n or former_info["vertices"] != n or former != original:
        raise ValueError("The published former graph does not match the repository")
    record_filename = f"N{degree}_D5_{case['record_order']}_FINAL.edges"
    record_data, record_url = get_file(record_filename, case["record_sha256"], input_dir)
    record, record_info = read_graph(record_data)
    if record_info["vertices"] != case["record_order"] or record_info["maximum_degree"] != degree:
        raise ValueError("Record order or maximum degree differs from the table")
    return {
        "degree": degree,
        "reported_diameter": 5,
        "detail_url": BASE + f"desc_g5.html#{degree}5",
        "record_name": f"SamSar_{case['record_order']}",
        "record_authors": ["Sami Hani Badaoui", "Sarah Ellen Mary Vaughan"],
        "communicated_on": "2026-10-22",
        "repository_graph": {"path": repository_path, **original_info},
        "published_former_graph": {"url": former_url, **former_info},
        "published_record_graph": {"url": record_url, **record_info},
        "order_increase_over_repository": record_info["vertices"] - n,
        "former_graph_equals_repository_with_same_labels": True,
        "record_edges_equal_to_repository_edges_with_same_integer_labels": len(record & original),
        "relationship_basis": "explicit attribution in the published detail page, whose former graph matches the repository",
        "vertex_correspondence_to_record_reconstructed": False,
        "independent_record_diameter_verification": False,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-dir", type=Path, help="Read the four downloaded files from this directory")
    parser.add_argument("--output", type=Path, default=Path(__file__).with_name("comparison.json"))
    args = parser.parse_args()
    result = {
        "accessed_on": "2026-10-23",
        "method": "literal undirected edge-set comparison; # prefixes on headers are ignored",
        "scope": "checks identity of the former graphs and record orders/degrees; the detail-page attribution is reviewed separately; no relabeling map or diameter proof for the external records",
        "program_sha256": sha256(Path(__file__).read_bytes()),
        "comparisons": [compare(case, args.input_dir) for case in CASES],
    }
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
