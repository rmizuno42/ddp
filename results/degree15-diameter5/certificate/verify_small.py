"""Exact certificate over the prime field F_5, using only the standard library."""
import json,itertools,sys
from pathlib import Path
R=Path(__file__).resolve().parent
q=5;s=5;inv=[1,0,2]
d=json.loads((R/'chart.json').read_text());A=d['matrices'];b=d['vectors']
a=[list(map(int,line.split()))for line in(R/'controller.adj').read_text().splitlines()];n=len(a)
def mv(M,v):return [sum(x*y for x,y in zip(row,v))%q for row in M]
def mm(M,N):return [[sum(M[i][k]*N[k][j]for k in range(s))%q for j in range(s)]for i in range(s)]
I=[[int(i==j)for j in range(s)]for i in range(s)]
for t in range(3):
 assert mm(A[t],A[inv[t]])==I
 assert mv(A[inv[t]],b[t])==b[inv[t]]
 for u in range(n):assert a[a[u][t]][inv[t]]==u
assert all(sorted(row[t]for row in a)==list(range(n))for t in range(3))
def reduce(w):
 out=[]
 for t in w:
  if out and inv[out[-1]]==t:out.pop()
  else:out.append(t)
 return tuple(out)
def words(k):
 return [w for w in itertools.product(range(3),repeat=k) if reduce(w)==w]
def rref(rows):
 rows=[list(v)for v in rows];piv=[];k=0
 for col in range(s):
  p=next((i for i in range(k,len(rows))if rows[i][col]),None)
  if p is None:continue
  rows[k],rows[p]=rows[p],rows[k];iv=pow(rows[k][col],-1,q)
  rows[k]=[x*iv%q for x in rows[k]]
  for i in range(len(rows)):
   if i!=k and rows[i][col]:
    f=rows[i][col];rows[i]=[(x-f*y)%q for x,y in zip(rows[i],rows[k])]
  piv.append(col);k+=1
 return tuple(tuple(v)for v in rows[:k]),piv
def control(w):
 cols=[];T=I
 for t in w:cols=[mv(A[t],v)for v in cols]+[b[t]];T=mm(A[t],T)
 return T,cols
rank5={w:len(rref(control(w)[1])[0])for w in words(5)}
good5=[w for w in rank5 if rank5[w]==5]
repairs={};good3=[]
for r in words(3):
 Tr,Mr=control(r);core,piv=rref(Mr);assert len(core)==3
 planes=set()
 for k in range(3,6):
  for w in itertools.product(range(3),repeat=k):
   if reduce(w)!=r:continue
   T,M=control(w);assert T==Tr
   H,_=rref(M)
   if len(H)==4:
    assert len(rref(list(H)+list(core))[0])==4
    planes.add(H)
 if len(planes)==6:
  for h1,h2 in itertools.combinations(planes,2):assert len(rref(list(h1)+list(h2))[0])==5
  good3.append(r)
 repairs[''.join(map(str,r))]={'hyperplanes':len(planes),'core':[list(v)for v in core], 'hyperplane_bases':[[list(v)for v in H]for H in sorted(planes)]}
def endpoint(u,w):
 for t in w:u=a[u][t]
 return u
cover=[];count5=count3=0
for u in range(n):
 rows={}
 for w in good5:rows.setdefault(endpoint(u,w),('full',w))
 count5+=len(rows)
 for w in good3:rows.setdefault(endpoint(u,w),('pencil',w))
 count3+=sum(kind=='pencil'for kind,w in rows.values())
 assert len(rows)==n,(u,set(range(n))-set(rows))
 cover.append([[kind,list(w)]for v,(kind,w)in sorted(rows.items())])
result={'q':q,'fiber_dimension':s,'controller_order':n,'lift_order':n*q**s,'maximum_degree_upper_bound':15,'diameter_upper_bound':5,'rank5_hist':{r:sum(v==r for v in rank5.values())for r in set(rank5.values())},'bad_five_letter_words':[''.join(map(str,w))for w,r in rank5.items()if r<5],'complete_pencil_words':[''.join(map(str,w))for w in good3], 'ordered_pairs_with_full_rank_route':count5,'ordered_pairs_repaired_by_pencil':count3,'controller_fixed_points_b':sum(row[2]==i for i,row in enumerate(a))}
(R/'small_certificate.json').write_text(json.dumps(result,indent=2));(R/'pencil_certificate.json').write_text(json.dumps(repairs,indent=2));(R/'route_assignment.json').write_text(json.dumps(cover))
print(json.dumps(result,indent=2))
