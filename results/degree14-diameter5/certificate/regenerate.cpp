// Independent edge generator. All arithmetic is in F_3; no external libraries.
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <vector>
#include <algorithm>
using namespace std;
int main(int argc,char**argv){
 if(argc!=3){cerr<<"usage: regenerate parameters.txt output.edges\n";return 2;}
 ifstream f(argv[1]);int n;f>>n;if(n!=364)throw runtime_error("unexpected controller order");
 vector<array<int,4>>C(n);for(auto&r:C)for(int&x:r)f>>x;
 int A[4][5][5],b[4][5];for(auto&M:A)for(auto&r:M)for(int&x:r)f>>x;for(auto&r:b)for(int&x:r)f>>x;
 vector<int>cc(n);for(int&x:cc)f>>x;int extra;if(!f||(f>>extra))throw runtime_error("parameter length");
 int V[243][5];for(int x=0;x<243;x++){int z=x;for(int j=0;j<5;j++){V[x][j]=z%3;z/=3;}}
 int image[4][243][3];for(int t=0;t<4;t++)for(int x=0;x<243;x++)for(int l=0;l<3;l++){int y=0,p=1;for(int i=0;i<5;i++){int v=l*b[t][i];for(int j=0;j<5;j++)v+=A[t][i][j]*V[x][j];y+=p*(v%3);p*=3;}image[t][x][l]=y;}
 uint64_t N=uint64_t(n)*243;vector<uint64_t>es;es.reserve(N*14);
 auto edge=[&](int u,int v){if(u==v)return;if(u>v)swap(u,v);es.push_back(uint64_t(u)*N+v);};
 for(int u=0;u<n;u++){for(int t=0;t<4;t++){if(C[u][t]<0||C[u][t]>=n||C[C[u][t]][t]!=u)throw runtime_error("bad involution");for(int x=0;x<243;x++)for(int l=0;l<3;l++)edge(243*u+x,243*C[u][t]+image[t][x][l]);}
 if(cc[u]<=0||cc[u]>=243)throw runtime_error("zero/invalid direction");
 for(int x=0;x<243;x++){int y=0,p=1;for(int j=0;j<5;j++){y+=p*((V[x][j]+V[cc[u]][j])%3);p*=3;}edge(243*u+x,243*u+y);}}
 sort(es.begin(),es.end());es.erase(unique(es.begin(),es.end()),es.end());ofstream out(argv[2]);out<<N<<' '<<es.size()<<'\n';for(auto k:es)out<<k/N<<' '<<k%N<<'\n';if(!out)throw runtime_error("output error");
 cerr<<"vertices="<<N<<" edges="<<es.size()<<'\n';
}
