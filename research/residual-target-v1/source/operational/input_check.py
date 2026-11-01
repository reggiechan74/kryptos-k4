"""Independent raw-input and common-law interpretation checks.

Source only until the separately approved invocation. This module has no
imports, file access, target literals, top-level calculations or CLI. It never
calls producer/reference feature, descriptor, lift or solver helpers.
"""

ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


def require(condition, message):
    if not condition:
        raise ValueError(message)


def _raw(raw, internal_id):
    require(type(internal_id) is str and internal_id in ('v000', 'v001', 'v002'),
            'independent scheduled internal ID')
    require(type(raw) is dict and set(raw) == {'ciphertext', 'length', 'indexing', 'cribs'},
            'independent raw schema')
    require(type(raw['length']) is int and raw['length'] == 97, 'independent exact length')
    require(type(raw['indexing']) is str and raw['indexing'] == 'one-based inclusive',
            'independent indexing convention')
    text = raw['ciphertext']
    require(type(text) is str and len(text) == 97 and all('A' <= c <= 'Z' for c in text),
            'independent raw uppercase ciphertext')
    blocks = raw['cribs']
    require(type(blocks) is list and len(blocks) == 2, 'independent two crib blocks')
    for ordinal, interval in enumerate(((22, 34), (64, 74))):
        block = blocks[ordinal]
        require(type(block) is dict and set(block) == {'start', 'end', 'plaintext'},
                'independent crib schema')
        require(type(block['start']) is int and type(block['end']) is int
                and (block['start'], block['end']) == interval, 'independent exact crib interval')
        word = block['plaintext']
        require(type(word) is str and len(word) == interval[1] - interval[0] + 1
                and all('A' <= c <= 'Z' for c in word), 'independent uppercase crib')
    if internal_id == 'v002':
        require(blocks[0]['plaintext'] == 'EASTNORTHEAST'
                and blocks[1]['plaintext'] == 'BERLINCLOCK', 'independent target crib literals')
    return text, blocks


def convert_raw_independent(raw, internal_id):
    """Window-slice conversion independent of the worker's index-lag converter."""
    text, blocks = _raw(raw, internal_id)
    contexts = []
    for beginning in range(91):
        preceding = text[beginning:beginning + 6]
        contexts.append([ord(symbol) - ord('A') for symbol in preceding[::-1]])
    observed = []
    for block in blocks:
        for offset, plain in enumerate(block['plaintext']):
            position = block['start'] - 1 + offset
            response = (ord(text[position]) - ord(plain)) % 26
            observed.append([position - 6, response])
    return {'id': internal_id, 'contexts': contexts, 'observed': observed,
            'sparsity': 3, 'allowed_features': list(range(31))}


def _theta(record):
    require(type(record) is dict and set(record) == {'piece', 'theta'},
            'independent feasibility witness schema')
    require(type(record['piece']) is str and 1 <= len(record['piece']) <= 100,
            'independent piece identity')
    sparse = record['theta']
    require(type(sparse) is list and 1 <= len(sparse) <= 3, 'independent original sparse support')
    coefficients = [0] * 31
    previous = -1
    for entry in sparse:
        require(type(entry) is list and len(entry) == 2, 'independent coefficient pair')
        index, value = entry
        require(type(index) is int and previous < index < 31,
                'independent distinct ordered original coordinates')
        require(type(value) is int and 1 <= value <= 25, 'independent nonzero Z26 coefficient')
        coefficients[index] = value
        previous = index
    alpha = [coefficient % 13 for coefficient in coefficients]
    beta = [coefficients[0] % 2]
    for lag in range(1, 7):
        beta.append((coefficients[lag] + coefficients[lag + 6]) % 2)
    beta.extend(coefficient % 2 for coefficient in coefficients[13:])
    require(any(alpha[28:]) or any(beta[22:]), 'independent essential full equality')
    require(any(beta[2:]), 'independent B exclusion')
    for equality in range(3):
        q, group = 28 + equality, 22 + equality
        old_carry = (alpha[q] in (1, 12) and beta[group] == 1
                     and all(value == 0 for index, value in enumerate(alpha)
                             if index != 0 and index != q)
                     and all(value == 0 for index, value in enumerate(beta)
                             if index != 0 and index != group))
        require(not old_carry, 'independent C exclusion')
    minimum = int(alpha[0] != 0 or beta[0] != 0)
    for lag in range(1, 7):
        nonzero = int(alpha[lag] != 0) + int(alpha[lag + 6] != 0)
        minimum += nonzero if nonzero else beta[lag]
    for coordinate in range(13, 31):
        minimum += int(alpha[coordinate] != 0 or beta[coordinate - 6] != 0)
    require(minimum == len(sparse) <= 3, 'independent minimum original-support lift')
    return sparse


def _raw_function_values(ciphertext, sparse):
    """Evaluate original-coordinate features directly on the raw six letters."""
    values = []
    for position in range(6, 97):
        history = tuple(ord(ciphertext[position - lag]) - 65 for lag in range(1, 7))
        total = 0
        for coordinate, coefficient in sparse:
            if coordinate == 0:
                feature = 1
            elif coordinate <= 6:
                feature = history[coordinate - 1]
            elif coordinate <= 12:
                letter = history[coordinate - 7]
                feature = letter * letter
            elif coordinate <= 27:
                index = 13
                feature = None
                for left in range(6):
                    for right in range(left + 1, 6):
                        if index == coordinate:
                            feature = history[left] * history[right]
                        index += 1
                require(feature is not None, 'independent product coordinate')
            else:
                left = 2 * (coordinate - 28)
                feature = int(history[left] == history[left + 1])
            total += coefficient * feature
        values.append(total % 26)
    return values


def interpret_verified(raw, instance, producer_result, verified):
    """Called only after complete reference verification; does not prove completeness."""
    require(type(instance) is dict and type(instance.get('id')) is str, 'independent instance')
    independently_converted = convert_raw_independent(raw, instance['id'])
    require(instance == independently_converted, 'independent raw instance mismatch')
    require(type(producer_result) is dict and type(verified) is dict, 'verified result objects')
    status = producer_result.get('status')
    require((status, verified.get('status')) in
            (('EXACT', 'VERIFIED_EXACT'), ('EMPTY', 'VERIFIED_EMPTY')),
            'independent matching complete status pair')
    count_names = ('pieces_checked', 'canonical_functions', 'original_lifts', 'joint_predictions')
    for name in count_names:
        require(type(verified.get(name)) is int and verified[name] >= 0,
                'independent exact count: ' + name)
    for name in ('masks', 'witnesses', 'provenance'):
        require(type(producer_result.get(name)) is list and len(producer_result[name]) == 91,
                'independent complete row shape: ' + name)
    require(type(producer_result.get('pieces')) is list
            and len(producer_result['pieces']) == verified['pieces_checked'],
            'independent piece count')
    if status == 'EMPTY':
        require(all(verified[name] == 0 for name in count_names), 'independent zero relation counts')
        require(producer_result['pieces'] == [] and producer_result.get('feasibility_witness') is None,
                'independent empty pieces/witness')
        require(all(type(mask) is list and mask == [] for mask in producer_result['masks']),
                'independent empty masks')
        require(all(type(row) is dict and row == {} for row in producer_result['witnesses'])
                and all(type(row) is dict and row == {} for row in producer_result['provenance']),
                'independent empty witness/provenance coverage')
        return {'classification': 'EMPTY', 'plaintext_masks': [[] for _ in range(91)],
                'example_plaintext_tail': None, 'first_six_claimed': False}
    require(all(verified[name] >= 1 for name in count_names), 'independent nonempty relation counts')
    text = raw['ciphertext']
    plaintext_masks = []
    for row, mask in enumerate(producer_result['masks']):
        require(type(mask) is list and 1 <= len(mask) <= 26
                and all(type(value) is int and 0 <= value <= 25 for value in mask)
                and mask == sorted(set(mask)), 'independent canonical function mask')
        current = ord(text[row + 6]) - 65
        plaintext_masks.append(sorted(ALPHABET[(current - value) % 26] for value in mask))
    sparse = _theta(producer_result.get('feasibility_witness'))
    function_values = _raw_function_values(text, sparse)
    require(all(function_values[row] == value for row, value in instance['observed']),
            'independent common law violates observation')
    require(all(value in producer_result['masks'][row] for row, value in enumerate(function_values)),
            'independent common law outside verified mask')
    plaintext = ''.join(ALPHABET[(ord(text[row + 6]) - 65 - value) % 26]
                        for row, value in enumerate(function_values))
    require(len(plaintext) == 91, 'independent modeled tail only')
    for row, value in enumerate(function_values):
        require((ord(plaintext[row]) - 65 + value) % 26 == ord(text[row + 6]) - 65,
                'independent forward tail check')
    if verified['joint_predictions'] == 1:
        require(all(len(mask) == 1 for mask in producer_result['masks']),
                'independent singleton joint/mask mismatch')
        classification = 'CONDITIONAL_SINGLETON_TAIL'
    else:
        require(any(len(mask) > 1 for mask in producer_result['masks']),
                'independent ambiguous joint/mask mismatch')
        classification = 'NONEMPTY_AMBIGUOUS'
    return {'classification': classification, 'plaintext_masks': plaintext_masks,
            'example_plaintext_tail': plaintext, 'first_six_claimed': False}


def verify_control_expectations(raw, instance, result, verified, interpretation, expected, preflight):
    """Compare disclosed expectations after the same complete scientific path."""
    require(type(expected) is dict and expected.get('schema') == 'k4-residual-disclosed-expectation-v1',
            'disclosed expectation schema')
    require(expected.get('kind') in ('positive', 'empty')
            and expected.get('internal_id') == instance['id'], 'disclosed control identity')
    require(instance['contexts'] == expected['expected_contexts']
            and instance['observed'] == expected['expected_observed'], 'disclosed converter expectation')
    require(preflight.get('status') == 'WORKLOAD_ADMITTED' and preflight.get('checked_supports') == 4495
            and type(preflight.get('exact_W')) is int
            and preflight['exact_W'] == expected['expected_preflight_W'], 'disclosed complete preflight')
    require(result.get('status') == expected['expected_producer_status']
            and verified.get('status') == expected['expected_reference_status'], 'disclosed status outcome')
    require(interpretation['classification'] == expected['expected_classification']
            and interpretation['first_six_claimed'] is False, 'disclosed interpretation outcome')
    counts = expected['expected_counts']
    require(len(result['pieces']) == counts['pieces']
            and verified['pieces_checked'] == counts['pieces']
            and all(verified[name] == counts[name]
                    for name in ('canonical_functions', 'original_lifts', 'joint_predictions')),
            'disclosed full relation counts')
    if expected['kind'] == 'positive':
        require(result['masks'] == [[value] for value in expected['expected_function_outputs']],
                'disclosed function/key output masks')
        require(result['feasibility_witness']['theta'] == expected['expected_original_coefficients'],
                'disclosed original law')
        require(interpretation['example_plaintext_tail'] == expected['expected_plaintext_tail']
                and interpretation['plaintext_masks'] == [[letter] for letter in expected['expected_plaintext_tail']],
                'disclosed plaintext output distinct from function output')
    else:
        require(expected['expected_function_outputs'] is None
                and expected['expected_plaintext_tail'] is None
                and expected['expected_original_coefficients'] is None
                and interpretation['example_plaintext_tail'] is None, 'disclosed empty nonvacuity')
    return True
