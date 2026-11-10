#!/usr/bin/env python3
"""Independently measure the November graphs using ordinary, unrestricted BFS.

Reads only the published edge lists and expected parameters from results.json.
No construction formula, graph symmetry, or previously computed distances are used.
"""
import argparse
from collections import Counter, deque
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IDS = {'degree3-diameter7', 'degree5-diameter5', 'degree6-diameter3', 'degree7-diameter3'}


def measure(path):
    lines = path.read_text().splitlines()
    n, declared_edges = map(int, lines[0].split())
    assert n > 0 and declared_edges >= 0
    adjacency = [set() for _ in range(n)]
    edges = set()
    for line in lines[1:]:
        u, v = map(int, line.split())
        assert 0 <= u < n and 0 <= v < n and u != v
        e = tuple(sorted((u, v)))
        assert e not in edges
        edges.add(e)
        adjacency[u].add(v)
        adjacency[v].add(u)
    assert len(edges) == declared_edges
    histogram = Counter()
    eccentricities = Counter()
    diameter, witness = -1, None
    for source in range(n):
        distances = [-1]*n
        distances[source] = 0
        queue = deque([source])
        while queue:
            u = queue.popleft()
            for v in adjacency[u]:
                if distances[v] == -1:
                    distances[v] = distances[u]+1
                    queue.append(v)
        assert min(distances) == 0, 'Disconnected graph'
        eccentricity = max(distances)
        eccentricities[eccentricity] += 1
        if eccentricity > diameter:
            diameter, witness = eccentricity, [source, distances.index(eccentricity)]
        histogram.update(distances)
    degrees = Counter(map(len, adjacency))
    return {'status': 'PASS', 'vertices': n, 'edges': len(edges),
            'simple': True, 'connected': True,
            'maximum_degree': max(degrees), 'degree_histogram': dict(degrees),
            'diameter': diameter, 'diameter_witness': witness,
            'all_sources_checked': n, 'ordered_pairs_checked': n*n,
            'distance_histogram_ordered_pairs': [histogram[d] for d in range(diameter+1)],
            'eccentricity_histogram': dict(eccentricities)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    index = json.loads((ROOT / 'results.json').read_text())
    checked = set()
    for result in index['results']:
        if result['id'] not in IDS:
            continue
        path = ROOT / result['edge_file']
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        assert digest == result['edge_file_sha256']
        measured = measure(path)
        for key in ['vertices', 'edges', 'diameter']:
            assert measured[key] == result[key]
        assert measured['maximum_degree'] == result['degree']
        assert {str(k): v for k, v in measured['degree_histogram'].items()} == result['degree_histogram']
        assert sum(measured['distance_histogram_ordered_pairs']) == result['vertices']**2
        assert hashlib.sha256(path.read_bytes()).hexdigest() == digest
        measured.update({'edge_file': result['edge_file'], 'edge_file_sha256': digest,
                         'verifier_source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                         'method': 'Ordinary all-pairs queue BFS without a depth limit or symmetry reduction.'})
        (args.output / (result['id']+'.json')).write_text(json.dumps(measured, indent=2)+'\n')
        checked.add(result['id'])
        print(f"PASS {result['id']}: n={measured['vertices']}, degree={measured['maximum_degree']}, diameter={measured['diameter']}")
    assert checked == IDS


if __name__ == '__main__':
    main()
