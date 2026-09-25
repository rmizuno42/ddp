#!/usr/bin/env python3
"""Independent exact verification; Python standard library only.
Regenerates the graph, checks inverses, pencils, all controller pairs,
and then checks the complete edge list by all-source bitset BFS.
"""
import argparse,collections,hashlib,itertools,json
from pathlib import Path
I=((1,0,0),(0,1,0),(0,0,1));ZERO=(0,0,0)
def need(ok,message):
 if not ok:raise ValueError(message)
def mat(A):return tuple(tuple(r) for r in A)
def mv(A,x):return tuple(sum(a*b for a,b in zip(row,x))%3 for row in A)
def mm(A,B):return tuple(zip(*(mv(A,col) for col in zip(*B))))
def inverse(A):
 T=[list(r)+[int(i==j) for j in range(3)] for i,r in enumerate(A)]
 for j in range(3):
  pivot=next(k for k in range(j,3) if T[k][j]);T[j],T[pivot]=T[pivot],T[j]
  z=pow(T[j][j],-1,3);T[j]=[v*z%3 for v in T[j]]
  for k in range(3):
   if k!=j:
    z=T[k][j];T[k]=[(a-z*b)%3 for a,b in zip(T[k],T[j])]
 return tuple(tuple(r[3:]) for r in T)
def add(x,y):return tuple((a+b)%3 for a,b in zip(x,y))
def scale(c,x):return tuple(c*a%3 for a in x)
def span(columns):
 S={ZERO}
 for b in columns:S={add(x,scale(a,b)) for x in S for a in range(3)}
 return frozenset(S)
def setup(data):
 gens=data['generators'];iv=data['inverse_ports'];L=list(map(tuple,data['return_directions']))
 A,B,T=map(mat,(data['A'],data['B'],data['T']));ordinary=[A,inverse(A),B,inverse(B)]
 C=[];M=[]
 for i in range(6):
  for j in range(9):
   C.append([9*((i+k)%6)+(j+pow(2,i,9)*ell)%9 for k,ell in gens])
   M.append(ordinary+[T if i<3 else inverse(T)])
 return C,M,L,iv

def main():
 here=Path(__file__).resolve().parent;p=argparse.ArgumentParser(description=__doc__)
 p.add_argument('--config',type=Path,default=here/'construction.json');p.add_argument('--output',type=Path,default=here/'regenerated.edges');p.add_argument('--report',type=Path,default=here/'verification.json');args=p.parse_args()
 data=json.loads(args.config.read_text());C,M,L,iv=setup(data);n=len(C)
 need(n==54,'wrong controller order')
 for u in range(n):
  need(len(set(C[u]))==5 and u not in C[u],'controller not simple 5-regular')
  for t in range(5):
   v=C[u][t];r=iv[t]
   need(C[v][r]==u,'inverse port mismatch')
   need(mm(M[v][r],M[u][t])==I,'edge matrices not inverse')
   need(mv(M[u][t],L[t])==L[r],'edge direction mismatch')
 def route(u,w):
  prod=I;columns=[]
  for t in w:
   columns=[mv(M[u][t],c) for c in columns]+[L[iv[t]]]
   prod=mm(M[u][t],prod);u=C[u][t]
  return u,prod,span(columns)
 # Set-based pencils, including their common affine centre matrix.
 plane_counts=collections.Counter()
 for u in range(n):
  for t in range(5):
   v,A,core=route(u,[t]);planes=set()
   for h in range(5):
    for w in [(h,iv[h],t),(t,h,iv[h])]:
     end,P,H=route(u,w)
     need(end==v and P==A and core<=H,'pencil endpoint or affine centre mismatch')
     if len(H)==9:planes.add(H)
   need(len(planes)==4 and len(set().union(*planes))==27,'incomplete pencil')
   plane_counts[len(planes)]+=1
 # All non-backtracking three-step paths, with no solver assumptions.
 rank_counts=collections.Counter();coverage=[];routes=[]
 words=[w for w in itertools.product(range(5),repeat=3) if w[1]!=iv[w[0]] and w[2]!=iv[w[1]]]
 for u in range(n):
  found={v:('edge_pencil',[t]) for t,v in enumerate(C[u])}
  for w in words:
   v,A,H=route(u,w);rank_counts[len(H)]+=1
   if len(H)==27:found.setdefault(v,('full_rank',list(w)))
  need(len(found)==n,f'controller pair missing at source {u}')
  for v,(kind,w) in sorted(found.items()):routes.append({'u':u,'v':v,'kind':kind,'ports':w})
  coverage.append(len(found))
 (here/'route_certificate.json').write_text(json.dumps(routes,indent=2)+'\n')
 # Generate the undirected simple graph directly from the formulas.
 points=[(i%3,(i//3)%3,i//9) for i in range(27)];enc=lambda x:x[0]+3*x[1]+9*x[2]
 edges=set()
 for u in range(n):
  for k,x in enumerate(points):
   a=27*u+k
   for t in range(5):
    base=mv(M[u][t],x)
    for z in range(3):
     b=27*C[u][t]+enc(add(base,scale(z,L[iv[t]])))
     need(a!=b,'self-loop');edges.add((min(a,b),max(a,b)))
 N=27*n;adj=[set() for _ in range(N)]
 for a,b in edges:adj[a].add(b);adj[b].add(a)
 need(len(edges)==10935 and all(len(row)==15 for row in adj),'wrong degree or size')
 args.output.write_text(f'{N} {len(edges)}\n'+''.join(f'{a} {b}\n' for a,b in sorted(edges)),encoding='ascii')
 masks=[sum(1<<v for v in row) for row in adj];allmask=(1<<N)-1;hist=[N,0,0,0]
 for u in range(N):
  reached=1<<u;prev=1
  for step in range(1,4):
   new=reached;rem=reached
   while rem:
    bit=rem&-rem;rem-=bit;new|=masks[bit.bit_length()-1]
   reached=new;now=reached.bit_count();hist[step]+=now-prev;prev=now
  need(reached==allmask,f'diameter exceeds three at {u}')
 need(sum(hist)==N*N and hist[3]>0,'invalid distance distribution')
 report={'implementation':'standard-library Python: explicit finite sets + all-source bitset BFS','controller_vertices':n,'controller_edges':135,'controller_directed_pencils_checked':270,'number_of_planes_per_pencil':dict(plane_counts),'three_step_image_cardinalities':dict(rank_counts),'controller_pair_counts':dict(collections.Counter(r['kind'] for r in routes)),'vertices':N,'edges':len(edges),'min_degree':15,'max_degree':15,'diameter':3,'sources_checked':N,'distance_histogram':hist,'all_pairs_reached':True,'sha256':hashlib.sha256(args.output.read_bytes()).hexdigest()}
 args.report.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
