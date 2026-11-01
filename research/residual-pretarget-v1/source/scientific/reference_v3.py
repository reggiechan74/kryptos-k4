"""Independent certified observation-fiber reference, version 3.

Development-only. No producer algebra imports. All public computations use an
explicit cumulative meter. See CONTRACT.md for units and supported inputs.
This source must not be executed before the joint pre-run freeze gate.
"""
from dataclasses import dataclass
from itertools import combinations, product
from pathlib import Path
import hashlib
import json
import math
import time

VERSION = 'independent-residual-reference-3'
CERT_VERSION = 'affine-certificate-3'
ENGINE_VERSION = 'canonical-residual-dev-1'
COMPILER = 'E-minus-B-union-exact156-C-1'
DEPENDENCY_SHA256 = '1e19e9ad872d517487cfe7968a9f4b906756007d5e710be216807620f078c90d'
SOURCE_SHA256 = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
COUNTERS = ('fiber_points', 'lift_trials', 'solve_calls', 'certificate_checks',
            'row_operations', 'work_units', 'witness_checks', 'output_records')


class VerificationError(ValueError):
    pass


class ReferenceLimit(RuntimeError):
    pass


def require(condition, message):
    if not condition:
        raise VerificationError(message)


@dataclass(frozen=True)
class BudgetV3:
    max_fiber_points: int
    max_lift_trials: int
    max_solve_calls: int
    max_certificate_checks: int
    max_row_operations: int
    max_work_units: int
    max_witness_checks: int
    max_output_records: int
    max_seconds: float


def _validate_budget(budget):
    require(type(budget) is BudgetV3, 'exact BudgetV3 required')
    for name in COUNTERS:
        value = getattr(budget, 'max_' + name)
        require(type(value) is int and value >= 0,
                'max_' + name + ' must be a built-in nonnegative integer')
    value = budget.max_seconds
    require((type(value) is int and value >= 0)
            or (type(value) is float and math.isfinite(value) and value >= 0),
            'max_seconds must be a finite built-in nonnegative number')


class Meter:
    def __init__(self, budget):
        _validate_budget(budget)
        self.budget = budget
        self.counts = {name: 0 for name in COUNTERS}
        self.generated_row_operations = 0
        self.replayed_row_operations = 0
        self.started = time.monotonic()

    def charge(self, name, amount=1):
        require(name in COUNTERS and type(amount) is int and amount >= 0,
                'internal meter request')
        if amount > getattr(self.budget, 'max_' + name) - self.counts[name]:
            raise ReferenceLimit(name + ' cap')
        if time.monotonic() - self.started >= self.budget.max_seconds:
            raise ReferenceLimit('wall-time cap')
        self.counts[name] += amount

    def work(self, amount=1):
        self.charge('work_units', amount)

    def preflight_fiber(self, count):
        if count > self.budget.max_fiber_points - self.counts['fiber_points']:
            raise ReferenceLimit('fiber_points preflight')
        if count > self.budget.max_work_units - self.counts['work_units']:
            raise ReferenceLimit('work_units fiber preflight')
        self.work(0)

    def receipt(self):
        return dict(self.counts, generated_row_operations=self.generated_row_operations,
                    replayed_row_operations=self.replayed_row_operations,
                    wall_seconds=time.monotonic() - self.started)


def _meter(meter):
    require(type(meter) is Meter, 'exact Meter required')
    _validate_budget(meter.budget)
    return meter


def _record(meter, count=1):
    meter.charge('output_records', count)


def _add(items, item, meter, weight=1):
    meter.work(max(1, weight))
    if item not in items:
        _record(meter)
        items.add(item)


def _dot(left, right, q, meter):
    require(len(left) == len(right), 'internal dot dimensions')
    meter.work(max(1, len(left)))
    return sum(x * y for x, y in zip(left, right)) % q


def _group(j):
    return j if j < 7 else j - 6


def _representative(g):
    return g if g < 7 else g + 6


def _equations(rows, n, meter):
    meter.work()
    require(type(n) is int and 0 <= n <= 3, 'equation width in [0,3] required')
    require(type(rows) in (list, tuple) and len(rows) <= 256, 'bounded equation list required')
    out = []
    for row in rows:
        meter.work(n + 2)
        require(type(row) in (list, tuple) and len(row) == n + 1, 'equation dimensions')
        require(all(type(x) is int and 0 <= x < 13 for x in row), 'equation residues')
        out.append(list(row))
    return out


def _binding(binding, n, meter):
    if binding is None:
        binding = {'role': 'generic', 'field': 13, 'n': n, 'reference_version': VERSION}
    meter.work()
    require(type(binding) is dict and len(binding) <= 16, 'certificate binding')
    out = {}
    for key, value in binding.items():
        meter.work()
        require(type(key) is str and len(key) <= 80, 'binding key')
        if type(value) is str:
            meter.work(len(value) + 1)
            require(len(value) <= 128, 'binding string')
            out[key] = value
        elif type(value) is int:
            require(0 <= value <= 256, 'binding integer')
            out[key] = value
        else:
            require(type(value) in (list, tuple) and len(value) <= 31, 'binding value')
            meter.work(len(value) + 1)
            require(all(type(x) is int and 0 <= x <= 256 for x in value), 'binding list')
            out[key] = list(value)
    return out


def _matrix_hash(rows, n, meter):
    meter.work(1 + len(rows) * (n + 1))
    return hashlib.sha256(json.dumps([13, n, rows], separators=(',', ':')).encode()).hexdigest()


def _derive_rref(matrix, original, n, meter):
    pivots = []
    zero_seen = False
    for row in matrix:
        meter.work(n + 1)
        lead = next((j for j, value in enumerate(row) if value), None)
        if lead is None:
            zero_seen = True
            continue
        require(not zero_seen, 'nonzero row after zero row')
        require(row[lead] == 1, 'RREF leading entry is not one')
        require(not pivots or lead > pivots[-1], 'RREF pivot order')
        pivots.append(lead)
    for i, col in enumerate(pivots):
        for k, row in enumerate(matrix):
            meter.work()
            require(row[col] == int(k == i), 'RREF pivot column')
    meter.work(n + len(pivots) + 1)
    rank_a = sum(col < n for col in pivots)
    consistent = n not in pivots
    free = [j for j in range(n) if j not in pivots]
    _record(meter, 1 + len(matrix) + (n-rank_a+1 if consistent else 0))
    point = None
    basis = None
    if consistent:
        meter.work(n*(len(free)+1))
        point = [0] * n
        for i, col in enumerate(pivots):
            point[col] = matrix[i][-1]
        basis = []
        for f in free:
            vector = [0] * n
            vector[f] = 1
            for i, col in enumerate(pivots):
                meter.work()
                vector[col] = -matrix[i][f] % 13
            basis.append(vector)
        for row in original:
            require(_dot(row[:-1], point, 13, meter) == row[-1], 'particular original equations')
            for vector in basis:
                require(_dot(row[:-1], vector, 13, meter) == 0, 'kernel original equations')
        for i, vector in enumerate(basis):
            for k, f in enumerate(free):
                meter.work()
                require(vector[f] == int(i == k), 'complete free-coordinate identity')
        require(len(basis) == n - rank_a, 'kernel dimension')
    return dict(consistent=consistent, rank=rank_a, rank_a=rank_a,
                rank_aug=len(pivots), pivots=pivots, free=free,
                dimension=(n-rank_a if consistent else None),
                point=point, basis=basis, rref=matrix)


def _validate_claim(name, supplied, actual, n, meter):
    meter.work()
    if name in ('rank_a', 'rank_aug'):
        require(type(supplied) is int, 'certificate rank type')
    elif name == 'dimension':
        require(supplied is None or type(supplied) is int, 'certificate dimension type')
    elif name == 'consistent':
        require(type(supplied) is bool, 'certificate consistency type')
    elif name in ('pivots', 'free'):
        require(type(supplied) is list and len(supplied) <= n + 1
                and all(type(x) is int for x in supplied), 'certificate index-list type')
    elif name == 'point':
        require(supplied is None or (type(supplied) is list and len(supplied) == n
                and all(type(x) is int and 0 <= x < 13 for x in supplied)), 'certificate point type')
    elif name == 'basis':
        require(supplied is None or (type(supplied) is list and len(supplied) <= n),
                'certificate basis type')
        if supplied is not None:
            for vector in supplied:
                meter.work(n + 1)
                require(type(vector) is list and len(vector) == n
                        and all(type(x) is int and 0 <= x < 13 for x in vector),
                        'certificate basis vector type')
    require(supplied == actual, 'false optional certificate claim: ' + name)


def replay_certificate(rows, n, certificate, *, meter, binding=None):
    meter = _meter(meter)
    meter.charge('certificate_checks')
    original = _equations(rows, n, meter)
    expected_binding = _binding(binding, n, meter)
    meter.work()
    require(type(certificate) is dict, 'certificate dictionary required')
    require(type(certificate.get('version')) is str and certificate['version'] == CERT_VERSION,
            'certificate version')
    require(type(certificate.get('q')) is int and certificate['q'] == 13, 'certificate field')
    require(type(certificate.get('n')) is int and certificate['n'] == n, 'certificate width')
    require('binding' in certificate and certificate['binding'] is not None, 'certificate binding required')
    supplied_binding = _binding(certificate['binding'], n, meter)
    require(supplied_binding == expected_binding, 'certificate binding mismatch')
    require(type(certificate.get('equations_sha256')) is str
            and certificate['equations_sha256'] == _matrix_hash(original, n, meter),
            'certificate original equations mismatch')
    ops = certificate.get('operations')
    require(type(ops) is list and len(ops) <= (n + 1) * (len(original) + 1),
            'certificate operation count')
    final = _equations(certificate.get('rref'), n, meter)
    require(len(final) == len(original), 'certificate row count')
    meter.work(len(original) * (n + 1))
    replay = [row[:] for row in original]
    for op in ops:
        meter.work()
        require(type(op) in (list, tuple) and len(op) in (3, 4), 'row operation shape')
        kind = op[0]
        require(type(kind) is str, 'row operation name')
        if kind == 'swap':
            require(len(op) == 3, 'swap width')
            _, i, j = op
            require(type(i) is int and type(j) is int
                    and 0 <= i < len(replay) and 0 <= j < len(replay), 'swap indices')
        elif kind == 'scale':
            require(len(op) == 3, 'scale width')
            _, i, u = op
            require(type(i) is int and 0 <= i < len(replay)
                    and type(u) is int and 1 <= u < 13, 'invertible scaling required')
        elif kind == 'add':
            require(len(op) == 4, 'add width')
            _, i, j, u = op
            require(type(i) is int and type(j) is int and i != j
                    and 0 <= i < len(replay) and 0 <= j < len(replay)
                    and type(u) is int and 0 <= u < 13, 'invertible row addition required')
        else:
            raise VerificationError('unknown row operation')
        meter.charge('row_operations')
        meter.work(n + 1)
        meter.replayed_row_operations += 1
        if kind == 'swap':
            replay[i], replay[j] = replay[j], replay[i]
        elif kind == 'scale':
            replay[i] = [x * u % 13 for x in replay[i]]
        else:
            replay[i] = [(x + u * y) % 13 for x, y in zip(replay[i], replay[j])]
    meter.work(len(final) * (n + 1))
    require(replay == final, 'row-operation replay mismatch')
    derived = _derive_rref(final, original, n, meter)
    for name in ('consistent', 'rank_a', 'rank_aug', 'dimension', 'pivots', 'free', 'point', 'basis'):
        if name in certificate:
            _validate_claim(name, certificate[name], derived[name], n, meter)
    return derived


def _make_space(rows, n, meter, binding=None):
    meter.charge('solve_calls')
    original = _equations(rows, n, meter)
    identity_binding = _binding(binding, n, meter)
    meter.work(len(original) * (n + 1))
    matrix = [row[:] for row in original]
    ops = []
    cursor = 0

    def emit(op):
        meter.charge('row_operations')
        meter.work(n + 2)
        _record(meter)
        meter.generated_row_operations += 1
        ops.append(op)

    for col in range(n + 1):
        pivot = None
        for i in range(cursor, len(matrix)):
            meter.work()
            if matrix[i][col]:
                pivot = i
                break
        if pivot is None:
            continue
        emit(['swap', cursor, pivot])
        matrix[cursor], matrix[pivot] = matrix[pivot], matrix[cursor]
        inverse = pow(matrix[cursor][col], -1, 13)
        emit(['scale', cursor, inverse])
        matrix[cursor] = [x * inverse % 13 for x in matrix[cursor]]
        for i in range(len(matrix)):
            meter.work()
            if i != cursor and matrix[i][col]:
                u = -matrix[i][col] % 13
                emit(['add', i, cursor, u])
                matrix[i] = [(x + u * y) % 13 for x, y in zip(matrix[i], matrix[cursor])]
        cursor += 1
    _record(meter, 1 + len(matrix))
    cert = dict(version=CERT_VERSION, q=13, n=n, binding=identity_binding,
                equations_sha256=_matrix_hash(original, n, meter), operations=ops, rref=matrix)
    # Nonoptional replay, rank and complete-kernel verification of every fresh solve.
    derived = replay_certificate(original, n, cert, meter=meter, binding=identity_binding)
    for name in ('consistent', 'rank_a', 'rank_aug', 'dimension', 'pivots', 'free', 'point', 'basis'):
        cert[name] = derived[name]
    return cert, derived


def certify_affine(rows, n, *, meter, binding=None):
    meter = _meter(meter)
    cert, _ = _make_space(rows, n, meter, binding)
    return cert


def _included(space, equations, meter):
    if not space['consistent']:
        return True
    for row in equations:
        if _dot(row[:-1], space['point'], 13, meter) != row[-1]:
            return False
        for vector in space['basis']:
            if _dot(row[:-1], vector, 13, meter) != 0:
                return False
    return True


def _same_spaces(a_rows, a_space, b_rows, b_space, meter):
    if a_space['consistent'] != b_space['consistent']:
        return False
    if not a_space['consistent']:
        return True
    return _included(a_space, b_rows, meter) and _included(b_space, a_rows, meter)


def equivalent_bases(rows_a, rows_b, n, *, meter):
    meter = _meter(meter)
    a = _equations(rows_a, n, meter)
    b = _equations(rows_b, n, meter)
    _, sa = _make_space(a, n, meter)
    _, sb = _make_space(b, n, meter)
    return _same_spaces(a, sa, b, sb, meter)


def _features(context, meter):
    meter.work(32)
    return tuple([1] + list(context) + [x*x % 26 for x in context]
                 + [context[i]*context[j] % 26 for i in range(6) for j in range(i+1, 6)]
                 + [int(context[i] == context[i+1]) for i in (0, 2, 4)])


def _normalise(contexts, observed, sparsity, allowed_features, meter):
    meter.work()
    require(type(contexts) in (list, tuple) and len(contexts) <= 128, 'bounded contexts required')
    normal = []
    for context in contexts:
        meter.work(7)
        require(type(context) in (list, tuple) and len(context) == 6
                and all(type(x) is int and 0 <= x < 26 for x in context), 'Z26 context required')
        normal.append(tuple(context))
    require(type(observed) is dict and len(observed) <= len(normal), 'observations dictionary')
    obs = {}
    for i, value in observed.items():
        meter.work(2)
        require(type(i) is int and 0 <= i < len(normal), 'observation index')
        require(type(value) is int and 0 <= value < 26, 'observation value')
        obs[i] = value
    require(type(sparsity) is int and 0 <= sparsity <= 3, 'sparsity in [0,3]')
    allowed = list(range(31)) if allowed_features is None else allowed_features
    require(type(allowed) in (list, tuple) and len(allowed) <= 31, 'allowed feature list')
    meter.work(len(allowed) + 1)
    require(all(type(j) is int and 0 <= j < 31 for j in allowed)
            and list(allowed) == sorted(set(allowed)), 'sorted unique allowed features')
    rows = [_features(context, meter) for context in normal]
    meter.work(len(normal)*6 + len(obs)*2 + len(allowed) + 1)
    identity = hashlib.sha256(json.dumps([VERSION, SOURCE_SHA256, COMPILER, normal,
        sorted(obs.items()), sparsity, allowed], separators=(',', ':')).encode()).hexdigest()
    return tuple(normal), obs, tuple(allowed), rows, identity


def _descriptor(theta, meter):
    meter.work(56)
    alpha = tuple(x % 13 for x in theta)
    beta = [0] * 25
    for j, x in enumerate(theta):
        beta[_group(j)] ^= x % 2
    return alpha, tuple(beta)


def _residual(alpha, beta, meter):
    meter.work(56)
    if not any(alpha[j] or beta[_group(j)] for j in (28, 29, 30)):
        return False
    if not any(beta[g] for g in range(2, 25)):
        return False
    for j in (28, 29, 30):
        meter.work(56)
        if (alpha[j] in (1, 12) and beta[_group(j)] == 1
                and all(alpha[k] == 0 for k in range(31) if k not in (0, j))
                and all(beta[g] == 0 for g in range(25) if g not in (0, _group(j)))):
            return False
    return True


def _minimum_support(alpha, beta, meter):
    meter.work(56)
    active = {_group(j) for j, x in enumerate(alpha) if x}
    return sum(x != 0 for x in alpha) + sum(beta[g] for g in range(25) if g not in active)


def _valid_descriptor(alpha, beta, meter):
    meter.work(58)
    require(type(alpha) in (list, tuple) and len(alpha) == 31
            and all(type(x) is int and 0 <= x < 13 for x in alpha), 'canonical alpha descriptor')
    require(type(beta) in (list, tuple) and len(beta) == 25
            and all(type(x) is int and x in (0, 1) for x in beta), 'canonical beta descriptor')


def residual(alpha, beta, *, meter):
    meter = _meter(meter)
    _valid_descriptor(alpha, beta, meter)
    return _residual(alpha, beta, meter)


def minimum_support(alpha, beta, *, meter):
    meter = _meter(meter)
    _valid_descriptor(alpha, beta, meter)
    return _minimum_support(alpha, beta, meter)


def _point(space, values, n, meter):
    meter.work(max(1, n*(len(values)+1)))
    return tuple((space['point'][j] + sum(t*v[j] for t, v in zip(values, space['basis']))) % 13
                 for j in range(n))


def _sat(equations, point, meter):
    for row in equations:
        if _dot(row[:-1], point, 13, meter) != row[-1]:
            return False
    return True


def _cut_member(forbidden, point, meter):
    return all(not _sat(system, point, meter) for system in forbidden)


def _keyed(mapping, modulus, meter):
    meter.work()
    require(type(mapping) is dict and len(mapping) <= modulus, 'bounded value dictionary')
    out = {}
    for key, value in mapping.items():
        meter.work(2)
        if type(key) is str:
            require(len(key) <= 2 and key.isdigit() and str(int(key)) == key,
                    'canonical decimal value key')
            key = int(key)
        require(type(key) is int and 0 <= key < modulus and key not in out,
                'duplicate or invalid value key')
        _record(meter)
        out[key] = value
    return out


def _mask(mask, modulus, meter):
    meter.work()
    require(type(mask) is list and len(mask) <= modulus, 'bounded mask list')
    meter.work(len(mask) + 1)
    require(all(type(x) is int and 0 <= x < modulus for x in mask)
            and mask == sorted(set(mask)), 'canonical sorted mask')
    _record(meter)
    return set(mask)


def _registry(result, allowed, sparsity, rows, meter):
    pieces = result.get('pieces')
    meter.work()
    require(type(pieces) is list and len(pieces) <= 40000, 'bounded producer piece list')
    registry = {}
    ids = {}
    for piece in pieces:
        meter.work()
        require(type(piece) is dict, 'piece dictionary')
        pid = piece.get('id')
        support = piece.get('support')
        beta = piece.get('beta')
        require(type(pid) is str and 1 <= len(pid) <= 100 and pid not in ids, 'unique piece id')
        require(type(support) is list and len(support) == min(sparsity, len(allowed)), 'piece support size')
        meter.work(len(support) + 1)
        require(all(type(j) is int and j in allowed for j in support)
                and support == sorted(set(support)), 'piece support domain')
        require(type(beta) is list and len(beta) <= len(support), 'piece beta size')
        meter.work(len(beta) + len(support) + 1)
        covered_groups = {_group(j) for j in support}
        require(all(type(g) is int and g in covered_groups for g in beta)
                and beta == sorted(set(beta)), 'piece beta coverage')
        key = (tuple(support), tuple(beta))
        require(key not in registry, 'duplicate support-beta piece')
        base = _equations(piece.get('base'), len(support), meter)
        forbidden = piece.get('forbidden')
        require(type(forbidden) in (list, tuple) and len(forbidden) <= 2, 'compiler cut-count contract')
        cuts = [_equations(w, len(support), meter) for w in forbidden]
        require(len(base) + sum(len(w) for w in cuts) <= 256, 'piece total equation bound')
        _record(meter, 2)
        registry[key] = (piece, base, cuts)
        ids[pid] = key
    return registry, ids


def _header(contexts, observed, sparsity, allowed, result, expected_source_sha256, meter):
    meter.work()
    require(type(expected_source_sha256) is str and len(expected_source_sha256) == 64
            and all(c in '0123456789abcdef' for c in expected_source_sha256), 'expected engine source pin')
    require(type(result) is dict, 'result dictionary')
    require(type(result.get('version')) is str and type(result.get('compiler')) is str
            and result['version'] == ENGINE_VERSION and result['compiler'] == COMPILER,
            'engine version/compiler mismatch')
    require(type(result.get('source_sha256')) is str and type(result.get('dependency_sha256')) is str
            and result['source_sha256'] == expected_source_sha256
            and result['dependency_sha256'] == DEPENDENCY_SHA256, 'engine source/dependency mismatch')
    meter.work(len(contexts)*6 + len(observed)*2 + len(allowed) + 1)
    identity = hashlib.sha256(json.dumps([ENGINE_VERSION, COMPILER, expected_source_sha256,
        DEPENDENCY_SHA256, contexts, sorted(observed.items()), sparsity, allowed],
        separators=(',', ':')).encode()).hexdigest()
    require(type(result.get('instance_sha256')) is str and result['instance_sha256'] == identity,
            'engine input identity mismatch')
    require(type(result.get('status')) is str and result['status'] in ('EXACT', 'EMPTY', 'INCOMPLETE'),
            'engine status')


def _reference(contexts, observed, sparsity, allowed, rows, identity, meter, registry=None):
    _record(meter, 5 + 2*len(rows))
    pieces, piece_masks, lifts, joints = {}, {}, {}, set()
    masks = [set() for _ in rows]
    provenance = [{} for _ in rows]
    stats = dict(supports=0, beta_candidates=0, eligible_beta=0, retained_points=0,
                 legacy_ambient_points_equivalent=0)
    n = min(sparsity, len(allowed))
    for support in combinations(allowed, n):
        meter.work(n + 1)
        stats['supports'] += 1
        groups = sorted({_group(j) for j in support})
        for size in range(len(groups)+1):
            for beta_active in combinations(groups, size):
                meter.work(len(beta_active) + 1)
                stats['beta_candidates'] += 1
                if not any(g not in (0, 1) for g in beta_active):
                    continue
                compatible = True
                for i, y in observed.items():
                    meter.work(len(beta_active) + 1)
                    if sum(rows[i][_representative(g)] for g in beta_active) % 2 != y % 2:
                        compatible = False
                        break
                if not compatible:
                    continue
                stats['eligible_beta'] += 1
                key = (support, beta_active)
                meter.work(len(observed)*(n+1) + 1)
                base = [[rows[i][j] % 13 for j in support] + [observed[i] % 13]
                        for i in sorted(observed)]
                binding = dict(request_sha256=identity, support=list(support), beta=list(beta_active),
                               role='observation', field=13, n=n, reference_version=VERSION,
                               reference_source_sha256=SOURCE_SHA256)
                _, space = _make_space(base, n, meter, binding)
                published = None if registry is None else registry.get(key)
                if not space['consistent']:
                    require(published is None, 'producer claims feasible inconsistent observation fiber')
                    continue
                if published is not None:
                    _, producer_base, cuts = published
                    p_binding = dict(binding, role='producer-base')
                    _, p_space = _make_space(producer_base, n, meter, p_binding)
                    require(_same_spaces(base, space, producer_base, p_space, meter),
                            'producer base is not equivalent to raw observation base')
                meter.work(25)
                beta = tuple(int(g in beta_active) for g in range(25))
                dimension = len(space['basis'])
                meter.preflight_fiber(13 ** dimension)
                for free_values in product(range(13), repeat=dimension):
                    meter.charge('fiber_points')
                    a = _point(space, free_values, n, meter)
                    meter.work(31+n)
                    alpha_list = [0]*31
                    for j, value in zip(support, a):
                        alpha_list[j] = value
                    alpha = tuple(alpha_list)
                    retained = _residual(alpha, beta, meter)
                    if published is not None:
                        require(retained == _cut_member(cuts, a, meter),
                                'canonical residual and producer cuts differ on observation fiber')
                    if not retained:
                        continue
                    if registry is not None:
                        require(published is not None, 'missing feasible support-beta piece')
                    stats['retained_points'] += 1
                    if key not in pieces:
                        _record(meter, 2+len(rows))
                        pieces[key] = set()
                        piece_masks[key] = [set() for _ in rows]
                    _add(pieces[key], a, meter, n)
                    prediction = []
                    for i, row in enumerate(rows):
                        meter.work(n + len(beta_active) + 2)
                        residue = _dot([row[j] for j in support], a, 13, meter)
                        parity = sum(row[_representative(g)] for g in beta_active) % 2
                        z = residue if residue % 2 == parity else residue + 13
                        prediction.append(z)
                        _add(masks[i], z, meter)
                        _add(piece_masks[key][i], z, meter)
                        if z not in provenance[i]:
                            _record(meter)
                            provenance[i][z] = set()
                        _add(provenance[i][z], key, meter, n+len(beta_active))
                    meter.work(len(rows))
                    _add(joints, tuple(prediction), meter, len(rows))
                    desc = (alpha, beta)
                    meter.work(56)
                    if desc not in lifts:
                        _record(meter)
                        lifts[desc] = set()
                    for assignment in product(range(2), repeat=n):
                        meter.charge('lift_trials')
                        meter.work(max(1, n*len(groups)))
                        if any(sum(bit for j, bit in zip(support, assignment) if _group(j) == g) % 2
                               != beta[g] for g in groups):
                            continue
                        meter.work(31+n)
                        theta = [0]*31
                        for j, value, parity in zip(support, a, assignment):
                            theta[j] = value if value % 2 == parity else value + 13
                        meter.work(31)
                        require(sum(x != 0 for x in theta) <= sparsity, 'reference lift support')
                        require(_descriptor(theta, meter) == desc, 'reference lift descriptor')
                        for i, y in observed.items():
                            require(_dot(theta, rows[i], 26, meter) == y, 'reference lift observations')
                        meter.work(31)
                        _add(lifts[desc], tuple(theta), meter, 31)
    if registry is not None:
        meter.work(len(registry) + len(pieces) + 1)
        require(set(registry) == set(pieces), 'extra/ineligible/empty producer piece')
    for support, _ in pieces:
        meter.work()
        stats['legacy_ambient_points_equivalent'] += 13 ** len(support)
    return dict(status='EXACT' if pieces else 'EMPTY', masks=masks, pieces=pieces,
                piece_masks=piece_masks, provenance=provenance, joints=joints, lifts=lifts,
                stats=stats)


def _core(piece, key, points, expected_masks, rows, meter):
    support, beta = key
    n = len(support)
    core = piece.get('core')
    meter.work()
    require(type(core) is dict and type(core.get('status')) is str and core['status'] == 'EXACT'
            and type(core.get('version')) is str and core['version'] == 'affine-filter-1',
            'feasible core status/version')
    meter.work(len(rows)*n + 1)
    scalars = [[row[j] % 13 for j in support] for row in rows]
    meter.work((len(piece['base']) + sum(len(w) for w in piece['forbidden'])) * (n+1))
    identity = hashlib.sha256(json.dumps(['affine-filter-1', 13, n, piece['base'],
        piece['forbidden'], scalars], separators=(',', ':')).encode()).hexdigest()
    require(type(core.get('instance_sha256')) is str and core['instance_sha256'] == identity,
            'core instance identity')
    require(type(core.get('masks')) is list and len(core['masks']) == len(rows), 'core mask rows')
    require(type(core.get('witnesses')) is list and len(core['witnesses']) == len(rows), 'core witness rows')

    def point_check(point):
        meter.charge('witness_checks')
        meter.work(n+1)
        require(type(point) in (list, tuple) and len(point) == n
                and all(type(x) is int and 0 <= x < 13 for x in point), 'core alpha witness shape')
        require(tuple(point) in points, 'core alpha outside complete residual fiber')

    for i in range(len(rows)):
        meter.work(len(expected_masks[i]) + 1)
        wanted = {z % 13 for z in expected_masks[i]}
        require(_mask(core['masks'][i], 13, meter) == wanted, 'incomplete core marginal mask')
        ws = _keyed(core['witnesses'][i], 13, meter)
        require(set(ws) == wanted, 'core witness coverage')
        for z, point in ws.items():
            point_check(point)
            require(_dot(scalars[i], point, 13, meter) == z, 'wrong core marginal witness')
    point_check(core.get('feasibility_witness'))


def _sparse_record(record, registry, ids, reference, rows, observed, sparsity, allowed,
                   meter, row_index=None, value=None, required_pid=None):
    meter.charge('witness_checks')
    meter.work()
    require(type(record) is dict, 'sparse witness record')
    pid = record.get('piece')
    require(type(pid) is str and 1 <= len(pid) <= 100 and pid in ids, 'sparse witness piece')
    if required_pid is not None:
        require(pid == required_pid, 'piece feasibility provenance')
    key = ids[pid]
    support, beta_active = key
    witness = record.get('theta')
    require(type(witness) in (list, tuple) and len(witness) <= sparsity, 'sparse witness size')
    meter.work(31)
    theta = [0]*31
    seen = []
    for pair in witness:
        meter.work(3)
        require(type(pair) in (list, tuple) and len(pair) == 2, 'sparse witness entry')
        j, coefficient = pair
        require(type(j) is int and j in allowed and j in support and j not in seen,
                'sparse witness original support')
        require(type(coefficient) is int and 1 <= coefficient < 26, 'sparse witness coefficient')
        theta[j] = coefficient
        seen.append(j)
    require(seen == sorted(seen), 'sparse witness ordering')
    alpha, beta = _descriptor(theta, meter)
    meter.work(25)
    require(tuple(g for g, bit in enumerate(beta) if bit) == beta_active, 'sparse witness beta')
    require(_residual(alpha, beta, meter), 'sparse witness outside R')
    require(_minimum_support(alpha, beta, meter) == len(seen), 'sparse witness not minimum support')
    meter.work(len(support) + 1)
    require(tuple(alpha[j] for j in support) in reference['pieces'][key], 'sparse witness outside piece')
    for i, y in observed.items():
        require(_dot(theta, rows[i], 26, meter) == y, 'sparse witness observation')
    if row_index is not None:
        require(_dot(theta, rows[row_index], 26, meter) == value, 'sparse witness marginal')


def _compare_expected(expected, reference, meter):
    require(type(expected) is dict, 'diagnostic expected memo must be a dictionary')
    # The memo never supplies a premise. Traverse reconstructed records to charge
    # comparisons, then require equality of every advertised semantic relation.
    def size(value):
        meter.work()
        if type(value) is dict:
            for k, v in value.items():
                size(k)
                size(v)
        elif type(value) in (list, tuple, set):
            for item in value:
                size(item)
    for field in ('status', 'masks', 'pieces', 'piece_masks', 'provenance', 'joints', 'lifts'):
        size(reference[field])
        require(field in expected and expected[field] == reference[field], 'diagnostic expected memo mismatch: '+field)


def _joint_claim(claim, reference, width, meter):
    meter.work()
    require(type(claim) is list and len(claim) <= 1_000_000,
            'optional joint claim must be a bounded JSON list')
    _record(meter)
    actual = set()
    for row in claim:
        meter.work(width+1)
        require(type(row) in (list, tuple) and len(row) == width
                and all(type(x) is int and 0 <= x < 26 for x in row), 'joint claim tuple domain')
        value = tuple(row)
        require(value not in actual, 'duplicate joint claim tuple')
        _add(actual, value, meter, width)
    meter.work(len(actual)*max(1, width) + 1)
    require(actual == reference['joints'], 'wrong advertised complete joint relation')


def _incomplete(status, meter, reason):
    return dict(version=VERSION, source_sha256=SOURCE_SHA256, status=status, reason=reason,
                masks=None, pieces=None, piece_masks=None, provenance=None, joints=None,
                lifts=None, witnesses=None, feasibility_witness=None, resources=meter.receipt())


def build_reference_v3(contexts, observed, sparsity=3, allowed_features=None, *, budget):
    meter = Meter(budget)
    try:
        contexts, observed, allowed, rows, identity = _normalise(
            contexts, observed, sparsity, allowed_features, meter)
        result = _reference(contexts, observed, sparsity, allowed, rows, identity, meter)
        meter.work()
        return dict(result, version=VERSION, source_sha256=SOURCE_SHA256,
                    request_sha256=identity, resources=meter.receipt())
    except ReferenceLimit as error:
        return _incomplete('INCOMPLETE', meter, str(error))


def verify_result_v3(contexts, observed, result, sparsity=3, allowed_features=None, *,
                     budget, expected_source_sha256, expected=None):
    meter = Meter(budget)
    try:
        contexts, observed, allowed, rows, identity = _normalise(
            contexts, observed, sparsity, allowed_features, meter)
        _header(contexts, observed, sparsity, allowed, result, expected_source_sha256, meter)
        if result['status'] == 'INCOMPLETE':
            for field in ('masks', 'witnesses', 'provenance', 'pieces', 'feasibility_witness'):
                meter.work()
                require(field in result and result[field] is None, 'producer INCOMPLETE leaks partial claims')
            for field in ('joints', 'piece_masks', 'lifts'):
                meter.work()
                require(field not in result or result[field] is None,
                        'producer INCOMPLETE leaks optional semantic claim: '+field)
            return _incomplete('PRODUCER_INCOMPLETE', meter, 'verified no-partial-claim format only')
        registry, ids = _registry(result, allowed, sparsity, rows, meter)
        reference = _reference(contexts, observed, sparsity, allowed, rows, identity, meter, registry)
        require(result['status'] == reference['status'], 'false exact/empty status')
        for field in ('masks', 'witnesses', 'provenance'):
            meter.work()
            require(type(result.get(field)) is list and len(result[field]) == len(rows), field+' row count')
        for key, (piece, _, _) in registry.items():
            _core(piece, key, reference['pieces'][key], reference['piece_masks'][key], rows, meter)
            _sparse_record(piece.get('feasibility_witness'), registry, ids, reference, rows,
                           observed, sparsity, allowed, meter, required_pid=piece['id'])
        for i in range(len(rows)):
            require(_mask(result['masks'][i], 26, meter) == reference['masks'][i], 'wrong complete Z26 mask')
            witnesses = _keyed(result['witnesses'][i], 26, meter)
            require(set(witnesses) == reference['masks'][i], 'top witness coverage')
            for z, record in witnesses.items():
                _sparse_record(record, registry, ids, reference, rows, observed, sparsity,
                               allowed, meter, row_index=i, value=z)
            provenance = _keyed(result['provenance'][i], 26, meter)
            require(set(provenance) == reference['masks'][i], 'provenance value coverage')
            for z, pids in provenance.items():
                meter.work()
                require(type(pids) is list and len(pids) <= len(ids), 'provenance list')
                meter.work(len(pids) + 1)
                require(all(type(pid) is str and 1 <= len(pid) <= 100 and pid in ids for pid in pids)
                        and len(pids) == len(set(pids)), 'provenance identifiers')
                require({ids[pid] for pid in pids} == reference['provenance'][i][z],
                        'incomplete or wrong cross-piece provenance')
        if result['status'] == 'EMPTY':
            require(result.get('feasibility_witness') is None, 'EMPTY feasibility witness')
        else:
            _sparse_record(result.get('feasibility_witness'), registry, ids, reference, rows,
                           observed, sparsity, allowed, meter)
        if expected is not None:
            _compare_expected(expected, reference, meter)
        meter.work()
        if 'joints' in result:
            _joint_claim(result['joints'], reference, len(rows), meter)
        meter.work(len(reference['lifts'])+1)
        return dict(version=VERSION, source_sha256=SOURCE_SHA256, request_sha256=identity,
                    status='VERIFIED_'+reference['status'], resources=meter.receipt(),
                    pieces_checked=len(reference['pieces']), canonical_functions=len(reference['lifts']),
                    original_lifts=sum(len(v) for v in reference['lifts'].values()),
                    joint_predictions=len(reference['joints']), stats=reference['stats'])
    except ReferenceLimit as error:
        return _incomplete('VERIFICATION_INCOMPLETE', meter, str(error))
