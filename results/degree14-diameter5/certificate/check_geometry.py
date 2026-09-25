"""Optional origin audit; needs NumPy. Main proof does not require this file."""
from pathlib import Path
from collections import deque,Counter
import json,numpy as np
R=Path(__file__).resolve().parent;d=np.load(R/'geometry/polar_H3.npz');a=d['incidence_adj'].tolist();p=list(map(int,d['polarity']));n=len(a);assert n==728
for u in range(n):
 assert len(set(a[u]))==4
 assert p[p[u]]==u and (u<364)!=(p[u]<364)
 assert set(p[v]for v in a[u])==set(a[p[u]])
 for v in a[u]:assert u in a[v]and (u<364)!=(v<364)
girth=n;hist=Counter()
for root in range(n):
 ds=[-1]*n;parent=[-1]*n;ds[root]=0;todo=[root]
 for u in todo:
  for v in a[u]:
   if ds[v]<0:ds[v]=ds[u]+1;parent[v]=u;todo.append(v)
   elif parent[u]!=v:girth=min(girth,ds[u]+ds[v]+1)
 assert len(todo)==n;hist.update(ds)
assert max(hist)==6 and girth==12
C=json.loads((R/'construction.json').read_text())['controller']
assert all(set(C[u])==set(p[v]for v in a[u])for u in range(364))
result={'incidence_vertices':n,'incidence_degree':4,'incidence_diameter':6,'incidence_girth':girth,'incidence_distance_layers':dict(hist),'polarity_involution_and_incidence_preservation':True,'quotient_matches_controller_after_edge_colouring':True,'controller_semiloops':sum(u in C[u]for u in range(364))}
(R/'geometry_certificate.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
