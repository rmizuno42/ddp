#!/usr/bin/env python3
"""Generate the explicit simple graph; requires only Python 3 standard library."""
from pathlib import Path
from collections import Counter
import argparse, hashlib, json, time
ROOT=Path(__file__).resolve().parent

def generate(output):
    start=time.time()
    raw=list(map(int,(ROOT/'data/controller_affine_chart.txt').read_text().split()))
    nc=raw[0];assert nc==364 and len(raw)==1+nc*4*31
    q=1; chart=[]
    for u in range(nc):
        row=[]
        for k in range(4):
            v=raw[q];q+=1; A=[raw[q+5*i:q+5*i+5]for i in range(5)];q+=25;b=raw[q:q+5];q+=5
            assert 0<=v<nc;row.append((v,A,b))
        chart.append(row)
    vectors=[[(x//(3**i))%3 for i in range(5)]for x in range(243)]
    powers=[1,3,9,27,81];n=nc*243;G=[set()for _ in range(n)]
    for u in range(nc):
        for v,A,b in chart[u]:
            for x,xx in enumerate(vectors):
                yy=[sum(A[i][j]*xx[j]for j in range(5))%3 for i in range(5)]
                s=243*u+x
                for lam in range(3):
                    y=sum(((yy[i]+lam*b[i])%3)*powers[i]for i in range(5));t=243*v+y
                    if s!=t:G[s].add(t)
    ordinary=dict(Counter(map(len,G)));assert ordinary=={12:87696,11:756}
    M=list(map(int,(ROOT/'data/main_matching.txt').read_text().split()));assert len(M)==n
    for s,t in enumerate(M):
        assert 0<=t<n and t!=s and M[t]==s and t not in G[s]
        G[s].add(t)
    assert Counter(map(len,G))=={13:87696,12:756}
    used=set();spare_count=0
    for line in(ROOT/'data/spare_matching.txt').read_text().splitlines():
        a,b=map(int,line.split());assert 0<=a<n and 0<=b<n and a!=b
        assert a not in used and b not in used and len(G[a])==len(G[b])==12
        assert b not in G[a] and a not in G[b];used.update((a,b));G[a].add(b);G[b].add(a);spare_count+=1
    assert spare_count==378 and len(used)==756
    assert all(len(row)==13 for row in G)
    for a,row in enumerate(G):
        for b in row:assert a in G[b]
    m=sum(map(len,G))//2;assert m==574938
    with Path(output).open('w')as f:
        f.write(f'{n} {m}\n')
        for a,row in enumerate(G):
            for b in sorted(row):
                if a<b:f.write(f'{a} {b}\n')
    digest=hashlib.sha256(Path(output).read_bytes()).hexdigest()
    result={'vertices':n,'edges':m,'degree':13,'simple':True,'undirected':True,'ordinary_degree_histogram':ordinary,'main_matching_edges':n//2,'spare_matching_edges':spare_count,'edge_file_sha256':digest,'seconds':time.time()-start}
    print(json.dumps(result,indent=2));return result
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',default=str(ROOT/'graph.edges'));a=p.parse_args();generate(a.output)
