"""Orient an Euler circuit and split the resulting 2-in/2-out digraph into permutations."""
from pathlib import Path
import sys,json
P=Path(__file__).resolve().parents[1];name=sys.argv[1];raw=[list(map(int,l.split())) for l in (P/'candidates'/f'{name}.rawadj').read_text().splitlines() if l.strip()];n=len(raw);assert all(len(set(r))==4 for r in raw)
G=[set(r) for r in raw];stack=[0];circuit=[]
while stack:
 u=stack[-1]
 if G[u]:
  v=min(G[u]);G[u].remove(v);G[v].remove(u);stack.append(v)
 else:circuit.append(stack.pop())
circuit=circuit[::-1];assert len(circuit)==2*n+1;out=[[] for _ in range(n)]
for u,v in zip(circuit,circuit[1:]):out[u].append(v)
assert all(len(r)==2 for r in out)
match=[-1]*n
def augment(u,seen):
 for v in out[u]:
  if seen[v]:continue
  seen[v]=True
  if match[v]<0 or augment(match[v],seen):match[v]=u;return True
 return False
for u in range(n):assert augment(u,[False]*n)
a=[0]*n
for v,u in enumerate(match):a[u]=v
b=[next(v for v in out[u] if v!=a[u]) for u in range(n)];assert len(set(a))==n and len(set(b))==n
C=[[0]*4 for _ in range(n)]
for u in range(n):C[u][0]=a[u];C[a[u]][1]=u;C[u][2]=b[u];C[b[u]][3]=u
for u in range(n):assert set(C[u])==set(raw[u])
(P/'candidates'/f'{name}.adj').write_text(''.join(' '.join(map(str,r))+'\n' for r in C));print(name,'labeled',n)
