// orbsearch2.cpp -- exhaustive search for G-invariant ("orbit") graphs with
// maximum degree <= Delta and diameter <= D on multi-orbit G-sets.
//
// Mathematical setting.  G acts on V = O_1 u ... u O_b (each O_i = G/H_i).
// A G-invariant simple graph on V is exactly a union of "edge classes"
// R u R*, R an orbital (G-orbit on ordered pairs of distinct points).
// Each class adds a constant number of neighbours to every vertex of the orbits
// it touches, so degrees are constant on orbits; eccentricity is constant on
// orbits, so diam <= D  <=>  BFS from one representative per orbit covers V
// within D steps.
//
// Search.  We enumerate *maximal* admissible selections of classes (no further
// class fits under the degree caps) -- adding edges never increases distances,
// so maximal selections dominate.  Pruning (sound): if the current selection
// together with ALL still-individually-admissible later classes does not reach
// diameter <= D, no completion does.  When the DFS finishes, the answer for this
// (G, orbit types, Delta, D) is exact.  An optional SA fallback is used only when
// the node cap is hit (reported as such).
//
// Usage:
//   orbsearch2 GROUPFILE CELLSFILE [--maxorb B] [--nodecap N] [--sa ITERS]
//              [--seed S] [--outdir DIR] [--maxcombos M] [--combo i,j,k]
//              [--mindeg-slack s]
//   CELLSFILE: lines "Delta D lo hi"
// Output (stdout):
//   FOUND Delta D n group combo sizes mode file
//   NONE  Delta D n group combo sizes classes nodes      (exhaustive: no graph)
//   OPEN  Delta D n group combo sizes classes bestf      (cap hit, SA failed)
#include <algorithm>
#include <chrono>
#include <climits>
#include <cmath>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <fstream>
#include <functional>
#include <iostream>
#include <map>
#include <numeric>
#include <random>
#include <sstream>
#include <string>
#include <vector>
using namespace std;

struct Action {
  int deg = 0;
  long stab = 0;
  string desc;
  vector<vector<int>> gens;
};
struct Cell {
  int Delta, D, lo, hi;
};

static string gname;
static long gorder = 0;
static int ngens = 0;
static vector<Action> acts;

static bool readGroup(const string& fn) {
  ifstream in(fn);
  if (!in) return false;
  string tok;
  while (in >> tok) {
    if (tok == "GROUP") {
      in >> gname >> gorder >> ngens;
    } else if (tok == "ACTION") {
      Action a;
      int k;
      in >> k >> a.deg >> a.stab >> a.desc;
      a.gens.assign(ngens, vector<int>(a.deg));
      for (int g = 0; g < ngens; g++)
        for (int i = 0; i < a.deg; i++) in >> a.gens[g][i];
      acts.push_back(std::move(a));
    } else if (tok == "END") {
      break;
    }
  }
  return !acts.empty() || true;
}

struct EdgeClass {
  int oi, oj, ci, cj;
  vector<int> ni, nj;
};

struct GSet {
  int n = 0, b = 0;
  vector<int> start, size, orbOf;
  vector<vector<int>> gens;
};

static GSet buildGSet(const vector<int>& combo) {
  GSet S;
  S.b = (int)combo.size();
  for (int a : combo) {
    S.start.push_back(S.n);
    S.size.push_back(acts[a].deg);
    S.n += acts[a].deg;
  }
  S.orbOf.resize(S.n);
  for (int o = 0; o < S.b; o++)
    for (int t = 0; t < S.size[o]; t++) S.orbOf[S.start[o] + t] = o;
  S.gens.assign(ngens, vector<int>(S.n));
  for (int g = 0; g < ngens; g++)
    for (int o = 0; o < S.b; o++) {
      const auto& p = acts[combo[o]].gens[g];
      for (int t = 0; t < S.size[o]; t++) S.gens[g][S.start[o] + t] = S.start[o] + p[t];
    }
  return S;
}

// Orbitals via BFS over ordered pairs from representatives: an orbital with
// source orbit i is determined by its pairs (rep_i, v); we label every ordered
// pair (u,v) by flood fill from (rep_i, v) under the generators.
static vector<EdgeClass> buildClasses(const GSet& S, int maxContrib) {
  int n = S.n;
  vector<int> lab((size_t)n * n, -1);
  vector<int> st;
  int nlab = 0;
  vector<int> labSrcOrb, labTgtOrb, labOut;  // out-degree from source vertex
  for (int i = 0; i < S.b; i++) {
    int ri = S.start[i];
    for (int v = 0; v < n; v++) {
      if (v == ri) continue;
      size_t key = (size_t)ri * n + v;
      if (lab[key] >= 0) continue;
      int L = nlab++;
      lab[key] = L;
      st.clear();
      st.push_back((int)key);
      long cnt = 0;
      while (!st.empty()) {
        size_t k = (size_t)st.back();
        st.pop_back();
        cnt++;
        int u = (int)(k / n), w = (int)(k % n);
        for (int g = 0; g < ngens; g++) {
          size_t k2 = (size_t)S.gens[g][u] * n + S.gens[g][w];
          if (lab[k2] < 0) {
            lab[k2] = L;
            st.push_back((int)k2);
          }
        }
      }
      labSrcOrb.push_back(i);
      labTgtOrb.push_back(S.orbOf[v]);
      labOut.push_back((int)(cnt / S.size[i]));
    }
  }
  vector<EdgeClass> cls;
  // pass 1: decide classes (metadata only)
  vector<int> classOf(nlab, -1);   // class index for a label (forward label of cross classes, both labels of inner)
  vector<char> fwd(nlab, 0);       // 1 if label is the forward label (source orbit = class.oi)
  for (int L = 0; L < nlab; L++) {
    int i = labSrcOrb[L], j = labTgtOrb[L];
    if (j < i) continue;
    int a = labOut[L];
    int ri = S.start[i];
    int v0 = -1;
    for (int v = S.start[j]; v < S.start[j] + S.size[j]; v++)
      if (v != ri && lab[(size_t)ri * n + v] == L) {
        v0 = v;
        break;
      }
    int P = lab[(size_t)v0 * n + ri];
    if (i == j) {
      bool selfPaired = (P == L);
      if (!selfPaired && L > P) continue;
      int contrib = selfPaired ? a : 2 * a;
      if (contrib > maxContrib) continue;
      EdgeClass E;
      E.oi = E.oj = i;
      E.ci = E.cj = contrib;
      E.ni.resize((size_t)S.size[i] * contrib);
      classOf[L] = (int)cls.size();
      fwd[L] = 1;
      if (!selfPaired) {
        classOf[P] = (int)cls.size();
        fwd[P] = 1;
      }
      cls.push_back(std::move(E));
    } else {
      long Rs = (long)a * S.size[i];
      int c = (int)(Rs / S.size[j]);
      if (a > maxContrib || c > maxContrib) continue;
      EdgeClass E;
      E.oi = i;
      E.oj = j;
      E.ci = a;
      E.cj = c;
      E.ni.resize((size_t)S.size[i] * a);
      E.nj.resize((size_t)S.size[j] * c);
      classOf[L] = (int)cls.size();
      fwd[L] = 1;
      cls.push_back(std::move(E));
    }
  }
  // pass 2: one sweep over all ordered pairs fills neighbour arrays
  vector<vector<int>> fillI(cls.size()), fillJ(cls.size());
  for (size_t c = 0; c < cls.size(); c++) {
    fillI[c].assign(S.size[cls[c].oi], 0);
    if (cls[c].oi != cls[c].oj) fillJ[c].assign(S.size[cls[c].oj], 0);
  }
  for (int x = 0; x < n; x++)
    for (int w = 0; w < n; w++) {
      if (w == x) continue;
      int L = lab[(size_t)x * n + w];
      int c = classOf[L];
      if (c < 0 || !fwd[L]) continue;
      EdgeClass& E = cls[c];
      int t = x - S.start[E.oi];
      E.ni[(size_t)t * E.ci + fillI[c][t]++] = w;
      if (E.oi != E.oj) {
        int s2 = w - S.start[E.oj];
        E.nj[(size_t)s2 * E.cj + fillJ[c][s2]++] = x;
      }
    }
  return cls;
}


// ---------------------------------------------------------------------------
// Cached orbitals per pair of actions (a,b): G-orbits on O_a x O_b (all ordered pairs,
// including the diagonal when a == b).  Only labels with out/in-degree <= CACHE_MAXC keep
// their pair lists.
static const int CACHE_MAXC = 16;
struct PairOrb {
  int sa = 0, sb = 0, nlab = 0, diagLab = -1;
  vector<int> cnt, transp;                 // per label
  vector<vector<pair<int, int>>> pairs;    // per label (empty if not admissible)
};
static map<pair<int, int>, PairOrb> pairCache;
static long cacheEntries = 0;
static const PairOrb& getPair(int a, int b) {
  auto key = make_pair(a, b);
  auto it = pairCache.find(key);
  if (it != pairCache.end()) return it->second;
  if (cacheEntries > 150000000L) {
    pairCache.clear();
    cacheEntries = 0;
  }
  PairOrb P;
  const Action& A1 = acts[a];
  const Action& A2 = acts[b];
  P.sa = A1.deg;
  P.sb = A2.deg;
  vector<int> lab((size_t)P.sa * P.sb, -1);
  vector<int> st;
  for (size_t k0 = 0; k0 < lab.size(); k0++) {
    if (lab[k0] >= 0) continue;
    int L = P.nlab++;
    lab[k0] = L;
    st.clear();
    st.push_back((int)k0);
    long c = 0;
    while (!st.empty()) {
      size_t k = (size_t)st.back();
      st.pop_back();
      c++;
      int x = (int)(k / P.sb), y = (int)(k % P.sb);
      for (int g = 0; g < ngens; g++) {
        size_t k2 = (size_t)A1.gens[g][x] * P.sb + A2.gens[g][y];
        if (lab[k2] < 0) {
          lab[k2] = L;
          st.push_back((int)k2);
        }
      }
    }
    P.cnt.push_back((int)c);
  }
  P.pairs.assign(P.nlab, {});
  vector<char> adm(P.nlab, 0);
  for (int L = 0; L < P.nlab; L++) {
    int outd = P.cnt[L] / P.sa, ind = P.cnt[L] / P.sb;
    adm[L] = (outd <= CACHE_MAXC && ind <= CACHE_MAXC);
    if (adm[L]) P.pairs[L].reserve(P.cnt[L]);
  }
  for (int x = 0; x < P.sa; x++)
    for (int y = 0; y < P.sb; y++) {
      int L = lab[(size_t)x * P.sb + y];
      if (adm[L]) P.pairs[L].push_back({x, y});
    }
  if (a == b) {
    P.transp.assign(P.nlab, -1);
    P.diagLab = lab[0];
    for (int L = 0; L < P.nlab; L++) {
      // find a representative pair of L
      // (scan row-wise; cheap relative to the flood fill)
      for (int x = 0; x < P.sa && P.transp[L] < 0; x++)
        for (int y = 0; y < P.sb; y++)
          if (lab[(size_t)x * P.sb + y] == L) {
            P.transp[L] = lab[(size_t)y * P.sb + x];
            break;
          }
    }
  }
  for (auto& v : P.pairs) cacheEntries += (long)v.size();
  cacheEntries += P.nlab;
  return pairCache.emplace(key, std::move(P)).first->second;
}

static vector<EdgeClass> buildClassesCached(const vector<int>& combo, const GSet& S, int maxContrib) {
  vector<EdgeClass> cls;
  int b = S.b;
  for (int i = 0; i < b; i++) {
    // inner classes of orbit i
    const PairOrb& P = getPair(combo[i], combo[i]);
    for (int L = 0; L < P.nlab; L++) {
      if (L == P.diagLab) continue;
      int T = P.transp[L];
      bool selfp = (T == L);
      if (!selfp && L > T) continue;
      int outd = P.cnt[L] / P.sa;
      int contrib = selfp ? outd : 2 * outd;
      if (contrib > maxContrib || P.pairs[L].empty()) continue;
      if (!selfp && P.pairs[T].empty()) continue;
      EdgeClass E;
      E.oi = E.oj = i;
      E.ci = E.cj = contrib;
      E.ni.resize((size_t)S.size[i] * contrib);
      vector<int> fill(S.size[i], 0);
      for (auto& pr : P.pairs[L]) E.ni[(size_t)pr.first * contrib + fill[pr.first]++] = S.start[i] + pr.second;
      if (!selfp)
        for (auto& pr : P.pairs[T]) E.ni[(size_t)pr.first * contrib + fill[pr.first]++] = S.start[i] + pr.second;
      cls.push_back(std::move(E));
    }
  }
  for (int i = 0; i < b; i++)
    for (int j = i + 1; j < b; j++) {
      int ai = combo[i], aj = combo[j];
      bool sw = ai > aj;
      const PairOrb& P = sw ? getPair(aj, ai) : getPair(ai, aj);
      for (int L = 0; L < P.nlab; L++) {
        if (P.pairs[L].empty()) continue;
        // orientation: x in O_i, y in O_j
        int outd = sw ? P.cnt[L] / P.sb : P.cnt[L] / P.sa;   // per vertex of O_i
        int ind = sw ? P.cnt[L] / P.sa : P.cnt[L] / P.sb;    // per vertex of O_j
        if (outd > maxContrib || ind > maxContrib) continue;
        EdgeClass E;
        E.oi = i;
        E.oj = j;
        E.ci = outd;
        E.cj = ind;
        E.ni.resize((size_t)S.size[i] * outd);
        E.nj.resize((size_t)S.size[j] * ind);
        vector<int> fi(S.size[i], 0), fj(S.size[j], 0);
        for (auto& pr : P.pairs[L]) {
          int x = sw ? pr.second : pr.first;   // local in O_i
          int y = sw ? pr.first : pr.second;   // local in O_j
          E.ni[(size_t)x * outd + fi[x]++] = S.start[j] + y;
          E.nj[(size_t)y * ind + fj[y]++] = S.start[i] + x;
        }
        cls.push_back(std::move(E));
      }
    }
  return cls;
}

struct Searcher {
  const GSet& S;
  const vector<EdgeClass>& C;
  vector<int> idx;  // classes admissible for this cell
  int Delta, D;
  vector<char> chosen;  // indexed by position in idx
  vector<int> deg;
  vector<vector<pair<int, int>>> inc;  // per orbit: (class id in C, side)
  vector<int> dist, q;
  mt19937_64 rng;
  long nodes = 0, nodeCap = 0, leaves = 0;
  bool found = false;
  vector<char> initSel;  // optional warm start (positions in idx)
  double tempScale = 0.02;
  // bitset adjacency (used when n <= 512)
  int W = 0;
  bool useBits = false;
  vector<uint64_t> A;  // n x W
  void toggleClass(int c) {
    const auto& E = C[c];
    int k = E.ci;
    bool inner = (E.oi == E.oj);
    for (int t = 0; t < S.size[E.oi]; t++) {
      int x = S.start[E.oi] + t;
      for (int r = 0; r < k; r++) {
        int y = E.ni[(size_t)t * k + r];
        A[(size_t)x * W + (y >> 6)] ^= (1ULL << (y & 63));
        // inner classes list each edge from both ends; cross classes only from the O_i end
        if (!inner) A[(size_t)y * W + (x >> 6)] ^= (1ULL << (x & 63));
      }
    }
  }
  int ballBits(int x) {
    uint64_t vis[8], fr[8], nf[8];
    for (int w = 0; w < W; w++) vis[w] = fr[w] = 0;
    vis[x >> 6] |= 1ULL << (x & 63);
    fr[x >> 6] |= 1ULL << (x & 63);
    for (int d = 0; d < D; d++) {
      for (int w = 0; w < W; w++) nf[w] = 0;
      bool any = false;
      for (int w = 0; w < W; w++) {
        uint64_t b = fr[w];
        while (b) {
          int y = (w << 6) + __builtin_ctzll(b);
          b &= b - 1;
          const uint64_t* row = &A[(size_t)y * W];
          for (int u = 0; u < W; u++) nf[u] |= row[u];
        }
      }
      for (int w = 0; w < W; w++) {
        nf[w] &= ~vis[w];
        vis[w] |= nf[w];
        fr[w] = nf[w];
        if (nf[w]) any = true;
      }
      if (!any) break;
    }
    int cnt = 0;
    for (int w = 0; w < W; w++) cnt += __builtin_popcountll(vis[w]);
    return cnt;
  }

  Searcher(const GSet& s, const vector<EdgeClass>& c, int Dl, int Dm, uint64_t seed)
      : S(s), C(c), Delta(Dl), D(Dm), rng(seed) {
    for (int k = 0; k < (int)C.size(); k++) {
      const auto& E = C[k];
      if (E.ci <= Delta && E.cj <= Delta) idx.push_back(k);
    }
    // order: larger contributions first, then by orbit pair (helps pruning)
    stable_sort(idx.begin(), idx.end(), [&](int a, int b) {
      int sa = C[a].ci + C[a].cj, sb = C[b].ci + C[b].cj;
      return sa > sb;
    });
    chosen.assign(idx.size(), 0);
    deg.assign(S.b, 0);
    inc.assign(S.b, {});
    dist.assign(S.n, -1);
    q.resize(S.n);
    if (S.n <= 512) {
      useBits = true;
      W = (S.n + 63) / 64;
      A.assign((size_t)S.n * W, 0);
    }
  }
  bool fits(int p) const {
    const auto& E = C[idx[p]];
    if (E.oi == E.oj) return deg[E.oi] + E.ci <= Delta;
    return deg[E.oi] + E.ci <= Delta && deg[E.oj] + E.cj <= Delta;
  }
  void add(int p) {
    const auto& E = C[idx[p]];
    chosen[p] = 1;
    if (useBits) toggleClass(idx[p]);
    deg[E.oi] += E.ci;
    inc[E.oi].push_back({idx[p], 0});
    if (E.oi != E.oj) {
      deg[E.oj] += E.cj;
      inc[E.oj].push_back({idx[p], 1});
    }
  }
  void rem(int p) {
    const auto& E = C[idx[p]];
    chosen[p] = 0;
    if (useBits) toggleClass(idx[p]);
    int c = idx[p];
    auto drop = [&](int o) {
      auto& L = inc[o];
      for (size_t k = 0; k < L.size(); k++)
        if (L[k].first == c) {
          L[k] = L.back();
          L.pop_back();
          break;
        }
    };
    deg[E.oi] -= E.ci;
    drop(E.oi);
    if (E.oi != E.oj) {
      deg[E.oj] -= E.cj;
      drop(E.oj);
    }
  }
  // BFS ball size from x over incidence lists L (per orbit)
  int ball(int x, const vector<vector<pair<int, int>>>& L) {
    int h = 0, t = 0;
    q[t++] = x;
    dist[x] = 0;
    while (h < t) {
      int y = q[h++];
      int dy = dist[y];
      if (dy >= D) continue;
      int o = S.orbOf[y], loc = y - S.start[o];
      for (auto& pr : L[o]) {
        const auto& E = C[pr.first];
        int k = pr.second == 0 ? E.ci : E.cj;
        const int* nb = pr.second == 0 ? &E.ni[(size_t)loc * k] : &E.nj[(size_t)loc * k];
        for (int r = 0; r < k; r++) {
          int z = nb[r];
          if (dist[z] < 0) {
            dist[z] = dy + 1;
            q[t++] = z;
          }
        }
      }
    }
    for (int r = 0; r < t; r++) dist[q[r]] = -1;
    return t;
  }
  long scoreWith(const vector<vector<pair<int, int>>>& L) {
    long f = 0;
    for (int o = 0; o < S.b; o++) f += (long)S.size[o] * (S.n - ball(S.start[o], L));
    return f;
  }
  long score() {
    if (!useBits) return scoreWith(inc);
    long f = 0;
    for (int o = 0; o < S.b; o++) f += (long)S.size[o] * (S.n - ballBits(S.start[o]));
    return f;
  }
  // superset test: chosen + all admissible classes at positions >= pos that fit individually
  // per-class bitset rows for the superset test (built lazily)
  vector<vector<uint64_t>> CB;
  bool cbReady = false;
  void buildCB() {
    CB.assign(idx.size(), {});
    for (size_t p = 0; p < idx.size(); p++) {
      const auto& E = C[idx[p]];
      vector<uint64_t> R((size_t)S.n * W, 0);
      int k = E.ci;
      bool inner = (E.oi == E.oj);
      for (int t = 0; t < S.size[E.oi]; t++) {
        int x = S.start[E.oi] + t;
        for (int r = 0; r < k; r++) {
          int y = E.ni[(size_t)t * k + r];
          R[(size_t)x * W + (y >> 6)] |= 1ULL << (y & 63);
          if (!inner) R[(size_t)y * W + (x >> 6)] |= 1ULL << (x & 63);
        }
      }
      CB[p] = std::move(R);
    }
    cbReady = true;
  }
  vector<uint64_t> U;
  int ballU(int x) {
    uint64_t vis[8], fr[8], nf[8];
    for (int w = 0; w < W; w++) vis[w] = fr[w] = 0;
    vis[x >> 6] |= 1ULL << (x & 63);
    fr[x >> 6] |= 1ULL << (x & 63);
    for (int d = 0; d < D; d++) {
      for (int w = 0; w < W; w++) nf[w] = 0;
      for (int w = 0; w < W; w++) {
        uint64_t b = fr[w];
        while (b) {
          int y = (w << 6) + __builtin_ctzll(b);
          b &= b - 1;
          const uint64_t* row = &U[(size_t)y * W];
          for (int u = 0; u < W; u++) nf[u] |= row[u];
        }
      }
      bool any = false;
      for (int w = 0; w < W; w++) {
        nf[w] &= ~vis[w];
        vis[w] |= nf[w];
        fr[w] = nf[w];
        any |= nf[w] != 0;
      }
      if (!any) break;
    }
    int c = 0;
    for (int w = 0; w < W; w++) c += __builtin_popcountll(vis[w]);
    return c;
  }
  bool supersetOK(int pos) {
    if (useBits && (long)idx.size() * S.n * W <= 40000000L) {
      if (!cbReady) buildCB();
      U = A;  // chosen classes
      for (int p = pos; p < (int)idx.size(); p++)
        if (!chosen[p] && fits(p)) {
          const auto& R = CB[p];
          for (size_t t = 0; t < U.size(); t++) U[t] |= R[t];
        }
      for (int o = 0; o < S.b; o++)
        if (ballU(S.start[o]) < S.n) return false;
      return true;
    }
    auto L = inc;
    for (int p = pos; p < (int)idx.size(); p++)
      if (!chosen[p] && fits(p)) {
        const auto& E = C[idx[p]];
        L[E.oi].push_back({idx[p], 0});
        if (E.oi != E.oj) L[E.oj].push_back({idx[p], 1});
      }
    for (int o = 0; o < S.b; o++)
      if (ball(S.start[o], L) < S.n) return false;
    return true;
  }
  void dfs(int pos) {
    if (found || nodes > nodeCap) return;
    nodes++;
    if (!supersetOK(pos)) return;
    if (pos == (int)idx.size()) {
      for (int p = 0; p < (int)idx.size(); p++)
        if (!chosen[p] && fits(p)) return;  // not maximal (a dominating selection exists)
      leaves++;
      if (score() == 0) found = true;
      return;
    }
    if (fits(pos)) {
      add(pos);
      dfs(pos + 1);
      if (found) return;
      rem(pos);
    }
    dfs(pos + 1);
  }
  // returns 1 found, 0 exhausted (none), -1 cap
  int exhaustive(long cap) {
    nodes = leaves = 0;
    nodeCap = cap;
    found = false;
    dfs(0);
    if (found) return 1;
    return nodes > nodeCap ? -1 : 0;
  }
  long anneal(long iters, int restarts) {
    int m = (int)idx.size();
    vector<int> order(m);
    iota(order.begin(), order.end(), 0);
    long gbest = LONG_MAX;
    vector<char> gsel;
    for (int rs = 0; rs < restarts; rs++) {
      for (int p = 0; p < m; p++)
        if (chosen[p]) rem(p);
      if (!initSel.empty()) {
        for (int p = 0; p < m; p++)
          if (initSel[p] && fits(p)) add(p);
      }
      shuffle(order.begin(), order.end(), rng);
      for (int p : order)
        if (fits(p)) add(p);
      long f = score(), best = f;
      vector<char> sel = chosen;
      if (f == 0) return 0;
      double T0 = max(1.0, tempScale * f), T1 = 0.5;
      vector<int> cl;
      for (long it = 0; it < iters && best > 0; it++) {
        double T = T0 * pow(T1 / T0, (double)it / iters);
        cl.clear();
        for (int p = 0; p < m; p++)
          if (chosen[p]) cl.push_back(p);
        if (cl.empty()) break;
        int k = (rng() % 4 == 0) ? 2 : 1;
        vector<int> removed;
        for (int r = 0; r < k && !cl.empty(); r++) {
          int j = rng() % cl.size();
          removed.push_back(cl[j]);
          rem(cl[j]);
          cl[j] = cl.back();
          cl.pop_back();
        }
        vector<char> before = chosen;
        if ((it & 63) == 0) shuffle(order.begin(), order.end(), rng);
        {
          int off = (int)(rng() % (uint64_t)m);
          for (int r = 0; r < m; r++) {
            int p = order[(off + r) % m];
            if (!chosen[p] && fits(p) && find(removed.begin(), removed.end(), p) == removed.end()) add(p);
          }
        }
        for (int p : removed)
          if (!chosen[p] && fits(p)) add(p);
        long g = score();
        if (g <= f || (double)(rng() % 1000000) / 1e6 < exp(-(double)(g - f) / T)) {
          f = g;
          if (f < best) {
            best = f;
            sel = chosen;
          }
        } else {
          for (int p = 0; p < m; p++)
            if (chosen[p] && !before[p]) rem(p);
          for (int p : removed) add(p);
        }
      }
      if (best < gbest) {
        gbest = best;
        gsel = sel;
      }
      if (gbest == 0) break;
    }
    for (int p = 0; p < m; p++)
      if (chosen[p]) rem(p);
    for (int p = 0; p < m; p++)
      if (gsel[p]) add(p);
    return gbest;
  }
  vector<vector<int>> adjacency() {
    vector<vector<int>> adj(S.n);
    for (int o = 0; o < S.b; o++)
      for (auto& pr : inc[o]) {
        const auto& E = C[pr.first];
        int k = pr.second == 0 ? E.ci : E.cj;
        const auto& V = pr.second == 0 ? E.ni : E.nj;
        for (int t = 0; t < S.size[o]; t++)
          for (int r = 0; r < k; r++) adj[S.start[o] + t].push_back(V[(size_t)t * k + r]);
      }
    return adj;
  }
};

// independent all-pairs check: returns diameter (99 disconnected, negative = not simple)
static pair<int, int> verifyGraph(const vector<vector<int>>& adj) {
  int n = (int)adj.size(), maxdeg = 0;
  for (int x = 0; x < n; x++) {
    auto v = adj[x];
    sort(v.begin(), v.end());
    if (adjacent_find(v.begin(), v.end()) != v.end()) return {-2, 0};
    for (int y : v) {
      if (y == x) return {-3, 0};
      if (find(adj[y].begin(), adj[y].end(), x) == adj[y].end()) return {-4, 0};
    }
    maxdeg = max(maxdeg, (int)v.size());
  }
  int diam = 0;
  vector<int> dd(n);
  for (int s = 0; s < n; s++) {
    fill(dd.begin(), dd.end(), -1);
    vector<int> qq{s};
    dd[s] = 0;
    for (size_t h = 0; h < qq.size(); h++)
      for (int z : adj[qq[h]])
        if (dd[z] < 0) {
          dd[z] = dd[qq[h]] + 1;
          qq.push_back(z);
        }
    if ((int)qq.size() < n) return {99, maxdeg};
    diam = max(diam, dd[qq.back()]);
  }
  return {diam, maxdeg};
}

static void writeEdges(const string& fn, const vector<vector<int>>& adj) {
  vector<pair<int, int>> ed;
  for (int x = 0; x < (int)adj.size(); x++)
    for (int y : adj[x])
      if (x < y) ed.push_back({x, y});
  sort(ed.begin(), ed.end());
  FILE* f = fopen(fn.c_str(), "w");
  fprintf(f, "%zu %zu\n", adj.size(), ed.size());
  for (auto& e : ed) fprintf(f, "%d %d\n", e.first, e.second);
  fclose(f);
}

static void genCombos(int maxorb, int lo, int hi, vector<vector<int>>& out, long cap) {
  vector<int> cur;
  int na = (int)acts.size();
  function<void(int, int)> rec = [&](int s0, int sum) {
    if ((long)out.size() >= cap) return;
    if (sum >= lo && sum <= hi && !cur.empty()) out.push_back(cur);
    if ((int)cur.size() == maxorb) return;
    for (int a = s0; a < na; a++) {
      if (sum + acts[a].deg > hi) continue;
      cur.push_back(a);
      rec(a, sum + acts[a].deg);
      cur.pop_back();
    }
  };
  rec(0, 0);
}

int main(int argc, char** argv) {
  if (argc < 3) {
    fprintf(stderr, "usage: orbsearch2 GROUPFILE CELLSFILE [opts]\n");
    return 1;
  }
  string gfile = argv[1], cfile = argv[2];
  int maxorb = 3, restarts = 2;
  long nodecap = 200000, saIters = 0, maxcombos = 2000000;
  uint64_t seed = 12345;
  string outdir = ".", onlyCombo;
  bool quietNone = false;
  long maxClasses = 1000000, screenIters = 0, escIters = 20000;
  string initFile;
  double tempScale = 0.02, saveOpen = -1;
  int screenRestarts = 1;
  int minRegular = 0;
  bool useCache = true;
  long preIters = 0;
  int preRestarts = 2;
  double preCut = 0.22;
  long esc2Iters = 0;
  int esc2Restarts = 12;
  double esc2Frac = 0.15;
  double escFrac = 0.004;
  for (int i = 3; i < argc; i++) {
    string a = argv[i];
    auto nx = [&]() { return string(argv[++i]); };
    if (a == "--maxorb") maxorb = stoi(nx());
    else if (a == "--nodecap") nodecap = stol(nx());
    else if (a == "--sa") saIters = stol(nx());
    else if (a == "--restarts") restarts = stoi(nx());
    else if (a == "--seed") seed = stoull(nx());
    else if (a == "--outdir") outdir = nx();
    else if (a == "--maxcombos") maxcombos = stol(nx());
    else if (a == "--combo") onlyCombo = nx();
    else if (a == "--quiet-none") quietNone = true;
    else if (a == "--all") onlyCombo = "ALL";
    else if (a == "--init") initFile = nx();
    else if (a == "--temp") tempScale = stod(nx());
    else if (a == "--screen-restarts") screenRestarts = stoi(nx());
    else if (a == "--min-regular") minRegular = stoi(nx());
    else if (a == "--nocache") useCache = false;
    else if (a == "--prescreen") preIters = stol(nx());
    else if (a == "--prescreen-restarts") preRestarts = stoi(nx());
    else if (a == "--prescreen-cut") preCut = stod(nx());
    else if (a == "--esc2") esc2Iters = stol(nx());
    else if (a == "--esc2-restarts") esc2Restarts = stoi(nx());
    else if (a == "--esc2frac") esc2Frac = stod(nx());
    else if (a == "--save-open") saveOpen = stod(nx());
    else if (a == "--maxclasses") maxClasses = stol(nx());
    else if (a == "--screen") screenIters = stol(nx());
    else if (a == "--esc") escIters = stol(nx());
    else if (a == "--escfrac") escFrac = stod(nx());
  }
  readGroup(gfile);
  vector<Cell> cells;
  {
    ifstream in(cfile);
    Cell c;
    while (in >> c.Delta >> c.D >> c.lo >> c.hi) cells.push_back(c);
  }
  int lo = INT32_MAX, hi = 0, maxDelta = 0;
  for (auto& c : cells) {
    lo = min(lo, c.lo);
    hi = max(hi, c.hi);
    maxDelta = max(maxDelta, c.Delta);
  }
  vector<vector<int>> combos;
  if (onlyCombo == "ALL") {
    vector<int> cmb(acts.size());
    iota(cmb.begin(), cmb.end(), 0);
    combos.push_back(cmb);
  } else if (!onlyCombo.empty()) {
    vector<int> cmb;
    stringstream ss(onlyCombo);
    string t;
    while (getline(ss, t, ',')) cmb.push_back(stoi(t));
    combos.push_back(cmb);
  } else {
    genCombos(maxorb, lo, hi, combos, maxcombos);
  }
  fprintf(stderr, "group %s order %ld: %zu actions, %zu combos\n", gname.c_str(), gorder, acts.size(),
          combos.size());
  mt19937_64 seeder(seed);
  long nNone = 0, nOpen = 0, nFound = 0, nTried = 0;
  auto t0 = chrono::steady_clock::now();
  for (auto& cmb : combos) {
    if (minRegular > 0) {
      int nr = 0;
      for (int a : cmb)
        if (acts[a].stab == 1) nr++;
      if (nr < minRegular) continue;
    }
    GSet S = buildGSet(cmb);
    bool any = false;
    int cellMaxDelta = 0;
    for (auto& cell : cells)
      if (S.n >= cell.lo && S.n <= cell.hi) {
        any = true;
        cellMaxDelta = max(cellMaxDelta, cell.Delta);
      }
    if (!any) continue;
    vector<EdgeClass> C = useCache ? buildClassesCached(cmb, S, cellMaxDelta) : buildClasses(S, cellMaxDelta);
    string cs, ss;
    for (size_t r = 0; r < cmb.size(); r++) {
      cs += (r ? "," : "") + to_string(cmb[r]);
      ss += (r ? "+" : "") + to_string(acts[cmb[r]].deg) + "[" + to_string(acts[cmb[r]].stab) + "]";
    }
    for (auto& cell : cells) {
      if (S.n < cell.lo || S.n > cell.hi) continue;
      // local Moore pre-check: every orbit needs degree >= dmin
      Searcher sr(S, C, cell.Delta, cell.D, seeder());
      if (sr.idx.empty()) continue;
      sr.tempScale = tempScale;
      if (!initFile.empty()) {
        // mark classes all of whose edges lie in the init edge set
        ifstream in(initFile);
        int nn, mm;
        in >> nn >> mm;
        vector<vector<char>> E0(S.n, vector<char>(S.n, 0));
        for (int e = 0; e < mm; e++) {
          int u, v;
          in >> u >> v;
          if (u < S.n && v < S.n) E0[u][v] = E0[v][u] = 1;
        }
        sr.initSel.assign(sr.idx.size(), 0);
        int marked = 0;
        for (size_t p = 0; p < sr.idx.size(); p++) {
          const auto& EC = C[sr.idx[p]];
          bool all = true;
          int k = EC.ci;
          for (int t = 0; t < S.size[EC.oi] && all; t++)
            for (int r = 0; r < k; r++)
              if (!E0[S.start[EC.oi] + t][EC.ni[(size_t)t * k + r]]) {
                all = false;
                break;
              }
          if (all) {
            sr.initSel[p] = 1;
            marked++;
          }
        }
        fprintf(stderr, "init: marked %d classes from %s\n", marked, initFile.c_str());
      }
      nTried++;
      int res = -1;
      string mode = "EX";
      long bestf = -1;
      if ((long)sr.idx.size() <= maxClasses) res = sr.exhaustive(nodecap);
      if (res == -1 && saIters > 0) {
        bestf = sr.anneal(saIters, restarts);
        if (bestf == 0) res = 1;
        mode = "SA";
      }
      bool preCutOff = false;
      if (res == -1 && screenIters > 0 && preIters > 0) {
        bestf = sr.anneal(preIters, preRestarts);
        mode = "PRE";
        if (bestf == 0) res = 1;
        else if (bestf > preCut * (double)S.n * S.n) preCutOff = true;
      }
      if (res == -1 && screenIters > 0 && !preCutOff) {
        bestf = sr.anneal(screenIters, screenRestarts);
        mode = "SC";
        if (bestf > 0 && esc2Iters > 0 && bestf <= esc2Frac * (double)S.n * S.n) {
          long b2 = sr.anneal(esc2Iters, esc2Restarts);
          bestf = min(bestf, b2);
          if (b2 == 0) bestf = 0;
          mode = "SC2";
        }
        if (bestf > 0 && bestf <= escFrac * (double)S.n * S.n) {
          bestf = sr.anneal(escIters, restarts);
          mode = "ESC";
        }
        if (bestf == 0) res = 1;
      }
      if (res == 1) {
        nFound++;
        auto adj = sr.adjacency();
        auto vd = verifyGraph(adj);
        string fn = outdir + "/found_d" + to_string(cell.Delta) + "_k" + to_string(cell.D) + "_n" +
                    to_string(S.n) + "_" + gname + "_" + cs + ".edges";
        for (auto& ch : fn)
          if (ch == ',') ch = '-';
        writeEdges(fn, adj);
        printf("FOUND %d %d %d %s %s %s %s verify_diam=%d maxdeg=%d %s\n", cell.Delta, cell.D, S.n,
               gname.c_str(), cs.c_str(), ss.c_str(), mode.c_str(), vd.first, vd.second, fn.c_str());
      } else if (res == 0) {
        nNone++;
        if (!quietNone)
          printf("NONE %d %d %d %s %s %s classes=%zu nodes=%ld\n", cell.Delta, cell.D, S.n, gname.c_str(),
                 cs.c_str(), ss.c_str(), sr.idx.size(), sr.nodes);
      } else {
        nOpen++;
        if (saveOpen > 0 && bestf > 0 && bestf <= saveOpen * (double)S.n * S.n) {
          string fn = outdir + "/open_d" + to_string(cell.Delta) + "_k" + to_string(cell.D) + "_n" +
                      to_string(S.n) + "_f" + to_string(bestf) + "_" + gname + "_" + cs + ".edges";
          for (auto& ch : fn)
            if (ch == ',') ch = '-';
          writeEdges(fn, sr.adjacency());
        }
        printf("OPEN %d %d %d %s %s %s classes=%zu bestf=%ld\n", cell.Delta, cell.D, S.n, gname.c_str(),
               cs.c_str(), ss.c_str(), sr.idx.size(), bestf);
      }
      fflush(stdout);
    }
  }
  double secs = chrono::duration<double>(chrono::steady_clock::now() - t0).count();
  fprintf(stderr, "done %s: tried=%ld found=%ld none=%ld open=%ld time=%.1fs\n", gname.c_str(), nTried, nFound,
          nNone, nOpen, secs);
  printf("SUMMARY %s order=%ld actions=%zu tried=%ld found=%ld none=%ld open=%ld time=%.1f\n", gname.c_str(),
         gorder, acts.size(), nTried, nFound, nNone, nOpen, secs);
  return 0;
}
