"""Explicit split-octonion construction of H(3), H(9), and exceptional duality.
Arithmetic uses F9=F3[a]/(a^2+1), code x+3*y. No online access needed.
"""
from pathlib import Path
from collections import Counter
import numpy as np,json,sys,math,time
from numba import njit
R=Path(__file__).resolve().parent

def field(q):
 add=np.zeros((q,q),np.int64);mul=add.copy()
 for x in range(q):
  for y in range(q):
   a,b=x%3,x//3;c,d=y%3,y//3
   add[x,y]=(a+c)%3+3*((b+d)%3)
   mul[x,y]=(a*c+2*b*d)%3+3*((a*d+b*c)%3)
 neg=np.array([next(y for y in range(q)if add[x,y]==0)for x in range(q)],np.int64)
 inv=np.array([0]+[next(y for y in range(q)if mul[x,y]==1)for x in range(1,q)],np.int64)
 return add,mul,neg,inv

@njit
def rr(A,add,mul,neg,inv):
 A=A.copy();nr,nc=A.shape;piv=np.empty(min(nr,nc),np.int64);r=0
 for c in range(nc):
  j=r
  while j<nr and A[j,c]==0:j+=1
  if j==nr:continue
  for k in range(nc):z=A[r,k];A[r,k]=A[j,k];A[j,k]=z
  v=inv[A[r,c]]
  for k in range(nc):A[r,k]=mul[v,A[r,k]]
  for j in range(nr):
   if j!=r and A[j,c]!=0:
    v=neg[A[j,c]]
    for k in range(nc):A[j,k]=add[A[j,k],mul[v,A[r,k]]]
  piv[r]=c;r+=1
  if r==nr:break
 return A,piv[:r]

@njit
def points(q,add,mul,neg):
 n=(q**6-1)//(q-1);out=np.empty((n,7),np.int64);lookup=np.full(q**7,-1,np.int32);cnt=0
 for code in range(1,q**7):
  x=np.zeros(7,np.int64);t=code;first=-1
  for k in range(7):
   x[k]=t%q;t//=q
   if first<0 and x[k]:first=k
  if x[first]!=1:continue
  norm=mul[x[0],x[0]]
  for k in range(3):norm=add[norm,mul[x[1+k],x[4+k]]]
  if norm==0:
   out[cnt]=x;lookup[code]=cnt;cnt+=1
 assert cnt==n
 return out,lookup

@njit
def linekey(x,y,q,add,mul,neg,inv):
 a=np.empty((2,7),np.int64);a[0]=x;a[1]=y
 b,piv=rr(a,add,mul,neg,inv);assert len(piv)==2
 z=0;power=1
 for r in range(2):
  for k in range(7):z+=power*b[r,k];power*=q
 return z

@njit
def all_linekeys(P,T,q,add,mul,neg,inv):
 n=len(P);keys=np.empty((n,q+1),np.int64)
 for pi in range(n):
  x=P[pi];A=np.zeros((7,7),np.int64)
  for i in range(7):
   for j in range(7):
    for k in range(7):
     A[k,j]=add[A[k,j],mul[x[i],T[i,j,k]]]
  mat,piv=rr(A,add,mul,neg,inv);assert len(piv)==4
  free=np.empty(3,np.int64);fc=0
  for i in range(7):
   if i not in piv:free[fc]=i;fc+=1
  K=np.zeros((3,7),np.int64)
  for i in range(3):
   K[i,free[i]]=1
   for r in range(4):K[i,piv[r]]=neg[mat[r,free[i]]]
  h=0
  while x[free[h]]==0:h+=1
  k1=(h+1)%3;k2=(h+2)%3
  for lam in range(q):
   y=np.empty(7,np.int64)
   for j in range(7):y[j]=add[K[k1,j],mul[lam,K[k2,j]]]
   keys[pi,lam]=linekey(x,y,q,add,mul,neg,inv)
  keys[pi,q]=linekey(x,K[k2],q,add,mul,neg,inv)
 return keys

@njit
def get_phi(keys,dual,q,lookup,add,mul,inv):
 n=len(keys);phi=np.empty(n,np.int32)
 for h in range(n):
  z=keys[h];x=np.empty(7,np.int64);y=x.copy()
  for i in range(7):x[i]=z%q;z//=q
  for i in range(7):y[i]=z%q;z//=q
  v=np.zeros(7,np.int64)
  for i in range(7):
   for j in range(7):
    t=mul[x[i],y[j]]
    for k in range(7):v[k]=add[v[k],mul[t,dual[i,j,k]]]
  first=0
  while first<7 and v[first]==0:first+=1
  assert first<7
  s=inv[v[first]];code=0;pw=1
  for i in range(7):code+=pw*mul[s,v[i]];pw*=q
  assert lookup[code]>=0
  phi[h]=lookup[code]
 return phi

@njit
def extend_tau(P,adj,phi,keys,q,add,mul,neg,inv):
 n=len(P);tau=np.empty(2*n,np.int32);tau[n:]=phi
 for p in range(n):
  ls=adj[p]-n;x=P[phi[ls[0]]];y=P[phi[ls[1]]]
  key=linekey(x,y,q,add,mul,neg,inv);idx=np.searchsorted(keys,key)
  assert idx<n and keys[idx]==key
  tau[p]=n+idx
 return tau

@njit
def verify_tau(adj,tau):
 n=len(adj)
 for u in range(n):
  for v in adj[u]:
   assert tau[v] in adj[tau[u]]

def cycles_order(perm):
 seen=np.zeros(len(perm),bool);hist=Counter();order=1
 for i in range(len(perm)):
  if seen[i]:continue
  j=i;c=0
  while not seen[j]:seen[j]=True;j=int(perm[j]);c+=1
  assert j==i;hist[c]+=1;order=math.lcm(order,c)
 return order,hist

def perm_power(p,m):
 r=np.arange(len(p),dtype=p.dtype);a=p.copy()
 while m:
  if m&1:r=a[r]
  a=a[a];m//=2
 return r

def build(q):
 start=time.monotonic();add,mul,neg,inv=field(q)
 data=np.load(R/'lie_data.npz');T=data['T'];dual=data['dual']
 P,lookup=points(q,add,mul,neg);n=len(P);print('points',q,n,flush=True)
 K=all_linekeys(P,T,q,add,mul,neg,inv);keys,ix=np.unique(K.ravel(),return_inverse=True);assert len(keys)==n
 adj=np.full((2*n,q+1),-1,np.int32);adj[:n]=ix.reshape((n,q+1))+n;deg=np.zeros(n,np.int32)
 for p in range(n):
  for l in adj[p]:adj[l,deg[l-n]]=p;deg[l-n]+=1
 assert np.all(deg==q+1);print('incidence graph',adj.shape,flush=True)
 phi=get_phi(keys,dual,q,lookup,add,mul,inv);assert len(set(phi))==n
 tau=extend_tau(P,adj,phi,keys,q,add,mul,neg,inv);assert len(set(tau))==2*n
 verify_tau(adj,tau);order,hist=cycles_order(tau);print('tau order',order,'cycles',hist,flush=True)
 np.savez_compressed(R/f'hexagon_q{q}.npz',points=P,adj=adj,keys=keys,tau=tau,phi=phi)
 out={'q':q,'points':n,'incidence_vertices':2*n,'incidence_degree':q+1,'tau_order':order,'tau_cycles':dict(hist),'tau_verified_automorphism':True,'elapsed_seconds':time.monotonic()-start}
 (R/f'hexagon_q{q}_checks.json').write_text(json.dumps(out,indent=2));return P,adj,keys,tau
if __name__=='__main__':build(int(sys.argv[1]))
