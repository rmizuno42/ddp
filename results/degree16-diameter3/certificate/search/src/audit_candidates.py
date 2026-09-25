"""Independent candidate checks; no search scores are trusted. Python + NumPy + Numba."""
from pathlib import Path
import json,itertools,collections,hashlib
import numpy as np
from numba import njit
ROOT=Path(__file__).resolve().parents[1]
CAND=ROOT/'candidates'; OUT=ROOT/'certificates';OUT.mkdir(exist_ok=True)
def loadC(p,labels=3):
 C=np.loadtxt(p,dtype=np.int32).reshape(-1,labels);n=len(C);iv=[1,0,2] if labels==3 else [1,0,3,2]
 assert np.all((C>=0)&(C<n))
 for t in range(labels):assert np.array_equal(C[C[:,t],iv[t]],np.arange(n))
 return C
@njit
def bfs(adj,source):
 n=len(adj);d=np.full(n,-1,np.int32);pr=np.full(n,-1,np.int32);que=np.empty(n,np.int32);d[source]=0;que[0]=source;head=0;tail=1
 while head<tail:
  u=que[head];head+=1
  for v in adj[u]:
   if d[v]<0:d[v]=d[u]+1;pr[v]=u;que[tail]=v;tail+=1
 return d,pr

def path(pr,s,t):
 z=[int(t)]
 while z[-1]!=s:
  if pr[z[-1]]<0:return None
  z.append(int(pr[z[-1]]))
 return z[::-1]

def check_weighted():
 report=[]
 for mode in ('weighted','reflected'):
  ch=json.loads((CAND/('reflection_chart.json' if mode=='reflected' else 'original_chart100k.json')).read_text());A=np.array(ch['matrices']);b=np.array(ch['vectors']);offsets=np.array(ch.get('offsets',[[0]*5 for _ in range(3)]))
  q=5;s=5;nf=3125;pts=(np.arange(nf)[:,None]//(5**np.arange(5)))%5;wei=5**np.arange(5)
  for n,r in [(16,2),(20,3),(22,4),(24,4)]:
   prefix=f'{mode}_c{n}_r{r}';C=loadC(CAND/(prefix+'.adj'));LS=[list(range(5)),list(range(5)),{2:[1,4],3:[0,1,4],4:[1,2,3,4]}[r]];N=n*nf
   neigh=[]
   for t in range(3):
    y=(pts@A[t].T+offsets[t])%5
    maps=(((y[:,None,:]+np.array(LS[t])[None,:,None]*b[t])%5)@wei).astype(np.int32)
    neigh.append((C[:,t,None,None]*nf+maps[None,:,:]).reshape(N,len(LS[t])))
   adj=np.concatenate(neigh,axis=1)
   keys=np.unique(np.arange(N,dtype=np.int64)[:,None]*N+adj)
   keys=keys[keys//N!=keys%N];rev=(keys%N)*N+keys//N;assert np.array_equal(keys,np.sort(rev))
   deg=np.bincount(keys//N,minlength=N);assert deg.max()<=10+r
   missing=0;first=None
   for u in range(n):
    d,pr=bfs(adj,u*nf); bad=np.where((d>5)|(d<0))[0];missing+=len(bad)
    if first is None and len(bad):
     v=int(bad[0]);first={'source':u*nf,'target':v,'distance':int(d[v]),'path':path(pr,u*nf,v),'target_controller':v//nf,'target_fibre_little_endian':[int(v%nf//5**j%5) for j in range(5)],'source_distance_histogram':dict(zip(map(str,*[np.unique(d).tolist()]),map(int,np.bincount(d)))) if np.all(d>=0) else {}}
   saved=json.loads((CAND/(prefix+'.json')).read_text());assert missing==saved['x0_missing_ordered_endpoints'],(prefix,missing,saved)
   res={'candidate':prefix,'order':N,'max_degree':int(deg.max()),'edges':len(keys)//2,'simple_undirected':True,'checked_sources':n,'scope':'one zero-fibre source for every controller vertex; NOT all graph sources','missing_ordered_endpoints_at_radius5':missing,'search_score_agrees':True,'counterexample':first,'chart':'reflection_chart.json' if mode=='reflected' else 'original_chart100k.json'}
   report.append(res);print(prefix,missing,first['distance'],flush=True)
 (OUT/'weighted_independent_bfs.json').write_text(json.dumps(report,indent=2))

def check_s7():
 ans=[];q=5;s=7
 for f in sorted(CAND.glob('s7_voltage*.adj')):
  C=loadC(f);n=len(C);worst=0;far=None;cap=None
  for u in range(n):
   d,pr=bfs(C,u);worst=max(worst,int(d.max()))
   if far is None and (d>7).any():
    v=int(np.where(d>7)[0][0]);far={'source':u,'target':v,'distance':int(d[v]),'path':path(pr,u,v)}
   counts=np.zeros((s+1,n),dtype=np.int64);counts[0,u]=1
   for ell in range(1,s+1):
    for v in range(n):
     for t in range(3):counts[ell,C[v,t]]+=counts[ell-1,v]
   caps=sum(counts[k]*q**k for k in range(s+1))
   if cap is None and (caps<q**s).any():
    v=int(np.where(caps<q**s)[0][0]);cap={'source':u,'target':v,'walk_counts_lengths_0_to_7':list(map(int,counts[:,v])),'capacity_upper_bound':int(caps[v]),'required_fibre_points':q**s,'distance':int(d[v])}
  ans.append({'candidate':f.stem,'controller_order':n,'lift_order_if_successful':n*q**s,'max_degree_bound':15,'controller_diameter':worst,'distance_obstruction':far,'route_capacity_obstruction':cap})
 (OUT/'s7_controller_audit.json').write_text(json.dumps(ans,indent=2));print('S7',ans,flush=True)

if __name__=='__main__':
 check_weighted();check_s7()
