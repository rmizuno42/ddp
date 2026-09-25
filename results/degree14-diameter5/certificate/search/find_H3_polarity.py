import numpy as np,json,itertools,time
from pathlib import Path
from collections import deque,Counter
R=Path(__file__).resolve().parents[1];h=np.load(R/'geometry/hexagon_q3.npz');P=h['points'];adj=h['adj'];tau=h['tau'];n=len(P)
# point images of the SL(3,3) subgroup in Zorn coordinates
lookup={tuple(v):i for i,v in enumerate(P)};lp={}
for line in range(n,2*n):
 for x,y in itertools.combinations(adj[line],2):lp[tuple(sorted((int(x),int(y))))]=line
perms=[]
for i in range(3):
 for j in range(3):
  if i==j:continue
  for c in [1,2]:
   X=P.copy();X[:,1+i]=(X[:,1+i]+c*X[:,1+j])%3;X[:,4+j]=(X[:,4+j]-c*X[:,4+i])%3
   perm=np.empty(2*n,dtype=np.int16)
   for v in range(n):
    x=X[v];first=np.flatnonzero(x)[0];x=x*int(x[first])%3;perm[v]=lookup[tuple(x)]
   for l in range(n,2*n):perm[l]=lp[tuple(sorted(map(int,perm[adj[l][:2]])))]
   assert all(set(map(int,perm[adj[u]]))==set(map(int,adj[perm[u]]))for u in range(2*n))
   perms.append(perm)
sigma=np.arange(2*n)
for k in range(3):sigma=tau[sigma]
print('sigma order4',np.all(sigma[sigma[sigma[sigma]]]==np.arange(2*n)),flush=True)
identity=np.arange(2*n,dtype=np.int16);seen={identity.tobytes()};q=deque([identity]);num=0;polar=None
while q:
 g=q.popleft();num+=1;d=sigma[g]
 if np.array_equal(d[d],identity):polar=d;break
 for a in perms:
  ng=a[g];key=ng.tobytes()
  if key not in seen:seen.add(key);q.append(ng)
print('tested',num,'subgroup explored',len(seen),'found',polar is not None,flush=True)
if polar is None:raise SystemExit(0)
# quotient identified with points; a line l maps to point polar(l)
Q=np.array([[int(polar[l])for l in adj[p]]for p in range(n)],dtype=np.int16)
assert all(u in Q[v]for u in range(n)for v in Q[u]);assert all(len(set(row))==4 for row in Q)
loops=[u for u in range(n)if u in Q[u]]
# Verify exact odd<=5 support from any root; expected full and 324 singleton reduced5
walks=[];allhist=Counter();counts=[]
for u in range(n):
 ct=[[int(i==u)for i in range(n)]]
 for l in range(5):
  z=[0]*n
  for v in range(n):
   for w in Q[v]:z[w]+=ct[-1][v]
  ct.append(z)
 assert all(ct[5][v]>0 for v in range(n))
 allhist.update(ct[5]);counts.append(ct[5])
print('loops',len(loops),'odd5count histogram',allhist)
np.savez_compressed(R/'geometry/polar_H3.npz',adj=Q,polarity=polar,incidence_adj=adj)
(R/'candidates/polar_H3_unlabelled.adj').write_text('\n'.join(' '.join(map(str,row))for row in Q)+'\n')
(R/'certificates/polar_H3.json').write_text(json.dumps({'n':n,'semi_degree':4,'fixed_points':loops,'subgroup_candidates_tested':num,'ordinary_length5_walk_histogram':dict(allhist),'polarity':list(map(int,polar))},indent=2))
