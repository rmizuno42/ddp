# 5,832 頂点の (12,4)-グラフ：構成と有限証明書

作成日：2026-09-24。

## 結果と比較対象

以下で定義する無向単純グラフ G は、頂点数 5,832、次数 12、直径 4 を持つ。したがって

\[
N(12,4)\ge 5832.
\]

2026-09-24 に参照した Comellas の表の (12,4) 欄は 5,184 であり、この掲載値より 648 頂点、12.5% 大きい。これは表に対する比較であり、未調査の文献を含めた網羅的な優先権調査の結論ではない。表の更新申請・外部への連絡は実施していない。

比較対象：
https://web.mat.upc.edu/francesc.comellas/delta-d/table_degree_diameter.html

## 1. 一般化 affine route-chart 定理

C を有限無向単純グラフ、V=F_q^s とする。有向辺 e=(u,v) に対して
A_e in GL_s(F_q), b_e != 0 を与え、逆辺について

\[
A_{\bar e}=A_e^{-1},\qquad
\langle b_{\bar e}\rangle=\langle A_e^{-1}b_e\rangle
\]

を仮定する。グラフ G の頂点を V(C)×V とし、辺を

\[
(u,x)\sim(v,A_ex+\lambda b_e),\qquad\lambda\in\mathbb F_q
\]

で定める。逆辺条件により無向となり、単純性と b_e != 0 より、(u,x) の次数は q deg_C(u) である。

controller walk P=e_1...e_l に対して

\[
A_P=A_{e_l}\cdots A_{e_1},\qquad
M_P=[A_{e_l}\cdots A_{e_2}b_{e_1}\mid\cdots\mid b_{e_l}]
\]

と置く。空の walk について A_P=I, Im(M_P)={0} とする。

**定理 1.** G の直径が D 以下であることと、すべての u,v,x に対し

\[
\mathbb F_q^s=
\bigcup_{P:u\to v,\ |P|\le D}
\left(A_Px+\operatorname{Im}M_P\right)
\]

が成立することは同値である。

**証明.** 固定した controller walk P に沿って到達する fiber 座標は、制御変数を順に代入すると厳密に A_P x+Im(M_P) となる。lift の walk は controller の walk に射影され、逆に上記集合の各点には対応する制御変数列がある。この対応により同値性が従う。walk の存在は同じ長さ以下の path の存在を意味する。□

## 2. Projective-pencil 補題と affine 中心

**補題 2.** K≤F_q^s, dim K=s-2 とする。K を含む相異なる q+1 個の超平面 H_0,...,H_q は F_q^s を覆い、相異なる二枚の交わりは K である。

**証明.** F_q^s/K は二次元であり、対応する一次元部分空間は P^1(F_q) の q+1 点で尽くされる。□

共通の affine (s-2)-flat を含む affine 超平面にも平行移動により同じ主張が成立する。ただし、方向部分空間が pencil をなすだけでは、異なる affine 中心を持つ到達集合の被覆は保証されない。

以下では A_{t^{-1}}=A_t^{-1} を厳密に満たす。したがって同じ reduced word r に自由簡約されるすべての word w は A_w=A_r を満たす。到達集合はすべて同じ中心 A_r x を持つ。この点が、始点 x=0 の検証をすべての始点に持ち上げる根拠である。

## 3. 明示的な fiber chart

体は F_3、fiber は F_3^4。座標は x=(x_0,x_1,x_2,x_3)^T とする。ラベルは A,B,C,D で、逆ラベルは A^{-1}=D, B^{-1}=C とする。

\[
A_A=\begin{pmatrix}
0&0&0&1\\
0&1&1&0\\
1&1&1&0\\
1&1&0&0
\end{pmatrix},\qquad
A_B=\begin{pmatrix}
2&1&0&0\\
0&0&1&0\\
1&0&0&1\\
2&1&0&2
\end{pmatrix}.
\]

\[
A_C=A_B^{-1}=\begin{pmatrix}
2&0&1&1\\
0&0&1&1\\
0&1&0&0\\
1&0&0&2
\end{pmatrix},\qquad
A_D=A_A^{-1}=\begin{pmatrix}
0&2&1&0\\
0&1&2&1\\
0&0&1&2\\
1&0&0&0
\end{pmatrix}.
\]

標準基底を e_0,...,e_3 とし、b_A=e_0, b_B=e_1, b_C=e_2, b_D=e_3 とする。直接計算により A_{t^{-1}}b_t=b_{t^{-1}} が成立する。

### 3.1 長さ4の単一 route

長さ4の reduced word 108 個のうち、次の8個だけが rank 3 であり、それ以外の100個は rank 4 である。

```
AABD ACDD BBAC BDCC CABB CCDB DBAA DDCA
```

この100個の集合を W_good とする。この有限な rank 検証は verify_certificate.py がすべて実行する。

### 3.2 長さ2の route の pencil 補修

任意の reduced word r of length 2 に対し、r に自由簡約され、長さが4以下の word は11個ある。到達部分空間のうち rank 3 のものは、相異なるものとしてちょうど4枚の超平面になる。それらは共通の二次元部分空間 Im(M_r) を含み、相異なる二枚の交わりは厳密に Im(M_r) である。

したがって補題2から

\[
\bigcup_{\substack{|w|\le4\\\operatorname{red}(w)=r}}
\operatorname{Im}M_w=\mathbb F_3^4.
\]

すべての w で A_w=A_r だから、任意の始点 x に対して同じ被覆が A_r x だけ平行移動される。

数の確認は 4(27-9)+9=81 である。

### 3.3 同一 fiber の補修

次の18個の二次元部分空間は相異なり、和集合は F_3^4 全体である。

\[
\left\{\langle e_i,e_j\rangle:0\le i<j\le3\right\}
\ \cup\
\left\{\langle e_t,A_t e_j\rangle:
0\le t,j\le3,\ j\ne t^{-1}\right\}.
\]

ここではラベル A,B,C,D を添字 0,1,2,3 と同一視している。

前半の平面には word i^{-1} i j^{-1} j に沿って到達する。後半の平面には word t^{-1} j^{-1} j t に沿って到達する。いずれも controller 上では始点に戻り、行列積は I である。よって任意の x から同一 fiber の全点に4歩以下で到達する。

この被覆は81個の座標について直接検証できる。verify_certificate.py は18平面の相異性・各平面の9点性・和集合の81点性をすべて確認する。空語に自由簡約される長さ4以下の33 word による被覆も独立に確認する。

## 4. 72頂点 controller

頂点は (g,i), 0≤g<8, i in Z/9Z。表の一行 (g,h,δ,t) はラベル t の辺

\[
(g,i)\xrightarrow{t}(h,i+\delta)
\]

をすべての i に与え、逆向きのラベルは t^{-1} とする。

| g | h | δ (mod 9) | label |
|---:|---:|---:|:---:|
|0|2|0|A|
|0|2|1|B|
|0|4|0|C|
|0|6|0|D|
|1|3|0|A|
|1|3|1|B|
|1|5|0|C|
|1|7|0|D|
|2|4|1|A|
|2|7|4|B|
|3|5|1|A|
|3|6|7|B|
|4|6|5|A|
|4|7|0|C|
|5|6|3|C|
|5|7|5|A|

この controller は無向単純4正則で、直径4、girth 5 である。

**有限 controller certificate.** 任意の ordered pair (u,v) について、次のいずれかが成立する。

- W_good のいずれかの word が u から v に到達する。
- 長さ2の reduced word が u から v に到達する。
- u=v。

重複は最初の条件を優先して分類すると、5,184 ordered pairs の内訳は順に 4,464、648、72 である。verify_certificate.py は72個すべての始点についてこの被覆を直接検証する。

この controller は exact-NB-4 ではない。長さちょうど4の NB walk で届かない頂点は、36個の始点では11個、残り36個の始点では9個ある。しかしそれらはすべて長さ2の route または同一 fiber の補修で処理できる。

## 5. 主定理

**定理3.** 上記 controller と fiber chart により定義されるグラフ

\[
V(G)=\{0,\ldots,7\}\times\mathbb Z_9\times\mathbb F_3^4
\]

は、5,832頂点の12正則無向単純グラフで、直径は4である。

**証明.** 各 controller 隣接点に対して3個の相異なる fiber 隣接点があり、異なる controller 隣接点の fiber は互いに異なる。したがって単純12正則で、頂点数は 8·9·3^4=5832 である。

任意の二頂点 (u,x),(v,y) を取る。controller certificate の最初の場合には rank 4 の一つの route に沿って任意の y に到達する。第二の場合には3.2の affine pencil によって任意の y に到達する。第三の場合には3.3の18平面被覆を使う。いずれの場合も長さ4以下であり、定理1から diam(G)≤4 である。

次数12、直径3の Moore 上界は 1+12+12·11+12·11^2=1597 <5832 だから、diam(G)≤3 は不可能である。したがって diam(G)=4。□

## 6. グラフ全体での独立検証

辺ファイル graph_12_4_5832.edges は、頂点を

\[
((9g+i)81)+(x_0+3x_1+9x_2+27x_3)
\]

で符号化した0-based edge list である。各無向辺は小さい端点を先にして一度だけ記載する。

全5,832始点の BFS を、route certificate と別の実装で実行した。C++17標準ライブラリのみの実装と Python/Numba の実装で、全距離分布が一致した。

|距離|ordered pairs|
|---:|---:|
|0|5,832|
|1|69,984|
|2|676,512|
|3|6,342,300|
|4|26,917,596|

合計は 34,012,224=5832^2。辺数は 34,992。C++検証器では頂点0と4の距離が4であることも確認した。

辺ファイルの SHA-256:

```
ea0846865021f05f38825ac03ca96a387815b50634a9117f9f42533080dbd05b
```

## 7. 前の探索に関する修正

「controller の girth が目標直径より大きければ、この種の affine lift は不可能」という一般論は正しくない。本構成の controller は girth 5 であるにもかかわらず、lift の直径は4である。各閉 route の rank が2以下でも、複数の二次元部分空間が F_3^4 を覆えることが理由である。

一方、Loz_1320 を用いた 1320×F_q^7 の候補は別の必要条件で排除できる。公開 SageMath スクリプトの sparse6 表現を復元した番号付けでは、頂点0から126への長さ7以下の controller walk は、長さ6のただ一本

```
0 -> 1 -> 1173 -> 1113 -> 127 -> 125 -> 126
```

だけである。その固定 route には q^6 個の制御列しかなく、q^7 点の target fiber は覆えない。この議論は行列選択によらず、1本の controller edge の各始点に q 個の隣接先を与えるより一般的な構成にも当てはまる。

Loz_1320 のデータ出典：
https://web.mat.upc.edu/francesc.comellas/delta-d/desc_g/adjacencies/adjD7/1320_loz_SageMath.txt

## 背景

Route-chart の考え方の比較対象は、R. Mizuno, "New lower bounds for the degree/diameter problem via interaction with a browser-accessible LLM", arXiv:2606.15860v1 である。
https://arxiv.org/html/2606.15860v1

本探索は、会話中で議論した8頂点 multibase を出発点として、voltage と F_3 の行列を再探索したもの。URSA 側の着想の出典・独立性・論文参照の有無についての推論は、本構成の証明に使用していない。
