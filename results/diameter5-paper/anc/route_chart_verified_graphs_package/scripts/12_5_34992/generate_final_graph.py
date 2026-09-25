import gzip
from verify_candidate import EDGE_DATA, MOD4, MOD6, HSIZE, gid, Q, A, B, mv
NBASE=6; FIB=Q**5
# encode/decode F_3^5
def dec(n):
    v=[]
    for _ in range(5): v.append(n%Q); n//=Q
    return v
def enc(v):
    n=0; p=1
    for x in v: n+=x*p; p*=Q
    return n
edges=set()
for beid,(u,v,xv,yv) in enumerate(EDGE_DATA):
    for x in range(MOD4):
        for y in range(MOD6):
            cu=u*HSIZE+gid(x,y); cv=v*HSIZE+gid(x+xv,y+yv)
            # symbol does not matter for controller construction here; need reproduce labelling? For graph generation, choose labels from 2-factorization.
# build controller + labels from verifier functions
from verify_candidate import build_controller,euler_2factor_coloring,orient_two_factors
adj,cedges=build_controller(); color=euler_2factor_coloring(adj,cedges); arc=orient_two_factors(adj,cedges,color)
NCTRL=len(adj); N=NCTRL*FIB
for u in range(NCTRL):
    for v,eid in adj[u]:
        if u < v:
            su=arc[(u,v)]; sv=arc[(v,u)]
            # add edges for direction u->v using symbol su; inverse formula ensures same set as v->u.
            for xi in range(FIB):
                xvec=dec(xi)
                Ax=mv(A[su],xvec)
                for lam in range(Q):
                    yvec=[(Ax[i]+lam*B[su][i])%Q for i in range(5)]
                    yi=enc(yvec)
                    a=u*FIB+xi; b=v*FIB+yi
                    if a>b: a,b=b,a
                    edges.add((a,b))
# verify degree
from collections import Counter
deg=Counter()
for a,b in edges:
    if a==b: raise RuntimeError('loop')
    deg[a]+=1; deg[b]+=1
assert len(deg)==N, (len(deg),N)
assert min(deg.values())==12 and max(deg.values())==12, (min(deg.values()), max(deg.values()))
with gzip.open('final_graph_edges.tsv.gz','wt') as f:
    f.write(f'# n={N} m={len(edges)} degree=12\n')
    for a,b in sorted(edges): f.write(f'{a}\t{b}\n')
print(f'Wrote final_graph_edges.tsv.gz: {N} vertices, {len(edges)} edges, all degrees 12.')
