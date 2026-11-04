#!/usr/bin/env python3
"""The 208-vertex graph, defined directly by a path and six voltage chords."""
from pathlib import Path
import argparse
B, Q = 13, 16
CHORDS = ((1,7,2), (2,12,-4), (3,9,8), (4,6,-5), (5,8,-1), (10,11,-1))

def construct():
    edges=set()
    def add(i,x,j,y):
        a=i*Q+x%Q;b=j*Q+y%Q
        if a==b:raise ValueError('self loop')
        e=tuple(sorted((a,b)))
        if e in edges:raise ValueError(f'duplicate edge {e}')
        edges.add(e)
    for x in range(Q):
        for i in range(B-1):add(i,x,i+1,x)
        add(0,x,0,x+1)
        for i,j,s in CHORDS:add(i,x,j,x+s)
    for x in range(Q//2):add(B-1,x,B-1,x+Q//2)
    return B*Q,edges

def write_files(folder):
    n,edges=construct();folder.mkdir(parents=True,exist_ok=True)
    (folder/'graph.edges').write_text(f'{n} {len(edges)}\n'+''.join(f'{a} {b}\n' for a,b in sorted(edges)))
    adj=[[] for _ in range(n)]
    for a,b in sorted(edges):adj[a].append(b);adj[b].append(a)
    (folder/'graph.adjlist').write_text('# n=208, degree=3, diameter=7; each row: vertex and ALL neighbours\n'+''.join(' '.join(map(str,[a]+sorted(adj[a])))+'\n' for a in range(n)))
    return n,edges
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,default=Path(__file__).parent/'graphs');a=p.parse_args()
    n,e=write_files(a.out);print(f'Constructed {n} vertices and {len(e)} edges.')
