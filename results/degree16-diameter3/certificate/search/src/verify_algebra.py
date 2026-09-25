"""Independent finite-field point-set and inverse checks for the retained charts."""
from pathlib import Path
import json,itertools,collections
ROOT=Path(__file__).resolve().parents[1];C=ROOT/'candidates';O=ROOT/'certificates';O.mkdir(exist_ok=True)
def arithmetic(q,s):
 def add(a,b):return a^b if q==4 else (a+b)%q
 def neg(a):return a if q==4 else -a%q
 def mul(a,b):
  if q!=4:return a*b%q
  z=0
  while b:
   if b&1:z^=a
   a<<=1;b>>=1
   if a&4:a^=7
  return z
 def plus(x,y):return tuple(add(a,b) for a,b in zip(x,y))
 def mv(A,x):
  y=[]
  for row in A:
   z=0
   for a,b in zip(row,x):z=add(z,mul(a,b))
   y.append(z)
  return tuple(y)
 def span(cols):
  U={(0,)*s}
  for c in cols:U={plus(x,tuple(mul(t,z) for z in c)) for x in U for t in range(q)}
  return frozenset(U)
 def rank(cols):
  a=[list(x) for x in cols];r=0
  for j in range(s):
   k=next((k for k in range(r,len(a)) if a[k][j]),None)
   if k is None:continue
   a[r],a[k]=a[k],a[r];iv=next(t for t in range(1,q) if mul(a[r][j],t)==1);a[r]=[mul(iv,v) for v in a[r]]
   for k in range(len(a)):
    if k!=r:
     c=a[k][j];a[k]=[add(x,neg(mul(c,y))) for x,y in zip(a[k],a[r])]
   r+=1
  return r
 return add,mul,plus,mv,span,rank

def validate(ch,iv):
 q,s=ch['q'],ch['s'];add,mul,plus,mv,span,rank=arithmetic(q,s);A=ch['matrices'];b=ch['vectors'];basis=[tuple(int(i==j) for j in range(s)) for i in range(s)]
 for t in range(len(A)):
  for e in basis:assert mv(A[iv[t]],mv(A[t],e))==e
  assert mv(A[iv[t]],b[t])==tuple(b[iv[t]])
 def red(w):
  z=[]
  for t in w:
   if z and z[-1]==iv[t]:z.pop()
   else:z.append(t)
  return tuple(z)
 def cols(w):
  z=[]
  for t in w:z=[mv(A[t],v) for v in z]+[tuple(b[t])]
  return z
 return (q,s,add,mul,plus,mv,span,rank,red,cols)

def check_s4():
 res=[]
 for q in [3,4]:
  ch=json.loads((C/f'chart{q}_s4.json').read_text());q,s,add,mul,plus,mv,span,rank,red,cols=validate(ch,[1,0,2]);N=q**s;W=[w for w in itertools.product(range(3),repeat=4) if red(w)==w];R=[w for w in itertools.product(range(3),repeat=2) if red(w)==w];full=[len(span(cols(w))) for w in W];assert full==[N]*24
  pencil=[]
  for r in R:
   core=span(cols(r));Hs={span(cols(w)) for w in itertools.product(range(3),repeat=4) if red(w)==r};Hs={H for H in Hs if len(H)==q**3};assert len(Hs)==q+1 and all(core<=H for H in Hs);assert len(set().union(*Hs))==N;pencil.append({'word':list(r),'hyperplanes':len(Hs),'core_size':len(core)})
  # Direct iteration through edge transitions, independent of control matrices.
  pts=list(itertools.product(range(q),repeat=s));trans=[]
  for t in range(3):
   trans.append({x:{plus(mv(ch['matrices'][t],x),tuple(mul(l,v) for v in ch['vectors'][t])) for l in range(q)} for x in pts})
  witness=None
  for x in pts:
   sets={():{x}};U={x};included=[()]
   for k in range(1,5):
    for w in itertools.product(range(3),repeat=k):
     sets[w]=set().union(*(trans[w[-1]][z] for z in sets[w[:-1]]))
     r=red(w)
     if not r or len(r)%2:U|=sets[w];included.append(w)
   missing=set(pts)-U
   if missing:
    y=min(missing);witness={'source':list(x),'unreachable_target':list(y),'allowed_word_count':len(included),'union_size':len(U),'fibre_size':N,'allowed_condition':'length<=4 and freely reduced length is 0,1,or3','every_allowed_word_checked':all(y not in sets[w] for w in included)};break
  assert witness
  res.append({'q':q,'s':s,'inverse_consistency':True,'all_24_length4_words_span_fibre':True,'six_complete_pencils':pencil,'subcritical_witness':witness})
 (O/'s4_independent_point_sets.json').write_text(json.dumps(res,indent=2));print('S4',res,flush=True)

def check_quartic():
 reports=[]
 for q in [3,4]:
  enumeration=json.loads((C/f'quartic_classification_q{q}.json').read_text());reps=enumeration['representatives'];checked=[]
  for i,rep in enumerate(reps):
   ch=dict(rep,q=q,s=3);q,s,add,mul,plus,mv,span,rank,red,cols=validate(ch,[1,0,3,2]);W=[w for w in itertools.product(range(4),repeat=3) if red(w)==w];sizes=[len(span(cols(w))) for w in W];ranks=[next(k for k in range(4) if q**k==n) for n in sizes];assert ranks==rep['ranks'];pencil=[];mask=0
   for j,rk in enumerate(ranks):
    if rk==3:mask|=1<<j
   for t in range(4):
    spaces={span(cols(w)) for w in itertools.product(range(4),repeat=3) if red(w)==(t,)};Hs={H for H in spaces if len(H)==q*q};pencil.append(len(Hs));assert len(Hs)==rep['pencil_counts'][t]
    if len(Hs)==q+1:
     core=span([rep['vectors'][t]]);assert all(core<=H for H in Hs);assert len(set().union(*Hs))==q**3;mask|=1<<(36+t)
   assert mask==rep['mask'];checked.append({'mask':mask,'full_words':ranks.count(3),'pencil_counts':pencil})
  reports.append({'q':q,'tested_representatives':len(checked),'scope':'independent point-set verification of retained representatives; not a second exhaustive enumeration','representatives':checked})
 (O/'quartic_representatives_independent.json').write_text(json.dumps(reports,indent=2));print('quartic representatives verified',[(d['q'],d['tested_representatives']) for d in reports],flush=True)

if __name__=='__main__':check_s4();check_quartic()
