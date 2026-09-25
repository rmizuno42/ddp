"""Independent exact finite proof. Python standard library only.
No search objective, geometry library, or large edge list is trusted.
"""
from pathlib import Path
from functools import lru_cache
from itertools import product,combinations
from collections import Counter
import json,time
R=Path(__file__).resolve().parent;start=time.monotonic()
d=json.loads((R/'construction.json').read_text());C=d['controller'];A=d['matrices'];b=d['vectors'];n=len(C);q=3;s=5
I=tuple(tuple(int(i==j)for j in range(5))for i in range(5))
def mv(M,v):return tuple(sum(x*y for x,y in zip(row,v))%3 for row in M)
def mm(M,N):return tuple(tuple(sum(M[i][k]*N[k][j]for k in range(5))%3 for j in range(5))for i in range(5))
def digits(x):return tuple(x//(3**j)%3 for j in range(5))
cs=[digits(x)for x in d['translation_codes']]
assert len(cs)==n and all(any(v)for v in cs)
for t in range(4):
 assert mm(A[t],A[t])==I and mv(A[t],b[t])==tuple(b[t]) and any(b[t])
 for u in range(n):assert 0<=C[u][t]<n and C[C[u][t]][t]==u
assert all(len(set(row))==4 for row in C)
def reduce(w):
 a=[]
 for t in w:
  if a and a[-1]==t:a.pop()
  else:a.append(t)
 return tuple(a)
@lru_cache(None)
def rr(rows):
 a=[list(v)for v in rows];k=0
 for j in range(5):
  p=next((p for p in range(k,len(a))if a[p][j]),None)
  if p is None:continue
  a[p],a[k]=a[k],a[p];z=a[k][j];a[k]=[z*x%3 for x in a[k]]
  for p in range(len(a)):
   if p!=k:
    z=a[p][j];a[p]=[(x-z*y)%3 for x,y in zip(a[p],a[k])]
  k+=1
  if k==len(a):break
 return tuple(tuple(v)for v in a[:k])
@lru_cache(None)
def image_basis(B):
 vs={(0,0,0,0,0)}
 for v in B:vs={tuple((a+la*z)%3 for a,z in zip(x,v))for x in vs for la in range(3)}
 assert len(vs)==3**len(B)
 return sum(1<<sum(x[j]*3**j for j in range(5))for x in vs)
def image(cols):return image_basis(rr(tuple(cols)))
@lru_cache(None)
def control(w):
 cols=[];T=I
 for t in w:cols=[mv(A[t],v)for v in cols]+[tuple(b[t])];T=mm(A[t],T)
 return T,tuple(cols)
W={ell:[w for w in product(range(4),repeat=ell)if reduce(w)==w]for ell in [1,3,5]}
rank_hist=Counter(len(rr(control(w)[1]))for w in W[5]);assert rank_hist=={5:324}
# Each starting controller state is covered exactly once by the 364 odd reduced words.
controller_counts=Counter();self_lengths=Counter()
for u in range(n):
 seen={}
 for ell in [1,3,5]:
  for w in W[ell]:
   v=u
   for t in w:v=C[v][t]
   assert v not in seen,(u,v,seen.get(v),w)
   seen[v]=w;controller_counts[ell]+=1
 assert len(seen)==n
 self_lengths[len(seen[u])]+=1
print('controller bijection and 324 ranks: PASS',flush=True)
# At a state after j base steps, c is transported by the remaining suffix.
def states(u,w):
 a=[u]
 for t in w:a.append(C[a[-1]][t])
 return a
def transported(w,st):
 out=[]
 for j,u in enumerate(st):
  z=cs[u]
  for t in w[j:]:z=mv(A[t],z)
  out.append(z)
 return out
triple_witnesses=[]
for u in range(n):
 for w in W[3]:
  core=control(w)[1];assert len(rr(core))==3
  dirs=transported(w,states(u,w))
  good=next(((i,j)for i,j in combinations(range(4),2)if len(rr(core+(dirs[i],dirs[j])))==5),None)
  assert good is not None,(u,w)
  triple_witnesses.append([u,list(w),list(good)])
print('13104 triple routes with two translations: PASS',flush=True)
# Direct set union for one-letter routes, not the quotient-coordinate oracle of the search.
basebits={};families={}
for t in range(4):
 bits=0
 for ell in [1,3,5]:
  for w in product(range(4),repeat=ell):
   if reduce(w)==(t,):
    T,cols=control(w);assert T==tuple(tuple(x)for x in A[t]);bits|=image(cols)
 basebits[t]=bits
 families[t]=[w for w in product(range(4),repeat=3)if reduce(w)==(t,)]
 assert len(families[t])==7
FULL=(1<<243)-1;single_points=[];single_witness_sizes=Counter()
for u in range(n):
 for t in range(4):
  bits=basebits[t];used=0
  for w in families[t]:
   T,cols=control(w);assert T==tuple(tuple(x)for x in A[t])
   ds=transported(w,states(u,w))
   for i,j in combinations(range(4),2):
    bits|=image(cols+(ds[i],ds[j]));used+=1
   if bits==FULL:break
  assert bits==FULL,(u,t,bits.bit_count())
  single_points.append(bits.bit_count());single_witness_sizes[used]+=1
print('1456 one-letter routes, each all 243 points: PASS',flush=True)
# Verify the explicit obstruction for the lift without translations.
ob=json.loads((R/'base_lift_obstruction.json').read_text());u0=ob['controller_source'];v0=ob['controller_target'];rs=set()
for ell in range(6):
 for w in product(range(4),repeat=ell):
  v=u0
  for t in w:v=C[v][t]
  if v==v0:rs.add(reduce(w))
assert rs=={(ob['label'],)} and basebits[ob['label']].bit_count()==135
moore4=1+14*sum(13**j for j in range(4));assert n*243>moore4
result={'method':'independent direct row reduction and explicit finite-set unions; standard-library Python','q':3,'s':5,'controller_states':n,'controller_labels':4,'inverse_labels':[0,1,2,3],'semiloops':sum(C[u][t]==u for u in range(n)for t in range(4)),'rank5_histogram':dict(rank_hist),'controller_odd_route_pair_counts':dict(controller_counts),'controller_self_pair_route_lengths':dict(self_lengths),'triple_routes_verified':len(triple_witnesses),'one_letter_routes_verified':len(single_points),'one_letter_covered_points_min':min(single_points),'base_one_letter_covered_points':[basebits[t].bit_count()for t in range(4)],'one_letter_plane_tests_histogram':dict(single_witness_sizes),'distinct_translation_directions':len(set(cs)),'lift_order':n*243,'maximum_degree_bound':14,'diameter_bound':5,'moore_bound_degree14_D4':moore4,'therefore_diameter':5,'seconds':time.monotonic()-start}
(R/'small_certificate.json').write_text(json.dumps(result,indent=2));(R/'triple_route_witnesses.json').write_text(json.dumps(triple_witnesses))
print(json.dumps(result,indent=2))
