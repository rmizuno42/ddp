"""Build the explicit 88,452-vertex graph; Python standard library only."""
from pathlib import Path
import json,collections,hashlib,argparse
R=Path(__file__).resolve().parent

def load():
 d=json.loads((R/'construction.json').read_text());return d['controller'],d['matrices'],d['vectors'],d['translation_codes']
def digits(x):return [(x//(3**j))%3 for j in range(5)]
def encode(v):return sum(int(x)%3*3**j for j,x in enumerate(v))
def generate():
 C,A,b,cs=load();n=len(C)*243;V=[digits(x)for x in range(243)]
 maps=[[[encode([sum(A[t][i][j]*x[j]for j in range(5))+la*b[t][i] for i in range(5)])for la in range(3)]for x in V]for t in range(4)]
 edges=set()
 for u in range(len(C)):
  for t in range(4):
   v=C[u][t]
   for x in range(243):
    a=u*243+x
    for y in maps[t][x]:
     z=v*243+y
     if a!=z:edges.add((min(a,z),max(a,z)))
  c=digits(cs[u])
  for x in range(243):
   a=u*243+x;z=u*243+encode([V[x][j]+c[j]for j in range(5)])
   assert a!=z
   edges.add((min(a,z),max(a,z)))
 return n,sorted(edges)
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--output',default='graph_d14_D5_n88452.edges');args=parser.parse_args()
 n,E=generate();p=Path(args.output);p=p if p.is_absolute() else R/p
 with p.open('w')as f:
  f.write(f'{n} {len(E)}\n')
  for u,v in E:f.write(f'{u} {v}\n')
 deg=[0]*n
 for u,v in E:deg[u]+=1;deg[v]+=1
 result={'vertices':n,'edges':len(E),'maximum_degree':max(deg),'degree_distribution':dict(sorted(collections.Counter(deg).items())),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'vertex_encoding':'243*u + x0 + 3*x1 + 9*x2 + 27*x3 + 81*x4','simple':True}
 (R/'graph_metadata.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
