// Ordinary queue BFS from every vertex; no finite-field or certificate code is used.
// Build: g++ -O3 -std=c++17 verify_bfs.cpp -o verify_bfs
#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>
int main(int argc, char** argv) {
  try {
    if (argc != 2) throw std::runtime_error("usage: verify_bfs graph.edges");
    std::ifstream in(argv[1]);
    int n, m;
    if (!(in >> n >> m) || n <= 0 || m < 0) throw std::runtime_error("invalid header");
    std::vector<std::vector<int>> adj(n);
    for (int k=0; k<m; ++k) {
      int u,v;
      if (!(in>>u>>v) || u<0 || u>=n || v<0 || v>=n || u==v)
        throw std::runtime_error("invalid edge");
      adj[u].push_back(v); adj[v].push_back(u);
    }
    std::string extra;
    if (in >> extra) throw std::runtime_error("extra input after declared edges");
    int mindeg=n, maxdeg=0;
    for (auto& row: adj) {
      std::sort(row.begin(),row.end());
      if (std::adjacent_find(row.begin(),row.end()) != row.end())
        throw std::runtime_error("parallel edge");
      mindeg=std::min(mindeg,int(row.size())); maxdeg=std::max(maxdeg,int(row.size()));
    }
    std::vector<int> queue(n), seen(n,-1), dist(n);
    std::array<std::uint64_t,4> hist{};
    int failures=0, witness_s=-1, witness_t=-1;
    for (int s=0;s<n;++s) {
      int head=0,tail=1; queue[0]=s; seen[s]=s; dist[s]=0; ++hist[0];
      while (head<tail) {
        int u=queue[head++];
        if (dist[u]==3) continue;
        for (int v:adj[u]) if (seen[v]!=s) {
          seen[v]=s; dist[v]=dist[u]+1; ++hist[dist[v]]; queue[tail++]=v;
        }
      }
      if (tail!=n) {
        ++failures;
        if (witness_s<0) { witness_s=s; for (int t=0;t<n;++t) if (seen[t]!=s) {witness_t=t;break;} }
      }
    }
    std::cout<<"{\"implementation\":\"ordinary queue BFS from all sources, radius 3\",\"vertices\":"<<n
      <<",\"edges\":"<<m<<",\"min_degree\":"<<mindeg<<",\"max_degree\":"<<maxdeg
      <<",\"all_sources_checked\":"<<n<<",\"distance_histogram\":[";
    for (int k=0;k<4;++k) { if(k) std::cout<<','; std::cout<<hist[k]; }
    std::cout<<"],\"failed_sources\":"<<failures;
    if (failures) std::cout<<",\"failure_pair\":["<<witness_s<<','<<witness_t<<']';
    else {int diameter=0;for(int k=0;k<4;++k)if(hist[k])diameter=k;std::cout<<",\"diameter\":"<<diameter;}
    std::cout<<"}\n";
    return failures ? 1 : 0;
  } catch (const std::exception& e) {std::cerr<<e.what()<<'\n';return 2;}
}
