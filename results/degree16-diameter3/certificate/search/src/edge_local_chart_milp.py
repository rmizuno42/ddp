"""Choose the one deficient turn at each controller edge, then realize it over F4.
The controller must have odd-walk radius at most three. No solver conclusion alone
is trusted: verify the chosen assignment, ranks, pencils, and graph separately.
"""
from pathlib import Path
import sys,json,itertools,collections,time
import numpy as np
from scipy.optimize import milp,Bounds,LinearConstraint
from scipy.sparse import csc_array
from audit_candidates import loadC
from verify_algebra import arithmetic
P=Path(__file__).resolve().parents[1];name=sys.argv[1];C=loadC(P/'candidates'/f'{name}.adj',4);n=len(C);inv=(1,0,3,2)
edge_of={};edges=[];opts=[]
for u in range(n):
 for t in range(4):
  if (u,t) in edge_of:continue
  v=int(C[u,t]);j=inv[t];e=len(edges);edges.append((u,t,v,j));edge_of[u,t]=(e,False);edge_of[v,j]=(e,True);opts.append([(i,k) for i in range(4) if i!=t for k in range(4) if k!=j])
clauses=[];empty=[];ignored=0;routes=collections.defaultdict(list)
for u in range(n):
 for w in itertools.product(range(4),repeat=3):
  if w[1]==inv[w[0]] or w[2]==inv[w[1]]:continue
  v1=int(C[u,w[0]]);v2=int(C[v1,w[1]]);v=int(C[v2,w[2]])
  e,rev=edge_of[v1,w[1]];pair=(inv[w[0]],w[2]) if not rev else (w[2],inv[w[0]])
  k=opts[e].index(pair);routes[u,v].append((9*e+k,w))
for u in range(n):
 for v in range(n):
  if v in C[u]:continue
  literals=sorted(set(lit for lit,w in routes[u,v]))
  if not literals:empty.append((u,v));continue
  if len(set(lit//9 for lit in literals))<len(literals):ignored+=1;continue
  clauses.append(literals)
res={'controller':name,'controller_order':n,'edge_variables':len(edges),'constraints':len(clauses),'automatically_satisfied_pairs':ignored,'no_odd_route_pairs':empty}
if empty:
 res['status']='controller fails necessary screen for this certificate';(P/'candidates'/f'{name}_edge_local.json').write_text(json.dumps(res,indent=2));print(json.dumps(res));sys.exit()
rows=[];cols=[];data=[];lb=[];ub=[]
for e in range(len(edges)):
 row=len(lb);lb.append(1);ub.append(1)
 for k in range(9):rows.append(row);cols.append(9*e+k);data.append(1)
for cl in clauses:
 row=len(lb);lb.append(-np.inf);ub.append(len(cl)-1)
 for lit in cl:rows.append(row);cols.append(lit);data.append(1)
A=csc_array((np.array(data,dtype=float),(np.array(rows,dtype=np.int32),np.array(cols,dtype=np.int32))),shape=(len(lb),9*len(edges)))
start=time.time();sol=milp(c=np.zeros(A.shape[1]),integrality=np.ones(A.shape[1],dtype=np.uint8),bounds=Bounds(0,1),constraints=LinearConstraint(A,np.array(lb),np.array(ub)),options={'time_limit':60})
res.update(solver_status=int(sol.status),solver_message=str(sol.message),seconds=time.time()-start)
if sol.x is None:
 res['status']='no assignment returned';(P/'candidates'/f'{name}_edge_local.json').write_text(json.dumps(res,indent=2));print(json.dumps(res));sys.exit()
x=np.rint(sol.x).astype(int);assert np.all(x.reshape(-1,9).sum(1)==1);assert all(sum(x[i] for i in cl)<len(cl) for cl in clauses);choices=np.argmax(x.reshape(-1,9),axis=1).tolist();print('feasible choices',choices,flush=True)
q=4;s=3;add,mul,plus,mv,span,rank=arithmetic(q,s);L=[(1,0,0),(0,1,0),(0,0,1),(1,1,1)]
def mm(A,B):return [list(mv(A,col)) for col in zip(*B)] # transpose below

def matmul(A,B):return [list(row) for row in zip(*mm(A,B))]
def inverse(A):
 T=[list(row)+[int(i==j) for j in range(3)] for i,row in enumerate(A)]
 for j in range(3):
  k=next(k for k in range(j,3) if T[k][j]);T[k],T[j]=T[j],T[k];ivv=next(v for v in range(1,4) if mul(T[j][j],v)==1);T[j]=[mul(v,ivv) for v in T[j]]
  for k in range(3):
   if k!=j:
    m=T[k][j];T[k]=[a^mul(m,b) for a,b in zip(T[k],T[j])]
 return [r[3:] for r in T]
def base(v):
 E=[(1,0,0),(0,1,0),(0,0,1)]
 for a,b in itertools.combinations(E,2):
  if rank([a,b,v])==3:return [list(row) for row in zip(a,b,v)]
lib={}
for t in range(4):
 U=base(L[t]);V=base(L[inv[t]]);Ui=inverse(U);dic={}
 for a,b,c,d in itertools.product(range(4),repeat=4):
  if mul(a,d)==mul(b,c):continue
  D=[[a,b,0],[c,d,0],[0,0,1]];M=matmul(matmul(V,D),Ui);bad=[]
  assert mv(M,L[t])==L[inv[t]]
  for i in range(4):
   if i==t:continue
   for j in range(4):
    if j==inv[t]:continue
    if rank([mv(M,L[i]),L[inv[t]],L[j]])<3:bad.append((i,j))
  if len(bad)==1:
   H={span([L[inv[t]],z]) for z in L+[mv(M,v) for v in L]};H={h for h in H if len(h)==16};assert len(H)==5 and len(set().union(*H))==64
   dic.setdefault(bad[0],M)
 assert len(dic)==9;lib[t]=dic
matrices=[[None]*4 for _ in range(n)]
for e,((u,t,v,j),k) in enumerate(zip(edges,choices)):
 M=lib[t][opts[e][k]];matrices[u][t]=M;matrices[v][j]=inverse(M)
cert=[];counts=collections.Counter()
for u in range(n):
 for v in range(n):
  if v in C[u]:
   t=next(t for t in range(4) if C[u,t]==v);cert.append({'u':u,'v':v,'kind':'edge_pencil','word':[t]});counts['edge_pencil']+=1;continue
  found=False
  for lit,w in routes[u,v]:
   if x[lit]:continue
   pos=u;col=[]
   for t in w:
    col=[mv(matrices[pos][t],z) for z in col]+[L[inv[t]]];pos=int(C[pos,t])
   assert pos==v and rank(col)==3;cert.append({'u':u,'v':v,'kind':'full_rank','word':list(w)});counts['full_rank']+=1;found=True;break
  assert found
res.update(status='verified_feasible_edge_local_certificate',q=4,dimension=3,lift_order=n*64,degree_upper_bound=16,diameter_upper_bound=3,edges=edges,bad_turn_choices=[list(opts[e][k]) for e,k in enumerate(choices)],controller=C.tolist(),outgoing_return_directions=[list(v) for v in L],matrices=matrices,certificate_counts=dict(counts),pair_certificate=cert)
(P/'candidates'/f'{name}_edge_local.json').write_text(json.dumps(res,indent=2));print({k:v for k,v in res.items() if k not in ['edges','bad_turn_choices','controller','outgoing_return_directions','matrices','pair_certificate']},flush=True)
