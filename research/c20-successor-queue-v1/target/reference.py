"""Unchanged function extraction from validated pilot.py; shared math, separate traversal."""

def require(condition, message):
    if not condition:
        raise RuntimeError(message)

def signature(word, q):
    if not word:
        return (None, tuple(() for _ in range(q)))
    queues = tuple(tuple(word[j+1] for j in range(len(word)-1) if word[j] == v) for v in range(q))
    return (word[0], queues)


def reversed_signature(word, q):
    start, queues = signature(word, q)
    if not word:
        return start, queues
    end = word[-1]
    changed = []
    for v, queue in enumerate(queues):
        if v == end:
            changed.append(queue[::-1])
        elif queue:
            changed.append(queue[-2::-1] + queue[-1:])
        else:
            changed.append(())
    return start, tuple(changed)


def full_reference(word):
    # Independent tuple/dictionary walk for disclosed length97 plants only.
    # Its mathematical construction is shared; tiny exhaustive lookup above
    # is the independent reconstruction oracle.
    if not word:
        return ()
    start, queues = reversed_signature(word, 26)
    pending = {i: queue for i, queue in enumerate(queues) if queue}
    out = [start]
    while pending:
        require(out[-1] in pending, 'reference premature end')
        queue = pending[out[-1]]
        v = queue[0]
        if len(queue) == 1:
            del pending[out[-1]]
        else:
            pending[out[-1]] = queue[1:]
        out.append(v)
    require(len(out) == len(word) and out[-1] == word[-1], 'reference endpoint/length')
    return tuple(out)

