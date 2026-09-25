#include <bits/stdc++.h>
#include <omp.h>
using namespace std;
int main(int argc,char**argv){
 if(argc<2){cerr<<"usage: verify_bitset edges [diameter]\n";return 2;}
 ifstream f(argv[1]);int n,m;f>>n>>m;vector<vector<int>>a(n);int u,v;
 for(int i=0;i<m;i++){if(!(f>>u>>v)||u<0||v<0||u>=n||v>=n||u==v)throw runtime_error("invalid edge");a[u].push_back(v);a[v].push_back(u);}
 int extra;if(f>>extra)throw runtime_error("extra edges");map<int,int>hist;
 for(auto& row:a){sort(row.begin(),row.end());if(adjacent_find(row.begin(),row.end())!=row.end())throw runtime_error("duplicate edge");hist[row.size()]++;}
 size_t W=(n+63)/64,N=size_t(n)*W;vector<uint64_t>p(N),q(N);for(u=0;u<n;u++)p[size_t(u)*W+u/64]|=1ull<<(u%64);
 uint64_t reached=n;vector<uint64_t>layer{uint64_t(n)};int D=argc>2?atoi(argv[2]):5;
 for(int d=1;d<=D;d++){
  uint64_t total=0;
  #pragma omp parallel for reduction(+:total) schedule(static)
  for(int i=0;i<n;i++){
   uint64_t *out=&q[size_t(i)*W];copy_n(&p[size_t(i)*W],W,out);
   for(int j:a[i]){const uint64_t*src=&p[size_t(j)*W];
    #pragma omp simd
    for(size_t k=0;k<W;k++)out[k]|=src[k];
   }
   for(size_t k=0;k<W;k++)total+=__builtin_popcountll(out[k]);
  }
  layer.push_back(total-reached);reached=total;p.swap(q);cerr<<"radius "<<d<<" reached "<<reached<<" / "<<uint64_t(n)*n<<"\n";
 }
 if(argc>3){ofstream bad(argv[3]);for(int i=0;i<n;i++)for(int j=i+1;j<n;j++)if(!(p[size_t(i)*W+j/64]>>(j%64)&1ull))bad<<i<<' '<<j<<'\n';}
 cout<<"{\"vertices\":"<<n<<",\"edges\":"<<m<<",\"degrees\":{";bool first=true;
 for(auto [d,c]:hist){if(!first)cout<<",";first=false;cout<<'"'<<d<<"\":"<<c;}cout<<"},\"distance_layers\":[";
 for(int d=0;d<=D;d++){if(d)cout<<",";cout<<layer[d];}cout<<"],\"unreachable_within_D\":"<<uint64_t(n)*n-reached<<",\"D\":"<<D<<"}\n";
 return reached==uint64_t(n)*n?0:1;
}
