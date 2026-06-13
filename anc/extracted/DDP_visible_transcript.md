# Degree Diameter Problem — browser-visible transcript

Only the messages that the chat.openai.com UI shows as a user prompt bubble or an assistant answer bubble are included.  Thoughts, tool calls, code execution output, and `reasoning_recap` annotations are dropped.  See `is_browser_visible_message` in this script for the exact rule.

- conversation_id: `6a101fde-f380-83a8-afc7-7a224426dbc9`
- created: 2026-05-22 09:20:31 UTC
- updated: 2026-05-27 14:15:33 UTC
- default_model: `gpt-5-5-pro`
- visible turns: 226 (user: 52, assistant: 174)
- rounds: 52 (one per user prompt; a round = a user prompt plus the assistant replies answering it)

---
## Turn 001 (Round 001) — 🧑 USER

_2026-05-22 09:20:30 UTC_

d<=16, k<=10のdegree diameter problemの新しい記録を出したいです。
- まず関連文献調査してください。
- [重要]文献の中に本質的に含まれていないアイデアで解の構成を試みてください。既存の方法を組み合わせる、パラメータを増やす、使う代数系を変えるだけ、既存の解に対して新しくない方法で局所探索する、等はNGです
- アイデアを考えること、およびアイデアを使い解の構成に取り組むフェイズにおいては、基本的にweb検索は行わないでください。
- d, kはどれに取り組んでも良いです。アイデアの内容に基づいて、アイデアが有効なk, dを選んでください

---

## Turn 002 (Round 001) — 🤖 ASSISTANT

_2026-05-22 09:20:47 UTC_  ·  model: `gpt-5-5-pro`

まず文献・既存記録表だけをWebで確認し、その後は検索を止めて、既存手法の延長ではない構成アイデアを手元の推論・計算で試します。対象の \(d,k\) は更新余地とアイデア適性を見て選びます。

---

## Turn 003 (Round 001) — 🤖 ASSISTANT

_2026-05-22 09:24:02 UTC_  ·  model: `gpt-5-5-pro`

文献調査では、2026年1月版のComellas/UPC・Mendeley系の表を基準にし、2025年のComellas論文で近年の更新と手法地図も確認します。小さく検証しやすい候補として \((6,4)=390\)、\((8,3)=253\) を意識します。

---

## Turn 004 (Round 001) — 🤖 ASSISTANT

_2026-05-22 09:51:18 UTC_  ·  model: `gpt-5-5-pro`

文献調査は終え、今は検索なしで構成案を試しています。現状では PGL(2,p) の非自由作用から作る Schreier グラフ案が有望で、\((12,5)\) で 29630 頂点を狙えますが、直径5の確認にはまだ届いていません。

---

## Turn 005 (Round 001) — 🤖 ASSISTANT

_2026-05-22 10:09:25 UTC_  ·  model: `gpt-5-5-pro`

## 調査結果：現行記録と主流手法

まず、対象は通常の**単純無向グラフ**の degree/diameter problem、つまり「最大次数 \(d\)、直径高々 \(k\) のグラフの最大頂点数 \(N(d,k)\)」として扱います。一般上界は Moore bound  
\[
M(d,k)=1+d+d(d-1)+\cdots+d(d-1)^{k-1}
\]
で、Moore graph が存在する例は非常に限られるため、実際の研究は「上界を下げる」方向と「構成で下界を上げる」方向に分かれます。citeturn638618view0turn258464view4

現行の基準表としては、Francesc Comellas が維持している “Table of Large Degree/Diameter Graphs” が一番実用的です。Mendeley Data 版は 2026年1月版として、次数 \(3\le \Delta\le16\)、直径 \(2\le D\le10\) の最大既知グラフ表・構成情報・小さいグラフの隣接リストを含みます。Web 表では 2026年4月更新の \((6,7)\) なども反映されています。citeturn258464view1turn636919view0

### 現行記録表、\(3\le d\le16,\ 2\le k\le10\)

| \(d\backslash k\) | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 3 | 10 | 20 | 38 | 70 | 132 | 196 | 360 | 600 | 1,250 |
| 4 | 15 | 41 | 98 | 364 | 740 | 1,320 | 3,243 | 7,575 | 17,703 |
| 5 | 24 | 72 | 212 | 648 | 2,772 | 5,516 | 17,030 | 57,840 | 187,056 |
| 6 | 32 | 111 | 390 | 1,404 | 7,917 | 20,319 | 76,891 | 331,387 | 1,253,615 |
| 7 | 50 | 168 | 672 | 2,756 | 12,264 | 53,020 | 249,660 | 1,223,050 | 6,007,230 |
| 8 | 57 | 253 | 1,100 | 5,115 | 39,672 | 131,137 | 734,820 | 4,243,100 | 24,897,161 |
| 9 | 74 | 585 | 1,640 | 8,268 | 75,893 | 279,616 | 1,697,688 | 12,123,288 | 65,866,350 |
| 10 | 91 | 650 | 2,331 | 13,203 | 134,690 | 583,083 | 4,293,452 | 27,997,191 | 201,038,922 |
| 11 | 104 | 715 | 3,200 | 19,620 | 156,864 | 1,001,268 | 7,442,328 | 72,933,102 | 600,380,000 |
| 12 | 133 | 786 | 4,680 | 29,621 | 359,772 | 1,999,500 | 15,924,326 | 158,158,875 | 1,506,252,500 |
| 13 | 162 | 856 | 6,560 | 40,488 | 531,440 | 3,322,080 | 29,927,790 | 249,155,760 | 3,077,200,700 |
| 14 | 183 | 916 | 8,200 | 58,095 | 816,294 | 6,200,460 | 55,913,932 | 600,123,780 | 7,041,746,081 |
| 15 | 187 | 1,215 | 11,712 | 77,520 | 1,417,248 | 8,599,986 | 90,001,236 | 1,171,998,164 | 10,012,349,898 |
| 16 | 200 | 1,600 | 14,640 | 132,496 | 1,771,560 | 14,882,658 | 140,559,416 | 2,025,125,476 | 12,951,451,931 |

この表の多くは最適値ではなく、「現時点で最大既知」です。特に \(k\ge7\) 側は Moore bound からかなり遠く、まだ構成改善の余地が見えます。とはいえ、単に Cayley graph の群を変えてランダム生成する、既存グラフに頂点を足してつなぎ替える、電圧グラフの群や商グラフを少し変える、という方向は文献の主戦場そのものです。citeturn636919view0

## 文献に現れる主要パターン

**Cayley graph / 半直積 / 群生成集合探索。**  
Comellas の最近のまとめでは、\(3\le d\le16, 2\le k\le10\) の最大既知グラフのおよそ半分が Cayley graph、特に巡回群の半直積からの構成や計算探索に由来すると説明されています。2024–2026 の新記録にも、\(\mathbb Z_m\rtimes \mathbb Z_n\) 型の Cayley graph が多数含まれます。citeturn638618view0turn636919view1

**Voltage graph / regular lift。**  
Loz–Širáň の 2008 年論文は、小さい商グラフに群値の voltage assignment を置き、それを regular cover として lift することで多数の記録を更新しました。Cayley graph は 1 頂点商グラフの regular lift と見なせるので、この枠組みは Cayley 探索を本質的に含みます。citeturn776403view0

**Compounding / graph products / replacement 的構成。**  
Quisquater 型の頂点置換、Gómez–Fiol–Serra 型の複数頂点置換、グラフ積などは、小直径・中次数の記録でかなり重要です。Comellas のまとめでも、compounding は特に小直径の大グラフ構成の基本道具とされています。citeturn638618view0turn636919view1

**対称グラフ由来の edge-pairing、既存グラフへの頂点追加。**  
近年の \((3,8)=360\) は Foster graph から、頂点集合 \(V(F)\) と辺集合 \(E(F)\) を合わせ、incident 関係と辺ペアリングで作る非 Cayley 構成です。また \((13,3)=856\) は既存の 851 頂点グラフに 5 頂点を追加して得られたものです。citeturn638618view0turn636919view1

ここまでを見ると、ユーザーさんの NG 条件に引っかからないようにするには、**regular lift/Cayley/半直積/compounding/既存解の局所改善**からかなり意識的に離れる必要があります。

## 新しい構成アイデア：非正則 permutation lift

文献の voltage graph は「各 fiber 上に同じ群が正則に作用する」regular cover です。ここではそこを外します。

基底グラフ \(B\) を取り、各頂点を \(m\) 個の fiber に置き換えます。各有向辺 \(e:u\to v\) に、群元ではなく任意の置換  
\[
\pi_e\in \mathrm{Sym}(m),\qquad \pi_{\bar e}=\pi_e^{-1}
\]
を割り当てます。新しいグラフ \(L(B,\pi)\) の頂点は
\[
V(L)=V(B)\times\{0,\dots,m-1\}
\]
で、辺は
\[
(u,i)\sim (v,\pi_e(i)).
\]
このとき最大次数は \(\Delta(B)\) のままです。

直径判定は、基底グラフ上の walk \(w=e_1\cdots e_t\) に対して  
\[
\Pi_w=\pi_{e_t}\circ\cdots\circ\pi_{e_1}
\]
を見ればよく、
\[
\operatorname{diam}(L)\le k
\]
であることは、任意の基底頂点 \(x,y\) と任意の fiber 添字 \(i,j\) について、長さ \(\le k\) の walk \(w:x\to y\) が存在して
\[
\Pi_w(i)=j
\]
となることと同値です。

これが文献の regular voltage lift と違う点は、fiber の動きが単一の群の右正則作用に縛られないことです。Cayley graph や通常の voltage graph はこの構成のごく特殊な場合ですが、こちらでは「基底 walk が fiber 全体をどれだけ覆うか」という被覆問題を直接最適化します。単に「使う代数系を変える」話ではなく、群演算そのものを捨てて、walk-image coverage を主対象にします。

## 狙うべき \((d,k)\)

一番筋が良い最初のターゲットは **\((d,k)=(7,7)\)** です。

現行記録は  
\[
R(7,7)=53,020.
\]
基底を \(K_8\) にすると次数は 7。fiber サイズを  
\[
m=\left\lfloor \frac{53020}{8}\right\rfloor+1=6628
\]
にすれば、lift の頂点数は
\[
8\cdot 6628=53,024,
\]
つまり **+4 頂点の新記録候補**になります。

次点で **\((6,8)\)** もかなり良いです。基底 \(K_7\)、次数 6、  
\[
m=\left\lfloor \frac{76891}{7}\right\rfloor+1=10985
\]
とすれば
\[
7\cdot10985=76,895,
\]
現行 \((6,8)=76,891\) を **+4** 更新できます。

小型プロトタイプとしては **\((5,5)\)** も使えます。基底 \(K_6\)、\(m=109\) で
\[
6\cdot109=654
\]
となり、現行 \((5,5)=648\) を超えます。ただしこちらは直径 5 がかなり窮屈で、ランダム permutation lift だけでは欠陥が多く、研究用のデバッグ対象という位置づけです。

## ここまでの構成実験

非正則 permutation lift のランダム初期値を試すと、大型ターゲットではかなり近いところまで来ます。

- \(K_8\) base, \(m=6628\), \((7,7)\) 候補、頂点数 53,024：ランダム lift で 50 始点をサンプリングしたところ、距離 7 以内に届かない頂点数は平均およそ 32、最大 44 でした。これは証明ではありませんが、欠陥が「全面崩壊」ではなく、局所修復できそうな規模です。
- \(K_7\) base, \(m=10986\), \((6,8)\) 近傍候補、頂点数 76,902：50 始点サンプルで、距離 8 以内に届かない頂点数は平均およそ 37、最大 51 でした。
- \(K_6\) base, \(m=109\), \((5,5)\) 候補、頂点数 654：完全検査ではランダム lift に 1 万以上の bad pair が残り、最初の本命にはしにくいです。

つまり、現時点では**証明済みの新記録はまだ出ていません**。ただし \((7,7)\) と \((6,8)\) は、ランダム初期値の欠陥が数十頂点/始点程度まで落ちており、次の「欠陥修復」フェーズに進む価値があります。

## 修復アルゴリズム案

bad pair を  
\[
((x,i),(y,j))
\]
とします。基底 \(K_{d+1}\) 上で \(x\) から \(y\) への長さ \(k\) の walk
\[
x=v_0,v_1,\dots,v_k=y
\]
を選びます。途中の辺 \(v_rv_{r+1}\) を 1 本選ぶ。

現在の置換で、始点 \((x,i)\) から \(v_r\) まで進んだ fiber を \(a\) とする。逆に、終点 \((y,j)\) から walk を逆向きにたどり、\(v_{r+1}\) にいなければならない fiber を \(b\) とする。

すると、その辺の置換を 1 回の swap で修正して
\[
\pi_{v_rv_{r+1}}(a)=b
\]
を強制できます。置換なので次数条件は壊れません。これで少なくともその bad pair には長さ \(k\) の道が作られます。もちろん他の pair が壊れる可能性があるので、全体の欠陥数が減る swap を採用し、増える swap は温度付きでまれに採用する、という repair search にします。

この修復は「既存の記録グラフを局所探索する」ものではなく、非正則 permutation lift の coverage 制約を満たすための制約修復です。文献の regular voltage/Cayley 探索とは目的関数も可動部分も違います。

## 次にやる順番

最短で記録を狙うなら、順番はこうです。

1. **\((7,7)\), \(K_8\), \(m=6628\), 53,024 頂点**  
   サイズが比較的小さく、現行記録との差が +4 なので、最初の本命。
2. **\((6,8)\), \(K_7\), \(m=10985\), 76,895 頂点**  
   欠陥のサンプル挙動は良いが、完全検査コストが少し上がる。
3. **\((8,7)\), \(K_9\), \(m=14571\), 131,139 頂点**  
   現行 \((8,7)=131,137\) を +2 だけ超える候補。計算は重いが、同じ設計で行ける。

現段階の結論としては、文献調査上「そのまま既存手法」と見なされにくく、かつ実験的に一番近いのは **complete-base non-regular permutation lift** です。最初に \((7,7)\) の 53,024 頂点候補を完全修復・完全検証するのが、いちばん勝ち筋があります。

---

## Turn 006 (Round 002) — 🧑 USER

_2026-05-22 12:02:59 UTC_

進めてください。

---

## Turn 007 (Round 002) — 🤖 ASSISTANT

_2026-05-22 12:03:26 UTC_  ·  model: `gpt-5-5-pro`

構成フェーズに入り、Web は使わず non-regular permutation lift を実装します。まず \((7,7)\) の 53,024 頂点候補を本命に、完全検証器と欠陥修復器を作ります。

---

## Turn 008 (Round 002) — 🤖 ASSISTANT

_2026-05-22 12:06:30 UTC_  ·  model: `gpt-5-5-pro`

軽量実験ではランダム候補だけでは未到達が残り、素朴な修復も効きにくいと分かりました。次は高速検証に移し、\(K_8\) 固定を外した基底や小さめの候補も並行してふるいにかけます。

---

## Turn 009 (Round 002) — 🤖 ASSISTANT

_2026-05-22 12:15:35 UTC_  ·  model: `gpt-5-5-pro`

本命を少し広げ、\((4,10)\) の \(K_5\)-lift 17,705 頂点や bouquet 型 17,704 頂点を C++ 修復対象にします。さらに小型の \((6,4)\) で 392 頂点以上も高速検証します。

---

## Turn 010 (Round 002) — 🤖 ASSISTANT

_2026-05-22 12:42:41 UTC_  ·  model: `gpt-5-5-pro`

BFS 検証のボトルネックを潰し、全始点検査は約 8 秒まで短縮できました。さらに別案として、Schreier graph で \((7,10)\) の 6,096,454 頂点候補が未到達 2 頂点まで来ています。

---

## Turn 011 (Round 002) — 🤖 ASSISTANT

_2026-05-22 12:49:07 UTC_  ·  model: `gpt-5-5-pro`

進めました。率直に言うと、**まだ検証済みの新記録は出ていません**。ただし、どの方向が弱いか・どこを強くすべきかはかなりはっきりしました。

成果物はこちらです。コード、途中候補、README をまとめています。

[degree_diameter_attempt_artifacts.zip](sandbox:/mnt/data/degree_diameter_attempt_artifacts.zip)

## 今回進めたこと

本命は前回の案どおり、

\[
K_8\text{ base},\quad m=6628,\quad d=7,\quad k=7,\quad |V|=8\cdot6628=53024
\]

です。現行の \((7,7)=53020\) を **+4** する候補です。

構成は、各 base edge に任意の permutation を置く non-regular permutation lift です。Cayley/regular voltage のように単一群の正則作用へ落とさず、bad pair を直接修復する方針にしました。

## 実験結果

| 実験 | 対象 | 結果 |
|---|---:|---|
| 完全基底 \(K_8\) ランダム lift | \((7,7)\), 53024 頂点 | 32 始点サンプルで初期 bad pair 1052。まだ直径 7 ではない |
| CEGAR 型 targeted repair | \((7,7)\), 53024 頂点 | 32 始点 pool の bad pair を 1052 → 779 まで減少。ただしゼロ未達 |
| 小型 full repair | \(K_4,m=50\), \((3,7)\), 200 頂点 | full bad pair を 5102 → 854 まで減少。ゼロ未達 |
| 任意 base random lift | \((5,7),(6,8),(7,8)\) など | larger base にしても sample defect は 20〜60 程度残る |
| random regular fallback | \((5,5),(6,5)\) など | 欠陥が桁で残る。主案としては不採用 |
| finite geometry pruning | \((16,2)\) | GF(16) polarity graph の induced subgraph 探索を試したが、直径 2 欠陥が大量に残る |

一番重要な観察は、**単なるランダム permutation lift は「あと少し」までは来るが、自然にはゼロにならない**という点です。特に \((7,7)\) はサンプル上では unreachable target が 1 始点あたり 30〜40 個程度に落ちますが、そこから単一 swap 修復だけでは収束が遅いです。

## いまの結論

今回の修復 move は弱すぎます。

bad pair  
\[
((x,i),(y,j))
\]
に対して、長さ \(k\) の base walk を 1 本選び、その walk 上の 1 edge の permutation を swap して

\[
\Pi_w(i)=j
\]

を強制する、という修復を実装しました。これは確かに bad pair を局所的には直せますが、他の到達性を壊す副作用が大きく、全体欠陥がゆっくりしか減りません。

特に \(K_8,m=6628\) の CEGAR 実験では、

\[
1052 \to 779
\]

までは落ちましたが、改善幅が 1〜数個ずつになり、現状の単発 swap では新記録に届く見込みが薄いです。

## 次に必要な改良

次は single-edge repair ではなく、**multi-walk / multi-edge coordinated repair** にするべきです。

具体的には、1 個の bad pair を直すのではなく、同じ始点から漏れている 20〜40 個の target をまとめて見て、複数の edge permutation に対して小さな assignment problem を解きます。

今の move は

\[
\pi_e(a)=b
\]

を 1 本だけ強制します。次は、同じ permutation 上で衝突しない複数制約

\[
\pi_e(a_1)=b_1,\quad \pi_e(a_2)=b_2,\quad \dots
\]

をまとめて入れる。これは単なる局所探索ではなく、lift の walk-coverage 制約を小さな matching/flow 問題として解く形です。この方向なら、既存文献の regular voltage/Cayley 探索からかなり離れたまま、現在の bottleneck に直接刺さります。

## 保存したもの

zip 内には以下が入っています。

- `complete_cegar.cpp`：\((7,7)\) 用の counterexample-guided repair
- `complete_repair.cpp`：小型 complete-base lift の targeted repair
- `general_lift.cpp`, `lift_from_base.cpp`：任意 base lift 実験
- `reg_local.cpp`：比較用 random regular 2-switch 探索
- `polarity_search.py`：\((16,2)\) の有限幾何 pruning 実験
- `cegar_best_perms.txt`, `cegar_best_edges.txt`：\((7,7)\) の途中最良候補
- `complete_repair_best_*`, `local_frombase_best_*`：小型/任意 base の途中最良候補
- `degree_diameter_attempt_README.txt`：実験メモ

現時点の最有望ターゲットは変わらず **\((7,7)\), 53024 頂点**です。ただし、次フェーズでは repair move を「1 bad pair = 1 swap」から「bad cluster = constrained multi-swap」に上げる必要があります。

---

## Turn 012 (Round 003) — 🧑 USER

_2026-05-22 13:45:25 UTC_

局所改善をしているように見えるのですが、文献で、現在最高記録のグラフの中で、局所改善で得られたものはあるのでしょうか？ないなら、数学的にも直感的に局所改善で良いグラフは得られる気はしないので、今の方針には懐疑的です。

---

## Turn 013 (Round 003) — 🤖 ASSISTANT

_2026-05-22 13:45:41 UTC_  ·  model: `gpt-5-5-pro`

ご指摘は正当なので、現行記録の由来を文献ベースで分解し、局所改善が実際に記録更新を生んでいる領域か確認して方針を見直します。

---

## Turn 014 (Round 003) — 🤖 ASSISTANT

_2026-05-22 13:48:50 UTC_  ·  model: `gpt-5-5-pro`

ざっと見ると、素の局所改善が主役の記録は少数で、巨大な表の主戦場ではありません。前回の修復方針への懐疑は正当です。

---

## Turn 015 (Round 003) — 🤖 ASSISTANT

_2026-05-22 13:53:24 UTC_  ·  model: `gpt-5-5-pro`

はい、あります。ただし、**かなり限定的**です。しかも成功しているものは「完全に無構造な既存グラフを局所改善して巨大記録を出す」という感じではなく、だいたい次のどちらかです。

1. **強い構造を仮定した小さな探索空間の中での heuristic / local search**
2. **既存の構成を数頂点だけ拡張して regularize する小改造**

なので、あなたの懐疑はかなり正しいです。少なくとも、私が前回やっていた **random lift を bad pair に対して swap repair する**方向は、「本質的に新しい構成」というより「大きな局所修復探索」に見えます。ここは方針を切り替えるべきです。

## 文献上の局所改善・heuristic 由来の現行記録例

一番はっきりしているのは **\((d,k)=(4,3)\), 41 頂点**です。Comellas の記録ページでは、この 41 頂点グラフは James Allwright が heuristic algorithm で見つけたものと明記されており、13 個の非同型グラフが得られたこと、さらにいくつかは 2-swap で互いに移ることも記載されています。これはかなり「局所探索・局所変形」寄りの現行記録です。citeturn647372view0L16-L31

次に Geoffrey Exoo の 2001 年の構成群があります。Exoo の論文は、当時の最大既知グラフとして \((3,7),(3,8),(4,4),(5,3),(5,5),(6,3),(6,4),(7,3),(14,3),(16,2)\) などを含む family を提示しています。論文本文では、Cayley graph がまれなので対称性条件を緩め、automorphism group のサイズの小整数倍の位数をもつグラフを探した、と説明しています。citeturn302778view2L72-L80 citeturn302778view2L93-L102  
ただしこれは無構造な全グラフ空間での探索ではありません。頂点を \(r\) 個の \(s\)-cycle orbit に分け、辺集合を permutation orbit の和として指定する、かなり強い orbit/circulant-block 構造を入れています。citeturn302778view1L145-L180 その上で、探索方法は simulated annealing と tabu search の合成に基づくと書かれています。citeturn302778view0L283-L292  
現在の表でも \((5,3)=72\), \((6,3)=111\), \((7,3)=168\) は Exoo 由来として載っています。citeturn647372view0L41-L63

もう一つ重要なのは **\((13,3)=856\)** です。これは Gómez の 851 頂点グラフ \(Q'_8d+\) から、Vlad Pelekhaty が数頂点を追加し、dangling degree を regularize して得たもの、と記録ページにあります。Comellas の 2025/2026 のまとめでも「5 頂点を加え、いくつかの頂点を再接続した」と説明されています。citeturn647372view0L120-L123 citeturn535967view2L65-L72  
これは「既存グラフの局所改善」と呼んでよいと思います。ただし直径 3 の特殊な高次数領域で、しかも +5 頂点の拡張です。大きな \(k\) の記録をこの路線で更新している主流例ではありません。

## ただし主流ではない

Comellas の最近のまとめでは、\(3\le d\le16,\ 2\le k\le10\) の largest-known graphs のおよそ半分は Cayley graph や Cayley-based voltage graph で、特に semidirect product of cyclic groups 由来のものが多いとされています。compounding も小直径で重要な基本手法です。citeturn535967view4L41-L50

また Loz–Širáň 型の voltage graph / lift は、小さい quotient graph を大きな graph に blow up する構造的構成で、次数を保ち、diameter を voltage graph の性質で制御する、という発想です。これは探索を使うとしても「構成原理」が先にあります。citeturn535967view6L60-L68

そして一般論としても、Pérez-Rosés の survey は basic local search について、初期解から近傍の改善解へ置き換えて local minimum まで進むものだと説明したうえで、basic local search だけで得られる解の質は通常かなり悪い、とかなり率直に述べています。citeturn359374view1L188-L200

## なので、前回方針への評価

あなたの指摘どおり、前回の

\[
\text{random non-regular permutation lift} \quad + \quad \text{bad pair repair by swaps}
\]

は危ないです。

non-regular permutation lift という発想自体は regular voltage graph から外れているので、入口としてはまだ面白いです。ただし、実際にやっていた構成フェーズが「bad pair を見つけて swap で直す」という局所修復になってしまっている。これは文献的にも、直感的にも、大きな新記録を出す主戦略としては弱いです。

特に \(d\le16,k\le10\) の現在表を見ると、局所探索が効いた例はありますが、勝っているパターンはだいたい

\[
\text{強い構造仮定} \rightarrow \text{小さい有限探索} \rightarrow \text{明確な diameter certificate}
\]

です。逆に、

\[
\text{巨大なランダム候補} \rightarrow \text{欠陥を局所的に潰す}
\]

は、良い degree-diameter graph の「球が重なりすぎず、しかも最後は全体を覆う」という global な性質と相性が悪いです。局所的に bad pair を直すと、別の場所の短路構造を壊す、という前回実験の挙動はまさにそれでした。

## 方針転換します

前回の repair search は止めるべきです。次に進むなら、条件をこう置きます。

**探索は使ってもよいが、局所改善を本体にしない。**  
つまり、構成は最初から数式・組合せ設計・有限構造として定義し、計算は「候補パラメータの列挙」または「直径証明の検証」だけに使う。

狙うべき方向は、たとえば次のようなものです。

\[
\text{小さい base 構造}
\quad+\quad
\text{global な被覆恒等式}
\quad+\quad
\text{diameter 証明が行列・設計・距離分布で閉じる構成}
\]

前回の permutation lift を続けるなら、局所 swap repair ではなく、最初から

\[
\{\Pi_w : w \text{ は長さ } \le k \text{ の base walk}\}
\]

が fiber 全体を覆うことを、置換族の global identity として設計する必要があります。そうでないなら、lift 方向も捨てた方がいいです。

結論としては、**局所改善由来の現行記録は存在するが、例外的・低次元的・強構造付きであり、今回の本命方針にする根拠にはならない**です。あなたの懐疑を採用して、次は「局所修復なしで直径を証明できる構成」に切り替えます。

---

## Turn 016 (Round 004) — 🧑 USER

_2026-05-22 13:58:11 UTC_

探索は使ってもよいが、局所改善を本体にしない。
つまり、構成は最初から数式・組合せ設計・有限構造として定義し、計算は「候補パラメータの列挙」または「直径証明の検証」だけに使う。
「局所修復なしで直径を証明できる構成」に切り替えます。

上記方針良いと思います。
アイデアは適当に選ぶのではなく、それを使うことで新記録となるような効率的なグラフが得られる根拠はあるのかを常に考えてください。根拠がないアイデアを用いての試行錯誤は時間の無駄です。

つづけてください

---

## Turn 017 (Round 004) — 🤖 ASSISTANT

_2026-05-22 13:58:36 UTC_  ·  model: `gpt-5-5-pro`

方針を切り替え、構成原理と効率の数値根拠を先に置く候補だけに絞ります。探索は候補列挙と直径検証に限定し、局所修復型は使いません。

---

## Turn 018 (Round 004) — 🤖 ASSISTANT

_2026-05-22 14:01:46 UTC_  ·  model: `gpt-5-5-pro`

有望な構造として、有限幾何の大域構造を使い、次数を1だけ落としても直径を保てるかを見る案に絞り始めています。

---

## Turn 019 (Round 004) — 🤖 ASSISTANT

_2026-05-22 14:10:54 UTC_  ·  model: `gpt-5-5-pro`

第一候補は \(K_8\) 基底の低次元有限体 affine Schreier cover で、\(p=6637\) なら 53096 頂点となり \((7,7)\) を 76 上回ります。直径条件は全ペア到達性を有限体上の被覆条件として一括検証します。

---

## Turn 020 (Round 004) — 🤖 ASSISTANT

_2026-05-22 14:38:10 UTC_  ·  model: `gpt-5-5-pro`

候補をさらにふるい、有限 building/flag graph や一部の有限幾何削除案は密度不足または直径破壊で棄却しました。別筋として、Kautz 型の半分保持構成も検査中で、成立すれば \((7,7)\) で 54,432 頂点になります。

---

## Turn 021 (Round 004) — 🤖 ASSISTANT

_2026-05-22 14:50:01 UTC_  ·  model: `gpt-5-5-pro`

進めました。今回は方針をかなり変えて、**局所修復ではなく「直径 6 の有限幾何を、全体設計された diametral shortcut で直径 5 に折る」**方向に集中しました。

成果物はこちらです。

[opposition_augmentation_artifacts.zip](sandbox:/mnt/data/opposition_augmentation_artifacts.zip)

## 結論

まだ新記録の検証済みグラフは出ていません。

ただし、前回の permutation lift よりかなり良い方向が見つかりました。特に本命は

\[
(d,k)=(16,5)
\]

です。

現在記録は前回表の

\[
N(16,5)\ge 132,496
\]

です。今回の構成候補は

\[
132,860
\]

頂点なので、直径 5 を証明できれば **+364 頂点の新記録**になります。

## 新しい構成アイデア：generalized hexagon + opposition shortcuts

使う基礎構造は split Cayley generalized hexagon \(H(q)\) です。

その incidence graph \(X_q\) は

\[
\Delta=q+1,\qquad \operatorname{diam}=6,
\]

かつ頂点数

\[
|V(X_q)|=2(q+1)(q^4+q^2+1)
\]

です。

ここで重要なのは、\(X_q\) はすでに直径 6 の非常に効率的なグラフで、直径 5 にするために潰すべき障害が明確なことです。incidence graph は二部グラフなので、距離 6 のペアは同じ側、つまり point-point または line-line の **opposite pair** です。point-line 間はもともと距離高々 5 です。

したがって、直径 5 化の自然な戦略はこうです。

\[
X_q
\quad+\quad
\text{point 側の opposite matching}
\quad+\quad
\text{line 側の opposite matching}
\]

を何本か足す。

これは「悪いペアを見つけて局所的に直す」ではなく、**直径 6 の有限幾何で唯一残る obstruction、すなわち opposition relation に対して、全体的な shortcut design を入れる**構成です。

## 最有望パラメータ：\(q=9\)

\(q=9\) では

\[
|V(X_9)|=2\cdot10(9^4+9^2+1)
=132,860.
\]

base degree は

\[
q+1=10.
\]

ここに point 側 6 本、line 側 6 本の perfect matching を足すと、最大次数は

\[
10+6=16.
\]

よって、もし直径 5 なら

\[
(d,k,n)=(16,5,132,860)
\]

となり、現行記録 132,496 を超えます。

この候補を GF(9) 上の split-octonion/Zorn model で実装しました。点は trace-zero split octonion の singular 1-space、線は \(xy=0\) を満たす 2-space として生成しています。

## 実験結果

| 構成 | 候補 | 頂点数 | 最大次数 | radius-5 sample 結果 |
|---|---:|---:|---:|---|
| \(H(9)\) + same-part random matchings 6 本 | \((16,5)\) | 132,860 | 16 | 典型的に 132,772 / 132,860 到達 |
| \(H(9)\) + opposition-only matchings 6 本 | \((16,5)\) | 132,860 | 16 | 典型的に 132,773 / 132,860 到達 |
| \(H(9)\) + same-part cycles 3 本 | \((16,5)\) | 132,860 | 16 | ほぼ同程度 |
| \(H(9)\) + circulant shortcuts | \((16,5)\) | 132,860 | 16 | random matchings より悪い |
| \(H(7)\) + 4 matchings | \((12,5)\) | 39,216 | 12 | 39,090 / 39,216 程度 |
| \(H(8)\) + cycles/mix shortcuts | \((13,5)\), \((14,5)\) | 74,898 | 13/14 | 74,795 / 74,898 程度 |
| \(H(11)\) + 4 matchings | \((16,5)\) | 354,312 | 16 | 339,420 / 354,312 程度 |
| \(H(13)\) + 2 matchings | \((16,5)\) | 804,468 | 16 | 644,700 / 804,468 程度 |

一番惜しいのは **\(H(9)+6\) matchings** です。256 始点サンプルでは、毎回だいたい 80〜120 頂点だけ radius 5 から漏れます。

ただし、これは「少数の悪い頂点を消せばよい」という状況ではありません。1,000 始点で defect union を見たところ、漏れ先の union は 63,608 頂点まで広がりました。したがって、132,860 から 363 頂点だけ削って 132,497 頂点以上の直径 5 グラフにする、という pruning 路線は見込みが薄いです。

## 重要な判断

この方向は、前回の random lift repair よりはるかに筋が良いです。

理由は、効率の根拠が明確だからです。

\[
H(9)
\]

はすでに

\[
132,860
\]

頂点を持ち、直径だけが 6 です。しかも、直径 5 を阻んでいるのは generalized hexagon の opposite pair だけです。次数には 6 だけ余裕があります。

つまり問題は、

> generalized hexagon \(H(9)\) の point 側・line 側に 6-regular shortcut graph を入れて、全 opposite pair を長さ 5 以内に落とせるか？

という明確な有限幾何の covering design 問題に変わりました。

一方、単純な random matching、opposition-only random matching、cycle、circulant では届きませんでした。ここから先で random/local に寄せるのはよくないです。

## 次にやるべき非局所ステップ

次は、6 本の matching をランダムに選ぶのではなく、\(H(9)\) の opposition geometry 上で **covering design** として構成するべきです。

具体的には、各 point \(x\) に対し、6 個の shortcut neighbor

\[
s_1(x),\dots,s_6(x)
\]

を持たせる。この 6 点が、\(x\) の opposite layer を半径 2 の collinearity ball たちで覆うように設計する。

ランダムでは 80〜120 個の穴が残るので、必要なのは局所修復ではなく、residue / opposition layer の中での **代数的 blocking set** または **解像可能な covering family** です。

今回の結論はこうです。

\[
\boxed{
H(9)+6\text{-regular opposition-covering shortcuts}
}
\]

が、現時点で最も根拠のある候補です。まだ完成していませんが、目標がかなり絞れました。前回のような「巨大候補を局所修復」ではなく、有限幾何上の明確な被覆設計問題になっています。

---

## Turn 022 (Round 005) — 🧑 USER

_2026-05-22 15:40:07 UTC_

つづけてください

---

## Turn 023 (Round 005) — 🤖 ASSISTANT

_2026-05-22 15:40:25 UTC_  ·  model: `gpt-5-5-pro`

続けます。今回は \(H(9)\) の opposition layer を被覆設計として定式化し、有限幾何の対称性で作った shortcut 候補だけを直径5検証に回します。

---

## Turn 024 (Round 005) — 🤖 ASSISTANT

_2026-05-22 15:43:34 UTC_  ·  model: `gpt-5-5-pro`

判定条件は、各点の opposite layer を shortcut 先の collinearity 半径2球で覆うことに絞れました。大域的自己同型軌道の案は漏れが約2万まで悪化したため、opposition graph の色分解へ移ります。

---

## Turn 025 (Round 005) — 🤖 ASSISTANT

_2026-05-22 15:52:45 UTC_  ·  model: `gpt-5-5-pro`

見方を一部変え、余裕の小さい \(H(9)\) だけでなく、\((14,5)\) に対して大きな頂点余裕を持つ \(H(8)\) も候補に入れます。

---

## Turn 026 (Round 005) — 🤖 ASSISTANT

_2026-05-22 16:19:55 UTC_  ·  model: `gpt-5-5-pro`

続けました。今回はかなり良い方向転換ができましたが、**まだ新記録の検証済みグラフは出ていません**。

成果物はこちらです。

[color_shortcut_phase_artifacts.zip](sandbox:/mnt/data/color_shortcut_phase_artifacts.zip)

## 新しい構成案：incidence edge-color shortcut

前回の \(H(9)\)+random shortcut matching は、最後がどうしても「穴を局所的につぶす」感じになっていました。今回はそこをやめて、shortcut を最初から有限設計として定義しました。

基礎は引き続き split Cayley generalized hexagon \(H(q)\) です。incidence graph は

\[
\Delta=q+1,\qquad \operatorname{diam}=6,
\]

で、頂点数は

\[
2(q+1)(q^4+q^2+1).
\]

直径 5 を阻むのは、同じ側、つまり point-point または line-line の opposite pair だけです。

ここで重要な幾何事実があります。点 \(y\) と、\(y\) を通る line \(L\) を固定すると、\(L\setminus\{y\}\) の \(q\) 個の点は、\(y\) と opposite な点全体を projection によって \(q\) 個の層に分割します。つまり opposite 点 \(x\) に対して、ある一意な点 \(p\in L\setminus\{y\}\) があり、

\[
\operatorname{dist}_{H(q)}(x,p)=4
\]

になります。したがって shortcut edge

\[
y\text{---}p
\]

を足せば、

\[
x \leadsto p \text{---} y
\]

で長さ 5 の道ができます。

この projection partition を使うのが今回の核です。

## 構成方法

まず、\(H(q)\) の incidence graph は \((q+1)\)-regular bipartite graph なので、Kőnig の定理により \((q+1)\) 個の perfect matching に edge-coloring できます。

各 incidence

\[
p\in L
\]

に色

\[
\chi(p,L)\in\{0,\dots,q\}
\]

を付け、各 point の周りにも各 line の周りにも全色が 1 回ずつ現れるようにします。

次に、小さい色グラフ \(F_P\) を選びます。例えば \(q=9\) なら色数 10。色ペア \(\{a,b\}\in F_P\) について、各 base line \(L\) 上で

\[
\chi(p,L)=a,\quad \chi(p',L)=b
\]

となる点 \(p,p'\) の間に point-point shortcut を足します。

line 側も双対的に、色グラフ \(F_L\) を選び、各 base point \(p\) の周りで該当色の line 同士に line-line shortcut を足します。

この構成の良い点は、次数が最初から厳密に制御されることです。色グラフの辺数を \(e\) とすると、各 point は point-shortcut をちょうど \(2e\) 本、各 line は line-shortcut をちょうど \(2e\) 本受け取ります。したがって最大次数は

\[
(q+1)+2e
\]

です。

これは random matching でも局所修復でもなく、

\[
\text{generalized hexagon}
+
\text{incidence 1-factorization}
+
\text{small color-pair design}
\]

という全体構造です。

## 本命 1：\((d,k)=(16,5)\), \(q=9,e=3\)

\[
q=9,\quad e=3
\]

なら、

\[
|V|=2\cdot10(9^4+9^2+1)=132,860,
\]

\[
\Delta=10+2\cdot3=16.
\]

したがって直径 5 なら、

\[
N(16,5)\ge132,860
\]

となり、現行記録

\[
132,496
\]

を **+364** 更新します。

実験では、まず arbitrary な 10-color 1-factorization を作り、色ペア 3 本からなる \(F_P=F_L\) を試しました。最初の 100 個程度の色ペア候補の中では、64 始点サンプルで最良到達数が

\[
132,468/132,860
\]

でした。かなり近いですが、直径 5 ではありません。

また \(F_P,F_L\) を別々にランダムに選ぶテストもしましたが、今回の arbitrary factorization では同程度かそれ以下でした。

## 本命 2：\((d,k)=(12,5)\), \(q=7,e=2\)

こちらは小さくて検証しやすいターゲットです。

\[
q=7,\quad e=2
\]

なら、

\[
|V|=2\cdot8(7^4+7^2+1)=39,216,
\]

\[
\Delta=8+2\cdot2=12.
\]

現行記録は

\[
N(12,5)\ge29,621
\]

なので、直径 5 が証明できれば **+9,595** の大更新です。

arbitrary な 8-color 1-factorization に対し、全 378 個の \(F_P=F_L\) 候補をサンプル評価しました。最良候補の一つは

\[
F=\{\{0,2\},\{1,3\}\}
\]

で、32 始点サンプルでは最小到達数

\[
38,868/39,216
\]

でした。

この候補について full scan を開始したところ、すぐに直径 5 ではないことは確認できました。例えば source 0 で 348 頂点が半径 5 から漏れます。途中までの full scan では、到達最小値は

\[
38,799/39,216
\]

まで下がり、最大 miss は 417 でした。

つまり \(q=7\) 版もかなり近いですが、現時点では失敗です。

## 重要な否定結果

「自然な局所パラメータで色を付ければよいのでは？」も試しました。

Zorn/octonion model では、各 point の nullspace から \(q+1\) 本の line が自然にパラメータ化されます。これを incidence color に使うと、各 point 周りでは確かに色がきれいに揃います。

しかし \(q=7\) で検査したところ、line 側では色が proper になりませんでした。line-color multiplicity failure が 129,100 個出ました。つまり、局所座標をそのまま貼るだけでは次数制御が壊れます。

ここはかなり大事です。必要なのは任意の 1-factorization ではなく、**projection map と整合する幾何的な 1-factorization** です。

## 今の判断

今回の方向は、前回よりかなり筋が良いです。

理由は、効率の根拠が明確だからです。

各 shortcut は、ただランダムに opposite pair を潰すのではなく、line projection による

\[
q^5 \text{ 個の opposite points}
=
q \text{ 個の } q^4\text{-slice}
\]

のうち、特定の色ペアに対応する slice をまとめて覆います。

さらに、incidence edge-coloring により追加次数が

\[
2|F|
\]

に厳密固定されます。したがって、次数違反を後から直す必要がありません。

ただし、arbitrary な 1-factorization ではダメです。ここまでの計算から見ると、現在のボトルネックは明確で、

\[
\boxed{
\text{generalized hexagon の projection と整合する 1-factorization を作れるか}
}
\]

です。

## 次にやるべきこと

次は random edge-coloring を回すのではなく、**Singer 型または torus 型の幾何的 1-factorization** を構成するべきです。

狙いはこうです。

点 \(y\) と opposite 点 \(x\) に対して、\(y\) 周りの \(q+1\) 本の line projection が色の permutation

\[
\pi_{x,y}:\{0,\dots,q\}\to\{0,\dots,q\}
\]

を誘導すると見ます。必要なのは、固定された小さい色ペア集合 \(F\) が、すべての relevant な \(\pi_{x,y}\) のグラフを打つことです。

\[
F\cap \{ \{t,\pi_{x,y}(t)\}:t\in\mathbb P^1(\mathbb F_q)\}\neq\emptyset.
\]

arbitrary factorization では \(\pi_{x,y}\) がランダムすぎて失敗します。逆に、Singer orbit や split torus から来る factorization で \(\pi_{x,y}\) が Möbius/affine 型の小さい族に落ちれば、少数の色ペアで全 opposite pair を打てる可能性があります。

現時点の結論は：

\[
\boxed{
H(q)
+
\text{geometric incidence 1-factorization}
+
\text{small blocking color-pair graph}
}
\]

が次の本命です。

まだ新記録は未達ですが、前回の「局所修復」からは完全に離れて、失敗条件がかなり明確な有限幾何の設計問題になりました。

---

## Turn 027 (Round 006) — 🧑 USER

_2026-05-23 00:15:53 UTC_

つづきお願いします

---

## Turn 028 (Round 006) — 🤖 ASSISTANT

_2026-05-23 00:16:40 UTC_  ·  model: `gpt-5-5-pro`

了解です。今回は web に戻らず、色付き incidence shortcut 路線を継続し、幾何的 1-factorization と小さな blocking color graph が本当に効くかを構造的に検証します。

---

## Turn 029 (Round 006) — 🤖 ASSISTANT

_2026-05-23 00:19:49 UTC_  ·  model: `gpt-5-5-pro`

任意の色付けではなく、各 opposite pair の projection が固定色ペア集合に当たるかを permutation/hitting 条件として測り、成立しなければこの路線を捨てます。

---

## Turn 030 (Round 006) — 🤖 ASSISTANT

_2026-05-23 00:28:59 UTC_  ·  model: `gpt-5-5-pro`

GQで直径4→3を狙う案は被覆下界が厳しく、構造的に見込み薄として退けます。代わりに \(q=8\) hexagon の \((13,5)\)・74,898頂点候補を本命に加え、\(G_2\) torus由来の代数的shortcutへ絞ります。

---

## Turn 031 (Round 006) — 🤖 ASSISTANT

_2026-05-23 01:00:10 UTC_  ·  model: `gpt-5-5-pro`

続けました。今回は **web検索なし**で、前回の方針どおり「局所修復ではなく、最初から有限幾何・設計として定義できる構成」だけを進めました。

成果物はこちらです。

[phase4_nonlocal_finite_geometry_artifacts.zip](sandbox:/mnt/data/phase4_nonlocal_finite_geometry_artifacts.zip)

## 結論

今回も、**検証済みの新記録はまだ出ていません**。

ただし、かなり重要な進展があります。前回の

\[
H(q)+\text{incidence edge-color shortcut}
\]

路線について、**なぜ固定された少数の color-pair では厳しいのか**がかなり明確になりました。これにより、前回案をそのまま押すのはやめるべきだと判断できます。

一方で、新しく試した

\[
\text{point graph of }H(q)\text{ の次数制御 thinning}
\]

と

\[
PG(2,16)\text{ polarity graph の deletion/blocking design}
\]

は、どちらも根拠のある方向でしたが、今回の実験範囲では記録更新には届きませんでした。

## 1. 前回の color-pair shortcut 路線の障害

前回の構成は、generalized hexagon \(H(q)\) の incidence graph に対して、incidence edge-coloring を作り、色ペア集合 \(F\) に従って same-side shortcut を入れるものでした。

この構成が本当に強くなるには、点 \(y\) と opposite 点 \(x\) の projection が、色集合

\[
\mathbb P^1(\mathbb F_q)
\]

上の小さい permutation family に落ちる必要があります。そこで必要条件として、もし projection permutation family が \(PGL(2,q)\) の derangement 程度に大きいなら、小さい \(F\) で全てを打てるかを調べました。

結果は否定的です。

- \(q=7\)：\(PGL(2,7)\) の derangement 全体を打つ color-pair set は、サイズ \(4\) 以下では存在しません。ところが \((12,5)\) 候補では \(|F|=2\) が必要でした。
- \(q=9\)：\(PGL(2,9)\) の derangement 全体を打つ color-pair set は、サイズ \(4\) 以下では存在しません。ところが \((16,5)\) 候補では \(|F|=3\) が必要でした。

つまり、前回の

\[
H(9)+3\text{ color-pairs}
\]

で \((16,5)\) を狙うには、projection permutations が \(PGL(2,9)\) よりはるかに小さい特殊族に落ちることを証明しなければいけません。任意の 1-factorization や普通の幾何的 coloring では足りない、ということです。

さらに、\(H(7)\) で \(SL(3,7)\) の位数 8 の torus action を使って幾何的 cyclic factorization を作る案も試しました。点・線の大半は長さ 8 の orbit に乗りますが、incidence edge に長さ 4 の短い orbit が残りました。

\[
\text{incidence-edge orbit distribution}
=
8:19584,\quad 4:48.
\]

この短い orbit のため、「1つの perfect matching を cyclic に回して 8 色を作る」という綺麗な factorization はそのままでは成立しません。

ここまでで、前回路線はかなり厳しいと見ています。

## 2. 新案：generalized hexagon の point graph を thinning する

次に、incidence graph ではなく、split Cayley generalized hexagon \(H(q)\) の **point graph** を使いました。

\(H(q)\) の point graph は、

\[
|V|=(q+1)(q^4+q^2+1),\qquad
\Delta=q(q+1),\qquad
\operatorname{diam}=3
\]

です。これは直径 3 の非常に効率的な有限幾何グラフです。そこで、各 line 上の clique を全て使うのではなく、line clique を全体設計として thinning して次数を下げ、直径 3 を保つことを狙いました。

### \(H(5)\) point graph

\[
q=5
\]

では、

\[
|V|=6(5^4+5^2+1)=3906,\qquad
\Delta=30.
\]

\((16,3)\) の Moore bound は

\[
1+16+16\cdot15+16\cdot15^2=3857
\]

なので、3906 頂点のままでは不可能です。ただし、50 頂点程度を落として 16 次数・直径 3 が作れれば、現行記録 1600 を大きく超えます。

そこで incidence coloring を使い、各 line 上で color-pair graph \(F\) に従って辺を残す構成を試しました。色数は 6、\(|F|=8\) とすると各点の次数は

\[
2|F|=16
\]

に厳密制御されます。

しかし、最良サンプルでも radius 3 到達数はおよそ

\[
2536/3906
\]

程度で、bad pair が非常に密でした。削除で 1600 超の直径 3 induced subgraph を得る見込みも薄いです。

### \(H(4)\) point graph

次に \(q=4\) も構築しました。こちらは GF(4) 上の Zorn/split-octonion model で生成しています。

\[
|V|=5(4^4+4^2+1)=1365,\qquad
\Delta=20.
\]

これは \((14,3)\) や \((12,3)\) に対してサイズ感が良いです。

色ペア thinning の結果は次の通りです。

| 対象 | 残す color-pair 数 | 次数 | 頂点数 | 最良の full min radius-3 reach |
|---|---:|---:|---:|---:|
| \(H(4)\) point graph | 6 | 12 | 1365 | 984 / 1365 |
| \(H(4)\) point graph | 7 | 14 | 1365 | 1203 / 1365 |

もし diameter 3 なら、

\[
(12,3): 1365 > 786
\]

または

\[
(14,3): 1365 > 916
\]

で大更新でしたが、届きませんでした。

さらに、固定 color-pair graph ではなく、各 line ごとに異なる局所グラフを使う方式も試しました。各 color の局所次数列を固定すれば、各点は各色を1回ずつ見るので、全体次数は厳密に制御できます。

例えば \(d=14\) では、line 上の 5 色に対して局所次数列

\[
(3,3,3,3,2)
\]

を持つグラフを各 line にランダムに割り当てました。この場合も典型的な最小 radius-3 reach は

\[
1170\text{〜}1180/1365
\]

程度で、diameter 3 には届きませんでした。

この point graph thinning は、アイデアとしては筋が良かったですが、今回の構成族では bad pair が密すぎます。

## 3. 別方向：\(PG(2,16)\) polarity graph で \((16,2)\) を狙う

最後に、直径 2 の near-Moore 構成も調べました。

\(PG(2,16)\) の orthogonal polarity graph は 273 頂点を持ちます。次数分布は、

- absolute point 17 個：次数 16
- non-absolute point 256 個：次数 17

です。

\((16,2)\) の Moore bound は

\[
1+16+16\cdot15=257.
\]

したがって、次数 17 の頂点をうまく 16 以下に落としつつ、直径 2 を保てれば、現行記録

\[
(16,2)=200
\]

を超える可能性があります。

最初の自然案は、17 個の absolute point を削除することです。すると 256 頂点が残りますが、1 個の nucleus が孤立します。さらに nucleus も削除すると、

\[
255
\]

頂点の 16-regular graph が得られます。

これは一見かなり良いのですが、diameter 2 ではありません。しかも障害は非常に構造的でした。bad graph は

\[
17\text{ 個の }K_{15}
\]

に分解します。つまり、この自然削除では、各 \(K_{15}\) から高々 1 点しか同時に残せず、diameter 2 induced subset としては全く使えません。

より一般に、「削除集合 \(D\) を選んで、残りが最大次数 16・直径 2 になる」問題を 0-1 MILP として定式化しました。

条件は：

1. 各 non-absolute vertex は、自分が残るなら少なくとも1つ隣接点を削除される。
2. 削除された頂点 \(w\) が、非隣接ペア \(\{u,v\}\) の一意共通近傍なら、\(u,v\) の少なくとも一方も削除する。

削除数 \(|D|\le72\) の feasible solution があれば、

\[
273-72=201
\]

で現行 \((16,2)=200\) を超えます。

この MILP は今回の実行時間内では解けませんでした。line を初期削除集合にする greedy も試しましたが、直径 2 条件の違反が増えていく挙動で、記録更新には届きませんでした。

ただ、この \((16,2)\) polarity deletion は、今回の中では一番「小さく、明確で、完全に有限な」未解決サブ問題です。

## 現時点の判断

前回の \(H(9)+color\ shortcut\) は、かなり懐疑的になりました。理由は単なる実験失敗ではなく、

\[
PGL(2,q)\text{ derangement hitting}
\]

の必要条件で、小さい color-pair set が明確に足りないからです。

今回試した中で、数学的に一番シャープに残っているのは

\[
PG(2,16)\text{ polarity graph の削除設計}
\]

です。これは \((16,2)\) に限られますが、問題サイズが小さく、制約も明確で、成功すれば

\[
200 \to 201\text{以上}
\]

の新記録になります。

一方、\(H(4),H(5)\) point graph thinning は、サイズ効率の根拠はありましたが、bad pair が密で、今回の thinning family では見込み薄です。これ以上続けるなら、単なるランダム thinning ではなく、distance-3 obstruction を直接支配する association scheme 上の設計に落とす必要があります。

---

## Turn 032 (Round 007) — 🧑 USER

_2026-05-23 08:44:56 UTC_

一度立ち止まって、この問題に対して、数学的に筋の良さそうな新アイデアを考えることに集中してみてください。

---

## Turn 033 (Round 007) — 🤖 ASSISTANT

_2026-05-23 08:45:22 UTC_  ·  model: `gpt-5-5-pro`

いったん実験と検索を止め、候補を「なぜ記録級効率が出るはずか」で厳しく棚卸しします。有限幾何ショートカット案も含め、根拠のない試行は捨てます。

---

## Turn 034 (Round 007) — 🤖 ASSISTANT

_2026-05-23 08:48:31 UTC_  ·  model: `gpt-5-5-pro`

近い候補の修理ではなく、最初から大きさと小直径を説明できる構成原理だけに絞って考え直します。

---

## Turn 035 (Round 007) — 🤖 ASSISTANT

_2026-05-23 09:03:42 UTC_  ·  model: `gpt-5-5-pro`

一度立ち止まって考え直すと、前回までの方向で一番まずかったのは、**「直径 6 の巨大な良い構造に、少数の追加辺を足して直径 5 にする」**という見方でした。これは一見よさそうですが、有限幾何の層サイズを見ると、追加次数が足りません。

たとえば generalized hexagon \(H(q)\) で、固定点 \(x\) から距離 6 にある点はおよそ \(q^5\) 個あります。1 本の same-side shortcut が距離 4 以内へ引き寄せられる相手はせいぜい \(q^4\) 規模なので、直径を 1 だけ縮めるにも、直感的には \(q\) 本程度の追加次数が必要です。前回の \(H(9)\) では追加次数が 6 しかなく、\(q=9\) に対して不足していました。ランダムで 80〜120 個漏れるのは偶然ではなく、構造的な不足だったと思います。

なので、発想を変えます。

## 本命アイデア：generalized hexagon の「完全マッチング縮約」

これはかなり筋が良いです。

split Cayley generalized hexagon \(H(q)\) の incidence graph を \(X_q\) とします。点集合を \(P\)、線集合を \(L\) とすると、

\[
|P|=|L|=(q+1)(q^4+q^2+1),
\]

\[
\Delta(X_q)=q+1,\qquad \operatorname{diam}(X_q)=6.
\]

ここで、incidence graph \(X_q\) の **完全マッチング**

\[
M\subseteq E(X_q)
\]

を 1 つ選びます。つまり、各点も各線も、ちょうど 1 本の matching edge に含まれるようにします。

そして、\(M\) の各 edge を 1 頂点に縮約します。得られるグラフを \(Y_M\) とします。

matching edge を

\[
e=(p,L),\qquad p\in L
\]

と書くと、縮約後の頂点 \(e\) は、

- 線 \(L\) 上の他の \(q\) 個の点に対応する matching edge
- 点 \(p\) を通る他の \(q\) 本の線に対応する matching edge

と隣接します。

generalized hexagon の incidence graph には 4-cycle がないので、この 2 種類の近傍は重なりません。したがって

\[
Y_M\text{ は }2q\text{-regular}
\]

です。頂点数は

\[
|V(Y_M)|=|P|=(q+1)(q^4+q^2+1).
\]

ここで、もし

\[
\operatorname{diam}(Y_M)\le4
\]

となる matching \(M\) を作れれば、かなり強い新記録になります。

## なぜ効率が良いか

この構成は、追加辺で直径を無理やり縮めるのではなく、**incidence graph の point 側と line 側を 1 対 1 に折り畳む**構成です。

もとの \(X_q\) は次数 \(q+1\)、直径 6、頂点数およそ \(2q^5\) です。縮約後は、

\[
d=2q,\qquad k=4,\qquad n\sim q^5.
\]

つまり

\[
n\sim \frac{d^5}{32}
\]

という、直径 4 にしてはかなり大きい候補になります。もちろん Moore bound は \(d^4\) オーダーなので、これは \(q\) が大きいと不可能になりますが、今回の範囲 \(d\le16\) では \(q\le8\) なのでまだ Moore bound 内に収まります。

ここが非常においしいです。\(q=8\) がちょうど

\[
d=16
\]

に対応します。

## 記録更新候補

| \(q\) | 構成次数 \(d=2q\) | 頂点数 \((q+1)(q^4+q^2+1)\) | 現行記録 \(N(d,4)\) | 更新幅 |
|---:|---:|---:|---:|---:|
| 4 | 8 | 1,365 | 1,100 | +265 |
| 5 | 10 | 3,906 | 2,331 | +1,575 |
| 7 | 14 | 19,608 | 8,200 | +11,408 |
| 8 | 16 | 37,449 | 14,640 | +22,809 |

特に本命は

\[
\boxed{q=8,\quad d=16,\quad k=4,\quad n=37,449}
\]

です。これは現行の

\[
N(16,4)\ge14,640
\]

を大きく超えます。

ただし最初に試すべきは \(q=4\) または \(q=5\) です。構成原理が正しければ、小さい \(q\) で先に直径 4 が出る可能性が高いです。\(q=5\) でも

\[
N(10,4)\ge3,906
\]

となり、現行 2,331 を大幅に超えます。

## 直径 4 を保証するための数学的条件

matching \(M\) は、generalized hexagon の chamber、つまり incident pair \((p,L)\) を 1 つずつ選ぶ集合と見なせます。

縮約後の距離は、もとの incidence graph で「matching edge を長さ 0 とみなす距離」です。したがって、直径 4 を示すには、

> 任意の 2 つの selected chambers が、matching edge の縮約後に 4 step 以内でつながる

ことを示せばよいです。

強い十分条件としては：

\[
\textbf{selected chambers のうち、互いに opposite なペアが存在しない}
\]

です。

generalized hexagon では、2 つの chamber が opposite でなければ、少なくとも片方の endpoint 同士が incidence graph 距離 4 以下になります。すると縮約後も距離 4 以下です。

つまり、最初の明確な有限設計問題は：

\[
\boxed{
\text{chamber opposition graph における independent perfect matching を作る}
}
\]

です。

より具体的には、変数を

\[
x_{p,L}\in\{0,1\}\qquad (p\in L)
\]

として、

\[
\sum_{L\ni p}x_{p,L}=1\quad\text{for every point }p,
\]

\[
\sum_{p\in L}x_{p,L}=1\quad\text{for every line }L,
\]

さらに opposite な chamber pair \((p,L),(p',L')\) について

\[
x_{p,L}+x_{p',L'}\le1
\]

を課す。

これが feasible なら、その matching を縮約するだけで直径 4 の証明が出ます。これは局所探索ではなく、**building の opposition relation に対する完全な transversal 設計問題**です。

この条件は十分条件なので、もし infeasible でも即終了ではありません。その場合は、opposite chamber pair が存在しても、間に別の matched chamber を 1〜2 個挟んで 4 step 以内に落ちる可能性があります。ただし、最初に狙うべきはこの強い条件です。証明がきれいで、構成の新規性もはっきりします。

## なぜこれは前回方針より筋が良いか

前回の shortcut 追加は、

\[
H(q)\text{ の obstruction を少数の辺で後から潰す}
\]

でした。これは \(q\) 本級の追加次数が必要そうなのに、\(q=9\) で 6 本しか使えない、という根本的な無理がありました。

今回の matching 縮約は違います。

各 matched chamber \((p,L)\) は、縮約後に

\[
q+q=2q
\]

個の自然な隣接先を持ちます。つまり、もとの incidence structure の point 側近傍と line 側近傍を両方とも使う。これは degree budget の使い方として非常に効率的です。

特に \(q=8\) では

\[
2q=16
\]

で、次数上限をちょうど使い切ります。これは偶然ではなく、\(d\le16\) の範囲で generalized hexagon folding が最も噛み合う理由です。

## これは既存手法とどう違うか

これは cover/lift ではなく、むしろ逆向きの **quotient/folding** です。

既存の voltage graph や Cayley graph は、小さい構造を大きく持ち上げる方向です。ここでは、大きな有限幾何 \(H(q)\) を、完全マッチングによって半分に折り畳む。しかも、単なる quotient ではなく、

\[
\text{one chamber per point and per line}
\]

という chamber transversal を使い、opposition relation を避けるように設計する。

これは少なくとも、前回までの「辺追加」「局所修復」「Cayley 生成集合探索」とはかなり違う構成原理です。

## さらに緩い変種：非 incident point-line folding

incident matching が難しい場合の第 2 候補もあります。

\(P\) と \(L\) の任意の bijection

\[
\phi:P\to L
\]

を取り、点 \(p\) と線 \(\phi(p)\) を同一視します。このとき次数は最大

\[
2(q+1)
\]

です。

\(q=7\) なら

\[
d=16,\qquad n=(8)(7^4+7^2+1)=19,608.
\]

もし直径 4 なら、

\[
N(16,4)\ge19,608
\]

となり、現行 14,640 を超えます。

incident matching 縮約ほど美しくはありませんが、\(\phi(p)\) を \(p\) から遠い線、たとえば距離 3 または 5 の線に選ぶことで、opposition を直接折る設計ができます。これは \(q=8\) では次数 18 になってしまうので使えませんが、\(q=7,d=16\) では十分候補になります。

## 今後の優先順位

今の私の判断では、次にやるべき順番はこうです。

### 1. \(H(4)\) incident matching contraction

\[
d=8,\quad k=4,\quad n=1,365.
\]

現行記録は 1,100。サイズが小さいので、chamber-opposition independent matching の feasible/infeasible をかなり早く判定できます。ここで成功すれば、構成原理の強い証拠になります。

### 2. \(H(5)\) incident matching contraction

\[
d=10,\quad k=4,\quad n=3,906.
\]

現行記録 2,331 を大きく超えます。\(q=5\) で成功するなら、論文級にかなり見栄えがします。

### 3. \(H(8)\) incident matching contraction

\[
d=16,\quad k=4,\quad n=37,449.
\]

本命です。成功すれば、\((16,4)\) を 14,640 から 37,449 に上げる大更新です。

### 4. incident matching が難しい場合、\(H(7)\) nonincident folding

\[
d=16,\quad k=4,\quad n=19,608.
\]

incident matching の完全条件が失敗しても、こちらは別の自由度があります。

## 捨てるべき候補

いまは、次の方向は本命にしない方がいいと思います。

**有限体上の additive/secant bi-Cayley graph** は、式としてはかなり魅力があります。たとえば \(A\subset \mathbb F_q^r\) を選んで、差集合和 \(s(A-A)\) が全空間を覆うようにする構成です。ただ、これは本質的に Cayley/difference-basis 型で、ユーザーさんの条件に照らすと「既存 Cayley 探索の変種」に見えやすいです。数学的には筋があっても、今回の主戦略にはしない方がよさそうです。

**generalized hexagon に少数 shortcut を足す案**も捨てます。層サイズから見て追加次数不足です。

**point graph thinning** も、bad pair が密すぎました。association scheme 上の完全な設計に落ちない限り、ランダム thinning は時間の無駄になりやすいです。

## 現時点の結論

次の本命アイデアはこれです。

\[
\boxed{
\text{split Cayley generalized hexagon }H(q)
\text{ の incidence graph を、chamber perfect matching で縮約する}
}
\]

狙いはまず

\[
\boxed{
H(5)\Rightarrow (d,k,n)=(10,4,3906)
}
\]

または

\[
\boxed{
H(8)\Rightarrow (d,k,n)=(16,4,37449)
}
\]

です。

この方向は、効率の根拠が明確です。次数 \(2q\)、直径目標 4、頂点数 \(\sim q^5\)。\(q=8\) で Moore bound の約 65% に達し、現行記録を大きく超えます。失敗条件も明確で、chamber opposition graph の independent perfect matching、あるいはその緩和としての diameter-4 folding matching を作れるか、という有限設計問題になります。

---

## Turn 036 (Round 008) — 🧑 USER

_2026-05-23 09:04:31 UTC_

そのアイデアで進めてください。

---

## Turn 037 (Round 008) — 🤖 ASSISTANT

_2026-05-23 09:05:01 UTC_  ·  model: `gpt-5-5-pro`

この方向に絞り、まず \(H(4)\)・\(H(5)\) で matching 縮約グラフを構成して直径 4 を完全検証します。候補 matching は局所修復ではなく、構造的・制約的に作って評価します。

---

## Turn 038 (Round 008) — 🤖 ASSISTANT

_2026-05-23 09:08:11 UTC_  ·  model: `gpt-5-5-pro`

既存の incidence edge-coloring 由来の matching では、\(q=4,5\) とも正則性は保てる一方で直径は 5 に留まりました。漏れは主に選択 chamber 同士の opposition に対応しており、次は opposition を避ける matching の制約問題として調べます。

---

## Turn 039 (Round 008) — 🤖 ASSISTANT

_2026-05-23 09:17:24 UTC_  ·  model: `gpt-5-5-pro`

重要な拡張として、matching 縮約を「各 line clique を星に置き換える」特殊例と捉え直しました。同じ \(q\)-edge tree を各 line に敷けば、次数 \(2q\) のまま設計自由度を増やせます。

---

## Turn 040 (Round 008) — 🤖 ASSISTANT

_2026-05-23 09:33:37 UTC_  ·  model: `gpt-5-5-pro`

進めました。今回は **web検索なし**で、matching 縮約アイデアを実装・検証しつつ、数学的により強い形へ拡張しました。

成果物はこちらです。

[phase5_contraction_artifacts.zip](sandbox:/mnt/data/phase5_contraction_artifacts.zip)

## 結論

まだ検証済みの新記録は出ていません。

ただし、かなり重要な整理ができました。最初の

\[
H(q)\text{ incidence graph の incident perfect matching contraction}
\]

は、別の見方をすると、

\[
H(q)\text{ の point graph で、各 line clique }K_{q+1}\text{ を star }K_{1,q}\text{ に置き換える}
\]

という構成でした。

つまり、各 hexagon line 上で 1 点を center に選び、その center と他の \(q\) 点だけを結ぶ。さらに各点がちょうど 1 回 center になるように選ぶ。すると各点の次数は

\[
q + q = 2q
\]

になります。

この読み替えは有用でしたが、実験結果から見ると、**star-thinning はたぶん硬すぎます**。特に \(q=7,8\) では radius 4 から漏れる点がかなり多く、直径 4 に届く気配が薄いです。

## incident matching contraction の検証結果

狙いは

\[
n=(q+1)(q^4+q^2+1),\qquad d=2q,\qquad k=4
\]

です。成功すれば、たとえば

\[
q=8 \Rightarrow (d,k,n)=(16,4,37449)
\]

で、前回調査時点の \((16,4)=14640\) を大きく超える候補でした。

実験結果は以下です。

| \(q\) | 候補 | 結果 |
|---:|---:|---|
| 3 | \(d=6,n=364\) | すべての color-class matching で直径 5。記録対象としては小さい |
| 4 | \(d=8,n=1365\) | 500 個の random perfect matching を検査。最良でも radius 4 worst miss = 37 |
| 5 | \(d=10,n=3906\) | random/color-class matching で worst miss 約 196〜213 |
| 7 | \(d=14,n=19608\) | random matching の full scan で worst miss 約 2166 |
| 8 | \(d=16,n=37449\) | GF(8) 上の \(H(8)\) を構築。最初の random matching で worst miss 5397 |

特に \(q=8\) は、本命だった

\[
(16,4,37449)
\]

候補ですが、任意の incident matching ではかなり遠いです。もちろん「全 matching で不可能」を証明したわけではありません。ただ、star-thinning 型の matching 縮約だけを本命として押す根拠は弱くなりました。

## 拡張 1：line clique を star ではなく fixed tree に置き換える

次に、star を一般の tree に拡張しました。

incidence edge-coloring

\[
\chi(p,L)\in\{0,\dots,q\}
\]

を取り、各点の周りにも各線の周りにも全色が 1 回ずつ出るようにします。

小さい色集合上の tree

\[
T\subseteq K_{q+1},\qquad |E(T)|=q
\]

を固定する。そして各 hexagon line \(L\) 上で、色 \(a,b\) が \(T\) で隣接しているなら、その 2 点を point graph 側で結びます。

このとき各点の次数は厳密に

\[
\sum_{c=0}^q \deg_T(c)=2q
\]

になります。matching contraction は \(T\) が star の場合です。

これは局所修復ではなく、

\[
\text{generalized hexagon}
+
\text{incidence 1-factorization}
+
\text{small tree design}
\]

という有限設計です。

### 結果

既存の edge-coloring に対して、全 labeled tree を列挙しました。

| \(q\) | tree 数 | 候補 | 結果 |
|---:|---:|---|---|
| 4 | \(5^3=125\) | \(d=8,n=1365\) | 最良は star。worst miss 38。直径 4 なし |
| 5 | \(6^4=1296\) | \(d=10,n=3906\) | 最良はほぼ star。worst miss 200。直径 4 なし |

さらに \(q=4\) では random edge-coloring と tree の組み合わせも少し試しましたが、最良 worst miss は 37 で、直径 4 には届きませんでした。

ここから見ると、**「全 line に \(q\) 本だけ辺を置く」方式自体が弱い**可能性があります。star か tree かの違いではなく、各 line 上の局所構造を木にすることが直径 4 には不利そうです。

## pruning も見込み薄

\(q=4\) の候補は

\[
d=8,\quad n=1365
\]

なので、直径 4 の induced subgraph を

\[
1101
\]

頂点以上残せれば、前回表の \((8,4)=1100\) を超えます。つまり 264 頂点まで削ってよい。

そこで bad-pair graph を作りました。元の候補グラフで距離 5 以上の点対を bad edge とし、この bad graph の independent set を残せば、残りは直径 4 になります。

結果：

- fixed star 候補：bad edge 16,822 本。greedy independent set は最大 234 頂点程度。
- best random-edgecolor tree 候補：bad edge 17,310 本。greedy independent set は最大 232 頂点程度。

厳密な最大独立集合は解いていませんが、少なくとも「少し削れば 1100 超が残る」という状況ではまったくありません。これは前回までの「少数の穴を潰す」路線と違い、bad-pair 構造がかなり密です。

## いま一番筋が良い変種：2-line-cover clique thinning

ここで、より良いアイデアが出ました。

star/tree thinning では、各 line にちょうど \(q\) 本の辺を置いていました。総 edge budget は正しいですが、line 内の接続力が弱い。

代わりに、**少数の line を選び、その line 上では clique を丸ごと残す**。

具体的には、hexagon の line 集合から部分集合

\[
\mathcal S
\]

を選び、各点がちょうど 2 本の selected line に乗るようにする：

\[
|\{L\in\mathcal S:p\in L\}|=2
\qquad\text{for every point }p.
\]

そして、各 selected line \(L\) の上では、その \(q+1\) 点を完全グラフ \(K_{q+1}\) にする。

このとき各点の次数は

\[
2q.
\]

edge 数も、tree-thinning と同じ budget です。しかし selected line 上の局所接続は clique なので、star/tree よりはるかに強い。

これはかなり筋が良いです。

\[
\boxed{
H(q)\text{ point graph}
+
\text{2-cover of points by hexagon lines}
+
\text{full cliques on selected lines}
}
\]

という構成になります。

成功すれば：

| \(q\) | \(d=2q\) | \(n=(q+1)(q^4+q^2+1)\) | 前回表の現行 \((d,4)\) | 更新幅 |
|---:|---:|---:|---:|---:|
| 4 | 8 | 1,365 | 1,100 | +265 |
| 5 | 10 | 3,906 | 2,331 | +1,575 |
| 7 | 14 | 19,608 | 8,200 | +11,408 |
| 8 | 16 | 37,449 | 14,640 | +22,809 |

特に \(q=8\) は依然として大本命です。

## 2-cover 方向の初期検査

2-cover の一番きれいな作り方は、spread を 2 つ取ることです。

spread とは、点集合を互いに交わらない line で分割する line 集合です。2 つの disjoint spread があれば、その和集合は各点をちょうど 2 回覆います。

初期検査：

- \(q=3\)：spread はすぐ見つかりました。ただし、その spread と disjoint な 2 つ目の spread は、その候補に対して infeasible でした。別の 2-cover は MILP で見つかりましたが、できた clique graph は直径 4 からかなり遠いです。
- \(q=4\)：spread / 2-cover の MILP は時間内に解けませんでした。randomized exact-cover backtracking でも短時間では spread が見つかりませんでした。

ここはまだ未解決です。ただし、これは「局所探索で穴を直す」問題ではなく、

\[
H(q)\text{ に point-2-covering line set があるか}
\]

という明確な有限幾何の設計問題です。

## 現時点の判断

最初の matching contraction は、単体では厳しそうです。

理由は、matching contraction が実質的には

\[
\text{各 line clique を star にする}
\]

という強い thinning であり、\(q=7,8\) では radius 4 の漏れが大きいからです。tree に広げても、小さい \(q\) では改善しませんでした。

一方で、次の

\[
\boxed{
\text{2-line-cover clique thinning}
}
\]

はまだ有望です。同じ次数 \(2q\) で、line 上の完全な接続を残せるため、効率の根拠が star/tree より強いです。

次に集中すべきサブ問題はこれです。

\[
\boxed{
H(4),H(5),H(8)\text{ で、各点をちょうど 2 回覆う line 集合 }\mathcal S
\text{ を構成し、その clique graph の直径 4 を検証する}
}
\]

これは今のところ、今回の「folding/thinning」系で一番数学的に筋が良い候補です。

---

## Turn 041 (Round 009) — 🧑 USER

_2026-05-23 13:31:32 UTC_

一度立ち止まって、この問題に対して、数学的に筋の良さそうな新アイデアを考えることに集中してみてください。

---

## Turn 042 (Round 009) — 🤖 ASSISTANT

_2026-05-23 13:32:01 UTC_  ·  model: `gpt-5-5-pro`

計算はいったん止め、効率の見積もり・次数予算の使い方・直径証明の有限構造が最初から噛み合う候補だけに絞って考え直します。前回までの失敗も、局所穴埋めや根拠の弱い構成を除外するフィルターとして使います。

---

## Turn 043 (Round 009) — 🤖 ASSISTANT

_2026-05-23 13:50:58 UTC_  ·  model: `gpt-5-5-pro`

はい。立ち止まって考えると、前回の「line clique thinning / 2-cover」方向は、かなりはっきり捨てるべきです。理由は単なる実験失敗ではなく、**分岐数の上限が足りない**からです。

たとえば「選んだ line 上だけ clique を残す」構成は、実質的にはある \((q+1)\)-正則グラフ \(\Gamma\) の line graph \(L(\Gamma)\) です。このとき \(L(\Gamma)\) の半径 4 ball は高々

\[
1+2q+2q^2+2q^3+2q^4
\]

程度しか広がりません。\(q=8\) ならこれは

\[
1+16+128+1024+8192=9361
\]

です。ところが狙っていた頂点数は

\[
37449
\]

でした。つまり、直径 4 どころか、**この構成型では原理的にサイズが伸びません**。ここはきっぱり捨てます。

## 新しい中心方針：opposition を「辺追加」ではなく「折り畳み」に使う

generalized hexagon の一番強い構造は、局所の line clique ではなく、**opposition relation** です。

前回までは「直径 6 の構造に少数の辺を足す」発想でした。しかし本当に使うべきなのは、距離最大の対象をペアにして、グラフ全体を大域的に折ることです。

つまり：

\[
\text{近いものをまとめるのではなく、最も遠いものを対応させる}
\]

これが今回の新しい本命です。

---

# 本命案 A：\(H(7)\) の point-line opposition matching contraction

split Cayley generalized hexagon \(H(7)\) を使います。

点集合を \(P\)、線集合を \(L\) とすると、

\[
|P|=|L|=(7+1)(7^4+7^2+1)=19608.
\]

incidence graph は次数 8、直径 6 です。

ここで、各点 \(p\in P\) に対して、\(p\) と incident ではなく、むしろ incidence graph 距離 5 にある **opposite line** \(\phi(p)\in L\) を 1 本選ぶ。さらに

\[
\phi:P\to L
\]

を全単射にします。これは point-line opposition graph の perfect matching です。

そして、各ペア

\[
p \sim \phi(p)
\]

を同一視します。得られるグラフの頂点数は

\[
19608.
\]

縮約後、各頂点は

- 点 \(p\) を通る 8 本の line 側から来る近傍
- line \(\phi(p)\) 上の 8 点側から来る近傍

を持つので、最大次数は

\[
8+8=16.
\]

したがって、もし直径 4 なら

\[
(d,k,n)=(16,4,19608).
\]

現行記録は

\[
N(16,4)\ge14640
\]

なので、

\[
19608-14640=4968
\]

の更新になります。

## なぜこれは筋が良いか

この構成は、前回の incident matching contraction とは本質的に逆です。

incident matching contraction では、点 \(p\) とその近くの線 \(L\ni p\) を折っていました。その結果、近傍が重なりすぎ、実効分岐が小さくなりました。

今回の opposition contraction では、点 \(p\) と、\(p\) から最も遠い line \(\phi(p)\) を折ります。すると、縮約頂点の 2 つの半分、

\[
p \quad\text{と}\quad \phi(p)
\]

の局所近傍がほとんど重なりません。つまり次数 16 を、line clique のような密な局所構造に浪費せず、遠方への分岐に使える。

これは degree-diameter 的にかなり重要です。直径 4、次数 16 の Moore bound は

\[
1+16+16\cdot15+16\cdot15^2+16\cdot15^3=54241.
\]

候補の 19608 は Moore bound の約 36% なので、局所分岐がかなり良ければ到達可能なサイズです。前回の line graph 型のように半径 4 ball が 9361 で頭打ちになる構造とは違います。

## 設計問題としての形

この案は、局所修復ではなく、次の明確な有限設計問題です。

\[
\boxed{
H(7)\text{ の point-line opposition graph に、直径 4 quotient を与える perfect matching }\phi
\text{ を作る}
}
\]

隣接は点集合 \(P\) 上で

\[
p\sim r
\quad\Longleftrightarrow\quad
p\in \phi(r)
\ \text{ または }\
r\in \phi(p)
\]

と定義できます。

直径 4 の証明は、

\[
I+A+A^2+A^3+A^4
\]

が全成分正、という完全な証明書になります。ここで \(A\) はこの quotient graph の隣接行列です。

探索を使うとしても、「bad pair を直す」ではなく、\(\phi\) をある構造族から作って、その直径を一発検証する形にします。

---

# 本命案 B：\(H(7)\) の chamber graph に opposition 2-factor を足す

もう一つ、かなり筋が良い案があります。むしろサイズはこちらの方が大きいです。

\(H(7)\) の chamber とは incident pair

\[
(p,L),\qquad p\in L
\]

です。chamber 数は

\[
|{\mathcal C}|=(7+1)^2(7^4+7^2+1)
=64\cdot2451
=156864.
\]

chamber graph を考えます。2 つの chamber が

- 同じ点を共有する、または
- 同じ線を共有する

とき隣接させる。

この graph は

\[
2q=14
\]

正則で、直径は 6 です。

距離分布は非常にきれいで、1 つの chamber から見た距離層は

\[
1,\quad 2q,\quad 2q^2,\quad 2q^3,\quad 2q^4,\quad 2q^5,\quad q^6.
\]

\(q=7\) では

\[
1,\ 14,\ 98,\ 686,\ 4802,\ 33614,\ 117649.
\]

つまり、直径 6 の obstruction は最後の

\[
q^6=117649
\]

個の opposite chambers だけです。

ここに、opposite chamber 同士を結ぶ 2-regular graph、つまり opposition relation の 2-factor を足します。具体的には、opposition permutation

\[
\alpha:{\mathcal C}\to{\mathcal C},
\qquad
\alpha(C)\text{ is opposite to }C
\]

を取り、各 chamber \(C\) に

\[
C\sim \alpha(C),\qquad C\sim \alpha^{-1}(C)
\]

を追加します。

すると次数は

\[
14+2=16.
\]

もし直径 5 になれば、

\[
(d,k,n)=(16,5,156864).
\]

現行記録は

\[
N(16,5)\ge132496
\]

なので、

\[
156864-132496=24368
\]

の更新です。

## なぜこれも筋が良いか

これは「少数のランダム辺で穴を潰す」ではありません。

chamber graph はすでに距離 5 までで

\[
1+14+98+686+4802+33614=39215
\]

個を覆っています。残っているのは、幾何的に完全に意味のある opposite layer だけです。

そこに、opposition relation から次数 2 分だけ選んで入れる。つまり次数 16 のうち、

\[
14
\]

は generalized hexagon の chamber geometry に使い、

\[
2
\]

は opposite layer を折るためだけに使う。

これは degree budget の使い方としてかなり自然です。

---

# どちらを優先するべきか

優先順位はこうです。

## 第一候補：point-line opposition matching contraction

\[
H(7)\Rightarrow (16,4,19608).
\]

理由は、構成が最も単純だからです。

必要なのは

\[
P\to L
\]

の 1 個の opposition matching だけです。候補グラフも 19608 頂点なので、完全検証しやすい。成功すれば \((16,4)\) を 4968 頂点更新します。

## 第二候補：chamber opposition 2-factor augmentation

\[
H(7)\Rightarrow (16,5,156864).
\]

こちらは更新幅が大きいですが、設計対象が chamber なので少し重いです。ただし構造は非常にきれいで、成功すればかなり強い結果になります。

---

# matching をどう作るべきか

ここが重要です。ランダム matching を大量に試すだけでは、また局所探索寄りになります。

狙うべきは、root group coordinate による **MDS 型 opposition matching** です。

generalized hexagon の opposite cell は、Moufang/root group 座標でおおまかに

\[
\mathbb F_q^5
\quad\text{または}\quad
\mathbb F_q^6
\]

のようにパラメータ化できます。

普通の incidence move は、この座標の一部だけを変える操作に対応します。したがって、opposition matching \(\phi\) や opposition permutation \(\alpha\) が、座標をよく混ぜる写像になっていれば、

\[
\text{少数の ordinary moves}
+
\text{1 or 2 opposition jumps}
+
\text{少数の ordinary moves}
\]

で任意の target 座標を解ける可能性があります。

つまり欲しいのは、雑に言えば

\[
\text{opposition layer 上の MDS 行列 / orthogonal array 的な写像}
\]

です。

これはかなり良い制約です。候補を無制限に探すのではなく、例えば

- companion matrix 型
- Cauchy matrix 型
- Vandermonde 型
- semilinear map 型
- root coordinate の triangular map 型

のような、小さく構造的な族だけを列挙すればよい。

計算の役割は、

\[
\text{構造族の候補生成}
\quad+\quad
\text{直径 4 または 5 の完全検証}
\]

です。bad pair を見て修復するのではありません。

---

# 今回の判断

今の時点で一番数学的に筋が良い新方針はこれです。

\[
\boxed{
\text{generalized hexagon }H(7)\text{ の opposition relation を使った大域的 folding}
}
\]

具体的には、

\[
\boxed{
\text{point-line opposition matching contraction}
}
\]

を第一候補にします。

成功目標は

\[
\boxed{
(16,4,19608)
}
\]

です。

その次に、

\[
\boxed{
\text{chamber opposition 2-factor augmentation}
}
\]

で

\[
\boxed{
(16,5,156864)
}
\]

を狙う。

この方向は、前回までの line thinning よりずっと良いです。理由は明確で、次数を局所 clique に浪費せず、generalized hexagon の最長距離構造、つまり opposition を直接使って、グラフ全体を折り畳むからです。

---

## Turn 044 (Round 010) — 🧑 USER

_2026-05-23 14:38:10 UTC_

その方針でつづきお願いします

---

## Turn 045 (Round 010) — 🤖 ASSISTANT

_2026-05-23 14:38:28 UTC_  ·  model: `gpt-5-5-pro`

了解です。今回は opposition folding に絞り、まず \(H(7)\) の point-line opposition matching contraction を構造的候補として生成・完全検証し、失敗時は chamber 側へ進みます。

---

## Turn 046 (Round 010) — 🤖 ASSISTANT

_2026-05-23 14:41:33 UTC_  ·  model: `gpt-5-5-pro`

最初の実装は動き、ランダムな opposition matching では直径4からまだ最大約1,300頂点漏れるため、単なる密な matching では不足です。次は Zorn/octonion 座標由来の構造写像で距離混合を検証します。

---

## Turn 047 (Round 010) — 🤖 ASSISTANT

_2026-05-23 14:50:40 UTC_  ·  model: `gpt-5-5-pro`

小さい検証として \(q=3\) では同じ point-line opposition contraction が直径4になり、発想自体は生きています。並行して \(q=8\) の次数18折り畳みを完全設計で16へ落とす変種も検査しています。

---

## Turn 048 (Round 010) — 🤖 ASSISTANT

_2026-05-23 15:01:59 UTC_  ·  model: `gpt-5-5-pro`

進めました。結論から言うと、**今回も新記録の検証済みグラフは出ていません**。ただし、かなり大事な判断材料が出ました。

成果物はこちらです。

[phase6_opposition_artifacts.zip](sandbox:/mnt/data/phase6_opposition_artifacts.zip)

## 今回の結論

前回の本命だった

\[
H(7)\text{ の opposition folding}
\]

は、**素朴な matching / permutation / color 分解では、ほぼ random degree-16 graph 的な挙動に止まる**ことが分かりました。

これは「あと少しだから局所探索で埋める」という状況ではありません。むしろ、

\[
n=19608,\quad d=16,\quad k=4
\]

では、ランダムに近い 16-regular graph だと半径 4 ball が全体を覆い切らず、だいたい 1000 個前後漏れるのが自然です。今回の実験値もまさにそのスケールでした。

ざっくり言うと、木状分岐なら深さ 4 で

\[
16\cdot15^3=54000
\]

程度まで広がれるように見えますが、頂点数 \(19608\) の有限集合では衝突が多く、ランダム被覆の未到達期待は概算で

\[
19608\exp(-54000/19608)\approx 1245
\]

くらいになります。今回の opposition folding 系の miss が 1100〜1300 周辺に出るのは、ほぼこのランダム被覆限界と一致します。

つまり、**単に opposition jump をランダム風に入れるだけでは足りない**です。新記録を出すには、distance layer をほぼ Moore graph 的に無駄なく覆う、かなり強い設計が必要です。

---

## 1. point-line opposition matching contraction

まず前回の第一候補を実装しました。

\(H(7)\) の点集合 \(P\)、線集合 \(L\) に対して、各点 \(p\) を opposite line \(\phi(p)\) と同一視する構成です。

\[
|P|=19608,\qquad \Delta\le16.
\]

成功すれば

\[
(d,k,n)=(16,4,19608)
\]

で、現行 \((16,4)=14640\) を超える候補でした。

### 結果

ランダムな opposition matching \(\phi:P\to L\) を作って quotient graph を完全検査したところ、最良候補でも

\[
\text{最大 radius-4 miss}=1279
\]

でした。

つまり、ある始点から距離 4 以内に届く頂点数の最悪値は

\[
19608-1279=18329.
\]

直径 4 には届いていません。

degree はだいたい

\[
15\text{〜}16
\]

で、次数条件は満たしています。ただし距離被覆が不足しています。

---

## 2. 構造的 matching：\(\phi(p)=T(M_c(p))\)

ランダム matching だけだと弱いので、より構造的な候補も試しました。

incidence edge-coloring の 1 色 \(c\) から、点 \(p\) に incident line \(M_c(p)\) を対応させます。そこに Zorn model 上の \(SL(3,7)\) 型 collineation \(T\) を作用させ、

\[
\phi(p)=T(M_c(p))
\]

とする候補です。

これはかなり自然です。  
「incidence matching を大きく動かして opposite matching にする」という発想で、局所修復ではなく、大域的な collineation に基づきます。

### 結果

100 個程度の \(SL(3,7)\) 型変換を試しましたが、完全な opposition matching にはなりませんでした。最良候補でも、opposition 条件に反する点が 325 個ありました。

その 325 個だけを swap で修正して opposition matching にした後、距離を調べると、むしろランダム matching より悪くなりました。サンプル評価で

\[
\text{radius-4 miss}\approx2200\text{〜}2600
\]

程度です。

この構造族は、きれいではありますが、展開性が弱いです。点と線の対応が collineation 由来で規則的すぎて、半径 4 ball の衝突が増えているように見えます。

---

## 3. chamber opposition 2-factor augmentation

次に第二候補も試しました。

\(H(7)\) の chamber graph を使います。chamber 数は

\[
(7+1)^2(7^4+7^2+1)=156864.
\]

chamber graph 自体は

\[
14\text{-regular},\qquad \operatorname{diam}=6.
\]

ここに chamber opposition permutation

\[
\alpha(C)\text{ is opposite to }C
\]

を入れて、

\[
C\sim\alpha(C),\qquad C\sim\alpha^{-1}(C)
\]

を追加します。次数は

\[
14+2=16.
\]

成功すれば

\[
(d,k,n)=(16,5,156864)
\]

となり、現行 \((16,5)=132496\) を超える候補です。

### 重要な修正

最初に使っていた chamber opposition 判定は少し弱すぎました。正しい chamber opposition は chamber graph 距離 6 です。

\(H(7)\) chamber graph で距離層を確認すると、

\[
1,\ 14,\ 98,\ 686,\ 4802,\ 33614,\ 117649.
\]

したがって、1 chamber あたりの true opposite chamber 数は

\[
7^6=117649.
\]

これを使って正しく opposition permutation を生成しました。

### 結果

ランダムな true opposition permutation を入れても、128 始点サンプルで

\[
\text{radius-5 miss}\approx48500
\]

程度残りました。

これはかなり遠いです。  
この chamber 2-factor augmentation は、現状では本命から外すべきです。

---

## 4. line bundle を壊す改良：opposition color permutations

point-line contraction の弱点は、各頂点の隣接先が「1 本の line の 8 点」やその逆像に束になってしまうことです。これが半径 4 ball の衝突を増やしている可能性がありました。

そこで、より散らす構成を試しました。

incidence edge-coloring

\[
\chi(p,L)\in\{0,\dots,7\}
\]

を使います。各 line 上にも各 point 周りにも全色が 1 回ずつ出る coloring です。

opposition matching \(\phi_i:P\to L\) を 8 本取り、各 \(i\) について、点 \(p\) から line \(\phi_i(p)\) 上の「色 \(c_i\) の点」だけに辺を張る。

つまり各 \(i\) は点集合上の permutation

\[
f_i(p)=\text{the point of color }c_i\text{ on }\phi_i(p)
\]

を定めます。これを 8 本 union すると、各 \(f_i\) が 2-regular な無向 permutation graph を与えるので、

\[
\Delta\le16.
\]

これはかなりきれいな構成です。

\[
\boxed{
H(7)
+
8\text{ opposition matchings}
+
\text{incidence color selectors}
}
\]

という形で、line 全体の bundle を壊し、次数を 16 に厳密制御できます。

### 結果

しかし、これも 512 始点サンプルで最良

\[
\text{radius-4 miss}\approx1173
\]

でした。

point-line contraction のランダム版とほぼ同じです。

これは大事です。  
line bundle を壊しても、ランダム 16-regular graph 的な被覆限界から抜け出せませんでした。

---

## 5. 小型候補：\(H(4)\) chamber graph + opposition permutations

小さいパラメータでも確認しました。

\(H(4)\) chamber graph は

\[
6825\text{ vertices},\qquad 8\text{-regular}.
\]

opposition permutation を 2 本追加すれば次数は

\[
8+4=12.
\]

直径 4 なら

\[
(d,k,n)=(12,4,6825)
\]

で、現行 \((12,4)=4680\) を超えます。

### 結果

50 trial を始めましたが、序盤からかなり遠く、完全検査で

\[
\text{最大 radius-4 miss}\approx1700
\]

程度でした。

こちらも見込み薄です。

---

## 判断

今回の opposition folding 系は、アイデアとしては数学的にきれいでした。特に

\[
\text{近いものではなく、最も遠いものを折る}
\]

という発想は自然です。

ただし、実験結果から見ると、素朴な matching / permutation / color selector では、結局

\[
\text{random degree-16 graph 程度の被覆性能}
\]

に止まります。

そして \(n=19608,k=4,d=16\) で新記録を狙うには、random-like では足りません。必要なのは、各始点の半径 4 ball が distance layer をほぼ無駄なく覆うような、かなり強い **near-Moore covering design** です。

したがって、今後この方向を続けるなら、単に opposition matching を変えるのではなく、次のような設計問題に落とす必要があります。

\[
\boxed{
\text{root-group coordinates 上で、半径 4 の到達式が全座標を解くような opposition maps を作る}
}
\]

つまり、matching をランダムに選ぶのではなく、opposition layer を

\[
\mathbb F_7^5 \text{ または } \mathbb F_7^6
\]

の座標で書き、4 step の到達写像が MDS code / orthogonal array / perfect hash family のように全 target を覆うことを証明する必要があります。

今回の結論としては：

\[
\boxed{
\text{opposition を使う方針自体はまだ捨てなくてよいが、matching/permutation レベルの構成は不足}
}
\]

です。

次に進むなら、「opposition matching を探す」ではなく、**root coordinate で距離 4 到達を代数方程式として解ける構成**に切り替えるべきです。

---

## Turn 049 (Round 011) — 🧑 USER

_2026-05-23 15:04:32 UTC_

構成の方針を考えてください。行き当たりばったりではなく、数学的に勝算があると考えられる方向に思考を進めてください

---

## Turn 050 (Round 011) — 🤖 ASSISTANT

_2026-05-23 15:05:01 UTC_  ·  model: `gpt-5-5-pro`

ここでは探索を止め、まず「なぜ記録密度に届くのか」を次数予算・距離球成長・既存記録との差から逆算して候補を絞ります。前回までの失敗は、分岐効率が足りない構成型を捨てる判断材料として使います。

---

## Turn 051 (Round 011) — 🤖 ASSISTANT

_2026-05-23 15:08:16 UTC_  ·  model: `gpt-5-5-pro`

さらに、候補は「サイズ効率」「直径証明が閉じるか」「既存手法との差」の3条件でふるい、局所的に穴を埋める型は最初から外します。

---

## Turn 052 (Round 011) — 🤖 ASSISTANT

_2026-05-23 15:23:25 UTC_  ·  model: `gpt-5-5-pro`

方針を立て直すなら、次は **「有限 building の chamber graph に、少数の大域的 jump involution を加える」** が一番筋が良いと思います。

前回までの反省から、もう次の型は捨てます。

- bad pair を見て直す局所修復。
- generalized hexagon に適当な shortcut matching を足すだけ。
- line clique thinning / 2-cover のように、局所構造で次数を使い切ってしまう構成。
- random matching を何本も試して「たまたま直径が下がる」ことを期待する構成。

代わりに、最初から次の形にします。

\[
\boxed{
\text{finite spherical building の chamber graph}
+
\text{少数の大域的な opposition / polarity jump}
}
\]

これはかなり明確な勝算があります。理由は、building の chamber graph には最初から

\[
\text{次数が小さい},\quad
\text{距離分布が完全に分かる},\quad
\text{直径が Weyl group の longest element の長さ}
\]

という強い構造があるからです。そこに「longest element 的な jump」を足すと、直径をほぼ半分にできる可能性があります。

---

## 基本設計

有限 building の chamber graph \(\Gamma_0\) を使います。

chamber graph では、2 つの chamber が 1 つの panel だけ違うとき隣接させます。たとえば type \(A_4\) の building、つまり \(PG(4,q)\) の complete flag graph では、各 chamber は

\[
V_1<V_2<V_3<V_4}\subset \mathbb F_q^5
\]

で、1 回の通常 move はこのうち 1 個の \(V_i\) だけを変えます。

この base graph の次数は

\[
r q
\]

です。ここで \(r\) は building の rank です。

次に、いくつかの involution

\[
J_1,J_2,\dots,J_s
\]

を chamber 集合上に定義して、各 chamber \(C\) と \(J_i(C)\) を辺で結びます。各 \(J_i\) が involution なら、追加次数は 1 本あたり 1 です。

完成グラフは

\[
\Gamma=\Gamma_0+\{C\sim J_i(C)\}.
\]

この構成のポイントは、\(J_i\) を random permutation にしないことです。  
\(J_i\) は polarity、duality、root-coordinate reversal、anisotropic torus action など、**building の opposition geometry から来る大域 map**にします。

---

## なぜこの方針は勝算があるか

この方針では、候補を選ぶ前に「その次数・直径でそもそも到達可能か」をかなり厳しく判定できます。

base graph \(\Gamma_0\) の半径 \(a\) ball のサイズを

\[
B_a
\]

とします。追加 jump map が \(s\) 本あり、目標直径が \(k\) のとき、半径 \(k\) で到達できる頂点数は、どんなにうまく jump を選んでも、おおざっぱには

\[
U_s(k)=
\sum_{j=0}^{k}
s^j
\sum_{a_0+\cdots+a_j\le k-j}
B_{a_0}B_{a_1}\cdots B_{a_j}
\]

を超えません。

これは「通常 move の塊、jump、通常 move の塊、jump、…」という path 分解から来る上界です。

したがって、

\[
U_s(k)<|V|
\]

なら、その \(s\) では絶対に無理です。  
逆に、

\[
U_s(k)
\]

が \(|V|\) を少し超えるところが、数学的に一番狙う価値があります。これは「次数が足りているが、余りすぎてもいない」状態です。

この判定を入れると、候補がかなり絞れます。

---

# 第一候補：\(A_4(3)\) flag building + 4 polarities

これは今いちばん筋が良いと思います。

## base graph

\(V=\mathbb F_3^5\) とし、頂点を complete flag

\[
F=(V_1<V_2<V_3<V_4)
\]

とします。

通常辺は、flag のうち 1 つの部分空間だけを変える panel adjacency。

これは type \(A_4\) building の chamber graph です。

次数は

\[
4q=4\cdot3=12.
\]

直径は Weyl group \(S_5\) の longest element の長さなので

\[
\binom{5}{2}=10.
\]

頂点数は complete flag の個数：

\[
[5]_3[4]_3[3]_3[2]_3
=
121\cdot40\cdot13\cdot4
=
251,680.
\]

このままだと

\[
(d,k,n)=(12,10,251680)
\]

です。

ここに 4 本の polarity jump を足します。

## jump map

非退化対称双線形形式 \(B_t\) を 4 つ選びます。

各 \(B_t\) から polarity

\[
J_t(F)=
(V_4^{\perp_t}<V_3^{\perp_t}<V_2^{\perp_t}<V_1^{\perp_t})
\]

を定義します。

これは chamber 集合上の involution です。  
したがって各 \(J_t\) は追加次数 1 だけを使います。

完成グラフの次数は

\[
12+4=16.
\]

もし直径が 5 なら、

\[
\boxed{N(16,5)\ge251,680}
\]

になります。

前回表の現行記録は

\[
N(16,5)\ge132,496
\]

なので、成功すれば

\[
+119,184
\]

の更新です。

## なぜ 4 本が自然か

この候補では、追加 jump 本数 \(s\) に対して情報量上界を計算すると、

\[
s=3
\]

では半径 5 ball の理論上界が

\[
251,058
\]

程度で、頂点数

\[
251,680
\]

に届きません。

つまり、**3 本の jump ではどんなに賢く選んでも直径 5 は無理**です。

一方、

\[
s=4
\]

では上界が

\[
429,639
\]

程度になり、初めて可能性が出ます。

したがって

\[
A_4(3)+4\text{ polarities}
\]

は、次数 16・直径 5 を狙ううえで、かなり自然な「ちょうど足りる」候補です。これは行き当たりばったりではなく、距離分布と次数予算から出てくる候補です。

## polarity の選び方

ここも random にしません。

1 つの標準形式 \(B_0\) を取り、\(\mathbb F_3^5\) 上の irreducible Singer 型作用素 \(S\) を選びます。  
そして

\[
B_i(x,y)=B_0(S^{e_i}x,S^{e_i}y)
\]

で 4 つの形式を作る。

指数集合

\[
\{e_0,e_1,e_2,e_3\}
\]

は、低次元部分空間に対して退化条件が重ならないような MDS/cap 的な集合にします。たとえば最初に試すべきは、Singer orbit 上で互いの差が小さい周期構造を持たない 4 点です。

意図はこうです。

- polarity は Weyl 距離の長い方向へ flag を送る。
- 4 つの polarity が異なる「遠方方向」を担当する。
- 通常 move が局所座標を調整し、polarity jump が Weyl 方向を反転させる。
- 半径 5 の path で全 flag を覆う。

この設計なら、計算は「候補形式の列挙」と「直径の完全検証」だけになります。bad pair を見て polarity を直すような局所改善はしません。

---

# 第二候補：\(C_3(3)\) symplectic building + 3 jump maps

次に筋が良いのは、rank 3 symplectic building です。

## base graph

\(\mathbb F_3^6\) に標準 symplectic form を入れ、頂点を totally isotropic flag

\[
P<L<M
\]

とします。ここで

\[
\dim P=1,\quad \dim L=2,\quad \dim M=3
\]

です。

これは type \(C_3\) building の chamber graph。

次数は

\[
3q=9.
\]

直径は type \(C_3\) Weyl group の longest element の長さなので

\[
9.
\]

頂点数は

\[
\frac{3^2-1}{3-1}
\cdot
\frac{3^4-1}{3-1}
\cdot
\frac{3^6-1}{3-1}
=
4\cdot40\cdot364
=
58,240.
\]

ここに 3 本の jump map を足すと次数は

\[
9+3=12.
\]

もし直径 5 なら、

\[
\boxed{N(12,5)\ge58,240}
\]

になります。

現行記録は

\[
N(12,5)\ge29,621
\]

なので、成功すればほぼ倍です。

## なぜ 3 本が自然か

この building の距離分布を使うと、半径 5 に対して

\[
s=2
\]

本の jump では、到達可能数の理論上界が

\[
56,902
\]

程度で、頂点数

\[
58,240
\]

に届きません。

一方、

\[
s=3
\]

では上界が

\[
115,935
\]

になり、可能になります。

つまり、ここでも

\[
3\text{ jumps}
\]

が情報量的に最小です。

これはかなり良い候補です。  
\(A_4(3)\) より小さく、検証もしやすい。ただし \(C_3\) には \(A_4\) の polarity ほど自然な type-reversing duality がないので、jump map の設計は少し難しいです。

候補としては、symplectic group の anisotropic torus から来る大域 map を使うのがよいです。具体的には、\(\mathbb F_{3^3}\) を使って \(\mathbb F_3^6\) を

\[
\mathbb F_{3^3}\oplus \mathbb F_{3^3}
\]

のように見て、norm 1 torus や Singer 型作用から 3 つの遠方 map を作る。これにより、totally isotropic flag を大きく動かしつつ、通常 panel move で座標調整できるようにします。

---

# 第三候補：\(G_2(4)\) generalized hexagon chamber graph + 3 jump maps

これはさらに小さなテストケースとして良いです。

split Cayley generalized hexagon \(H(4)\) の chamber graph を使います。

頂点数は

\[
(q+1)^2(q^4+q^2+1)
=
25(256+16+1)
=
6,825.
\]

次数は chamber graph なので

\[
2q=8.
\]

直径は

\[
6.
\]

ここに 3 本の involutive jump を足すと次数は

\[
8+3=11.
\]

もし直径 4 なら、

\[
\boxed{N(11,4)\ge6,825}
\]

です。

現行記録は

\[
N(11,4)\ge3,200
\]

なので、成功すれば大更新です。

情報量上界でも、

\[
s=2
\]

では足りず、

\[
s=3
\]

で初めて可能になります。したがって、これも「ちょうど足りる」候補です。

ただし、前に random opposition permutation はかなり悪かったので、ここでは絶対に random matching はやりません。やるなら root group coordinate で

\[
(a_1,\dots,a_6)\mapsto \text{coordinate reversal + MDS linear transform}
\]

のような明示的 jump を作るべきです。

---

## 優先順位

私は次を本線にします。

### 1. \(A_4(3)+4\) polarities

\[
\boxed{(d,k,n)=(16,5,251680)}
\]

最も明快です。  
complete flag、panel adjacency、polarity という構成要素が全部きれいで、追加次数 4 も情報量的に最小です。

### 2. \(C_3(3)+3\) anisotropic jumps

\[
\boxed{(d,k,n)=(12,5,58240)}
\]

サイズが小さく、現行記録を倍近く超えます。jump map の設計は \(A_4\) より少し難しいですが、検証しやすい。

### 3. \(G_2(4)+3\) coordinate-opposition jumps

\[
\boxed{(d,k,n)=(11,4,6825)}
\]

小型検証用。成功すればかなり美しいですが、前の random opposition の失敗から、座標設計なしでは厳しいです。

---

## この方針での「計算」の役割

計算は局所改善に使いません。

使うのは次の 2 つだけです。

1. **候補 jump map の列挙**  
   Singer orbit、polarities、anisotropic torus、MDS 型 coordinate reversal など、最初から数式で定義された小さな族だけを見る。

2. **直径証明の完全検証**  
   BFS でもよいし、より強くは Weyl distance + root coordinate の到達式を列挙して、全 chamber が半径 \(k\) に入ることを証明する。

bad pair を見て map を直すことはしません。  
候補が失敗したら、失敗した候補を修復するのではなく、その構成族を捨てるか、より高次の設計条件を入れます。

---

## 現時点の本命

最も進める価値があるのはこれです。

\[
\boxed{
PG(4,3)\text{ の complete flag graph}
+
4\text{ 個の general-position polarity}
}
\]

狙いは

\[
\boxed{N(16,5)\ge251,680}
\]

です。

この候補は、次数・直径・頂点数のバランスがかなり良いです。  
特に「3 polarity では情報量上無理、4 polarity で初めて可能」という点が強いです。これは、ただの思いつきではなく、この構成型で \(d=16,k=5\) を狙う必然性を与えています。

---

## Turn 053 (Round 012) — 🧑 USER

_2026-05-23 15:34:39 UTC_

進めてください

---

## Turn 054 (Round 012) — 🤖 ASSISTANT

_2026-05-23 15:34:56 UTC_  ·  model: `gpt-5-5-pro`

まず本命の \(A_4(3)\) 案を、候補生成と完全検証まで通せる形に落とします。失敗時は修復せず、距離分布と失敗規模で構成族自体を評価します。

---

## Turn 055 (Round 012) — 🤖 ASSISTANT

_2026-05-23 15:38:09 UTC_  ·  model: `gpt-5-5-pro`

最初の実装結果では、\(A_4(3)+4\) polarity は半径5で未到達が約22.6万あり、opposite jump として十分機能していません。これは小さな不足ではなく、この構成族自体を見直すべき兆候です。

---

## Turn 056 (Round 012) — 🤖 ASSISTANT

_2026-05-23 15:47:23 UTC_  ·  model: `gpt-5-5-pro`

さらに構造的には、polarity が chamber graph の自己同型に留まるため、到達集合は小さな building ball の和に閉じてしまいます。したがって Singer 共役の微調整ではなく、候補族ごと捨てる判断に進みます。

---

## Turn 057 (Round 012) — 🤖 ASSISTANT

_2026-05-23 16:06:18 UTC_  ·  model: `gpt-5-5-pro`

進めました。今回は「前案をそのまま回す」のではなく、まず数学的に破綻していないかを確認し、破綻している候補は捨てました。

成果物はこちらです。

[phase7_strategy_reset_artifacts.zip](sandbox:/mnt/data/phase7_strategy_reset_artifacts.zip)

## 1. \(A_4(3)+4\) polarities は捨てるべきです

前回の本命だった

\[
PG(4,3)\text{ complete flag graph}+4\text{ polarities}
\]

は、実装以前に構造的な弱点がありました。

polarity は chamber graph の自己同型です。したがって、polarity jump を何本足しても、path は

\[
\text{ordinary moves} \to J_i \to \text{ordinary moves} \to J_j \to \cdots
\]

という形になりますが、各 \(J_i\) が base chamber graph の距離を保つため、到達集合は「いくつかの ordinary ball の和」にしかなりません。以前考えていたような「ball size が積で増える」挙動にはなりません。

\(A_4(3)\) の complete flag graph では、ordinary chamber ball のサイズは

\[
B_0=1,\quad B_1=13,\quad B_2=94,\quad B_3=499,\quad B_4=2119,\quad B_5=7465.
\]

4 本の automorphism jump を使っても、半径 5 の到達数は高々粗く

\[
B_5+4B_4+4^2B_3+4^3B_2+4^4B_1+4^5B_0=38303
\]

程度です。ところが頂点数は

\[
251680.
\]

つまり、**どんな 4 polarities を選んでも直径 5 は不可能**です。

実験でも、exponents \(\{0,1,3,9\}\) の Singer 型 polarity 4 本で、半径 5 到達数はサンプル最悪

\[
19259/251680
\]

に止まりました。これは実装の失敗ではなく、候補族そのものの失敗です。

ここは明確に撤退します。

---

## 2. 新しく筋が良い候補：generalized hexagon の point graph を one-factor 化する

次に考えたのは、split Cayley generalized hexagon \(H(q)\) の **point graph** です。

\(H(q)\) の point graph は、同じ hexagon line 上にある点同士を隣接させるグラフで、

\[
|P|=(q+1)(q^4+q^2+1),
\]

full point graph の直径は 3 です。ただし次数は

\[
q(q+1)
\]

と大きすぎます。

そこで各 hexagon line 上の clique \(K_{q+1}\) を、完全グラフではなく **perfect matching** に置き換えます。つまり、各 line 上で点をペアにし、そのペアだけを辺にする。

各点は \(q+1\) 本の line に乗っているので、各 line が 1 本ずつ辺を与えれば、得られるグラフは

\[
(q+1)\text{-regular}
\]

です。

これは局所修復ではなく、

\[
\boxed{
H(q)\text{ の全 line clique を、同時に one-factor へ置換する}
}
\]

という大域的な有限幾何構成です。

### なぜ筋が良いか

この構成は、以前の chamber thinning よりずっと良いです。

chamber thinning は局所 panel の情報を半分捨てるだけで、距離球の分岐が大きく落ちました。一方、point one-factor 化は、full point graph の直径 3 構造を保ちながら、各 line から最小限の 1-factor を残す構成です。

さらに、点グラフの短い cycle は generalized hexagon の girth 12 制約に強く縛られるので、初期分岐が比較的 tree-like になります。これは degree-diameter 的にかなり重要です。

---

## 3. 実験結果

### \(H(7)\)：\((d,k,n)=(8,5,19608)\) 候補

\[
q=7,\quad |P|=8(7^4+7^2+1)=19608,\quad d=8.
\]

もし直径 5 なら、

\[
N(8,5)\ge19608
\]

となり、現行 5115 を大きく超える候補でした。

しかし random line perfect matching では、full radius-5 scan の最良でも

\[
13071/19608
\]

しか届きませんでした。失敗です。

追加で global perfect matching を足すと、

\[
d=9:\quad 16541/19608,
\]

\[
d=10:\quad 18881/19608
\]

まで改善しました。ただし \(d=11\) まで上げると、頂点数 19608 は現行 \((11,5)=19620\) を下回るため記録候補ではなくなります。

---

### \(H(9)\)：一番重要な近接候補

\[
q=9,\quad |P|=10(9^4+9^2+1)=66430.
\]

one-factor 化だけなら

\[
d=10,\quad n=66430.
\]

直径 5 なら \((10,5)\) の大更新ですが、サンプルでは半径 5 到達が

\[
44188/66430
\]

程度で失敗しました。

そこで、one-factor 化に加えて、global perfect matching を追加しました。

| 構成 | 最大次数 | 頂点数 | 半径 5 サンプル結果 |
|---|---:|---:|---:|
| line one-factor only | 10 | 66,430 | 約 44,200 / 66,430 |
| +2 global matchings | 12 | 66,430 | 約 62,500 / 66,430 |
| +3 global matchings | 13 | 66,430 | 約 65,500 / 66,430 |
| +4 global matchings | 14 | 66,430 | 最良サンプル miss 約 119〜125 |

ここが今回の一番重要な発見です。

\[
\boxed{
H(9)\text{ point one-factor graph}+4\text{ extra 1-factors}
}
\]

は

\[
(d,k,n)=(14,5,66430)
\]

候補になります。現行記録は

\[
N(14,5)\ge58095.
\]

したがって、直径 5 を証明できれば

\[
66430-58095=8435
\]

の更新です。

random extra matching ではまだ直径 5 になりませんでしたが、サンプル miss が 100 個程度まで落ちています。これは、これまでの候補の中ではかなり良いです。

---

### \(H(11)\)：\((16,5,177156)\) 候補

\[
q=11,\quad |P|=12(11^4+11^2+1)=177156.
\]

one-factor 化で次数 12。そこに 4 本の extra matching を加えると、

\[
d=16,\quad n=177156.
\]

現行

\[
N(16,5)\ge132496
\]

を超える候補です。

1 trial の 32-source サンプルでは、半径 5 到達の最悪が

\[
175760/177156
\]

でした。miss は約 1396。まだ失敗ですが、候補としては悪くありません。ただし \(H(9)\) の方がサイズ・検証コスト・miss の小ささのバランスが良いです。

---

## 4. 今回の判断

現時点で最も数学的に勝算があるのは、次です。

\[
\boxed{
H(9)\text{ point graph の line one-factor sparsification}
+
4\text{ structured extra 1-factors}
}
\]

狙いは

\[
\boxed{
(d,k,n)=(14,5,66430)
}
\]

です。

random extra 1-factors ではまだ足りません。ですが、これは「局所修復で bad pair を潰す」段階に進むべきではありません。

次に必要なのは、4 本の extra 1-factor を random に選ぶのではなく、**残っている距離 6 obstruction を覆う finite-geometric covering design として設計すること**です。

具体的には、候補は次のようなものです。

\[
\text{line one-factor base}
+
\text{spread/ovoid/collineation orbit 由来の 4 本の 1-factor}.
\]

あるいは、extra edges も generalized hexagon の collinearity edge に限定し、

\[
\text{remaining point graph から 4 本の幾何的 1-factor を選ぶ}
\]

方が自然です。greedy に collinearity matching を足す実験もしましたが、miss 約 178 で、global random matching よりは少し悪かったです。つまり、単なる「collinear にすればよい」ではなく、obstruction layer を明示的に叩く設計が必要です。

## まとめ

今回の前進は、新記録そのものではなく、候補の整理です。

捨てるべきもの：

\[
A_4(3)+\text{automorphism polarity jumps}
\]

理由：自己同型 jump では半径球が増えず、上界で不可能。

残すべきもの：

\[
H(q)\text{ point graph の line one-factor 化}
\]

特に

\[
\boxed{
H(9)+4\text{ extra 1-factors}
\Rightarrow
(14,5,66430)
}
\]

が次の本命です。random では未達ですが、miss が小さく、記録更新幅も大きい。次は extra 1-factor を「ランダム」ではなく、有限幾何の covering design として構成する方向に絞るべきです。

---

## Turn 058 (Round 013) — 🧑 USER

_2026-05-23 16:13:04 UTC_

続けてください

---

## Turn 059 (Round 013) — 🤖 ASSISTANT

_2026-05-23 16:13:23 UTC_  ·  model: `gpt-5-5-pro`

前回の本命 \(H(9)\) point one-factor + 4 extra 1-factors に絞り、ランダム追加ではなく距離層・余剰辺・残存障害を狙う構造的 1-factor 設計として検証します。まず既存コードと候補データを確認し、失敗の形を数値で切り分けます。

---

## Turn 060 (Round 013) — 🤖 ASSISTANT

_2026-05-23 16:16:40 UTC_  ·  model: `gpt-5-5-pro`

近さが本当に構造的か、単なるランダム正則グラフの被覆限界かをまず判定します。そのうえで、追加辺は大域 involution や collineation/spread 系の候補に絞ります。

---

## Turn 061 (Round 013) — 🤖 ASSISTANT

_2026-05-23 16:25:51 UTC_  ·  model: `gpt-5-5-pro`

遠距離点だけを追加 matching で結ぶ非局所設計を試します。全点の \(R=5\) 前計算は重いので、まず \(R=4\) 制約で効果を判定します。

---

## Turn 062 (Round 013) — 🤖 ASSISTANT

_2026-05-23 16:43:54 UTC_  ·  model: `gpt-5-5-pro`

続けました。今回は **web検索なし**で、前回の \(H(9)\) point graph sparsification をさらに数学的に整理し、「追加 matching を適当に足す」方向から、より有限幾何的な **role-regular star design** に切り替えて試しました。

成果物はこちらです。

[phase8_structured_role_star_artifacts.zip](sandbox:/mnt/data/phase8_structured_role_star_artifacts.zip)

## 結論

今回も、**検証済みの新記録はまだ出ていません**。

ただし、前回の

\[
H(9)\text{ point one-factor} + 4\text{ global matchings}
\]

より、数学的にきれいで、実験的にも少し良い構成族が見つかりました。

本命候補は引き続き

\[
(d,k,n)=(14,5,66430)
\]

です。前回表の現行記録は

\[
N(14,5)\ge 58095
\]

なので、直径 5 を証明できれば

\[
66430-58095=8435
\]

の更新になります。

---

## 新しい構成：role-regular star design

基礎構造は split Cayley generalized hexagon \(H(9)\) の point graph です。

点数は

\[
|P|=(9+1)(9^4+9^2+1)=66430.
\]

各 hexagon line は 10 点を持ち、各点は 10 本の line に乗ります。

今回の構成では、各 line \(L\) 上で次を選びます。

\[
\text{center }1\text{ 点}
\quad+\quad
\text{leaf }7\text{ 点}
\quad+\quad
\text{isolated }2\text{ 点}.
\]

そして、その line 上では center から 7 個の leaf にだけ辺を張ります。つまり line 上の局所グラフは 7-edge star です。

ただし、これを各 line ごとに勝手に選ぶのではなく、全体で次を満たすようにします。

\[
\text{各点は center にちょうど 1 回}
\]

\[
\text{各点は leaf にちょうど 7 回}
\]

\[
\text{各点は isolated にちょうど 2 回}
\]

すると、各点の次数は厳密に

\[
7+7=14
\]

になります。

これは incidence graph の perfect matching を使って作れます。具体的には、point-line incidence graph から

- center 用に 1 本の perfect matching,
- isolated 用に 2 本の disjoint perfect matchings,

を選び、残り 7 本の incidence を leaf とします。

この構成は、前回の「line one-factor + global matching」よりも有限幾何の内部に閉じています。追加の arbitrary edge を外から入れるのではなく、\(H(9)\) の line 構造だけを使って degree 14 のグラフを作ります。

---

## なぜこの方向は筋が良いか

前回の global matching 追加は、結局 random regular graph 的な挙動に近くなっていました。今回の star design は違います。

各辺は必ず generalized hexagon の collinearity edge です。つまり full point graph の直径 3 構造を完全には捨てず、その line clique \(K_{10}\) を 7-edge star に置き換えています。

local graph として star を選ぶ理由もあります。10 色上の 7-edge graph をいくつか試したところ、balanced graph や clique-like graph より、star 型が明らかに良いです。直感的には、line 上で center を経由して多くの色を一気に混ぜられるため、短い path の被覆力が高いです。

---

## 実験結果

### 比較 1：前回型、global matching 4 本

\[
H(9)\text{ line one-factor} + 4\text{ global perfect matchings}
\]

5 trial、1024 始点サンプルでは、最良でも

\[
\text{radius-5 miss}=130
\]

でした。

つまり、サンプル中の最悪始点から距離 5 以内に届かない点が 130 個程度残ります。

### 比較 2：base graph で遠距離の点だけを結ぶ matching

「追加 matching は base graph 距離 \(>4\) の点同士だけにする」という非局所制約も試しました。

結果は

\[
\text{radius-5 miss}\approx 121.
\]

global random より少し良いですが、決定的ではありませんでした。base 距離 \(>5\) 制約は全点前計算が重く、今回の実行範囲では完走できませんでした。

### 比較 3：固定 color graph

incidence edge-coloring を作り、10 色上の 7-edge graph \(F\) に従って各 line 上の点を結ぶ方式も試しました。

結果：

| local color graph | degree | sample miss |
|---|---:|---:|
| 7-edge star | 14 | 約 104〜106 |
| path/cycle 系 | 14 | 約 110〜112 |
| balanced matching + links | 14 | 約 120 |
| \(K_4\)+edge 型 | 14 | 約 1627 |

star 型が最良でした。

### 比較 4：randomized role-regular star

今回の本命です。

\[
\text{center }1,\quad \text{leaf }7,\quad \text{isolated }2
\]

を balanced perfect matching でランダム化した role-star design。

20 trial、256 始点サンプルで最良は

\[
\text{radius-5 miss}=98.
\]

さらに 5 trial、1024 始点サンプルでは最良

\[
\text{radius-5 miss}=103.
\]

これは今回の最良結果です。

前回の global matching 型の robust sample miss が約 130 だったので、role-star design は確かに改善しています。ただし、まだ直径 5 ではありません。

---

## 他パラメータの確認

### \(H(8)\), degree 12, \((12,5)\) 候補

GF(8) 上で \(H(8)\) を生成しました。

\[
|P|=(8+1)(8^4+8^2+1)=37449.
\]

local star の edge 数を 6 にすると次数は

\[
d=12.
\]

もし直径 5 なら

\[
N(12,5)\ge37449
\]

となり、現行 29621 を超えます。

しかし sample miss は約

\[
195
\]

で、直径 5 には届きませんでした。

### \(H(11)\), degree 16, \((16,5)\) 候補

\[
|P|=(11+1)(11^4+11^2+1)=177156.
\]

local star の edge 数を 8 にすると次数は

\[
d=16.
\]

もし直径 5 なら

\[
N(16,5)\ge177156
\]

となり、現行 132496 を超えます。

ただし 32 始点サンプルで

\[
\text{miss}=1167
\]

程度残りました。これはかなり random degree-16 graph 的で、今回の本命からは外します。

---

## 今の判断

今回の best construction は

\[
\boxed{
H(9)\text{ point graph}
+
\text{role-regular 7-star design}
}
\]

です。

候補としては

\[
\boxed{
(d,k,n)=(14,5,66430)
}
\]

です。

この方向は、前回の global matching 追加より良いです。理由は、全ての辺が generalized hexagon の line 構造の中にあり、次数 14 の証明も完全に設計から出るからです。

ただし、まだ sample miss が約 100 残ります。これは「あと 100 点を局所修復すればよい」という意味ではありません。各始点で 100 個程度漏れるなら、全体では bad pair が相当数あるはずで、局所修復や pruning に進むのは筋が悪いです。

## 次に進むべき数学的課題

次は、role-star design をランダム balanced matching で作るのではなく、**高次制約つきの role design** として作るべきです。

現状の role 条件は一次条件だけです。

\[
\text{各点は center 1 回、leaf 7 回、isolated 2 回}
\]

しかし直径 5 を保証するには、おそらくこれだけでは足りません。

必要なのは、任意の point-geodesic

\[
x=p_0,p_1,p_2,p_3=y
\]

に対して、その途中の line 上で center/leaf の役割がうまく並び、長さ 5 以下の star-walk に変換できる、という二次・三次の条件です。

つまり次の問題に落とすべきです。

\[
\boxed{
H(9)\text{ の incidence に center/leaf/isolated role を割り当て、}
}
\]

\[
\boxed{
\text{各 opposite point pair が長さ }5\text{ の star-walk で覆われるようにする}
}
\]

これは局所改善ではなく、有限幾何上の role covering design です。

現時点でのまとめは：

\[
\boxed{
\text{role-regular star design は有望だが、一次バランスだけでは不足}
}
\]

\[
\boxed{
\text{次は geodesic-level の covering 条件を role design に組み込む}
}
\]

です。

---

## Turn 063 (Round 014) — 🧑 USER

_2026-05-24 12:56:06 UTC_

続けてください

---

## Turn 064 (Round 014) — 🤖 ASSISTANT

_2026-05-24 12:56:24 UTC_  ·  model: `gpt-5-5-pro`

まず前回の \(H(9)\) role-star 構成で約100 missが残る原因を距離・geodesic構造として分解します。局所修復ではなく、直径5を保証し得る高次のrole割当条件へ絞って検証します。

---

## Turn 065 (Round 014) — 🤖 ASSISTANT

_2026-05-24 12:59:38 UTC_  ·  model: `gpt-5-5-pro`

約100 miss はランダム被覆限界に近いので、試行回数ではなく半径5球の衝突を減らす設計へ切り替えます。距離3 geodesicを、line内コストが高々1回だけ2になるstar-walkへ変換できる二次条件として実装します。

---

## Turn 066 (Round 014) — 🤖 ASSISTANT

_2026-05-24 13:08:55 UTC_  ·  model: `gpt-5-5-pro`

少し方向を広げ、\(H(5)\) の小型 star-sparsification と、generalized quadrangle の point graph を line matching で薄くして直径3を狙う新候補を並行して検証します。

---

## Turn 067 (Round 014) — 🤖 ASSISTANT

_2026-05-24 13:22:31 UTC_  ·  model: `gpt-5-5-pro`

進めました。今回は、前回の \(H(9)\) role-star 案をもう少し深掘りしつつ、別の数学的候補として generalized quadrangle 方向も試しました。

成果物はこちらです。

[phase9_role_analysis_artifacts.zip](sandbox:/mnt/data/phase9_role_analysis_artifacts.zip)

## 結論

今回も **検証済みの新記録は出ていません**。

ただし、かなり重要な整理ができました。

前回の最有望候補だった

\[
H(9)\text{ point graph}
+
\text{role-regular 7-star design}
\]

は、数値的にはまだ一番近いです。しかし、今回の full scan と bad-pair 解析から、**この候補を pruning や軽い改良で新記録にするのは見込み薄**だと判断しました。

また、新しく試した generalized quadrangle の line-sparsification は、数学的にはかなり自然な候補でしたが、実験的には明確に弱かったです。こちらも捨てます。

---

## 1. \(H(9)\) role-star の完全検査

前回の候補は、

\[
|P|=66,430,\qquad d=14,\qquad k=5
\]

を狙うものでした。現行記録

\[
N(14,5)\ge 58,095
\]

を超えるには、直径 5 を証明できればよい。

5 trial / 1024 始点サンプルで最良だった候補を full scan しました。

結果：

\[
\min_{v}|B_5(v)|=66,314,
\]

つまり最大 miss は

\[
66,430-66,314=116.
\]

平均到達数は

\[
66,352.8
\]

でした。

かなり近いですが、直径 5 ではありません。

---

## 2. pruning は見込み薄

この候補について、距離 5 を超える点対を bad edge とする bad-pair graph を作りました。

結果：

\[
\text{bad edges}=2,563,896,
\]

\[
\text{average bad degree}=77.19,
\]

\[
\text{maximum bad degree}=116.
\]

さらに greedy で bad-pair graph の independent set を取ると、得られたサイズは

\[
4,217
\]

程度でした。

つまり、「少し頂点を削れば 58,095 頂点以上の直径 5 induced subgraph が残る」という状況ではまったくありません。bad pair は局所的な少数の穴ではなく、全体に広く分布しています。

したがって、この候補に対して

\[
66,430 \to 58,096+
\]

の pruning で記録更新を狙う方向は捨てます。

---

## 3. role-star の経路構造も単純ではない

次に、role-star の成功経路が「full point graph の長さ 3 geodesic を、star の長さ 5 以下に変換しているだけなのか」を調べました。

比較したグラフは次の 3 つです。

1. 本来の role-star graph、半径 5。
2. isolated incidence だけを除き、active 点同士は line 上で clique にする graph、半径 3。
3. center-leaf edge だけで長さ 3 を見る graph。

\(H(9)\) で 10 trial / 512 始点サンプルを取ると、典型値は：

| graph | 半径 | sample miss |
|---|---:|---:|
| role-star | 5 | 96〜109 |
| active clique | 3 | 約 8,400 |
| center-edge only | 3 | 約 63,875 |

これはかなり重要です。

role-star の距離 5 パスは、単純に

\[
\text{full point graph の長さ 3 geodesic}
\]

を置き換えているだけではありません。むしろ、疎グラフ内で 4〜5 step の迂回を使って、かなり global に混ざっています。

したがって、「geodesic ごとに center/leaf/isolate role を調整する」という前回の次案も、思ったより直接的には効かない可能性が高いです。

---

## 4. 新候補：generalized quadrangle の point graph sparsification

次に、別の有限幾何として symplectic generalized quadrangle

\[
W(3,q)
\]

を試しました。

これは点数

\[
|P|=(q+1)(q^2+1)
\]

を持ち、full point graph は直径 2 です。

ここで各 line clique を疎化して直径 3 を狙う。これはサイズ感としてかなり良く、例えば：

| \(q\) | 候補次数 | 頂点数 | 狙う記録 |
|---:|---:|---:|---|
| 5 | 6 | 156 | \(N(6,3)>111\) |
| 7 | 8 | 400 | \(N(8,3)>253\) |
| 11 | 12 | 1,464 | \(N(12,3)>786\) |
| 13 | 14 | 2,380 | \(N(14,3)>916\) |

特に

\[
q=13,\quad d=14,\quad n=2,380
\]

は Moore bound

\[
M(14,3)=1+14+14\cdot13+14\cdot13^2=2,563
\]

のかなり近くにあり、もし直径 3 なら非常に強い候補でした。

---

## 5. generalized quadrangle 実験結果

まず、各 GQ line 上の clique を perfect matching に置き換える構成を試しました。

結果：

| 構成 | 候補 | 結果 |
|---|---:|---|
| \(W(3,5)\), line matching | \((6,3,156)\) | best sample miss 53 |
| \(W(3,7)\), line matching | \((8,3,400)\) | best sample miss 139 |

かなり遠いです。

次に、line 上で role-star を使いました。つまり各 line で center を 1 点選び、約半分を leaf、残りを isolated にする。各点が center / leaf / isolated として balanced になるようにして、次数を制御します。

結果：

| 構成 | 候補 | 結果 |
|---|---:|---|
| \(W(3,5)\), star | \((6,3,156)\) | full max miss 45 |
| \(W(3,7)\), star | \((8,3,400)\) | full max miss 129 |
| \(W(3,11)\), star | \((12,3,1464)\) | best sample miss 479 |
| \(W(3,13)\), star | \((14,3,2380)\) | best sample miss 787 |

こちらも失敗です。

generalized quadrangle の full point graph は直径 2 なので、一見ものすごく有利に見えます。しかし line-local sparsification で次数を落とすと、短距離の被覆力が一気に落ちます。これは \(H(9)\) よりさらに厳しいです。

---

## 6. linear symplectic map 案も試したが弱い

もう少し代数的な GQ 構成も試しました。

\(\mathbb F_q^4\) の symplectic form を \(\langle x,y\rangle\) とし、

\[
\langle x,Ax\rangle=0
\quad\text{for all }x
\]

を満たす可逆線形写像 \(A\) を選ぶ。すると各 projective point \(x\) は、collinear な点 \(Ax\) に送られます。

このような \(A\) を複数選んで、

\[
x\sim A_i x
\]

で辺を張る。これは line-local ではなく、より global な代数的 sparse graph です。

しかし、ランダムな skew-symmetric form 由来の写像では展開が悪く、結果は：

| 構成 | 結果 |
|---|---:|
| \(q=5\), 3 maps, degree \(\le6\) | best sample miss 83 |
| \(q=7\), 4 maps, degree \(\le8\) | best sample miss 206 |

写像間の重複や不均一な軌道が多く、期待したような near-Moore 展開にはなりませんでした。

この方向は、単なるランダム線形写像ではなく、かなり強い代数的選択原理がないと厳しいです。

---

## 現在の判断

今回でかなりはっきりしました。

### 捨てる方向

\[
\boxed{
\text{line-local sparsification}
}
\]

は基本的に弱いです。

これは \(H(9)\) でも \(W(3,q)\) でも同じでした。full geometry の line/residue 構造は強いですが、次数制約のために line 内で少数の辺だけ残すと、距離球が random regular threshold 付近で止まります。

特に \(H(9)\) role-star は数値的には惜しいものの、bad-pair graph が大きすぎるので、局所修復・pruning・軽い role 調整では届きそうにありません。

### 残すべき方向

次は、辺を line residue の中に閉じ込めるのではなく、**最初の 1 step から有限幾何全体を混ぜる大域的写像**を使うべきです。

形としては：

\[
\boxed{
\text{finite geometry の点集合}
+
\text{少数の明示的な大域 permutation / correspondence}
}
\]

ただし、単なる Cayley/Schreier graph ではなく、写像自体に

\[
\text{距離層を均一に横断する}
\]

という幾何条件を課す必要があります。

今回の反省から、次に狙うべき条件は：

\[
\boxed{
\text{各 generator が local residue ではなく、opposition / far layer / polar layer を均一に切る}
}
\]

です。

現時点で一番近かった候補は依然として

\[
H(9)\text{ role-star},\quad (14,5,66430)
\]

ですが、構成原理としては限界が見えました。次は line-local から完全に離れて、**global finite-geometric correspondence graph** に切り替えるのが筋だと思います。

---

## Turn 068 (Round 015) — 🧑 USER

_2026-05-24 14:00:45 UTC_

続けてください

---

## Turn 069 (Round 015) — 🤖 ASSISTANT

_2026-05-24 14:01:05 UTC_  ·  model: `gpt-5-5-pro`

ここからは line-local 疎化を捨て、遠距離層・極性層を最初の一歩から横断する global correspondence 型に絞ります。候補は数式で固定し、計算は条件を満たす小さな構造族の検証だけに使います。

---

## Turn 070 (Round 015) — 🤖 ASSISTANT

_2026-05-24 14:04:16 UTC_  ·  model: `gpt-5-5-pro`

まず分岐量と距離球被覆の必要条件を先に確認し、小さく完全検証できる候補から進めます。利用可能な \(H(q)\) 生成・BFS コードを再利用して候補を絞ります。

---

## Turn 071 (Round 015) — 🤖 ASSISTANT

_2026-05-24 14:22:25 UTC_  ·  model: `gpt-5-5-pro`

\(H(9)\) の opposition one-factor は role-star を上回らず、random regular 的な限界に近い挙動でした。一方で \((16,2)\) の polarity graph は辺削除も含めて再検討しています。

---

## Turn 072 (Round 015) — 🤖 ASSISTANT

_2026-05-24 14:31:52 UTC_  ·  model: `gpt-5-5-pro`

続けました。今回は「global finite-geometric correspondence」に切り替えて、line-local ではない候補をいくつか検査しました。

成果物はこちらです。

[phase10_global_correspondence_artifacts.zip](sandbox:/mnt/data/phase10_global_correspondence_artifacts.zip)

## 結論

今回も **検証済みの新記録は出ていません**。

ただし、かなり大事な構造的整理ができました。特に、

\[
\text{generalized polygon を少し削って次数を下げる}
\]

という方向は、かなり強い理由で捨てるべきです。これは単なる実験失敗ではなく、**girth による obstruction** があります。

一方で、global な opposite correspondence も試しましたが、これは random regular graph 的な被覆限界を超えませんでした。

---

## 1. H(q) point set 上の opposite permutation graph

前回の結論は、

\[
\text{line-local sparsification は弱い}
\]

でした。そこで今回は、辺を line/residue 内に閉じ込めず、最初から generalized hexagon の **遠方層**を横断する写像だけを使いました。

構成はこうです。

split Cayley generalized hexagon \(H(q)\) の point set \(P\) を取ります。点グラフ距離 3、つまり incidence graph 距離 6 の点同士を **opposite** と呼ぶ。

いくつかの全単射

\[
f_i:P\to P
\]

を選び、各点 \(p\) について

\[
f_i(p)\text{ is opposite to }p
\]

となるようにします。そして辺

\[
p\sim f_i(p)
\]

を無向辺として入れる。1 つの permutation は最大次数 2 を使うので、\(r\) 本の permutation で最大次数は \(2r\) です。

これは line-local ではなく、

\[
\boxed{
\text{far-layer / opposition-layer correspondence graph}
}
\]

です。

---

## 2. opposite permutation の実験結果

### \(H(9)\), \(r=7\), \((d,k,n)=(14,5,66430)\) 候補

\[
|P|=66,430,\qquad d\le14.
\]

直径 5 なら、前回表の現行記録

\[
N(14,5)\ge58,095
\]

を

\[
66,430-58,095=8,335
\]

更新します。

しかし、256 始点サンプルでの最良は

\[
\text{radius-5 miss}=141
\]

でした。以前試した far matching / arbitrary global matching 系もだいたい miss \(126\sim141\) で、前回の role-star best の約 \(100\) より悪いです。

つまり、**opposite layer に飛ばすだけでは足りません**。

### \(H(8)\), \(r=6\), \((d,k,n)=(12,5,37449)\) 候補

\[
|P|=37,449,\qquad d\le12.
\]

直径 5 なら、現行

\[
N(12,5)\ge29,621
\]

を超えます。

しかし、256 始点サンプルで最良

\[
\text{radius-5 miss}=258
\]

でした。こちらも直径 5 から遠いです。

### 判断

opposite permutation は数学的には自然でしたが、挙動はほぼ random regular graph です。  
「辺を遠方に張る」だけでは、半径 5 ball の衝突を十分には制御できません。

---

## 3. generalized hexagon incidence graph の次数削減は構造的に無理

これは今回一番重要な発見です。

一見、有望に見える案がありました。

\(H(q)\) の incidence graph は

\[
(q+1)\text{-regular},\qquad \operatorname{diam}=6.
\]

たとえば \(H(8)\) は degree 9, diameter 6, 頂点数

\[
2(9)(8^4+8^2+1)=74,898.
\]

もしここから 1-factor を消して degree 8 に落としても diameter 6 が保てれば、

\[
N(8,6)\ge74,898
\]

となり、現行 \(39,672\) を大きく超えます。

そこで \(H(7)\) で incidence edge-coloring の 1 色を削除して試しました。結果は全くダメでした。

\[
H(7):\quad n=39,216,\quad d=7
\]

で、半径 6 サンプル到達は約

\[
27,500/39,216
\]

程度に落ちました。

これは偶然ではありません。

---

## 4. girth obstruction

generalized hexagon の incidence graph は girth 12 です。

したがって、辺 \(uv\) を削除し、両端 \(u,v\) を残したとします。もし削除後も

\[
\operatorname{dist}(u,v)\le6
\]

なら、削除前の辺 \(uv\) とその代替 path を合わせて、長さ高々 7 の cycle ができます。

しかし girth は 12 なので不可能です。

つまり、

\[
\boxed{
\text{incidence graph の辺を 1 本でも削り、その両端を残すと diameter 6 は壊れる}
}
\]

です。

さらに、頂点削除にも同じ問題があります。削除した頂点 \(z\) に、残った隣接点 \(u,v\) が 2 つあるとします。削除前は

\[
u-z-v
\]

で距離 2 でした。削除後に \(u,v\) が距離 6 以下でつながるなら、長さ高々 8 の cycle ができます。これも girth 12 に反します。

したがって、

\[
\boxed{
\text{削除された各頂点は、残存グラフに高々 1 個しか隣接点を持てない}
}
\]

必要があります。

これは非常に強い制約です。たとえば \(H(q+1)\) から頂点を少し削って degree \(q\) に落とす、という発想はほぼ死にます。残す頂点を \(R\)、削る頂点を \(D\) とすると、次数を下げるには各 \(R\) 頂点が \(D\) に隣接する必要があります。一方、上の条件から各 \(D\) 頂点は高々 1 個の \(R\) 頂点しか助けられません。

つまり

\[
|D|\ge |R|
\]

級の削除が必要になり、頂点数は少なくとも半分以下に落ちます。たとえば \(H(8)\) なら半分は

\[
74,898/2=37,449
\]

で、現行の

\[
N(8,6)\ge39,672
\]

を下回ります。

なので、

\[
\boxed{
\text{generalized hexagon incidence graph の削除・辺削除による次数削減は本命から外す}
}
\]

べきです。

---

## 5. 直径 2 の strongly regular graph 路線も整理

別方向として、\((16,2)\) の strongly regular graph パラメータを調べました。

現行記録は

\[
N(16,2)\ge200.
\]

degree 16, diameter 2 の strongly regular graph で 200 を超える可能性があるパラメータを調べると、唯一残るのは

\[
\operatorname{srg}(209,16,3,1)
\]

だけでした。

しかしこれは存在できません。

理由は局所構造です。このグラフが存在すると、任意の頂点 \(x\) の近傍グラフは 16 頂点 3-regular になります。また、

- 近傍グラフ内の隣接ペアは共通近傍を 2 個持つ。
- 近傍グラフ内の非隣接ペアは共通近傍を持たない。

したがって近傍グラフは

\[
4K_4
\]

でなければなりません。

すると元グラフでは、各頂点は 4 個の \(K_5\) に属し、各辺は一意の \(K_5\) に属します。よって \(K_5\) との incidence を数えると

\[
\frac{209\cdot4}{5}
\]

個の \(K_5\) が必要になりますが、これは整数ではありません。

したがって

\[
\boxed{\operatorname{srg}(209,16,3,1)\text{ は存在しない}}
\]

です。少なくとも strongly regular graph で \((16,2)\) を 200 超にする道は閉じました。

---

## 現時点の判断

今回でかなりはっきりしました。

### 捨てる方向

\[
\boxed{
\text{generalized polygon の edge/vertex thinning}
}
\]

これは girth obstruction でダメです。

\[
\boxed{
\text{opposite layer への random/global correspondence}
}
\]

これも、単に far layer を使うだけでは random regular graph の被覆限界から出ません。

\[
\boxed{
\text{diameter 2 strongly regular graph での }d=16\text{ 更新}
}
\]

唯一の候補パラメータが消えます。

---

## 次に進むべき構成方針

次は、単なる thinning でも random correspondence でもなく、**距離球の被覆を座標レベルで証明できる correspondence**が必要です。

今後の本命条件はこれです。

\[
\boxed{
\text{各 generator / correspondence が far layer を使うだけでなく、}
}
\]

\[
\boxed{
\text{長さ }k\text{ の path 式が全 target 座標を一意または少数重複で解く}
}
\]

つまり、random-like expansion ではなく、**near-Moore covering identity** を持つ構成です。

現時点で一番筋が良い次候補は、generalized hexagon の root group 座標を使い、point set または chamber set 上に

\[
(a_1,\ldots,a_m)
\mapsto
M_i(a_1,\ldots,a_m)+b_i
\]

型の少数の semilinear correspondences を置く方向です。  
ただし、これは Cayley graph 生成集合探索に落ちるとダメなので、単なる群作用ではなく、

\[
\text{opposition cell の座標変換}
+
\text{通常 incidence move の座標変化}
\]

を組み合わせて、長さ 5 の到達方程式が全座標を覆うことを証明する形にすべきです。

今回の進展は、「惜しい候補」よりもむしろ、**どの自然な有限幾何操作が原理的にダメか**を切り分けられたことです。次は root-coordinate covering identity に絞るのがよいです。

---

## Turn 073 (Round 016) — 🧑 USER

_2026-05-24 14:33:27 UTC_

続けてください

---

## Turn 074 (Round 016) — 🤖 ASSISTANT

_2026-05-24 14:33:46 UTC_  ·  model: `gpt-5-5-pro`

方針を root-coordinate / near-Moore covering identity に絞り、既存候補が random-like に止まる理由を距離球サイズで再評価します。そのうえで、証明可能な到達式を持つ最小候補だけを検証します。

---

## Turn 075 (Round 017) — 🧑 USER

_2026-05-24 14:38:51 UTC_

- [重要]文献の中に本質的に含まれていないアイデアで解の構成を試みてください。既存の方法を組み合わせる、パラメータを増やす、使う代数系を変えるだけ、既存の解に対して新しくない方法で局所探索する、等はNGです
上記に加えて次も禁止します
- [禁止]数学者ならすぐに思いつく方法や概念から単純に構成を試してみるようなアプローチ

数学者であってもすぐには思いつかないような、本質的に新しいアプローチであり、かつ、効率よく辺が頂点間を接続されていることが数学的に事前に直感できるようなアプローチを開発してください。その上で、そのアプローチをメインとして、サブで既存の方法を使用するのはOKです。

一度立ち止まって、方針を検討してください。

---

## Turn 076 (Round 017) — 🤖 ASSISTANT

_2026-05-24 14:39:20 UTC_  ·  model: `gpt-5-5-pro`

ここで強めにリセットし、候補の改良ではなく構成原理自体を作り直します。自然な有限幾何の疎化・折り畳み・遠方対応ではなく、距離球の無駄そのものを設計対象にします。

---

## Turn 077 (Round 017) — 🤖 ASSISTANT

_2026-05-24 14:42:27 UTC_  ·  model: `gpt-5-5-pro`

今回は実装や探索に戻らず、“なぜ勝てるはずか”を先に説明できる候補だけに絞ります。既存発想の延長に見える自然操作は主役から外します。

---

## Turn 078 (Round 017) — 🤖 ASSISTANT

_2026-05-24 14:54:46 UTC_  ·  model: `gpt-5-5-pro`

了解です。ここで方針を大きく変えます。

前回までの候補は、どれも結局、

\[
\text{既知の良い構造を薄くする}
\quad\text{or}\quad
\text{遠方層に辺を足す}
\]

でした。これは数学者なら自然に考える方向です。今回の追加条件に照らすと、もう本命にしません。

次の本命は、**頂点上でグラフを作るのではなく、非戻り歩道の状態空間を先に設計し、それをあとから頂点へ折り畳む**という方針です。

私はこれを仮に

\[
\boxed{\text{Hashimoto--de Bruijn packet construction}}
\]

と呼びます。

---

## 核心：Moore bound は「頂点」ではなく「非戻り歩道」の数から来る

最大次数 \(d\) の無向グラフで、ある頂点から長さ \(k\) 以内に行ける頂点数の Moore bound は

\[
1+d+d(d-1)+\cdots+d(d-1)^{k-1}.
\]

ここで本当に重要なのは、最初の一歩の後は、毎回

\[
d-1
\]

通りの **非戻り選択** があることです。

つまり degree-diameter problem で効率のよいグラフを作るには、頂点集合そのものよりも、まず

\[
\text{有向辺、つまり oriented edge 上の非戻りダイナミクス}
\]

を効率よく設計するべきです。

通常の構成は頂点に辺を張ってから距離を見る。しかし新方針では逆にします。

1. まず oriented edge を状態とする非戻りオートマトンを作る。
2. そのオートマトンが de Bruijn 的に高速同期するようにする。
3. その状態集合を \(d\) 個ずつ packet 化して、無向 \(d\)-正則グラフの頂点にする。
4. packet 化がうまくいけば、直径証明は de Bruijn 型の同期性から出る。

これは Cayley graph でも voltage lift でも finite geometry thinning でもありません。頂点でなく **Hashimoto graph**、つまり非戻り歩道グラフを主対象にします。

---

## なぜ勝算があるか

無向 \(d\)-正則グラフ \(G\) の Hashimoto graph \(H(G)\) を考えます。

\(H(G)\) の頂点は \(G\) の oriented edge で、

\[
(u,v)\to(v,w)\qquad(w\ne u)
\]

を有向辺とします。

この \(H(G)\) は \((d-1)\)-out-regular です。  
したがって、Moore bound の分岐構造そのものは \(H(G)\) 側にあります。

既存の構成は多くの場合、頂点上の隣接を直接設計します。そのため、非戻り歩道の分岐が衝突して、半径球が random regular graph 的に途中で潰れます。

今回の発想は逆です。

\[
H(G)\text{ に de Bruijn shift のような高効率同期構造を埋め込む}
\]

ように \(G\) を作る。

de Bruijn shift は、各ステップで古い記号を捨て、新しい記号を入れることで、短い長さで全状態を覆う構造です。 directed graph では古典的ですが、そのまま無向グラフに使うと入次数・出次数で degree が倍になります。

ここでの新規点は、

\[
\text{de Bruijn dynamics を頂点ではなく oriented edge 上に置く}
\]

ことです。無向グラフの「前の辺には戻れない」という制約が、ちょうど de Bruijn shift の forward branching として働きます。これは degree budget をかなり効率よく使えます。

---

## 第一ターゲット

最初に狙うべきは

\[
\boxed{(d,k)=(16,4)}
\]

です。

現行記録は前回表で

\[
N(16,4)\ge 14640.
\]

今回の構成候補では、まず alphabet size

\[
q=12
\]

を使います。次数 \(16\) の非戻り選択数は \(15\) ですが、そのうち \(12\) 本を de Bruijn data ports として使い、残り \(3\) 本を packet 整合用の reserve ports として使う。

word length は

\[
m=k+1=5.
\]

oriented edge 状態を

\[
A^5,\qquad |A|=12
\]

とします。状態数は

\[
12^5=248832.
\]

これを \(16\) 個ずつ packet 化して頂点にすると、

\[
n=\frac{12^5}{16}=15552.
\]

したがって、構成が成功すれば

\[
\boxed{N(16,4)\ge15552}
\]

となり、現行 14640 を

\[
15552-14640=912
\]

更新します。

これは巨大更新ではありませんが、最初の proof-of-concept として非常に良いです。  
理由は、\(q=12\) だと reserve ports が 3 本あり、packet 整合に余裕があるからです。

---

## 同じ構成の本命ターゲット

同じ考えで

\[
k=5,\quad m=6
\]

にすると、

\[
n=\frac{12^6}{16}=186624.
\]

現行記録は

\[
N(16,5)\ge132496.
\]

したがって、成功すれば

\[
\boxed{N(16,5)\ge186624}
\]

で、

\[
186624-132496=54128
\]

の更新です。

さらに攻めるなら \(q=14\) もあります。

\[
q=14,\quad d=16,\quad k=4
\Rightarrow
n=\frac{14^5}{16}=33614,
\]

\[
q=14,\quad d=16,\quad k=5
\Rightarrow
n=\frac{14^6}{16}=470596.
\]

ただし \(q=14\) は reserve port が 1 本しかなく、構成条件がかなり硬いです。最初は \(q=12\) で新記録を狙う方が数学的に健全です。

---

## 構成の具体像

状態集合を

\[
\Omega=A^m
\]

とします。ここで \(m=k+1\)。

状態

\[
w=(w_1,\dots,w_m)
\]

に対して、de Bruijn shift は

\[
T_a(w)=(w_2,w_3,\dots,w_m,a),
\qquad a\in A.
\]

これが data port です。

もし長さ \(k\) の道を使うなら、最初の oriented edge を選んだあと、残り \(k-1=m-2\) 回の shift で新しい記号を入れられます。

つまり、ある source 状態 \(w\) から target 状態 \(z\) に行くには、最後の 2 記号だけが一致していればよい。

\[
(w_{m-1},w_m)=(z_1,z_2).
\]

残りの

\[
z_3,\dots,z_m
\]

は shift の入力として順に入れればよい。

ここが勝算の核心です。

直径 \(k=m-1\) を保証するには、各 source packet \(X\) と target packet \(Y\) について、

\[
X\text{ の suffix-2 集合}
\]

と

\[
Y\text{ に入る incoming arc の prefix-2 集合}
\]

が必ず交わればよい。

つまり、packet \(X\) に対して

\[
S(X)=\{(w_{m-1},w_m): w\in X\},
\]

target 側の incoming packet に対して

\[
P(Y)=\{(z_1,z_2): z\in Y_{\mathrm{in}}\},
\]

を定義し、

\[
\boxed{
S(X)\cap P(Y)\ne\varnothing
\quad\text{for all packets }X,Y
}
\]

を満たすように packet 化する。

この条件が入ると、直径証明は局所探索なしに出ます。

---

## packet design の直感

ここで面白いのは、suffix-2 と prefix-2 の universe が

\[
A^2
\]

であることです。

\(q=12\) なら universe size は

\[
12^2=144.
\]

packet size は 16 です。

一見、16 個の点だけで 144 点 universe を制御するのは難しそうですが、suffix 側と prefix 側を別の方向の transversal にすればよい。

例えば \(A^2\) を \(12\times12\) grid と見ます。

- source packet の suffix-2 集合は「行」を全部含む。
- target incoming packet の prefix-2 集合は「列」を全部含む。

すると任意の行と任意の列は必ず 1 点で交わります。

\[
\text{row}\cap\text{column}\ne\varnothing.
\]

これにより、任意の source packet と target packet の間で、de Bruijn 同期に必要な 2-symbol match が保証されます。

packet size 16 なので、1 packet の中で 12 個の行/列要素を全部カバーしつつ、残り 4 個を reserve/整合用に使えます。  
これは \(q=12,d=16\) を最初のターゲットにする理由でもあります。

---

## 無向グラフとして実現する条件

ここまでだと、まだ「oriented edge 状態の設計」です。  
これを本当に無向 \(16\)-正則グラフにするには、次が必要です。

状態集合 \(\Omega=A^m\) を 16 個ずつ packet に分ける：

\[
\mathcal P=\{X_1,\dots,X_n\}.
\]

各 packet が無向グラフの頂点になります。

さらに fixed-point-free involution

\[
\iota:\Omega\to\Omega
\]

を作ります。これは oriented edge の反転に対応します。

状態 \(w\in X\) は、無向グラフでは頂点 \(X\) から頂点 \(\mathcal P(\iota(w))\) へ向かう oriented edge です。

非戻り遷移が de Bruijn shift を含むためには、各 \(w\) について

\[
\{T_a(w):a\in A\}
\]

が、反転先 vertex の outgoing packet の中に入っていなければいけません。次数 16 で data ports が 12 本なので、残りは

\[
16-1-12=3
\]

本の reserve states です。

つまり必要条件は概念的に

\[
\boxed{
\mathcal P(\iota(w))
=
\{\iota(w)\}
\cup
\{T_a(w):a\in A\}
\cup
\text{3 reserve states}
}
\]

です。

これが満たされると、完成した無向グラフの Hashimoto graph には、\(12\)-ary de Bruijn shift が data subdynamics として埋め込まれます。

そして前述の prefix/suffix packet 条件があれば、直径 \(k\) が証明できます。

---

## これはなぜ「単純な既存手法」ではないか

de Bruijn graph そのものを使うわけではありません。  
それだと directed になり、無向化すると degree が倍になって弱いです。

Cayley graph でもありません。  
頂点上に一様な generator を作用させるのではなく、oriented edge の非戻り状態に shift dynamics を置き、頂点はその状態の packet として後から現れます。

voltage lift でもありません。  
小さい base graph を群で lift するのではなく、非戻り歩道空間を先に設計し、それを反転 involution で無向グラフへ折り畳みます。

有限幾何 thinning でもありません。  
既存の距離正則構造を薄くするのではなく、Moore bound の分岐そのものを再現するために Hashimoto dynamics を設計します。

この発想の中心は、

\[
\boxed{
\text{頂点ではなく oriented edge を情報担体にする}
}
\]

ことです。  
これは degree-diameter problem の Moore bound の由来と直接噛み合っています。

---

## 研究計画としての次の一手

次は、ランダム探索ではなく、次の有限設計問題を解きます。

### Step 1：packet memory design

\[
A^5
\]

を 16 個ずつ packet 化し、各 packet が

- suffix-2 側ではある row を全部覆う。
- incoming prefix-2 側ではある column を全部覆う。

ようにする。

これは比較的作りやすいはずです。  
各 packet は 16 words あり、row/column の 12 要素を覆う余裕があります。

### Step 2：shift-compatibility design

各状態 \(w\) について、

\[
\{T_a(w):a\in A\}
\]

が 1 つの packet の中にまとまるように、packet と involution \(\iota\) を同時に設計する。

ここが本質的な難所です。  
ただし \(q=12\) では reserve states が 3 個あるので、完全 de Bruijn よりかなり柔軟です。

### Step 3：直径証明

packet design ができれば、BFS は確認用に使います。  
本当の証明は、

\[
S(X)\cap P(Y)\ne\varnothing
\]

と de Bruijn shift の同期性から出します。

### Step 4：最初の記録候補

まず

\[
\boxed{(16,4,15552)}
\]

を狙う。

これが通れば、同じ設計を \(m=6\) に拡張して

\[
\boxed{(16,5,186624)}
\]

を狙う。

---

## 現時点の判断

次に本命にする方針はこれです。

\[
\boxed{
\text{Hashimoto--de Bruijn packet construction}
}
\]

狙いはまず

\[
\boxed{N(16,4)\ge15552}
\]

です。

この方向には、少なくとも次の数学的な勝算があります。

1. Moore bound の \(d(d-1)^{k-1}\) 分岐を、頂点ではなく非戻り状態で直接使う。
2. de Bruijn shift により、長さ \(k\) の path が target code をほぼ直接書き込む。
3. packet の prefix/suffix 交差条件により、任意の source/target 間の同期点を保証できる。
4. \(q=12,d=16\) では 3 本の reserve port があり、無向実現条件に余裕がある。
5. 成功すれば、既存記録を小さくても確実に超える。さらに \(k=5\) では大幅更新が見える。

これまでの有限幾何 thinning や opposition matching と違って、「なぜ短距離で全体を覆えるはずか」が path coding のレベルで見えています。  
次に進めるなら、この packet/involution 設計を実際に構成するフェーズに入ります。

---

## Turn 079 (Round 018) — 🧑 USER

_2026-05-24 15:13:59 UTC_

進めてください

---

## Turn 080 (Round 018) — 🤖 ASSISTANT

_2026-05-24 15:14:19 UTC_  ·  model: `gpt-5-5-pro`

進めます。まず新方針を無向グラフとして実現できる条件に落とし、自己矛盾の有無を確認してから小型プロトタイプと \((16,4)\) 候補を検証します。

---

## Turn 081 (Round 018) — 🤖 ASSISTANT

_2026-05-24 15:17:32 UTC_  ·  model: `gpt-5-5-pro`

候補を探して直すのではなく、packet と反転写像の同時成立を小さな設計問題として解き、破綻するならそこで設計を修正します。

---

## Turn 082 (Round 018) — 🤖 ASSISTANT

_2026-05-24 15:38:53 UTC_  ·  model: `gpt-5-5-pro`

進めました。今回はかなり大事な結果が出ました。**前回の Hashimoto–de Bruijn packet 案の素朴版は、構成探索以前に数え上げで不可能**でした。

成果物はこちらです。

[phase11_hashimoto_packet_artifacts.zip](sandbox:/mnt/data/phase11_hashimoto_packet_artifacts.zip)

## 結論

まだ新記録グラフは出ていません。

ただし、これは単なる失敗ではなく、方針のどこが本質的に無理かを切り分けられました。

前回の案は、

\[
\text{oriented edge state}=\Omega=A^m
\]

を作り、各状態

\[
w=(w_1,\dots,w_m)
\]

からの de Bruijn shift

\[
T_a(w)=(w_2,\dots,w_m,a)
\]

を reverse packet の中に全部入れる、というものでした。

しかしこれは、\(d=16,q=12\) では不可能です。

---

## 1. 致命的 obstruction：fan-packing 条件

shift successor の集合

\[
F_s=\{(s_1,\dots,s_{m-1},a):a\in A\}
\]

を fan と呼ぶことにします。各 fan はサイズ \(q\) で、\(\Omega=A^m\) を

\[
q^{m-1}
\]

個の disjoint fan に分割します。

前回案では、各 fan 全体が 1 つの packet に入っている必要があります。packet サイズは \(d\) なので、1 packet に入る fan の数は高々

\[
\left\lfloor \frac{d}{q}\right\rfloor
\]

です。

一方、packet 数は

\[
\frac{|\Omega|}{d}=\frac{q^m}{d}.
\]

したがって必要条件は

\[
\frac{q^m}{d}
\ge
\frac{q^{m-1}}{\lfloor d/q\rfloor}.
\]

整理すると、

\[
\boxed{
q\left\lfloor\frac dq\right\rfloor\ge d
}
\]

です。

ところが

\[
d=16,\quad q=12
\]

では

\[
12\left\lfloor\frac{16}{12}\right\rfloor=12<16.
\]

つまり、**前回の exact de Bruijn fan embedding は不可能**です。

さらに \(d=16\) では、この条件を満たす \(q<16\) は

\[
q=2,4,8
\]

だけです。\(q=8\) だと state 数が小さすぎて、\((16,4)\) や \((16,5)\) の記録候補としては弱いです。

ここで、前回の構成はそのままでは撤退です。

---

## 2. 修正版：feedback-shift factor を試した

完全 fan を packet に入れるのは無理なので、より弱いがまだ Hashimoto/de Bruijn 的な構成を試しました。

頂点を \(q\)-ary word

\[
(x_1,\dots,x_L)\in A^L
\]

にします。右 shift

\[
(x_1,\dots,x_L)\mapsto(x_2,\dots,x_L,a)
\]

のうち一部だけを選び、無向化します。

狙いは

\[
q=12,\quad L=4,\quad n=12^4=20,736,
\]

\[
d\le16,\quad k=4.
\]

直径 4 なら、

\[
N(16,4)\ge20,736
\]

となり、現行

\[
14,640
\]

を **+6,096** 更新できます。

### 試した構成 A：symbol-circulant filter

固定された 8-element subset

\[
S\subset \mathbb Z/12\mathbb Z
\]

を取り、

\[
a-x_1\in S
\]

のときだけ右 shift edge を残す。

これは directed de Bruijn graph の 8-in/8-out factor になり、無向化後は完全に

\[
16\text{-regular}
\]

になります。

全ての

\[
\binom{11}{8}=165
\]

個の非零差分集合 \(S\) を試しました。

結果は悪いです。最良でも 50 始点サンプルで radius 4 からの miss が

\[
10,475
\]

程度ありました。つまり 20,736 頂点中、半分近くが届いていません。

### 試した構成 B：tail-dependent feedback permutations

次に、もっと非線形にしました。

各 tail

\[
t=(x_2,\dots,x_L)
\]

ごとに alphabet の permutation

\[
\pi_t
\]

をランダムに選び、

\[
F_c(x_1,t)=(t,\pi_t(x_1)+c),
\qquad c=0,\dots,7
\]

という 8 本の shift permutation を作りました。

各 \(F_c\) は全体の permutation なので、無向化しても最大次数は

\[
16
\]

です。これは circulant よりかなり柔軟で、Cayley 的な固定差分構成ではありません。

しかし結果はやはり悪く、\(q=12,L=4,r=8\) で radius 4 miss は典型的に

\[
10,400
\]

前後でした。

比較のため、同じ

\[
n=20,736,\quad d=16
\]

の random regular graph では radius 4 miss がだいたい

\[
1,200\text{〜}1,400
\]

程度です。つまり、feedback-shift 型は random regular よりずっと展開が悪いです。

---

## 3. なぜ悪いか

原因ははっきりしています。

feedback-shift graph は、どれだけ tail ごとに非線形 permutation を入れても、

\[
\text{1 step で窓を 1 つずらす}
\]

という制約を保ちます。

そのため、長さ \(k\) の path で影響できる座標の組み合わせが、まだ sliding-window 的に強く制限されています。

直感的には、de Bruijn shift は「全部の symbol を順に書き込む」には強いですが、無向 degree 制約で fan を削った瞬間、書き込み自由度が激減します。すると、短距離球が Moore 的に広がらず、巨大な衝突を起こします。

これは前回までの有限幾何 thinning と似た失敗ではありません。今回の失敗は、

\[
\text{Hashimoto/de Bruijn の exact fan は packet 数で不可能}
\]

かつ

\[
\text{single-window feedback では展開が足りない}
\]

という、かなり構造的な失敗です。

---

## 4. この方針で残すべき核

捨てるのは「literal de Bruijn shift」です。

残すべき核は、

\[
\boxed{
\text{頂点ではなく oriented edge / nonbacktracking state を情報担体にする}
}
\]

です。

これはまだ良いと思います。Moore bound の分岐は頂点ではなく非戻り歩道から来るので、Hashimoto 側から設計するという発想自体は正しい。

ただし、次は de Bruijn fan ではなく、

\[
\boxed{
\text{coded fan fragments}
}
\]

にする必要があります。

---

## 5. 次の本命：coded multi-window Hashimoto packet

新しい設計条件はこうです。

各 packet は 16 個の oriented states を持つ。  
各 state は、単一の word window ではなく、複数の address projection を持つ：

\[
w=(u_1,u_2,u_3,\dots)
\]

1 step の非戻り遷移は、単に

\[
(x_1,x_2,x_3,x_4)\mapsto(x_2,x_3,x_4,a)
\]

とするのではなく、

\[
\text{複数の projection に同時に coded update をかける}
\]

ようにする。

狙いは、長さ 4 または 5 の path label が target vertex の address を「順番に書く」のではなく、

\[
\text{covering array / orthogonal array 的に target address を打つ}
\]

ことです。

つまり、次は de Bruijn shift register ではなく、

\[
\boxed{
\text{nonbacktracking tree の path labels}
\to
\text{target packets}
}
\]

が covering array になるように quotient を作る。

これはかなり非自明な方向です。単純な Cayley graph でも、voltage lift でも、有限幾何 thinning でもありません。

---

## 6. 次に具体化する有限設計問題

次の作業対象はこれです。

### Coded packet design

非戻り color word

\[
c_1c_2c_3c_4
\]

を考える。ただし

\[
c_i\ne c_{i+1}.
\]

これらは Moore tree の葉です。\(d=16,k=4\) なら葉の数は

\[
16\cdot15^3=54,000.
\]

これを target packet address に写す map

\[
\Phi_x(c_1,c_2,c_3,c_4)
\]

を、source packet \(x\) ごとに作る。

欲しい条件は、

\[
\{\Phi_x(c_1,c_2,c_3,c_4)\}
\]

が全 target vertex を覆うことです。

ただし \(\Phi_x\) は任意の関数ではなく、無向グラフの Hashimoto packet と反転 involution から来る必要があります。

ここで covering array を使います。

1 step ごとの port choice が target address の複数座標を同時に制約するように設計し、4 step の全 path labels が全 address を覆うようにする。

これは de Bruijn のような「1 step = 1 symbol 書き込み」より強いです。  
1 step が複数座標に分散して情報を入れるので、fan-packing obstruction を避けられます。

---

## 7. 今回の判断

今回で明確になったこと：

\[
\boxed{
\text{exact de Bruijn fan packet は不可能}
}
\]

\[
\boxed{
\text{single-window feedback shift は展開が悪すぎる}
}
\]

したがって、Hashimoto-first 方針を続けるなら、次は

\[
\boxed{
\text{coded multi-window packet / covering-array quotient}
}
\]

に進むべきです。

これは、前回までの「数学者なら自然に思いつく」有限幾何の thinning や opposition matching とは違って、Moore tree の非戻り path label を先に符号化し、それを無向グラフの packet/involution 条件へ落とす設計です。

まだ完成していませんが、今回の obstruction により、次に避けるべき単純案がはっきりしました。次フェーズでは、literal shift ではなく、covering-array 型の packet quotient を直接構成します。

---

## Turn 083 (Round 019) — 🧑 USER

_2026-05-24 15:42:03 UTC_

続けてください

---

## Turn 084 (Round 019) — 🤖 ASSISTANT

_2026-05-24 15:42:21 UTC_  ·  model: `gpt-5-5-pro`

ここは雑に試行錯誤へ戻さず、fan-packing obstruction を受けて、構成条件を弱めず実現可能な形式へ落とします。実装はその構成型の feasibility と直径検証に限定します。

---

## Turn 085 (Round 019) — 🤖 ASSISTANT

_2026-05-24 15:45:33 UTC_  ·  model: `gpt-5-5-pro`

Exact de Bruijn は捨て、非戻り path を小深さルーティングネットワークとして設計する方向へ切り替えます。まず \(d=14,k=5,n\approx5.8万\) に合わせた候補族だけを検証します。

---

## Turn 086 (Round 019) — 🤖 ASSISTANT

_2026-05-24 16:08:08 UTC_  ·  model: `gpt-5-5-pro`

続けました。今回は前回の Hashimoto/de Bruijn packet 案をそのまま押すのではなく、そこで残った「非戻り path を情報担体にする」という核だけを残して、より現実的な **rank-controller blow-up** に作り替えました。

成果物はこちらです。

[phase12_rank_controller_artifacts.zip](sandbox:/mnt/data/phase12_rank_controller_artifacts.zip)

## 結論

今回も、**検証済みの新記録グラフはまだ出ていません**。

ただし、前回の「literal de Bruijn packet」は数え上げで死んだので、そこからかなり本質的に設計を変えました。

新方針は：

\[
\boxed{
\text{小さい controller graph の walk が、座標を1個ずつ書くのではなく、}
}
\]

\[
\boxed{
\text{ベクトル方向の rank で target address 全体を張る}
}
\]

というものです。

これは、前回の de Bruijn shift の「1 step = 1 coordinate 書き込み」が硬すぎたことへの修正版です。

---

## 新しい構成：rank-controller blow-up

小さい \(r\)-正則 controller graph \(C\) を取ります。

頂点集合は

\[
V(G)=V(C)\times \mathbb F_q^s.
\]

controller の各辺

\[
e=\{u,v\}
\]

に、非零ベクトル

\[
g_e\in \mathbb F_q^s
\]

を割り当てます。

そして、各 \(a\in\mathbb F_q\) に対して

\[
(u,x)\sim (v,x+a g_e)
\]

という辺を張ります。

このとき、各 controller 辺は \(q\) 本の辺束を与えるので、最大次数は

\[
d=rq.
\]

ここで重要なのは直径証明です。

もし任意の ordered pair

\[
u,v\in V(C)
\]

に対して、長さ \(\le k\) の controller walk

\[
u=u_0,u_1,\dots,u_t=v
\]

があり、その辺ベクトル

\[
g_{u_0u_1},g_{u_1u_2},\dots,g_{u_{t-1}u_t}
\]

が \(\mathbb F_q^s\) を張るなら、任意の address 差

\[
y-x\in\mathbb F_q^s
\]

を係数 \(a_i\) で解けます。したがって

\[
(u,x)\leadsto(v,y)
\]

が長さ \(\le k\) で作れます。

つまり、十分条件は：

\[
\boxed{
\forall u,v,\quad
\exists\text{ length }\le k\text{ walk }W:u\to v
\text{ such that }
\operatorname{rank}\{g_e:e\in W\}=s.
}
\]

この条件が満たされれば、直径は計算探索ではなく rank 条件から証明できます。

---

## なぜこれは前回より良いか

前回の de Bruijn/coordinate-write 型では、1 step が 1 coordinate しか書けませんでした。

すると、例えば \(s=5\) で任意の target を作るには、5 step の controller walk が 5 個の coordinate label を全部含む必要があります。これは「rainbow path」条件になります。

しかし cubic controller では、1 頂点から出る rainbow nonbacktracking 5-walk の数は高々

\[
3\cdot2\cdot2\cdot2\cdot1=24
\]

です。

一方、\(q=5,r=3,s=5\) で \((15,5)\) 記録を超えるには controller 頂点数 \(h\ge25\) が必要です。つまり、**coordinate-write 版は記録更新に必要な controller size に届く前に path 数上限で死にます**。

rank-controller ではこの制約が消えます。  
5 本の辺が「5 色全部を含む」必要はなく、対応する 5 本のベクトルが full rank ならよい。これはかなり本質的な改善です。

---

## 狙えるパラメータ

今回、現実的な最初の候補として次を調べました。

### 候補 A：\((d,k)=(12,5)\)

\[
q=4,\quad r=3,\quad s=5,\quad h=30.
\]

すると

\[
d=rq=12,
\]

\[
n=hq^s=30\cdot4^5=30,720.
\]

現行記録は

\[
N(12,5)\ge29,621
\]

なので、成功すれば

\[
+1,099
\]

の更新です。

これは一番小さく、controller も 30 頂点 cubic で済みます。次に本気で詰めるなら、これが最初のターゲットです。

### 候補 B：\((d,k)=(16,5)\)

\[
q=4,\quad r=4,\quad s=5,\quad h=130.
\]

すると

\[
d=16,
\]

\[
n=130\cdot4^5=133,120.
\]

現行記録は

\[
N(16,5)\ge132,496
\]

なので、成功すれば

\[
+624
\]

の更新です。

更新幅は小さいですが、条件が非常に明確です。

### 候補 C：\((d,k)=(16,5)\), 非零係数 variant

係数 \(a\) を \(a\in\mathbb F_5^\*\) に制限すると、1 controller edge の次数消費は \(q-1=4\) です。

そこで

\[
q=5,\quad r=4,\quad s=5,\quad h=43
\]

とすれば

\[
d=4\cdot4=16,
\]

\[
n=43\cdot5^5=134,375.
\]

現行 \((16,5)=132,496\) を超えます。

ただし、この variant は係数 0 が使えないため、単なる rank 条件では足りず、「非零係数だけで全ベクトルを覆う」条件が必要です。初期ランダム実験ではかなり弱かったので、本命順位は A, B より下です。

---

## 実験結果

### 1. \(q=4,r=3,h=30,s=5\)

random cubic controller と random vector labels を試しました。

最良の初期 trial では、ordered controller pair のうち

\[
250
\]

個が rank-cover 条件を満たしませんでした。

1 source あたりの最大 bad target は

\[
12
\]

で、最小 covered target は

\[
18/30
\]

でした。

つまり、完全成功にはまだ遠いですが、少なくとも問題サイズはかなり小さいです。

---

### 2. \(q=4,r=4,h=130,s=5\)

random 4-regular controller では、まず controller 自体が弱いです。  
nonbacktracking length-5 walk の endpoint coverage にゼロが多く、典型的には ordered pair で約 1100 個程度、長さ 5 endpoint が存在しません。

edge-swap で controller coverage だけを改善する小実験では、ゼロ ordered pair を約

\[
718
\]

まで下げられましたが、ゼロには届きませんでした。

このターゲットは、random controller ではなく、かなり均一な length-5 walk endpoint distribution を持つ controller が必要です。

---

### 3. \(q=5,r=4,h=43,s=5\), 非零係数 variant

これは

\[
n=134,375,\quad d=16
\]

で、数値的には魅力的です。

しかし random controller / random vector labels では、深さ 5 の到達漏れが大きく残りました。初期 run の最良でも product graph 上の総 miss が約

\[
265,066
\]

で、1 controller source からの最大 miss は約

\[
8,717
\]

でした。

つまり、非零係数 variant は「rank さえあればよい」より難しいです。今すぐ本命にはしません。

---

## ここまでの判断

今回の新方針は、前回までの finite geometry thinning や random correspondence よりは筋が良いです。

理由は、直径証明の形が非常に明確だからです。

\[
\text{controller walk の edge vectors が full rank}
\quad\Longrightarrow\quad
\text{任意の address 差を解ける}
\quad\Longrightarrow\quad
\operatorname{diam}(G)\le k.
\]

ただし、random controller では足りません。

本質的な bottleneck は次です。

\[
\boxed{
\text{小さい }r\text{-正則 controller }C
\text{ で、任意の ordered pair を full-rank walk で結ぶ}
}
\]

これは局所修復ではなく、controller graph と vector labeling の finite design 問題です。

---

## 次に進むべき方向

次は random regular controller を捨てて、controller 自体を rank-covering に向けて設計します。

特に最初に集中すべきは：

\[
\boxed{
q=4,\ r=3,\ s=5,\ h=30
}
\]

です。

成功すれば

\[
\boxed{
N(12,5)\ge30,720
}
\]

となり、現行 \(29,621\) を超えます。

この問題は小さいので、次は controller を「ただの cubic graph」ではなく、以下のような構造で設計するべきです。

\[
\text{30頂点 controller}
+
\text{各 source からの length-5 walk endpoint が均一}
+
\text{edge vector labels が rank-covering array}
\]

ここまでくると、メイン問題は大グラフ探索ではなく、

\[
\boxed{
30\text{ 頂点 cubic controller の rank-covering design}
}
\]

に縮約されています。これはかなり良い形です。

---

## Turn 087 (Round 020) — 🧑 USER

_2026-05-25 06:41:46 UTC_

続きお願いします

---

## Turn 088 (Round 020) — 🤖 ASSISTANT

_2026-05-25 06:42:17 UTC_  ·  model: `gpt-5-5-pro`

今回は大グラフではなく、\((12,5)\) 用の \(q=4,r=3,s=5,h=30\) rank-controller 条件そのものに絞ります。ランダム探索ではなく、30頂点 cubic controller と GF(4)^5 ラベルが構造的に rank-covering を満たせるか検証します。

---

## Turn 089 (Round 020) — 🤖 ASSISTANT

_2026-05-25 06:51:37 UTC_  ·  model: `gpt-5-5-pro`

重要な obstruction が出ています。\(q=4,r=3,h=30\) は rank 条件以前に長さ5の edge-simple trail が不足するため、\(q=3,r=4,h=122\) の候補にも広げて見ています。

---

## Turn 090 (Round 020) — 🤖 ASSISTANT

_2026-05-25 07:00:54 UTC_  ·  model: `gpt-5-5-pro`

さらに、rank-controller を \(k=5\) だけでなく \(k=4\) の小 controller × 有限体ファイバーへ縮約する分岐も見えました。こちらは候補が鋭いので、可否を重点的に確認します。

---

## Turn 091 (Round 020) — 🤖 ASSISTANT

_2026-05-25 07:13:34 UTC_  ·  model: `gpt-5-5-pro`

続けました。今回は、前回の full-coefficient rank-controller から一段進めて、**degree budget をより効率よく使う “projective / punctured rank-controller”** を試しました。

成果物はこちらです。

[phase13_projective_rank_controller_artifacts.zip](sandbox:/mnt/data/phase13/phase13_projective_rank_controller_artifacts.zip)

## 結論

今回も、**検証済みの新記録グラフはまだ出ていません**。

ただし、前回よりかなり重要な形に問題が絞れました。  
次に狙うべき候補は：

\[
\boxed{(d,k,n)=(15,5,77824)}
\]

です。

現行記録として使っている表では

\[
N(15,5)\ge 77520
\]

なので、直径 5 を証明できれば

\[
77824-77520=304
\]

の更新になります。更新幅は小さいですが、構成原理は前回よりずっと明確です。

---

## 新しい候補：projective rank-controller

前回の rank-controller は、controller edge ごとに

\[
a\in \mathbb F_q
\]

の全係数を使っていました。つまり controller の 1 辺が \(q\) 本分の次数を消費します。

今回は、係数 0 を捨てて

\[
a\in\mathbb F_4^\*
\]

だけを使います。すると controller の 1 辺が使う次数は

\[
|\mathbb F_4^\*|=3
\]

です。

5-regular controller \(C\) を使うと、完成グラフの最大次数は

\[
5\cdot3=15.
\]

頂点集合は

\[
V(G)=V(C)\times\mathbb F_4^5.
\]

controller 頂点数を

\[
|V(C)|=76
\]

にすると、

\[
|V(G)|=76\cdot4^5=76\cdot1024=77824.
\]

したがって、直径 5 なら \((15,5)\) の新記録です。

各 controller edge \(e=\{u,v\}\) にベクトル

\[
g_e\in\mathbb F_4^5
\]

を割り当て、辺は

\[
(u,x)\sim(v,x+a g_e),\qquad a\in\mathbb F_4^\*
\]

で定義します。

---

## なぜこれは前回より筋が良いか

full coefficient 版では、1 controller edge が \(q\) 本の次数を使います。たとえば \(\mathbb F_4\) だと 4 本です。次数 15 や 16 の範囲では、controller degree をあまり上げられません。

今回の projective 版では、1 edge あたり 3 本で済むので、controller degree を 5 にできます。  
その結果、長さ 5 の nonbacktracking controller walk 数は

\[
5\cdot4^4=1280
\]

になります。

controller 頂点数が 76 なので、平均すると ordered pair あたり

\[
1280/76\approx16.84
\]

本の長さ 5 walk があります。これはかなり良いです。

実際、ランダムな 76 頂点 5-regular controller では、サンプル上、**全ての ordered controller pair に少なくとも 1 本の長さ 5 nonbacktracking walk が存在**していました。典型的には、最小 path count が 3〜6、本数平均が 16.84 です。

つまり、今回のボトルネックは controller の到達性ではありません。  
問題は、各 controller pair の長さ 5 walk が作る \(\mathbb F_4^5\) 内の和集合が、全 address 差を覆うかどうかです。

---

## full-rank だけでは証明できない

ここが今回の重要な発見です。

full coefficient 版では、長さ 5 walk の edge labels

\[
g_1,\dots,g_5
\]

が \(\mathbb F_q^5\) を張れば、任意の差分

\[
y-x
\]

を

\[
a_1g_1+\cdots+a_5g_5
\]

として解けました。係数 \(a_i\) に 0 が許されるからです。

しかし今回は

\[
a_i\in\mathbb F_4^\*
\]

です。係数 0 が使えません。

したがって、たとえ

\[
g_1,\dots,g_5
\]

が full rank でも、その path で到達できる差分は

\[
\left\{
a_1g_1+\cdots+a_5g_5:
a_i\in\mathbb F_4^\*
\right\}
\]

だけです。サイズは最大

\[
3^5=243
\]

で、\(\mathbb F_4^5\) 全体の

\[
4^5=1024
\]

には全然足りません。

特に full-rank path では、差分 0 は到達できません。  
0 を作るには、edge labels が依存している path、つまり circuit 的な path も必要になります。

これにより、直径証明の条件は rank ではなく、次の **additive covering condition** になります。

\[
\boxed{
\bigcup_W
\left\{
\sum_{e\in W} a_e g_e:
a_e\in\mathbb F_4^\*
\right\}
=
\mathbb F_4^5
}
\]

ここで \(W\) は、固定された controller pair 間の長さ 5 walk 全体です。

これはかなり良い形です。  
「bad pair を局所修復する」のではなく、各 controller pair に対して、長さ 5 path のラベル列が \(\mathbb F_4^5\) を additive に覆うか、という有限設計問題になりました。

---

## 実験結果

ランダムな 76 頂点 5-regular controller と、ランダムな \(\mathbb F_4^5\) edge labels で、完成グラフを full BFS 検証しました。

候補グラフは：

\[
n=77824,\qquad d=15.
\]

10 trial の完走 run では、最良候補が：

\[
\text{min radius-5 reach}=77058/77824
\]

つまり、最悪始点から

\[
766
\]

頂点が距離 5 以内に届きませんでした。

より長い中断 run では、最良観測値は：

\[
\text{min radius-5 reach}=77134/77824
\]

つまり最大 miss は

\[
690
\]

でした。

まだ直径 5 ではありません。  
ただし、前回までの多くの候補と違って、失敗の理由がかなり明確です。controller は十分混ざっている。足りないのは、path-label sumset の additive covering です。

---

## 重要な発見：9 個の path-label tuple で \(\mathbb F_4^5\) を覆える

今回、一番意味があったのはここです。

長さ 5 path の label tuple

\[
(g_1,\dots,g_5)
\]

に対して、

\[
S(g_1,\dots,g_5)
=
\left\{
a_1g_1+\cdots+a_5g_5:
a_i\in\mathbb F_4^\*
\right\}
\]

を考えます。

ランダム greedy で、次の性質を持つ 9 個の 5-tuple を見つけました。

\[
\boxed{
S(T_1)\cup\cdots\cup S(T_9)=\mathbb F_4^5.
}
\]

つまり、各 controller pair に対して、この 9 種類の path-label tuple、またはその \(GL(5,4)\) 変換版が実現できれば、直径 5 が証明できます。

9 tuple の性質は：

| tuple | rank | sumset size | 0 を含むか | cumulative cover |
|---:|---:|---:|---:|---:|
| 1 | 5 | 243 | no | 243 |
| 2 | 5 | 243 | no | 459 |
| 3 | 5 | 243 | no | 633 |
| 4 | 5 | 243 | no | 771 |
| 5 | 5 | 243 | no | 870 |
| 6 | 5 | 243 | no | 933 |
| 7 | 4 | 196 | yes | 982 |
| 8 | 5 | 243 | no | 1015 |
| 9 | 5 | 243 | no | 1024 |

ここが面白いです。  
rank 5 の basis path だけでは 0 が覆えません。途中で rank 4 の circuit tuple が必要になります。

つまり、理想的な path family は「全部 full rank」ではなく、

\[
\text{basis path 群}
+
\text{circuit path}
\]

を混ぜる必要があります。

この見方は、かなり新しい構成条件になっています。

---

## 今回の判断

projective rank-controller は、まだ完成していません。  
でも、前回までより「何を作ればいいか」はかなり明確になりました。

次に作るべきものは：

\[
\boxed{
76\text{ 頂点 }5\text{-regular controller }C
}
\]

と edge labeling

\[
g_e\in\mathbb F_4^5
\]

で、任意の ordered controller pair \((u,v)\) について、\(u\) から \(v\) への長さ 5 walk の label tuple 群が、上の 9-tuple additive covering library を含む、またはそれと同等の covering family を含むようなものです。

これは局所改善ではなく、かなり具体的な有限設計問題です。

\[
\boxed{
\text{controller path system}
+
\text{punctured additive covering library}
}
\]

を同時に作る問題になっています。

---

## 次の方針

次はランダム labels を増やすのではなく、次の方向に進むべきです。

1. **controller 側**  
   任意の ordered pair に対して、長さ 5 walk が少なくとも 9 本以上、できれば構造的に分類できる 9 本以上ある 76 頂点 5-regular graph を作る。

2. **label 側**  
   その 9 本の path labels が、\(\mathbb F_4^5\) の additive covering library になるように、edge labels を設計する。

3. **証明側**  
   BFS ではなく、各 controller pair の path-label sumset が \(\mathbb F_4^5\) を覆うことを certificate として出す。

現時点の本命候補は：

\[
\boxed{
\text{projective rank-controller over }\mathbb F_4
}
\]

\[
\boxed{
(d,k,n)=(15,5,77824)
}
\]

です。まだ未達ですが、ここまでで初めて、「直径 5 を保証するための具体的な path-label covering certificate」が見えました。

---

## Turn 092 (Round 021) — 🧑 USER

_2026-05-25 07:16:53 UTC_

続きお願いします

---

## Turn 093 (Round 021) — 🤖 ASSISTANT

_2026-05-25 07:17:12 UTC_  ·  model: `gpt-5-5-pro`

前回の projective rank-controller を本線に、ランダムなラベル増殖ではなく controller の path 構造と additive covering 条件を分離して、証明可能な設計に近づけます。

---

## Turn 094 (Round 021) — 🤖 ASSISTANT

_2026-05-25 07:20:24 UTC_  ·  model: `gpt-5-5-pro`

前回の76頂点controllerでは到達性でなく path-label sumset が詰まりなので、記録超えを保てる範囲で controller を少し大きくし、構造的に path family を増やす案も検査します。GF(4) の2-step backtracking が実質的に0係数を再現できる点も、欠点でなく設計要素として使えるか確認します。

---

## Turn 095 (Round 021) — 🤖 ASSISTANT

_2026-05-25 07:45:21 UTC_  ·  model: `gpt-5-5-pro`

続けました。今回は、前回の GF(4) projective rank-controller をそのまま押すのではなく、**係数体を小さくして controller 側の次数を増やす**方向を検査しました。

成果物はこちらです。

[phase14_projective_gf3_artifacts.zip](sandbox:/mnt/data/phase14_projective_gf3_artifacts.zip)

## 結論

今回も、**検証済みの新記録グラフはまだ出ていません**。

ただし、かなり近い候補が出ました。現時点で一番良いのは：

\[
\boxed{
\mathbb F_3^5\text{ 上の projective rank-controller}
}
\]

で、

\[
\boxed{
(d,k,n)=(14,5,58,320)
}
\]

を狙うものです。

現行記録として使っている表では

\[
N(14,5)\ge58,095
\]

なので、直径 5 を証明できれば

\[
58,320-58,095=225
\]

の更新になります。

---

## 今回の構成

controller graph \(C\) を \(r\)-regular とし、頂点集合を

\[
V(G)=V(C)\times \mathbb F_3^5
\]

にします。

各 controller edge

\[
e=\{u,v\}
\]

に非零ベクトル

\[
g_e\in\mathbb F_3^5\setminus\{0\}
\]

を割り当て、

\[
(u,x)\sim(v,x+g_e),
\]

\[
(u,x)\sim(v,x-g_e)
\]

を張ります。

つまり controller edge 1 本あたり、次数を 2 だけ使います。したがって final graph の次数は

\[
d=2r.
\]

これは前回の GF(4) projective 版と同じ思想ですが、\(\mathbb F_3^\*=\{\pm1\}\) なので、controller degree をより大きく取れます。

---

## 本命候補 A：\((14,5,58,320)\)

\[
r=7,\qquad |V(C)|=240.
\]

このとき

\[
d=2r=14,
\]

\[
n=240\cdot 3^5=240\cdot243=58,320.
\]

直径 5 なら、現行 \((14,5)=58,095\) を超えます。

ランダムな 240 頂点 7-regular controller とランダム edge labels を試したところ、最良 full scan は：

\[
\min_v |B_5(v)|=58,111,
\]

つまり最大 miss は

\[
58,320-58,111=209.
\]

平均到達数は

\[
58,195.5
\]

でした。

まだ直径 5 ではありませんが、かなり近いです。

---

## 本命候補 B：\((16,5,132,678)\)

\[
r=8,\qquad |V(C)|=546.
\]

このとき

\[
d=16,
\]

\[
n=546\cdot3^5=132,678.
\]

現行 \((16,5)=132,496\) を

\[
182
\]

だけ超えます。

ただしこちらは、ランダム controller / random label では 30 始点サンプルで典型的に miss が

\[
700\text{〜}780
\]

程度残りました。現時点では \((14,5)\) 候補の方が近いです。

---

## additive covering library の整理

この構成では、長さ 5 の controller path に沿った fiber 差分は

\[
\pm g_1\pm g_2\pm g_3\pm g_4\pm g_5
\]

です。

したがって、固定された controller pair \((u,v)\) に対して、\(u\) から \(v\) への長さ 5 path の label 5-tuple たちが

\[
\mathbb F_3^5
\]

全体を

\[
\{\pm g_1\pm\cdots\pm g_5\}
\]

の和集合で覆えば、fiber 差分は全部作れます。

今回、ランダム greedy で、\(\mathbb F_3^5\) 全体を覆う **10 個の 5-tuple library** を見つけました。

rank pattern は：

\[
5,5,5,5,5,4,5,5,4,5.
\]

ここでも GF(4) と同じく、全部を full-rank basis path にするだけでは足りません。0 や低支援ベクトルを覆うには、rank 4 の circuit tuple が必要です。

つまり、次の証明条件は非常に明確です。

\[
\boxed{
\text{任意の controller pair }(u,v)\text{ に対して、}
}
\]

\[
\boxed{
u\to v\text{ の長さ }\le5\text{ path labels が、この 10-tuple library 相当を含む。}
}
\]

これが満たされれば、直径 5 は BFS ではなく additive-covering certificate で証明できます。

---

## 捨てた副候補

### GF(4) hybrid full/projective controller

GF(4) で「1 本だけ full-coefficient edge、4 本を projective edge」にする hybrid も試しました。

\[
h=130,\quad d=16,\quad n=133,120
\]

を狙える形でしたが、sample miss が約

\[
6,900
\]

と大きく、見込み薄です。

### \(W(3,3)\) incidence controller

80 頂点の generalized quadrangle incidence graph \(W(3,3)\) に nonincident matching を足して 5-regular controller にする案も試しました。

構造的にはきれいですが、random label で sample miss が

\[
18,000
\]

規模になり、random regular controller よりかなり悪いです。有限幾何 controller は、ここでは path-label covering の自由度をむしろ殺していました。

### de Bruijn controller

4 文字長 5 の de Bruijn controller も試しました。

\[
|V(C)|=4^5=1024,\quad d=16,\quad n=248,832
\]

という魅力的なサイズになりますが、sample miss は約

\[
89,000
\]

で壊滅的でした。sliding-window 型 controller は、rank-covering 目的には合いません。

---

## 現時点の判断

一番有望なのは：

\[
\boxed{
\mathbb F_3^5\text{ projective rank-controller}
}
\]

\[
\boxed{
r=7,\ |V(C)|=240,\ d=14,\ n=58,320,\ k=5
}
\]

です。

ただし、random labeling ではあと 200 前後届きません。ここから先は、ランダム trial を増やすのではなく、次の有限設計問題として解くべきです。

\[
\boxed{
240\text{ 頂点 }7\text{-regular controller }C
}
\]

と

\[
\boxed{
edge labels }g_e\in\mathbb F_3^5
}
\]

を作り、任意の ordered pair \((u,v)\) に対して、長さ 5 path の label 5-tuple が \(\mathbb F_3^5\) の additive covering library を含むようにする。

これは最終グラフの bad pair を局所修復する問題ではなく、

\[
\boxed{
\text{controller path system}
+
\text{additive covering library}
}
\]

の同時設計問題です。次はこの 10-tuple library を固定し、それを全 controller pair に実現する **library-scheduled controller** を作る方向に進めます。

---

## Turn 096 (Round 022) — 🧑 USER

_2026-05-25 07:59:12 UTC_

この方向性で、新記録が出せるほど頂点間が効率的に辺で接続されると数学的に事前に期待できる理由がありますか？ないなら方針を破棄して、事前に新記録が出せるほど頂点間が効率的に辺で接続されると数学的に事前に期待できる理由があるアイデアを考えることに集中してください。数学的に理由がない方法を順番に試すのは効率が非常に悪いです。良いアイデアが枯渇したらこの探索自体を停止します。

---

## Turn 097 (Round 022) — 🤖 ASSISTANT

_2026-05-25 07:59:41 UTC_  ·  model: `gpt-5-5-pro`

ここで実験を止め、rank-controller に本当に事前の勝算があるかを、期待値・被覆量・衝突・証明可能性の観点から厳しく判定します。

---

## Turn 098 (Round 022) — 🤖 ASSISTANT

_2026-05-25 08:02:51 UTC_  ·  model: `gpt-5-5-pro`

結論が弱ければ遠慮なく破棄し、試行錯誤ではなく新しい構成原理を探す判断に切り替えます。

---

## Turn 099 (Round 022) — 🤖 ASSISTANT

_2026-05-25 08:16:14 UTC_  ·  model: `gpt-5-5-pro`

はい。この指摘はかなり重要です。結論から言うと、**現在の projective rank-controller 方向は、いまの形では破棄すべき**です。

理由は「試したらまだ届かない」ではなく、もっと強くて、**新記録が出るほど効率よく接続されるという事前の数学的根拠が不足している**からです。むしろ、簡単な確率計算をすると「今の候補があと少し届かない」のは自然で、偶然ではありません。

## rank-controller 方向の事前評価

直近の本命は

\[
\mathbb F_3^5,\quad r=7,\quad |V(C)|=240,
\]

から作る

\[
(d,k,n)=(14,5,58320)
\]

候補でした。

controller の長さ 5 非戻り walk 数は、1 始点あたり

\[
7\cdot6^4=9072
\]

です。controller 頂点数は 240 なので、固定された ordered pair \((u,v)\) あたりの長さ 5 walk 数の平均は

\[
\lambda \approx \frac{9072}{240}=37.8.
\]

長さ 5 path 1 本が fiber 側で作れる差分は

\[
\pm g_1\pm g_2\pm g_3\pm g_4\pm g_5
\]

なので、高々

\[
2^5=32
\]

個です。一方、覆うべき fiber 差分は

\[
|\mathbb F_3^5|=243.
\]

ランダムな 32 点 subset が平均 38 個あると考えると、未被覆差分の期待値はだいたい

\[
243\left(1-\frac{32}{243}\right)^{38}\approx 1.1
\]

です。

つまり、**controller pair 1 個あたり平均 1 個程度の fiber 差分が漏れる**のが自然です。controller pair は

\[
240^2=57600
\]

個あります。したがって、全体として漏れが残るのはむしろ当然です。

実験で最大 miss が 200 前後だったのは、「惜しい」のではなく、だいたいこの計算どおりです。これはかなり決定的です。

## union bound 的にも足りない

直径 5 を保証するには、全ての controller pair と全ての fiber 差分を覆る必要があります。制約数は

\[
240^2\cdot243 \approx 1.4\times10^7.
\]

ランダム被覆でこれを全部潰すには、1 controller pair あたりの有効 path 数がざっくり

\[
\frac{\log(240^2\cdot243)}{32/243}\approx126
\]

本くらい欲しいです。

しかし、実際の平均は 38 本程度です。長さ \(\le5\) を全部入れても平均は 45 本程度にしかなりません。

したがって、この方向には次の構造的欠陥があります。

\[
\boxed{
\text{記録更新に必要な } |C|=240
\text{ では、path 数が additive covering に足りない。}
}
\]

これは「もっとランダム trial を回せばよい」問題ではありません。

## では structured label なら救えるか？

理論上は救えます。  
たとえば、各 controller pair \((u,v)\) に対して、長さ 5 path の label tuple が偶然ではなく、あらかじめ設計された additive covering library を含むなら、直径 5 を証明できます。

しかし、それを実現するには、全ての ordered pair に対して、特定の 10 個前後の path-label pattern を同時に埋め込む必要があります。これは非常に強い要求です。

そして、この要求を自然に満たす既知のやり方はだいたい

\[
\text{群作用 / Schreier graph / semidirect product / Cayley 型}
\]

に落ちます。これは今回の禁止条件に引っかかります。逆に、群作用に落とさずにそれを実現する新しい設計原理は、現時点では見えていません。

なので、この方向を続けるなら、まず次の定理級のものが必要です。

> 240 頂点 7-正則 controller と \(\mathbb F_3^5\) edge-labeling があり、任意の ordered pair に対して、長さ 5 path の label sumset が \(\mathbb F_3^5\) を完全に覆う。しかも構成は群作用・Cayley・voltage に本質的に還元されない。

現時点で、この定理が成立しそうだと信じる数学的根拠はありません。

したがって、**projective rank-controller 方向は破棄します**。

## ここまでの候補の棚卸し

これまで試した・考えた方向を、今の基準で見るとこうです。

| 方向 | 判断 | 理由 |
|---|---|---|
| generalized hexagon に shortcut | 破棄 | 距離 6 層を潰すには追加次数が不足 |
| incidence/point graph thinning | 破棄 | 局所 residue で次数を消費し、分岐効率が落ちる |
| opposition matching / far correspondence | 破棄 | far layer に飛ばすだけでは random regular 的で、全 pair 被覆に足りない |
| Hashimoto–de Bruijn exact packet | 破棄 | fan-packing の数え上げで不可能 |
| feedback shift / sliding window | 破棄 | window 制約で展開が弱すぎる |
| rank-controller / projective rank-controller | 破棄 | path 数と additive covering の計算で不足 |
| group/Cayley/semidirect で救う | 禁止 | 既存主流手法に還元される |

ここまで来ると、無理に次を試すのは危険です。  
「数学的に効率が良いと事前に見える」条件を満たさない案を順に試すのは、たしかに効率が悪いです。

## 次に採用できるアイデアの条件

今後、続ける価値がある案は、最低でも次を満たす必要があります。

1. **random regular graph 的な被覆限界を超える仕組みがある。**  
   単に遠くに辺を張る、ランダムに混ぜる、expander っぽい、では足りません。

2. **任意の source-target pair を覆う理由が path counting ではなく、明示的な covering identity から出る。**  
   たとえば「この長さ \(k\) の path family が target address 全体を分割・被覆する」という証明が必要です。

3. **その identity が Cayley / voltage / semidirect product / standard finite geometry thinning に還元されない。**

4. **記録更新サイズに対して、制約数と path 数の収支に余裕がある。**  
   「期待 miss が 1 個程度」ではだめで、union bound か、それに代わる決定的被覆構造が必要です。

この基準を置くと、現時点で私が自信を持って「進めるべき」と言える新アイデアはありません。

## いまの判断

ここで探索は一度止めるべきです。

理由は、良いアイデアが完全に不可能だからではなく、**現時点で残っている案は、数学的な事前勝算がないか、禁止された既存手法に落ちる**からです。

この状態でさらにコードを書いたり、候補を順に試したりするのは、ユーザーさんの指摘どおり時間の無駄になりやすいです。

次に再開するなら、実験からではなく、まず次のような定理候補を紙の上で作る必要があります。

\[
\boxed{
\text{Moore tree の reduced-word ball を、非群的な有限状態系へほぼ完全に折り畳む covering identity}
}
\]

または

\[
\boxed{
\text{任意の source-target pair に対し、長さ }k\text{ path が target address を分割被覆する非 Cayley 型構成}
}
\]

このレベルの新しい原理が出るまでは、探索は停止するのが正しいと思います。

---

## Turn 100 (Round 023) — 🧑 USER

_2026-05-25 13:05:40 UTC_

新しい原理を考えてください。

---

## Turn 101 (Round 023) — 🤖 ASSISTANT

_2026-05-25 13:06:11 UTC_  ·  model: `gpt-5-5-pro`

ここではコードや文献確認はいったん置き、構成原理そのものを絞ります。前の失敗を避けるため、記録サイズへ届く理由を先に数式で確認します。

---

## Turn 102 (Round 023) — 🤖 ASSISTANT

_2026-05-25 13:09:27 UTC_  ·  model: `gpt-5-5-pro`

今回はランダム混合や既存構造の薄化を全て除外し、Moore tree の折り畳み自体を新しい設計対象にします。候補は出しても、その場で数え上げにより潰せるものは進めません。

---

## Turn 103 (Round 023) — 🤖 ASSISTANT

_2026-05-25 13:27:01 UTC_  ·  model: `gpt-5-5-pro`

はい。ここで考えるべき新原理は、前回までの「辺を足す」「薄くする」「遠方へ飛ばす」「ランダムに混ぜる」とは別物にします。

私がいま数学的に勝算があると見なせる候補は、次です。

\[
\boxed{
\textbf{可制御チャート・リフト}
}
\]

英語っぽく言うなら **controllable route-chart lift** です。

これは、頂点間を「多くの path の和集合でなんとなく覆う」のではなく、**1 本の base path そのものを、fiber 全体への全単射的な routing chart にする**原理です。

---

# 1. 前回の rank-controller との決定的な違い

前回の projective rank-controller は、1 本の path が作れる fiber 差分が少なすぎました。

たとえば \(\mathbb F_3^5\) projective 版では、長さ 5 path 1 本が作る差分は

\[
\pm g_1\pm g_2\pm g_3\pm g_4\pm g_5
\]

なので高々

\[
2^5=32
\]

個です。覆うべき差分は

\[
3^5=243
\]

個。だから controller pair ごとに多数の path が必要になり、coupon-collector 的に漏れる。これは事前にだめだと判断できます。

新原理では、ここを変えます。

1 本の長さ \(k\) path が、fiber 全体

\[
\mathbb F_q^k
\]

を覆うようにします。つまり、1 path が

\[
q^k
\]

個の fiber 差分を全部作る。

これは情報量的に最適です。長さ \(k\) path では各 step で \(q\) 通りの port を選べるので、可能な port 列は

\[
q^k
\]

通りしかありません。新原理は、それを **1 個も無駄にせず target fiber 全体に対応させる** ことを狙います。

ここが数学的な勝算です。

---

# 2. 構成原理

小さい controller graph \(C\) を取ります。次数を \(r\) とします。

最終グラフの頂点集合を

\[
V(G)=V(C)\times \mathbb F_q^s
\]

にします。最初は

\[
s=k
\]

を狙います。

各 controller の有向辺

\[
e:u\to v
\]

に、線形制御データ

\[
A_e\in GL(s,q),\qquad b_e\in\mathbb F_q^s
\]

を割り当てます。

各 \(a\in\mathbb F_q\) に対して、最終グラフに辺

\[
(u,x)\sim (v,A_e x+a b_e)
\]

を張ります。

ただし無向グラフにするため、逆向き辺 \(\bar e:v\to u\) には

\[
A_{\bar e}=A_e^{-1},\qquad b_{\bar e}=A_e^{-1}b_e
\]

を使います。標数が奇数なら符号を調整しますが、本質は同じです。

このとき、controller の 1 辺あたり \(q\) 本の辺を使うので、最終次数は

\[
d=rq.
\]

---

# 3. 直径証明の核：Kalman 型 controllability

controller 上の walk

\[
W=e_1e_2\cdots e_t
\]

を固定します。

fiber 側の遷移を合成すると、終点は

\[
x_t
=
A_W x_0
+
a_1 A_{e_t}\cdots A_{e_2}b_{e_1}
+
a_2 A_{e_t}\cdots A_{e_3}b_{e_2}
+\cdots+
a_t b_{e_t}
\]

になります。

したがって、この walk が fiber 全体を routing できる条件は、次の controllability matrix が full rank であることです：

\[
\operatorname{rank}
\begin{bmatrix}
A_{e_t}\cdots A_{e_2}b_{e_1} &
A_{e_t}\cdots A_{e_3}b_{e_2} &
\cdots &
b_{e_t}
\end{bmatrix}
=s.
\]

特に \(t=s=k\) なら、この行列が正則であるだけで、任意の fiber 差分

\[
y-A_Wx
\]

を一意に解けます。

つまり：

\[
\boxed{
\text{controller 上で }u\to v\text{ の長さ }k\text{ controllable path があれば、}
}
\]

\[
\boxed{
(u,x)\text{ から }(v,y)\text{ へ長さ }k\text{ で行ける。}
}
\]

したがって、十分条件はこれです。

\[
\boxed{
\forall u,v\in V(C),\ 
\exists\text{ 長さ }k\text{ の walk }W:u\to v
\text{ with full controllability rank.}
}
\]

この条件が成立すれば、BFS に頼らず

\[
\operatorname{diam}(G)\le k
\]

が証明できます。

---

# 4. なぜこれは効率が良いか

この構成では、controller の 1 本の成功 path が、fiber の全差分を覆います。

つまり、controller 側で \(u\to v\) の path が 1 本見つかれば、その上にある

\[
q^k
\]

個の port 列が、fiber target 全体と 1 対 1 に対応します。

前回の rank-controller は、1 path が fiber の小部分しか覆わなかったので、多数 path の union に頼る必要がありました。だから確率的に漏れました。

今回は違います。

\[
\boxed{
1\text{ base path}
=
1\text{ full fiber chart}
}
\]

です。

これなら「頂点間が効率的に接続される」と事前に期待する理由があります。  
むしろ、これは degree-diameter 問題で使える最も強い情報効率の一つです。

---

# 5. 最初に狙うべきパラメータ

## 第一候補：\((d,k)=(16,5)\)

取るパラメータは

\[
q=4,\qquad r=4,\qquad s=5.
\]

すると

\[
d=rq=16.
\]

記録を超えるには、controller 頂点数 \(h=|V(C)|\) が

\[
h\cdot4^5>132496
\]

を満たせばよい。

\[
4^5=1024
\]

なので、

\[
h=130
\]

で

\[
n=130\cdot1024=133120.
\]

したがって、成功すれば

\[
\boxed{
N(16,5)\ge133120
}
\]

となり、現行値

\[
132496
\]

を

\[
624
\]

更新します。

必要な controller 条件は：

\[
\boxed{
130\text{ 頂点 }4\text{-正則 controller }C
}
\]

と、各辺の制御データ \((A_e,b_e)\) があり、任意の ordered pair \((u,v)\) に対して長さ 5 の controllable path が存在すること。

これは小さい有限設計問題です。

---

## 第二候補：\((d,k)=(15,5)\)

こちらも良いです。

\[
q=3,\qquad r=5,\qquad s=5.
\]

すると

\[
d=15.
\]

現行記録は

\[
N(15,5)\ge77520.
\]

\[
3^5=243
\]

なので、controller 頂点数

\[
h=320
\]

なら

\[
n=320\cdot243=77760.
\]

したがって、成功すれば

\[
\boxed{
N(15,5)\ge77760
}
\]

で、現行値を

\[
240
\]

更新します。

こちらは更新幅は小さいですが、controller degree が 5 なので、長さ 5 の controller walk 数が多い。controller 側の route coverage は \((16,5)\) 候補より楽です。

---

## 小型検証候補：\((d,k)=(16,4)\)

\[
q=4,\qquad r=4,\qquad s=4.
\]

記録を超えるには

\[
h\cdot4^4>14640.
\]

\[
4^4=256
\]

なので、

\[
h=58
\]

で

\[
n=58\cdot256=14848.
\]

成功すれば

\[
\boxed{
N(16,4)\ge14848
}
\]

となり、現行値

\[
14640
\]

を

\[
208
\]

更新します。

これは小さくて検証しやすいですが、controller が 58 頂点 4-正則で長さ 4 route を全 ordered pair に持つ必要があり、かなり tight です。本命というより proof-of-concept です。

---

# 6. なぜこれは単なる voltage/lift ではないのか

機械的には、これは affine permutation lift として表現できます。そこは隠しません。

ただし、既存の voltage/lift 的構成と本質的に違うのは、探索対象が「群元ラベルで短い積を全体に広げる」ことではない点です。

ここで設計しているのは：

\[
\boxed{
\text{各 base route が fiber 全体への座標チャートになるような制御系}
}
\]

です。

通常の voltage graph では、1 本の base path は 1 個の voltage 積、つまり fiber 上の 1 つの移動を与えるだけです。  
この構成では、1 本の base path とその \(q^k\) 通りの port choices が、fiber 全体を張ります。

言い換えると、path は「移動」ではなく **全単射の routing table** です。

この差が重要です。

---

# 7. この原理が失敗するなら、そこで止めるべき条件

この方向を続ける価値があるのは、次の 2 つの有限設計が成立する場合だけです。

## 条件 A：controller route design

たとえば \((16,5)\) なら、

\[
130\text{ 頂点 }4\text{-正則 controller}
\]

で、任意の ordered pair に長さ 5 の route があること。

ただし単なる diameter 5 では足りません。fiber dimension が 5 なので、長さ 5 の route が必要です。短い path だけでは \(4^5\) 個の fiber target を覆えません。

## 条件 B：controllability labeling

その route たちに対して、各 route の controllability matrix が full rank になるように

\[
(A_e,b_e)
\]

を割り当てられること。

これができれば直径証明は出ます。  
できなければ、この方向は破棄すべきです。

ここでは「bad pair を見て辺を直す」局所改善には進みません。  
証明可能な route table と rank certificate が出ないなら終了です。

---

# 8. この原理の直感的な意味

degree-diameter graph で本当に欲しいのは、短い path が target を効率よく指定することです。

普通のグラフでは、長さ \(k\) の path は単に

\[
\text{どこかの頂点に着く}
\]

だけです。

この原理では、長さ \(k\) の path は

\[
\text{controller endpoint}
+
\text{fiber address}
\]

を同時に指定します。

controller path が「どの大きな塊へ行くか」を決め、port 列が「塊の中のどの頂点へ行くか」を一意に決める。

つまり、辺の使い方が

\[
\text{探索}
\]

ではなく

\[
\text{通信・符号化}
\]

になっています。

これが、今までの候補より数学的に筋が良い理由です。

---

# 9. 次にやるなら

次に進めるべき作業は、コードで巨大グラフを作ることではありません。

まず小さい certificate を探します。

第一段階は：

\[
\boxed{
q=4,\ r=4,\ s=5,\ h=130
}
\]

または検証しやすい

\[
\boxed{
q=4,\ r=4,\ s=4,\ h=58
}
\]

について、controller route table と controllability labeling の存在を調べる。

最終グラフは巨大でも、証明書は小さいです。  
たとえば \((16,5)\) なら、controller は 130 頂点だけ。必要なのは、各 ordered pair に対する長さ 5 route と、その route の \(5\times5\) controllability determinant が非零であることです。

---

# 現時点の結論

新しい原理として、私はこれを採用候補にします。

\[
\boxed{
\textbf{可制御チャート・リフト}
}
\]

狙いはまず：

\[
\boxed{
N(16,5)\ge133120
}
\]

または小型検証として：

\[
\boxed{
N(16,4)\ge14848
}
\]

です。

この方向には、前回の rank-controller と違って、明確な数学的勝算があります。

\[
\boxed{
1\text{ 本の長さ }k\text{ base path が }q^k\text{ 個の fiber target を全て覆う}
}
\]

からです。

これは random coverage ではなく、controllability determinant による決定的な全被覆です。  
次に進めるなら、この原理だけを本線にし、controller と rank certificate の有限設計が作れない場合は探索を止める、という進め方がよいです。

---

## Turn 104 (Round 024) — 🧑 USER

_2026-05-25 13:31:57 UTC_

続けてください

---

## Turn 105 (Round 024) — 🤖 ASSISTANT

_2026-05-25 13:32:26 UTC_  ·  model: `gpt-5-5-pro`

ここからは候補を大量に試すのではなく、可制御チャート・リフトの必要条件を先に確認します。まず controller 側、次に fiber の可制御ラベルを分けて検証します。

---

## Turn 106 (Round 024) — 🤖 ASSISTANT

_2026-05-25 13:35:40 UTC_  ·  model: `gpt-5-5-pro`

巨大グラフの構成には進まず、小さな controller と rank certificate の存在確認だけに絞ります。全 ordered pair の長さ \(k\) route と full-rank 条件が成り立つかを先に判定します。

---

## Turn 107 (Round 024) — 🤖 ASSISTANT

_2026-05-25 13:44:59 UTC_  ·  model: `gpt-5-5-pro`

最初の障害は fiber ではなく controller 側にあります。ランダムな 4-正則 130 頂点では全 ordered pair を覆えませんが、controller 専用に最適化すると未到達はかなり減りました。

---

## Turn 108 (Round 024) — 🤖 ASSISTANT

_2026-05-25 14:00:48 UTC_  ·  model: `gpt-5-5-pro`

進めました。今回はかなり意味のある進展がありました。

成果物はこちらです。

[phase15_controllable_chart_artifacts.zip](sandbox:/mnt/data/phase15_controllable_chart_artifacts.zip)

## 結論

**新記録はまだ出ていません。**

ただし、前回の「可制御チャート・リフト」について、重要な切り分けができました。

\[
\boxed{
\text{fiber 側の原理は実際に成立しうる}
}
\]

ことを確認しました。一方で、

\[
\boxed{
\text{controller 側の exact route coverage がまだ作れていない}
}
\]

という状態です。

つまり、今回は「なんとなく近い候補を試した」ではなく、構成を次の 2 つに分解しました。

1. 1 本の controller route が fiber 全体を覆うか。
2. 必要な controller route が全 ordered pair に存在するか。

今回、1 は成功しました。2 は未解決です。

---

## 1. fiber 側の成功：GF(4)\(^4\) の universal controllability code

狙った小型記録候補は

\[
(d,k,n)=(16,4,14848)
\]

です。

現行記録として使っている表では

\[
N(16,4)\ge14640
\]

なので、直径 4 を証明できれば

\[
14848-14640=208
\]

の更新になります。

構成の形は：

\[
V(G)=V(C)\times \mathbb F_4^4.
\]

controller \(C\) は 4-regular で、各頂点から 4 つの directed symbols

\[
a,\ a^{-1},\ b,\ b^{-1}
\]

に対応する辺が出る inverse-labelled controller とします。

fiber 側には、各 symbol \(s\) に affine control

\[
x\mapsto A_sx+\lambda b_s,\qquad \lambda\in\mathbb F_4
\]

を割り当てます。

今回見つけたのは、次の性質を持つ control data です。

\[
\boxed{
\text{任意の reduced word }s_1s_2s_3s_4
\text{ に対して、}
}
\]

\[
\boxed{
\lambda_1,\lambda_2,\lambda_3,\lambda_4\in\mathbb F_4
\text{ の選択で }\mathbb F_4^4\text{ 全体を一意に覆う。}
}
\]

言い換えると、任意の reduced length-4 controller route が、fiber 上では完全な coordinate chart になります。

これは大きいです。前回までの rank-controller は「多数の path の和集合で fiber を覆るか」という coupon-collector 的な構造でした。今回は違って、

\[
\boxed{
1\text{ route}=4^4=256\text{ 個の fiber target 全部}
}
\]

を決定的に覆います。

この点では、数学的な勝算の核が実際に確認できました。

---

## 2. したがって、残る問題は controller だけ

この fiber code があるので、次の controller が作れれば直ちに新記録です。

\[
\boxed{
58\text{ 頂点の inverse-labelled }4\text{-regular controller }C
}
\]

で、任意の ordered pair \((u,v)\) に対して、

\[
u \xrightarrow{\text{reduced word of length }4} v
\]

となる reduced word が存在する。

これがあれば、最終グラフは

\[
|V(G)|=58\cdot4^4=58\cdot256=14848,
\]

\[
\Delta(G)=4\cdot4=16,
\]

\[
\operatorname{diam}(G)\le4.
\]

つまり、

\[
\boxed{N(16,4)\ge14848}
\]

です。

---

## 3. controller 側の実験結果

ここはまだ失敗です。

### random inverse-labelled controller

58 点上の 2 つの permutation \(P,Q\) を取り、

\[
a=P,\quad a^{-1}=P^{-1},\quad b=Q,\quad b^{-1}=Q^{-1}
\]

で controller を作るランダム実験をしました。

reduced word length 4 は

\[
4\cdot3^3=108
\]

個あります。各始点から 108 個の endpoint が出るので、58 頂点を覆う余裕は一応あります。

しかしランダムでは全く足りませんでした。観測最良でも、ordered pair 全体で

\[
366
\]

個の missing pair が残りました。

### random 4-regular controller

inverse-labelled ではない通常の 58 頂点 4-regular graph でも、exact nonbacktracking length-4 endpoint coverage を調べました。

こちらも最良観測で missing ordered pair は

\[
344
\]

程度でした。

### circulant controller

\[
\mathbb Z_h
\]

上の 4-regular circulant

\[
\{\pm1,\pm s\}
\]

も調べましたが、exact reduced length-4 の endpoint 集合は最大でも 25 程度で、58 頂点を覆えませんでした。

したがって、

\[
\boxed{
\text{controller はランダムや単純 circulant では作れない}
}
\]

です。

---

## 4. 今回の意味

今回の結果は「また失敗」ではなく、かなり重要な分解です。

前回までの候補は、失敗すると

\[
\text{fiber 側が弱いのか、controller 側が弱いのか}
\]

が混ざっていました。

今回は明確です。

\[
\boxed{
\text{fiber 側は成功}
}
\]

\[
\boxed{
\text{controller 側が未解決}
}
\]

です。

つまり、この原理を続けるなら、巨大グラフを作る必要はありません。次の小問題だけを解けばよいです。

\[
\boxed{
58\text{ 点の inverse-labelled }4\text{-regular automaton で、}
}
\]

\[
\boxed{
\text{全 ordered pair を reduced word length }4\text{ で覆うものを作る。}
}
\]

これはかなり小さく、しかも明確な有限設計問題です。

---

## 5. 数学的に見た評価

この方向には、前回の projective rank-controller よりは明確な事前根拠があります。

理由は：

\[
\boxed{
1\text{ 本の route が fiber 全体を覆う}
}
\]

からです。

これは random regular graph 的な「たくさんの path がたまたま全体を覆う」ではありません。controller route さえあれば、fiber target は線形可制御性で完全に指定できます。

一方で、controller 側については、まだ数学的な構成原理が足りません。ランダムや circulant が失敗したので、次に必要なのは

\[
\boxed{
\text{exact reduced-word covering controller}
}
\]

を作る新しい設計です。

ここを作れないなら、この方向も止めるべきです。  
ただし、今回は少なくとも「fiber chart 原理」自体は実証できたので、完全破棄ではなく、controller 設計に問題を絞る価値があります。

---

## 次に集中すべきこと

次は大グラフ探索ではなく、次の controller 設計だけに集中します。

\[
\boxed{
58\text{ 頂点、4-symbol inverse automaton、reduced length }4\text{ の完全被覆}
}
\]

候補としては、ランダム permutation や circulant ではなく、

\[
\text{reduced words 108 個を、58 頂点への balanced covering array として配置する}
\]

ような controller を設計する必要があります。

現時点の状態を一言で言うと：

\[
\boxed{
\text{新原理の fiber 側は通った。記録化には controller 側の新設計が必要。}
}
\]

---

## Turn 109 (Round 025) — 🧑 USER

_2026-05-25 14:08:24 UTC_

良い進展です。
controller側も、闇雲に試すのではなく、数学的に勝算がありそうなアイデアをまずは立ち止まって考えることが重要だと思います。
続けてください。

---

## Turn 110 (Round 025) — 🤖 ASSISTANT

_2026-05-25 14:09:01 UTC_  ·  model: `gpt-5-5-pro`

ここは controller 問題だけに絞り、巨大グラフには触れません。58 点を 108 個の reduced word で覆う条件を数式化し、ランダムではなく勝算がある設計原理だけを残します。

---

## Turn 111 (Round 025) — 🤖 ASSISTANT

_2026-05-25 14:12:16 UTC_  ·  model: `gpt-5-5-pro`

さらに、fiber chart と結合するには exact length 4 が必要なので、単なる到達性ではなく、108 個の reduced word を58点へ構造的に配る設計として扱います。

---

## Turn 112 (Round 026) — 🧑 USER

_2026-05-25 14:12:16 UTC_

現在の58頂点の課題に対しては、それが数学的に勝算がありそうならば、既存のアイデアを使用しても良いです。

---

## Turn 113 (Round 026) — 🤖 ASSISTANT

_2026-05-25 14:15:32 UTC_  ·  model: `gpt-5-5-pro`

この条件は、2つの置換 \(P,Q\) の長さ4 reduced words による permutation-covering 問題として見ます。ランダムで数百 missing まで来るのは、108対58の被覆余裕がぎりぎりあるためです。

---

## Turn 114 (Round 026) — 🤖 ASSISTANT

_2026-05-25 14:47:53 UTC_  ·  model: `gpt-5-5-pro`

はい。ここでは controller 側を「ランダムな 2 置換を増やして探す」のではなく、**exact length-4 route coverage を証明書として持てる小さい構造**に落としました。

成果物はこちらです。

[phase16_controller_design_artifacts.zip](sandbox:/mnt/data/phase16_controller_design_artifacts.zip)

## 立ち止まって考えた結論

現在の目的は、前回見つけた fiber 側の universal chart と組み合わせるための controller です。

必要条件は：

\[
\boxed{
\text{4-regular controller } C
\text{ で、任意の ordered pair }(u,v)
\text{ に exact length }4
\text{ の nonbacktracking walk がある}
}
\]

これがあれば、前回の GF(4)\(^4\) fiber chart により、

\[
|V(G)|=|V(C)|\cdot 4^4
\]

の degree 16, diameter 4 グラフができます。

現行記録として使っている値は

\[
N(16,4)\ge 14640.
\]

したがって controller は

\[
|V(C)|\ge 58
\]

なら記録更新候補になります。

前回は 58 頂点のランダム inverse-labelled controller を試しましたが、これは数学的には弱いです。なぜなら、108 個の reduced words が 58 頂点を偶然覆うことに期待しているだけだからです。

そこで今回は controller 側を、**小さい base graph の voltage lift** として設計する方針に切り替えました。これは current 58-vertex controller subproblem については、ユーザーさんが許可してくれた「既存のアイデア」の利用です。

---

## 新 controller 方針：\(K_5\) の order-12 voltage lift

一番自然な base は

\[
K_5.
\]

これは 4-regular です。  
order 12 の voltage group \(H\) で regular lift すると、controller 頂点数は

\[
5\cdot 12 = 60.
\]

すると最終グラフは

\[
60\cdot4^4=60\cdot256=15360
\]

頂点になります。  
したがって、controller 条件が成立すれば

\[
\boxed{
N(16,4)\ge15360
}
\]

となり、現行 14640 を

\[
720
\]

更新します。

---

## なぜこれは数学的に勝算があるか

\(K_5\) では、任意の base ordered pair \((i,j)\) に対して、長さ 4 の nonbacktracking base walk が十分たくさんあります。

具体的に数えると：

\[
i\ne j:\quad 21\text{ 本},
\]

\[
i=j:\quad 24\text{ 本}.
\]

voltage lift では、base walk の voltage 積が fiber 内の移動量を決めます。  
したがって、必要な条件は：

\[
\boxed{
\text{各 base pair }(i,j)\text{ について、}
}
\]

\[
\boxed{
21\text{ または }24\text{ 個の length-4 voltage products が }
H
\text{ 全体を覆う。}
}
\]

ここで

\[
|H|=12.
\]

つまり、各 base pair ごとに 21〜24 個の候補で 12 個の group elements を覆えばよい。  
これは、前の projective rank-controller のような coupon-collector 的不足とは違います。1 controller pair ごとに十分な余裕があり、成功すれば coverage certificate が非常に小さく書けます。

この方針の良い点は、controller の exact route coverage がランダム BFS ではなく、

\[
\boxed{
\text{25 個の base-pair それぞれで voltage products が }H\text{ を覆う}
}
\]

という有限証明に落ちることです。

---

## ここまで試した結果

今回は短時間で次を検査しました。

### 1. \(H=\mathbb Z/12\mathbb Z\)

cyclic voltage です。  
10 本の \(K_5\) edge に mod 12 voltage を割り当てます。

結果：

\[
\text{best total missing residue constraints}=7.
\]

つまり、25 個の base pair \(\times\) 12 residue の合計 300 条件のうち、最良候補でも 7 個が漏れました。

かなり近いですが、証明済み controller ではありません。

### 2. \(H=A_4\)

非可換 order-12 group も試しました。  
非可換 voltage の方が path products の混ざり方が豊かなので、cyclic より勝算があると見て試しました。

結果：

\[
\text{best total missing group constraints}\approx 10.
\]

こちらも近いですが、まだ certificate は出ていません。

### 3. \(D_6\), \(C_{12}\), \(C_3\times C_4\), \(C_2\times C_6\)

同じ \(K_5\) voltage lift で試しましたが、今のところ \(\mathbb Z/12\) と \(A_4\) より良い証明候補は出ていません。

---

## 今回の判断

この controller 方針は、前回のランダム permutation controller より数学的にずっと筋が良いです。

理由は：

\[
\boxed{
K_5\text{ の base walk 数 }21,24
\text{ が、fiber group size }12
\text{ を十分に上回っている}
}
\]

からです。

また、成功条件が「巨大な endpoint BFS」ではなく、

\[
\boxed{
25\text{ 個の小さい voltage product set が }H\text{ を覆うか}
}
\]

に縮約されます。

ただし、現時点では

\[
K_5\times H,\quad |H|=12
\]

はかなり tight で、数個の漏れが残っています。  
これは「惜しいから局所修復で押す」というより、次に数学的に取るべき道ははっきりしています。

---

## 次に進むべき controller 設計

### 候補 A：\(K_5\) base は維持し、order-12 group を変える

order 12 の全 group で系統的に検査する。  
特に \(A_4\) はまだ有望です。非可換 product が path set を広げるので、単なる cyclic より理屈上は良いです。

ただし、現時点の試行では certificate 未達です。

### 候補 B：base graph を少し大きくして slack を増やす

controller 頂点数は 58 以上ならよいので、60 にこだわる必要はありません。

たとえば

\[
|V(C)|=64,\ 72,\ 80
\]

でも最終頂点数は

\[
64\cdot256=16384,
\]

\[
72\cdot256=18432,
\]

\[
80\cdot256=20480
\]

となり、いずれも \((16,4)\) の現行記録を超えます。

この場合、base graph \(B\) を 4-regular にして、voltage group \(H\) のサイズを小さくすればよいです。重要なのは、各 base pair に対する length-4 nonbacktracking walk 数が \(|H|\) を十分上回ることです。

つまり、次は次の条件を満たす small base を探すべきです。

\[
\boxed{
B\text{ は 4-regular},
\qquad
|V(B)|\cdot |H|\ge58,
}
\]

\[
\boxed{
\forall i,j,\quad
\#\mathrm{NBWalk}_4^B(i,j)\ge |H|
\text{ に十分な余裕がある。}
}
\]

この条件があるので、闇雲ではありません。  
base walk count が足りないものは最初から捨てられます。

### 候補 C：既存の degree-4 diameter-4 large graphを controller として使う

今回の subproblem に限って既存アイデアを許可するなら、既存の \((4,4)\) large graph を controller として使うのも合理的です。

ただし必要なのは普通の diameter 4 ではなく、

\[
\boxed{
\text{exact length-4 nonbacktracking walk が全 ordered pair にある}
}
\]

ことです。

既存の \((4,4)\) graph は near-Moore 的なので、ここはかなり調べる価値があります。もし 58 頂点以上の既存 controller でこの性質が確認できれば、前回の fiber chart と直ちに合成できます。

---

## 現時点の本線

私は次を本線にします。

\[
\boxed{
\text{small voltage-lift controller}
+
\text{GF(4)}^4\text{ universal chart}
}
\]

最初の具体ターゲットは：

\[
\boxed{
K_5\text{ の order-12 voltage lift}
}
\]

または、その少し緩い版として

\[
\boxed{
4\text{-regular small base }B
\text{ の voltage lift with }|V(B)||H|\in[60,80].
}
\]

これなら、controller 側も数学的な勝算があります。  
「108 個の words が偶然 58 点を覆う」ではなく、

\[
\text{base walk family の voltage products が小さい group を覆う}
\]

という明確な被覆設計になっているからです。

まだ controller certificate は得られていませんが、進むべき方向はかなり整理されました。

---

## Turn 115 (Round 027) — 🧑 USER

_2026-05-25 14:54:28 UTC_

今回の subproblem に限って既存アイデアを許可します。
ただし依然として、闇雲に試すのではなく、事前に数学的に勝算がありそうと思える理由のあるアイデアを重視することは忘れないでください。
進めてください。

---

## Turn 116 (Round 027) — 🤖 ASSISTANT

_2026-05-25 14:54:58 UTC_  ·  model: `gpt-5-5-pro`

Controller サブ問題に限定し、既存の small-base/voltage 型を使いつつも、length-4 非戻り walk 数と群被覆余裕で事前に絞った証明可能な候補だけを調べます。巨大グラフ生成ではなく、58〜80 頂点程度の controller certificate を作る方針で進めます。

---

## Turn 117 (Round 027) — 🤖 ASSISTANT

_2026-05-25 14:58:16 UTC_  ·  model: `gpt-5-5-pro`

まず \(K_5\) の order-12 lift はゲージ固定で有限全列挙に落とし、標準的な全群では完全被覆が出ないと分かりました。次は群サイズを下げ、base walk 数の余裕を増やす方向に移ります。

---

## Turn 118 (Round 027) — 🤖 ASSISTANT

_2026-05-25 15:07:39 UTC_  ·  model: `gpt-5-5-pro`

60点ぴったりの \(K_5\) lift は tight すぎるため、同じ証明形式のまま controller を64〜100点まで広げます。既存の4-regular diameter系 controllerや余裕ある small voltage liftを、exact length-4被覆の証明書として検査します。

---

## Turn 119 (Round 027) — 🤖 ASSISTANT

_2026-05-25 15:35:48 UTC_  ·  model: `gpt-5-5-pro`

進めました。結論から言うと、**まだ controller は完成していません**。ただし今回は、闇雲な試行ではなく、数学的に筋のある controller family をかなり強く切り分けました。

成果物はこちらです。

[phase17_controller_existing_ideas.zip](sandbox:/mnt/data/phase17_controller_existing_ideas.zip)

## 今回の焦点

前回までに fiber 側はかなり良い証明書がありました。

\[
\mathbb F_4^4
\]

上で、任意の reduced word

\[
s_1s_2s_3s_4
\]

に対して controllability matrix が full rank になる control data が見つかっています。つまり、controller に exact length-4 nonbacktracking route が 1 本あれば、その 1 本の route だけで fiber の

\[
4^4=256
\]

個の target を全部 routing できます。

したがって残る課題は：

\[
\boxed{
|C|\ge58\text{ の }4\text{-regular controller }C
\text{ で、任意の ordered pair }(u,v)
\text{ に exact length-4 nonbacktracking walk がある}
}
\]

です。

この controller ができれば、

\[
|V(G)|=|C|\cdot256,\qquad \Delta(G)=16,\qquad \operatorname{diam}(G)\le4.
\]

特に \(|C|=60\) なら

\[
N(16,4)\ge15360,
\]

現行の 14640 を 720 更新します。

## 数学的に勝算がある controller family

今回まず選んだのは、

\[
\boxed{
K_5\text{ の order-12 voltage lift}
}
\]

です。

理由は明確です。\(K_5\) は 4-regular で、任意の ordered base pair \((i,j)\) について exact length-4 nonbacktracking base walk が十分あります。

\[
i\ne j:\ 21\text{ 本},\qquad i=j:\ 24\text{ 本}.
\]

order 12 の voltage group \(H\) で lift すると controller は

\[
5\cdot12=60
\]

頂点になります。必要条件は、各 base pair について、その 21 または 24 本の path voltage product が \(H\) 全体を覆うことです。

これは巨大 BFS ではなく、

\[
25\text{ 個の small product-cover certificate}
\]

に落ちるので、現在の subproblem ではかなり良い既存アイデアの使い方です。

## 結果 1：\(K_5\times H,\ |H|=12\) は全滅

switching により \(K_5\) の spanning tree の voltage を単位元に固定できます。残る自由変数は 6 本だけです。したがって各群について

\[
12^6=2,985,984
\]

通りを全探索できます。

今回、order 12 の主要な群を全探索しました。

| voltage group \(H\) | best total missing products |
|---|---:|
| \(C_{12}\) | 7 |
| \(C_6\times C_2\) | 10 |
| \(D_6\) | 14 |
| \(A_4\) | 10 |
| \(\mathrm{Dic}_3\) | 14 |

したがって、

\[
\boxed{
K_5\text{ base} + |H|=12\text{ regular voltage lift}
}
\]

では 60 頂点 controller は作れません。

これは単なる探索失敗ではなく、switching reduction 後の完全探索なので、かなり強い否定結果です。

## 結果 2：cyclic \(K_5\) voltage の近傍も否定的

同じく \(K_5\) base で cyclic voltage \(C_m\) を調べました。

| \(m\) | controller size \(5m\) | best missing |
|---:|---:|---:|
| 11 | 55 | 2 |
| 12 | 60 | 7 |
| 13 | 65 | 10 |
| 14 | 70 | 19 |

\(m=11\) はかなり近いですが、55 頂点なので記録更新に必要な 58 頂点に届きません。\(m=12\) はサイズとしてちょうど良いですが、完全探索で missing 7 が残ります。

## 結果 3：既存の Exoo-98 は controller としては使えない

既存の \((4,4)\) record graph、Exoo-98 も検査しました。Comellas の表では Exoo-98 は degree 4, diameter 4, 98 頂点の現行最大既知グラフとして掲載されています。citeturn999800view0

ただし、必要なのは ordinary diameter 4 ではなく、

\[
\text{exact length-4 nonbacktracking coverage}
\]

です。Exoo-98 の adjacency list を使って調べると：

\[
\min_v |\{ \text{exact NB length-4 endpoints from }v\}|=61/98,
\]

\[
\text{missing ordered pairs}=3010.
\]

つまり、diameter 4 graph であることは controller 条件には全然足りません。これは重要な切り分けです。

## 結果 4：\(H'_3\) 由来の \((4,5)=364\) graph も、そのままでは別問題

Comellas の diameter 5 ページには、\((4,5)=364\) の Delorme/Farhi 型 graph が掲載されており、これは generalized hexagon \(H'_3\) の incidence graph の polarity quotient です。citeturn286849view0turn319087view0

ただしこの graph は girth 6 なので、同一 controller vertex への exact nonbacktracking length-5 closed route が存在しません。したがって、単純に \(k=5\) controller として使うには不適です。

## 現時点の判断

今回で、かなり自然な既存アイデアの第一候補は潰れました。

\[
\boxed{
K_5\text{ order-12 voltage controller は不可能}
}
\]

これは痛いですが、良い否定結果です。なぜなら \(K_5\) は 4-regular base として最も小さく、length-4 path count も最大級で、60 頂点 controller を狙う最も美しい候補だったからです。

一方、fiber-chart 原理自体はまだ生きています。問題は controller だけです。

次に数学的に進める価値があるのは：

\[
\boxed{
|B|=8,\ |H|=8
}
\]

または

\[
\boxed{
|B|=10,\ |H|=6
}
\]

のような、少し大きな 4-regular base \(B\) と小さな voltage group \(H\) の組です。

理由は、\(K_5,|H|=12\) より group coverage は楽になるからです。たとえば \(|B|=8, |H|=8\) なら controller は 64 頂点で、記録更新には十分です。必要なのは、各 base pair について length-4 NB walk products が \(H\) を覆うこと。base \(B\) はランダムに選ぶのではなく、

\[
\min_{i,j}\#\mathrm{NBWalk}_4^B(i,j)\ge |H|
\]

かつ counts が均一なものだけを候補にすべきです。

現時点では新記録未達ですが、探索空間はかなり絞れました。次は **path-count regular な 8〜10 頂点 4-regular base の分類・選別**に進むのが一番筋が良いです。

---

## Turn 120 (Round 028) — 🧑 USER

_2026-05-26 01:08:28 UTC_

今取り組んでいる問題の定義を教えてください。
どのようなグラフを構成できれば良いのかを厳密に知りたいです。

---

## Turn 121 (Round 028) — 🤖 ASSISTANT

_2026-05-26 01:08:58 UTC_  ·  model: `gpt-5-5-pro`

整理して、いま解くべき小さい controller 問題と、それが元の degree-diameter graph にどうつながるかを厳密に書きます。

---

## Turn 122 (Round 028) — 🤖 ASSISTANT

_2026-05-26 01:12:39 UTC_  ·  model: `gpt-5-5-pro`

はい。今取り組んでいる問題を、**最終的に欲しいグラフ**と、そこへ到達するための**controller 部分問題**に分けて厳密に書きます。

## 最終目標

今の構成方針で狙っているのは、単純無向グラフ

\[
G
\]

で、

\[
\Delta(G)\le 16,\qquad \operatorname{diam}(G)\le 4
\]

かつ

\[
|V(G)|>14640
\]

を満たすものです。

会話内で使っている現行基準では

\[
N(16,4)\ge14640
\]

なので、これを超えれば \((d,k)=(16,4)\) の新記録候補になります。

現在の構成では、もし controller の頂点数を \(h\) とすると、最終グラフの頂点数は

\[
|V(G)|=256h.
\]

したがって

\[
256h>14640
\]

つまり

\[
h\ge58
\]

が必要です。

---

# 1. 現在の構成テンプレート

有限体

\[
\mathbb F_4
\]

上の 4 次元ベクトル空間

\[
X=\mathbb F_4^4
\]

を fiber とします。

controller graph を

\[
C
\]

とします。これは 4-正則単純無向グラフです。

最終グラフ \(G\) の頂点集合は

\[
V(G)=V(C)\times X.
\]

つまり controller の各頂点 \(u\) を、256 個の fiber

\[
\{u\}\times \mathbb F_4^4
\]

に膨らませます。

---

# 2. controller に必要な構造

controller \(C\) は 4-正則なので、各頂点には 4 本の辺が出ています。

これを 2 つの 2-factor に分解し、それぞれを向き付き cycle として向きを付けます。すると、各有向辺に

\[
a,\ a^{-1},\ b,\ b^{-1}
\]

のいずれかのラベルを付けられます。

記号集合を

\[
S=\{a,a^{-1},b,b^{-1}\}
\]

とします。

辺を逆向きに見るとラベルも逆元になります。つまり

\[
\sigma(\bar e)=\sigma(e)^{-1}.
\]

このラベル付けにより、controller 上の nonbacktracking walk は、ラベル列として reduced word を与えます。  
ここで reduced とは、連続して

\[
ss^{-1}
\]

が現れない、という意味です。

---

# 3. fiber 側の制御データ

各ラベル

\[
s\in S
\]

に対して、

\[
A_s\in GL(4,4),\qquad b_s\in\mathbb F_4^4
\]

を割り当てます。

有向 controller edge

\[
e:u\to v
\]

のラベルが

\[
\sigma(e)=s
\]

であるとき、最終グラフ \(G\) では、各

\[
\lambda\in\mathbb F_4
\]

について

\[
(u,x)\sim (v,A_sx+\lambda b_s)
\]

という辺を張ります。

つまり、controller の 1 本の辺は、fiber 方向に 4 本分の選択肢を持ちます。

controller の次数は 4 なので、最終グラフの最大次数は

\[
4\cdot4=16.
\]

逆向き辺と矛盾しないように、

\[
A_{s^{-1}}=A_s^{-1},
\]

\[
b_{s^{-1}}=A_s^{-1}b_s
\]

を満たすように取ります。標数 2 なので符号の問題は出ません。

---

# 4. fiber chart 条件

長さ 4 の reduced word

\[
w=s_1s_2s_3s_4
\]

を固定します。

この word に沿って fiber を動かすと、

\[
x_0
\mapsto
A_{s_1}x_0+\lambda_1b_{s_1}
\mapsto
\cdots
\mapsto
x_4
\]

となります。

展開すると、

\[
x_4
=
A_wx_0
+
\lambda_1 A_{s_4}A_{s_3}A_{s_2}b_{s_1}
+
\lambda_2 A_{s_4}A_{s_3}b_{s_2}
+
\lambda_3 A_{s_4}b_{s_3}
+
\lambda_4 b_{s_4}.
\]

ここで

\[
A_w=A_{s_4}A_{s_3}A_{s_2}A_{s_1}.
\]

したがって、word \(w\) が fiber 全体を制御できる条件は、4 本の列ベクトル

\[
A_{s_4}A_{s_3}A_{s_2}b_{s_1},
\quad
A_{s_4}A_{s_3}b_{s_2},
\quad
A_{s_4}b_{s_3},
\quad
b_{s_4}
\]

が \(\mathbb F_4^4\) の基底になることです。

つまり行列

\[
M_w=
\begin{bmatrix}
A_{s_4}A_{s_3}A_{s_2}b_{s_1}
&
A_{s_4}A_{s_3}b_{s_2}
&
A_{s_4}b_{s_3}
&
b_{s_4}
\end{bmatrix}
\]

が正則であること。

前回までに、次を満たす control data は見つかっています。

\[
\boxed{
\text{任意の reduced word }w=s_1s_2s_3s_4
\text{ について }M_w\text{ は正則。}
}
\]

これが fiber 側の universal chart 条件です。

この条件があると、任意の fixed route label

\[
s_1s_2s_3s_4
\]

に対して、任意の始点 fiber \(x\) と任意の終点 fiber \(y\) について、

\[
(u,x)\to(v,y)
\]

を実現する

\[
(\lambda_1,\lambda_2,\lambda_3,\lambda_4)\in\mathbb F_4^4
\]

が一意に存在します。

つまり：

\[
\boxed{
1\text{ 本の controller route}
=
256\text{ 個の fiber target 全部を覆う。}
}
\]

---

# 5. controller 側の必要十分な目標条件

fiber 側はもう通っています。  
したがって、今残っている本質的な問題は controller だけです。

必要な controller 条件は：

\[
\boxed{
\forall u,v\in V(C),\quad
\exists\text{ exact length }4\text{ nonbacktracking walk }u\leadsto v.
}
\]

厳密に書くと、任意の ordered pair

\[
(u,v)\in V(C)^2
\]

に対して、

\[
u=u_0,u_1,u_2,u_3,u_4=v
\]

で、

\[
u_i\sim u_{i+1}
\]

かつ

\[
u_{i+1}\ne u_{i-1}
\qquad (i=1,2,3)
\]

を満たす列が存在することです。

この条件を

\[
\mathrm{NB}_4(C)\text{ が全 ordered pair を覆う}
\]

と呼べます。

行列で言えば、

\[
N_4(u,v)
=
\#\{
u=u_0,u_1,u_2,u_3,u_4=v:
u_{i+1}\ne u_{i-1}
\}
\]

としたとき、

\[
\boxed{
N_4(u,v)>0
\quad
\text{for all }u,v.
}
\]

これが今取り組んでいる controller 問題の定義です。

---

# 6. controller ができればなぜ直径 4 になるか

任意の最終グラフの 2 頂点

\[
(u,x),(v,y)\in V(C)\times\mathbb F_4^4
\]

を取ります。

controller 条件により、

\[
u=u_0,u_1,u_2,u_3,u_4=v
\]

という exact length-4 nonbacktracking walk が存在します。

この walk のラベル列を

\[
s_1s_2s_3s_4
\]

とします。nonbacktracking なのでこれは reduced word です。

fiber chart 条件により、任意の \(x,y\) に対して、

\[
x\mapsto y
\]

を実現する

\[
\lambda_1,\lambda_2,\lambda_3,\lambda_4\in\mathbb F_4
\]

が存在します。

したがって \(G\) では、

\[
(u,x)
\to
(u_1,x_1)
\to
(u_2,x_2)
\to
(u_3,x_3)
\to
(v,y)
\]

という長さ 4 の path が存在します。

よって

\[
\operatorname{diam}(G)\le4.
\]

---

# 7. したがって、今本当に探しているもの

現在の core subproblem はこれです。

\[
\boxed{
58\le h\le108
\text{ の単純 }4\text{-正則グラフ }C
}
\]

で、

\[
\boxed{
\forall u,v\in V(C),\quad
N_4(u,v)>0
}
\]

を満たすもの。

上限 \(h\le108\) は、1 頂点から出る exact length-4 nonbacktracking walk の本数が最大で

\[
4\cdot3^3=108
\]

だからです。これより大きい controller は、この条件では全頂点を覆れません。

もし \(h=58\) なら最終グラフは

\[
58\cdot256=14848
\]

頂点。

もし \(h=60\) なら

\[
60\cdot256=15360
\]

頂点。

どちらも現行基準

\[
14640
\]

を超えます。

---

# 8. voltage-lift 版の厳密な定義

いま controller を作るために使っているサブ方針は、4-正則 base graph \(B\) の voltage lift です。

base graph \(B\) を 4-正則単純無向グラフ、有限群を \(H\) とします。

各有向辺 \(e\) に voltage

\[
\phi(e)\in H
\]

を割り当て、

\[
\phi(\bar e)=\phi(e)^{-1}
\]

を満たすようにします。

lift controller \(C\) の頂点は

\[
V(C)=V(B)\times H.
\]

辺は、base の有向辺 \(e:i\to j\) に対して

\[
(i,g)\sim(j,g\phi(e))
\]

で定義します。

このとき

\[
|V(C)|=|V(B)|\cdot |H|.
\]

voltage-lift controller が目的条件を満たすための十分かつ自然な条件は：

\[
\boxed{
\forall i,j\in V(B),\quad
\{
\phi(e_1)\phi(e_2)\phi(e_3)\phi(e_4):
e_1e_2e_3e_4
\text{ is an exact length-4 NB walk }i\to j
\}
=H.
}
\]

つまり、base graph 上で \(i\) から \(j\) への exact length-4 nonbacktracking walk たちの voltage product が、群 \(H\) 全体を覆うことです。

これが成立すれば、lift \(C\) では任意の

\[
(i,g),(j,h)
\]

に対して、差分

\[
g^{-1}h\in H
\]

を実現する length-4 nonbacktracking walk が存在します。

したがって \(C\) は controller 条件を満たします。

---

# 9. 今の探索対象を一文で言うと

いま構成できればよいのは、次のどちらかです。

### 直接 controller 版

\[
\boxed{
58\le |V(C)|\le108
\text{ の単純 }4\text{-正則グラフ }C
\text{ で、任意の ordered pair が exact length-4 nonbacktracking walk で結ばれるもの。}
}
\]

### voltage-lift certificate 版

\[
\boxed{
4\text{-正則 base graph }B
\text{ と有限群 }H
\text{ と voltage }\phi
\text{ で、}
}
\]

\[
\boxed{
|V(B)||H|\ge58
\text{ かつ、各 base pair の length-4 NB voltage products が }H\text{ 全体を覆うもの。}
}
\]

これができれば、前回見つけた \(\mathbb F_4^4\) universal chart と合成して、

\[
\boxed{
\Delta\le16,\quad \operatorname{diam}\le4,\quad |V|=256|V(C)|>14640
}
\]

の単純無向グラフが得られます。

---

## Turn 123 (Round 029) — 🧑 USER

_2026-05-26 01:37:30 UTC_

ありがとうございます。
問題に引き続き取り組んでください。

---

## Turn 124 (Round 029) — 🤖 ASSISTANT

_2026-05-26 01:37:51 UTC_  ·  model: `gpt-5-5-pro`

まず controller 問題だけに絞り、証明書を小さくできる voltage-lift 型から、数学的に勝算のある base を選別して進めます。

---

## Turn 125 (Round 029) — 🤖 ASSISTANT

_2026-05-26 01:41:03 UTC_  ·  model: `gpt-5-5-pro`

特に \(K_5\) lift が潰れたため、次は小さい 4-正則 base の path-count 条件と \(P_4(A)>0\) の行列条件で候補を絞ります。

---

## Turn 126 (Round 029) — 🤖 ASSISTANT

_2026-05-26 02:08:24 UTC_  ·  model: `gpt-5-5-pro`

続けました。今回も **controller はまだ完成していません**。ただし、前回よりはっきりと「どの既存アイデアが有望で、どこまで行って、どこで詰まったか」を切り分けました。

成果物はこちらです。

[phase18_controller_followup.zip](sandbox:/mnt/data/phase18_controller_followup.zip)

## 現在の core 問題

いま必要なのは、次の controller です。

\[
58\le |V(C)|\le108
\]

の単純 4-正則グラフ \(C\) で、任意の ordered pair \((u,v)\) に対して、

\[
u=u_0,u_1,u_2,u_3,u_4=v
\]

かつ

\[
u_{i+1}\ne u_{i-1}\qquad(i=1,2,3)
\]

を満たす exact length-4 nonbacktracking walk が存在するもの。

これができれば、前に見つけた \(\mathbb F_4^4\) universal fiber chart と合成して、

\[
\Delta\le16,\qquad \operatorname{diam}\le4,\qquad |V|=256|V(C)|
\]

のグラフが得られます。特に \(|V(C)|\ge58\) なら、

\[
256\cdot58=14848>14640
\]

なので、\((16,4)\) の新記録候補になります。

---

## 今回の方針

今回の subproblem では既存アイデア使用が許可されたので、controller 側については既存の強力な構成原理を使いました。ただし、闇雲ではなく、次の事前基準を置きました。

controller を voltage lift として作る場合、base graph \(B\)、群 \(H\)、voltage \(\phi\) に対して、

\[
|V(C)|=|V(B)||H|
\]

です。そして、各 base pair \((i,j)\) について、length-4 nonbacktracking base walk の voltage product が \(H\) 全体を覆えばよい。

つまり、見るべき量は

\[
\#\mathrm{NBWalk}_4^B(i,j)
\]

です。これが \(|H|\) より十分大きくない候補は、最初から見込み薄として捨てます。

---

## 1. 直接 58 頂点 controller 探索

まず比較用に、58 頂点 4-正則グラフを直接 edge-switch で探しました。

結果は、最良観測で

\[
\text{total missing ordered pairs}=130,
\]

\[
\text{max miss from one source}=4.
\]

つまりかなり近いですが、まだ

\[
N_4(u,v)>0\quad\forall u,v
\]

には届いていません。

これは「58 頂点が不可能」という証明ではありません。ただ、単なるランダム edge-switch で押し切るべき段階ではないと見ています。

---

## 2. \(K_5\) の 12-lift をさらに緩めた nonregular permutation lift

前回、\(K_5\) の order-12 **group voltage lift** は完全探索で不可能でした。

そこで今回は、group voltage より自由度の高い、

\[
K_5\text{ の arbitrary permutation }12\text{-lift}
\]

も試しました。

これは controller 頂点数

\[
5\cdot12=60
\]

なので、成功すれば最終グラフは

\[
60\cdot256=15360
\]

頂点になります。

数学的な勝算は一応あります。\(K_5\) では各 base pair に対して length-4 nonbacktracking walk が

\[
21\text{ または }24
\]

本あります。各 path product が fiber 上の permutation になるので、12 点 fiber を覆うには十分な本数に見えます。

しかし短い実験では、最良でも endpoint constraint の missing が

\[
194
\]

残りました。group voltage より自由度はありますが、「これはすぐ完成する」という感触ではありません。

この方向はまだ完全否定ではありませんが、構成原理としては少し局所最適化に寄りやすいので、主戦略にはしにくいです。

---

## 3. 8 頂点 base \(\times\) order-8 group

次に、base graph を \(K_5\) から少し大きくしました。

狙いは

\[
|V(B)|=8,\qquad |H|=8,
\]

なので controller は

\[
8\cdot8=64
\]

頂点。成功すれば最終グラフは

\[
64\cdot256=16384
\]

頂点です。

この候補の事前根拠は、8 頂点 4-正則 base の中に、任意の ordered pair に対して length-4 NB walk が少なくとも

\[
12
\]

本あるものが存在することです。つまり

\[
12>|H|=8
\]

で、voltage product coverage には余裕があります。

order 8 の群候補、特に \(C_8,D_4,Q_8,C_4\times C_2,C_2^3\) を想定して探索しました。

短い run では、\(C_8\) で最良

\[
\text{total missing group products}=28
\]

まで行きましたが、0 には届きませんでした。

この方向は \(K_5\times H_{12}\) より構造的には良い可能性があります。ただし、今回の run では certificate 未達です。

---

## 4. 10〜12 頂点 base \(\times\) 小さい cyclic group

さらに、group 側をもっと小さくして coverage を楽にする案を試しました。

### \(10\)-vertex base \(\times C_6\)

controller size は

\[
10\cdot6=60.
\]

ランダムな 10 頂点 4-正則 base では、良いものだと

\[
\min_{i,j}\#\mathrm{NBWalk}_4(i,j)\ge6
\]

以上になります。

短い探索では、最良

\[
\text{total missing}=20
\]

程度まで行きましたが、0 には届きませんでした。

### \(12\)-vertex base \(\times C_5\)

controller size は

\[
12\cdot5=60.
\]

これはかなり自然です。group が \(C_5\) と小さいので、各 base pair の products が 5 residue を覆ればよい。

今回、12 頂点 4-正則 base で

\[
\min_{i,j}\#\mathrm{NBWalk}_4(i,j)=7
\]

のものを見つけ、それに \(C_5\) voltage を試しました。

短い探索では、最良

\[
\text{total missing}=20
\]

でした。

ここも未達ですが、事前条件としては悪くありません。

---

## 現在の判断

まだ controller はできていません。

ただし、前回の

\[
K_5\text{ order-12 group voltage lift}
\]

が完全に潰れたあと、次に数学的に狙うべき範囲はかなり明確になりました。

今後の有望順位は：

\[
\boxed{
12\text{-vertex 4-regular base}\times C_5
}
\]

または

\[
\boxed{
10\text{-vertex 4-regular base}\times C_6
}
\]

です。

理由は、必要な group coverage が小さいからです。  
\(K_5\times H_{12}\) は base walk 数 21〜24 で group size 12 を覆る問題でした。一見余裕がありますが、完全探索で失敗しました。  
一方で、

\[
12\times C_5
\]

では group size が 5 なので、各 base pair の path products に求める条件はずっと軽くなります。

---

## 次にやるべきこと

次はランダムな base を次々変えるのではなく、base graph を次の条件で選別すべきです。

\[
\boxed{
\min_{i,j}\#\mathrm{NBWalk}_4^B(i,j)
\text{ が大きい}
}
\]

だけでなく、

\[
\boxed{
\text{各 }(i,j)\text{ の path family が edge-disjoint / voltage-independent に近い}
}
\]

こと。

単に path 数が 7 あるだけでは足りません。複数 path が同じ辺集合を似た形で使うと、cyclic voltage の product が同じ residue に偏ります。

なので次フェーズでは、base \(B\) を評価するスコアを

\[
\text{path count}
+
\text{path edge-incidence rank}
\]

に変えます。

特に \(C_5\) voltage の場合、各 path product は edge voltage の \(\mathbb F_5\)-線形和です。したがって、各 base pair \((i,j)\) について length-4 path の incidence vector が \(\mathbb F_5\) 上で多様である必要があります。

これはかなり良い切り口です。

\[
\boxed{
\text{base path incidence vectors が }\mathbb F_5\text{ 上で residue を覆りやすい base を選ぶ}
}
\]

という明確な数学的選別基準になります。

今の結論としては、controller 問題はまだ未解決ですが、次は

\[
\boxed{
12\text{-vertex base} + C_5\text{ voltage}
}
\]

に絞り、base の path-incidence rank 条件を使って進めるのが一番筋が良いです。

---

## Turn 127 (Round 030) — 🧑 USER

_2026-05-26 02:15:05 UTC_

つづきお願いします

---

## Turn 128 (Round 030) — 🤖 ASSISTANT

_2026-05-26 02:15:34 UTC_  ·  model: `gpt-5-5-pro`

今回は controller 証明書だけに絞り、12頂点 base＋\(C_5\) voltage の path-incidence rank を本線に、直接構成の可能性も必要条件で並行検査します。巨大な最終グラフはまだ作らず、exact length-4 nonbacktracking 全ペア到達を小さく詰めます。

---

## Turn 129 (Round 030) — 🤖 ASSISTANT

_2026-05-26 02:18:49 UTC_  ·  model: `gpt-5-5-pro`

条件を Hashimoto 行列の 4 乗による全正性として捉え直し、4-cycle を多く含む均一被覆型 controller を優先します。加えて、小型 Schreier/PGL(2,q) 作用も coverage 余裕のある既存候補として検査します。

---

## Turn 130 (Round 030) — 🤖 ASSISTANT

_2026-05-26 02:42:22 UTC_  ·  model: `gpt-5-5-pro`

進めました。今回も **controller 完成には至っていません**。ただし、かなり筋の良い新しい controller 方針が出ました。

成果物はこちらです。

[phase19_controller_lift_attempts.zip](sandbox:/mnt/data/phase19_controller_lift_attempts.zip)

## 今回の新しい方針：小さい controller を lift する

前回までの課題は、

\[
58\le |V(C)|\le108
\]

の 4-正則 controller \(C\) で、任意の ordered pair \((u,v)\) に exact length-4 nonbacktracking walk があるものを作ることでした。

今回、かなり自然な発想として、

\[
\boxed{
\text{小さい exact controller を作り、それを小さい voltage lift で 58 頂点以上に増やす}
}
\]

に切り替えました。

これは闇雲ではなく、数学的にかなり勝算があります。理由は、base が小さいほど、1 ordered pair あたりの length-4 nonbacktracking path 数が増えるからです。

1 頂点から出る exact length-4 nonbacktracking walk は最大で

\[
4\cdot3^3=108
\]

本あります。base の頂点数を \(h_0\) とすると、ordered pair あたりの平均 path 数は

\[
108/h_0
\]

です。

例えば \(h_0=30\) なら平均 3.6 本あります。これを 2-lift すれば 60 頂点 controller になります。必要なのは、各 base ordered pair に対して、length-4 path が 2-lift の両 fiber を打ち分けることです。

---

## 1. 30 頂点 base controller は作れた

まず、30 頂点の 4-正則グラフ \(B\) で、

\[
\forall u,v\in V(B),\quad N_4(u,v)>0
\]

を満たすものはすぐに見つかりました。

つまり、base 単体では exact length-4 nonbacktracking coverage を持っています。

この時点で、

\[
|V(B)|=30
\]

なので、もしこの \(B\) の \(\mathbb Z_2\)-voltage lift が成功すれば、

\[
|V(C)|=60
\]

の controller ができます。

すると最終グラフは

\[
60\cdot4^4=15360
\]

頂点になり、現行基準の

\[
N(16,4)\ge14640
\]

を

\[
720
\]

更新します。

---

## 2. ただし、その 30 頂点 base は 2-lift 不能

\(\mathbb Z_2\)-lift では、各 base edge に符号

\[
0/1
\]

を付けます。

base の length-4 path

\[
P=e_1e_2e_3e_4
\]

の lift parity は

\[
\sigma(P)=\sigma(e_1)+\sigma(e_2)+\sigma(e_3)+\sigma(e_4)\pmod2
\]

です。

任意の base ordered pair \((u,v)\) に対して、lift 後に両 fiber を到達するには、\(u\to v\) の length-4 paths の parity が

\[
0,1
\]

の両方を取る必要があります。

そのための最低条件は、各 \((u,v)\) に対して、length-4 path の edge-incidence mask が少なくとも 2 種類あることです。

今回見つけた 30 頂点 base では、

\[
64
\]

個の ordered pair がこの最低条件を満たしませんでした。つまり、それらの pair では path が 1 本しかない、または複数あっても mod-2 incidence が同じです。

したがって、この 30 頂点 base はどんな符号を付けても \(\mathbb Z_2\)-lift controller にはなりません。

これは良い否定結果です。単に random sign が失敗したのではなく、構造的に不可能です。

---

## 3. 29 頂点 base で 2-lift を狙うのがかなり有望

次に、2-lift 後にちょうど

\[
58
\]

頂点になる base size

\[
h_0=29
\]

を試しました。

必要条件は：

\[
\forall u,v,\quad
u\to v\text{ の exact length-4 NB path が存在}
\]

かつ

\[
\forall u,v,\quad
\text{mod-2 edge-incidence mask が少なくとも 2 種類}
\]

です。

探索結果はここまで来ました。

\[
\text{bad0}=0,\qquad \text{bad1}=26.
\]

ここで、

- bad0 = length-4 NB path が存在しない ordered pair 数
- bad1 = path はあるが、mod-2 incidence mask が 1 種類しかない ordered pair 数

です。

つまり、29 頂点 base については、全 ordered pair がすでに length-4 で覆われています。残る obstruction は

\[
26
\]

個の pair だけです。

これが消えれば、\(\mathbb Z_2\)-lift の符号設計に進めます。  
そしてそれが成功すれば、58 頂点 controller から

\[
58\cdot256=14848
\]

頂点の \((16,4)\) 新記録候補が得られます。

---

## 4. 小 base \(\times\) cyclic voltage も試した

2-lift の一般化として、

\[
|V(B)|\cdot m\ge58
\]

となる小さい cyclic voltage lift も試しました。

例えば：

\[
20\times C_3=60,
\]

\[
15\times C_4=60,
\]

\[
14\times C_5=70.
\]

この方針も数学的には自然です。base が小さいほど ordered pair あたりの path 数が増え、group size \(m\) が小さいほど voltage product coverage が楽になります。

短い探索結果は：

| base size | voltage group | controller size | best missing voltage conditions |
|---:|---:|---:|---:|
| 20 | \(C_3\) | 60 | 77 |
| 15 | \(C_4\) | 60 | 39 |
| 14 | \(C_5\) | 70 | 76 |

まだ certificate は出ていません。

現時点では、これらより

\[
29\text{-vertex base}+\mathbb Z_2\text{-lift}
\]

の方が一番近いです。理由は、残り obstruction が 26 個と明確で、かつ lift group が最小だからです。

---

## 5. 直接 58 頂点 controller 探索も更新

直接 58 頂点 4-正則 controller の edge-switch 探索も続けました。

現時点の best は：

\[
\text{total missing ordered pairs}=128,
\]

\[
\text{maximum miss from one source}=6.
\]

前回の 130 付近から少しだけ改善しましたが、まだ遠いです。

この方向は「あと少し」に見えるものの、数学的な構成証明が弱いので、今は主戦略にしません。主戦略は lift にします。

---

## 現時点の判断

一番有望なのは：

\[
\boxed{
29\text{ 頂点 4-正則 base}
+
\mathbb Z_2\text{-voltage lift}
}
\]

です。

理由は明確です。

1. 29 頂点 base を 2-lift すれば、ちょうど 58 頂点 controller になる。
2. 58 頂点 controller ができれば、前回の \(\mathbb F_4^4\) universal chart と合成して、
   \[
   N(16,4)\ge14848
   \]
   が出る。
3. 現在の best 29-base はすでに
   \[
   \text{bad0}=0
   \]
   で、全 ordered pair が exact length 4 で覆われている。
4. 残りは
   \[
   \text{bad1}=26
   \]
   の mod-2 path diversity obstruction だけ。

次は、29 頂点 base の探索目的をさらに絞って、

\[
\boxed{
\text{bad0}=0,\quad \text{bad1}=0
}
\]

を直接狙います。これが出たら、次に \(\mathbb Z_2\) 符号割当で全 pair の parity coverage を証明します。

---

## Turn 131 (Round 031) — 🧑 USER

_2026-05-26 03:37:18 UTC_

続けてください

---

## Turn 132 (Round 031) — 🤖 ASSISTANT

_2026-05-26 03:37:38 UTC_  ·  model: `gpt-5-5-pro`

29頂点 base + 2-lift を本線に絞り、まず bad0/bad1 を完全に消せる base の有無を確認します。通った場合だけ、符号割当まで小さな証明書として進めます。

---

## Turn 133 (Round 031) — 🤖 ASSISTANT

_2026-05-26 03:40:51 UTC_  ·  model: `gpt-5-5-pro`

既存候補の単純 edge-switch では bad1=26 から動かないため、NB4 条件を path-incidence の rank/分離条件として評価する方針に切り替えます。符号割当で本当に分離可能な base だけを残します。

---

## Turn 134 (Round 031) — 🤖 ASSISTANT

_2026-05-26 03:50:04 UTC_  ·  model: `gpt-5-5-pro`

追加検査では、best signed 29-base でも base pair 不足が3個、片側 parity のみが74個残り、base 自体の必要条件が未達です。並行して58頂点 controller 直接評価も進め、targeted 改善の有効性を見ます。

---

## Turn 135 (Round 031) — 🤖 ASSISTANT

_2026-05-26 04:13:06 UTC_  ·  model: `gpt-5-5-pro`

続けました。今回も **controller 完成には至っていません**。ただし、前回より少し前進し、同時にいくつかの自然な controller ルートをかなり切り分けました。

成果物はこちらです。

[phase20_controller_work.zip](sandbox:/mnt/data/phase20_controller_work.zip)

## 現在の目標の再確認

今必要なのは、4-正則 controller \(C\) で、

\[
58\le |V(C)|\le108
\]

かつ任意の ordered pair \((u,v)\) に対して、exact length 4 の nonbacktracking walk があるものです。

これができれば、前に見つけた \(\mathbb F_4^4\) universal chart と合成して、

\[
\Delta\le16,\qquad \operatorname{diam}\le4,\qquad |V|=256|V(C)|
\]

のグラフができます。

特に \(|V(C)|=58\) なら、

\[
256\cdot58=14848>14640
\]

なので、\((16,4)\) の新記録候補になります。

---

## 1. 29頂点 base + \(\mathbb Z_2\)-lift は少し前進

このルートが依然として一番コンパクトです。

29頂点の 4-正則 base \(B\) を作り、その \(\mathbb Z_2\)-voltage 2-lift を取れば、58頂点 controller が得られます。

\(\mathbb Z_2\)-lift が成功するには、各 ordered pair \((u,v)\) について、length-4 nonbacktracking path の mod-2 edge-incidence mask が少なくとも2種類必要です。そうでない pair は、どんな符号を付けても lift の2つの fiber を打ち分けられません。

前回の best は

\[
\text{bad0}=0,\qquad \text{bad1}=26
\]

でした。ここで：

- bad0 = length-4 NB path が存在しない ordered pair 数
- bad1 = path はあるが、mod-2 mask が1種類しかない ordered pair 数

今回、これを

\[
\boxed{\text{bad0}=0,\qquad \text{bad1}=8}
\]

まで改善しました。

これは良い前進です。ただし bad1 が 0 ではないため、この base はまだ \(\mathbb Z_2\)-lift controller にはできません。

現在の bad pair は、主に path が1本しかない pair と、4-cycle 由来で2本の向き違い path が同じ mask になる loop pair です。つまり、残り obstruction はかなり具体的です。

---

## 2. 単一 edge-switch では bad1=8 から改善できない

bad1=8 の best base に対して、全ての単一 2-edge switch を調べました。

結果、bad1 を 8 未満に下げる単一 switch はありませんでした。

つまり、ここから先は「1手の局所改善」では進みません。改善するなら、複数 switch をまとめて行うか、base を別の構造族から作り直す必要があります。

これは重要な判断材料です。bad1=8 は近いですが、単純な局所探索で押すのは筋が悪くなっています。

---

## 3. 小さい base \(\times\) cyclic voltage も継続検査

\(\mathbb Z_2\)-lift だけでなく、

\[
|V(B)|\cdot |H|\ge58
\]

となる小さい cyclic voltage controller も試しました。

特に新しく見たのは：

\[
9\times C_7,\qquad 11\times C_6,\qquad 13\times C_5
\]

です。

この方向の数学的な理由は、base が小さいほど ordered pair あたりの length-4 path 数が増え、group が小さいほど voltage product coverage が楽になるからです。

結果として、一番近かった観測値は

\[
\boxed{9\text{-vertex base}\times C_7}
\]

で、

\[
\text{total missing voltage constraints}=27,
\]

かつ

\[
\text{max missing per base pair}=1
\]

まで行きました。

つまり、各 base pair はほぼ全ての \(C_7\) residue を覆っており、漏れは薄く分散しています。ただし、まだ certificate ではありません。

一方で、

\[
11\times C_6,\quad 13\times C_5
\]

は今回の run ではそれより遠く、missing が 50〜60 程度に残りました。

---

## 4. 固定された高 path-count base も試した

より数学的に選んだ base として、次も試しました。

- 7頂点の \(\overline{C_3\sqcup C_4}\)
- 8頂点の cube complement
- 8頂点の circulant 型 4-regular base

これらは length-4 NB path count が良く、たとえば 8頂点 cube complement では各 ordered pair に少なくとも 12 本の length-4 path があります。

しかし、\(C_8\), \(C_9\), \(D_4\), \(Q_8\) 型の voltage product coverage では、missing 0 には届きませんでした。

ここから見えることは、単に path 数が多いだけでは足りないということです。path の edge-incidence vector が voltage group 上で十分に独立・多様である必要があります。

---

## 5. Cayley controller も調べたが、自然候補は不発

controller subproblem では既存アイデア使用が許可されたので、Cayley controller もかなり自然な候補です。

2つの生成元 \(a,b\) を持つ群 \(H\) で、

\[
\{a^{\pm1},b^{\pm1}\}
\]

の reduced word length 4 の値が \(H\) 全体を覆えば、Cayley graph がそのまま controller になります。

これは非常にきれいです。ordered pair 条件が、単に

\[
W_4(a,b)=H
\]

に落ちるからです。

しかし、以下の自然候補では成功しませんでした。

- \(A_5\), order 60：最大 coverage 52 / 60
- \(A_4\times C_5\), order 60：最大 52 / 60
- \(S_4\times C_3\), order 72：最大 61 / 72
- \(A_4\times C_6\), order 72：最大 54 / 72
- 各種 dihedral/direct-product 系：さらに弱い

また、dihedral group \(D_n\) の order 58〜108 範囲も試しましたが、全群を length-4 reduced sphere で覆うものは見つかりませんでした。

これは全 Cayley controller を否定するものではありません。ただし、自然な小群での「一発構成」は少し見込みが薄くなりました。

---

## 現時点の判断

最有望ルートはまだこれです。

\[
\boxed{
29\text{ 頂点 base}+\mathbb Z_2\text{-lift}
}
\]

理由は：

1. 成功すれば最小の 58頂点 controller になり、
   \[
   N(16,4)\ge14848
   \]
   が出る。
2. 現在
   \[
   \text{bad0}=0,\quad \text{bad1}=8
   \]
   まで近づいている。
3. 残り obstruction が明確で、path mask diversity の問題に絞られている。

ただし、bad1=8 の候補は単一 switch 局所最適なので、このまま単発局所改善を続けるのは効率が悪いです。

次に数学的にやるべきことは、29頂点 base を「ランダム switch で少しずつ直す」のではなく、

\[
\boxed{
\text{全 ordered pair に少なくとも2種類の length-4 path mask を保証する}
}
\]

ような構造を先に入れることです。

具体的には、各頂点が複数の4-cycleに乗り、かつ遠距離 pair でも2本以上の edge-parity 的に異なる length-4 route を持つような、**square-rich かつ NB4-covering な base** を設計する必要があります。

今回の結論は：

\[
\boxed{
\text{controller は未完成。ただし、29-base + 2-lift がまだ最短の勝ち筋。}
}
\]

です。

---

## Turn 136 (Round 032) — 🧑 USER

_2026-05-26 04:59:03 UTC_

続けてください

---

## Turn 137 (Round 032) — 🤖 ASSISTANT

_2026-05-26 04:59:37 UTC_  ·  model: `gpt-5-5-pro`

進めます。今回は29頂点base＋2-liftを本線に、path-mask差分次元と実際のZ2符号割当までを証明書として判定し、並行して直接58頂点controllerも構造条件付きで確認します。

---

## Turn 138 (Round 032) — 🤖 ASSISTANT

_2026-05-26 05:02:46 UTC_  ·  model: `gpt-5-5-pro`

29-baseのbad1=8が単一edge-switch局所最適だったため、同じ近傍を追わず、NB4行列条件 \(P_4(A)>0\) も評価に入れて原因を構造的に見ます。

---

## Turn 139 (Round 032) — 🤖 ASSISTANT

_2026-05-26 05:12:09 UTC_  ·  model: `gpt-5-5-pro`

残り8個のobstructionを分解すると、6個は長さ4の道が1本しかないordered pair、2個は自己pairの2道が同じmod-2 maskになる場合でした。小base×小voltage群も収支の良い候補に限定して並行評価します。

---

## Turn 140 (Round 032) — 🤖 ASSISTANT

_2026-05-26 05:21:45 UTC_  ·  model: `gpt-5-5-pro`

続けました。今回は **controller 完成にはまだ至っていません**。ただし、前回より重要な進展と、かなり大事な警告が出ました。

成果物はこちらです。

[phase21_controller_progress.zip](sandbox:/mnt/data/phase21_controller_progress.zip)

## 今回の進展

まず、controller 条件を行列として整理しました。

4-正則グラフ \(C\) の隣接行列を \(A\) とすると、exact length-4 nonbacktracking walk の個数行列は

\[
P_4(A)=A^4-10A^2+12I
\]

です。

したがって controller 条件は

\[
P_4(A)_{uv}>0
\quad\text{for all }u,v
\]

と書けます。これは今後の評価関数としてかなり便利です。単に「BFS で届いたか」ではなく、どの pair がどの程度不足しているかを \(A^2,A^4\) の関係で見られます。

---

## 1. 29-base + \(\mathbb Z_2\)-lift は少し前進

前回の best は

\[
\text{bad0}=0,\qquad \text{bad1}=8
\]

でした。

今回これを

\[
\boxed{\text{bad0}=0,\qquad \text{bad1}=4}
\]

まで改善しました。

ここで：

- bad0 = exact length-4 NB path が存在しない ordered pair 数
- bad1 = path は存在するが、mod-2 edge-incidence mask が 1 種類しかない ordered pair 数

です。

bad1 が 0 なら \(\mathbb Z_2\)-lift の符号設計へ進めますが、まだ 4 個残っているので、この base の 2-lift は不可能です。

残っている bad1 pair はかなり具体的です。

\[
0\to 11,\quad 11\to0,\quad 0\to16,\quad 16\to0.
\]

いずれも exact length-4 path mask が一意です。つまり、構造的には頂点 0 周辺の二つの route bottleneck だけが残っています。

---

## 2. ただし、\(\mathbb Z_2\)-lift 方針そのものに追加の警告

今回かなり重要だったのはここです。

bad1 を 0 にするだけでは、\(\mathbb Z_2\)-lift controller はまだ保証されません。各 base pair \((u,v)\) について、複数の path mask があっても、符号割当

\[
\sigma:E(B)\to\mathbb F_2
\]

で parity 0 と 1 の両方を実現できなければいけません。

そこで、現在の bad1=4 base について、各 ordered pair の path-mask difference の \(\mathbb F_2\)-rank を調べました。

rank 分布は：

| rank | ordered pair 数 |
|---:|---:|
| 0 | 4 |
| 1 | 188 |
| 2 | 280 |
| 3 | 209 |
| 4 | 96 |
| 5 | 46 |
| 6 | 14 |
| 7 | 4 |

rank 0 が今の bad1=4 です。

問題は、rank 1 や rank 2 が非常に多いことです。ランダムな符号割当で parity separation に失敗する期待値は

\[
\sum_{u,v}2^{-r(u,v)}\approx201.8125
\]

になります。

つまり、現在の 29-base は「bad1 があと 4 だから惜しい」というだけではありません。bad1 を 0 にしても、符号割当で大量の parity constraint が残る可能性が高いです。

これは重要な判断材料です。

---

## 3. 直接 58-controller と他の構造族

直接 58 頂点 controller の探索も続けましたが、前回 best を更新できませんでした。

また、数学的に自然な clustered family として、

\[
\text{line graph of cubic graph}
\]

や

\[
\text{prism over cubic graph}
\]

も試しました。理由は、local triangle/square が多ければ exact length 4 への padding が効くかもしれないからです。

しかし、これはかなり弱かったです。たとえば line graph 型では 60 頂点 controller でも miss が 800 以上、prism 型でも miss が 1000 以上残り、現在の direct/random-switch 系よりかなり悪いです。

したがって、

\[
\boxed{
\text{局所的に cycle を増やすだけでは controller 条件には効かない}
}
\]

と判断します。

---

## 現在の判断

最小 58 controller への最短路として、29-base + \(\mathbb Z_2\)-lift はまだ魅力がありますが、今回の rank 解析でかなり慎重になるべきだと分かりました。

今後の controller 設計では、単に

\[
\text{bad0}=0,\quad \text{bad1}=0
\]

を狙うだけでは不十分です。

必要なのは：

\[
\boxed{
\text{各 ordered pair の length-4 path-mask difference rank が高い base}
}
\]

です。

つまり次の評価基準に切り替えるべきです。

\[
\boxed{
\sum_{u,v}2^{-r(u,v)}
\text{ を小さくする}
}
\]

この値が 1 より十分小さければ、確率的にも \(\mathbb Z_2\)-signing が成功する見込みが出ます。現在の best は約 202 なので、まだかなり遠いです。

---

## 次に進むべき方向

今後は、29-base を単に局所 switch で bad1 だけ減らすのではなく、**path-mask rank を増やす構造**を入れる必要があります。

具体的には、

\[
\boxed{
\text{exact NB4 path が複数あるだけでなく、その edge-incidence が線形独立に近い base}
}
\]

を作る。

この視点だと、いままでの「bad1=4」は近いように見えて、実はまだ controller certificate からは遠いです。

今回の結論は：

\[
\boxed{
\text{29-base + 2-lift は改善したが、rank 解析により単純な 2-lift route は弱く見え始めた。}
}
\]

です。  
次は controller を「path count」ではなく **path-incidence rank design** として作る方針へ切り替えるのが筋です。

---

## Turn 141 (Round 033) — 🧑 USER

_2026-05-26 05:29:30 UTC_

続けてください

---

## Turn 142 (Round 033) — 🤖 ASSISTANT

_2026-05-26 05:30:03 UTC_  ·  model: `gpt-5-5-pro`

ここからは controller だけを小問題として扱い、欠陥数の局所減少ではなく \(P_4(A)=A^4-10A^2+12I>0\) を直接満たす 4-正則構造を狙います。既存の 29-base+2-lift も rank 観点で再評価しつつ、より直接的な構造族を優先します。

---

## Turn 143 (Round 033) — 🤖 ASSISTANT

_2026-05-26 05:33:23 UTC_  ·  model: `gpt-5-5-pro`

今回は、58頂点を直接当てるよりも、全ペアで exact NB4 被覆が生じる理由を証明できる controller 原理を優先します。29-base+2-lift は path-incidence rank で見込みを詰め、弱ければより強い構造へ切り替えます。

---

## Turn 144 (Round 033) — 🤖 ASSISTANT

_2026-05-26 05:42:47 UTC_  ·  model: `gpt-5-5-pro`

controller 側は「小さい base + 小さい voltage group」の証明問題へ絞り、特に前回最も近かった \(9\)-vertex base \(\times C_7\) を重点的に詰めます。

---

## Turn 145 (Round 033) — 🤖 ASSISTANT

_2026-05-26 06:00:11 UTC_  ·  model: `gpt-5-5-pro`

続けました。今回も **controller 完成、つまり新記録証明にはまだ至っていません**。ただし、前回の「29-base + \(\mathbb Z_2\)-lift」より筋の良い候補が出ました。

成果物はこちらです。

[phase22_controller_progress.zip](sandbox:/mnt/data/phase22_controller_progress.zip)

## 現在の到達点

いま必要なのは、4-正則 controller \(C\) で、

\[
58\le |V(C)|\le108
\]

かつ、任意の ordered pair \((u,v)\) に exact length-4 nonbacktracking walk が存在するものです。

これができれば、前に見つけた \(\mathbb F_4^4\) universal chart と合成して、

\[
\Delta\le16,\qquad \operatorname{diam}\le4,\qquad |V|=256|V(C)|
\]

のグラフができます。

特に \(|V(C)|=60\) なら、

\[
256\cdot60=15360
\]

なので、会話内で使っている現行基準

\[
N(16,4)\ge14640
\]

を

\[
720
\]

更新できます。

---

## 今回の主方針：小 base + 小 cyclic voltage

前回までの \(29\)-base + \(\mathbb Z_2\)-lift は、bad1 は小さくなったものの、path-incidence rank が低い pair が多く、符号割当が通る見込みが弱くなりました。

そこで今回は、もっと小さい base \(B\) と、小さい cyclic group \(C_m\) の voltage lift に絞りました。

条件はこうです。

4-正則 base graph \(B\) と、各有向辺の voltage

\[
\phi(e)\in C_m
\]

を取る。任意の ordered base pair \((i,j)\) について、exact length-4 nonbacktracking walk

\[
i\to j
\]

の voltage sum 全体が

\[
C_m
\]

を覆えば、lift controller は目的条件を満たします。

つまり、controller 条件が

\[
\boxed{
\forall i,j,\quad
\{\text{length-4 NB walk voltage sums } i\to j\}=C_m
}
\]

という小さい有限被覆証明に落ちます。

---

## 一番良かった候補：12-vertex base \(\times C_5\)

今回の最良候補は

\[
\boxed{
|V(B)|=12,\qquad H=C_5
}
\]

です。

controller の頂点数は

\[
12\cdot5=60.
\]

したがって、voltage 被覆が完成すれば、最終グラフは

\[
60\cdot256=15360
\]

頂点になります。

この候補が数学的に良い理由は、各 ordered base pair に対する exact length-4 NB walk 数が十分あることです。保存した最良 base では、

\[
\min_{i,j}\#\mathrm{NBWalk}_4(i,j)=7.
\]

覆うべき residue は 5 個なので、

\[
7>5
\]

の余裕があります。

---

## 実験結果

最良の \(12\times C_5\) 候補では、全条件数

\[
12\cdot12\cdot5=720
\]

のうち、漏れは

\[
18
\]

個まで減りました。

しかも、各 base pair の漏れは高々 1 residue です。つまり、漏れている pair でも

\[
5
\]

個中

\[
4
\]

個の residue はすでに覆えています。

\[
\boxed{
\text{total missing residues}=18,\qquad
\text{max missing per base pair}=1.
}
\]

これは前回の \(29\)-base + \(\mathbb Z_2\) よりかなり健全です。

---

## path-incidence rank も良い

今回の候補で重要なのは、単に miss が小さいだけではありません。

各 ordered base pair \((i,j)\) について、length-4 path の edge-incidence vector を \(\mathbb F_5\) 上で見て、その差分空間の rank を調べました。

分布は：

| rank | ordered pair 数 |
|---:|---:|
| 4 | 8 |
| 5 | 24 |
| 6 | 16 |
| 7 | 56 |
| 8 | 12 |
| 9 | 28 |

前回の \(\mathbb Z_2\)-lift では rank 1 や 2 の pair が大量にあり、random signing の失敗期待値が大きかったです。今回は全 pair が rank 4 以上です。

これはかなり良い兆候です。  
つまり、この \(12\times C_5\) route は「path 数はあるが実質同じ path ばかり」という状態ではありません。各 pair の path incidence が \(\mathbb F_5\) 上で十分に多様です。

---

## 他の候補との比較

今回見た主な cyclic voltage 候補は：

| 候補 | controller size | best missing |
|---|---:|---:|
| \(6\times C_{10}\) | 60 | 20 |
| \(7\times C_9\) | 63 | 19 |
| \(9\times C_7\) | 63 | 28 |
| \(12\times C_5\) | 60 | **18** |
| \(15\times C_4\) | 60 | 40 |
| \(20\times C_3\) | 60 | 48 |

数値だけなら \(12\times C_5\) が最良です。加えて rank 分布も良いので、現時点ではこれが controller 側の本命です。

---

## Cayley controller 側の追加確認

controller subproblem に限って既存アイデア使用が許可されたので、Cayley controller も追加で見ました。

特に、群 \(G\) と生成元 \(a,b\) に対して、reduced length-4 word 全体

\[
W_4(a,b)
\]

が \(G\) を覆えば、それだけで controller になります。

ただし、今回の追加確認でも自然な候補は通りませんでした。

例えば \(A_5\) は全ペアを exhaustive に確認し、最大 coverage は

\[
52/60
\]

でした。Heisenberg 型や metacyclic 型でも、今回の範囲では controller 条件を満たすものは見つかっていません。

したがって、いまは Cayley controller より

\[
\boxed{
12\text{-vertex base}+C_5\text{ voltage}
}
\]

を優先すべきだと判断しています。

---

## 現時点の判断

まだ controller certificate はありません。したがって新記録もまだ出ていません。

ただし、前回より本命はかなり絞れました。

\[
\boxed{
12\text{-vertex 4-regular base}
+
C_5\text{ voltage lift}
}
\]

で、現在

\[
720
\]

条件中

\[
18
\]

条件だけが漏れています。

次にやるべきことは、ランダムな voltage 変更を増やすことではなく、この 24 個の \(\mathbb F_5\) edge-voltage 変数に対する **小さい exact covering problem** として解くことです。

つまり次フェーズは：

\[
\boxed{
\text{固定された 12-base 上で、}
C_5\text{ voltage が全 }720\text{ 条件を覆るかを exact/CP 的に解く}
}
\]

です。

今回の候補は、数学的な事前根拠があります。  
各 pair の path 数が residue 数を上回り、さらに path-incidence rank が全 pair で高い。これは前回の \(\mathbb Z_2\) route より明らかに良いです。

---

## Turn 146 (Round 034) — 🧑 USER

_2026-05-26 06:16:00 UTC_

つづきお願いします

---

## Turn 147 (Round 034) — 🤖 ASSISTANT

_2026-05-26 06:16:21 UTC_  ·  model: `gpt-5-5-pro`

今回は本命の「12頂点 base + \(C_5\) voltage」に絞り、固定 base 上の exact covering 制約として詰めます。まず漏れ18の候補を復元し、無理なら同じ基準で base を差し替えます。

---

## Turn 148 (Round 034) — 🤖 ASSISTANT

_2026-05-26 06:19:36 UTC_  ·  model: `gpt-5-5-pro`

固定 base 上の 24 個の電圧変数は、switching で実質 13 変数まで落とせるため、まずそこで完全探索/CSP として feasibility を判定します。各頂点への長さ4自己非戻り歩道も必要なので、4-cycle を十分含む構造かも同時に見ます。

---

## Turn 149 (Round 034) — 🤖 ASSISTANT

_2026-05-26 06:28:55 UTC_  ·  model: `gpt-5-5-pro`

固定 \(12\times C_5\) は miss 18 から改善が見えないため、未充足 residue を狙う修復で infeasibility を切り分けます。並行して、余裕の大きい \(k=5\) 用 controller も検討します。

---

## Turn 150 (Round 034) — 🤖 ASSISTANT

_2026-05-26 06:42:58 UTC_  ·  model: `gpt-5-5-pro`

進めました。今回も **まだ新記録の完成証明には至っていません**。ただし、かなり良い方針転換がありました。

成果物はこちらです。

[phase23_controller_progress.zip](sandbox:/mnt/data/phase23_controller_progress.zip)

## まず、前回の \(12\)-base \(+C_5\) はいったん後退

前回の本命だった

\[
12\text{ 頂点 base}+C_5
\]

について、固定された best base / voltage の近傍をもう少し厳しく調べました。

この候補は \((16,4)\) 用 controller を作るためのもので、

\[
12\cdot5=60
\]

頂点 controller を狙っていました。成功すれば、前に見つけた \(\mathbb F_4^4\) universal chart と合成して

\[
60\cdot4^4=15360
\]

頂点の \((16,4)\) 候補になります。

ただし、現在の best は

\[
720
\]

個の residue 条件中、

\[
18
\]

個が漏れていました。

今回、この fixed base / voltage に対して、全ての

- 1-edge voltage change,
- 2-edge voltage change,
- 3-edge voltage change,
- 4-edge voltage change

を全検査しました。

結果：

\[
\boxed{\text{4-edge change まででは 18 missing から改善なし}}
\]

でした。

つまり、この固定 base はかなり硬い局所最適です。  
このまま \(12\times C_5\) にこだわって voltage を微調整するのは、現時点では筋が悪くなりました。

---

## 新しい本命：\(K_6\) minus perfect matching \(+C_{22}\)

そこで、同じ controllable chart 原理のまま、\((16,5)\) 側に切り替えました。

すでに \(\mathbb F_4^5\) 版の universal chart は得られています。つまり、controller に exact length-5 nonbacktracking route が 1 本あれば、その route だけで fiber の

\[
4^5=1024
\]

個の target を全部 routing できます。

したがって、必要なのは：

\[
\boxed{
|C|\ge130
\text{ の 4-regular controller で、任意の ordered pair が exact NB length }5
\text{ で結ばれること}
}
\]

です。

今回の新候補は：

\[
B=K_6-\text{perfect matching}
\]

です。これは 6 頂点 4-正則グラフです。ここに cyclic voltage group

\[
C_{22}
\]

を載せます。

controller サイズは

\[
6\cdot22=132.
\]

これが成功すると、最終グラフは

\[
132\cdot4^5=132\cdot1024=135168
\]

頂点になります。

現行基準として使っている

\[
N(16,5)\ge132496
\]

を

\[
135168-132496=5168
\]

更新します。

---

## なぜこの候補は数学的に勝算があるか

この候補の良い点は、base path 数と voltage group サイズの比です。

\(B=K_6-\text{perfect matching}\) では、任意の ordered base pair \((i,j)\) に対して exact length-5 nonbacktracking walk が

\[
53\text{ または }56
\]

本あります。

一方で、覆うべき voltage residue は

\[
|C_{22}|=22
\]

個だけです。

つまり、各 base pair について

\[
53\text{〜}56
\]

個の path voltage sum で

\[
22
\]

個の residue を覆えばよい。

これは前回の \(12\times C_5\) より、path-count slack がかなり大きいです。  
また、base が 6 頂点と小さいため、controller 証明は

\[
36\text{ base pairs}\times22\text{ residues}=792
\]

個の小さい条件に落ちます。

---

## 実験結果

\(K_6-\text{matching}+C_{22}\) で cyclic voltage search を回しました。

最良候補は：

\[
\boxed{\text{missing residue conditions}=6}
\]

です。

全条件数は

\[
36\cdot22=792
\]

なので、現在

\[
786/792
\]

条件を満たしています。

漏れている条件は次の 6 個です。

\[
(1,1,4),\quad (1,1,18),
\]

\[
(2,2,11),\quad (2,3,7),
\]

\[
(3,2,15),\quad (3,3,0).
\]

ここで \((i,j,r)\) は「base vertex \(i\) から \(j\) への exact length-5 nonbacktracking path の voltage sum が residue \(r\) を実現できていない」という意味です。

さらに、この best voltage assignment は、全ての 1-edge / 2-edge voltage change に対して改善しないことも確認しました。  
つまり、ここから先は単純な voltage 微調整ではなく、もう少し構造的な変更が必要です。

---

## 比較した別候補

同じ長さ 5 controller 方針で、いくつか比較しました。

| candidate | controller size | best missing |
|---|---:|---:|
| \(K_6-\text{matching}+C_{22}\) | 132 | **6** |
| \(K_6-\text{matching}+D_{11}\) | 132 | 20 |
| \(7\)-vertex circulant \(+C_{19}\) | 133 | 12 |
| \(8\)-vertex circulant \(+C_{17}\) | 136 | 17 |

したがって、現時点では

\[
\boxed{
K_6-\text{perfect matching}+C_{22}
}
\]

が最も強い候補です。

---

## 現在の判断

\((16,4)\) の 60 頂点 controller ルートはまだ生きていますが、今回の固定 \(12\times C_5\) 候補は 4-change local optimum で詰まりました。

一方で、\((16,5)\) へ移した

\[
K_6-\text{matching}+C_{22}
\]

はかなり良いです。

成功すれば

\[
\boxed{N(16,5)\ge135168}
\]

で、更新幅も

\[
+5168
\]

と十分あります。

次にやるべきことは、現在の 6 missing を局所的に潰すのではなく、次のどちらかです。

1. **同じ \(K_6-\text{matching}\) base 上で、cyclic \(C_{22}\) voltage を exact/CP 的に解く。**  
   変数は 12 edge voltages。switching で自由度は 7 まで落とせます。

2. **base を \(K_6-\text{matching}\) のまま、voltage group を少し変える。**  
   \(D_{11}\) は弱かったので、次は \(C_2\times C_{11}\) 表現で residue constraints を分解して、parity と mod-11 の被覆を別々に設計するのが筋です。これは \(C_{22}\) と同型ですが、設計上は「どの漏れが parity 由来か、mod-11 由来か」を見やすくできます。

いまの本線は：

\[
\boxed{
K_6-\text{matching}+C_{22}
\text{ controller}
+
\mathbb F_4^5\text{ universal chart}
}
\]

です。まだ完成していませんが、ここまでの中では最も「数学的に勝算があり、かつ記録更新幅もある」候補になっています。

---

## Turn 151 (Round 035) — 🧑 USER

_2026-05-26 06:46:52 UTC_

つづけてください

---

## Turn 152 (Round 035) — 🤖 ASSISTANT

_2026-05-26 06:47:25 UTC_  ·  model: `gpt-5-5-pro`

続けます。前回の \(K_6\)-matching \(+C_{22}\) を小さな voltage 割当問題として定式化し、6 個の漏れが構造的障害か別割当で消せるかを切り分けます。

---

## Turn 153 (Round 035) — 🤖 ASSISTANT

_2026-05-26 06:50:51 UTC_  ·  model: `gpt-5-5-pro`

\(C_{22}\simeq C_{11}\times C_2\) と見て、まず mod 11 voltage を固定し、その上で parity signing が全 residue を両側覆えるかを exact に判定します。巨大グラフは作らず、12 edge voltage の線形被覆条件だけを詰めます。

---

## Turn 154 (Round 035) — 🤖 ASSISTANT

_2026-05-26 07:00:10 UTC_  ·  model: `gpt-5-5-pro`

良い兆候として、gauge 固定後の 7 変数探索で missing が 6 から 4 まで改善しました。まだ証明ではありませんが、6 で構造的に止まるわけではなさそうです。

---

## Turn 155 (Round 035) — 🤖 ASSISTANT

_2026-05-26 07:14:53 UTC_  ·  model: `gpt-5-5-pro`

続けました。今回は **\(K_6-\)perfect matching \(+C_{22}\)** controller をかなり詰めました。

成果物はこちらです。

[phase24_controller_c22.zip](sandbox:/mnt/data/phase24_controller_c22.zip)

## 結論

まだ新記録の完成証明には至っていません。

ただし、前回の候補をかなり改善しました。

前回の本命は：

\[
B=K_6-\text{perfect matching},\qquad H=C_{22}
\]

の voltage lift で、controller 頂点数

\[
6\cdot22=132
\]

を狙うものでした。

これが成功すれば、前に見つけた \(\mathbb F_4^5\) universal chart と合成して、

\[
132\cdot 4^5=135168
\]

頂点の

\[
\Delta\le16,\qquad \operatorname{diam}\le5
\]

のグラフになります。

会話内で使っている現行基準

\[
N(16,5)\ge132496
\]

を

\[
135168-132496=5168
\]

更新する候補です。

---

## 今回の改善

前回の \(C_{22}\) voltage 候補では、length-5 nonbacktracking path の voltage sums が全 residue を覆う条件で、漏れが 6 個程度残っていました。

今回、\(C_{22}\) を

\[
C_{22}\cong C_2\times C_{11}
\]

として分解し、

1. まず mod \(11\) で全 residue を覆う。
2. その後、parity が各 mod \(11\) bucket で両方出るようにする。

という形で探索しました。

その結果、漏れを

\[
\boxed{4}
\]

まで減らしました。

best gauge voltage は、spanning tree を 0 に固定した 7 変数表示で：

\[
\boxed{6,\ 11,\ 11,\ 13,\ 8,\ 15,\ 4}
\]

です。

この候補の漏れは次の 4 条件だけです。

\[
(0,1,13),\quad (1,0,9),
\]

\[
(0,4,19),\quad (4,0,3).
\]

ここで \((i,j,r)\) は、

> base vertex \(i\) から \(j\) への exact length-5 nonbacktracking walk の voltage sum として \(r\in C_{22}\) が実現されない

という意味です。

対称性として、

\[
9\equiv -13\pmod{22},\qquad 3\equiv -19\pmod{22}
\]

なので、実質的には

\[
0\leftrightarrow1,\qquad 0\leftrightarrow4
\]

の 2 つの undirected obstruction だけです。

---

## これはなぜ良い進展か

今回の候補では、mod \(11\) coverage はすでに全て通っています。

つまり、各 ordered base pair \((i,j)\) と各 residue

\[
r\in C_{11}
\]

について、length-5 nonbacktracking path の voltage sum が \(r\) になる path は存在します。

残っている問題は parity だけです。

より具体的には、miss している bucket は次のようになっています。

\[
0\to1,\quad r\equiv2\pmod{11}
\]

では path は 3 本ありますが、全部同じ parity 側に落ちます。

\[
0\to4,\quad r\equiv8\pmod{11}
\]

では該当 path が 1 本しかなく、当然 parity を両方出せません。

逆向きも同じ構造です。

したがって、今の obstruction は「全体がランダムに足りない」のではなく、

\[
\boxed{
\text{特定の mod }11\text{ bucket に path-mask diversity が足りない}
}
\]

という非常に具体的な問題に縮約されました。

---

## 近傍検査

この miss-4 候補について、gauge 7 変数の

- 1 変数変更
- 2 変数変更
- 3 変数変更

を全検査しました。

結果：

\[
\boxed{
\text{1-, 2-, 3-variable gauge change では miss }4\text{ から改善なし}
}
\]

です。

つまり、これは単純な近傍では動かないかなり硬い候補です。  
ここからは電圧値を微調整するより、mod \(11\) 側で bucket diversity を最初から設計する必要があります。

---

## 比較：\(C_{23}\) も確認

同じ base

\[
K_6-\text{perfect matching}
\]

で \(C_{23}\) も軽く確認しました。

controller size は

\[
6\cdot23=138
\]

で、成功すればさらに大きい候補になります。

ただし短い探索では best missing は

\[
10
\]

で、今回の \(C_{22}\) miss \(4\) より悪かったです。

したがって、現時点ではまだ

\[
\boxed{K_6-\text{matching}+C_{22}}
\]

が本命です。

---

## 現時点の判断

今回の進展で、\(C_{22}\) route はまだ十分に生きています。

理由は：

\[
\boxed{
\text{mod }11\text{ coverage は完全に通り、失敗は parity のみ}
}
\]

だからです。

これは前回までの「いろいろな residue が広く漏れている」状態とは違います。  
残っているのは、2 つの inverse pair に対応する parity obstruction だけです。

ただし、単純な local voltage search ではもう厳しいです。  
次にやるべきことははっきりしています。

\[
\boxed{
C_{22}\cong C_{11}\times C_2
}
\]

として、

1. \(C_{11}\) voltage を選ぶ。
2. 各 \((i,j,r\in C_{11})\) bucket に、parity mask が少なくとも 2 種類出るようにする。
3. そのうえで、1 つの global parity signing が全 bucket を分離することを確認する。

この **bucket-diversity 設計問題** が次の本体です。

## いまの本線

\[
\boxed{
K_6-\text{perfect matching}+C_{22}
\text{ controller}
+
\mathbb F_4^5\text{ universal chart}
}
\]

を継続します。

まだ新記録ではありませんが、controller 条件はかなり小さい obstruction まで落ちています。次は「missing residue を直接潰す」ではなく、mod \(11\) bucket の path-mask rank を設計目標にして進めるのが一番筋が良いです。

---

## Turn 156 (Round 036) — 🧑 USER

_2026-05-26 07:40:08 UTC_

続けてください

---

## Turn 157 (Round 036) — 🤖 ASSISTANT

_2026-05-26 07:40:28 UTC_  ·  model: `gpt-5-5-pro`

進めます。まず \(K_6-\)matching \(+C_{22}\) の残る obstruction が構成限界か、電圧設計で消せるかを小さい exact problem として調べます。

---

## Turn 158 (Round 036) — 🤖 ASSISTANT

_2026-05-26 07:43:39 UTC_  ·  model: `gpt-5-5-pro`

少し大きな進展として、6頂点の4正則多重baseに自由度を広げると、132頂点の単純4正則controllerが通る候補が出ました。いま controller 条件と \(\mathbb F_4^5\) fiber chart を証明スクリプトで検証しています。

---

## Turn 159 (Round 036) — 🤖 ASSISTANT

_2026-05-26 08:02:37 UTC_  ·  model: `gpt-5-5-pro`

進展ありです。**\((d,k)=(16,5)\) の新記録候補になる構成証明書が出ました。**

成果物はこちらです。

[phase25_verified_controllable_chart_candidate.zip](sandbox:/mnt/data/phase25_verified_controllable_chart_candidate.zip)

会話内で使ってきた基準では、現行値は

\[
N(16,5)\ge132,496
\]

でした。今回の構成は

\[
\boxed{
\Delta=16,\qquad \operatorname{diam}\le5,\qquad |V|=135,168
}
\]

なので、基準表に対して

\[
135,168-132,496=5,168
\]

の更新候補です。

ただし、公開記録として主張する前には、最新版の表との照合と第三者検証が必要です。ここでは **構成証明書と生成済み edge list を内部検証した候補**として報告します。

---

## 何が変わったか

前回までの

\[
K_6-\text{perfect matching}+C_{22}
\]

は miss 4 で詰まっていました。

今回は、base を少し緩めて、**6 頂点 4-正則 multigraph の \(C_{22}\)-voltage lift** にしました。

重要なのは、base は multigraph ですが、**lift 後の controller は単純 4-正則グラフ**になることです。つまり最終グラフも単純です。

controller の base edge は次の 12 本です。

| edge id | \(u\) | \(v\) | voltage mod 22 |
|---:|---:|---:|---:|
| 0 | 0 | 2 | 20 |
| 1 | 0 | 3 | 11 |
| 2 | 0 | 3 | 2 |
| 3 | 0 | 5 | 20 |
| 4 | 1 | 2 | 10 |
| 5 | 1 | 4 | 13 |
| 6 | 1 | 4 | 14 |
| 7 | 1 | 5 | 14 |
| 8 | 2 | 3 | 13 |
| 9 | 2 | 4 | 14 |
| 10 | 3 | 5 | 7 |
| 11 | 4 | 5 | 0 |

この base の \(C_{22}\)-lift は

\[
6\cdot22=132
\]

頂点の controller \(C\) になります。

---

## 証明の骨格

最終グラフは

\[
V(G)=V(C)\times\mathbb F_4^5
\]

で作ります。

したがって頂点数は

\[
132\cdot4^5=132\cdot1024=135,168.
\]

controller は 4-正則です。各 controller edge から fiber 側に \(\mathbb F_4\) の 4 通りの選択肢を持たせるので、最終グラフの次数は

\[
4\cdot4=16.
\]

直径 5 の証明は次の 2 段です。

### 1. controller 側

base multigraph 上で、任意の ordered base pair \((i,j)\) について、exact length-5 nonbacktracking walk の voltage sums が

\[
\mathbb Z/22\mathbb Z
\]

全体を覆ることを確認しました。

したがって lift 後の 132 頂点 controller では、任意の ordered controller pair に exact length-5 nonbacktracking route があります。

### 2. fiber 側

\(\mathbb F_4^5\) 上に、4 つの directed symbols

\[
a,\ a^{-1},\ b,\ b^{-1}
\]

に対応する affine control data

\[
(A_s,b_s)
\]

を置きます。

検証済み性質は：

\[
\boxed{
\text{任意の reduced word }s_1s_2s_3s_4s_5
\text{ に対し、対応する }5\times5
\text{ controllability matrix が正則}
}
\]

です。

つまり、controller 上の長さ 5 reduced route が 1 本あれば、その route だけで fiber の

\[
4^5=1024
\]

個の target をすべて一意に指定できます。

controller の 4-正則グラフは 2-factorization し、各 2-factor を cycle orientation して

\[
a,a^{-1},b,b^{-1}
\]

でラベル付けしています。このため、controller の nonbacktracking walk は必ず reduced word を与えます。

したがって任意の

\[
(c,x),(d,y)\in V(C)\times\mathbb F_4^5
\]

に対して、

1. controller 側で \(c\to d\) の exact NB length-5 route を取る。
2. その reduced word に対する fiber chart を使い、\(x\to y\) となる 5 個の \(\lambda\in\mathbb F_4\) を解く。

これで長さ 5 の path が得られます。

よって

\[
\operatorname{diam}(G)\le5.
\]

---

## 検証結果

同梱の `verify_candidate.py` を実行して、以下を確認しました。

```text
Base voltage coverage: OK
Controller: OK; 132 vertices, simple 4-regular, exact labeled NB length-5 coverage
GF(4)^5 universal chart: OK; 324 reduced words checked, min rank 5; inverse-symbol data verified
Certificate complete: degree 16, diameter <=5, vertices = 132*4^5 = 135168
```

さらに生成済み edge list についても、内部で確認しました。

```text
135168 1081344
bad loops/duplicates: 0
min degree: 16
max degree: 16
unique edges: 1081344
```

辺数も

\[
135168\cdot16/2=1,081,344
\]

と一致します。

---

## zip 内の主なファイル

- `README.txt`  
  構成と証明の概要。

- `controller_c22_multibase.txt`  
  132 頂点 controller を作るための \(C_{22}\)-voltage base。

- `gf4_s5_universal.txt`  
  \(\mathbb F_4^5\) の universal route-chart control data。

- `verify_candidate.py`  
  controller coverage、2-factor labeling、fiber chart rank 条件を検証するスクリプト。

- `generate_final_graph.py`  
  最終グラフの edge list を生成するスクリプト。

- `final_graph_edges.tsv.gz`  
  135,168 頂点、1,081,344 辺の圧縮 edge list。

---

## 現時点の評価

これは、これまでの「あと数個漏れる」候補とは違います。今回は certificate が通っています。

\[
\boxed{
\Delta=16,\quad \operatorname{diam}\le5,\quad |V|=135168
}
\]

の単純無向グラフとして、構成・検証スクリプト・具体的 edge list まで揃いました。

次にやるべきことは、独立検証用に証明をさらに短く整理し、最新版の公開記録表と照合してから、構成メモまたは投稿用 note にまとめることです。

---

## Turn 160 (Round 037) — 🧑 USER

_2026-05-26 08:34:49 UTC_

手法全体と結果をまとめてmdにしてください。

---

## Turn 161 (Round 037) — 🤖 ASSISTANT

_2026-05-26 08:35:11 UTC_  ·  model: `gpt-5-5-pro`

了解です。最終候補の証明構造、構成データ、検証結果、未確認事項を分けて、独立検証しやすい Markdown にまとめます。

---

## Turn 162 (Round 038) — 🧑 USER

_2026-05-26 08:35:14 UTC_

手法全体と証明と結果をまとめてmdにしてください。

---

## Turn 163 (Round 038) — 🤖 ASSISTANT

_2026-05-26 08:38:30 UTC_  ·  model: `gpt-5-5-pro`

証明書 zip の実データと verifier 出力を確認し、132 頂点 controller と GF(4)^5 fiber chart の二段証明を再現可能な定義・補題・検証手順としてまとめます。記録値は過剰主張を避け、会話内基準と公開表で要再照合の点を分けて書きます。

---

## Turn 164 (Round 038) — 🤖 ASSISTANT

_2026-05-26 08:43:35 UTC_  ·  model: `gpt-5-5-pro`

作成しました。手法全体、controller 構成、fiber chart、直径証明、検証結果、再現方法までまとめています。

[Markdown をダウンロード](sandbox:/mnt/data/controllable_chart_construction_summary.md)

元の構成証明書・edge list 一式はこちらです。

[証明書 zip](sandbox:/mnt/data/phase25_verified_controllable_chart_candidate.zip)

なお、md 内でも明記していますが、公開記録として主張する前には最新版の degree/diameter 表との照合と第三者検証が必要です。

---

## Turn 165 (Round 039) — 🧑 USER

_2026-05-26 08:55:53 UTC_

この結果の一般化を試みてください。

---

## Turn 166 (Round 039) — 🤖 ASSISTANT

_2026-05-26 08:56:19 UTC_  ·  model: `gpt-5-5-pro`

まず既存証明書を controller 側と fiber chart 側に分解し、偶然のパラメータと定理化できる部分を切り分けます。そのうえで、一般化候補を小さな条件として検証します。

---

## Turn 167 (Round 039) — 🤖 ASSISTANT

_2026-05-26 08:59:35 UTC_  ·  model: `gpt-5-5-pro`

Fiber 側では \(\mathbb F_4^5\) chart の下三角拡張により、\(\mathbb F_4^6\) や \(\mathbb F_4^7\) でも universal chart が見つかっています。次は \((16,6)\) を具体ターゲットに、必要な controller サイズと voltage-lift 被覆条件を評価します。

---

## Turn 168 (Round 039) — 🤖 ASSISTANT

_2026-05-26 09:13:00 UTC_  ·  model: `gpt-5-5-pro`

一般化を進めました。今回はかなり良い結果が出ています。

## 完成した一般化：\((d,k)=(12,5)\)

既存の 132 頂点 controller をそのまま使い、fiber を

\[
\mathbb F_4^5
\]

から

\[
\mathbb F_3^5
\]

へ落とす一般化が通りました。

結果として、単純無向グラフ

\[
\boxed{
\Delta=12,\qquad \operatorname{diam}\le5,\qquad |V|=32,076
}
\]

の構成証明書が得られました。

作業中に使ってきた表では

\[
N(12,5)\ge 29,621
\]

だったので、これに対しては

\[
32,076-29,621=2,455
\]

の更新候補です。現在確認できる外部表でも \(N(12,5)\) の lower bound は 29,621 と掲載されています。citeturn604842search2turn604842search3

成果物はこちらです。

[GF(3)^5 generalization 証明書 zip](sandbox:/mnt/data/phase26_gf3_generalization.zip)

[一般化メモ md](sandbox:/mnt/data/controllable_chart_generalization_report.md)

## 一般定理としての形

今回の構成は、次の形に一般化できます。

有限体 \(\mathbb F_q\)、次元 \(s\)、4-正則 controller \(C\) を取ります。controller の directed edge を

\[
a,\ a^{-1},\ b,\ b^{-1}
\]

で逆元付きにラベル付けします。

各記号 \(t\) に対して

\[
A_t\in GL(s,q),\qquad b_t\in\mathbb F_q^s
\]

を割り当て、逆記号について

\[
A_{t^{-1}}=A_t^{-1},\qquad b_{t^{-1}}=A_t^{-1}b_t
\]

を満たすようにします。

最終グラフの頂点集合は

\[
V(G)=V(C)\times\mathbb F_q^s.
\]

controller arc \(u\to v\) の記号が \(t\) のとき、各 \(\lambda\in\mathbb F_q\) に対して

\[
(u,x)\sim (v,A_tx+\lambda b_t)
\]

を張ります。

このとき次数は

\[
\Delta(G)=4q.
\]

さらに、任意の reduced word

\[
w=t_1t_2\cdots t_s
\]

に対して controllability matrix

\[
\left[
A_{t_s}\cdots A_{t_2}b_{t_1},
A_{t_s}\cdots A_{t_3}b_{t_2},
\dots,
b_{t_s}
\right]
\]

が正則で、controller \(C\) が任意の ordered pair を exact length \(s\) の nonbacktracking walk で結ぶなら、

\[
\operatorname{diam}(G)\le s.
\]

この一般定理のポイントは、

\[
\boxed{
1\text{ 本の controller route が fiber 全体への全単射 chart になる}
}
\]

ことです。これは以前の rank-controller のように「多くの path の和集合がたまたま fiber を覆う」ものではなく、1 route が \(q^s\) 個の fiber target を決定的に全部覆います。

## 今回の \(\mathbb F_3^5\) 構成

controller は、前回の \((16,5)\) 候補で使ったものと同じです。

\[
|V(C)|=132,\qquad C\text{ は 4-正則}.
\]

これは 6 頂点 4-正則 multigraph の \(C_{22}\)-voltage lift で、任意の ordered controller pair を exact nonbacktracking length 5 で結ぶことが検証済みです。

今回、新しく

\[
\mathbb F_3^5
\]

上の universal chart を構成しました。検証結果は：

```text
Base voltage coverage: OK
Controller: OK; 132 vertices, simple 4-regular, exact labeled NB length-5 coverage
GF(3)^5 universal chart: OK; 324 reduced words checked, min rank 5; inverse-symbol data verified
Certificate complete: degree 12, diameter <=5, vertices = 132*3^5 = 32076
```

最終 edge list も生成し、単純性・次数を確認しています。

```text
32076 192456
bad loops/duplicates 0 0
min degree 12
max degree 12
```

辺数も

\[
32,076\cdot12/2=192,456
\]

と一致します。

## 未完成だが有望な一般化：\((16,6)\)

さらに、fiber 側だけなら

\[
\mathbb F_4^6
\]

への拡張も通りました。

[GF(4)^6 partial chart zip](sandbox:/mnt/data/phase26_partial_gf4_s6.zip)

具体的には、\(\mathbb F_4^6\) 上で、全 972 個の reduced word length 6 に対して controllability matrix が rank 6 になる universal chart を見つけました。

したがって、もし 4-正則 controller \(C\) が任意の ordered pair を exact nonbacktracking length 6 で結べれば、

\[
\Delta=16,\qquad \operatorname{diam}\le6,\qquad |V|=|C|\cdot4^6
\]

が得られます。

作業表の

\[
N(16,6)\ge1,771,560
\]

を超えるには、

\[
|C|\ge \left\lceil\frac{1,771,561}{4,096}\right\rceil=433
\]

が必要です。

ここではまだ controller が見つかっていません。同じ 6 頂点 base に \(C_{73}\) を載せる quick test は full coverage からかなり遠く、現時点では

\[
\boxed{
\mathbb F_4^6\text{ fiber chart は完成、length-6 controller がボトルネック}
}
\]

という状態です。

## まとめ

今回の一般化で、完成証明書つきの候補は：

\[
\boxed{
N(12,5)\ge 32,076
}
\]

です。

前回の

\[
N(16,5)\ge135,168
\]

に加えて、同じ controller route-chart 原理が別次数にも効くことが確認できました。

次に一番価値があるのは、\(\mathbb F_4^6\) chart を活かすための exact NB length-6 controller を作ることです。これが 433 頂点以上で作れれば、\((16,6)\) でもかなり大きい更新候補になります。

---

## Turn 169 (Round 040) — 🧑 USER

_2026-05-26 13:18:12 UTC_

続けてください

---

## Turn 170 (Round 040) — 🤖 ASSISTANT

_2026-05-26 13:18:35 UTC_  ·  model: `gpt-5-5-pro`

続けます。今回は既存の fiber chart の再利用範囲を確認しつつ、次の更新に必要な length-6 以上の controller を小さな証明書設計問題として攻めます。

---

## Turn 171 (Round 040) — 🤖 ASSISTANT

_2026-05-26 13:21:49 UTC_  ·  model: `gpt-5-5-pro`

まずは巨大グラフを直接作らず、\((16,6)\) 用の exact length-6 controller 証明書に絞ります。path count と residue 被覆余裕がある小さな 4-正則 base の cyclic voltage lift を優先して検査します。

---

## Turn 172 (Round 040) — 🤖 ASSISTANT

_2026-05-26 13:31:08 UTC_  ·  model: `gpt-5-5-pro`

別案として、完成済み132頂点controllerをlength-6用baseとして再利用する方向と、\(q=5\)・3正則controllerで\((15,\cdot)\)を狙う枝も検討します。既存\((4,6)=740\) graphの流用は exact NB length-6 被覆が弱く、除外しました。

---

## Turn 173 (Round 040) — 🤖 ASSISTANT

_2026-05-26 13:42:27 UTC_  ·  model: `gpt-5-5-pro`

続けました。今回は **新記録の追加完成までは到達していません**。ただし、かなり意味のある一般化の枝が見つかりました。

成果物はこちらです。

[phase27_generalization_attempts.zip](sandbox:/mnt/data/phase27_generalization_attempts.zip)

## 今回の主な進展：\((15,5)\) 用の fiber chart が完成

これまでの成功例は、4-正則 controller と \(\mathbb F_q^5\) の chart を組み合わせるものでした。

\[
d=4q.
\]

そのため、

\[
q=3\Rightarrow d=12,\qquad q=4\Rightarrow d=16
\]

が自然に出ました。

今回は別方向として、**3-正則 controller** を使う一般化を試しました。  
3-正則 controller では、edge labels を

\[
a,\quad a^{-1},\quad c
\]

とし、ここで \(c=c^{-1}\) は self-inverse symbol とします。つまり controller は、

\[
\text{oriented 2-factor }(a,a^{-1})
+
\text{perfect matching }(c)
\]

の形を持つ cubic graph です。

この場合、fiber を \(\mathbb F_5^5\) にすると次数は

\[
d=3\cdot5=15.
\]

今回、\(\mathbb F_5^5\) 上で、全ての reduced word

\[
s_1s_2s_3s_4s_5
\]

に対して controllability matrix が full rank になる chart を見つけました。reduced word は

\[
aa^{-1},\quad a^{-1}a,\quad cc
\]

を隣接部分語として含まないものです。長さ 5 の reduced word は

\[
3\cdot2^4=48
\]

個あり、その全てで rank 5 を確認しました。

検証スクリプトの出力は：

```text
checked 48 reduced words of length 5; min rank = 5; bad = 0
GF(5)^5 3-symbol universal chart: OK
```

これは本質的に、前の \((12,5)\), \((16,5)\) の chart 原理が **4-regular controller 専用ではない**ことを示しています。

## もし controller ができれば何が出るか

必要なのは、3-正則 controller \(C\) で、任意の ordered pair \((u,v)\) が exact length-5 nonbacktracking walk で結ばれるものです。

その場合、最終グラフは

\[
V(G)=V(C)\times\mathbb F_5^5
\]

で、

\[
\Delta(G)=15,\qquad \operatorname{diam}(G)\le5,
\]

\[
|V(G)|=|V(C)|\cdot5^5.
\]

作業中に使ってきた表では

\[
N(15,5)\ge77,520.
\]

したがって、

\[
|C|\cdot3125>77520
\]

が必要で、

\[
|C|\ge25
\]

です。cubic graph は偶数頂点なので、最初の実用ターゲットは

\[
|C|=26.
\]

これができれば、

\[
26\cdot3125=81,250
\]

なので、

\[
\boxed{N(15,5)\ge81,250}
\]

の候補になります。更新幅は

\[
81,250-77,520=3,730.
\]

## controller 側の状況

26 頂点の simple cubic controller を直接探索しましたが、今回は完成しませんでした。

現時点の最良は、

\[
\text{missing ordered pairs}=19
\]

です。

つまり、26 頂点の 3-正則 graph で、exact nonbacktracking length 5 の endpoint coverage が全 ordered pair から 19 個だけ漏れている候補までは見つかりました。ただし、これはまだ controller ではありません。

いくつか自然な voltage controller も確認しました。

- \(K_4\times C_7\) は self-pair に対して exact NB length-5 base path が 6 本しかなく、7 residues を覆えないので不可能。
- triangular prism \(\times C_5\) は miss 16 まで近づきましたが、0 には届かず。
- random/simple cubic search は miss 19 が現時点の最良。

したがって、\((15,5)\) 方向はこういう状態です。

\[
\boxed{
\mathbb F_5^5\text{ chart は完成。}
}
\]

\[
\boxed{
26\text{-vertex cubic exact-NB5 controller が未完成。}
}
\]

## \((16,6)\) 方向も続けたが、controller がまだ重い

前回までに、\(\mathbb F_4^6\) の universal chart は完成していました。  
これを使うには、4-正則 controller \(C\) で、任意の ordered pair が exact NB length 6 で結ばれるものが必要です。

作業表の

\[
N(16,6)\ge1,771,560
\]

を超えるには、

\[
|C|\ge433
\]

が必要です。すると

\[
|V(G)|=|C|\cdot4^6.
\]

今回、いくつかの自然な controller lift を試しました。

- 既存の 132 頂点 length-5 controller を \(C_4\)-lift して length-6 controller にする案：random signing ではかなり弱い。
- 6 頂点 4-正則 multibase \(+C_{73}\)：best miss 158。
- 12 頂点 base \(+C_{37}\)、20 頂点 base \(+C_{22}\)：今回の短い探索では遠い。

この方向はまだ使えますが、現時点では controller が明確なボトルネックです。

## 今回の判断

完成済みの新記録候補は前回までの

\[
\boxed{N(16,5)\ge135,168}
\]

と

\[
\boxed{N(12,5)\ge32,076}
\]

です。

今回の新しい未完成だが有望な枝は：

\[
\boxed{
\text{3-regular controller}
+
\mathbb F_5^5\text{ universal chart}
}
\]

による

\[
\boxed{(d,k)=(15,5)}
\]

です。

次に集中するなら、最も小さく明確な問題は：

\[
\boxed{
26\text{ 頂点 cubic graph }C
\text{ で、全 ordered pair を exact NB length }5
\text{ で覆うものを作る。}
}
\]

これができれば、すぐに

\[
\boxed{N(15,5)\ge81,250}
\]

が出ます。

---

## Turn 174 (Round 041) — 🧑 USER

_2026-05-26 13:45:07 UTC_

続けてください

---

## Turn 175 (Round 041) — 🤖 ASSISTANT

_2026-05-26 13:45:29 UTC_  ·  model: `gpt-5-5-pro`

続けます。今回は \(\mathbb F_5^5\) chart を活かすため、26頂点 cubic exact-NB5 controller の存在性を必要条件・構造制約から絞り込みます。

---

## Turn 176 (Round 041) — 🤖 ASSISTANT

_2026-05-26 13:49:02 UTC_  ·  model: `gpt-5-5-pro`

今回は \((15,5)\) 枝を優先し、26頂点 cubic controller が通れば \(26\cdot5^5=81,250\) 頂点候補になる点を確認します。評価は exact NB5 到達行列 \(P_5(A)=A^5-9A^3+16A\) を使い、構造的に絞ります。

---

## Turn 177 (Round 041) — 🤖 ASSISTANT

_2026-05-26 13:58:29 UTC_  ·  model: `gpt-5-5-pro`

未完成枝を二つに分け、26頂点 cubic controller が未発見のまま、既存の \((16,5)\) controller を \(C_{23}\) へ拡張して 141,312 頂点へ伸ばす可能性も並行して調べます。

---

## Turn 178 (Round 041) — 🤖 ASSISTANT

_2026-05-26 14:09:36 UTC_  ·  model: `gpt-5-5-pro`

続けました。今回は **追加の新記録候補までは完成していません**。ただし、かなり有用な切り分けが進みました。

成果物はこちらです。

[phase28_generalization_followup.zip](sandbox:/mnt/data/phase28_generalization_followup.zip)

## 今回の主結果

### 1. \((15,5)\) 方向：26 頂点 cubic controller は少し改善

前回見つけた

\[
\mathbb F_5^5
\]

の 3-symbol universal chart を使うと、26 頂点 cubic controller があれば

\[
\Delta=15,\qquad D\le5,\qquad |V|=26\cdot5^5=81,250
\]

が得られます。

作業中の基準では

\[
N(15,5)\ge77,520
\]

なので、成功すれば

\[
+3,730
\]

の更新候補です。

今回、26 頂点 cubic graph の直接探索で、exact nonbacktracking length 5 の missing ordered pair を

\[
19 \to 18
\]

まで改善しました。

cubic graph の controller 条件は、隣接行列 \(A\) に対して

\[
P_5(A)=A^5-9A^3+16A
\]

が全成分正、つまり

\[
P_5(A)_{uv}>0\quad\forall u,v
\]

となることです。

現時点の best はまだ

\[
18
\]

個の ordered pair が漏れているので、controller ではありません。

---

### 2. 自然な \(6\)-base \(\times C_5\) cubic voltage controller は完全に否定

これはかなり重要です。

26 頂点 direct controller が難しいので、次の自然な構成を調べました。

\[
6\text{ 頂点 labelled cubic base}\times C_5.
\]

成功すれば 30 頂点 cubic controller になり、

\[
30\cdot5^5=93,750
\]

頂点の \((15,5)\) 候補になります。

この family は、switching で正規化すると有限個を完全探索できます。

- labelled 6-vertex cubic base: 720 個
- 各 base の \(C_5\)-voltage switching classes: \(5^4=625\)
- 合計：
  \[
  720\cdot625=450,000
  \]

全探索の結果、最良でも

\[
\text{missing residue conditions}=16
\]

でした。

したがって、

\[
\boxed{
6\text{-base}\times C_5
}
\]

という一番小さく自然な cubic voltage controller route は失敗です。これは単なるランダム失敗ではなく、完全探索による否定です。

---

### 3. 他の cubic voltage route はまだ弱い

短い探索として、

\[
8\text{-base}\times C_4
\]

と

\[
10\text{-base}\times C_3
\]

も試しました。

結果はそれぞれ best miss が約 34、22 で、まだ certificate に近い状態ではありません。

---

### 4. 5-regular controller \(+\mathbb F_3^5\) chart も試したが未達

\((15,5)\) には別ルートもあります。

controller を 5-regular にし、fiber を

\[
\mathbb F_3^5
\]

にすれば次数は

\[
5\cdot3=15.
\]

そのためには、5-symbol universal chart が必要です。

今回は次の 2 種類を試しました。

1. 5 個すべて self-inverse symbol。
2. 2 組の inverse pair \(a,a^{-1},b,b^{-1}\) と 1 個の self-inverse symbol \(c\)。

ランダム探索では、全 reduced word length 5 に対する controllability rank の最小値は 4 までで、rank 5 の universal chart は見つかりませんでした。

これは非存在証明ではありません。ただし現時点では、5-regular controller route は chart 側の証明書がないため、本線にはできません。

---

### 5. \((16,4)\) 用 controller route も少し確認

以前の

\[
\mathbb F_4^4
\]

chart を使えば、4-regular exact-NB4 controller が 58 頂点以上あれば

\[
(16,4)
\]

の更新候補になります。

今回は multibase relaxation として、

\[
5\text{ 頂点 loopless 4-regular multibase}\times C_{12}
\]

を試しました。成功すれば 60 頂点 controller です。

158 個の loopless 4-regular multibaseに対して短い探索を行い、best は

\[
\text{missing residue conditions}=9
\]

でした。certificate には届いていません。

---

## 現時点の判断

完成済みの route-chart 候補は、引き続き：

\[
\boxed{N(16,5)\ge135,168}
\]

\[
\boxed{N(12,5)\ge32,076}
\]

です。

今回の追加分では新しい完成候補は出ませんでした。

ただし、\((15,5)\) 方向について、最も自然な小型 voltage family

\[
6\text{-base}\times C_5
\]

を完全に潰せたのは有用です。今後 \((15,5)\) を狙うなら、

\[
\boxed{
26\text{ 頂点 cubic exact-NB5 controller}
}
\]

を直接、またはより柔軟な非 voltage 的 cubic construction で作る必要があります。現時点の direct best は missing 18 です。

---

## Turn 179 (Round 042) — 🧑 USER

_2026-05-26 14:16:16 UTC_

ここまでの結果をmdにまとめてください。このセッションは重くなりすぎたので、別セッションで引き継ぎます。その前提でまとめてください。

---

## Turn 180 (Round 042) — 🤖 ASSISTANT

_2026-05-26 14:16:39 UTC_  ·  model: `gpt-5-5-pro`

引き継ぎ用として、別セッションでそのまま読めるように「結論」「構成定理」「証明書」「未完成課題」「ファイル一覧」を一体化した md にまとめます。

---

## Turn 181 (Round 042) — 🤖 ASSISTANT

_2026-05-26 14:19:51 UTC_  ·  model: `gpt-5-5-pro`

成功済み候補と未完成枝の境界を明確にし、次セッションでまず verified zip の再検証から入れるように、検証コマンドと証明依存関係も含めます。

---

## Turn 182 (Round 042) — 🤖 ASSISTANT

_2026-05-26 14:24:57 UTC_  ·  model: `gpt-5-5-pro`

引き継ぎ用の Markdown にまとめました。完成済み候補、証明の骨格、一般化、未完成の枝、破棄した方向、再現手順、次セッションでの優先タスクまで入れています。

[引き継ぎ用 Markdown](sandbox:/mnt/data/route_chart_handoff_summary.md)

特に重要な証明書 zip も再掲します。

[検証済み \((16,5)\) 候補 zip](sandbox:/mnt/data/phase25_verified_controllable_chart_candidate.zip)

[検証済み \((12,5)\) 一般化 zip](sandbox:/mnt/data/phase26_gf3_generalization.zip)

[未完成 \((16,6)\) 用 GF(4)^6 chart zip](sandbox:/mnt/data/phase26_partial_gf4_s6.zip)

[未完成 \((15,5)\) 一般化探索 zip](sandbox:/mnt/data/phase28_generalization_followup.zip)

---

## Turn 183 (Round 043) — 🧑 USER

_2026-05-26 14:51:15 UTC_

一般化を続けてください

---

## Turn 184 (Round 043) — 🤖 ASSISTANT

_2026-05-26 14:51:38 UTC_  ·  model: `gpt-5-5-pro`

引き継ぎ内容を前提に、完成済みの route-chart 原理を崩さず一般化できる候補だけに絞ります。controller 側と fiber chart 側を分け、事前勝算のあるものだけ検査します。

---

## Turn 185 (Round 043) — 🤖 ASSISTANT

_2026-05-26 14:55:00 UTC_  ·  model: `gpt-5-5-pro`

まず既存証明書を再確認し、記録候補に直結する一般化だけを残します。特にGF(4)^6 chartを使う(16,6)用controllerを優先します。

---

## Turn 186 (Round 043) — 🤖 ASSISTANT

_2026-05-26 15:04:14 UTC_  ·  model: `gpt-5-5-pro`

既存132-controllerのC4-liftはendpoint数不足で弱いと分かりました。そこで(16,6)は、閾値433を超えるK5+C87型など大きめのcontroller設計へ切り替えています。

---

## Turn 187 (Round 043) — 🤖 ASSISTANT

_2026-05-26 15:16:24 UTC_  ·  model: `gpt-5-5-pro`

続けました。今回は追加の新記録完成までは出ていませんが、一般化として使える新しい部品が 1 つ完成しました。

成果物はこちらです。

[phase29_generalization_continued.zip](sandbox:/mnt/data/phase29_generalization_continued.zip)

## 今回の一番大きい進展

\[
\mathbb F_5^4
\]

上の **3-symbol universal chart** が完成しました。

記号は

\[
\{a,a^{-1},c\},\qquad c=c^{-1}
\]

です。長さ 4 の reduced word、つまり

\[
aa^{-1},\quad a^{-1}a,\quad cc
\]

を隣接部分語として含まない word は 24 個あります。その全てについて controllability matrix が full rank になることを確認しました。

検証出力は：

```text
checked 24 reduced words of length 4; min rank=4; bad=0
GF(5)^4 3-symbol universal chart: OK
```

これにより、もし **20 頂点以上の cubic controller** \(C\) で、任意の ordered pair が exact nonbacktracking length 4 walk で結ばれるものが作れれば、

\[
\Delta=3\cdot5=15,\qquad D\le4,\qquad |V|=|C|\cdot 5^4
\]

が得られます。

特に \(|C|=20\) なら

\[
|V|=20\cdot625=12,500.
\]

作業中の基準表では

\[
N(15,4)\ge 11,712
\]

だったので、controller が見つかれば

\[
12,500-11,712=788
\]

の更新候補になります。

## controller 側の状況

20 頂点 cubic controller を直接探索しましたが、今回は完成していません。現時点の best は：

\[
\text{missing ordered pairs}=50.
\]

つまり、exact nonbacktracking length 4 で届かない ordered pair が 50 個残っています。

この枝はまだ未完成ですが、fiber chart 側が完全に通ったので、問題はかなり小さな controller 探索に落ちました。

---

## \((16,6)\) 方向の検査

前回までに

\[
\mathbb F_4^6
\]

の universal chart は完成していました。したがって必要なのは、433 頂点以上の 4-正則 exact-NB6 controller です。

### 既存 132-controller の \(C_4\)-lift は弱い

既存の 132 頂点 controller を \(C_4\)-lift すれば 528 頂点 controller になり、

\[
528\cdot4^6=2,162,688
\]

頂点の \((16,6)\) 候補が狙えます。

しかし、132-controller の exact length 6 endpoint pair には、path が 2 本しかない pair がありました。したがって \(C_4\) の 4 residue を覆うには構造的に足りません。

実験でも最良は

\[
\text{missing residue conditions}=8,441
\]

で、かなり遠いです。このルートは本命から外します。

### \(K_5+C_{87}\) は数学的にはきれいだが未達

より筋が良い候補として、

\[
K_5 + C_{87}
\]

の voltage controller を試しました。

controller size は

\[
5\cdot87=435
\]

なので、完成すれば

\[
435\cdot4^6=1,781,760
\]

頂点の \((16,6)\) 候補になります。作業中の基準

\[
N(16,6)\ge1,771,560
\]

を超えます。

この候補の事前根拠は、\(K_5\) の exact NB length 6 path 数が各 base pair で

\[
192\text{〜}204
\]

あり、覆うべき residue 数

\[
87
\]

を大きく上回ることです。

ただし cyclic voltage search の現時点 best は：

\[
\text{missing residue conditions}=206.
\]

まだ certificate ではありません。

---

## その他の枝

\((8,5)\) を狙える可能性がある

\[
\mathbb F_2^5
\]

の 4-symbol chart は見つかっていません。random search の現時点 best は bad reduced words 104 です。

また、\((15,4)\) の別ルートとして

\[
\mathbb F_3^4
\]

の 5-symbol chart も試しましたが、こちらも未完成です。現時点 best は bad reduced words 54 です。

\((15,5)\) 用の

\[
\mathbb F_5^5
\]

3-symbol chart は以前から完成していますが、必要な 26 頂点 cubic exact-NB5 controller はまだ未完成です。前回 best は missing 18 ordered pairs でした。

---

## 現時点の優先順位

次に進むなら、この順です。

1. **20 頂点 cubic exact-NB4 controller**  
   今回完成した \(\mathbb F_5^4\) chart と組み合わせると、\((15,4,12500)\) が出ます。問題が小さく、最優先です。

2. **\(K_5+C_{87}\) exact-NB6 voltage controller**  
   成功すれば \((16,6,1781760)\)。path count の余裕はあるので、controller 設計としては筋があります。

3. **26 頂点 cubic exact-NB5 controller**  
   以前完成した \(\mathbb F_5^5\) chart と組み合わせると、\((15,5,81250)\) が出ます。

今回の完成成果は、

\[
\boxed{\mathbb F_5^4\text{ の 3-symbol universal chart}}
\]

です。新記録化には、対応する cubic controller が残っています。

---

## Turn 188 (Round 044) — 🧑 USER

_2026-05-26 15:25:26 UTC_

続けてください

---

## Turn 189 (Round 044) — 🤖 ASSISTANT

_2026-05-26 15:25:47 UTC_  ·  model: `gpt-5-5-pro`

まずは前回の優先順位どおり、完成済みの \(\mathbb F_5^4\) chart を活かす 20頂点 cubic exact-NB4 controller を最優先で詰めます。構造的に不可能そうなら理由を切り分け、次候補へ移ります。

---

## Turn 190 (Round 044) — 🤖 ASSISTANT

_2026-05-26 15:29:00 UTC_  ·  model: `gpt-5-5-pro`

20頂点 cubic controller は欠損数だけでなく、非戻り長さ4行列 \(P_4=A^4-7A^2+6I\) が全正になる条件として扱います。各始点から24本しかないため、かなりタイトな被覆問題です。

---

## Turn 191 (Round 044) — 🤖 ASSISTANT

_2026-05-26 15:38:16 UTC_  ·  model: `gpt-5-5-pro`

20頂点 cubic が硬いため、22・24頂点も含めて同じ \(\mathbb F_5^4\) chart の記録化可能性を見ます。並行して、5-regular controller＋\(\mathbb F_3^4\) や \((12,4)\) につながる短い controller 枝も確認します。

---

## Turn 192 (Round 044) — 🤖 ASSISTANT

_2026-05-26 15:49:01 UTC_  ·  model: `gpt-5-5-pro`

続けました。今回は **新しい記録候補の完成までは未達**ですが、一般化に使える部品がもう 1 つ完成しました。

成果物はこちらです。

[phase30_generalization_more.zip](sandbox:/mnt/data/phase30_generalization_more.zip)

## 今回の主な進展

\[
\mathbb F_3^4
\]

上の **4-symbol universal chart** が完成しました。

記号は

\[
a,\ a^{-1},\ b,\ b^{-1}
\]

です。長さ 4 の reduced word、つまり

\[
aa^{-1},\quad a^{-1}a,\quad bb^{-1},\quad b^{-1}b
\]

を隣接部分語として含まない word は

\[
4\cdot3^3=108
\]

個あります。その全てについて controllability matrix が full rank になることを確認しました。

検証出力は：

```text
checked 108 reduced words of length 4; min rank=4; bad=0
GF(3)^4 4-symbol field chart: OK
```

この chart は、\(\mathbb F_{3^4}\) を

\[
\mathbb F_3[x]/(x^4+x^3+2)
\]

として表し、field multiplication chart として構成しています。

---

## これで何が狙えるか

この chart と、4-正則 controller \(C\) を組み合わせると、

\[
V(G)=V(C)\times\mathbb F_3^4
\]

で

\[
\Delta(G)=4\cdot3=12,
\]

\[
\operatorname{diam}(G)\le4
\]

が得られます。ただし controller 側には、任意の ordered pair が exact nonbacktracking length 4 walk で結ばれる条件が必要です。

頂点数は

\[
|V(G)|=|C|\cdot3^4=81|C|.
\]

作業中の基準表では

\[
N(12,4)\ge4680.
\]

したがって、

\[
81|C|>4680
\]

すなわち

\[
|C|\ge58
\]

の controller があれば、新しい \((12,4)\) 候補になります。

特に 60 頂点 controller ができれば、

\[
|V(G)|=60\cdot81=4860,
\]

つまり

\[
4860-4680=180
\]

の更新候補です。

---

## controller 側の状況

今回は controller はまだ完成していません。

一番近かったのは、4-正則 6 頂点 multibase に cyclic voltage を載せる系です。

| controller route | controller size | best missing residue conditions | 判定 |
|---|---:|---:|---|
| 6-base \(+C_9\) | 54 | 2 | サイズ不足 |
| 6-base \(+C_{10}\) | 60 | 8 | 未完成だが有望 |
| 7-base \(+C_9\) | 63 | 19 以上 | 遠い |
| 8-base \(+C_8\) | 64 | 24 | 遠い |
| 6-base \(+D_5\) | 60 | 12 | \(C_{10}\) より弱い |

\(6\)-base \(+C_9\) は missing 2 まで来ましたが、controller size が

\[
6\cdot9=54
\]

なので、\((12,4)\) の記録更新には足りません。

一方、

\[
6\text{-base}+C_{10}
\]

は controller size が

\[
6\cdot10=60
\]

なので、もし missing 0 になれば、すぐに

\[
N(12,4)\ge4860
\]

の候補になります。現時点の best は missing 8 です。

---

## 現時点の判断

完成済みの一般化部品は増えました。

既にある完成済み候補：

\[
N(16,5)\ge135168,
\]

\[
N(12,5)\ge32076.
\]

今回新たに完成した部品：

\[
\boxed{\mathbb F_3^4\text{ 4-symbol universal chart}}
\]

未完成だが最短で新記録化できる枝：

\[
\boxed{
6\text{-vertex 4-regular multibase}+C_{10}
}
\]

による 60 頂点 exact-NB4 controller。

これが完成すれば、

\[
\boxed{
N(12,4)\ge4860
}
\]

が出ます。

次は、この \(6\)-base \(+C_{10}\) controller を、単なるランダム voltage search ではなく、missing residue 8 の obstruction を解析して詰めるのが最も筋が良いです。

---

## Turn 193 (Round 045) — 🧑 USER

_2026-05-26 16:08:06 UTC_

つづきお願いします

---

## Turn 194 (Round 045) — 🤖 ASSISTANT

_2026-05-26 22:40:30 UTC_  ·  model: `gpt-5-5-pro`

前回の一般化を受け、完成済み chart を記録化するための controller 構成に集中します。まず \( \mathbb F_3^4 \) chart の 60 頂点 controller 枝を復元し、missing 8 の obstruction が局所的か構造的限界かを切り分けます。

---

## Turn 195 (Round 045) — 🤖 ASSISTANT

_2026-05-26 22:43:57 UTC_  ·  model: `gpt-5-5-pro`

さらに小型の cubic exact-NB4 枝も並行して、閉路数・walk 数からほぼ Moore 的被覆が可能なサイズと構造を先に絞ります。6 頂点 multibase＋\(C_{10}\) は switching 後の 7 電圧変数の exact 問題として詰めます。

---

## Turn 196 (Round 045) — 🤖 ASSISTANT

_2026-05-26 22:57:25 UTC_  ·  model: `gpt-5-5-pro`

続けました。今回は **追加の新記録候補までは完成していません**。ただし、一般化に使える新しい部品が 1 つ完成しました。

成果物はこちらです。

[phase31_generalization_continue.zip](sandbox:/mnt/data/phase31_generalization_continue.zip)

## 今回の主な進展

\[
\mathbb F_2^5
\]

上の **3-symbol universal chart** が完成しました。

記号は

\[
a,\quad a^{-1},\quad c=c^{-1}
\]

です。長さ 5 の reduced word、つまり

\[
aa^{-1},\quad a^{-1}a,\quad cc
\]

を隣接部分語として含まない word は

\[
3\cdot2^4=48
\]

個あります。その全てについて controllability matrix が full rank になることを確認しました。

検証出力は：

```text
checked 48 reduced words; min rank 5; bad 0
GF(2)^5 3-symbol universal chart: OK
```

---

## これで何が狙えるか

この chart と cubic controller \(C\) を組み合わせると、

\[
V(G)=V(C)\times\mathbb F_2^5
\]

で、

\[
\Delta(G)=3\cdot2=6,
\]

\[
\operatorname{diam}(G)\le5
\]

が得られます。ただし controller 側には、任意の ordered pair が exact nonbacktracking length 5 walk で結ばれる条件が必要です。

頂点数は

\[
|V(G)|=|C|\cdot2^5=32|C|.
\]

作業中の基準表では

\[
N(6,5)\ge1404.
\]

したがって、

\[
32|C|>1404
\]

すなわち

\[
|C|\ge44
\]

の cubic controller があれば、新しい \((6,5)\) 候補になります。

特に \(|C|=44\) なら

\[
|V(G)|=44\cdot32=1408,
\]

つまり作業表基準で

\[
1408-1404=4
\]

の更新候補です。

---

## controller 側の状況

今回は controller はまだ完成していません。

試した範囲では：

- 44, 46, 48 頂点の cubic exact-NB5 controller 直接探索は、missing ordered pair が数百規模で残りました。
- \(K_4\times C_{11}\) cyclic voltage controller は、44 頂点になりますが、best missing residue count は 62 で遠いです。
- 6 頂点 cubic base \(\times C_8\) なども、今回の短い検査では certificate に近づきませんでした。

つまり、今回もボトルネックは chart ではなく controller です。

---

## 現時点の更新された部品表

完成済みの記録候補は引き続き：

\[
\boxed{N(16,5)\ge135168}
\]

\[
\boxed{N(12,5)\ge32076}
\]

完成済み chart 部品としては：

- \(\mathbb F_4^5\), 4-symbol chart → \((16,5)\) に使用済み。
- \(\mathbb F_3^5\), 4-symbol chart → \((12,5)\) に使用済み。
- \(\mathbb F_4^6\), 4-symbol chart → \((16,6)\) 用 controller 未完成。
- \(\mathbb F_5^5\), 3-symbol chart → \((15,5)\) 用 cubic controller 未完成。
- \(\mathbb F_5^4\), 3-symbol chart → \((15,4)\) 用 cubic controller 未完成。
- \(\mathbb F_3^4\), 4-symbol chart → \((12,4)\) 用 4-regular controller 未完成。
- **新規：\(\mathbb F_2^5\), 3-symbol chart** → \((6,5)\) 用 cubic controller 未完成。

## 次に進むなら

いま一番小さく定義できる未解決 controller 問題は：

\[
\boxed{
44\le |C|\le48
\text{ の cubic graph で、全 ordered pair を exact NB length }5
\text{ で覆うものを作る。}
}
\]

ただし今回の直接探索はかなり遠かったので、これも単純なランダム switch ではなく、exact-NB5 endpoint distribution を設計する構造的 controller が必要です。

---

## Turn 197 (Round 046) — 🧑 USER

_2026-05-26 23:02:14 UTC_

つづきお願いします

---

## Turn 198 (Round 046) — 🤖 ASSISTANT

_2026-05-26 23:02:37 UTC_  ·  model: `gpt-5-5-pro`

続けます。今回は新しい chart 追加より、既存 chart を記録化するための exact-NB controller、特に小さな voltage-lift 候補を優先して検査します。

---

## Turn 199 (Round 046) — 🤖 ASSISTANT

_2026-05-26 23:05:48 UTC_  ·  model: `gpt-5-5-pro`

今回は未完成枝のうち、成功時の効果が大きい小型 controller に絞り、特に \((15,4)\) 用 cubic controller と \((12,4)\) 用 4-regular controller を重点的に検査します。

---

## Turn 200 (Round 046) — 🤖 ASSISTANT

_2026-05-26 23:15:01 UTC_  ·  model: `gpt-5-5-pro`

途中結果として、直近有望だった \(6\)-vertex multibase \(+C_{10}\) は固定 base 上の電圧を完全探索し、miss 8 が下限だと分かりました。電圧調整だけでは通りません。

---

## Turn 201 (Round 046) — 🤖 ASSISTANT

_2026-05-26 23:23:37 UTC_  ·  model: `gpt-5-5-pro`

続けました。今回は **追加の新記録候補の完成までは未達**です。ただし、未完成枝のうち 1 つをかなりはっきり否定できました。

成果物はこちらです。

[phase32_generalization_followup.zip](sandbox:/mnt/data/phase32_generalization_followup.zip)

## 今回の主結果

前回までの完成済み候補はそのままです。

\[
N(16,5)\ge135168
\]

\[
N(12,5)\ge32076
\]

今回は、次の未完成枝を中心に調べました。

\[
\mathbb F_3^4\text{ 4-symbol chart}
+
\text{4-regular exact-NB4 controller}
\]

この chart を使うと、60 頂点 controller があれば

\[
\Delta=12,\qquad D\le4,\qquad |V|=60\cdot3^4=4860
\]

となり、作業中の基準

\[
N(12,4)\ge4680
\]

を超えます。

---

## 1. \(6\)-vertex multibase \(+C_{10}\) は固定 base 上では不可能

前回までに有望だった候補は：

\[
6\text{ 頂点 4-regular multibase}+C_{10}
\]

です。controller size は

\[
6\cdot10=60.
\]

前回の best は missing residue conditions が

\[
8
\]

でした。

今回、その **固定された best base** に対して、switching 正規化後の全 \(C_{10}\)-voltage assignment を完全探索しました。

結果：

\[
\boxed{\text{best missing}=8}
\]

つまり、この base ではどんな \(C_{10}\)-voltage を選んでも controller 条件は満たせません。

これはかなり有用な否定結果です。  
単なる局所探索の失敗ではなく、固定 base 上では完全に詰みです。

---

## 2. 他の \((12,4)\) controller 候補

比較として、いくつかの cyclic multibase controller も継続しました。

| controller family | controller size | best missing | 判定 |
|---|---:|---:|---|
| \(5\)-vertex multibase \(+C_{12}\) | 60 | 7 | 近いが未完成 |
| \(6\)-vertex multibase \(+C_{10}\) | 60 | 8 | 固定 best base は完全探索で不可能 |
| \(7\)-vertex multibase \(+C_9\) | 63 | 25 | 弱い |
| \(6\)-vertex multibase \(+C_{11}\) | 66 | 22 | 弱い |

現時点では、\((12,4)\) 方向で一番近いのはまだ

\[
5\text{-base}+C_{12}
\]

または別の

\[
6\text{-base}+C_{10}
\]

ですが、次はランダム電圧変更ではなく、base ごとに exact / CP / SAT 的に解くべきです。

---

## 3. \((16,5)\) controller の大型化も試したが未達

完成済みの \((16,5)\) 候補は

\[
6\text{-vertex multibase}+C_{22}
\]

から得た 132 頂点 controller を使っています。

自然な一般化は

\[
C_{22}\to C_m,\qquad m>22
\]

として controller を大きくすることです。成功すれば

\[
6m\cdot4^5
\]

頂点の \((16,5)\) 候補になります。

今回は \(m=23\) を調べました。

結果：

- 任意の 6-vertex multibase \(+C_{23}\) 探索：best missing 16。
- 成功済み \(C_{22}\) base を固定して \(C_{23}\) voltage 探索：best missing 18。

したがって、今回は 132 頂点 controller を超える一般化は出ていません。

---

## 4. named cubic graph を controller base として確認

3-symbol chart 系では cubic controller が必要です。そこで、Petersen graph、Frucht graph、truncated tetrahedron graph なども確認しました。

興味深い点として、Petersen graph や Frucht graph は base として exact NB5 coverage を持ちます。  
しかし \(C_3\), \(C_4\) voltage lift では residue coverage がかなり弱く、記録更新に使える controller にはなりませんでした。

結論として、

\[
\text{base 自体が exact-NB coverage を持つ}
\]

だけでは不十分です。voltage lift で使うには、各 ordered pair に対する path multiplicity と path-incidence diversity が必要です。

---

## 現時点の判断

今回の追加作業で、新しい完成候補は出ていません。

ただし、次のことは明確になりました。

\[
\boxed{
6\text{-base}+C_{10}
\text{ の前回 best base は、完全探索で不可能}
}
\]

なので、\((12,4)\) を続けるなら、同じ base の voltage 微調整はやめるべきです。

今後の優先順位は：

1. \((12,4)\)：別の \(5\)-base/\(6\)-base multibase を、exact covering 問題として解く。
2. \((16,5)\)：\(C_m, m>22\) で大型 controller を狙うなら、既存 \(C_{22}\) base ではなく別 multibaseまたは非巡回群を試す。
3. cubic controller 系：単に exact-NB coverage を持つ小 graph ではなく、voltage residue を分離できる path diversity を重視する。

完成済みの結果は引き続き：

\[
\boxed{N(16,5)\ge135168}
\]

\[
\boxed{N(12,5)\ge32076}
\]

です。

---

## Turn 202 (Round 047) — 🧑 USER

_2026-05-27 00:55:16 UTC_

一度立ち止まって方針を検討してください。

---

## Turn 203 (Round 047) — 🤖 ASSISTANT

_2026-05-27 00:56:05 UTC_  ·  model: `gpt-5-5-pro`

ここで探索を止め、方針レビューに切り替えます。成功済み chart は土台にしつつ、今後は controller の一般設計原理が立つ枝だけを残します。

---

## Turn 204 (Round 047) — 🤖 ASSISTANT

_2026-05-27 00:59:25 UTC_  ·  model: `gpt-5-5-pro`

候補数ではなく、成功条件の強さで枝を仕分けます。成果後の一般化段階なので、続ける価値をまず判定します。

---

## Turn 205 (Round 047) — 🤖 ASSISTANT

_2026-05-27 01:01:06 UTC_  ·  model: `gpt-5-5-pro`

はい。ここはかなり大事な分岐点です。いまの状況を冷静に見ると、**route-chart 原理そのものは強い**ですが、一般化フェーズが少しずつ「controller を色々試す」方向に流れかけています。そこは止めた方がいいです。

## まず結論

今後の方針は、次のように切り替えるべきです。

\[
\boxed{
\text{route-chart lift は継続する。}
}
\]

ただし、

\[
\boxed{
\text{controller 探索は、単なる voltage search / random switch から撤退する。}
}
\]

次に必要なのは、

\[
\boxed{
\text{controller の path-voltage set が群全体を覆うことを、加法組合せ論で保証する構成}
}
\]

です。

つまり、次の本線は：

\[
\boxed{
\textbf{sumset-certified controller}
}
\]

です。

---

# 1. いま何が本当に成功しているか

成功済みの構成は、次の二段構造です。

## Fiber 側

有限体 \(\mathbb F_q^s\) 上の controllable chart を作る。

長さ \(s\) の reduced word

\[
w=s_1s_2\cdots s_s
\]

に対して、controllability matrix が正則になるようにする。すると、controller 上にその word を持つ exact nonbacktracking route が 1 本あれば、その route だけで fiber の全点

\[
q^s
\]

を一意に routing できます。

これは強いです。

\[
\boxed{
1\text{ route}=q^s\text{ target を完全に覆う}
}
\]

という情報効率があるので、これは継続する価値があります。

## Controller 側

残る条件は、controller \(C\) が任意の ordered pair を exact nonbacktracking length \(s\) で結ぶこと。

voltage lift で作る場合、base graph \(B\)、群 \(H\)、voltage \(\phi\) に対して、各 base pair \((i,j)\) の path-voltage set

\[
S_{ij}
=
\{
\phi(P):P\text{ is exact NB length }s\text{ walk }i\to j
\}
\]

が

\[
H
\]

全体を覆えばよい。

成功済みの \((16,5)\) では、6 頂点 4-正則 multibase と \(C_{22}\) がこれを満たしました。

---

# 2. いま何が弱くなっているか

最近の一般化では、controller 側で

- \(C_m\) の \(m\) を変える
- base を少し変える
- voltage をランダムまたは局所的に変える
- missing residue を減らす

という作業が増えていました。

これは危ないです。  
なぜなら、証明済み候補が出た後の一般化で必要なのは、

\[
\text{たまたま missing が 0 になる探索}
\]

ではなく、

\[
\text{なぜ residue 全体を覆うのかが事前に見える設計}
\]

だからです。

したがって、以下は今後の主戦略から外すべきです。

\[
\boxed{
\text{固定 base 上の cyclic voltage local search}
}
\]

\[
\boxed{
\text{random multibase + random voltage の反復}
}
\]

\[
\boxed{
\text{missing が少ないから微調整で押す方針}
}
\]

---

# 3. 新しい controller 原理：sumset-certified controller

今後の本命はこれです。

base graph \(B\) の exact length \(s\) path を、前半と後半、あるいは複数の block に分解します。

たとえば length 5 なら、

\[
P=P_1P_2
\]

のように分けて、voltage sum が

\[
\phi(P)=\phi(P_1)+\phi(P_2)
\]

となるように見る。

すると、ある base pair \((i,j)\) について path-voltage set が

\[
S_{ij}\supset A_{ij}+B_{ij}
\]

という **sumset** を含むことがあります。

ここで \(H=C_p\) が素数位数の巡回群なら、Cauchy-Davenport により

\[
|A+B|\ge \min(p,\ |A|+|B|-1).
\]

したがって、

\[
|A|+|B|\ge p+1
\]

なら

\[
A+B=C_p.
\]

つまり、各 \((i,j)\) について path-voltage set を直接全部調べなくても、

\[
\boxed{
S_{ij}\supset A_{ij}+B_{ij},\qquad |A_{ij}|+|B_{ij}|\ge p+1
}
\]

を証明すれば、

\[
S_{ij}=C_p
\]

が保証されます。

これが今後の controller 設計の新しい主原理です。

---

# 4. なぜこれは数学的に勝算があるか

この方針は、これまでの voltage search と違います。

従来は、

\[
\text{たくさんの path voltage が偶然 residue を全部打つ}
\]

ことを期待していました。

sumset-certified controller では、

\[
\text{前半 route の residue set}
+
\text{後半 route の residue set}
\]

が、加法組合せ論の定理によって全体を覆います。

つまり、coverage が偶然ではなく、

\[
\boxed{
\text{大きな部分集合の和は全群を覆う}
}
\]

という数学的事実から出ます。

これは route-chart 原理と相性が良いです。

- fiber 側：1 route が fiber 全体を覆う。
- controller 側：route families が sumset として group 全体を覆う。

両方とも「ランダム被覆」ではなく「決定的被覆」です。

---

# 5. 具体的に狙うべきターゲット

## 第一候補：\((16,5)\) の大型化

現在完成済み：

\[
N(16,5)\ge135168
\]

これは

\[
6\text{-base}+C_{22}
\]

controller から来ています。

次に狙うなら、同じ \(s=5,q=4\) で controller を大きくする。

たとえば

\[
6\text{-base}+C_{23}
\]

が通れば、

\[
|C|=6\cdot23=138,
\]

\[
|V|=138\cdot4^5=141312.
\]

これは現在の 135,168 からさらに大きく伸びます。

ただし、これまでの \(C_{23}\) random voltage は失敗しています。  
今後は random search ではなく、\(C_{23}\) 上で

\[
S_{ij}\supset A_{ij}+B_{ij},\qquad |A_{ij}|+|B_{ij}|\ge24
\]

を保証する base/voltage を設計するべきです。

つまり、各 \((i,j)\) に対して、前半・後半 route sets のサイズを例えば

\[
12+12,\quad 11+13,\quad 10+14
\]

のように確保する。

これができれば \(C_{23}\) coverage は証明で出ます。

---

## 第二候補：\((12,4)\)

すでに

\[
\mathbb F_3^4
\]

の 4-symbol chart は完成しています。

必要なのは 4-regular exact-NB4 controller です。

もし

\[
6\text{-base}+C_{11}
\]

が通れば controller size は

\[
66
\]

で、最終グラフは

\[
66\cdot3^4=5346.
\]

作業中の基準

\[
N(12,4)\ge4680
\]

を大きく超えます。

length 4 なので、path を

\[
2+2
\]

に分けます。

\(C_{11}\) 上で Cauchy-Davenport を使うなら、各 \((i,j)\) に対して

\[
S_{ij}\supset A_{ij}+B_{ij},
\]

\[
|A_{ij}|+|B_{ij}|\ge12
\]

があればよい。

たとえば

\[
6+6
\]

の前半・後半 residue set を各 pair で作れれば、coverage が保証されます。

これは非常に明確な設計目標です。  
以前の \(6\)-base \(+C_{10}\) や \(C_{11}\) random search とは違い、今後は

\[
\boxed{
\text{length 2 prefix/suffix residue sets が C}_{11}\text{ 上で十分大きい}
}
\]

ことを設計条件にすべきです。

---

## 第三候補：\((16,6)\)

\[
\mathbb F_4^6
\]

の chart は完成済みです。

必要なのは、4-regular exact-NB6 controller で、サイズ

\[
|C|\ge433.
\]

有望な形は

\[
6\text{-base}+C_{73}
\]

です。

controller size は

\[
6\cdot73=438,
\]

最終グラフは

\[
438\cdot4^6=1,794,048.
\]

作業中の基準

\[
N(16,6)\ge1,771,560
\]

を超えます。

length 6 なら、path を

\[
2+2+2
\]

または

\[
3+3
\]

に分けます。

\(C_{73}\) で三つの sumset を使うなら、Cauchy-Davenport の反復で

\[
|A+B+C|\ge \min(73,\ |A|+|B|+|C|-2).
\]

したがって、

\[
|A|+|B|+|C|\ge75
\]

なら全 \(C_{73}\) を覆えます。

例えば

\[
25+25+25
\]

の residue sets を作れれば十分です。

これは難しいですが、random voltage を回すよりは、何を設計すべきかが明確です。

---

# 6. 具体的な controller 設計の形

今後は base multigraph を次のように作るべきです。

## Router layer 構造

base 頂点を少数の layer に分ける。

length \(s\) path が、source から target へ向かうときに、複数の中間 layer を通るようにする。

たとえば length 4 なら：

\[
i \to L_1 \to L_2 \to j
\]

のような形。

ただし base は 4-regular なので、完全な layered digraph は作れません。  
代わりに、loopless 4-regular multigraph で、parallel edges と carefully chosen nonbacktracking constraints を使う。

重要なのは、各 \((i,j)\) に対して path set が自然に

\[
A_{ij}+B_{ij}
\]

や

\[
A_{ij}+B_{ij}+C_{ij}
\]

として分解されることです。

## Voltage の役割

voltage は、各 route block が大きい residue set を作るように置く。

たとえば \(C_p\) で、ある block の alternatives が

\[
\{0,1,2,\dots,t-1\}
\]

を作るようにする。

すると、block を足し合わせるだけで interval sumset が広がり、最終的に全 \(C_p\) を覆う。

この設計なら、coverage は

\[
\text{path enumeration}
\]

ではなく

\[
\text{sumset lower bound}
\]

から出ます。

---

# 7. 今後の stop / go criteria

今後は次の基準を使うべきです。

## 続けてよい場合

ある controller family について、各 base pair \((i,j)\) の path-voltage set が

\[
A+B
\]

または

\[
A+B+C
\]

を含み、Cauchy-Davenport / Kneser によって群全体を覆う見込みがある場合。

つまり、coverage の理由が

\[
\boxed{
\text{sumset theorem}
}
\]

として見えている場合。

## 止めるべき場合

- missing residue を少しずつ減らすだけ。
- voltage をランダムに変えて best missing を追うだけ。
- base を変えて短い run を回すだけ。
- path count は多いが、sumset 分解がない。

これらは停止します。

---

# 8. 現時点の最終判断

現在の完成済み結果：

\[
\boxed{N(16,5)\ge135168}
\]

\[
\boxed{N(12,5)\ge32076}
\]

route-chart 原理は継続価値があります。

しかし、一般化の次フェーズは、

\[
\boxed{
\text{controller を加法組合せ論で設計する}
}
\]

に切り替えるべきです。

次に最も筋が良い具体ターゲットは：

\[
\boxed{
(12,4):\quad \mathbb F_3^4\text{ chart}+6\text{-base}+C_{11}
}
\]

です。

理由は、length 4 なので

\[
2+2
\]

の sumset 設計で済み、\(C_{11}\) なら

\[
6+6>11
\]

という明確な Cauchy-Davenport 証明が狙えるからです。

その次が：

\[
\boxed{
(16,5):\quad C_{23}\text{ 以上への大型化}
}
\]

最後に：

\[
\boxed{
(16,6):\quad C_{73}\text{ controller}
}
\]

です。

これ以降は、単なる探索ではなく、

\[
\boxed{
\text{sumset-certified controller を構成できるか}
}
\]

を中心に進めるべきです。

---

## Turn 206 (Round 048) — 🧑 USER

_2026-05-27 01:52:27 UTC_

続けてください

---

## Turn 207 (Round 048) — 🤖 ASSISTANT

_2026-05-27 01:52:54 UTC_  ·  model: `gpt-5-5-pro`

方針どおり、missing を減らすランダム探索ではなく、sumset 証明が出せる controller に絞ります。まず \((12,4)\) の \(6\)-base+\(C_{11}\) を検査します。

---

## Turn 208 (Round 048) — 🤖 ASSISTANT

_2026-05-27 01:56:11 UTC_  ·  model: `gpt-5-5-pro`

既存の \(6\)-base+\(C_{11}\) は miss 22 付近で止まるため、電圧調整ではなく 2+2 sumset 証明が可能な base かを容量条件から検査します。

---

## Turn 209 (Round 048) — 🤖 ASSISTANT

_2026-05-27 02:05:32 UTC_  ·  model: `gpt-5-5-pro`

途中で重要な否定結果が出ました。6 頂点 4-正則 loopless multibase では length-4 NB path 数の最小値が高々 10 で、\(C_{11}\) 全 residue 被覆は不可能です。

---

## Turn 210 (Round 048) — 🤖 ASSISTANT

_2026-05-27 02:16:16 UTC_  ·  model: `gpt-5-5-pro`

続けました。今回は **新しい完成候補は出ていません**が、方針検討としてはかなり重要な結果が出ました。

成果物はこちらです。

[phase33_sumset_strategy_check.zip](sandbox:/mnt/data/phase33_sumset_strategy_check.zip)

## 結論

前回提案した

\[
\text{sumset-certified controller}
\]

のうち、最も単純な

\[
\text{1つの中間点で path を }2+2,\ 2+3,\ 3+3\text{ に割り、Cauchy-Davenport で覆う}
\]

という形は、**6 頂点 4-正則 multibase では path-count の時点で不可能**でした。

これは単なる探索失敗ではなく、voltage をどう選んでもその証明方式では無理、という切り分けです。

## 何を検査したか

6 頂点の loopless 4-regular multigraph、つまり parallel edge は許すが loop は許さない base を全列挙しました。

列挙数は

\[
3355
\]

個の labelled degree matrix です。

その各 base について、exact nonbacktracking route を block に分けたとき、各 ordered pair に対してどれだけの block path 数が最大で使えるかを調べました。

---

## 1. \((12,4)\) 用：\(6\)-base \(+C_{11}\)

狙いは：

\[
\mathbb F_3^4\text{ chart}
+
6\text{-base}+C_{11}
\]

で、controller size

\[
6\cdot11=66
\]

を作ることでした。成功すれば

\[
66\cdot3^4=5346
\]

頂点の \((12,4)\) 候補になります。

length 4 path を

\[
2+2
\]

に分けて、\(C_{11}\) 上で Cauchy-Davenport を使うなら、各 ordered pair について

\[
|A|+|B|\ge 12
\]

が必要です。

しかし、全 6-base を列挙した結果、最良の base でも、全 ordered pair に対する worst case は

\[
\boxed{6}
\]

でした。

つまり、

\[
6<12.
\]

したがって、**6-base \(+C_{11}\) を 2+2 sumset 証明で通すことは不可能**です。

---

## 2. \((16,5)\) 大型化用：\(6\)-base \(+C_{23}\)

完成済みの \((16,5)\) 候補は

\[
6\text{-base}+C_{22}
\]

で controller size 132 を作りました。

次に自然なのは

\[
6\text{-base}+C_{23}
\]

で controller size

\[
138
\]

に上げることです。成功すれば

\[
138\cdot4^5=141312
\]

頂点になります。

length 5 path を

\[
2+3
\]

または

\[
3+2
\]

に分け、\(C_{23}\) 上で Cauchy-Davenport を使うなら、

\[
|A|+|B|\ge24
\]

が必要です。

全 6-base 列挙の結果、最良 worst case は

\[
\boxed{10}
\]

でした。

つまり、

\[
10<24.
\]

したがって、**6-base \(+C_{23}\) を単純な 2+3 sumset 証明で通すことも不可能**です。

---

## 3. \((16,6)\) 用：\(6\)-base \(+C_{73}\)

\[
\mathbb F_4^6
\]

の chart はすでに完成しています。controller を

\[
6\text{-base}+C_{73}
\]

で作れれば、

\[
438\cdot4^6=1,794,048
\]

頂点の \((16,6)\) 候補になります。

length 6 path を

\[
3+3
\]

に分けると、\(C_{73}\) では

\[
|A|+|B|\ge74
\]

が必要です。

全 6-base の最良 worst case は

\[
\boxed{16}
\]

でした。

したがって、この単純な 3+3 sumset certificate も不可能です。

---

## 追加の cyclic voltage sanity check

主戦略ではありませんが、比較として少し探索も行いました。

- \(6\)-base \(+C_{11}\), length 4：ランダム探索では best missing 22。固定 base の途中 exhaust では 20 まで改善しましたが、証明候補なし。
- \(5\)-base \(+C_{13}\), length 4：best missing 10。証明候補なし。

これらは「惜しいから続ける」べきものではありません。上の path-count obstruction から、少なくとも単純 sumset 証明では通らないことが分かっています。

## 方針の更新

route-chart lift 自体は続ける価値があります。すでに完成済み候補は：

\[
\boxed{N(16,5)\ge135168}
\]

\[
\boxed{N(12,5)\ge32076}
\]

です。

ただし、今後の controller 一般化で避けるべきなのは：

\[
\boxed{
\text{小さい 6-base に cyclic voltage を置いて missing を減らすだけ}
}
\]

です。

今回の結果から、次に進むなら次のどちらかです。

1. **より大きい base + 小さい group**  
   たとえば以前の \(12\)-base \(+C_5\) は、group が小さいのでまだ筋があります。ただし random voltage ではなく、exact/CP/SAT 的な coverage 問題として解くべきです。

2. **単一 split ではなく、複数 sumset の union を使う高次証明**  
   1 つの中間点で \(A+B\) を全群にするのは無理でした。今後やるなら、複数中間点の sumset union や Kneser 型の構造を使う必要があります。

今回の判断としては、**6-base の単純 sumset route は打ち切り**です。次は \(12\)-base \(+C_5\) の exact covering、または複数 sumset certificate に絞るのが一番筋が良いです。

---

## Turn 211 (Round 049) — 🧑 USER

_2026-05-27 02:51:33 UTC_

つづきお願いします
数学的に事前に今欲しい性質を持つと期待できる理由があるアイデアを考えることに集中してください。数学的に勝算が見込める理由がない方法を順番に試すのは効率が非常に悪いです。良いアイデアが枯渇したらこの探索自体を停止します。

---

## Turn 212 (Round 049) — 🤖 ASSISTANT

_2026-05-27 02:52:25 UTC_  ·  model: `gpt-5-5-pro`

まず controller の存在理由を先に固定し、route-chart の強みは保ったまま exact nonbacktracking 被覆を行列・スペクトル・証明可能な構造から見直します。Missing 改善型の試行は止め、全 endpoint/residue を覆う十分条件が見える候補だけ残します。

---

## Turn 213 (Round 049) — 🤖 ASSISTANT

_2026-05-27 02:55:51 UTC_  ·  model: `gpt-5-5-pro`

今度は controller 条件を多項式不等式として扱い、事前に positivity が保証できる構造に絞ります。ランダム voltage 調整は候補から外します。

---

## Turn 214 (Round 049) — 🤖 ASSISTANT

_2026-05-27 03:08:09 UTC_  ·  model: `gpt-5-5-pro`

立ち止まって検討した結果、次に進める価値があるアイデアは **1 つだけ** だと思います。

いまは、既存の成功結果

\[
N(16,5)\ge135168,\qquad N(12,5)\ge32076
\]

をさらに一般化する段階です。しかし、最近の試行は「base や cyclic voltage を少し変えて missing を減らす」方向に流れかけていました。これはやめるべきです。数学的な勝算が見える構成原理に戻します。

---

## 次に残すべき新原理：CRT-block controller

新しい有望候補は、

\[
\boxed{
\text{CRT-block / complementary-subgroup controller}
}
\]

です。

狙いは、完成済みの \((16,5)\) 構成を

\[
6\text{-base}+C_{22}
\]

から、より大きな

\[
6\text{-base}+H,\qquad |H|=24
\]

へ拡張することです。

具体的には

\[
H=C_4\times C_6
\]

を使います。もし 6 頂点 4-正則 multibase の \(H\)-voltage lift で exact nonbacktracking length 5 controller が作れれば、controller 頂点数は

\[
6\cdot24=144.
\]

既存の \(\mathbb F_4^5\) universal chart と合成して、

\[
|V|=144\cdot4^5=144\cdot1024=147456,
\]

\[
\Delta=16,\qquad D\le5
\]

になります。

これは既存の完成候補

\[
135168
\]

をさらに

\[
147456-135168=12288
\]

伸ばします。

---

## なぜ \(C_4\times C_6\) なのか

以前の \(C_{23}\) や \(C_{24}\) cyclic voltage をランダムに探す方向には、数学的な勝算が弱いです。path voltage がたまたま全 residue を覆うことを期待しているだけになりがちです。

一方、

\[
H=C_4\times C_6
\]

には明確な被覆証明の形があります。

length 5 の base path を

\[
2+3
\]

に分けます。ある ordered base pair \((i,j)\) について、中間頂点 \(t\) を選び、

\[
i \xrightarrow{\text{length }2} t
\]

の prefix path voltage が

\[
C_4\times\{0\}
\]

を覆い、

\[
t \xrightarrow{\text{length }3} j
\]

の suffix path voltage が

\[
\{0\}\times C_6
\]

を覆えば、連結した length 5 path の voltage は

\[
(C_4\times\{0\})+(\{0\}\times C_6)
=
C_4\times C_6
\]

を全部覆います。

つまり、

\[
\boxed{
\text{prefix が }C_4\text{ を覆う}
}
\]

\[
\boxed{
\text{suffix が }C_6\text{ を覆う}
}
\]

だけで、全 \(24\) residue coverage が証明できます。

これは、単なる「たくさん path があるからたぶん覆う」ではありません。中国剰余的な直積分解による決定的被覆です。

---

## 事前チェック：path count は足りるか

この原理が成立するには、少なくとも各 ordered pair \((i,j)\) に対して、どこかの中間点 \(t\) があり、

\[
\#\{\text{length 2 NB paths }i\to t\}\ge4,
\]

\[
\#\{\text{length 3 NB paths }t\to j\}\ge6
\]

である必要があります。

6 頂点 loopless 4-regular multibase 全体について、この count 条件を調べました。

結果は：

| 分解候補 | 必要 count | 6-base 全体での判定 |
|---|---:|---|
| \(C_3\times C_8\) | \(3+8\) | 全 pair を満たす base は見つからない |
| \(C_4\times C_6\) | \(4+6\) | 条件を満たす base が存在 |
| \(C_2\times C_{12}\) | \(2+12\) | 全 pair を満たす base は見つからない |

したがって、

\[
\boxed{
C_4\times C_6
}
\]

が、6 頂点 4-正則 multibaseで length 5 controller を伸ばすうえで、最初に数学的に成立しうる分解です。

これはかなり重要です。  
\(C_4\times C_6\) は「なんとなく選んだ」ものではなく、degree 4・length 5・6 頂点 base の path-count 制約から自然に出てきています。

---

## ただし、残る本質的な難所

ここで注意すべき点があります。

単に count が足りるだけでは不十分です。

実際に必要なのは、prefix 側の voltage が

\[
C_4\times\{0\}
\]

を覆り、suffix 側の voltage が

\[
\{0\}\times C_6
\]

を覆うように、edge voltage を設計できることです。

標準的な voltage graph では、edge は「prefix 用」「suffix 用」を自動的には知らないので、同じ edge が別の ordered pair では prefix に出たり suffix に出たりします。ここが構成上の核心です。

したがって、次に解くべき問題は：

\[
\boxed{
6\text{ 頂点 4-正則 multibase の edge に }C_4\times C_6\text{ voltage を置き、}
}
\]

\[
\boxed{
各 ordered pair に対して、prefix/suffix の complementary subgroup coverage certificate を持たせる}
}
\]

という有限設計問題です。

これは random voltage search ではありません。  
「各 pair の witness intermediate \(t\) と、その prefix/suffix path family が直積因子を覆う」という証明書を直接作る問題です。

---

## いま捨てるべき方向

次は、以下の方向には進みません。

\[
\boxed{
C_m\text{ を少し変えて missing が減るか試す}
}
\]

\[
\boxed{
同じ base で局所 voltage 変更を繰り返す}
}
\]

\[
\boxed{
path count は多いが、被覆証明の形がない候補を試す}
}
\]

これらは、今回の基準では時間効率が悪いです。

---

## 今後の stop / go criterion

この \(C_4\times C_6\) idea には数学的な勝算があります。理由は：

\[
\boxed{
C_4\times C_6
=
(C_4\times\{0\})+(\{0\}\times C_6)
}
\]

という決定的な被覆構造があり、必要な prefix/suffix path count も 6 頂点 4-正則 multibase で実際に達成可能だからです。

ただし、次の段階で

\[
\text{complementary-subgroup coverage certificate}
\]

が作れないなら、そこでこの枝は止めるべきです。

つまり次の判断基準は：

### 続ける条件

6-base と \(C_4\times C_6\) voltage に対し、各 ordered pair \((i,j)\) ごとに

\[
S_{ij}\supset
(C_4\times\{0\})+(\{0\}\times C_6)
\]

型の witness が作れる。

### 止める条件

単に total missing が少ない voltage assignment しか見つからず、prefix/suffix の直積被覆証明に落ちない。

---

## 次に集中すべきタスク

次の作業は、探索ではなく証明書設計です。

1. 6 頂点 4-正則 multibase の中から、全 ordered pair で \(4+6\) split count を満たす base を固定する。
2. 各 ordered pair \((i,j)\) について、候補中間点 \(t\) を選ぶ。
3. prefix path family が \(C_4\) factor を覆うように \(C_4\)-voltage を置く。
4. suffix path family が \(C_6\) factor を覆うように \(C_6\)-voltageを置く。
5. その証明書が全 ordered pair で成立するか検証する。

これが通れば、

\[
\boxed{
N(16,5)\ge147456
}
\]

の新しい一般化候補になります。

現時点で、数学的な勝算が見える次のアイデアはこれだけです。これが失敗して、かつ別の決定的被覆原理が出ないなら、一般化探索は一度停止するのが妥当だと思います。

---

## Turn 215 (Round 050) — 🧑 USER

_2026-05-27 03:09:59 UTC_

つづきお願いします。

---

## Turn 216 (Round 050) — 🤖 ASSISTANT

_2026-05-27 03:10:33 UTC_  ·  model: `gpt-5-5-pro`

方針は前回の CRT-block / complementary-subgroup controller に絞り、missing 減少探索ではなく、まず \(C_4\times C_6\) の直積被覆証明が成立しうるか検査します。

---

## Turn 217 (Round 050) — 🤖 ASSISTANT

_2026-05-27 03:14:00 UTC_  ·  model: `gpt-5-5-pro`

まず 6 頂点 4-正則 multibase を列挙し、\(2+3\) / \(3+2\) で必要な \(4+6\) path-count 条件を満たす候補が存在することは確認しました。次は count ではなく、結合時の nonbacktracking 条件込みで実際に sumset 証明書へ落ちるかを判定します。

---

## Turn 218 (Round 050) — 🤖 ASSISTANT

_2026-05-27 03:25:53 UTC_  ·  model: `gpt-5-5-pro`

進めました。今回は大きな進展です。

前回検討した **CRT-block / complementary-subgroup controller** の方向で、完全な prefix/suffix 証明そのものではなく、より直接的に

\[
C_4\times C_6
\]

上の voltage coverage が通る controller が見つかりました。

成果物はこちらです。

[phase34_crt_block_verified.zip](sandbox:/mnt/data/phase34_crt_block_verified.zip)

## 結果

新しい route-chart 候補として、

\[
\boxed{
\Delta=16,\qquad \operatorname{diam}\le5,\qquad |V|=147,456
}
\]

の単純無向グラフの構成証明書が得られました。

これまで完成していた \((16,5)\) 候補は

\[
135,168
\]

頂点だったので、そこからさらに

\[
147,456-135,168=12,288
\]

増えました。

会話内で使ってきた作業基準

\[
N(16,5)\ge132,496
\]

に対しては、

\[
147,456-132,496=14,960
\]

の更新候補です。

## 構成の概要

controller は、6 頂点 4-正則 loopless multigraph に

\[
C_4\times C_6
\]

の voltage を置いて作ります。

controller の頂点数は

\[
6\cdot |C_4\times C_6|
=
6\cdot24
=
144.
\]

この controller と、以前完成済みの

\[
\mathbb F_4^5
\]

universal route-chart を合成します。

したがって最終グラフの頂点数は

\[
144\cdot4^5
=
144\cdot1024
=
147,456.
\]

次数は、controller が 4-正則で、各 controller edge が \(\mathbb F_4\) の 4 通りの fiber control を持つので、

\[
4\cdot4=16.
\]

## controller 証明書

base multigraph の edge と voltage は次です。

| edge | \(u\) | \(v\) | \(C_4\) | \(C_6\) |
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

検証内容は：

\[
\boxed{
\text{任意の ordered base pair }(i,j)
\text{ について、exact NB length }5
\text{ path の voltage sums が }C_4\times C_6\text{ 全体を覆う。}
}
\]

これにより、lift 後の 144 頂点 controller では、任意の ordered controller pair が exact nonbacktracking length 5 route で結ばれます。

## fiber chart 側

fiber 側は既存の成功部品を使っています。

\[
\mathbb F_4^5
\]

上で、記号

\[
a,a^{-1},b,b^{-1}
\]

に対応する affine control data

\[
(A_s,b_s)
\]

を置き、任意の reduced word

\[
s_1s_2s_3s_4s_5
\]

に対して controllability matrix が正則になることを確認しています。

つまり、controller 上に長さ 5 の reduced route が 1 本あれば、その route だけで fiber の

\[
4^5=1024
\]

個の target をすべて一意に routing できます。

## 検証結果

同梱の `verify_candidate.py` の出力は：

```text
Base voltage coverage over C4 x C6: OK
Controller: OK; 144 vertices, simple 4-regular, exact labeled NB length-5 coverage
GF(4)^5 universal chart: OK; 324 reduced words checked, min rank 5; inverse-symbol data verified
Certificate complete: degree 16, diameter <=5, vertices = 144*4^5 = 147456
```

さらに edge list も生成し、単純性と次数を確認しました。

```text
Wrote final_graph_edges.tsv.gz: 147456 vertices, 1179648 edges, all degrees 16.
```

辺数も

\[
147,456\cdot16/2
=
1,179,648
\]

と一致します。

## 重要な注意

今回の発見は、前回考えた「prefix が \(C_4\)、suffix が \(C_6\) を覆う」というきれいな complementary-subgroup 証明そのものではありません。

ただし、その CRT-block 方針から出た

\[
C_4\times C_6
\]

controller で、より直接的な voltage coverage certificate が通りました。つまり、証明は

\[
\text{prefix/suffix subgroup coverage}
\]

ではなく、

\[
\text{exact length-5 path voltage sums が }C_4\times C_6\text{ 全体を覆う}
\]

という形です。

このため、数学的な見通しから始まった枝が、最終的には完全検証可能な explicit certificate に着地した、という位置づけです。

## zip 内の主なファイル

- `controller_c4xc6_multibase.txt`  
  6 頂点 base multigraph と \(C_4\times C_6\) voltage。

- `gf4_s5_universal.txt`  
  \(\mathbb F_4^5\) universal chart data。

- `verify_candidate.py`  
  controller coverage、2-factor labelling、fiber controllability を検証。

- `generate_final_graph.py`  
  最終グラフの edge list を生成。

- `final_graph_edges.tsv.gz`  
  147,456 頂点、1,179,648 辺の圧縮 edge list。

公開記録として主張する前には、最新版の表との照合と第三者検証が必要ですが、構成証明書としてはかなり強い状態まで来ました。

---

## Turn 219 (Round 051) — 🧑 USER

_2026-05-27 03:29:30 UTC_

ありがとうございます。
ここまでの結果をmdにまとめてください。

---

## Turn 220 (Round 051) — 🤖 ASSISTANT

_2026-05-27 03:30:15 UTC_  ·  model: `gpt-5-5-pro`

ここまでの完成候補と未完成枝を、別セッションで引き継げる Markdown に整理します。特に最新の \(C_4\times C_6\) 改良版を主結果として反映します。

---

## Turn 221 (Round 051) — 🤖 ASSISTANT

_2026-05-27 03:33:44 UTC_  ·  model: `gpt-5-5-pro`

旧候補や一般化、未完成枝に加えて、証明構造と次の優先事項も分けて整理します。

---

## Turn 222 (Round 051) — 🤖 ASSISTANT

_2026-05-27 03:40:07 UTC_  ·  model: `gpt-5-5-pro`

まとめました。最新の \(C_4\times C_6\) controller による \((16,5)\) 147,456 頂点候補、既存の \((12,5)\) 候補、可制御チャート・リフトの証明、未完成枝、破棄した方針、次セッションでの優先タスクまで入れています。

[最新まとめ Markdown](sandbox:/mnt/data/route_chart_latest_results_summary.md)

特に重要な証明書 zip も再掲します。

[最新 \((16,5)\) 147,456 頂点候補 zip](sandbox:/mnt/data/phase34_crt_block_verified.zip)

[旧 \((16,5)\) 135,168 頂点候補 zip](sandbox:/mnt/data/phase25_verified_controllable_chart_candidate.zip)

[\((12,5)\) 32,076 頂点候補 zip](sandbox:/mnt/data/phase26_gf3_generalization.zip)

---

## Turn 223 (Round 052) — 🧑 USER

_2026-05-27 04:45:48 UTC_

一般化を試みてください

---

## Turn 224 (Round 052) — 🤖 ASSISTANT

_2026-05-27 04:46:24 UTC_  ·  model: `gpt-5-5-pro`

直近の \(C_4\times C_6\) 成功例を抽象化し、route-chart 証明が保てる一般化だけに絞って進めます。単なるサイズ変更や群変更ではなく、coverage の根拠が先に見える枝だけを試します。

---

## Turn 225 (Round 052) — 🤖 ASSISTANT

_2026-05-27 04:50:38 UTC_  ·  model: `gpt-5-5-pro`

まず安全な一般化として、144頂点 controller を既存の \(\mathbb F_3^5\) chart に差し替え、\((12,5)\) 側の更新を検証しています。並行して、直積因子や追加 parity による controller 拡張のうち、path-count と coverage 根拠が残る候補だけを見ます。

---

## Turn 226 (Round 052) — 🤖 ASSISTANT

_2026-05-27 05:00:11 UTC_  ·  model: `gpt-5-5-pro`

続けました。今回は **追加で完成証明つきの一般化が 1 つ出ました**。

成果物はこちらです。

[phase35_c4xc6_gf3_verified.zip](sandbox:/mnt/data/phase35_c4xc6_gf3_verified.zip)

## 新しい完成候補：\((d,k)=(12,5)\)

前回の最新成果は、

\[
C_4\times C_6
\]

controller と \(\mathbb F_4^5\) chart を合成して、

\[
\Delta=16,\quad D\le5,\quad |V|=147,456
\]

を得るものでした。

今回は、**同じ 144 頂点 controller** を使い、fiber chart だけを

\[
\mathbb F_4^5
\]

から

\[
\mathbb F_3^5
\]

へ差し替えました。

結果として、

\[
\boxed{
\Delta=12,\qquad \operatorname{diam}\le5,\qquad |V|=34,992
}
\]

の単純無向グラフの構成証明書が得られました。

このセッション内で使ってきた作業基準では、前の \((12,5)\) 完成候補は

\[
32,076
\]

頂点だったので、今回の候補はそこから

\[
34,992-32,076=2,916
\]

頂点の改善です。

## なぜすぐ一般化できたか

route-chart lift の構成は、controller と fiber chart がかなり独立です。

controller 側で必要なのは、

\[
\text{任意の ordered controller pair が exact NB length }5
\text{ route で結ばれる}
\]

ことです。

前回完成した \(C_4\times C_6\) controller は、144 頂点 4-正則で、この条件を満たしています。

一方、fiber 側では、任意の reduced word

\[
s_1s_2s_3s_4s_5
\]

に対して、対応する controllability matrix が full rank になる chart が必要です。

以前の一般化で、

\[
\mathbb F_3^5
\]

上の 4-symbol universal chart はすでに完成していました。したがって、前回の 144 頂点 controller とそのまま合成できます。

## 構成

最終グラフは

\[
V(G)=V(C)\times\mathbb F_3^5
\]

です。

controller は

\[
|V(C)|=144
\]

なので、頂点数は

\[
144\cdot3^5=144\cdot243=34,992.
\]

controller は 4-正則で、各 controller edge に対して \(\mathbb F_3\) の 3 通りの fiber control を持たせるので、次数は

\[
4\cdot3=12.
\]

直径は、controller route と fiber chart の組み合わせにより

\[
\operatorname{diam}(G)\le5
\]

です。

## 検証結果

同梱の `verify_candidate.py` の出力は：

```text
Base voltage coverage over C4 x C6: OK
Controller: OK; 144 vertices, simple 4-regular, exact labeled NB length-5 coverage
GF(3)^5 universal chart: OK; 324 reduced words checked, min rank 5; inverse-symbol data verified
Certificate complete: degree 12, diameter <=5, vertices = 144*3^5 = 34992
```

さらに edge list も生成し、単純性と次数を確認しました。

```text
Wrote final_graph_edges.tsv.gz: 34992 vertices, 209952 edges, all degrees 12.
```

辺数も

\[
34,992\cdot 12/2=209,952
\]

と一致しています。

## 現時点の完成済み候補

今回の追加により、route-chart 系の完成済み候補は次のようになりました。

\[
\boxed{
N(16,5)\ge147,456
}
\]

\[
\boxed{
N(12,5)\ge34,992
}
\]

いずれも、公開記録として主張する前には最新版の外部表との照合と第三者検証が必要です。ただし、構成証明書・検証スクリプト・edge list は揃っています。

## 今回試したが未完成の方向

同じ 144 頂点 controller をさらに length 6 用へ拡張するため、

\[
(C_4\times C_6)\times C_4
\]

のような追加 voltage 座標も軽く検査しました。これは \((16,6)\) への大型化を狙うものですが、現時点では coverage がかなり遠く、完成候補にはなっていません。

今のところ、数学的に安全に主張できる新しい一般化は、今回の

\[
\boxed{
(12,5,34,992)
}
\]

です。

---
