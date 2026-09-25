#!/usr/bin/env python3
"""Verify every indexed graph directly from its edge list, and save reports.

Requires Python 3.10+ and a C++17 compiler (c++ by default).
Example: python3 verification/verify_all.py --threads 8 --batch-size 16384
"""
import argparse
import datetime
import gzip
import hashlib
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parent.parent


def sha256(path):
    digest = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(block)
    return digest.hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--compiler', default='c++')
    parser.add_argument('--threads', type=int, default=min(8, os.cpu_count() or 1))
    parser.add_argument('--batch-size', type=int, default=16384)
    parser.add_argument('--output', type=Path, default=ROOT / 'verification' / 'final')
    args = parser.parse_args()
    if not 1 <= args.threads <= 64 or not 1 <= args.batch_size <= 1048576:
        parser.error('threads must be 1..64 and batch-size must be 1..1048576')
    index_path = ROOT / 'results.json'
    index = json.loads(index_path.read_text())
    source = ROOT / 'verification' / 'verify_edges.cpp'
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    # A failed rerun must not leave a stale summary claiming overall success.
    summary_path = output / 'summary.json'
    summary_path.unlink(missing_ok=True)
    reports = []
    with tempfile.TemporaryDirectory(prefix='ddp-final-') as temporary:
        temporary = Path(temporary)
        executable = temporary / 'verify_edges'
        command = [args.compiler, '-O3', '-std=c++17', '-pthread', '-Wall', '-Wextra',
                   '-pedantic', str(source), '-o', str(executable)]
        subprocess.run(command, check=True)
        compiler = subprocess.check_output([args.compiler, '--version'], text=True).splitlines()[0]
        for result in index['results']:
            report_path = output / (result['id'] + '.json')
            report_path.unlink(missing_ok=True)
            edge_path = ROOT / result['edge_file']
            digest = sha256(edge_path)
            if digest != result['edge_file_sha256']:
                raise RuntimeError(f"edge-file checksum mismatch: {result['id']}")
            input_path = edge_path
            if edge_path.suffix == '.gz':
                input_path = temporary / (result['id'] + '.edges')
                with gzip.open(edge_path, 'rb') as src, input_path.open('wb') as dst:
                    shutil.copyfileobj(src, dst)
            has_header = not result['edge_file_format'].startswith('headerless')
            print(f"Checking {result['id']}: {result['vertices']:,} vertices", flush=True)
            completed = subprocess.run(
                [str(executable), str(input_path), str(result['vertices']),
                 str(result['degree']), str(result['diameter']), str(int(has_header)),
                 str(args.threads), str(args.batch_size)],
                stdout=subprocess.PIPE, text=True, check=True)
            report = json.loads(completed.stdout)
            expected = {'status': 'PASS', 'vertices': result['vertices'],
                        'edges': result['edges'], 'maximum_degree': result['degree'],
                        'diameter': result['diameter'], 'simple': True, 'connected': True,
                        'degree_histogram': result['degree_histogram'],
                        'all_sources_checked': result['vertices'],
                        'ordered_pairs_checked': result['vertices'] ** 2,
                        'unreachable_within_claimed_diameter': 0}
            for key, value in expected.items():
                if report[key] != value:
                    raise RuntimeError(f"{result['id']}: {key} mismatch: {report[key]} != {value}")
            if sum(report['distance_histogram_ordered_pairs']) != result['vertices'] ** 2:
                raise RuntimeError('distance histogram does not sum to n squared')
            if sha256(edge_path) != digest:
                raise RuntimeError('edge file changed during verification')
            report.update({'result_id': result['id'], 'edge_file': result['edge_file'],
                           'edge_file_sha256': digest, 'compiler': compiler,
                           'verifier_source_sha256': sha256(source),
                           'platform': platform.platform(),
                           'verified_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat()})
            report_path.write_text(json.dumps(report, indent=2) + '\n')
            reports.append(report_path.name)
            print(f"PASS {result['id']} ({report['elapsed_seconds']:.2f} seconds)", flush=True)
    summary = {'status': 'PASS', 'graphs_checked': len(reports), 'reports': reports,
               'results_index_sha256': sha256(index_path),
               'verifier_source_sha256': sha256(source),
               'runner_source_sha256': sha256(Path(__file__)),
               'completed_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat()}
    summary_path.write_text(json.dumps(summary, indent=2) + '\n')
    print(f"PASS: all {len(reports)} graphs verified. Reports: {output}", flush=True)


if __name__ == '__main__':
    main()
