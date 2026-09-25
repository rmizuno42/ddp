#!/usr/bin/env python3
"""An explicit 54-word certificate and the uniform rank classification.
Standard library only. Calls matrix/set helpers from verify.py, not its BFS.
"""
import itertools,json,collections
from pathlib import Path
from verify import setup,mat,I,mv,mm,span,need
here=Path(__file__).resolve().parent
D=json.loads((here/'construction.json').read_text());C,M,L,iv=setup(D)
words=[w for w in itertools.product(range(5),repeat=3) if w[1]!=iv[w[0]] and w[2]!=iv[w[1]]]
expected_bad={(0,4,2),(1,4,3),(2,4,0),(3,4,1)}
def walk(u,w):
 columns=[]
 for t in w:
  columns=[mv(M[u][t],b) for b in columns]+[L[iv[t]]];u=C[u][t]
 return u,span(columns)
for u in range(54):
 bad={w for w in words if len(walk(u,w)[1])<27}
 need(bad==expected_bad,'rank exceptions depend on the controller start')
reps={}
for w in words:
 if w not in expected_bad:
  v,H=walk(0,w);reps.setdefault(v,list(w))
need(len(reps)==49,'49 states must have a good three-step word')
need(set(range(54))-set(reps)==set(C[0]),'only the five neighbors may be omitted')
certificate=[]
for v in range(54):
 if v in reps:kind='full_rank';w=reps[v]
 else:kind='edge_pencil';w=[C[0].index(v)]
 certificate.append({'target':v,'group_coordinates':[v//9,v%9],'kind':kind,'ports':w})
need(len(certificate)==54,'incomplete certificate')
out={'uniform_over_all_54_starts':True,'number_reduced_words':80,'full_rank_words':76,'bad_words':[list(w) for w in sorted(expected_bad)],'good_word_endpoints_from_identity':49,'remaining_five_endpoints':sorted(C[0]),'first_controller_identity_return':[d for d in certificate if d['target']==0][0],'controller_generators':D['generators'],'word_certificate':certificate}
(here/'uniform_word_certificate.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='word_certificate'},indent=2))
