import numpy as np,json,time
from pathlib import Path
from scipy.optimize import milp,Bounds,LinearConstraint
from scipy.sparse import coo_matrix
R=Path(__file__).resolve().parents[1];adj=np.load(R/'geometry/polar_H3.npz')['adj'].tolist();n=len(adj)
edges=[(u,v)for u in range(n)for v in adj[u]if u<=v]
for u in range(n):edges += [(u,u)]*(4-len(adj[u]))
rows=[];cols=[];val=[]
for e,(u,v)in enumerate(edges):
 for t in range(4):
  rows.extend([e,len(edges)+4*u+t]);cols.extend([4*e+t]*2);val.extend([1]*2)
  if u!=v:rows.append(len(edges)+4*v+t);cols.append(4*e+t);val.append(1)
M=coo_matrix((val,(rows,cols)),shape=(len(edges)+4*n,4*len(edges))).tocsc();lb=np.zeros(4*len(edges));ub=np.ones_like(lb)
# fix colours around vertex0 to break S4 symmetry
es=[e for e,uv in enumerate(edges)if 0 in uv]
for t,e in enumerate(es):lb[4*e+t]=1
st=time.monotonic();res=milp(np.zeros(len(lb)),integrality=np.ones(len(lb)),bounds=Bounds(lb,ub),constraints=LinearConstraint(M,np.ones(M.shape[0]),np.ones(M.shape[0])),options={'time_limit':80})
print('status',res.message,'seconds',time.monotonic()-st,flush=True)
if res.x is not None:
 C=np.full((n,4),-1,dtype=int)
 for e,(u,v)in enumerate(edges):
  t=int(np.argmax(res.x[4*e:4*e+4]));assert C[u,t]==-1 and (u==v or C[v,t]==-1);C[u,t]=v;C[v,t]=u
 assert np.all(C>=0)
 np.savetxt(R/'candidates/polar364_coloured.adj',C,fmt='%d')
 print('saved',n,'loops',sum(C[u,t]==u for u in range(n)for t in range(4)),flush=True)
