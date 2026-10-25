/* Exact exhaustive scorer for experiment052. No cryptographic/linguistic heuristic.
 * Python supplies the double-valued score lookup tables. No floating arithmetic
 * except comparisons occurs here. All models are evaluated. Compile without
 * fast-math; tie ordering is supplied explicitly by the Python wrapper.
 */
#include <stddef.h>
#include <stdint.h>
#include <string.h>
#include <float.h>

#define L 97
#define RMAX 32
#define NUNKNOWN 73
#define DCOUNT 1152
#define TIEWORDS 18
#define SCORECOLS 74

static int unknown(int i) {
    return !((i >= 21 && i < 34) || (i >= 63 && i < 74));
}

static void consider(double value, int desc, const int *ranks, double *best,
                     int *best_desc, uint64_t *ties, double *all_scores) {
    if (all_scores) all_scores[desc] = value;
    if (value > *best) {
        *best = value;
        *best_desc = desc;
        if (ties) {
            memset(ties, 0, TIEWORDS * sizeof(uint64_t));
            ties[desc / 64] |= UINT64_C(1) << (desc % 64);
        }
    } else if (value == *best) {
        if (ranks[desc] < ranks[*best_desc]) *best_desc = desc;
        if (ties) ties[desc / 64] |= UINT64_C(1) << (desc % 64);
    }
}

int score_bank(size_t count, const uint8_t *plaintexts, const uint8_t *ciphertexts,
               const double *period_scores, const double *auto_scores,
               const int *ranks, double *out_best, int *out_desc,
               uint64_t *out_ties, double *out_all_scores) {
    if (!count || !plaintexts || !ciphertexts || !period_scores || !auto_scores ||
        !ranks || !out_best || !out_desc) return -1;
    int positions[NUNKNOWN], npos = 0;
    for (int i = 0; i < L; ++i) if (unknown(i)) positions[npos++] = i;
    if (npos != NUNKNOWN) return -2;
    for (size_t row = 0; row < count; ++row) {
        double best = -DBL_MAX;
        int best_desc = 0;
        uint64_t *ties = out_ties ? out_ties + row * TIEWORDS : NULL;
        double *all = out_all_scores ? out_all_scores + row * DCOUNT : NULL;
        if (ties) memset(ties, 0, TIEWORDS * sizeof(uint64_t));
        for (int pa = 0; pa < 2; ++pa) {
            const uint8_t *p = plaintexts + (row * 2 + (size_t)pa) * L;
            for (int ca = 0; ca < 2; ++ca) {
                const uint8_t *c = ciphertexts + ca * L;
                for (int op = 0; op < 3; ++op) {
                    const int ti = (pa * 2 + ca) * 3 + op;
                    uint8_t q[L];
                    for (int i = 0; i < L; ++i) {
                        int v = op == 0 ? (int)c[i] - p[i] :
                                op == 1 ? (int)c[i] + p[i] : (int)p[i] - c[i];
                        if (v < 0) v += 26;
                        if (v >= 26) v -= 26;
                        q[i] = (uint8_t)v;
                    }
                    for (int r = 1; r <= RMAX; ++r) {
                        uint8_t counts[RMAX][26];
                        uint8_t maxima[RMAX];
                        memset(counts, 0, sizeof(counts));
                        memset(maxima, 0, sizeof(maxima));
                        int total_matches = 0;
                        for (int j = 0; j < NUNKNOWN; ++j) {
                            const int i = positions[j], residue = i % r, value = q[i];
                            const uint8_t n = ++counts[residue][value];
                            if (n > maxima[residue]) {
                                maxima[residue] = n;
                                ++total_matches;
                            }
                        }
                        const int e = NUNKNOWN - total_matches;
                        const int desc = ti * 96 + (r - 1);
                        consider(period_scores[(r - 1) * SCORECOLS + e], desc, ranks,
                                 &best, &best_desc, ties, all);
                    }
                    for (int r = 1; r <= RMAX; ++r) {
                        int ep = 0, ec = 0;
                        for (int j = 0; j < NUNKNOWN; ++j) {
                            const int i = positions[j];
                            if (i >= r) {
                                ep += q[i] != p[i - r];
                                ec += q[i] != c[i - r];
                            }
                        }
                        consider(auto_scores[(r - 1) * SCORECOLS + ep],
                                 ti * 96 + 32 + (r - 1), ranks, &best, &best_desc, ties, all);
                        consider(auto_scores[(r - 1) * SCORECOLS + ec],
                                 ti * 96 + 64 + (r - 1), ranks, &best, &best_desc, ties, all);
                    }
                }
            }
        }
        out_best[row] = best;
        out_desc[row] = best_desc;
    }
    return 0;
}
