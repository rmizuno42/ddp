# 探索の再実行（証明の検査には不要）

```bash
g++ -O3 -std=c++17 chart_search.cpp -o chart_search
./chart_search 1200000 530 recovered_chart 3 3 1 0
g++ -O3 -std=c++17 controller_search.cpp -o controller_search
./controller_search 32 5 30000000 3202 recovered_controller 2 - optimistic_controller.words
```

候補生成の語集合は全12種類の三歩語を含む楽観的条件です。それだけでは直径証明になりません。完成後に実際に有効な八種類だけを使って証明を検査します。今回の保存候補はその検査にも合格しています。

乱数分布や浮動小数点の細部で探索軌道は処理系依存になり得ます。最終行列とcontrollerの証明書を検査する方法は乱数に依存しません。
