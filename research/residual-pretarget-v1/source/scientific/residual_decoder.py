"""Development-only exact canonical residual decoder; no target parser or data.

All feasible support/beta fibers are retained. Marginals are not joint tuples.
See PLAN.md for fixed residual semantics and all authorization boundaries.
"""
from dataclasses import dataclass
from itertools import combinations
from pathlib import Path
import hashlib
import json
import time
import affine_filter as af

VERSION = 'canonical-residual-dev-1'
COMPILER = 'E-minus-B-union-exact156-C-1'
DEPENDENCY_SHA256 = '1e19e9ad872d517487cfe7968a9f4b906756007d5e710be216807620f078c90d'
if hashlib.sha256(Path(af.__file__).read_bytes()).hexdigest() != DEPENDENCY_SHA256:
    raise RuntimeError('generic module source pin mismatch')
SOURCE_SHA256 = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
GROUP = tuple([0] + list(range(1, 7)) + list(range(1, 7)) + list(range(7, 25)))
REPS = tuple(GROUP.index(g) for g in range(25))
EQUALITY = (28, 29, 30)
EQGROUP = (22, 23, 24)


@dataclass(frozen=True)
class Budget:
    max_steps: int = 2_000_000
    max_pieces: int = 40_000
    max_core_work: int = 200_000_000
    max_core_solves: int = 1_000_000
    max_core_terms: int = 100_000
    max_seconds: float = 60.0


class Exhausted(Exception):
    pass


def require(condition, message):
    if not condition:
        raise af.CertificateError(message)


def features(context):
    # Public decode validates inputs; equality is on unreduced Z26 symbols.
    return ([1] + list(context) + [v*v % 26 for v in context]
            + [context[i]*context[j] % 26 for i, j in combinations(range(6), 2)]
            + [int(context[i] == context[i+1]) for i in (0, 2, 4)])


def descriptor(theta):
    alpha = [v % 13 for v in theta]
    beta = [0] * 25
    for j, v in enumerate(theta):
        beta[GROUP[j]] ^= v % 2
    return alpha, beta


def residual(alpha, beta):
    """Canonical function predicate, never support-container syntax."""
    if not any(alpha[j] or beta[GROUP[j]] for j in EQUALITY):
        return False
    if not any(beta[g] for g in range(2, 25)):
        return False
    for q in EQUALITY:
        if (beta[GROUP[q]] == 1
                and not any(beta[g] for g in range(25) if g not in (0, GROUP[q]))
                and alpha[q] in (1, 12)
                and not any(alpha[j] for j in range(31) if j not in (0, q))):
            return False
    return True


def support_cost(alpha, beta):
    active = {GROUP[j] for j, v in enumerate(alpha) if v}
    return sum(v != 0 for v in alpha) + sum(beta[g] for g in range(25) if g not in active)


def lift(support, a, beta_active):
    """Construct an exact minimum-support original lift INSIDE support."""
    alpha = dict(zip(support, a))
    parity = {}
    for g in beta_active:
        members = [j for j in support if GROUP[j] == g]
        require(bool(members), 'beta outside common original support')
        active = [j for j in members if alpha[j]]
        parity[(active or members)[0]] = 1
    return [[j, alpha[j] + 13 * ((parity.get(j, 0) - alpha[j]) % 2)]
            for j in support if alpha[j] or parity.get(j, 0)]


def compile_exclusions(support, beta_active):
    """Exactly (!E) union C for a fixed B-eligible beta, restricted to T."""
    n = len(support)
    def equation(j, value):
        return [int(k == j) for k in support] + [value]
    cuts = []
    b = set(beta_active)
    if not b.intersection(EQGROUP):
        cuts.append([equation(j, 0) for j in EQUALITY])
    for q in EQUALITY:
        if GROUP[q] in b and b.issubset({0, GROUP[q]}):
            zeros = [equation(j, 0) for j in support if j not in (0, q)]
            cuts.extend([zeros + [equation(q, value)] for value in (1, 12)])
    require(len(cuts) <= 2 and all(len(r) == n+1 for c in cuts for r in c), 'compiler shape')
    return cuts


def _validate(contexts, observed, sparsity, allowed_features, budget):
    if type(contexts) not in (tuple, list) or len(contexts) > 128:
        raise ValueError('contexts must be a bounded list/tuple')
    for context in contexts:
        if (type(context) not in (tuple, list) or len(context) != 6
                or any(type(v) is not int or not 0 <= v < 26 for v in context)):
            raise ValueError('context must have six canonical Z26 integers')
    if type(observed) is not dict or any(type(i) is not int or not 0 <= i < len(contexts)
            or type(v) is not int or not 0 <= v < 26 for i, v in observed.items()):
        raise ValueError('observed must map context indices to canonical Z26 values')
    if type(sparsity) is not int or not 0 <= sparsity <= 3:
        raise ValueError('sparsity must be an integer in [0,3]')
    if allowed_features is None:
        allowed_features = list(range(31))
    if (type(allowed_features) not in (tuple, list)
            or any(type(j) is not int or not 0 <= j < 31 for j in allowed_features)
            or list(allowed_features) != sorted(set(allowed_features))):
        raise ValueError('allowed_features must be sorted distinct original indices')
    if type(budget) is not Budget:
        raise ValueError('Budget required')
    for value in (budget.max_steps, budget.max_pieces, budget.max_core_work,
                  budget.max_core_solves, budget.max_core_terms):
        if type(value) is not int or not 0 <= value <= 10**12:
            raise ValueError('invalid integer resource cap')
    if type(budget.max_seconds) not in (int, float) or not 0 <= budget.max_seconds <= 3600:
        raise ValueError('invalid time cap')
    return tuple(tuple(x) for x in contexts), dict(observed), tuple(allowed_features)


def check_sparse_witness(contexts, observed, sparsity, allowed_features, theta, row=None, value=None):
    """Strict local witness validation; NOT a complete-result verifier."""
    contexts, observed, allowed_features = _validate(contexts, observed, sparsity, allowed_features, Budget())
    if type(theta) not in (tuple, list) or len(theta) > sparsity:
        raise ValueError('invalid sparse witness size')
    seen = set()
    vector = [0] * 31
    for pair in theta:
        if type(pair) not in (tuple, list) or len(pair) != 2:
            raise ValueError('invalid sparse pair')
        j, v = pair
        if (type(j) is not int or j not in allowed_features or j in seen
                or type(v) is not int or not 1 <= v < 26):
            raise ValueError('invalid sparse coordinate')
        seen.add(j)
        vector[j] = v
    alpha, beta = descriptor(vector)
    require(residual(alpha, beta), 'witness is outside canonical residual')
    require(support_cost(alpha, beta) <= len(theta), 'minimum support contradiction')
    values = [sum(v*w for v, w in zip(features(c), vector)) % 26 for c in contexts]
    require(all(values[i] == v for i, v in observed.items()), 'witness violates observation')
    if row is not None or value is not None:
        if type(row) is not int or not 0 <= row < len(contexts) or type(value) is not int or not 0 <= value < 26:
            raise ValueError('invalid requested row/value')
        require(values[row] == value, 'witness has wrong scalar value')
    return True


def decode(contexts, observed, sparsity=3, allowed_features=None, budget=Budget()):
    contexts, observed, allowed = _validate(contexts, observed, sparsity, allowed_features, budget)
    identity = hashlib.sha256(json.dumps([VERSION, COMPILER, SOURCE_SHA256, DEPENDENCY_SHA256,
        contexts, sorted(observed.items()), sparsity, allowed], separators=(',', ':')).encode()).hexdigest()
    header = dict(version=VERSION, compiler=COMPILER, source_sha256=SOURCE_SHA256,
                  dependency_sha256=DEPENDENCY_SHA256, instance_sha256=identity)
    start = time.monotonic()
    stats = dict(containers=0, beta_candidates=0, incompatible_beta=0, excluded_B=0,
                 eligible_pieces=0, empty_pieces=0, feasible_pieces=0)
    resources = dict(steps=0, core_work=0, core_solves=0, core_terms=0)
    def tick(amount=1):
        if amount > budget.max_steps - resources['steps']:
            raise Exhausted('step budget')
        resources['steps'] += amount
        if time.monotonic() - start >= budget.max_seconds:
            raise Exhausted('wall-time budget')
    def finish(status, **data):
        return dict(header, status=status, stats=stats, resources=dict(resources,
                    wall_seconds=time.monotonic()-start), **data)
    masks = [set() for _ in contexts]
    witnesses = [{} for _ in contexts]
    provenance = [{} for _ in contexts]
    pieces = []
    feasibility_witness = None
    try:
        tick()
        rows = [features(c) for c in contexts]
        inds = sorted(observed)
        wanted = sum((observed[i] % 2) << k for k, i in enumerate(inds))
        synd = [sum((rows[i][REPS[g]] % 2) << k for k, i in enumerate(inds)) for g in range(25)]
        for support in combinations(allowed, min(sparsity, len(allowed))):
            tick()
            stats['containers'] += 1
            groups = sorted({GROUP[j] for j in support})
            base = [[rows[i][j] % 13 for j in support] + [observed[i] % 13] for i in inds]
            scalars = [[row[j] % 13 for j in support] for row in rows]
            for k in range(len(groups)+1):
                for beta in combinations(groups, k):
                    tick()
                    stats['beta_candidates'] += 1
                    if not any(g not in (0, 1) for g in beta):
                        stats['excluded_B'] += 1
                        continue
                    z = 0
                    for g in beta:
                        z ^= synd[g]
                    if z != wanted:
                        stats['incompatible_beta'] += 1
                        continue
                    if stats['eligible_pieces'] >= budget.max_pieces:
                        raise Exhausted('piece budget')
                    stats['eligible_pieces'] += 1
                    cuts = compile_exclusions(support, beta)
                    remaining = max(0.0, budget.max_seconds - (time.monotonic()-start))
                    core = af.project_filtered_affine(13, len(support), base, cuts, scalars,
                        af.Budget(budget.max_core_work-resources['core_work'],
                                  budget.max_core_solves-resources['core_solves'],
                                  budget.max_core_terms-resources['core_terms'], remaining))
                    for key in ('work', 'solves', 'terms'):
                        resources['core_'+key] += core['resources'][key]
                    tick()
                    if core['status'] == 'INCOMPLETE':
                        raise Exhausted('affine core: ' + core['reason'])
                    if core['status'] == 'EMPTY':
                        stats['empty_pieces'] += 1
                        continue
                    require(core['status'] == 'EXACT', 'unknown core status')
                    pid = 'p%06d' % len(pieces)
                    piece = dict(id=pid, support=list(support), beta=list(beta), base=base,
                                 forbidden=cuts, core=core)
                    pieces.append(piece)
                    stats['feasible_pieces'] += 1
                    def make_witness(a):
                        theta = lift(support, a, beta)
                        vector = [0]*31
                        for j, v in theta:
                            vector[j] = v
                        alpha, bits = descriptor(vector)
                        require(all(alpha[j] == v for j, v in zip(support, a)), 'lift alpha')
                        require([g for g, v in enumerate(bits) if v] == list(beta), 'lift beta')
                        require(len(theta) == support_cost(alpha, bits) <= sparsity, 'lift minimum support')
                        require(residual(alpha, bits), 'lift residual')
                        require(all(sum(row[j]*v for j, v in theta) % 26 == observed[i]
                                    for i, row in enumerate(rows) if i in observed), 'lift observation')
                        return dict(piece=pid, theta=theta)
                    # Retain a feasible original-coordinate witness even for no outputs.
                    fw = make_witness(core['feasibility_witness'])
                    piece['feasibility_witness'] = fw
                    if feasibility_witness is None:
                        feasibility_witness = fw
                    for i, row in enumerate(rows):
                        parity = sum(row[REPS[g]] for g in beta) % 2
                        for a in core['masks'][i]:
                            tick()
                            value = a + 13*((parity-a) % 2)
                            provenance[i].setdefault(value, []).append(pid)
                            masks[i].add(value)
                            if value not in witnesses[i]:
                                w = make_witness(core['witnesses'][i][a])
                                require(sum(row[j]*v for j, v in w['theta']) % 26 == value, 'lift scalar')
                                witnesses[i][value] = w
        tick()
        return finish('EXACT' if pieces else 'EMPTY', masks=[sorted(m) for m in masks],
                      witnesses=witnesses, provenance=provenance, pieces=pieces,
                      feasibility_witness=feasibility_witness)
    except Exhausted as exc:
        return finish('INCOMPLETE', reason=str(exc), masks=None, witnesses=None,
                      provenance=None, pieces=None, feasibility_witness=None)


def check_joint(contexts, observed, result, piece_id, alpha, values):
    """Check one joint candidate in ONE retained fiber; never combine marginals.

    This is a trusted in-memory result helper, not an untrusted-result verifier.
    """
    if result.get('status') != 'EXACT':
        raise ValueError('joint check requires EXACT result')
    piece = next((p for p in result['pieces'] if p['id'] == piece_id), None)
    if piece is None or type(alpha) not in (tuple, list) or len(alpha) != len(piece['support']):
        raise ValueError('invalid piece/alpha')
    if any(type(a) is not int or not 0 <= a < 13 for a in alpha):
        raise ValueError('noncanonical alpha')
    if type(values) not in (tuple, list) or len(values) != len(contexts) or any(type(v) is not int or not 0 <= v < 26 for v in values):
        raise ValueError('invalid joint values')
    sat = lambda eqs: all(sum(x*y for x, y in zip(e[:-1], alpha)) % 13 == e[-1] for e in eqs)
    require(sat(piece['base']) and all(not sat(c) for c in piece['forbidden']), 'joint point outside fiber')
    theta = lift(piece['support'], alpha, piece['beta'])
    check_sparse_witness(contexts, observed, len(piece['support']), piece['support'], theta)
    require(all(sum(features(c)[j]*v for j, v in theta) % 26 == z for c, z in zip(contexts, values)), 'not one joint prediction')
    return theta
