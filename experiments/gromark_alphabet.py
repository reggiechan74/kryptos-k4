"""Component-offset packing for two complete modular alphabet bijections."""
import time
from bounded_models import deadline_check


def expand(base, primer, lags, length):
    if (type(base) is not int or not 2 <= base <= 26 or not primer
            or any(type(d) is not int or not 0 <= d < base for d in primer)
            or len(lags) != 2 or any(type(k) is not int or not 1 <= k <= len(primer) for k in lags)
            or lags[0] >= lags[1] or type(length) is not int or length < len(primer)):
        raise ValueError('explicit valid base/primer/two lags/length required')
    digits = list(primer)
    for i in range(len(primer), length):
        digits.append((digits[i - lags[0]] + digits[i - lags[1]]) % base)
    return digits


def prepare(alphabet, edges):
    if not isinstance(alphabet, str) or not 2 <= len(alphabet) <= 26 or len(set(alphabet)) != len(alphabet):
        raise ValueError('two to26 distinct alphabet symbols required')
    m = len(alphabet)
    adjacency = {}
    for index, edge in enumerate(edges):
        if (len(edge) != 3 or edge[0] not in alphabet or edge[1] not in alphabet
                or type(edge[2]) is not int or not 0 <= edge[2] < m):
            raise ValueError('literal alphabet edges with modular integer offsets required')
        p, c, key = edge
        left, right = ('P', p), ('C', c)
        adjacency.setdefault(left, []).append((right, key, index))
        adjacency.setdefault(right, []).append((left, -key % m, index))
    potential = {}
    components = []
    first_cycle = None
    first_collision = None
    for root in sorted(adjacency):
        if root in potential:
            continue
        potential[root] = 0
        queue = [root]
        nodes = []
        while queue:
            node = queue.pop(0)
            nodes.append(node)
            for target, offset, edge_index in sorted(adjacency[node]):
                expected = (potential[node] + offset) % m
                if target not in potential:
                    potential[target] = expected
                    queue.append(target)
                elif potential[target] != expected and first_cycle is None:
                    first_cycle = {'edge_index_zero_based': edge_index,
                                   'from_node': ':'.join(node), 'to_node': ':'.join(target),
                                   'assigned_value': potential[target], 'required_value': expected}
        relative = {':'.join(node): potential[node] for node in sorted(nodes)}
        for side in ('P', 'C'):
            seen = {}
            for node in sorted(nodes):
                if node[0] != side:
                    continue
                value = potential[node]
                if value in seen and first_collision is None:
                    first_collision = {'nodes': [seen[value], ':'.join(node)], 'relative_value': value}
                seen[value] = ':'.join(node)
        components.append({'root': ':'.join(root), 'relative_potentials': relative,
                           'observed_node_count': len(nodes)})
    return {'modulus': m, 'observed_nodes': len(adjacency), 'edges': len(edges),
            'components': components, 'component_count': len(components),
            'local_filter_passed': first_cycle is None and first_collision is None,
            'first_cycle_conflict': first_cycle, 'first_same_side_collision': first_collision}


def complete(alphabet, graph, offsets):
    m = len(alphabet)
    maps = {'P': {}, 'C': {}}
    for index, component in enumerate(graph['components']):
        for node, value in component['relative_potentials'].items():
            maps[node[0]][node[2:]] = (value + offsets[index]) % m
    observed = {side: dict(values) for side, values in maps.items()}
    strings = {}
    for side in ('P', 'C'):
        unused = iter(sorted(set(range(m)) - set(maps[side].values())))
        for letter in sorted(alphabet):
            if letter not in maps[side]:
                maps[side][letter] = next(unused)
        assert len(set(maps[side].values())) == m
        strings[side] = ''.join(sorted(alphabet, key=maps[side].get))
    return {'plain_alphabet': strings['P'], 'cipher_alphabet': strings['C'],
            'observed_plain_values': observed['P'], 'observed_cipher_values': observed['C'],
            'completion': 'unobserved letters alphabetical into unused coordinates ascending'}


def verify(alphabet, edges, plain_alphabet, cipher_alphabet):
    m = len(alphabet)
    if (len(plain_alphabet) != m or len(cipher_alphabet) != m
            or set(plain_alphabet) != set(alphabet) or set(cipher_alphabet) != set(alphabet)):
        return False
    return all((cipher_alphabet.index(c) - plain_alphabet.index(p)) % m == key for p, c, key in edges)


class StateCap(Exception):
    pass


def solve(alphabet, edges, max_states=100000, limit=10):
    started = time.monotonic()
    deadline_check(started, limit)
    if type(max_states) is not int or max_states < 0:
        raise ValueError('nonnegative integer state cap required')
    graph = prepare(alphabet, edges)
    result = {'graph': graph, 'search_states': 0, 'candidate_offset_trials': 0,
              'translation_domain_checks': 0, 'gauge': 'component0 translation0 if any observed component',
              'exhausted': False, 'witness': None}
    if not graph['local_filter_passed']:
        result.update(feasibility='unsatisfiable', reason='local_filter_rejected', exhausted=True)
        return result
    m = len(alphabet)
    domains = []
    for component in graph['components']:
        by_side = [[value for node, value in component['relative_potentials'].items() if node[0] == side]
                   for side in ('P', 'C')]
        domains.append([(sum(1 << ((value + t) % m) for value in by_side[0]),
                         sum(1 << ((value + t) % m) for value in by_side[1])) for t in range(m)])
    assigned = {0: 0} if domains else {}
    def visit(remaining, used_p, used_c):
        deadline_check(started, limit)
        if result['search_states'] >= max_states:
            raise StateCap()
        result['search_states'] += 1
        if not remaining:
            return dict(assigned)
        choices = []
        for index in remaining:
            legal = []
            for shift, (pmask, cmask) in enumerate(domains[index]):
                result['translation_domain_checks'] += 1
                if not (pmask & used_p or cmask & used_c):
                    legal.append(shift)
            if not legal:
                return None
            component = graph['components'][index]
            choices.append((len(legal), -component['observed_node_count'], component['root'], index, legal))
        _, _, _, index, legal = min(choices)
        rest = tuple(i for i in remaining if i != index)
        for shift in legal:
            result['candidate_offset_trials'] += 1
            assigned[index] = shift
            pmask, cmask = domains[index][shift]
            answer = visit(rest, used_p | pmask, used_c | cmask)
            if answer is not None:
                return answer
            del assigned[index]
        return None
    try:
        masks = domains[0][0] if domains else (0, 0)
        answer = visit(tuple(range(1, len(domains))), *masks)
    except StateCap:
        result.update(feasibility='unresolved', reason='state_cap_reached')
        return result
    if answer is None:
        result.update(feasibility='unsatisfiable', reason='global_offsets_exhausted', exhausted=True)
    else:
        witness = complete(alphabet, graph, answer)
        assert verify(alphabet, edges, witness['plain_alphabet'], witness['cipher_alphabet'])
        witness['component_offsets'] = [{'root': c['root'], 'offset': answer[i]}
                                        for i, c in enumerate(graph['components'])]
        result.update(feasibility='satisfiable', reason='complete_bijection_witness', witness=witness)
    deadline_check(started, limit)
    return result


def encrypt(plain, stream, plain_alphabet, cipher_alphabet):
    if len(plain) != len(stream):
        raise ValueError('explicit full stream required')
    return ''.join(cipher_alphabet[(plain_alphabet.index(p) + key) % len(plain_alphabet)]
                   for p, key in zip(plain, stream))


def decrypt(cipher, stream, plain_alphabet, cipher_alphabet):
    if len(cipher) != len(stream):
        raise ValueError('explicit full stream required')
    return ''.join(plain_alphabet[(cipher_alphabet.index(c) - key) % len(plain_alphabet)]
                   for c, key in zip(cipher, stream))
