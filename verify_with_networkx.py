#!/usr/bin/env python3
"""
edge list の order / degree / diameter を NetworkX で独立検証する.

使い方:
    python3 verify_with_networkx.py <edge_file.tsv.gz> <n> <d> [<k>]

例:
    python3 verify_with_networkx.py final_graph_edges.tsv.gz 34992 12
    python3 verify_with_networkx.py final_graph_edges.tsv.gz 147456 16

引数:
    edge_file : 検証する辺リスト (gzip 圧縮 TSV). 先頭行は "n m", 以降は "u<TAB>v".
    n         : 主張する頂点数
    d         : 主張する次数 Δ
    k         : 主張する直径上界 (省略時 5)

検証項目 (どれか1つでも違反すると AssertionError で停止):
    1. self-loop なし                        (file 内の各行で u != v)
    2. ファイル内の辺数 == header の m
    3. 重複辺なし                            (nx.Graph の dedup 個数を比較)
    4. order (G.number_of_nodes()) == n
    5. 全頂点で次数 == d  (= Δ-正則)
    6. 2 * m == n * d   (handshake)
    7. diameter (nx.diameter) <= k
"""

import sys
import gzip
import networkx as nx


def main():
    if len(sys.argv) < 4:
        sys.exit(__doc__)

    edge_file = sys.argv[1]
    n_expected = int(sys.argv[2])
    d_expected = int(sys.argv[3])
    k_expected = int(sys.argv[4]) if len(sys.argv) >= 5 else 5

    # ---- 1. ファイル読み込み ----
    print(f'読込: {edge_file}')
    edges = []
    with gzip.open(edge_file, 'rt') as f:
        n_hdr, m_hdr = map(int, f.readline().split())
        print(f'  ヘッダ: n={n_hdr}, m={m_hdr}')
        for line in f:
            u_str, v_str = line.split('\t')
            u, v = int(u_str), int(v_str)
            assert u != v, f'self-loop at vertex {u}'
            edges.append((u, v))

    assert len(edges) == m_hdr, (
        f'ファイル内辺数 {len(edges)} != header m={m_hdr}'
    )

    # ---- 2. NetworkX グラフ構築 ----
    # range(n_expected) を先に追加して、孤立頂点も含める.
    G = nx.Graph()
    G.add_nodes_from(range(n_expected))
    G.add_edges_from(edges)

    # ---- 3. 重複辺なし (nx.Graph は重複を黙って捨てるので, 個数比較で検出) ----
    assert G.number_of_edges() == len(edges), (
        f'重複辺: file={len(edges)} 件, graph={G.number_of_edges()} 件'
    )

    # ---- 4. order ----
    assert G.number_of_nodes() == n_expected, (
        f'order = {G.number_of_nodes()} != {n_expected}'
    )

    # ---- 5. 次数: Δ-正則 ----
    degs = [deg for _, deg in G.degree()]
    assert min(degs) == max(degs) == d_expected, (
        f'degree range [{min(degs)}, {max(degs)}] != {d_expected}'
    )

    # ---- 6. handshake ----
    assert 2 * G.number_of_edges() == G.number_of_nodes() * d_expected

    print(f'  order      = {G.number_of_nodes()}')
    print(f'  edges      = {G.number_of_edges()}')
    print(f'  degree     = {d_expected} (regular)')
    print(f'  simple     = yes (no self-loops, no duplicate edges)')

    # ---- 7. diameter ----
    # nx.diameter は内部で全頂点 BFS を行う.
    # usebounds=True で Crescenzi et al. の extrema-bounding 法を使う高速版になる.
    # どちらでも返り値は EXACT な diameter (近似ではない).
    # 規則的グラフでは usebounds=True が数十倍速いため既定でこちらを使う.
    print(f'  diameter 計算中 (nx.diameter, usebounds=True) ...')
    diam = nx.diameter(G, usebounds=True)
    assert diam <= k_expected, f'diameter = {diam} > {k_expected}'

    print(f'  diameter   = {diam} (<= {k_expected})')
    print()
    print('PASS')


if __name__ == '__main__':
    main()
