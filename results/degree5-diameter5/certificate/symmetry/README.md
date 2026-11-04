# Full automorphism groups

The saved reports were computed from edge lists using nauty 2.9.3.
The main graph has full automorphism-group order 60. The base graph has
order 60, while the September regular completion has order 12.
The [matrix verifier](../verify.py) independently checks all 60 explicit
automorphisms of the main graph and that the saved nauty generators
generate exactly that group. The upper bound on the full group order
comes from nauty's exhaustive computation.

| Graph | Full group order | Report |
|---|---:|---|
| Main graph | 60 | [nauty.json](nauty.json) |
| Base graph | 60 | [algebraic-nauty.json](algebraic-nauty.json) |
| September regular graph | 12 | [september-regular-nauty.json](september-regular-nauty.json) |

To recompute the main report, install nauty separately and compile the
repository's [exporter](../../../../verification/automorphisms.cpp).
For a Homebrew installation, run from the repository root:

    c++ -O3 -std=c++17 -I"$(brew --prefix)/include" \
      verification/automorphisms.cpp -L"$(brew --prefix)/lib" -lnauty \
      -o /tmp/ddp-automorphisms
    /tmp/ddp-automorphisms results/degree5-diameter5/certificate/graph.edges /tmp/ddp-660-nauty.json

For other installations, adjust the include and library paths. Use
the algebraic edge list to check the base graph. The September
regular edge list is in the preserved source archive; change its first
line from 660 to the two integers 660 and 1650 before passing it to the exporter.
The [run metadata](run.json) records hashes of the input files and exporter.

nauty is needed only to recompute the full group, not to verify the
order, degree, diameter, or construction.
