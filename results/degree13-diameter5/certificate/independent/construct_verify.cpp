#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <numeric>
#include <stdexcept>
#include <string>
#include <vector>
using namespace std;
constexpr int FIBRE=243,CONTROLLERS=364,N=CONTROLLERS*FIBRE,DEGREE=13;
using Graph=vector<vector<int>>;
void need(bool b,const string& why){if(!b)throw runtime_error(why);}
int mod3(int x){x%=3;return x<0?x+3:x;}
int encode(const array<int,5>&x){int y=0;for(int j=4;j>=0;j--)y=3*y+mod3(x[j]);return y;}
void normalize(vector<int>&a,int vertex){sort(a.begin(),a.end());a.erase(unique(a.begin(),a.end()),a.end());a.erase(remove(a.begin(),a.end(),vertex),a.end());}
vector<int> read_integers(const string&name,int count){ifstream f(name);need(bool(f),"Cannot open "+name);vector<int>x(count);for(int&v:x)need(bool(f>>v),"Truncated "+name);int extra;need(!(f>>extra),"Extra entry in "+name);return x;}
Graph construct(){
 Graph A(N);ifstream f("controller_affine_chart.txt");int n;need(bool(f>>n)&&n==CONTROLLERS,"Invalid chart header");
 array<array<int,5>,FIBRE> digits{};for(int x=0;x<FIBRE;x++)for(int j=0,p=1;j<5;j++,p*=3)digits[x][j]=(x/p)%3;
 for(int u=0;u<n;u++)for(int port=0;port<4;port++){
  int v,M[5][5],b[5];need(bool(f>>v)&&v>=0&&v<n,"Invalid controller neighbour");
  for(auto&row:M)for(int&a:row)need(bool(f>>a)&&a>=0&&a<3,"Invalid matrix entry");
  for(int&a:b)need(bool(f>>a)&&a>=0&&a<3,"Invalid direction entry");
  for(int x=0;x<FIBRE;x++)for(int l=0;l<3;l++){
   array<int,5> y{};for(int i=0;i<5;i++){y[i]=l*b[i];for(int j=0;j<5;j++)y[i]+=M[i][j]*digits[x][j];}
   A[u*FIBRE+x].push_back(v*FIBRE+encode(y));
  }
 }
 int extra;need(!(f>>extra),"Extra chart entry");array<int,14> ordinary{};
 for(int v=0;v<N;v++){normalize(A[v],v);need(A[v].size()==11||A[v].size()==12,"Unexpected ordinary degree");ordinary[A[v].size()]++;}
 need(ordinary[11]==756&&ordinary[12]==N-756,"Unexpected ordinary degree histogram");
 for(int v=0;v<N;v++)for(int w:A[v])need(binary_search(A[w].begin(),A[w].end(),v),"Ordinary graph is not undirected");
 auto mate=read_integers("main_matching.txt",N);
 for(int v=0;v<N;v++){int w=mate[v];need(w>=0&&w<N&&w!=v&&mate[w]==v,"Invalid main involution");need(!binary_search(A[v].begin(),A[v].end(),w),"Main edge duplicates an ordinary edge");}
 for(int v=0;v<N;v++){A[v].push_back(mate[v]);sort(A[v].begin(),A[v].end());}
 ifstream sp("spare_matching.txt");need(bool(sp),"Cannot open spare edge file");vector<bool>used(N);int a,b,count=0;
 while(sp>>a>>b){need(a>=0&&a<N&&b>=0&&b<N&&a!=b,"Invalid spare endpoint");need(!used[a]&&!used[b],"Repeated spare endpoint");need(A[a].size()==12&&A[b].size()==12,"Spare edge uses an occupied degree slot");need(!binary_search(A[a].begin(),A[a].end(),b),"Spare edge duplicates an existing edge");used[a]=used[b]=true;A[a].push_back(b);A[b].push_back(a);sort(A[a].begin(),A[a].end());sort(A[b].begin(),A[b].end());count++;}
 need(sp.eof()&&count==378,"Invalid spare edge count");
 for(int v=0;v<N;v++){need(A[v].size()==DEGREE,"Final degree is not 13");need(!binary_search(A[v].begin(),A[v].end(),v),"Final graph has a loop");for(int w:A[v])need(binary_search(A[w].begin(),A[w].end(),v),"Final graph is not undirected");}
 cout<<"CONSTRUCTION vertices="<<N<<" degree="<<DEGREE<<" edges="<<(uint64_t(N)*DEGREE/2)<<" ordinary_degree11="<<ordinary[11]<<" ordinary_degree12="<<ordinary[12]<<"\n";return A;
}
vector<int> orbit_sources(const Graph&A){
 auto g=read_integers("controller_order7_permutation.txt",CONTROLLERS);vector<int>sorted(CONTROLLERS);iota(sorted.begin(),sorted.end(),0);auto check=g;sort(check.begin(),check.end());need(check==sorted,"Controller map is not a permutation");
 vector<bool>seen(CONTROLLERS);vector<int>sources;
 for(int u=0;u<CONTROLLERS;u++)if(!seen[u]){int v=u;for(int p=0;p<7;p++){need(!seen[v],"Controller orbit does not have length seven");seen[v]=true;v=g[v];}need(v==u,"Controller orbit does not close at seven");for(int x=0;x<FIBRE;x++)sources.push_back(u*FIBRE+x);}
 need(sources.size()==12636,"Wrong number of source representatives");
 for(int v=0;v<N;v++){vector<int>image;for(int w:A[v])image.push_back(g[w/FIBRE]*FIBRE+w%FIBRE);sort(image.begin(),image.end());need(image==A[g[v/FIBRE]*FIBRE+v%FIBRE],"Controller action is not a graph automorphism");}
 cout<<"AUTOMORPHISM free_order=7 source_representatives="<<sources.size()<<"\n";return sources;
}
void verify(const Graph&A,bool all){
 auto sources=orbit_sources(A);if(all){sources.resize(N);iota(sources.begin(),sources.end(),0);}
 vector<int>queue(N);vector<uint8_t>distance(N);array<uint64_t,6>hist{};int tested=0;
 for(int s:sources){fill(distance.begin(),distance.end(),255);int head=0,tail=1;queue[0]=s;distance[s]=0;
  while(head<tail){int v=queue[head++];if(distance[v]==5)continue;for(int w:A[v])if(distance[w]==255){distance[w]=distance[v]+1;queue[tail++]=w;}}
  if(tail!=N){int t=find(distance.begin(),distance.end(),255)-distance.begin();throw runtime_error("Distance exceeds five: "+to_string(s)+" "+to_string(t));}
  for(auto d:distance)hist[d]++;tested++;if(tested%243==0)cout<<"VERIFIED_SOURCES "<<tested<<"/"<<sources.size()<<"\n";
 }
 uint64_t scale=all?1:7,total=0;cout<<"DISTANCE_HISTOGRAM";for(int d=0;d<=5;d++){hist[d]*=scale;total+=hist[d];cout<<" "<<d<<":"<<hist[d];}cout<<"\n";need(total==uint64_t(N)*N&&hist[5]>0,"Invalid distance histogram");
 cout<<"CERTIFIED vertices=88452 degree=13 diameter=5 missing_ordered_pairs=0\n";
}
int main(int argc,char**argv){try{string mode=argc>1?argv[1]:"--orbits";need(argc<=2,"Usage: construct_verify [--orbits|--all|--generate]");auto A=construct();if(mode=="--generate"){ofstream out("graph.adj");out<<N<<" "<<DEGREE<<"\n";for(auto const&row:A){for(int j=0;j<DEGREE;j++){if(j)out<<" ";out<<row[j];}out<<"\n";}need(bool(out),"Cannot write graph.adj");cout<<"WROTE graph.adj\n";}else{need(mode=="--orbits"||mode=="--all","Unknown mode");verify(A,mode=="--all");}return 0;}catch(const exception&e){cerr<<"FAIL: "<<e.what()<<"\n";return 1;}}
