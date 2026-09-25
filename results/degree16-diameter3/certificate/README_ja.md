# 次数16・直径3・1,920頂点の構成

**N(16,3) ≥ 1,920。** 無向単純16正則、15,360辺、直径3。
2026年9月25日閲覧時のComellas掲載値1,610に対して+310（約19.25%）。第三者検証・掲載申請は未実施。

## 最小の検証手順

Python標準ライブラリだけで、全代数証明書、全辺再生成、全始点bitset BFSを検査する。

```bash
python verify.py
```

`regenerated.edges` と `verification_run.json` が生成される。保存した辺ファイルとのbyte-for-byte一致も記録する。

別方式の通常BFS（C++17。OpenMPや追加ライブラリ不要）：

```bash
g++ -O3 -std=c++17 verify_bfs.cpp -o verify_bfs
./verify_bfs graph_d16_D3_n1920.edges
```

期待する距離分布：`[1920, 30720, 387840, 3265920]`。未到達始点数0、最小次数=最大次数=16、直径3。

## 内容

- `PROOF_ja.md`：辺依存affine lift、五平面pencil、一辺につき一つの例外turn、直径証明。
- `construction.json`：全30頂点controller、全120向き付き辺行列、全900組のroute証明書。
- `controller.adj`：30行4列。各行の四つの近傍。逆portは(1,0,3,2)。
- `edge_choices.csv`：全60無向辺の例外turnと順方向3×3行列。
- `graph_d16_D3_n1920.edges`：ヘッダー付き0-based無向辺リスト。各辺を一度ずつ記載。
- `verify.py`：ソルバー非依存の検証器・生成器。
- `verify_bfs.cpp`：辺リストだけを読む通常の全始点BFS。
- `verification_run.json`、`bfs_certificate.json`：異なる計算方法による最終検証結果。
- `original_independent_certificate.json`：探索時とは別の点集合検証器の初回結果。
- `search/`：探索に用いたソース、保存controller、実行ログ。以下参照。
- `SHA256SUMS`：同封ファイルのSHA-256。

## 規約

F₄の符号0,1,2,3は0,1,α,α+1を表す。α²+α+1=0。整数mod4ではない。
頂点番号は64u+x₀+4x₁+16x₂。ベクトルは列ベクトル。

`construction.json`内のsolver statusや保存距離分布を信用しなくても、検証コードだけで結果を再計算できる。

## 探索自体の再実行（証明書の検査には不要）

以下にはNumPy、SciPy、NumbaおよびC++17コンパイラが必要。保存した構成を再生成するだけなら不要。

```bash
cd search
mkdir -p candidates logs certificates
g++ -O3 -std=c++17 src/primitive3_graph_search.cpp -o primitive_search
./primitive_search 30 30000000 30086 candidates/replay_c30 6 0 -
python src/label_regular_controller.py replay_c30
python src/edge_local_chart_milp.py replay_c30
cd ..
python verify.py --config search/candidates/replay_c30_edge_local.json --output replay.edges --report replay_verification.json
```

探索はC++標準ライブラリやMILPソルバーの版によって別解になる可能性があり、常に同じ解を返す保証はない。一方、保存済み`construction.json`からの辺生成と検証は決定的である。

## 参照表

Francesc Comellas, “The (Degree, Diameter) Problem for Graphs”.
https://web.mat.upc.edu/francesc.comellas/delta-d/table_degree_diameter.html
2026年9月25日閲覧。頁の最終更新表示は2026年9月24日。

このパッケージはグラフの数学的性質を検証するものであり、優先権・掲載受理を証明するものではない。
