// Portable C++17, no external library. Checks every source, without symmetry reduction.
#include <algorithm>
#include <atomic>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <map>
#include <mutex>
#include <stdexcept>
#include <string>
#include <thread>
#include <vector>
using namespace std;
static void require(bool ok,const string&message){if(!ok)throw runtime_error(message);}
int main(int argc,char**argv){try{
 require(argc==2||argc==3,"Usage: verify_graph graph.edges [threads]");
 const auto start=chrono::steady_clock::now();ifstream in(argv[1]);int n=0;long long m=0;in>>n>>m;
 require(bool(in)&&n==88452&&m==574938,"Unexpected graph header");
 vector<vector<int>> rows(n);int a,b;long long count=0;
 while(in>>a>>b){require(0<=a&&a<b&&b<n,"Invalid, reversed, or loop edge");rows[a].push_back(b);rows[b].push_back(a);count++;}
 require(in.eof()&&count==m,"Malformed or incomplete edge list");
 vector<int> offset(n+1),adj;map<int,int>hist;
 for(int s=0;s<n;s++){auto&r=rows[s];sort(r.begin(),r.end());require(adjacent_find(r.begin(),r.end())==r.end(),"Duplicate edge");require(r.size()==13,"Graph is not 13-regular");hist[r.size()]++;offset[s+1]=offset[s]+int(r.size());adj.insert(adj.end(),r.begin(),r.end());}
 rows.clear();rows.shrink_to_fit();require(adj.size()==2*size_t(m),"Edge count mismatch");
 const int threads=argc==3?stoi(argv[2]):2;require(threads>=1&&threads<=256,"Invalid thread count");
 atomic<int>next{0},done{0};atomic<long long>missing{0};mutex output;
 cout<<"INPUT vertices="<<n<<" edges="<<m<<" degree=13 threads="<<threads<<endl;
 vector<thread>workers;
 for(int k=0;k<threads;k++)workers.emplace_back([&]{vector<int>seen(n,-1),queue(n);
  while(true){int s=next.fetch_add(1);if(s>=n)break;int head=0,tail=1;queue[0]=s;seen[s]=s;
   for(int depth=0;depth<5&&tail<n;depth++){int end=tail;while(head<end&&tail<n){int v=queue[head++];for(int j=offset[v];j<offset[v+1];j++){int w=adj[j];if(seen[w]!=s){seen[w]=s;queue[tail++]=w;}}}}
   if(tail!=n){missing.fetch_add(n-tail);lock_guard<mutex>lock(output);cout<<"FAIL source="<<s<<" missing="<<n-tail<<endl;}
   int d=done.fetch_add(1)+1;if(d%4000==0){lock_guard<mutex>lock(output);cout<<"PROGRESS sources="<<d<<" missing="<<missing.load()<<endl;}
  }
 });
 for(auto&t:workers)t.join();require(done==n,"Not every source was processed");
 cout<<"FINAL sources="<<done<<" ordered_pairs_at_distance_gt5="<<missing<<" seconds="<<chrono::duration<double>(chrono::steady_clock::now()-start).count()<<endl;
 if(missing!=0)return 2;
 const long long moore4=1+13*(1+12+144+1728);require(n>moore4,"The order does not certify diameter >=5");
 cout<<"PASS: simple undirected 13-regular graph; order 88452; diameter exactly 5."<<endl;return 0;
}catch(const exception&e){cerr<<"ERROR: "<<e.what()<<endl;return 1;}}
