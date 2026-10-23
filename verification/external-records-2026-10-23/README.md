# Subsequent records based on repository graphs — 2026-10-23

The [Comellas table](https://web.mat.upc.edu/francesc.comellas/delta-d/table_degree_diameter.html),
last changed on 2026-10-22 and accessed on 2026-10-23, lists larger graphs for
(14,5) and (15,5). Its detail page explicitly attributes both to modifications
of the corresponding Mizuno graphs in this repository.

| Parameters | Repository order | Published record | Increase |
|---|---:|---|---:|
| (14,5) | 88,452 | [SamSar_94186: 94,186](https://web.mat.upc.edu/francesc.comellas/delta-d/desc_g/desc_g5.html#145) | 5,734 |
| (15,5) | 100,000 | [SamSar_100132: 100,132](https://web.mat.upc.edu/francesc.comellas/delta-d/desc_g/desc_g5.html#155) | 132 |

Both entries name Sami Hani Badaoui and Sarah Ellen Mary Vaughan and give
2026-10-22 as the communication date. Each is followed by the corresponding
former Mizuno entry, a link to its repository folder, and a downloadable copy
of its edge list. The two GitHub links point to the correct folders even
though their visible labels both say `degree16-diameter3`.

## What the edge files establish

The former graphs downloaded from the detail page have exactly the same
vertex labels and undirected edge sets as the repository's (14,5) and (15,5)
graphs. Their file hashes differ because of the header formatting; normalizing
the header and sorting the edges reproduces the repository edge-file hashes.
Thus the graphs referred to in the published attribution are unambiguous.

The two new edge lists also pass checks for their declared orders, edge
counts, absence of loops and duplicate edges, and maximum degrees:

| Graph | Vertices | Edges | Degree distribution |
|---|---:|---:|---|
| SamSar_94186 | 94,186 | 657,452 | 15 of degree 12; 3,670 of degree 13; 90,501 of degree 14 |
| SamSar_100132 | 100,132 | 749,732 | 18 of degree 13; 2,480 of degree 14; 97,634 of degree 15 |

The conclusion that they were constructed from the repository graphs rests
on the detail page's explicit attribution. This check does not reconstruct
the vertex correspondence or the sequence of graph modifications. Equal
integer labels in two different files do not establish a correspondence:
their literal edge intersections have only 111 and 113 edges, respectively.
Those counts cannot measure how many edges were retained after relabeling.
In particular, no claim is made that either new graph contains its predecessor
as an unchanged subgraph.

Diameter 5 is reported by the published table. The checks here do not rerun
all-pairs distances for these external graphs. They remain external records;
the eight graphs and their existing verification reports in this repository
are unchanged.

## Reproduce

From the repository root, using Python 3 and its standard library:

```bash
python3 verification/external-records-2026-10-23/compare_edges.py --output /tmp/ddp-external-comparison.json
```

The script downloads the four linked edge files, requires their saved SHA-256
hashes, and performs the comparisons above. To use existing downloads, pass
`--input-dir` with the directory containing the four filenames recorded in
the URLs. No downloaded code is executed.

- [Comparison report, file URLs, and hashes](comparison.json).
- [Comparison program](compare_edges.py).
- [Dated table snapshot and incoming repository links](../table-snapshot-2026-10-23.json).
- [Repository overview](../../README.md).
