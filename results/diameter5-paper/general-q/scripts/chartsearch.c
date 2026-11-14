/*
 * chartsearch.c -- simulated-annealing search for a universal route chart on
 * GF(q)^5 over the symmetric alphabet S = {a, a^-1, b, b^-1} = {0, 1, 2, 3}.
 *
 * A route chart (arXiv:2606.15860, Definition A.4) assigns A_t in GL_5(q) and
 * b_t in GF(q)^5 to each symbol with A_{t^-1} = A_t^{-1}, b_{t^-1} = A_t^{-1} b_t.
 * It is universal if, for every reduced word w = t1..t5, the controllability
 * matrix M_w = [A_t5..A_t2 b_t1 | A_t5..A_t3 b_t2 | ... | A_t5 b_t4 | b_t5]
 * is nonsingular.  The free data are A_0, A_2, b_0, b_2; the inverse symbols
 * are derived.  The objective is the total rank deficiency over the 324
 * reduced words; the search stops when it reaches 0.
 *
 * Usage: chartsearch TABLEFILE SEED ITERS [T0 T1]
 *   TABLEFILE: text file "q" then the q*q addition table, the q*q
 *   multiplication table, q negatives and q inverses (inv[0] unused),
 *   as written by tables.py.
 * Output: one JSON line {"q":..,"seed":..,"A":[A0,A1,A2,A3],"b":[b0,b1,b2,b3]}
 * on success (exit 0); otherwise a line with the best objective (exit 1).
 */
#include <math.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define N 5
#define MAXQ 1024

static int q;
static uint16_t ADD[MAXQ][MAXQ], MUL[MAXQ][MAXQ];
static int NEG[MAXQ], INV[MAXQ];

static uint64_t rng_state;
static inline uint64_t rng(void) {
    rng_state ^= rng_state >> 12;
    rng_state ^= rng_state << 25;
    rng_state ^= rng_state >> 27;
    return rng_state * 2685821657736338717ULL;
}
static inline double rnd01(void) { return (rng() >> 11) * (1.0 / 9007199254740992.0); }

static const int SINV[4] = {1, 0, 3, 2};

/* reduced sequences, stored as suffixes (t_{j}..t_5); index 0 = empty */
#define MAXSEQ 512
static int nseq;
static int seq_len[MAXSEQ], seq_first[MAXSEQ], seq_rest[MAXSEQ];
static int words[324][N];          /* reduced words of length 5 */
static int word_col[324][N];       /* seq index of (t_j..t_5) for column j */

static int A[4][N][N], B[4][N];
static int S[MAXSEQ][N][N];        /* suffix products A_t5 ... A_t(j)  for seq (t_j..t_5) */
static int V[MAXSEQ][N];           /* column vector for seq (t_j..t_5): S(t_{j+1}..t_5) b_{t_j} */

static int find_seq(int first, int rest) {
    for (int i = 1; i < nseq; i++)
        if (seq_first[i] == first && seq_rest[i] == rest) return i;
    return -1;
}

static void build_sequences(void) {
    nseq = 1;
    seq_len[0] = 0; seq_first[0] = -1; seq_rest[0] = -1;
    int start = 0, end = 1;
    for (int L = 1; L <= N; L++) {
        int newend = nseq;
        for (int r = start; r < end; r++) {
            for (int t = 0; t < 4; t++) {
                if (seq_len[r] > 0 && SINV[t] == seq_first[r]) continue; /* keep reduced */
                seq_len[nseq] = L; seq_first[nseq] = t; seq_rest[nseq] = r;
                nseq++;
                newend = nseq;
            }
        }
        start = end; end = newend;
    }
    /* words of length 5 = sequences of length 5 */
    int nw = 0;
    for (int i = 0; i < nseq; i++) {
        if (seq_len[i] != N) continue;
        int cur = i;
        for (int j = 0; j < N; j++) {
            words[nw][j] = seq_first[cur];
            word_col[nw][j] = cur;          /* column j uses seq (t_j..t_5) */
            cur = seq_rest[cur];
        }
        nw++;
    }
    if (nw != 324) { fprintf(stderr, "expected 324 words, got %d\n", nw); exit(2); }
}

static void matmul(int X[N][N], int Y[N][N], int Z[N][N]) {
    for (int i = 0; i < N; i++)
        for (int j = 0; j < N; j++) {
            int s = 0;
            for (int k = 0; k < N; k++) s = ADD[s][MUL[X[i][k]][Y[k][j]]];
            Z[i][j] = s;
        }
}

static void matvec(int X[N][N], const int *v, int *out) {
    for (int i = 0; i < N; i++) {
        int s = 0;
        for (int k = 0; k < N; k++) s = ADD[s][MUL[X[i][k]][v[k]]];
        out[i] = s;
    }
}

/* inverse by Gauss-Jordan; returns 0 if singular */
static int inverse(int X[N][N], int Y[N][N]) {
    int M[N][2 * N];
    for (int i = 0; i < N; i++)
        for (int j = 0; j < N; j++) { M[i][j] = X[i][j]; M[i][N + j] = (i == j); }
    for (int c = 0; c < N; c++) {
        int p = -1;
        for (int i = c; i < N; i++) if (M[i][c]) { p = i; break; }
        if (p < 0) return 0;
        if (p != c) for (int j = 0; j < 2 * N; j++) { int t = M[c][j]; M[c][j] = M[p][j]; M[p][j] = t; }
        int f = INV[M[c][c]];
        for (int j = 0; j < 2 * N; j++) M[c][j] = MUL[f][M[c][j]];
        for (int i = 0; i < N; i++) {
            if (i == c || !M[i][c]) continue;
            int g = NEG[M[i][c]];
            for (int j = 0; j < 2 * N; j++) M[i][j] = ADD[M[i][j]][MUL[g][M[c][j]]];
        }
    }
    for (int i = 0; i < N; i++) for (int j = 0; j < N; j++) Y[i][j] = M[i][N + j];
    return 1;
}

/* rank of the N x N matrix whose columns are the given vectors */
static int rank_cols(int *cols[N]) {
    int M[N][N];
    for (int i = 0; i < N; i++) for (int j = 0; j < N; j++) M[i][j] = cols[j][i];
    int r = 0;
    for (int c = 0; c < N && r < N; c++) {
        int p = -1;
        for (int i = r; i < N; i++) if (M[i][c]) { p = i; break; }
        if (p < 0) continue;
        if (p != r) for (int j = 0; j < N; j++) { int t = M[r][j]; M[r][j] = M[p][j]; M[p][j] = t; }
        int f = INV[M[r][c]];
        for (int j = c; j < N; j++) M[r][j] = MUL[f][M[r][j]];
        for (int i = r + 1; i < N; i++) {
            if (!M[i][c]) continue;
            int g = NEG[M[i][c]];
            for (int j = c; j < N; j++) M[i][j] = ADD[M[i][j]][MUL[g][M[r][j]]];
        }
        r++;
    }
    return r;
}

static int derive(void) {
    if (!inverse(A[0], A[1])) return 0;
    if (!inverse(A[2], A[3])) return 0;
    matvec(A[1], B[0], B[1]);
    matvec(A[3], B[2], B[3]);
    return 1;
}

static int objective(void) {
    /* suffix products: S[seq] = A_{t5} ... A_{t_j} for seq (t_j..t_5) */
    for (int i = 0; i < N; i++) for (int j = 0; j < N; j++) S[0][i][j] = (i == j);
    for (int s = 1; s < nseq; s++) {
        matmul(S[seq_rest[s]], A[seq_first[s]], S[s]);
        matvec(S[seq_rest[s]], B[seq_first[s]], V[s]);
    }
    int def = 0;
    for (int w = 0; w < 324; w++) {
        int *cols[N];
        for (int j = 0; j < N; j++) cols[j] = V[word_col[w][j]];
        def += N - rank_cols(cols);
    }
    return def;
}

static void print_chart(long seed) {
    printf("{\"q\":%d,\"seed\":%ld,\"A\":[", q, seed);
    for (int t = 0; t < 4; t++) {
        printf("%s[", t ? "," : "");
        for (int i = 0; i < N; i++) {
            printf("%s[", i ? "," : "");
            for (int j = 0; j < N; j++) printf("%s%d", j ? "," : "", A[t][i][j]);
            printf("]");
        }
        printf("]");
    }
    printf("],\"b\":[");
    for (int t = 0; t < 4; t++) {
        printf("%s[", t ? "," : "");
        for (int i = 0; i < N; i++) printf("%s%d", i ? "," : "", B[t][i]);
        printf("]");
    }
    printf("]}\n");
}

int main(int argc, char **argv) {
    if (argc < 4) { fprintf(stderr, "usage: %s TABLEFILE SEED ITERS [T0 T1]\n", argv[0]); return 2; }
    FILE *f = fopen(argv[1], "r");
    if (!f || fscanf(f, "%d", &q) != 1 || q < 2 || q > MAXQ) { fprintf(stderr, "bad table file\n"); return 2; }
    for (int i = 0; i < q; i++) for (int j = 0; j < q; j++) { int v; if (fscanf(f, "%d", &v) != 1) return 2; ADD[i][j] = v; }
    for (int i = 0; i < q; i++) for (int j = 0; j < q; j++) { int v; if (fscanf(f, "%d", &v) != 1) return 2; MUL[i][j] = v; }
    for (int i = 0; i < q; i++) if (fscanf(f, "%d", &NEG[i]) != 1) return 2;
    for (int i = 0; i < q; i++) if (fscanf(f, "%d", &INV[i]) != 1) return 2;
    fclose(f);
    long seed = atol(argv[2]);
    long iters = atol(argv[3]);
    double T0 = argc > 4 ? atof(argv[4]) : 1.5, T1 = argc > 5 ? atof(argv[5]) : 0.05;
    rng_state = 0x9E3779B97F4A7C15ULL ^ (uint64_t)(seed * 1000003 + 17);
    for (int i = 0; i < 20; i++) rng();

    build_sequences();

    if (iters == 0) {
        /* evaluation mode: read A_0 (25), A_2 (25), b_0 (5), b_2 (5) from stdin */
        for (int t = 0; t < 4; t += 2)
            for (int i = 0; i < N; i++) for (int j = 0; j < N; j++)
                if (scanf("%d", &A[t][i][j]) != 1) return 2;
        for (int t = 0; t < 4; t += 2)
            for (int i = 0; i < N; i++) if (scanf("%d", &B[t][i]) != 1) return 2;
        if (!derive()) { printf("singular A\n"); return 1; }
        printf("deficiency %d\n", objective());
        return 0;
    }

    /* random start with invertible A_0, A_2 and nonzero b */
    do {
        for (int t = 0; t < 4; t += 2) {
            for (int i = 0; i < N; i++) for (int j = 0; j < N; j++) A[t][i][j] = rng() % q;
            for (int i = 0; i < N; i++) B[t][i] = rng() % q;
        }
    } while (!derive());
    int cur = objective(), best = cur;
    int bestA[4][N][N], bestB[4][N];
    memcpy(bestA, A, sizeof A); memcpy(bestB, B, sizeof B);

    for (long it = 0; it < iters && cur > 0; it++) {
        double T = T0 * pow(T1 / T0, (double)it / (double)iters);
        /* pick one of the 60 free entries */
        int r = rng() % 60, t, i, j = -1, old;
        int nv = 1 + rng() % (q - 1);
        if (r < 50) {
            t = (r < 25) ? 0 : 2; i = (r % 25) / 5; j = r % 5;
            old = A[t][i][j];
            A[t][i][j] = ADD[old][nv];
        } else {
            t = (r < 55) ? 0 : 2; i = (r - 50) % 5;
            old = B[t][i];
            B[t][i] = ADD[old][nv];
        }
        int ok = derive();
        int cand = ok ? objective() : 1 << 30;
        int delta = cand - cur;
        if (ok && (delta <= 0 || rnd01() < exp(-delta / T))) {
            cur = cand;
            if (cur < best) {
                best = cur;
                memcpy(bestA, A, sizeof A); memcpy(bestB, B, sizeof B);
            }
        } else {
            if (j >= 0) A[t][i][j] = old; else B[t][i] = old;
            derive();
        }
    }
    if (best == 0) {
        memcpy(A, bestA, sizeof A); memcpy(B, bestB, sizeof B);
        derive();
        if (objective() != 0) { fprintf(stderr, "internal error\n"); return 3; }
        print_chart(seed);
        return 0;
    }
    printf("{\"q\":%d,\"seed\":%ld,\"best_deficiency\":%d}\n", q, seed, best);
    return 1;
}
