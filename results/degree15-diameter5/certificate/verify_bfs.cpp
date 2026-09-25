#include <bits/stdc++.h>
#include <omp.h>
using namespace std;
int main(int argc,char**argv){if(argc<2)return 2;ifstream f(argv[1]);int n,m;f>>n>>m;vector<vector<int>>adj(n);int u,v;
 for(int i=0;i<m;i++){if(!(f>>u>>v)||u<0||v<0||u>=n||v>=n||u==v)throw runtime_error("bad edge");adj[u].push_back(v);adj[v].push_back(u);}int ex;if(f>>ex)throw runtime_error("extra input");int maxdeg=0;vector<int>off(n+1);vector<int>a;for(int i=0;i<n;i++){sort(adj[i].begin(),adj[i].end());if(adjacent_find(adj[i].begin(),adj[i].end())!=adj[i].end())throw runtime_error("duplicate");maxdeg=max(maxdeg,(int)adj[i].size());off[i]=a.size();for(int j:adj[i])a.push_back(j);}off[n]=a.size();vector<vector<int>>().swap(adj);
 unsigned long long hist[6]={0,0,0,0,0,0};vector<int>fail(n,-1);
 #pragma omp parallel reduction(+:hist[:6])
 {
  vector<int>seen(n,-1),queue(n);vector<unsigned char>depth(n);
  #pragma omp for schedule(dynamic,64)
  for(int s=0;s<n;s++){
   queue[0]=s;depth[s]=0;seen[s]=s;int h=0,t=1;hist[0]++;
   while(h<t){int x=queue[h++];int d=depth[x];if(d==5)continue;for(int k=off[x];k<off[x+1];k++){int y=a[k];if(seen[y]!=s){seen[y]=s;depth[y]=d+1;queue[t++]=y;hist[d+1]++;}}}
   if(t!=n){for(int y=0;y<n;y++)if(seen[y]!=s){fail[s]=y;break;}}
  }
 }
 int bad=0;for(int x:fail)bad+=x>=0;cout<<"{\"implementation\":\"ordinary BFS, all sources, depth 5\",\"vertices\":"<<n<<",\"edges\":"<<m<<",\"max_degree\":"<<maxdeg<<",\"distance_layers\":[";
 for(int d=0;d<6;d++){if(d)cout<<',';cout<<hist[d];}cout<<"],\"failed_sources\":"<<bad;if(bad){for(int s=0;s<n;s++)if(fail[s]>=0){cout<<",\"unreachable_pair\":["<<s<<','<<fail[s]<<']';break;}}cout<<"}\n";return bad?1:0;
}
