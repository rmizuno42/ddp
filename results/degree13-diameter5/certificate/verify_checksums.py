#!/usr/bin/env python3
from pathlib import Path
import argparse,hashlib,json,sys
root=Path(__file__).resolve().parent
p=argparse.ArgumentParser();p.add_argument('--graph');args=p.parse_args()
manifest=json.loads((root/'SHA256SUMS.json').read_text());bad=[]
for name,expected in manifest.items():
 f=root/name
 actual=hashlib.sha256(f.read_bytes()).hexdigest()if f.is_file()else None
 if actual!=expected:bad.append(name)
if args.graph:
 f=Path(args.graph);expected=json.loads((root/'certificate.json').read_text())['canonical_edge_file_sha256']
 if not f.is_file()or hashlib.sha256(f.read_bytes()).hexdigest()!=expected:bad.append(str(f))
if bad:
 print('CHECKSUM FAILURE:',*bad,sep='\n');sys.exit(1)
print('PASS:',len(manifest),'packaged file hashes verified'+('; canonical edge-list hash verified'if args.graph else ''))
