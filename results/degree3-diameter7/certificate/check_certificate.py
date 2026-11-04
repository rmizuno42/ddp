#!/usr/bin/env python3
"""Check depth-7 spanning-tree certificates without computing shortest paths."""
from pathlib import Path
import json

def neighbours(v):
    i,x=divmod(v,16);out=set()
    def add(j,y):out.add(16*j+y%16)
    if i>0:add(i-1,x)
    if i<12:add(i+1,x)
    if i==0:add(0,x-1);add(0,x+1)
    if i==12:add(12,x+8)
    shifts={1:(7,2),7:(1,-2),2:(12,-4),12:(2,4),3:(9,8),9:(3,-8),4:(6,-5),6:(4,5),5:(8,-1),8:(5,1),10:(11,-1),11:(10,1)}
    if i in shifts:j,t=shifts[i];add(j,x+t)
    assert len(out)==3 and v not in out
    return out

def check():
    obj=json.loads((Path(__file__).parent/'certificates/thirteen_trees.json').read_text())
    assert obj['vertices']==208 and obj['maximum_depth']==7
    assert [z['root'] for z in obj['trees']]==list(range(0,208,16))
    adj=[neighbours(v) for v in range(208)]
    for v in range(208):
        assert all(v in adj[w] for w in adj[v])
        i,x=divmod(v,16)
        for c in range(16):
            assert {16*(w//16)+(w%16+c)%16 for w in adj[v]}==adj[16*i+(x+c)%16]
    for tree in obj['trees']:
        root=tree['root'];p=tree['parent'];d=tree['depth']
        assert len(p)==208 and len(d)==208 and p[root]==root and d[root]==0
        for v in range(208):
            if v!=root:assert 1<=d[v]<=7 and 0<=p[v]<208 and p[v] in adj[v] and d[p[v]]==d[v]-1
    assert 208>1+3*sum(2**r for r in range(6))
    return dict(vertices=208,trees_checked=13,parent_edges_checked=13*207,maximum_depth=7,translation_automorphisms_checked=16,moore_bound_degree3_diameter6=190,diameter_exactly=7,valid=True)
if __name__=='__main__':
    print(json.dumps(check(),indent=2))
