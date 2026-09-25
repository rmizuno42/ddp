# (14,5) の下界 88,452 — 再検証パッケージ

**結果：88,452頂点、618,786辺、最大次数14、直径5。**

次数分布は13が756頂点、14が87,696頂点です。正則ではありません。比較：2026年9月25日閲覧のComellas表61,887、本セッション前回66,430。

## 最小の再検証

Python標準ライブラリだけで十分条件の全有限証明書を検査します。

```bash
python verify_small.py
```

この検証は、大きい辺ファイル、探索ログ、SciPy、有限幾何の名称を信用しません。`construction.json` に記載した有限データから、逆整合性・全324語のrank・controllerの全対・短いrouteの補修を直接確認します。

## 全辺の再生成

```bash
python build_graph.py --output regenerated.edges
```

別に実装したC++生成器：

```bash
g++ -O3 -std=c++17 regenerate.cpp -o regenerate
./regenerate parameters.txt regenerated_cpp.edges
```

両者は同じ辺ファイルを生成します。SHA-256：
`ae192f45dc5cfb5a44530f520fe258610ff5a46e720e2cb739cca9fbc929b39a`

## 最終辺リストの直接検査

```bash
g++ -O3 -std=c++17 -fopenmp verify_bfs.cpp -o verify_bfs
OMP_NUM_THREADS=2 ./verify_bfs graph_d14_D5_n88452.edges

g++ -O3 -std=c++17 -fopenmp verify_bitset.cpp -o verify_bitset
OMP_NUM_THREADS=2 ./verify_bitset graph_d14_D5_n88452.edges 5
```

bitset検査は約2 GBの主要配列を使います。両コードは全始点・全頂点対を扱います。保存された検証結果は `bfs_certificate.json`, `bitset_certificate.json` です。

## データの形式

- `construction.json`：controller・四つの行列・四つの制御ベクトル・364個の平行移動方向。全係数は整数 mod 3。
- `controller.adj`：364行、各行にラベル0,1,2,3の行き先。行の先頭に始点番号はありません。
- `parameters.txt`：C++生成器用の同じデータ。364、controller364行、行列20行、制御ベクトル4行、平行移動方向364個の順。
- `graph_d14_D5_n88452.edges`：先頭行は `88452 618786`、以降は0-basedの無向辺を一回ずつ。番号は `243*u+x0+3*x1+9*x2+27*x3+81*x4`。
- `triple_route_witnesses.json`：13,104個の三歩routeについて、平行移動を挿入する二箇所。
- `PROOF_ja.md`：定義、補題、計算証明の範囲。

## 有限幾何との対応（任意）

```bash
python check_geometry.py
```

ここだけNumPyが必要です。保存された728頂点の接続グラフの二部性・次数・girth・直径、極性の自己同型性と位数2、商とcontrollerの一致を検証します。

`geometry/build_hexagon.py` と `lie_data.npz` は本セッションで以前使用した座標生成器です。主証明は保存された364状態の整数データの検査だけで成立し、座標生成器を信頼する必要はありません。

## 探索の再実験

探索のやり直しは証明の検証には不要です。`search/README_ja.md` を参照してください。探索スクリプトは非存在や最適性を証明するものではありません。

第三者検証・文献上の優先権の確定・表への掲載申請は未実施です。
