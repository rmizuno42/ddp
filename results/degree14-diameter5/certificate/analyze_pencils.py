"""Optional stronger subcertificate: boundary-only translations at each edge."""
import verify_small as s
from collections import Counter
import json
counts=Counter();yes=[]
for u in range(s.n):
 for t in range(4):
  K=s.rr((tuple(s.b[t]),s.mv(s.A[t],s.cs[u]),s.cs[s.C[u][t]]))
  planes=set();bits=0
  for w in s.families[t]:
   st=s.states(u,w);ds=s.transported(w,st);basis=s.rr(s.control(w)[1]+(ds[0],ds[3]));bits|=s.image_basis(basis)
   if len(basis)==4:planes.add(basis)
  counts[(len(K),len(planes),bits.bit_count())]+=1
  if len(K)==3 and len(planes)==4:yes.append([u,t])
result={'note':'Optional narrower proof family; the main certificate uses all insertion positions and is valid for all pairs.','pairs_with_complete_boundary_pencil':len(yes),'histogram':{str(k):v for k,v in counts.items()}}
(s.R/'boundary_pencil_analysis.json').write_text(json.dumps(result,indent=2));print(result)
