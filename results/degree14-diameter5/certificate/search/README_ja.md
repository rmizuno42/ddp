# 探索資料

成功した方向配置は `../construction.json` に保存済みです。全探索を再実行しなくても `../verify_small.py` で検証できます。

## 状態ごとの平行移動方向の探索

```bash
g++ -O3 -std=c++17 local_translation.cpp -o local_translation
./local_translation chartH3_universal.txt ../controller.adj trial 621 16 150 80
```

引数は、係数ファイル、controller、出力prefix、seed、初期の共通方向の符号（0ならランダム）、時間上限（秒）、annealing温度の上限です。今回保存した解はseed621、提案55,258回目、十分条件の未到達点数0です。標準ライブラリやCPUによる乱数分布・時間制限の違いにより、探索の経過そのものが一致することは保証しません。

`chart4_invol.cpp` は四つの自己逆行列、あるいは一逆元対＋二自己逆行列の探索です。行列の候補生成も今回の研究の一部ですが、証明には選択済みの係数の有限検査だけを使います。

`find_H3_polarity.py` は3元体のSL(3)作用と保存された双対性から極性を探したコード、`colour_H3_full.py` は半ループを残すcontrollerの4色化をSciPy MILPで求めたコードです。再実行時にはパッケージのルートに `candidates` と `certificates` の作業ディレクトリを作ってください。4色化の解は一意ではないため、保存された色付け `../controller.adj` を使うことが再検証の最短手順です。

探索で採用したのは「全ての短いrouteを指定した族で補修する」という十分条件です。探索が失敗しても、別のroute族や別のグラフの非存在を意味しません。
