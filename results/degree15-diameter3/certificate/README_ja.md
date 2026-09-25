# 次数15・直径3・1,458頂点：再現可能な証明書

## 結果

無向単純15正則、1458頂点、10935辺、直径3。2026年9月25日閲覧のComellas表の1224を234頂点（約19.12%）上回る。第三者検証・掲載申請・文献上の優先権確認は未実施。

## 最小検証（Python標準ライブラリのみ）

```bash
python verify.py
python verify_uniform.py
```

`verify.py` は構成JSONから全逆辺、全270 pencil、全4320 non-backtracking三歩route、全2916 controller pairsを検査する。次に全辺を生成し、全1458始点で三歩以内の到達を確認する。`regenerated.edges` と `verification.json`、`route_certificate.json` を書き出す。

`verify_uniform.py` は80語のrankが全54始点で一様であることと、群単位元での54語の圧縮証明書を確認する。

```bash
cmp regenerated.edges graph_d15_D3_n1458.edges
```

## 別の生成器・通常BFS（C++17）

```bash
g++ -O3 -std=c++17 regenerate.cpp -o regenerate_cpp
./regenerate_cpp regenerated_cpp.edges
cmp regenerated_cpp.edges graph_d15_D3_n1458.edges

g++ -O3 -std=c++17 verify_bfs.cpp -o verify_bfs
./verify_bfs graph_d15_D3_n1458.edges
```

C++生成器はJSONやPythonの生成ロジックを使わず、三種類の前向き辺の公式から生成する。C++検証器は最終辺リストしか読まず、通常のqueue BFSを全始点で行う。最適化ソルバー、NumPy、NetworkX等は不要。

## ファイル

- `PROOF_ja.md`：自己完結した構成と証明。
- `construction.json`：群、五生成元、三行列、番号付け。
- `graph_d15_D3_n1458.edges`：ヘッダー `1458 10935`、以後0-based無向辺、各辺一回、辞書順。
- `verify.py`、`verify_uniform.py`：代数・有限集合・全始点検証。
- `regenerate.cpp`：別方式の全辺生成器。
- `verify_bfs.cpp`：queue BFS全始点検証。
- `route_certificate.json`：2916 controller pairsの証明route。
- `uniform_word_certificate.json`：全始点に適用できる54語の圧縮証明書。
- `verification.json`、`bfs_certificate.json`：一致した距離分布。
- `regeneration_cpp.json`、`reproduction_checks.json`：生成・再現検査。
- `sources.json`：比較資料と閲覧日。
- `SHA256SUMS`：配布ファイルのチェックサム。

体は整数mod 3。群座標はmod 6とmod 9であり、fiberの演算と混同しないこと。

距離分布（ordered pairs）：[1458, 21870, 274104, 1828332]。

グラフファイルのSHA-256：
`85182ecb372ce24b3fdc1912ca0c14a6cec5353400ef3a6f4bd94b4520113546`
