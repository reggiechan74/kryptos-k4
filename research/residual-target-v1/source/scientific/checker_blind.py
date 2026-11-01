"""Independent serialized blind full31 workload checker; source-only until freeze.

No author preflight helpers are imported. Original dictionary values, input
semantics, beta lists, support order, cumulative bounds and byte hashes are
reconstructed here. The previously audited immutable v3 checker performs the
second F13 transcript replay; no additional solve or third replay is hidden.
"""
import hashlib
from itertools import combinations, product
import json

SCHEMA = 'fresh-residual-workload-evidence-v2'
REFERENCE_SHA256 = '0730f8b0a26109919ba6eb558be18063d137ced233b397cd188dc261a13fe8f9'
CONTROL_KEYS = {'id','contexts','observed','sparsity','allowed_features'}
HEADER_KEYS = {'kind','schema','case_id','input_sha256','public_sha256',
               'point_cap','sparsity','allowed_features','reference_sha256','freeze_sha256'}
SUPPORT_KEYS = {'kind','index','support','input_sha256','certificate','beta_groups',
                'compatible_betas','term','prefix_lower_bound'}
TERMINAL_KEYS = {'kind','status','support_count','lower_bound','exact_W','content_sha256'}


class CheckerError(ValueError):
    pass


def require(ok, message):
    if not ok:
        raise CheckerError(message)


def canonical_bytes(value):
    return (json.dumps(value,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()


def digest_string(value):
    return type(value) is str and len(value) == 64 and all(x in '0123456789abcdef' for x in value)


def _unique(pairs):
    result = {}
    for key,value in pairs:
        require(key not in result,'duplicate JSON key')
        result[key] = value
    return result


def _nonfinite(_value):
    raise CheckerError('nonfinite JSON number')


def parse_canonical_line(raw, meter):
    require(type(raw) is bytes,'exact evidence bytes required')
    if len(raw) > meter.caps.max_line_bytes:
        raise CheckerError('evidence line exceeds frozen byte bound')
    # Explicit units: parse, canonical re-encode and hash each cost one
    # conservative 64-byte block. Charge before any of those operations.
    meter.work(3*max(1,(len(raw)+63)//64))
    meter.record()
    require(raw.endswith(b'\n') and raw.count(b'\n') == 1,'one LF-terminated JSON record')
    try:
        obj = json.loads(raw,object_pairs_hook=_unique,parse_constant=_nonfinite)
    except (UnicodeError,json.JSONDecodeError) as error:
        raise CheckerError('invalid evidence JSON') from error
    require(type(obj) is dict,'evidence record object')
    require(canonical_bytes(obj) == raw,'noncanonical JSON bytes')
    return obj


def _features(context,meter):
    meter.work(32)
    row = [1]
    row.extend(context)
    row.extend(value*value % 26 for value in context)
    for left in range(6):
        for right in range(left+1,6):
            row.append(context[left]*context[right] % 26)
    for left in (0,2,4):
        row.append(1 if context[left] == context[left+1] else 0)
    return tuple(row)


def _group(j):
    return j if j < 7 else j-6


def _control(control,meter):
    meter.work()
    require(type(control) is dict and set(control) == CONTROL_KEYS,'independent control schema')
    identity=control['id']
    require(type(identity) is str and identity in ('G0','G1')+tuple('v%03d'%i for i in range(12)),'case identity')
    gate=identity in ('G0','G1')
    require(type(control['sparsity']) is int and control['sparsity']==3,'original sparsity')
    require(type(control['allowed_features']) is list and len(control['allowed_features'])==31
            and all(type(j) is int for j in control['allowed_features'])
            and control['allowed_features']==list(range(31)),'all original indices')
    lengths = dict(contexts=1 if gate else 91,observed=0 if identity=='G0' else 1 if identity=='G1' else 24)
    for field,length in lengths.items():
        meter.work()
        require(type(control[field]) is list and len(control[field]) == length,'control size: '+field)
    for context in control['contexts']:
        meter.work(7)
        require(type(context) is list and len(context) == 6
                and all(type(v) is int and 0 <= v < 26 for v in context),'original Z26 context')
    last=-1
    for pair in control['observed']:
        meter.work(3)
        require(type(pair) is list and len(pair) == 2
                and all(type(v) is int for v in pair),'observation pair types')
        i,y=pair
        require(last<i<len(control['contexts']) and 0<=y<26,'observation indices/residues')
        last=i
    if gate:
        require(control['contexts'] == [[0,0,0,0,0,0]],'literal gate context')
        require(control['observed']==([] if identity=='G0' else [[0,0]]),'literal gate observations')
    else:
        require([pair[0] for pair in control['observed']]==list(range(15,28))+list(range(57,68)),
                'fixed public position pattern')
        for row in range(1,91):
            meter.work(5)
            require(control['contexts'][row][1:]==control['contexts'][row-1][:5],
                    'independent contiguous context binding')
    rows = tuple(_features(context,meter) for context in control['contexts'])
    # Maximum supported blind instance is well under16KiB. A fixed upper
    # allowance debits serialization+hash before constructing its byte string.
    meter.work(2*256)
    encoded = canonical_bytes(control)
    require(len(encoded) <= 16384,'bounded literal control bytes')
    return rows,hashlib.sha256(encoded).hexdigest()


class EvidenceChecker:
    """One ordered evidence stream and one shared, already validated Meter.

    consume() is called on exact written/read-back bytes, once per line. No
    author-provided cursor, running sum, digest, matrix or beta count is trusted.
    This class deliberately provides no admission from incomplete evidence.
    """
    def __init__(self,control,public_sha256,reference_sha256,freeze_sha256,reference,meter,point_cap=1000000):
        require(type(point_cap) is int and point_cap >= 0,'built-in point cap')
        require(point_cap == meter.caps.point_cap,'checker/meter point-cap identity')
        require(digest_string(public_sha256) and digest_string(freeze_sha256),'public/freeze source pins')
        require(reference_sha256 == REFERENCE_SHA256 and type(reference_sha256) is str,
                'fixed reference source pin')
        require(reference.SOURCE_SHA256 == REFERENCE_SHA256,'loaded reference identity')
        self.reference,self.meter = reference,meter
        self.rows,self.input_sha256 = _control(control,meter)
        meter.work(1+3*len(control['observed']))
        self.control = dict(id=control['id'],observed=tuple((i,y) for i,y in control['observed']))
        self.public_sha256,self.reference_sha256,self.freeze_sha256 = public_sha256,reference_sha256,freeze_sha256
        self.point_cap = point_cap
        self.supports = iter(combinations(range(31),3))
        self.checked_supports = 0
        self.lower_bound = 0
        self.header_seen = False
        self.terminal_seen = False
        self.failed = False
        self.content_hash = hashlib.sha256()
        self.byte_count = 0
        self.status = None
        self.exact_W = None

    def _header(self,record):
        self.meter.work(40)
        require(set(record) == HEADER_KEYS,'header exact schema')
        require(type(record['point_cap']) is int and type(record['sparsity']) is int,'header integer types')
        require(type(record['allowed_features']) is list and len(record['allowed_features']) == 31
                and all(type(x) is int for x in record['allowed_features']),'header original indices')
        wanted = dict(kind='header',schema=SCHEMA,case_id=self.control['id'],
            input_sha256=self.input_sha256,public_sha256=self.public_sha256,
            point_cap=self.point_cap,sparsity=3,allowed_features=list(range(31)),
            reference_sha256=self.reference_sha256,freeze_sha256=self.freeze_sha256)
        require(record == wanted,'header literal identity')
        self.header_seen = True
        return dict(kind='header',input_sha256=self.input_sha256)

    def _support(self,record):
        meter = self.meter
        meter.work(12)
        require(set(record) == SUPPORT_KEYS,'support exact schema')
        require(self.lower_bound <= self.point_cap,'support after first strict cap crossing')
        require(self.checked_supports < 4495,'extra support')
        require(type(record['index']) is int and record['index'] == self.checked_supports,'support index')
        support = next(self.supports)
        require(type(record['support']) is list and len(record['support']) == 3
                and all(type(j) is int for j in record['support'])
                and record['support'] == list(support),'exact original lexicographic support')
        require(type(record['input_sha256']) is str and record['input_sha256'] == self.input_sha256,
                'support input binding')
        meter.work(1+4*len(self.control['observed']))
        equations = [[self.rows[i][j] % 13 for j in support]+[value % 13]
                     for i,value in self.control['observed']]
        binding = dict(role='fresh-residual-workload-v2',field=13,n=3,input_sha256=self.input_sha256,
                       support=list(support),case_id=self.control['id'],reference_version=self.reference.VERSION)
        proof = self.reference.replay_certificate(equations,3,record['certificate'],meter=meter.ref,binding=binding)
        meter.work(7)
        groups = sorted(set(_group(j) for j in support))
        require(type(record['beta_groups']) is list and len(record['beta_groups']) <= 3
                and all(type(g) is int for g in record['beta_groups'])
                and record['beta_groups'] == groups,'covered canonical beta groups')
        representatives = {g:next(j for j in support if _group(j) == g) for g in groups}
        actual = []
        for bits in product((0,1),repeat=len(groups)):
            meter.charge('audit_beta_candidates')
            meter.work(len(groups)+1)
            active = [g for g,bit in zip(groups,bits) if bit]
            valid = True
            for i,y in self.control['observed']:
                meter.charge('audit_parity_row_tests')
                meter.work(max(1,len(active)))
                parity = sum(self.rows[i][representatives[g]] for g in active) % 2
                if parity != y % 2:
                    valid = False
            meter.work(len(active)+1)
            if valid and any(g not in (0,1) for g in active):
                meter.record(1+len(active))
                actual.append(active)
        claimed = record['compatible_betas']
        require(type(claimed) is list and len(claimed) <= 8,'bounded compatible-beta claim')
        for active in claimed:
            meter.work(4)
            require(type(active) is list and len(active) <= 3
                    and all(type(g) is int for g in active),'beta claim canonical types')
        require(claimed == actual,'complete ordered compatible-beta list')
        meter.work(4)
        term = len(actual)*13**(3-proof['rank_a']) if proof['consistent'] else 0
        require(type(record['term']) is int and record['term'] == term,'exact fiber contribution')
        require(type(record['prefix_lower_bound']) is int
                and record['prefix_lower_bound'] == self.lower_bound+term,'independent prefix sum')
        self.checked_supports += 1
        self.lower_bound += term
        return dict(kind='support',term=term,checked_supports=self.checked_supports,lower_bound=self.lower_bound)

    def _terminal(self,record):
        self.meter.work(10)
        require(set(record) == TERMINAL_KEYS,'terminal exact schema')
        require(type(record['support_count']) is int and record['support_count'] == self.checked_supports,
                'terminal support inventory')
        require(type(record['lower_bound']) is int and record['lower_bound'] == self.lower_bound,'terminal sum')
        require(digest_string(record['content_sha256'])
                and record['content_sha256'] == self.content_hash.hexdigest(),'terminal exact content hash')
        require(type(record['status']) is str,'terminal status type')
        if record['status'] == 'GATE_REJECTED_LOWER_BOUND':
            require(self.checked_supports > 0 and self.lower_bound > self.point_cap,'uncertified gate rejection')
            require(record['exact_W'] is None,'prefix cannot claim exact W')
        elif record['status'] == 'WORKLOAD_ADMITTED':
            require(self.checked_supports == 4495 and self.lower_bound <= self.point_cap,'incomplete or excessive admission')
            require(type(record['exact_W']) is int and record['exact_W'] == self.lower_bound,'exact full W')
        else:
            raise CheckerError('unknown completed preflight status')
        self.status,self.exact_W = record['status'],record['exact_W']
        self.terminal_seen = True
        return dict(kind='terminal',status=self.status,checked_supports=self.checked_supports,
                    lower_bound=self.lower_bound,exact_W=self.exact_W)

    def _consume(self,raw_line):
        require(not self.failed,'failed checker cannot resume')
        require(not self.terminal_seen,'data after terminal')
        require(type(raw_line) is bytes,'evidence bytes')
        require(len(raw_line) <= self.meter.caps.max_file_bytes-self.byte_count,'audit file byte bound')
        record = parse_canonical_line(raw_line,self.meter)
        require(type(record.get('kind')) is str,'record kind')
        if not self.header_seen:
            require(record['kind'] == 'header','header must be first')
            result = self._header(record)
        elif record['kind'] == 'support':
            result = self._support(record)
        elif record['kind'] == 'terminal':
            result = self._terminal(record)
        else:
            raise CheckerError('unexpected record kind')
        if record['kind'] != 'terminal':
            self.content_hash.update(raw_line)
        self.byte_count += len(raw_line)
        return result

    def consume(self,raw_line):
        try:
            return self._consume(raw_line)
        except BaseException:
            self.failed = True
            raise

    def finish(self):
        require(not self.failed and self.header_seen and self.terminal_seen,
                'failed or unfinished evidence is not a completed proof')
        self.meter.work(0)
        return dict(status=self.status,checked_supports=self.checked_supports,
                    lower_bound=self.lower_bound,exact_W=self.exact_W,
                    input_sha256=self.input_sha256,bytes=self.byte_count)
