# N(15,5) ≥ 100,000：再検証用パッケージ

新しい結果は `PROOF_ja.md`。辺ファイルは `graph_d15_D5_n100000.edges`。
15正則・100,000頂点・750,000辺・直径5の無向単純グラフである。

## 最小検証（Python標準ライブラリのみ）

```bash
python verify_small.py
python verify_independent.py
```

第一の実装はrankとprojective pencilを検査する。第二の実装はLeibniz公式の行列式と到達点集合の直接生成を用いる。ともに、全1024 controller pairsを検査する。巨大グラフの全頂点対探索は必要ない。

## 辺の再生成（Python標準ライブラリのみ）

```bash
python regenerate.py --output regenerated.edges
```

NumPy版は `python build_graph.py`。両者による生成ファイルは完全一致している。

頂点番号は

    u*3125 + x0 + 5*x1 + 25*x2 + 125*x3 + 625*x4

である。先頭行は `100000 750000`。以降は0-basedの無向辺をu<vで一度ずつ、辞書順に記録している。

## 全頂点対の直接検証（C++17 + OpenMP）

```bash
g++ -O3 -std=c++17 -fopenmp verify_bfs.cpp -o verify_bfs
OMP_NUM_THREADS=2 ./verify_bfs graph_d15_D5_n100000.edges

g++ -O3 -std=c++17 -fopenmp verify_bitset.cpp -o verify_bitset
OMP_NUM_THREADS=2 ./verify_bitset graph_d15_D5_n100000.edges 5
```

bitset版は大きなメモリ領域（主要な二つの配列だけで約2.5 GB）を必要とする。メモリに制限がある環境では通常BFSまたは小さな証明書を用いる。

## 主な証明書

- `small_certificate.json`：rankとpencilによる証明書の検査結果。
- `independent_small_certificate.json`：別の有限算術実装による検査結果。
- `route_assignment.json`：配列[u][v]に証明方式とラベル語。
- `pencil_certificate.json`：共通coreと超平面の基底。
- `bfs_certificate.json`、`bitset_certificate.json`：全100億ordered pairsの検査結果。
- `regeneration_certificate.json`：別生成器とのSHA-256一致。
- `verification_summary.json`：整合性照合。
- `sources.json`：比較元と既存研究。

`MANIFEST_SHA256.json` は同封ファイルの整合性確認用。探索用の乱数履歴や探索プログラムは `search/` にあり、証明には不要である。探索の過程には未成立候補も含まれるため、完成グラフと混同しないこと。

第三者検証・表への掲載・最適性は未主張。比較する掲載値は今回確認したComellas主表の82,684である。
