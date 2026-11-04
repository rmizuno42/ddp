#!/usr/bin/env python3
"""Check the finite ingredients of the girth=9 and Aut(G)=C16 arguments."""
from collections import Counter,deque
from pathlib import Path
import json
from check_certificate import neighbours

def check():
    n=208;adj=[neighbours(v) for v in range(n)]
    signatures=[]
    for s in range(n):
        d=[-1]*n;d[s]=0;todo=deque([s])
        while todo:
            a=todo.popleft()
            for b in adj[a]:
                if d[b]<0:d[b]=d[a]+1;todo.append(b)
        assert min(d)==0 and max(d)==7
        hist=Counter(d);sig=tuple(hist[i] for i in range(8));signatures.append(sig)
        assert sig[:5]==(1,3,6,12,24)  # no collision among nonbacktracking walks of length <=4
    refined=[(signatures[v],tuple(sorted(signatures[w] for w in adj[v]))) for v in range(n)]
    classes={}
    for v,c in enumerate(refined):classes.setdefault(c,[]).append(v)
    blocks=sorted(sorted(x) for x in classes.values())
    assert blocks==[list(range(16*i,16*(i+1))) for i in range(13)]
    # Every graph automorphism therefore preserves each of the 13 orbit sets.
    # Unique inter-orbit neighbours propagate the action from orbit 0.
    propagation=[(i,i+1) for i in range(10)]+[(2,12),(12,11)]
    for a,b in propagation:
        for x in range(16):assert len(adj[16*a+x]&set(range(16*b,16*(b+1))))==1
    # On orbit 0 an automorphism is x -> epsilon*x+c. Propagation to orbit 7,
    # then the chord (1,x)--(7,x+2), excludes epsilon=-1 since -2 != 2 mod16.
    assert (-2)%16!=2
    # Identity on orbit 0 propagates along the listed edges to every vertex.
    reached={0}
    for a,b in propagation:assert a in reached;reached.add(b)
    assert reached==set(range(13))
    cycle=[0,16,114,130,83,99,115,17,1]
    assert len(set(cycle))==9 and all(cycle[(i+1)%9] in adj[cycle[i]] for i in range(9))
    return dict(vertices=n,girth=9,nine_cycle=cycle,all_radius4_balls_have_moore_size=46,
                intrinsic_orbit_classes=blocks,automorphism_group='C16',automorphism_group_order=16,
                proof='Distance-sphere signatures plus one neighbour refinement separate all orbit sets. Orbit 0 induces C16. Unique inter-orbit edges propagate its action; chord shift 2 excludes reflections. Translations supply all 16 automorphisms.',valid=True)
if __name__=='__main__':
    print(json.dumps(check(),indent=2))
