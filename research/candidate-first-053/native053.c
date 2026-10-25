/* Independent fixed-family arithmetic / language scoring for experiment 053.
 * No corpus, candidate bank, ciphertext target, or control data is embedded.
 * Build without fast-math; additions deliberately follow reference order.
 */
#include <math.h>
#include <stddef.h>
#include <stdint.h>

#define NLET 97
#define NMODELS 12
#define RADIX 26
#define CTX3 17576

static const uint8_t axis[2][RADIX] = {
    {0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25},
    {10,17,24,15,19,14,18,0,1,2,3,4,5,6,7,8,9,11,12,13,16,20,21,22,23,25}
};

/* IDs: plaintext axis, ciphertext axis, then V/B/VB, each in fixed order. */
static void inverse_axes(uint8_t inv[2][RADIX]) {
    for (int a = 0; a < 2; ++a)
        for (int i = 0; i < RADIX; ++i)
            inv[a][axis[a][i]] = (uint8_t)i;
}

static void derive_unchecked(const uint8_t *cipher, const uint8_t *plain,
                             int model, const uint8_t inv[2][RADIX],
                             uint8_t *key) {
    const int pa = model / 6;
    const int ca = (model / 3) % 2;
    const int op = model % 3;
    for (int i = 0; i < NLET; ++i) {
        const int p = inv[pa][plain[i]];
        const int c = inv[ca][cipher[i]];
        int residue;
        if (op == 0) residue = (c - p + RADIX) % RADIX;
        else if (op == 1) residue = (c + p) % RADIX;
        else residue = (p - c + RADIX) % RADIX;
        key[i] = axis[pa][residue];
    }
}

int cf053_abi_version(void) { return 1; }

int cf053_derive_key(const uint8_t *cipher, const uint8_t *plain,
                     int model, uint8_t *key) {
    if (!cipher || !plain || !key || model < 0 || model >= NMODELS) return 1;
    for (int i = 0; i < NLET; ++i)
        if (cipher[i] >= RADIX || plain[i] >= RADIX) return 2;
    uint8_t inv[2][RADIX];
    inverse_axes(inv);
    derive_unchecked(cipher, plain, model, inv, key);
    return 0;
}

/* Add one span to an existing accumulator; history restarts at each span. */
static double add_span(const uint8_t *key, int start, int end,
                       const double *const logs[4], double sum) {
    unsigned context = 0;
    for (int pos = start; pos < end; ++pos) {
        const int depth = pos - start < 3 ? pos - start : 3;
        const unsigned index = context * RADIX + key[pos];
        sum += logs[depth][index];
        context = index % CTX3;
    }
    return sum;
}

/* Both output matrices are candidate-major, then model ID (0..11).
 * baseline and choice are Python-computed once to match binary64 constants.
 * Choice is log2(nbank) + log2(12); primary is (baseline + sum) - choice.
 */
int cf053_score_all(const uint8_t *cipher, const uint8_t *bank, size_t nbank,
                    const double *log1, const double *log2,
                    const double *log3, const double *log4,
                    double baseline, double choice,
                    double *scores, double *full_h) {
    if (!cipher || !bank || !scores || !full_h || !log1 || !log2 ||
        !log3 || !log4 || !nbank || nbank > SIZE_MAX / (NLET * NMODELS)) return 1;
    if (!isfinite(baseline) || !isfinite(choice)) return 3;
    for (int i = 0; i < NLET; ++i) if (cipher[i] >= RADIX) return 2;
    for (size_t i = 0; i < nbank * NLET; ++i) if (bank[i] >= RADIX) return 2;
    uint8_t inv[2][RADIX];
    inverse_axes(inv);
    const double *logs[4] = {log1, log2, log3, log4};
    for (size_t candidate = 0; candidate < nbank; ++candidate) {
        const uint8_t *plain = bank + candidate * NLET;
        for (int model = 0; model < NMODELS; ++model) {
            uint8_t key[NLET];
            derive_unchecked(cipher, plain, model, inv, key);
            double sum = 0.0;
            sum = add_span(key, 0, 21, logs, sum);
            sum = add_span(key, 34, 63, logs, sum);
            sum = add_span(key, 74, 97, logs, sum);
            const size_t out = candidate * NMODELS + (size_t)model;
            scores[out] = (baseline + sum) - choice;
            const double whole = add_span(key, 0, NLET, logs, 0.0);
            full_h[out] = -whole / NLET;
        }
    }
    return 0;
}
