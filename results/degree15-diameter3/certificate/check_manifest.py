#!/usr/bin/env python3
"""Validate SHA256SUMS using the Python standard library."""
from pathlib import Path
import hashlib
here=Path(__file__).resolve().parent
count=0
for line in (here/'SHA256SUMS').read_text().splitlines():
 expected,name=line.split('  ',1)
 path=here/name
 actual=hashlib.sha256(path.read_bytes()).hexdigest()
 if actual!=expected:raise SystemExit(f'Checksum mismatch: {name}')
 count+=1
print(f'PASS: {count} files match SHA256SUMS')
