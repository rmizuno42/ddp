# Verification procedure

This is a **clean, runnable** copy of the route-chart construction package.
It contains the same graphs and the same construction data as
`route_chart_verified_graphs_package/` (kept elsewhere as the original, unedited
provenance record). The scripts have been cleaned up so that a verifier can run
them in sequence without hitting environment-specific paths or errors, and the
construction data for each parameter set is provided here as a single unified
machine-readable certificate, `certificates/<param>/certificate.json`.

The two constructed graphs are simple undirected graphs:

| params   |   \|V\| | degree Δ | diameter | edge list                                     |
| -------- | ------: | -------: | -------: | --------------------------------------------- |
| `(12,5)` |  34,992 |       12 |      ≤ 5 | `graphs/12_5_34992/final_graph_edges.tsv.gz`  |
| `(16,5)` | 147,456 |       16 |      ≤ 5 | `graphs/16_5_147456/final_graph_edges.tsv.gz` |

The edge lists are gzip-compressed TSV: line 1 is the header `n m`, and every
following line is one undirected edge `u<TAB>v` with `0 ≤ u,v < n`.


## Requirements

- **Python 3.7+** (standard library only) for the certificate scripts
  (`scripts/.../verify_candidate.py`, `scripts/.../generate_final_graph.py`)
  and for `verify_graphs_identical.py`.
- **igraph** — `pip install python-igraph` — for the independent order/degree/diameter check in Step 3.

The scripts `verify_with_igraph.py`, 
`verify_graphs_identical.py`, and `verify_provenance_equivalence.py` live **one
directory above this package** (alongside it in the paper's supplementary
material). The commands below assume
you run them from this package's root directory, so they are referenced as
`../verify_with_igraph.py`, etc. Adjust the path if you placed them elsewhere.


## Procedure

Run everything from this package's root directory:

```bash
cd route_chart_clean_package
```

### Step 0 (optional) — Confirm this package matches the provenance package

If you also have `route_chart_verified_graphs_package/`, this check confirms that
the clean package verifies the *same* construction: the certificate data and the
bundled graphs here are equivalent to those in the provenance package. The
certificate comparison is semantic (the formats differ: unified JSON here,
original text files there); the graph comparison is on uncompressed content.

```bash
python3 ../verify_provenance_equivalence.py
```

Expected: each parameter set reports `certificate (semantic): OK` and
`graph content SHA-256 : OK`, ending with `PASS`.

### Step 1 — Verify the construction certificates

`verify_candidate.py` loads the construction data from
`certificates/<param>/certificate.json` and re-checks, from that certificate,
that the controller has the required nonbacktracking-walk coverage and that the
fiber chart has full controllability rank for every length-5 reduced word. (As a
guard against accidental edits, it also asserts that the loaded certificate
matches a reference copy embedded in the script, so the checked construction
cannot change silently.) It prints `OK` lines and writes no files.

```bash
python3 scripts/12_5_34992/verify_candidate.py
python3 scripts/16_5_147456/verify_candidate.py
```

Expected output (each case):

```text
Base voltage coverage over C4 x C6: OK
Controller: OK; 144 vertices, simple 4-regular, exact labeled NB length-5 coverage
GF(3)^5 universal chart: OK; 324 reduced words checked, min rank 5; inverse-symbol data verified
Certificate complete: degree 12, diameter <=5, vertices = 144*3^5 = 34992
```

(The `(16,5)` case prints `GF(4)^5 ... degree 16 ... 144*4^5 = 147456`.)

### Step 2 — Regenerate the edge lists and confirm they match the bundled graphs

`generate_final_graph.py` rebuilds the full edge list from the verified
controller and chart. Each script takes an optional output path (default:
`./final_graph_edges.tsv.gz`); here we write to `/tmp` to avoid clobbering the
bundled files.

```bash
python3 scripts/12_5_34992/generate_final_graph.py  /tmp/gen_12_5.tsv.gz
python3 scripts/16_5_147456/generate_final_graph.py /tmp/gen_16_5.tsv.gz
```

Then confirm the regenerated graphs equal the bundled ones (body SHA-256 plus
parsed vertex/edge-set equality):

```bash
python3 ../verify_graphs_identical.py \
    --package . \
    --gen12 /tmp/gen_12_5.tsv.gz \
    --gen16 /tmp/gen_16_5.tsv.gz
```

Expected: both cases report `IDENTICAL GRAPH` and the script ends with
`ALL GRAPHS IDENTICAL.` (exit code 0). The cleaned generators reproduce the
bundled edge lists with **identical uncompressed content**, so this check
should pass byte-for-byte on the edge body.

### Step 3 — Independently check order, degree, and diameter

This is the graph-theoretic check that does not rely on any of the construction
machinery: it reads the edge list and verifies it is a simple Δ-regular graph on
`n` vertices with diameter ≤ `k`. Arguments: `<edge_file> <n> <d> [<k>]`
(`k` defaults to 5).

```bash
python3 ../verify_with_igraph.py graphs/12_5_34992/final_graph_edges.tsv.gz   34992 12 5
python3 ../verify_with_igraph.py graphs/16_5_147456/final_graph_edges.tsv.gz 147456 16 5
```

Expected output (the script also prints a few progress lines; each case ends with):

```text
  order      = 34992
  edges      = 209952
  degree     = 12 (regular)
  simple     = yes (no self-loops, no duplicate edges)
  diameter   = 5 (<= 5)

PASS
```

You can also run Step 3 on the edge lists you regenerated in Step 2
(`/tmp/gen_12_5.tsv.gz`, `/tmp/gen_16_5.tsv.gz`) — the result is identical.


## What each step establishes

- **Step 0** (if run) ties this package to the provenance record: the
  certificate and graph here describe the same construction the original package
  contains.
- **Step 1** proves the *construction* is sound, working from the certificate:
  the controller routes every ordered vertex pair by an exact length-5
  nonbacktracking walk, and the fiber chart lifts every such walk onto all `q^5`
  fiber targets (full rank). Together these imply diameter ≤ 5 and degree `4q`
  by construction.
- **Step 2** proves the bundled edge list is exactly the graph that construction
  produces (no transcription error between the proof and the data file).
- **Step 3** is a self-contained sanity check on the edge list itself, using a
  standard graph library, independent of how the graph was built.

Passing Steps 1-3 is end-to-end verification: the construction is valid, the
edge file matches the construction, and the edge file really is a simple
Δ-regular graph of diameter ≤ 5.


## Integrity

`SHA256SUMS.txt` lists the SHA-256 of every file in this package. Check with:

```bash
shasum -a 256 -c SHA256SUMS.txt        # or: sha256sum -c SHA256SUMS.txt
```

The `graphs/` files are byte-for-byte copies of the originals in
`route_chart_verified_graphs_package/`. The `certificates/` were reformatted into
a single unified JSON per parameter set, and the `scripts/` were cleaned; both
carry the same construction data as the provenance package, which
`verify_provenance_equivalence.py` (Step 0) checks.


## Layout

```text
route_chart_clean_package/
  VERIFY.md                      # this file
  SHA256SUMS.txt
  graphs/
    12_5_34992/final_graph_edges.tsv.gz
    16_5_147456/final_graph_edges.tsv.gz
  certificates/                  # unified machine-readable construction data
    12_5_34992/certificate.json
    16_5_147456/certificate.json
  scripts/
    12_5_34992/verify_candidate.py
    12_5_34992/generate_final_graph.py
    16_5_147456/verify_candidate.py
    16_5_147456/generate_final_graph.py
```
