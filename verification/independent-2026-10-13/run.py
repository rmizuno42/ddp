#!/usr/bin/env python3
"""Independently measure the new graph from its edge list, using ordinary BFS.

Requires Python 3.10+ and a C++17 compiler. Does not read construction data,
results.json, the package verifier, or any saved graph verification report.
"""
import argparse
from collections import Counter, deque
import datetime
import gzip
import hashlib
import json
from pathlib import Path
import random
import subprocess
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
EDGE_FILE = ROOT / 'results/degree13-diameter5/certificate/graph.edges.gz'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def floyd_warshall(n, edges):
    """A different shortest-path algorithm for small reference graphs."""
    unreachable = n + 1
    distances = [[unreachable] * n for _ in range(n)]
    degrees = [0] * n
    for u in range(n):
        distances[u][u] = 0
    for u, v in edges:
        distances[u][v] = distances[v][u] = 1
        degrees[u] += 1
        degrees[v] += 1
    for k in range(n):
        for u in range(n):
            for v in range(n):
                distances[u][v] = min(distances[u][v], distances[u][k] + distances[k][v])
    counts = Counter(d for row in distances for d in row if d < unreachable)
    missing = sum(d == unreachable for row in distances for d in row)
    ecc = Counter(max(row) for row in distances if max(row) < unreachable)
    return {
        'vertices': n, 'edges': len(edges), 'simple': True, 'undirected': True,
        'distinct_vertex_labels_in_edges': sum(d > 0 for d in degrees),
        'minimum_degree': min(degrees), 'maximum_degree': max(degrees),
        'degree_histogram': {str(d): c for d, c in Counter(degrees).items()},
        'connected': missing == 0,
        'diameter': max(counts) if missing == 0 else None,
        'all_sources_checked': n, 'ordered_pairs_reached': n * n - missing,
        'unreachable_ordered_pairs': missing,
        'distance_histogram_ordered_pairs': [counts[d] for d in range(max(counts) + 1)],
        'eccentricity_histogram': {str(d): c for d, c in ecc.items()},
    }


def check_implementation(executable, directory):
    fixtures = [
        (1, []),
        (9, [(v, v + 1) for v in range(8)]),  # Diameter eight: no depth-five cutoff.
        (7, [(0, v) for v in range(1, 7)]),
        (12, [(v, v + 1) for v in range(11)] + [(0, 11)]),
        (7, [(0, 1), (1, 2), (0, 2), (3, 4), (4, 5), (3, 5)]),
        (8, [(u, v) for u in range(8) for v in range(u + 1, 8)]),
    ]
    rng = random.Random(20261013)
    for n, probability in [(25, 0.13), (47, 0.08)]:
        fixtures.append((n, [(u, v) for u in range(n) for v in range(u + 1, n)
                             if rng.random() < probability]))
    checks = 0
    path = directory / 'fixture.edges'
    for n, edges in fixtures:
        path.write_text(f'{n} {len(edges)}\n' + ''.join(f'{u} {v}\n' for u, v in edges))
        expected = floyd_warshall(n, edges)
        for threads in [1, 3]:
            actual = json.loads(subprocess.check_output([str(executable), str(path), str(threads)], text=True))
            for key, value in expected.items():
                if actual[key] != value:
                    raise RuntimeError(f'Reference mismatch: n={n}, threads={threads}, {key}')
            checks += 1
    malformed = [
        '', '0 0\n', '3 2\n0 1\n', '2 1\n0 0\n',
        '2 2\n0 1\n1 0\n', '2 1\n0 2\n', '2 1\n0 1 extra\n', '2 1 extra\n0 1\n',
    ]
    for text in malformed:
        path.write_text(text)
        run = subprocess.run([str(executable), str(path), '1'], capture_output=True)
        if run.returncode == 0:
            raise RuntimeError('Malformed input was accepted')
    return {'reference_algorithm': 'Floyd-Warshall', 'reference_graphs': len(fixtures),
            'reference_comparisons_passed': checks, 'tested_thread_counts': [1, 3],
            'malformed_inputs_rejected': len(malformed), 'random_seed': 20261013}


def check_witness(data, source, target):
    rows = data.decode('ascii').splitlines()
    n, _ = map(int, rows[0].split())
    adjacency = [[] for _ in range(n)]
    for row in rows[1:]:
        u, v = map(int, row.split())
        adjacency[u].append(v)
        adjacency[v].append(u)
    parent = [-1] * n
    parent[source] = source
    queue = deque([source])
    while queue and parent[target] == -1:
        u = queue.popleft()
        for v in adjacency[u]:
            if parent[v] == -1:
                parent[v] = u
                queue.append(v)
    if parent[target] == -1:
        raise RuntimeError('Diameter witness is unreachable')
    path = [target]
    while path[-1] != source:
        path.append(parent[path[-1]])
    path.reverse()
    return {'source': source, 'target': target, 'distance': len(path) - 1,
            'shortest_path': path, 'method': 'separate Python queue BFS'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--compiler', default='c++')
    parser.add_argument('--threads', type=int, default=8)
    parser.add_argument('--output', type=Path, default=HERE / 'result.json')
    args = parser.parse_args()
    if not 1 <= args.threads <= 64:
        parser.error('threads must be between 1 and 64')
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.unlink(missing_ok=True)
    compressed = EDGE_FILE.read_bytes()
    data = gzip.decompress(compressed)
    with tempfile.TemporaryDirectory(prefix='ddp-independent-bfs-') as temporary:
        temporary = Path(temporary)
        executable = temporary / 'verify_bfs'
        subprocess.run([args.compiler, '-O3', '-std=c++17', '-pthread', '-Wall', '-Wextra',
                        '-pedantic', str(HERE / 'verify_bfs.cpp'), '-o', str(executable)], check=True)
        implementation_checks = check_implementation(executable, temporary)
        print('PASS: reference graphs and malformed-input checks.', flush=True)
        edges = temporary / 'graph.edges'
        edges.write_bytes(data)
        print('Measuring all-source distances from the edge list, without a depth limit.', flush=True)
        run = subprocess.run([str(executable), str(edges), str(args.threads)],
                             stdout=subprocess.PIPE, text=True, check=True)
        measured = json.loads(run.stdout)
    claimed = {'vertices': 88452, 'degree': 13, 'diameter': 5}
    expected = {'vertices': claimed['vertices'], 'distinct_vertex_labels_in_edges': claimed['vertices'],
                'minimum_degree': claimed['degree'], 'maximum_degree': claimed['degree'],
                'degree_histogram': {'13': claimed['vertices']}, 'diameter': claimed['diameter'],
                'simple': True, 'undirected': True, 'connected': True,
                'all_sources_checked': claimed['vertices'],
                'ordered_pairs_reached': claimed['vertices'] ** 2, 'unreachable_ordered_pairs': 0}
    for key, value in expected.items():
        if measured[key] != value:
            raise RuntimeError(f'Reported claim not confirmed: {key} = {measured[key]}')
    witness = check_witness(data, *measured['largest_finite_distance_witness'])
    if witness['distance'] != measured['diameter']:
        raise RuntimeError('Python witness check disagrees with measured diameter')
    if EDGE_FILE.read_bytes() != compressed:
        raise RuntimeError('Input changed during verification')
    report = {
        'status': 'PASS', 'method': 'independent ordinary queue BFS from every source; no depth limit',
        'claimed_parameters': claimed, 'measured': measured, 'diameter_witness': witness,
        'implementation_checks': implementation_checks,
        'edge_file': str(EDGE_FILE.relative_to(ROOT)),
        'compressed_edge_sha256': digest(compressed), 'uncompressed_edge_sha256': digest(data),
        'verifier_source_sha256': digest((HERE / 'verify_bfs.cpp').read_bytes()),
        'runner_source_sha256': digest(Path(__file__).read_bytes()),
        'compiler': subprocess.check_output([args.compiler, '--version'], text=True).splitlines()[0],
        'threads': args.threads,
        'input_repository_commit': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
        'completed_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    }
    args.output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
