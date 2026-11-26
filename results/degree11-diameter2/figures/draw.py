"""Draw the published edge list and its orbit matrix. Requires Matplotlib 3.7+."""
import json
import math
import string
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, PathPatch, Rectangle
from matplotlib.path import Path as Curve

HERE = Path(__file__).resolve().parent
CERT = HERE.parent/'certificate'
DATA = json.loads((CERT/'orbits.json').read_text())
EDGES = [tuple(map(int,s.split())) for s in (CERT/'graph.edges').read_text().splitlines()[1:]]
INK, MUTED, LINE, PAPER = '#172f37', '#425e65', '#cfdbda', '#fffefa'
FIXED, CENTER, OUTER = '#694678', '#006f73', '#b1572b'
PALETTE = (FIXED,CENTER,OUTER)
FIXED_XY = [(0.516,.799),(.249,.341),(1,.859),(.064,.491),(.282,.733),(0,.723),
            (.67,1),(.349,.976),(.009,.234),(.15,.243),(.691,.184),(.513,.397),
            (.609,0),(.997,.28),(.819,.708),(.818,.445),(.091,.076)]
RADII = [174,151,191,228,208,244,132,269,300,283,325,309,339]
# Phase in units of one seventh-turn; the same angle increment is used in every fibre.
PHASES = [.02,.37,.75,.16,.51,.84,.66,.12,2.35,1.51,4.71,3.81,5.97]
LETTERS = string.ascii_uppercase
matplotlib.rcParams.update({'font.family':'DejaVu Sans','svg.fonttype':'none','svg.hashsalt':'ddp108-v1',
                            'pdf.fonttype':42, 'axes.unicode_minus':True})


def plate(height):
    fig=plt.figure(figsize=(12.4,height/100),facecolor=PAPER)
    ax=fig.add_axes([0,0,1,1],xlim=(0,1240),ylim=(height,0),aspect='equal')
    ax.axis('off')
    return fig,ax


def label(ax,x,y,s,size=12,color=INK,**style):
    return ax.text(x,y,s,fontsize=size,color=color,va='center',zorder=9,**style)


def rule(ax,x,y,x2,y2,color=LINE):
    ax.plot([x,x2],[y,y2],color=color,lw=.7,zorder=0)


def disk(ax,x,y,r,color,**kw):
    p=Circle((x,y),r,facecolor=color,**kw);ax.add_patch(p)
    return p


def save(fig,name):
    for ext,meta in [('svg',{'Date':None}),('pdf',{'CreationDate':None,'ModDate':None}),('png',{})]:
        fig.savefig(HERE/f'{name}.{ext}',dpi=180,metadata=meta,facecolor=PAPER)
    plt.close(fig)


def role(v):
    return 0 if v<17 else (1 if v<66 else 2)


def positions():
    xy=[((x-.5)*101,(y-.5)*76) for x,y in FIXED_XY]
    for i,(r,phase) in enumerate(zip(RADII,PHASES)):
        for k in range(7):
            a=math.tau*(k+phase)/7-math.pi/2
            xy.append((r*math.cos(a),r*math.sin(a)))
    return xy


def wire(xy,e):
    """Route mobile-to-mobile chords around the core with an equivariant circular detour."""
    u,v=e
    a,b=xy[u],xy[v]
    if u>=17:
        theta,phi=math.atan2(a[1],a[0]),math.atan2(b[1],b[0])
        angle=(phi-theta+math.pi)%math.tau-math.pi
        r,s=math.hypot(*a),math.hypot(*b)
        # Bend long chords only. Keeping the inner area clear separates the fixed subgraph.
        bend=min(1,max(0,(abs(angle)-1.35)/1.15))*.74
        if bend>0:
            points=[]
            for j in range(37):
                t=j/36
                direct=((1-t)*a[0]+t*b[0],(1-t)*a[1]+t*b[1])
                rad=(1-t)*r+t*s;phi=theta+t*angle
                arc=(rad*math.cos(phi),rad*math.sin(phi))
                points.append(tuple((1-bend)*d+bend*k for d,k in zip(direct,arc)))
            return points
    return [a,b]


def clearances(points, coordinates):
    starts=points[:-1]
    directions=points[1:]-starts
    offsets=coordinates[:,None,:]-starts
    t=np.clip(np.sum(offsets*directions,axis=2)/np.sum(directions**2,axis=1),0,1)
    return np.linalg.norm(offsets-t[:,:,None]*directions,axis=2).min(axis=1)


def detour(points, center, radius):
    """Replace each excursion inside a vertex disk by the shorter boundary arc."""
    out=[points[0]]
    entry=None
    for a,b in zip(points,points[1:]):
        direction=b-a
        offset=a-center
        norm=direction@direction
        middle=-(direction@offset)/norm
        gap=radius**2-np.sum((offset+middle*direction)**2)
        if gap>1e-12:
            span=math.sqrt(gap/norm)
            for t,entering in [(middle-span,True),(middle+span,False)]:
                if not 0<t<=1:continue
                hit=a+t*direction
                if entering:
                    entry=math.atan2(*(hit-center)[::-1])
                    out.append(hit)
                elif entry is not None:
                    angle=math.atan2(*(hit-center)[::-1])
                    delta=(angle-entry+math.pi)%math.tau-math.pi
                    count=max(1,math.ceil(abs(delta)/.12))
                    for step in range(1,count+1):
                        theta=entry+delta*step/count
                        out.append(center+radius*np.array([math.cos(theta),math.sin(theta)]))
                    entry=None
        if entry is None and np.linalg.norm(out[-1]-b)>1e-9:
            out.append(b)
    assert entry is None
    return np.array(out)


def routed_edges(xy):
    coordinates=np.array(xy)
    radii=np.array([5.3 if i<17 else 6.35 for i in range(108)])
    separations=np.linalg.norm(coordinates[:,None,:]-coordinates[None,:,:],axis=2)
    assert np.all((separations+np.eye(108)*1000)>radii[:,None]+radii[None,:])
    result={};minimum=float('inf')
    for u,v in EDGES:
        path=np.array(wire(xy,(u,v)))
        distances=clearances(path,coordinates)
        distances[[u,v]]=np.inf
        for i in np.flatnonzero(distances<radii-1e-8):
            path=detour(path,coordinates[i],radii[i])
        distances=clearances(path,coordinates)
        distances[[u,v]]=np.inf
        assert np.all(distances>=radii-.025)
        minimum=min(minimum,float(distances.min()))
        result[u,v]=path
    return result,minimum


def full_graph():
    fig,ax=plate(846)
    label(ax,42,48,'The 108-vertex graph',30,fontfamily='DejaVu Serif')
    label(ax,43,89,'Degree 11   /   Diameter 2   /   594 edges',14,MUTED)
    rule(ax,42,119,1198,119)
    cx,cy=405,484
    xy=positions()
    paths,minimum=routed_edges(xy)
    P={(0,0):('#805988',.66,.91),(0,1):('#94749b',.42,.54),
       (1,1):('#137a7a',.72,.74),(1,2):('#447a80',.44,.42),(2,2):('#b9663a',.72,.75)}
    def kind(e):return role(e[0]),role(e[1])
    order=[(1,2),(0,1),(1,1),(2,2),(0,0)]
    for e in sorted(EDGES,key=lambda e:order.index(kind(e))):
        col,width,alpha=P[kind(e)]
        pts=[(cx+x,cy+y) for x,y in paths[e]]
        patch=PathPatch(Curve(pts),fill=False,lw=width,edgecolor=col,alpha=alpha,zorder=2,
                        capstyle='round',joinstyle='round',gid=f'edge-{e[0]}-{e[1]}')
        ax.add_patch(patch)
    for v,(x,y) in enumerate(xy):
        disk(ax,cx+x,cy+y,3.45 if v<17 else 4.65,PALETTE[role(v)],
             edgecolor=PAPER,linewidth=.73,zorder=5,gid=f'vertex-{v}')
        if 59<=v<=65:
            disk(ax,cx+x,cy+y,2.55,PAPER,linewidth=0,zorder=6)
    rule(ax,778,148,778,805)
    label(ax,812,166,'Reading the symmetry',19,fontfamily='DejaVu Serif')
    label(ax,812,203,'One step adds 1 modulo 7 to every',12,MUTED)
    label(ax,812,226,'fibre coordinate. The 91 moving points',12,MUTED)
    label(ax,812,249,'advance together by a seventh-turn.',12,MUTED)
    for n,(color,words) in enumerate(zip(PALETTE,['17 fixed vertices','49 vertices on 7 centre fibres','42 vertices on 6 outer fibres'])):
        y=297+33*n
        disk(ax,820,y,5,color,linewidth=0,zorder=5)
        label(ax,838,y,words,12)
    label(ax,812,384,'Hollow points mark one 7-point orbit.',10.5,MUTED)
    rule(ax,812,411,1197,411)
    label(ax,812,440,'The fixed subgraph',19,fontfamily='DejaVu Serif')
    label(ax,812,473,'The 17 central points, enlarged',12,MUTED)
    inset=[(835+330*x,512+215*y) for x,y in FIXED_XY]
    for u,v in EDGES:
        if v<17:
            a,b=inset[u],inset[v]
            ax.plot([a[0],b[0]],[a[1],b[1]],lw=.94,color='#9a85a1',zorder=2)
    for v,(x,y) in enumerate(inset):
        disk(ax,x,y,10.6,FIXED,edgecolor=PAPER,linewidth=.9,zorder=5)
        label(ax,x,y,str(v),8.0,'white',ha='center',weight='bold')
    label(ax,812,778,'Each fixed vertex has four neighbours',11.8,MUTED)
    label(ax,812,801,'here and seven on one centre fibre.',11.8,MUTED)
    save(fig,'n112_108_symmetry')
    # Compare all drawn IDs with the certificate, and check the displayed rotation on every moving edge.
    trans=DATA['translation']; edges=set(EDGES)
    angle=math.tau/7
    def rotate(p):return (p[0]*math.cos(angle)-p[1]*math.sin(angle),p[0]*math.sin(angle)+p[1]*math.cos(angle))
    for v in range(17,108):assert math.dist(rotate(xy[v]),xy[trans[v]])<1e-8
    for e in EDGES:
        u,v=e;image=(trans[u],trans[v])
        assert tuple(sorted(image)) in edges
        if u<17:continue
        first,last=paths[e],paths[image]
        assert len(first)==len(last) and all(math.dist(rotate(p),q)<1e-8 for p,q in zip(first,last))
    return {f'{a}-{b}':sum(kind(e)==(a,b) for e in EDGES) for a,b in order},minimum


def pretty_ids(vertices):
    if len(vertices)>1 and vertices[-1]-vertices[0]+1==len(vertices):
        return f'{vertices[0]}–{vertices[-1]}'
    return ', '.join(map(str,vertices))


def quotient():
    fig,ax=plate(826)
    label(ax,42,49,'Ten orbits of the full automorphism group',26,fontfamily='DejaVu Serif')
    label(ax,44,90,'252 automorphisms   /   108 vertices   /   23 edge orbits',14,MUTED)
    rule(ax,42,120,1198,120)
    label(ax,44,164,'Vertex orbits',18,fontfamily='DejaVu Serif')
    label(ax,533,164,'Neighbours per vertex',18,fontfamily='DejaVu Serif')
    label(ax,44,206,'Class',10,MUTED);label(ax,113,206,'Vertex IDs',10,MUTED)
    label(ax,428,206,'Size',10,MUTED,ha='right')
    x0,y0,w=597,243,47
    values=DATA['neighbors_per_vertex']
    for i,vs in enumerate(DATA['vertices']):
        y=y0+i*w;color=PALETTE[role(vs[0])]
        rule(ax,44,y+w/2-1,438,y+w/2-1)
        disk(ax,55,y,6,color,linewidth=0)
        label(ax,72,y,LETTERS[i],12,weight='bold')
        label(ax,113,y,pretty_ids(vs),12)
        label(ax,428,y,str(len(vs)),13,ha='right',weight='bold')
        label(ax,x0+i*w,206,LETTERS[i],12,color,ha='center',weight='bold')
        label(ax,x0-40,y,LETTERS[i],12,color,ha='center',weight='bold')
        for j,n in enumerate(values[i]):
            x=x0+w*j
            fill={0:'#f0f3ef',1:'#d8e9e4',2:'#b8d9d0',3:'#8fc2b9',4:'#609d95',6:'#286e6c',7:'#145758'}[n]
            ax.add_patch(Rectangle((x-22,y-22),44,44,facecolor=fill,linewidth=0))
            if n:label(ax,x,y,str(n),13,'white' if n>=6 else INK,ha='center',weight='bold')
    rule(ax,42,727,1198,727)
    label(ax,44,759,'Reading a row',14,fontfamily='DejaVu Serif')
    label(ax,232,759,'Every vertex in G has six neighbours in J. Every vertex in J has three in G.',12,MUTED)
    label(ax,232,789,'Blank cells are zero. Each row sums to 11.',12,MUTED)
    save(fig,'n112_108_orbits')


if __name__=='__main__':
    import xml.etree.ElementTree as ET
    tally,clearance=full_graph()
    quotient()
    doc=ET.parse(HERE/'n112_108_symmetry.svg')
    ids=[node.get('id','') for node in doc.iter()]
    drawn_edges=[tag for tag in ids if tag.startswith('edge-')]
    assert len(drawn_edges)==594 and set(drawn_edges)=={f'edge-{u}-{v}' for u,v in EDGES}
    assert sorted(int(s[7:]) for s in ids if s.startswith('vertex-'))==list(range(108))
    report=dict(vertices=108,edges=594,svg_edge_ids_match=True,vertex_ids_match=True,
                moving_vertices_checked=91,rotated_edge_paths_checked=sum(u>=17 for u,v in EDGES),
                minimum_edge_to_nonincident_vertex=round(clearance,4),
                edge_counts_by_role=tally,roles=['fixed','centre','outer'])
    (HERE/'drawing-check.json').write_text(json.dumps(report,indent=2)+'\n')
