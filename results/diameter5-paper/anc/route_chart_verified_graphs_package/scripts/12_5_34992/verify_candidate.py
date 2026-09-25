from collections import deque, defaultdict
MOD4, MOD6, NBASE, S = 4, 6, 6, 5
HSIZE = MOD4 * MOD6
Q = 3
EDGE_DATA = [(0,2,1,0),(0,3,2,4),(0,4,2,0),(0,4,2,5),(1,2,1,2),(1,3,3,5),(1,5,1,1),(1,5,1,0),(2,4,2,2),(2,5,1,5),(3,4,1,5),(3,5,3,1)]

def gid(x,y): return (x%MOD4)*MOD6 + (y%MOD6)
# ---------- controller ----------
def verify_base_voltage_coverage():
    adj=[[] for _ in range(NBASE)]
    for eid,(u,v,x,y) in enumerate(EDGE_DATA):
        adj[u].append((v,eid,x%MOD4,y%MOD6)); adj[v].append((u,eid,(-x)%MOD4,(-y)%MOD6))
    sums=[[set() for _ in range(NBASE)] for __ in range(NBASE)]
    def rec(st,u,last,d,x,y):
        if d==S: sums[st][u].add(gid(x,y)); return
        for v,eid,dx,dy in adj[u]:
            if eid!=last: rec(st,v,eid,d+1,x+dx,y+dy)
    for s in range(NBASE): rec(s,s,-1,0,0,0)
    bad=[]
    for i in range(NBASE):
        for j in range(NBASE):
            miss=set(range(HSIZE))-sums[i][j]
            if miss: bad.append((i,j,sorted(miss),len(sums[i][j])))
    assert not bad, f'base voltage coverage failed: {bad[:5]}'

def build_controller():
    edges=[]; seen=set()
    for beid,(u,v,xv,yv) in enumerate(EDGE_DATA):
        for x in range(MOD4):
            for y in range(MOD6):
                a=u*HSIZE+gid(x,y); b=v*HSIZE+gid(x+xv,y+yv)
                key=(a,b) if a<b else (b,a)
                if key in seen: raise AssertionError(f'duplicate controller edge {key}')
                seen.add(key); edges.append((key[0],key[1],beid))
    n=NBASE*HSIZE; adj=[[] for _ in range(n)]
    for eid,(u,v,beid) in enumerate(edges): adj[u].append((v,eid)); adj[v].append((u,eid))
    assert all(len(a)==4 for a in adj), sorted(set(len(a) for a in adj))
    q=deque([0]); seenv={0}
    while q:
        u=q.popleft()
        for v,eid in adj[u]:
            if v not in seenv: seenv.add(v); q.append(v)
    assert len(seenv)==n, f'disconnected controller {len(seenv)}/{n}'
    return adj,edges

def euler_2factor_coloring(adj,edges):
    n=len(adj); m=len(edges); used=[False]*m; it=[0]*n; stack=[(0,-1)]; circuit=[]
    while stack:
        u,ine=stack[-1]
        while it[u]<len(adj[u]) and used[adj[u][it[u]][1]]: it[u]+=1
        if it[u]==len(adj[u]): circuit.append(stack.pop())
        else:
            v,eid=adj[u][it[u]]; used[eid]=True; stack.append((v,eid))
    order=[e for _,e in reversed(circuit)][1:]
    assert len(order)==m and all(used)
    color={eid:(k&1) for k,eid in enumerate(order)}
    deg=[[0,0] for _ in range(n)]
    for eid,(u,v,_) in enumerate(edges): c=color[eid]; deg[u][c]+=1; deg[v][c]+=1
    assert all(d==[2,2] for d in deg)
    return color

def orient_two_factors(adj,edges,color):
    n=len(adj); arc={}
    for c in (0,1):
        sub=[[] for _ in range(n)]
        for eid,(u,v,_) in enumerate(edges):
            if color[eid]==c: sub[u].append((v,eid)); sub[v].append((u,eid))
        f,inv=(0,1) if c==0 else (2,3); used=set()
        for st in range(n):
            for nxt,e0 in sub[st]:
                if e0 in used: continue
                cyc=[st]; u=nxt; e=e0
                while True:
                    used.add(e); cyc.append(u); opts=sub[u]
                    v,ne = opts[1] if opts[0][1]==e else opts[0]
                    if v==st:
                        used.add(ne); arc[(u,st)]=f; arc[(st,u)]=inv; break
                    u,e=v,ne
                for a,b in zip(cyc[:-1],cyc[1:]): arc[(a,b)]=f; arc[(b,a)]=inv
    invsym={0:1,1:0,2:3,3:2}; cnt=[defaultdict(int) for _ in range(n)]
    for (u,v),s in arc.items(): cnt[u][s]+=1; assert arc[(v,u)]==invsym[s]
    assert all(all(cnt[u][s]==1 for s in range(4)) for u in range(n))
    return arc

def verify_labeled_nb5(adj,arc):
    inv={0:1,1:0,2:3,3:2}; n=len(adj); bad=[]
    for s in range(n):
        reach=set()
        def rec(u,prev,d,last):
            if d==S: reach.add(u); return
            for v,eid in adj[u]:
                if v==prev: continue
                sym=arc[(u,v)]; assert last is None or sym!=inv[last]
                rec(v,u,d+1,sym)
        rec(s,-1,0,None)
        if len(reach)!=n: bad.append((s,n-len(reach)))
    assert not bad, f'NB5 labeled coverage failed: {bad[:5]}'
# ---------- GF(3)^5 chart ----------
A = [
[[1,2,0,2,0],[1,2,1,2,0],[1,2,1,1,0],[2,0,0,0,0],[1,2,2,0,1]],
[[0,0,0,2,0],[2,2,1,2,0],[2,1,0,0,0],[0,1,2,0,0],[1,0,1,0,1]],
[[2,1,0,0,0],[0,1,1,0,0],[2,2,0,1,0],[2,0,1,0,0],[2,2,1,1,1]],
[[1,2,0,1,0],[2,2,0,1,0],[1,2,0,2,0],[0,1,1,2,0],[2,1,2,1,1]]]
B = [[2,2,2,0,0],[0,1,0,0,1],[2,1,2,0,2],[1,0,1,0,2]]
SINV={0:1,1:0,2:3,3:2}
def mm(X,Y): return [[sum(X[i][k]*Y[k][j] for k in range(len(Y)))%Q for j in range(len(Y[0]))] for i in range(len(X))]
def mv(M,v): return [sum(M[i][j]*v[j] for j in range(len(v)))%Q for i in range(len(M))]
def rank_cols(cols):
    n=len(cols[0]); m=len(cols); M=[list(row) for row in zip(*cols)]; r=0
    for c in range(m):
        piv=None
        for i in range(r,n):
            if M[i][c]%Q: piv=i; break
        if piv is None: continue
        M[r],M[piv]=M[piv],M[r]
        inv=1 if M[r][c]==1 else 2
        M[r]=[(inv*x)%Q for x in M[r]]
        for i in range(n):
            if i!=r and M[i][c]:
                f=M[i][c]
                M[i]=[(M[i][j]-f*M[r][j])%Q for j in range(m)]
        r+=1
        if r==n: return r
    return r

def verify_chart():
    I=[[1 if i==j else 0 for j in range(5)] for i in range(5)]
    for p,q in [(0,1),(2,3)]:
        assert mm(A[p],A[q])==I and mm(A[q],A[p])==I
        assert mv(A[q],B[p])==B[q] and mv(A[p],B[q])==B[p]
    words=[]
    def gen(w):
        if len(w)==5: words.append(tuple(w)); return
        for s in range(4):
            if not w or s!=SINV[w[-1]]: w.append(s); gen(w); w.pop()
    gen([]); mr=99
    for w in words:
        suff=I; cols=[]
        for s in reversed(w): cols.append(mv(suff,B[s])); suff=mm(suff,A[s])
        r=rank_cols(cols); mr=min(mr,r); assert r==5, (w,r)
    return len(words),mr
if __name__=='__main__':
    verify_base_voltage_coverage()
    adj,edges=build_controller(); color=euler_2factor_coloring(adj,edges); arc=orient_two_factors(adj,edges,color); verify_labeled_nb5(adj,arc)
    nw,mr=verify_chart()
    print('Base voltage coverage over C4 x C6: OK')
    print('Controller: OK; 144 vertices, simple 4-regular, exact labeled NB length-5 coverage')
    print(f'GF(3)^5 universal chart: OK; {nw} reduced words checked, min rank {mr}; inverse-symbol data verified')
    print('Certificate complete: degree 12, diameter <=5, vertices = 144*3^5 = 34992')
