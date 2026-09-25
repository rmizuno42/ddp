// Independent graph-level verification. C++17 standard library only.
// g++ -O3 -std=c++17 verify_bfs.cpp -o verify_bfs
// ./verify_bfs graph_12_4_5832.edges > bfs_certificate_cpp.json
#include <algorithm>
#include <array>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <vector>
int main(int argc, char** argv) {
  try {
    if (argc != 2) throw std::runtime_error("Usage: verify_bfs EDGE_FILE");
    constexpr int n=5832, degree=12;
    std::ifstream in(argv[1]);
    if (!in) throw std::runtime_error("Cannot open edge file");
    std::vector<std::vector<int>> adj(n);
    int u,v,edges=0;
    while (in >> u >> v) {
      if (!(0<=u && u<v && v<n)) throw std::runtime_error("Invalid or noncanonical edge");
      adj[u].push_back(v); adj[v].push_back(u); ++edges;
    }
    if (!in.eof()) throw std::runtime_error("Malformed edge file");
    if (edges!=34992) throw std::runtime_error("Unexpected edge count");
    for (auto& row: adj) {
      std::sort(row.begin(),row.end());
      if (row.size()!=degree || std::adjacent_find(row.begin(),row.end())!=row.end())
        throw std::runtime_error("Graph is not simple 12-regular");
    }
    std::vector<int> seen(n,0),queue(n),dist(n);
    std::array<long long,5> histogram={};
    int witness_u=-1,witness_v=-1;
    for (int root=0;root<n;++root) {
      int tail=1; queue[0]=root;seen[root]=root+1;dist[root]=0;
      for (int head=0;head<tail;++head) {
        int a=queue[head];
        if (dist[a]==4) continue;
        for (int b:adj[a]) if (seen[b]!=root+1) {
          seen[b]=root+1;dist[b]=dist[a]+1;queue[tail++]=b;
        }
      }
      if (tail!=n) throw std::runtime_error("Diameter exceeds four (or graph disconnected)");
      for (int a=0;a<n;++a) {
        ++histogram[dist[a]];
        if (dist[a]==4 && witness_u<0) {witness_u=root;witness_v=a;}
      }
    }
    if (histogram[4]==0) throw std::runtime_error("Diameter is less than four");
    const std::array<long long,5> expected={5832,69984,676512,6342300,26917596};
    if (histogram!=expected) throw std::runtime_error("Unexpected all-pairs distance histogram");
    std::cout << "{\n  \"result\": \"PASS\",\n  \"order\": 5832,\n  \"edges\": 34992,\n  \"degree\": 12,\n  \"diameter\": 4,\n  \"all_sources_checked\": 5832,\n  \"ordered_pairs_checked\": 34012224,\n  \"distance_histogram_ordered_pairs\": [";
    for(int i=0;i<5;++i)std::cout<<(i?", ":"")<<histogram[i];
    std::cout << "],\n  \"distance_four_witness\": [" <<witness_u<<", "<<witness_v<<"]\n}\n";
  } catch (const std::exception& e) {
    std::cerr << "FAIL: " <<e.what()<<"\n";return 1;
  }
}
