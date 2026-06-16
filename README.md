# New lower bounds for the degree/diameter problem via interaction with a browser-accessible LLM

This repository accompanies the paper *"New lower bounds for the degree/diameter problem via interaction with a browser-accessible LLM"*.

📄 **[Download the paper (PDF)](https://github.com/rmizuno42/ddp/releases/latest/download/paper.pdf)** · 📚 **[arXiv:2606.15860](https://arxiv.org/abs/2606.15860)**

## Overview

Let $N(\Delta, D)$ be the maximum number of vertices in a simple undirected connected graph with maximum degree at most $\Delta$ and diameter at most $D$ — the **degree/diameter problem**. This paper gives explicit graph constructions establishing two new lower bounds for diameter $5$:

$$N(12,5) \ge 34{,}992, \qquad N(16,5) \ge 147{,}456,$$

improving the previously recorded lower bounds of $29{,}621$ and $132{,}496$.

The construction was discovered through a long dialogue with ChatGPT via its standard web interface, **without any external orchestration layer** — no custom agent framework, automated evaluator-driven search loop, problem-specific search engine, or formal proof assistant was set up in advance. The motivating question is how far mathematical search and discovery can proceed using only an LLM available through a standard browser.

The paper makes two contributions that can be read independently:

1. **Improved mathematical lower bounds.** Explicit simple-graph constructions and finite certificates for $N(12,5)$ and $N(16,5)$ (Appendix A). Their correctness can be verified from the construction alone, independently of how they were discovered.
2. **A record and analysis of the discovery process.** A description of the roughly six-day dialogue — including unsuccessful intervals — and of the author's meta-level interventions near the junctures at which the search moved toward abstraction and finite-certificate design, based on the visible transcript.

## The paper

- **[paper.pdf](https://github.com/rmizuno42/ddp/releases/latest/download/paper.pdf)** — the compiled paper, attached to the latest [GitHub Release](https://github.com/rmizuno42/ddp/releases/latest). Also available on [arXiv](https://arxiv.org/abs/2606.15860).
- **[paper.tex](paper.tex)** — LaTeX source. It compiles with [Tectonic](https://tectonic-typesetting.github.io/) in one command:

  ```bash
  tectonic paper.tex
  ```

  The bibliography source is `references.bib`; the compiled `paper.bbl` is also included (as submitted to arXiv) so the source builds without a separate BibTeX run.

## Other materials

Everything else in this repository — the visible ChatGPT transcript and the script that produces it, the construction packages (the provenance package and a cleaned, runnable version), and the independent verification scripts — is **described in the paper**. See **Appendix B, "Structure of the supplementary materials,"** and the verification and reproducibility notes in §A.8.

## Citation

```bibtex
@misc{Mizuno2026DegreeDiameter,
  title         = {New lower bounds for the degree/diameter problem via interaction with a browser-accessible LLM},
  author        = {Ryosuke Mizuno},
  year          = {2026},
  eprint        = {2606.15860},
  archivePrefix = {arXiv},
  primaryClass  = {math.GM},
  url           = {https://arxiv.org/abs/2606.15860},
}
```
