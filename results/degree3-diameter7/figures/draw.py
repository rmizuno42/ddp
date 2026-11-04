"""Draw the actual edge list with C16-equivariant coordinates and a voltage key."""
import json
import math
import os
from pathlib import Path
import tempfile
os.environ.setdefault('MPLCONFIGDIR', str(Path(tempfile.gettempdir()) / 'ddp-matplotlib'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
from matplotlib.path import Path as MplPath
HERE = Path(__file__).resolve().parent.parent
rows = [tuple(map(int, line.split())) for line in (HERE/'certificate/graph.edges').read_text().splitlines()]
assert rows[0] == (208, 312)
actual = set(rows[1:])
assert len(actual) == 312
chords = [(1,7,2),(2,12,-4),(3,9,8),(4,6,-5),(5,8,-1),(10,11,-1)]
colors = ['#087E8B','#C86B2B','#7C55A5','#3D8A55','#C14869','#3566B2']
plt.rcParams.update({'font.family':'DejaVu Sans', 'svg.fonttype':'none', 'pdf.fonttype':42})
background = '#FCFBF7'
fig, ax = plt.subplots(figsize=(11,12), facecolor=background)
ax.set_facecolor(background); ax.set_aspect('equal'); ax.axis('off')
radii = [6.5 - .395*i for i in range(13)]
points = {}
for i in range(13):
    for x in range(16):
        theta = math.pi/2 + 2*math.pi*x/16
        points[16*i+x] = (radii[i]*math.cos(theta),radii[i]*math.sin(theta))
drawn = set()
def remember(u,v):
    edge=tuple(sorted((u,v)))
    assert edge in actual and edge not in drawn, edge
    drawn.add(edge)
for i in range(12):
    for x in range(16):
        u,v=16*i+x,16*(i+1)+x; remember(u,v)
        ax.plot([points[u][0],points[v][0]],[points[u][1],points[v][1]],color='#7D8991',lw=.8,alpha=.65,zorder=1)
for x in range(16):
    u,v=x,(x+1)%16; remember(u,v)
    ax.plot([points[u][0],points[v][0]],[points[u][1],points[v][1]],color='#263B4A',lw=1.5,zorder=2)
for x in range(8):
    u,v=192+x,192+x+8;remember(u,v)
    ax.plot([points[u][0],points[v][0]],[points[u][1],points[v][1]],color='#546472',lw=.9,alpha=.8,zorder=1)
for k,(i,j,s) in enumerate(chords):
    for x in range(16):
        u,v=16*i+x,16*j+(x+s)%16;remember(u,v)
        xs=[];ys=[]
        for z in range(61):
            t=z/60
            # A small equivariant bend keeps chords clear of unrelated vertices.
            theta=math.pi/2+2*math.pi*(x+s*t+.14*math.sin(math.pi*t))/16
            radius=(1-t)*radii[i]+t*radii[j]
            xs.append(radius*math.cos(theta));ys.append(radius*math.sin(theta))
        for w, (wx, wy) in points.items():
            if w in (u,v): continue
            for segment in range(len(xs)-1):
                dx,dy=xs[segment+1]-xs[segment],ys[segment+1]-ys[segment]
                tau=max(0,min(1,((wx-xs[segment])*dx+(wy-ys[segment])*dy)/(dx*dx+dy*dy)))
                assert math.hypot(wx-xs[segment]-tau*dx,wy-ys[segment]-tau*dy)>.04, (u,v,w)
        ax.plot(xs,ys,color=colors[k],lw=.75,alpha=.72,zorder=2)
for i in range(13):
    xy=[points[16*i+x] for x in range(16)]
    ax.scatter([p[0] for p in xy],[p[1] for p in xy],s=17,c='#17384A',edgecolors=background,linewidths=.65,zorder=5)
    angle=math.pi/2+math.pi/16
    ax.text(radii[i]*math.cos(angle),radii[i]*math.sin(angle),str(i),ha='center',va='center',fontsize=8.5,
            color='#334C59',bbox=dict(boxstyle='round,pad=.1',fc=background,ec='none',alpha=.95),zorder=6)
assert drawn==actual and len(points)==208 and len(drawn)==312
ax.set_xlim(-7.1,7.1);ax.set_ylim(-7.0,7.0)
fig.suptitle('208 vertices · degree 3 · diameter 7',fontsize=23,fontweight='medium',color='#183747',y=.972)
fig.text(.5,.933,'16-fold rotational symmetry  /  13 orbits of 16 vertices',ha='center',fontsize=12,color='#536B78')
fig.text(.5,.048,'Aut(G) ≅ C₁₆     •     (i, x) ↦ (i, x + 1)',ha='center',fontsize=14,color='#183747')
fig.text(.5,.025,'All 312 edges are drawn. Crossings without dots are not vertices. Ring labels give i.',ha='center',fontsize=9,color='#536B78')
fig.subplots_adjust(left=.035,right=.965,bottom=.075,top=.91)
for suffix in ['png','svg','pdf']:
    output=HERE/f'figures/n37_208_rotation.{suffix}'
    fig.savefig(output,dpi=180,facecolor=background)
    if suffix=='svg':
        output.write_text('\n'.join(line.rstrip() for line in output.read_text().splitlines())+'\n')
plt.close(fig)

fig,ax=plt.subplots(figsize=(14,5.6),facecolor=background);ax.set_facecolor(background);ax.axis('off')
for i in range(12):ax.plot([i,i+1],[0,0],color='#81909A',lw=2,zorder=1)
for i in range(13):
    ax.scatter(i,0,s=530,c='#183747',edgecolor=background,lw=2,zorder=4)
    ax.text(i,0,str(i),ha='center',va='center',fontsize=12,color='white',zorder=5)
arc_heights=[1.65,-2.2,2.25,-.95,-1.25,.8]
for k,((i,j,s),height) in enumerate(zip(chords,arc_heights)):
    sign=1 if height>0 else -1
    path=MplPath([(i+.13,.14*sign),((i+j)/2,2*height),(j-.14,.14*sign)],
                 [MplPath.MOVETO,MplPath.CURVE3,MplPath.CURVE3])
    patch=FancyArrowPatch(path=path,arrowstyle='-|>',mutation_scale=15,color=colors[k],lw=2,zorder=2)
    ax.add_patch(patch)
    ax.text((i+j)/2,height+.18*sign,f'{s:+d}',ha='center',va='center',fontsize=12,color=colors[k],
            bbox=dict(fc=background,ec='none',pad=2))
ax.text(0,.6,'cycle +1',ha='center',fontsize=11,color='#183747')
ax.text(12,.6,'matching +8',ha='center',fontsize=11,color='#183747')
ax.set_xlim(-.7,12.7);ax.set_ylim(-2.85,2.8)
fig.suptitle('A compact description of all 312 edges',fontsize=21,color='#183747',y=.98)
fig.text(.5,.89,r'Each node i represents $\{(i,x):x\in\mathbb{Z}_{16}\}$. An arrow $i\to j$ with label s means $(i,x)\sim(j,x+s)$.',ha='center',fontsize=11,color='#536B78')
fig.text(.5,.055,'At i = 0: (0,x) ~ (0,x+1).   At i = 12: (12,x) ~ (12,x+8).   All arithmetic is modulo 16.',ha='center',fontsize=11,color='#536B78')
fig.text(.5,.018,'Arrowheads specify the sign of the shift; the graph itself is undirected.',ha='center',fontsize=10,color='#536B78')
fig.text(.5,.82,'Gray path edges have shift 0.',ha='center',fontsize=10,color='#697D89')
fig.subplots_adjust(left=.025,right=.975,bottom=.12,top=.84)
for suffix in ['png','svg','pdf']:
    output=HERE/f'figures/n37_208_voltage.{suffix}'
    fig.savefig(output,dpi=180,facecolor=background)
    if suffix=='svg':
        output.write_text('\n'.join(line.rstrip() for line in output.read_text().splitlines())+'\n')
plt.close(fig)
(HERE/'figures/drawing-check.json').write_text(json.dumps(dict(vertices=len(points),edges=len(drawn),
    exact_edge_set_match=True,chords_avoid_nonincident_vertices=True,coordinates={str(v):xy for v,xy in points.items()},chord_rules=chords),indent=2)+'\n')
print('Saved rotation and voltage figures as PNG, SVG, PDF; exact 208 vertices / 312 edges checked.')
