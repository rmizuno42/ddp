"""Generate the undirected simple affine lift. Requires NumPy."""
import numpy as np,json,hashlib
from pathlib import Path
R=Path(__file__).resolve().parent;d=json.loads((R/'chart.json').read_text());q=s=5;Q=q**s
A=np.asarray(d['matrices'],dtype=np.int64);b=np.asarray(d['vectors'],dtype=np.int64);C=np.loadtxt(R/'controller.adj',dtype=np.int64);n=len(C)*Q
powers=q**np.arange(s,dtype=np.int64);X=(np.arange(Q)[:,None]//powers)%q
relation=[]
for t in range(3):
 Y=(X@A[t].T)[:,None,:]+np.arange(q)[None,:,None]*b[t][None,None,:]
 relation.append((Y%q@powers).reshape(-1))
E=[]
for u in range(len(C)):
 U=u*Q+np.repeat(np.arange(Q),q)
 for t in range(3):
  V=C[u,t]*Q+relation[t];good=U<V;E.append(np.stack((U[good],V[good]),axis=1))
E=np.unique(np.concatenate(E),axis=0);degrees=np.bincount(E.ravel(),minlength=n);assert int(max(degrees))<=15
path=R/f'graph_d15_D5_n{n}.edges'
with path.open('w')as f:
 f.write(f'{n} {len(E)}\n');np.savetxt(f,E,fmt='%d')
values,counts=np.unique(degrees,return_counts=True)
meta={'vertices':n,'edges':len(E),'degree_hist':dict(zip(map(str,values),map(int,counts))),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
(R/'graph_metadata.json').write_text(json.dumps(meta,indent=2));print(meta)
