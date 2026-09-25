#include <bits/stdc++.h>
using namespace std;
int main(int argc,char**argv){
 if(argc<9){cerr<<"N D steps seed output [warm]\n";return 1;}
 int n=stoi(argv[1]),D=stoi(argv[2]);long long steps=stoll(argv[3]);mt19937_64 gen(stoull(argv[4]));string out=argv[5];double maxT=stod(argv[6]);
 if(n>64||n<4)return 2;
 vector<array<int,3>> a(n);vector<int>p(n);iota(p.begin(),p.end(),0);shuffle(p.begin(),p.end(),gen);
 for(int i=0;i<n;i++){a[p[i]][0]=p[(i+1)%n];a[p[(i+1)%n]][1]=p[i];}
 do{shuffle(p.begin(),p.end(),gen);for(int i=0;i+1<n;i+=2){a[p[i]][2]=p[i+1];a[p[i+1]][2]=p[i];}if(n%2)a[p[n-1]][2]=p[n-1];}while(false);
 if(argc>7 && string(argv[7])!="-"){ifstream in(argv[7]);for(auto &v:a)for(int &x:v)in>>x;}
 struct Node{int parent=-1,t=-1;bool final=false;array<int,3>child{-1,-1,-1};};vector<Node>tr(1);ifstream wf(argv[8]);string w;while(wf>>w){int u=0;for(char s:w){int t=s-'0';if(tr[u].child[t]<0){int v=tr.size();tr[u].child[t]=v;Node nd;nd.parent=u;nd.t=t;tr.push_back(nd);}u=tr[u].child[t];}tr[u].final=true;}
 auto score=[&](){int dest[256][64];uint64_t reach[64]={};for(int v=0;v<n;v++)dest[0][v]=v;for(int k=1;k<(int)tr.size();k++){int p=tr[k].parent,t=tr[k].t;for(int v=0;v<n;v++){int u=a[dest[p][v]][t];dest[k][v]=u;if(tr[k].final)reach[v]|=1ull<<u;}}
 int s=0;for(int v=0;v<n;v++)s+=n-__builtin_popcountll(reach[v]);return s;};
 int val=score(),best=val;auto bestA=a;long long bi=0,accept=0,valid=0;auto start=chrono::steady_clock::now();
 for(long long it=0;it<steps;it++){
  if(val<best){best=val;bestA=a;bi=it;ofstream f(out+".adj");for(auto v:a)f<<v[0]<<' '<<v[1]<<' '<<v[2]<<'\n';cerr<<"best "<<best<<" step "<<it<<"\n";if(!best)break;}
  int u=gen()%n,v=gen()%n;if(u==v)continue;int kind=gen()%3;int x=a[u][kind==0?0:2],y=a[v][kind==0?0:2];auto old=a;
  if(kind==0){a[u][0]=y;a[y][1]=u;a[v][0]=x;a[x][1]=v;}
  else if(kind==1){ // conjugate the involution by (u v)
    auto sw=[&](int z){return z==u?v:(z==v?u:z);};
    a[u][2]=sw(y);a[v][2]=sw(x);if(x!=u&&x!=v)a[x][2]=v;if(y!=u&&y!=v)a[y][2]=u;
  }else{
    if(x==v){a[u][2]=u;a[v][2]=v;}
    else if(x==u&&y==v){a[u][2]=v;a[v][2]=u;}
    else continue;
  }
  valid++;int z=score();double phase=(it%500000)/500000.;double T=.15+maxT*pow(.006,phase);bool keep=z<=val||uniform_real_distribution<double>(0,1)(gen)<exp((val-z)/T);
  if(keep){val=z;accept++;}else a=old;
  if(it%500000==499999){if(gen()%2){a=bestA;val=best;}}
 }
 if(val<best){best=val;bestA=a;bi=steps;}ofstream f(out+".adj");for(auto v:bestA)f<<v[0]<<' '<<v[1]<<' '<<v[2]<<'\n';
 ofstream j(out+".json");j<<"{\"n\":"<<n<<",\"D\":"<<D<<",\"steps\":"<<steps<<",\"valid\":"<<valid<<",\"accepted\":"<<accept<<",\"best_missing_ordered_pairs\":"<<best<<",\"best_iteration\":"<<bi<<",\"seconds\":"<<chrono::duration<double>(chrono::steady_clock::now()-start).count()<<"}";cerr<<"FINAL "<<n<<" "<<best<<"\n";
}
