"""One exists-different query, certified independently of search heuristics."""
import time

from bounded_models import deadline_check
from gromark_alphabet import prepare, complete


def checked_maps(alphabet, edges, witness):
    pa, ca = witness['plain_alphabet'], witness['cipher_alphabet']
    if len(pa) != len(alphabet) or len(ca) != len(alphabet) or sorted(pa) != sorted(alphabet) or sorted(ca) != sorted(alphabet):
        raise ValueError('complete alphabet permutations required')
    p, c = ({letter: i for i, letter in enumerate(s)} for s in (pa, ca))
    if not all((c[b] - p[a]) % len(alphabet) == k for a, b, k in edges):
        raise ValueError('witness violates a base equation')
    return p, c


def check_counterexample(alphabet, edges, reference, witness, cipher, key):
    rp, rc = checked_maps(alphabet, edges, reference)
    p, c = checked_maps(alphabet, edges, witness)
    ref_letter = reference['plain_alphabet'][(rc[cipher] - key) % len(alphabet)]
    return (c[cipher] - p[ref_letter]) % len(alphabet) != key


class StateCap(Exception):
    pass


def difference(alphabet, edges, reference, cipher, key, pool=(), max_states=10000, limit=0.25):
    started = time.monotonic()
    graph = prepare(alphabet, edges)
    checked_maps(alphabet, edges, reference)
    if cipher not in alphabet or type(key) is not int or not 0 <= key < len(alphabet):
        raise ValueError('literal target cipher symbol and modular key required')
    if type(max_states) is not int or max_states < 0:
        raise ValueError('nonnegative integer state cap required')
    if not graph['local_filter_passed']:
        raise ValueError('reference graph must be consistent')
    m = len(alphabet)
    ref_letter = reference['plain_alphabet'][(reference['cipher_alphabet'].index(cipher) - key) % m]
    result = {'classification': 'unresolved', 'search_states': 0,
              'selected_translation_trials': 0, 'translation_domain_checks': 0,
              'exact_search_invoked': False, 'counterexample': None}
    def variable(witness, kind, certificate):
        deadline_check(started, limit)
        assert check_counterexample(alphabet, edges, reference, witness, cipher, key)
        deadline_check(started, limit)
        return {**result, 'classification': 'variable', 'method': kind, 'certificate': certificate,
                'counterexample': {'plain_alphabet': witness['plain_alphabet'],
                                   'cipher_alphabet': witness['cipher_alphabet']},
                'independent_equation_and_difference_check': True}
    try:
        deadline_check(started, limit)
        seen_p, seen_c = {a for a, _, _ in edges}, {b for _, b, _ in edges}
        for side, symbol, unseen in [('P', ref_letter, sorted(set(alphabet) - seen_p)),
                                      ('C', cipher, sorted(set(alphabet) - seen_c))]:
            if symbol not in unseen or len(unseen) < 2:
                continue
            other = next(letter for letter in unseen if letter != symbol)
            field = 'plain_alphabet' if side == 'P' else 'cipher_alphabet'
            values = list(reference[field])
            a, b = values.index(symbol), values.index(other)
            values[a], values[b] = values[b], values[a]
            witness = dict(reference)
            witness[field] = ''.join(values)
            return variable(witness, 'unused_plaintext_swap' if side == 'P' else 'unused_ciphertext_swap',
                            {'side': side, 'swapped_coordinates_zero_based': [a, b],
                             'both_labels_absent_from_base_side': True})
        components = [{**c, 'relative_potentials': dict(c['relative_potentials'])} for c in graph['components']]
        membership = {node: i for i, comp in enumerate(components) for node in comp['relative_potentials']}
        pn, cn = 'P:' + ref_letter, 'C:' + cipher
        if pn in membership and cn in membership and membership[pn] == membership[cn]:
            comp = components[membership[pn]]
            pv, cv = comp['relative_potentials'][pn], comp['relative_potentials'][cn]
            assert (cv - pv) % m == key
            deadline_check(started, limit)
            return {**result, 'classification': 'forced', 'model_conditional_letter': ref_letter,
                    'method': 'same_component_invariant', 'certificate': {'root': comp['root'],
                        'plain_node': pn, 'cipher_node': cn, 'plain_potential': pv,
                        'cipher_potential': cv, 'difference_modulus': (cv - pv) % m,
                        'target_key': key, 'proof_complete': True}}
        for entry in pool:
            deadline_check(started, limit)
            checked_maps(alphabet, edges, entry)
            if check_counterexample(alphabet, edges, reference, entry, cipher, key):
                return variable(entry, 'supplied_complete_certificate', {'source_id': entry['id']})
        result['exact_search_invoked'] = True
        for node in sorted(set((pn, cn)) - set(membership)):
            membership[node] = len(components)
            components.append({'root': node, 'relative_potentials': {node: 0}, 'observed_node_count': 1})
        graph = {**graph, 'components': components}
        pi, ci = membership[pn], membership[cn]
        pv, cv = components[pi]['relative_potentials'][pn], components[ci]['relative_potentials'][cn]
        assigned = {0: 0}
        domains = []
        for comp in components:
            pvalues = [v for n, v in comp['relative_potentials'].items() if n[0] == 'P']
            cvalues = [v for n, v in comp['relative_potentials'].items() if n[0] == 'C']
            domains.append([(sum(1 << ((v + t) % m) for v in pvalues),
                             sum(1 << ((v + t) % m) for v in cvalues)) for t in range(m)])
        def inequality_ok():
            return pi not in assigned or ci not in assigned or (cv + assigned[ci] - pv - assigned[pi]) % m != key
        def visit(remaining, used_p, used_c):
            deadline_check(started, limit)
            if result['search_states'] >= max_states:
                raise StateCap()
            result['search_states'] += 1
            if not inequality_ok():
                return None
            if not remaining:
                return dict(assigned)
            choices = []
            for i in remaining:
                legal = []
                for t, (pm, cm) in enumerate(domains[i]):
                    result['translation_domain_checks'] += 1
                    if pm & used_p or cm & used_c:
                        continue
                    assigned[i] = t
                    if inequality_ok():
                        legal.append(t)
                    del assigned[i]
                if not legal:
                    return None
                choices.append((len(legal), -components[i]['observed_node_count'], components[i]['root'], i, legal))
            _, _, _, i, legal = min(choices)
            for t in legal:
                result['selected_translation_trials'] += 1
                assigned[i] = t
                pm, cm = domains[i][t]
                answer = visit(tuple(j for j in remaining if j != i), used_p | pm, used_c | cm)
                if answer is not None:
                    return answer
                del assigned[i]
            return None
        answer = visit(tuple(range(1, len(components))), *domains[0][0])
        if answer is not None:
            witness = complete(alphabet, graph, answer)
            return variable(witness, 'exact_difference_CSP_witness',
                            {'component_roots': [c['root'] for c in components],
                             'offsets': [answer[i] for i in range(len(components))]})
        deadline_check(started, limit)
        return {**result, 'classification': 'forced', 'model_conditional_letter': ref_letter,
                'method': 'exhausted_difference_CSP', 'certificate': {
                    'component_roots': [c['root'] for c in components],
                    'root_potential_zero': True, 'first_component_offset_zero': True,
                    'all_other_offsets_exhausted': True, 'missing_endpoints_included': True,
                    'proof_complete': True}}
    except StateCap:
        return {**result, 'method': 'unresolved', 'reason': 'per_query_state_cap'}
    except TimeoutError:
        return {**result, 'method': 'unresolved', 'reason': 'per_query_time_cap'}
