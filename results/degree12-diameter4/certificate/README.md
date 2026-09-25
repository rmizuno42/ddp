# N(12,4) >= 5,832：構成・証明・再現用ファイル

次数12、直径4、5,832頂点、34,992辺の無向単純グラフです。
2026-09-24 に参照した Comellas の (12,4) 掲載値5,184を648頂点上回ります。

## 検証

Python 3 の標準ライブラリだけで、小さな数学的証明書を検証し、辺ファイルを再生成できます。

```sh
python verify_certificate.py --write-edges
```

これは行列の逆整合性、100本の full-rank word、12組の projective pencil、同一 fiber の18平面被覆、controller の全72^2 ordered pairs を検証します。成功時には `small_certificate.json` を生成し、再生成した辺ファイルの SHA-256 も照合します。

グラフ全体の直径は、別実装の C++17 プログラムで検証できます。

```sh
g++ -O3 -std=c++17 verify_bfs.cpp -o verify_bfs
./verify_bfs graph_12_4_5832.edges > bfs_certificate_cpp.json
```

これは全5,832始点から BFS を実行し、全34,012,224 ordered pairs の距離分布まで照合します。外部ライブラリ・ネットワーク接続は不要です。

## ファイル

`proof_ja.md` が一般化定理・pencil補題・明示的構成・直径証明です。
`construction.json` が行列、制御ベクトル、16本の base-edge orbit の完全な構成データです。
`graph_12_4_5832.edges` は1行1辺、0-based、ヘッダーなしの辺リストです。
`small_certificate.json` と2つの `bfs_certificate_*.json` は実行済みの検証結果です。
`controller_routes.json` は8つの循環対称性代表始点からの具体的な route 証人です。
`pencil_routes.json` は各長さ2の reduced word に対する4枚の超平面の route 証人です。
`SHA256SUMS` はファイルのチェックサムです。

Python/Numba BFS と C++ BFS は、別々の実装で同じ全距離分布を確認しました。
これは独立した実装による検証であり、独立した第三者による検証や査読を受けたという意味ではありません。
Comellas 氏への送信・表への掲載申請は実施していません。

## 比較対象

https://web.mat.upc.edu/francesc.comellas/delta-d/table_degree_diameter.html

表の値は参照日のスナップショットです。無関係な未調査文献に対する優先権までは、このファイル群では主張しません。
