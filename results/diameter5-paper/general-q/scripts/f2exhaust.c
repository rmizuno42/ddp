/*
 * f2exhaust.c -- exhaustive search for universal route charts on GF(2)^5 over
 * S = {a, a^-1, b, b^-1}, up to simultaneous conjugation.
 *
 * Reduction.  The word aaaaa forces (A_a, b_a) to be controllable, so A_a is
 * cyclic.  Conjugating every A_t and b_t by one P in GL_5(2) preserves
 * universality (M_w -> P M_w), so A_a may be taken to be the companion matrix
 * C_f of its characteristic polynomial f (degree 5, f(0) = 1: 16 choices).
 * The centralizer of C_f, the units of GF(2)[C_f], acts simply transitively
 * on the cyclic vectors of C_f, so b_a may be taken to be e_0.  Every other
 * datum is enumerated: all A_b in GL_5(2) and all nonzero b_b.
 *
 * Vectors are 5-bit integers; a matrix is stored by its columns and applied
 * through a 32-entry lookup table.
 *
 * Usage: f2exhaust F_INDEX   (0..15: f = x^5 + c4 x^4 + ... + c1 x + 1 with
 *                             (c1..c4) the bits of F_INDEX)
 * Prints the number of (A_b, b_b) completing (C_f, e_0) to a universal chart.
 */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static const int SINV[4] = {1, 0, 3, 2};
static int words[324][5];
static int nwords;

static void gen(int *w, int len) {
    if (len == 5) {
        for (int i = 0; i < 5; i++) words[nwords][i] = w[i];
        nwords++;
        return;
    }
    for (int t = 0; t < 4; t++) {
        if (len && t == SINV[w[len - 1]]) continue;
        w[len] = t;
        gen(w, len + 1);
    }
}

static inline void table(const int col[5], uint8_t T[32]) {
    for (int v = 0; v < 32; v++) {
        int s = 0;
        for (int j = 0; j < 5; j++) if (v >> j & 1) s ^= col[j];
        T[v] = s;
    }
}

/* insert v into a GF(2) basis indexed by leading bit; return 0 if dependent */
static inline int insert(int basis[5], int v) {
    for (int bit = 4; bit >= 0; bit--) {
        if (!(v >> bit & 1)) continue;
        if (!basis[bit]) { basis[bit] = v; return 1; }
        v ^= basis[bit];
    }
    return 0;
}

int main(int argc, char **argv) {
    int fi = atoi(argv[1]);
    int w[5];
    gen(w, 0);
    if (nwords != 324) return 2;

    /* companion matrix: C e_j = e_{j+1} (j < 4), C e_4 = (1, c1, c2, c3, c4) */
    int ca[5] = {2, 4, 8, 16, 1 | ((fi & 15) << 1)};
    uint8_t T[4][32];
    table(ca, T[0]);
    for (int v = 0; v < 32; v++) T[1][T[0][v]] = v;     /* inverse table */
    int B[4];
    B[0] = 1;                    /* e_0 */
    B[1] = T[1][B[0]];           /* A_a^-1 b_a */

    long long solutions = 0, invertible = 0;
    int col[5];
    if (argc == 8) {
        /* test mode: f2exhaust F_INDEX c0 c1 c2 c3 c4 BB -> number of singular words */
        for (int j = 0; j < 5; j++) col[j] = atoi(argv[2 + j]);
        table(col, T[2]);
        for (int v = 0; v < 32; v++) T[3][T[2][v]] = v;
        B[2] = atoi(argv[7]);
        B[3] = T[3][B[2]];
        int singular = 0;
        for (int k = 0; k < 324; k++) {
            const int *x = words[k];
            int c[5], bs[5] = {0, 0, 0, 0, 0}, good = 1;
            c[4] = B[x[4]];
            c[3] = T[x[4]][B[x[3]]];
            c[2] = T[x[4]][T[x[3]][B[x[2]]]];
            c[1] = T[x[4]][T[x[3]][T[x[2]][B[x[1]]]]];
            c[0] = T[x[4]][T[x[3]][T[x[2]][T[x[1]][B[x[0]]]]]];
            for (int j = 0; j < 5 && good; j++) good = insert(bs, c[j]);
            singular += !good;
        }
        printf("%d\n", singular);
        return 0;
    }
    for (col[0] = 1; col[0] < 32; col[0]++)
    for (col[1] = 1; col[1] < 32; col[1]++)
    for (col[2] = 1; col[2] < 32; col[2]++)
    for (col[3] = 1; col[3] < 32; col[3]++)
    for (col[4] = 1; col[4] < 32; col[4]++) {
        int basis[5] = {0, 0, 0, 0, 0}, ok = 1;
        for (int j = 0; j < 5 && ok; j++) ok = insert(basis, col[j]);
        if (!ok) continue;
        invertible++;
        table(col, T[2]);
        for (int v = 0; v < 32; v++) T[3][T[2][v]] = v;
        for (int bb = 1; bb < 32; bb++) {
            B[2] = bb;
            B[3] = T[3][bb];
            int good = 1;
            for (int k = 0; k < 324 && good; k++) {
                const int *x = words[k];
                int c[5];
                c[4] = B[x[4]];
                c[3] = T[x[4]][B[x[3]]];
                c[2] = T[x[4]][T[x[3]][B[x[2]]]];
                c[1] = T[x[4]][T[x[3]][T[x[2]][B[x[1]]]]];
                c[0] = T[x[4]][T[x[3]][T[x[2]][T[x[1]][B[x[0]]]]]];
                int bs[5] = {0, 0, 0, 0, 0};
                for (int j = 0; j < 5 && good; j++) good = insert(bs, c[j]);
            }
            if (good) {
                if (solutions < 3)
                    printf("SOLUTION f=%d A_b cols %d %d %d %d %d b_b %d\n",
                           fi, col[0], col[1], col[2], col[3], col[4], bb);
                solutions++;
            }
        }
    }
    printf("f_index %d: A_b candidates in GL_5(2) %lld, solutions %lld\n", fi, invertible, solutions);
    return 0;
}
