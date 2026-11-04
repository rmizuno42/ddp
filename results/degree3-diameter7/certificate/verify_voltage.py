#!/usr/bin/env python3
"""Direct modular-set proof of the diameter upper bound. No graph-file/BFS input."""
import json
from pathlib import Path

def verify():
    q=16;b=13
    arcs=[[] for _ in range(b)]
    for i in range(12):arcs[i].append((i+1,0));arcs[i+1].append((i,0))
    arcs[0].extend([(0,1),(0,15)]);arcs[12].append((12,8))
    for a,c,t in [(1,7,2),(2,12,12),(3,9,8),(4,6,11),(5,8,15),(10,11,15)]:
        arcs[a].append((c,t));arcs[c].append((a,(-t)%16))
    assert all(len(x)==3 and len(set(x))==3 for x in arcs)
    for i in range(b):
        for j,t in arcs[i]:assert (i,(-t)%q) in arcs[j]
    roots=[]
    for root in range(b):
        R=[set() for _ in range(b)];R[root].add(0)
        sizes=[list(map(len,R))];spheres=[1]
        for step in range(1,8):
            T=[set(x) for x in R]
            for i in range(b):
                for j,t in arcs[i]:T[j].update((x+t)%q for x in R[i])
            spheres.append(sum(map(len,T))-sum(map(len,R)));R=T;sizes.append(list(map(len,R)))
        assert all(x==set(range(q)) for x in R),(root,R)
        roots.append(dict(root_orbit=root,reachable_counts_by_step=sizes,spheres=spheres,final_sets=[sorted(x) for x in R]))
    return dict(arcs=arcs,quotient_order=b,cyclic_order=q,checked_root_target_orbit_pairs=b*b,diameter_at_most=7,all_final_sets_complete=True,roots=roots)
if __name__=='__main__':
    print(json.dumps(verify(),indent=2))
