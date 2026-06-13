"""Generate final edge list for the C4 x C6 CRT-block route-chart candidate."""
import gzip, sys
from verify_candidate import build_controller, euler_2factor_coloring, orient_two_factors, A, B, MUL
FIB = 4**5

def idx_to_vec(x):
    v=[]
    for _ in range(5):
        v.append(x & 3); x >>= 2
    return v

def vec_to_idx(v):
    x=0
    for i,a in enumerate(v): x |= (a & 3) << (2*i)
    return x

def mv(M,v):
    out=[]
    for row in M:
        z=0
        for a,b in zip(row,v): z ^= MUL[a][b]
        out.append(z)
    return out

def add_scaled(v,lam,b):
    return [v[i] ^ MUL[lam][b[i]] for i in range(5)]

def main():
    outfn=sys.argv[1] if len(sys.argv)>1 else '/mnt/data/phase34_crt_block_verified/final_graph_edges.tsv.gz'
    adj,cedges=build_controller()
    color=euler_2factor_coloring(adj,cedges)
    arc=orient_two_factors(adj,cedges,color)
    oriented=[]
    for u,v,_ in cedges:
        su=arc[(u,v)]; sv=arc[(v,u)]
        if su in (0,2): tail,head,sym=u,v,su
        elif sv in (0,2): tail,head,sym=v,u,sv
        else: raise RuntimeError('no forward orientation')
        oriented.append((tail,head,sym))
    n_final=len(adj)*FIB
    m_final=len(cedges)*FIB*4
    deg=[0]*n_final; seen=set()
    opener=gzip.open if outfn.endswith('.gz') else open
    with opener(outfn,'wt') as f:
        f.write(f'{n_final} {m_final}\n')
        for tail,head,sym in oriented:
            M=A[sym]; b=B[sym]
            for xidx in range(FIB):
                x=idx_to_vec(xidx); Ax=mv(M,x); U=tail*FIB+xidx
                for lam in range(4):
                    yidx=vec_to_idx(add_scaled(Ax,lam,b)); V=head*FIB+yidx
                    if U==V: raise RuntimeError('self loop')
                    key=(U,V) if U<V else (V,U)
                    if key in seen: raise RuntimeError(f'duplicate edge {key}')
                    seen.add(key); deg[U]+=1; deg[V]+=1
                    f.write(f'{key[0]}\t{key[1]}\n')
    assert len(seen)==m_final, (len(seen),m_final)
    assert min(deg)==max(deg)==16, (min(deg),max(deg))
    print(f'Wrote {outfn}: {n_final} vertices, {m_final} edges, all degrees 16.')
if __name__=='__main__': main()
