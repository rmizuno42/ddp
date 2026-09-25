// Independent graph generator: three explicit forward-edge formulas only.
// No use of construction.json, route certificates, or the Python generator.
#include <array>
#include <fstream>
#include <iostream>
#include <set>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>
using V=std::array<int,3>;
using M=std::array<V,3>;
V mul(const M& A,const V& x){V y{};for(int i=0;i<3;++i)for(int j=0;j<3;++j)y[i]=(y[i]+A[i][j]*x[j])%3;return y;}
int enc(int i,int j,const V& x){return 27*(9*i+j)+x[0]+3*x[1]+9*x[2];}
int main(int argc,char**argv){try{
 const M A={V{0,1,1},V{1,0,0},V{0,1,2}};
 const M B={V{1,0,1},V{0,2,0},V{1,2,2}};
 const M T={V{1,2,0},V{2,2,0},V{0,0,1}};
 const V pA{0,1,0},pB{1,2,0},pT{0,0,1};
 std::set<std::pair<int,int>> edges;
 auto put=[&](int u,int i,int j,V base,const V& p){
  for(int lam=0;lam<3;++lam){V y{};for(int k=0;k<3;++k)y[k]=(base[k]+lam*p[k])%3;
   int v=enc(i,j,y);if(u==v)throw std::runtime_error("self-loop");edges.emplace(std::min(u,v),std::max(u,v));}
 };
 int pow2=1;
 for(int i=0;i<6;++i){for(int j=0;j<9;++j)for(int z=0;z<27;++z){
  V x{z%3,(z/3)%3,z/9};int u=enc(i,j,x);
  put(u,(i+2)%6,(j+pow2)%9,mul(A,x),pA);
  put(u,(i+2)%6,(j+6*pow2)%9,mul(B,x),pB);
  if(i<3)put(u,i+3,j,mul(T,x),pT);
 }pow2=(pow2*2)%9;}
 if(edges.size()!=10935)throw std::runtime_error("wrong edge count");
 std::vector<int> degree(1458);for(auto [u,v]:edges){++degree[u];++degree[v];}
 for(int d:degree)if(d!=15)throw std::runtime_error("not 15-regular");
 std::string path=argc>1?argv[1]:"regenerated_cpp.edges";std::ofstream f(path);if(!f)throw std::runtime_error("cannot open output");
 f<<1458<<' '<<edges.size()<<'\n';for(auto [u,v]:edges)f<<u<<' '<<v<<'\n';
 std::cout<<"{\"implementation\":\"C++ explicit three forward formulas\",\"vertices\":1458,\"edges\":"<<edges.size()<<",\"degree\":15,\"simple\":true}\n";
 }catch(const std::exception&e){std::cerr<<e.what()<<'\n';return 1;}return 0;}
