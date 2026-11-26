#!/usr/bin/env bash
set -eu
cd "$(dirname "$0")"
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT
python3 construct.py "$tmp/regenerated.edges"
cmp graph.edges "$tmp/regenerated.edges"
# The original independent readers take one edge per line.
tail -n +2 graph.edges > "$tmp/body.edges"
python3 verify_layers.py "$tmp/body.edges" "$tmp/layers.bin"
"${CXX:-c++}" -std=c++17 -O2 verify_queue.cpp -o "$tmp/verify_queue"
"$tmp/verify_queue" "$tmp/body.edges" "$tmp/queue.bin"
cmp "$tmp/layers.bin" "$tmp/queue.bin"
python3 - "$tmp" <<'PY'
from hashlib import sha256
from pathlib import Path
import sys

temporary = Path(sys.argv[1])
for name, path in [('published edge list', Path('graph.edges')),
                   ('source edge rows', temporary/'body.edges'), ('distance matrix', temporary/'queue.bin')]:
    print(name, sha256(path.read_bytes()).hexdigest())
PY
python3 symmetry.py
