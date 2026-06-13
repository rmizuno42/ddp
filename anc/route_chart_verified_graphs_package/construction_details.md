# Route-chart lift による degree/diameter グラフ構成

このパッケージには、route-chart lift に基づく 2 つの構成済みグラフを収録している。

| パラメータ | 頂点数 | 最大次数 | 直径上界 | edge list |
|---|---:|---:|---:|---|
| `(16,5)` | 147,456 | 16 | 5 | `graphs/16_5_147456/final_graph_edges.tsv.gz` |
| `(12,5)` | 34,992 | 12 | 5 | `graphs/12_5_34992/final_graph_edges.tsv.gz` |

公開記録として主張する前には、最新版の degree/diameter 表との照合と第三者検証を行うこと。
この文書は、構成方法をこの zip だけで理解・再現できるようにまとめたものである。

---

## 1. 背景と目標

degree/diameter problem では、最大次数 `d`、直径高々 `k` の単純無向グラフで、頂点数をなるべく大きくする。
ここで構成するグラフは、いずれも単純無向グラフであり、次を満たす。

- `(16,5)` 構成：`|V| = 147456`, `Δ = 16`, `diam <= 5`
- `(12,5)` 構成：`|V| = 34992`, `Δ = 12`, `diam <= 5`

両方とも同じ 144 頂点 controller を使い、fiber だけを変える。

---

## 2. 構成の全体像

構成は次の直積型である。

\[
V(G)=V(C)\times F^5.
\]

ここで `C` は 144 頂点の 4-正則 controller、`F` は有限体である。

- `(16,5)` では `F = GF(4)` なので `|F|^5 = 4^5 = 1024`。
- `(12,5)` では `F = GF(3)` なので `|F|^5 = 3^5 = 243`。

従って、

\[
144\cdot 4^5 = 147456,
\qquad
144\cdot 3^5 = 34992.
\]

controller は 4-正則である。各 controller edge ごとに `|F|` 通りの fiber control を張るため、最終グラフの次数は

\[
4|F|.
\]

したがって `(16,5)` では次数 16、`(12,5)` では次数 12 になる。

---

## 3. Controller の構成

### 3.1 Base multigraph

controller は、6 頂点の loopless 4-正則 multigraph に、群

\[
H=C_4\times C_6
\]

の voltage を載せた regular lift として作る。

base の頂点は `0,1,2,3,4,5`。base edge と voltage は次である。

| edge id | u | v | voltage in C4 | voltage in C6 |
|---:|---:|---:|---:|---:|
| 0 | 0 | 2 | 1 | 0 |
| 1 | 0 | 3 | 2 | 4 |
| 2 | 0 | 4 | 2 | 0 |
| 3 | 0 | 4 | 2 | 5 |
| 4 | 1 | 2 | 1 | 2 |
| 5 | 1 | 3 | 3 | 5 |
| 6 | 1 | 5 | 1 | 1 |
| 7 | 1 | 5 | 1 | 0 |
| 8 | 2 | 4 | 2 | 2 |
| 9 | 2 | 5 | 1 | 5 |
| 10 | 3 | 4 | 1 | 5 |
| 11 | 3 | 5 | 3 | 1 |

同じ 2 頂点を結ぶ parallel edge は edge id で区別する。loop はない。
この表は `certificates/*/controller_c4xc6_multibase.txt` に収録している。

### 3.2 Voltage lift

`H=C4 x C6` の元を `(x,y)`、ただし `x mod 4`, `y mod 6` と書く。
base edge `e=(u,v)` の voltage を `γ_e=(α,β)` とする。

controller `C` の頂点は

\[
V(C)=\{0,1,2,3,4,5\}\times C_4\times C_6.
\]

従って

\[
|V(C)|=6\cdot 4\cdot 6=144.
\]

各 base edge `e=(u,v)` と各 `h=(x,y) in H` に対し、controller に無向辺

\[
(u,h) \sim (v,h+\gamma_e)
\]

を張る。逆向きでは voltage は `-γ_e` である。
検証スクリプトは、この controller が単純 4-正則連結グラフであることを確認する。

### 3.3 Controller coverage 条件

controller に必要な性質は：任意の ordered pair `(p,q)` について、長さちょうど 5 の nonbacktracking walk が存在すること。

ここで nonbacktracking とは、直前に使った edge をすぐ逆向きに戻らない walk のことである。

この性質は base voltage で確認できる。任意の base 頂点対 `(i,j)` について、base 上の exact length 5 nonbacktracking walk `P` の voltage sum 全体

\[
\{\gamma(P):P:i\to j,\ |P|=5,\ P\text{ nonbacktracking}\}
\]

が `H=C4 x C6` 全体を覆うことを検証する。そうすれば、lift 後の任意の `(i,h)` から `(j,h')` へは、差分 `h'-h` を持つ base walk を選べばよい。

同梱の `verify_candidate.py` はこの coverage を全てチェックする。

---

## 4. Controller edge の記号ラベル

fiber 側では controller walk の記号列を使う。記号集合は

\[
\{a,a^{-1},b,b^{-1}\}
\]

である。

controller は 4-正則なので、edge を 2 個の 2-factor に分けることができる。検証スクリプトでは、Euler tour の交互彩色により 2-factorization を作る。
各 2-factor は disjoint cycle の合併なので、各 cycle に向きを付ける。

- 第 1 の 2-factor の順向き edge を `a`、逆向きを `a^{-1}` とする。
- 第 2 の 2-factor の順向き edge を `b`、逆向きを `b^{-1}` とする。

このとき各 controller 頂点からは、4 記号 `a,a^{-1},b,b^{-1}` の edge がちょうど 1 本ずつ出る。
また、nonbacktracking walk では直前 edge の逆向きを使えないので、記号列には隣接する逆元対が現れない。したがって controller の nonbacktracking walk は reduced word を与える。

---

## 5. Fiber chart

### 5.1 Fiber transition

有限体 `F` 上の 5 次元空間 `F^5` を fiber とする。
各記号 `s in {a,a^{-1},b,b^{-1}}` に対して、行列

\[
A_s\in GL(5,F)
\]

とベクトル

\[
b_s\in F^5
\]

を用意する。

controller arc `u -> v` の記号が `s` のとき、最終グラフでは各 `λ in F` について

\[
(u,x)\sim (v,A_sx+\lambda b_s)
\]

という edge を張る。

逆向き edge と矛盾しないように、逆記号は

\[
A_{s^{-1}}=A_s^{-1},
\qquad
b_{s^{-1}}=A_s^{-1}b_s
\]

を満たすように取る。符号の違いは `λ` が体全体を走るため吸収される。

### 5.2 Controllability matrix

長さ 5 の reduced word

\[
w=s_1s_2s_3s_4s_5
\]

を固定する。この word に沿って fiber transition を合成すると、終点は

\[
x_5=A_wx_0+
\lambda_1 A_{s_5}A_{s_4}A_{s_3}A_{s_2}b_{s_1}+
\lambda_2 A_{s_5}A_{s_4}A_{s_3}b_{s_2}+
\lambda_3 A_{s_5}A_{s_4}b_{s_3}+
\lambda_4 A_{s_5}b_{s_4}+
\lambda_5 b_{s_5}.
\]

従って、次の 5 本の列ベクトルが `F^5` の基底であれば、任意の始点 fiber `x_0` と任意の終点 fiber `y` に対して、係数 `λ_1,...,λ_5` が一意に存在し、`x_5=y` を実現できる。

\[
M_w=\left[
A_{s_5}A_{s_4}A_{s_3}A_{s_2}b_{s_1},
A_{s_5}A_{s_4}A_{s_3}b_{s_2},
A_{s_5}A_{s_4}b_{s_3},
A_{s_5}b_{s_4},
b_{s_5}
\right].
\]

この構成では、全ての reduced word 長 5 について `M_w` が正則であることを検証している。
reduced word は

\[
4\cdot 3^4=324
\]

個である。

### 5.3 収録している chart data

- `(16,5)` 用：`certificates/16_5_147456/gf4_s5_universal.txt`
  - `GF(4)` の符号化は `0,1,2=α,3=α+1`, `α^2=α+1`。
- `(12,5)` 用：`certificates/12_5_34992/gf3_s5_universal.txt`
  - `GF(3)` は通常の mod 3 演算。

各 `verify_candidate.py` は chart data を内部に持ち、全 reduced word の rank 条件を検証する。

---

## 6. 直径証明

任意の 2 頂点

\[
(c,x),(d,y)\in V(C)\times F^5
\]

を取る。

1. controller coverage により、`c` から `d` への exact length 5 nonbacktracking walk が存在する。
2. その walk の記号列は reduced word `s_1...s_5` である。
3. fiber chart 条件により、任意の `x,y` に対して、`x` を `y` に送る `λ_1,...,λ_5 in F` が存在する。
4. それらの `λ_i` に対応する edge を使えば、最終グラフで長さ 5 の path が得られる。

従って

\[
\operatorname{diam}(G)\le 5.
\]

次数は、controller の各頂点から 4 記号の edge が出て、それぞれに `|F|` 通りの fiber control があるので

\[
\Delta(G)=4|F|.
\]

---

## 7. Edge list の形式

各 edge list は gzip 圧縮 TSV である。

先頭行：

```text
n m
```

以降の各行：

```text
u<TAB>v
```

ここで頂点番号は `0,1,...,n-1`。

- `(16,5)` edge list:
  - `n=147456`
  - `m=1179648`
  - `m = n*16/2`
- `(12,5)` edge list:
  - `n=34992`
  - `m=209952`
  - `m = n*12/2`

---

## 8. 再現・検証方法

Python 3 で以下を実行する。

### `(16,5)`

```bash
cd scripts/16_5_147456
python3 verify_candidate.py
python3 generate_final_graph.py
```

期待される検証メッセージ：

```text
Base voltage coverage over C4 x C6: OK
Controller: OK; 144 vertices, simple 4-regular, exact labeled NB length-5 coverage
GF(4)^5 universal chart: OK; 324 reduced words checked, min rank 5; inverse-symbol data verified
Certificate complete: degree 16, diameter <=5, vertices = 144*4^5 = 147456
```

### `(12,5)`

```bash
cd scripts/12_5_34992
python3 verify_candidate.py
python3 generate_final_graph.py
```

期待される検証メッセージ：

```text
Base voltage coverage over C4 x C6: OK
Controller: OK; 144 vertices, simple 4-regular, exact labeled NB length-5 coverage
GF(3)^5 universal chart: OK; 324 reduced words checked, min rank 5; inverse-symbol data verified
Certificate complete: degree 12, diameter <=5, vertices = 144*3^5 = 34992
```

---

## 9. ファイル構成

```text
construction_details.md
SHA256SUMS.txt
graphs/
  16_5_147456/final_graph_edges.tsv.gz
  12_5_34992/final_graph_edges.tsv.gz
certificates/
  16_5_147456/controller_c4xc6_multibase.txt
  16_5_147456/gf4_s5_universal.txt
  12_5_34992/controller_c4xc6_multibase.txt
  12_5_34992/gf3_s5_universal.txt
scripts/
  16_5_147456/verify_candidate.py
  16_5_147456/generate_final_graph.py
  12_5_34992/verify_candidate.py
  12_5_34992/generate_final_graph.py
```

`SHA256SUMS.txt` は、この zip 内のファイルの SHA-256 checksum である。
