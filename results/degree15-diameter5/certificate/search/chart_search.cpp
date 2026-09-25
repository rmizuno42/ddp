#include <bits/stdc++.h>
using namespace std;const int Q=5,S=5;
using Vec=array<int,S>;using Mat=array<Vec,S>;
int invf[5]={0,1,3,2,4};
Vec mv(const Mat&a,const Vec&b){Vec c{};for(int i=0;i<S;i++){int t=0;for(int j=0;j<S;j++)t+=a[i][j]*b[j];c[i]=t%Q;}return c;}
bool inverse(Mat a,Mat &b){b={};for(int i=0;i<S;i++)b[i][i]=1;for(int k=0;k<S;k++){int p=k;while(p<S&&!a[p][k])p++;if(p==S)return false;swap(a[k],a[p]);swap(b[k],b[p]);int iv=invf[a[k][k]];for(int j=0;j<S;j++){a[k][j]=a[k][j]*iv%Q;b[k][j]=b[k][j]*iv%Q;}for(int i=0;i<S;i++)if(i!=k&&a[i][k]){int v=a[i][k];for(int j=0;j<S;j++){a[i][j]=(a[i][j]-v*a[k][j]+25)%Q;b[i][j]=(b[i][j]-v*b[k][j]+25)%Q;}}}return true;}
int rankm(vector<Vec> c){int k=0;for(int col=0;col<S&&k<(int)c.size();col++){int p=k;while(p<(int)c.size()&&!c[p][col])p++;if(p==(int)c.size())continue;swap(c[k],c[p]);int iv=invf[c[k][col]];for(int j=col;j<S;j++)c[k][j]=c[k][j]*iv%5;for(int i=k+1;i<(int)c.size();i++)if(c[i][col]){int v=c[i][col];for(int j=col;j<S;j++)c[i][j]=(c[i][j]-v*c[k][j]+25)%5;}k++;}return k;}
vector<vector<int>> words(int D){vector<vector<int>> W{{}};int inv[3]={1,0,2};for(int k=0;k<D;k++){vector<vector<int>>N;for(auto w:W)for(int t=0;t<3;t++)if(w.empty()||t!=inv[w.back()]){auto v=w;v.push_back(t);N.push_back(v);}W=N;}return W;}
int main(int ac,char**av){if(ac<5)return 1;long long its=stoll(av[1]);mt19937_64 gen(stoull(av[2]));string out=av[3];int pweight=stoi(av[4]); int plus= ac>5?stoi(av[5]):3; int zidx=ac>6?stoi(av[6]):1; int active_mode=ac>7?stoi(av[7]):0;auto W=words(5),R=words(3);Mat a[3];a[2]={};for(int i=0;i<S;i++)a[2][i][i]=i<plus?1:4;Vec b[3];b[0]={};b[0][0]=1;b[0][min(plus,4)]=1;b[2]={};b[2][zidx]=1;int inv[3]={1,0,2};
 auto init=[&](){do{for(auto &v:a[0])for(auto &x:v)x=gen()%5;}while(!inverse(a[0],a[1]));b[1]=mv(a[1],b[0]);};init();
 vector<int>bestRanks,bestPens;int badrank=0,badpen=0;
 auto control=[&](const vector<int>&w){vector<Vec>M;for(int t:w){for(auto &v:M)v=mv(a[t],v);M.push_back(b[t]);}return M;};
 auto eval=[&](vector<int>*rk=nullptr,vector<int>*pn=nullptr){int score=0;brank:;badrank=badpen=0;if(rk)rk->clear();if(pn)pn->clear();for(auto&w:W){int r=rankm(control(w));if(rk)rk->push_back(r);badrank+=5-r;}
 if(pweight||pn)for(int ridx=0;ridx<(int)R.size();ridx++){auto&w=R[ridx];bool active=active_mode==0 || (active_mode==1&&(ridx==2||ridx==7||ridx==9||ridx==11));auto core=control(w);if(rankm(core)!=3){badpen+=10;if(pn)pn->push_back(0);continue;}
 // row-reduce core to find quotient coordinates by elimination.
 vector<Vec>C=core;int k=0;vector<int> piv;for(int col=0;col<5;col++){int p=k;while(p<3&&!C[p][col])p++;if(p==3)continue;swap(C[k],C[p]);int iv=invf[C[k][col]];for(int j=0;j<5;j++)C[k][j]=C[k][j]*iv%5;for(int i=0;i<3;i++)if(i!=k&&C[i][col]){int z=C[i][col];for(int j=0;j<5;j++)C[i][j]=(C[i][j]-z*C[k][j]+25)%5;}piv.push_back(col);if(++k==3)break;}
 bool seen[25]={};int count=0;for(int pos=0;pos<=3;pos++)for(int s=0;s<3;s++){Vec v=b[inv[s]];for(int j=pos;j<3;j++)v=mv(a[w[j]],v);for(int i=0;i<3;i++){int z=v[piv[i]];for(int j=0;j<5;j++)v[j]=(v[j]-z*C[i][j]+25)%5;}int z=0,first=-1;for(int j=0;j<5;j++)if(v[j]){first=j;break;}if(first<0)continue;int iv=invf[v[first]];for(int j=0;j<5;j++)if(find(piv.begin(),piv.end(),j)==piv.end())z=5*z+v[j]*iv%5;if(!seen[z]){seen[z]=true;count++;}}
 if(active)badpen+=6-count;if(pn)pn->push_back(count);
 }
 return 3*badrank+pweight*badpen;};
 int val=eval(),best=val;Mat bestA=a[0];long long bi=0;auto start=chrono::steady_clock::now();
 for(long long it=0;it<its;it++){
 if(val<best){best=val;bestA=a[0];bi=it;cerr<<"best "<<best<<" badrank "<<badrank<<" badpen "<<badpen<<" step "<<it<<'\n';{ofstream ck(out+"_checkpoint.json"); vector<int> cr,cp;eval(&cr,&cp);ck<<"{\"q\":5,\"s\":5,\"iteration\":"<<it<<",\"score\":"<<best<<",\"matrices\":[";for(int t=0;t<3;t++){if(t)ck<<',';ck<<'[';for(int i=0;i<S;i++){if(i)ck<<',';ck<<'[';for(int j=0;j<S;j++)ck<<(j?",":"")<<a[t][i][j];ck<<']';}ck<<']';}ck<<"],\"vectors\":[";for(int t=0;t<3;t++){if(t)ck<<',';ck<<'[';for(int j=0;j<S;j++)ck<<(j?",":"")<<b[t][j];ck<<']';}ck<<"],\"ranks\":[";for(int i=0;i<(int)cr.size();i++)ck<<(i?",":"")<<cr[i];ck<<"],\"pencil_directions\":[";for(int i=0;i<(int)cp.size();i++)ck<<(i?",":"")<<cp[i];ck<<"]}";}if(!best)break;}
 if(it%100000==99999){init();val=eval();}
 int i=gen()%S,j=gen()%S,old=a[0][i][j];a[0][i][j]=(old+1+gen()%4)%5;
 Mat AI; if(!inverse(a[0],AI)){a[0][i][j]=old;continue;}a[1]=AI;b[1]=mv(a[1],b[0]);
 int z=eval();double temp=.05+2.*pow(.004,(it%10000)/10000.);bool keep=z<=val||uniform_real_distribution<double>(0,1)(gen)<exp((val-z)/temp);
 if(keep)val=z;else{a[0][i][j]=old;inverse(a[0],a[1]);b[1]=mv(a[1],b[0]);}
 }
 if(val<best){best=val;bestA=a[0];bi=its;}a[0]=bestA;inverse(a[0],a[1]);b[1]=mv(a[1],b[0]);eval(&bestRanks,&bestPens);
 ofstream f(out+".json");f<<"{\"q\":5,\"s\":5,\"seed\":"<<av[2]<<",\"iterations\":"<<its<<",\"best_iteration\":"<<bi<<",\"score\":"<<best<<",\"matrices\":[";for(int t=0;t<3;t++){if(t)f<<',';f<<'[';for(int i=0;i<S;i++){if(i)f<<',';f<<'[';for(int j=0;j<S;j++)f<<(j?",":"")<<a[t][i][j];f<<']';}f<<']';}f<<"],\"vectors\":[";for(int t=0;t<3;t++){if(t)f<<',';f<<'[';for(int i=0;i<S;i++)f<<(i?",":"")<<b[t][i];f<<']';}f<<"],\"ranks\":[";for(int i=0;i<(int)bestRanks.size();i++)f<<(i?",":"")<<bestRanks[i];f<<"],\"pencil_directions\":[";for(int i=0;i<(int)bestPens.size();i++)f<<(i?",":"")<<bestPens[i];f<<"],\"seconds\":"<<chrono::duration<double>(chrono::steady_clock::now()-start).count()<<"}";
 cerr<<"FINAL score "<<best<<" badrank "<<badrank<<" badpen "<<badpen<<"\n";
}
