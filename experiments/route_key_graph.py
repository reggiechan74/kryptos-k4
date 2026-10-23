"""Exact modular bipartite sum constraints, retaining component offsets."""
from collections import deque


def solve_graph(vertex_count, edges, modulus=26):
    if vertex_count < 1 or modulus < 2:
        raise ValueError('positive vertex count and modulus>=2 required')
    adjacency = [[] for _ in range(vertex_count)]
    for index, edge in enumerate(edges):
        u, v, delta = edge['u'], edge['v'], edge['delta']
        if not 0 <= u < vertex_count or not 0 <= v < vertex_count or u == v:
            raise ValueError('distinct graph endpoints required')
        adjacency[u].append((v, -delta, index))
        adjacency[v].append((u, delta, index))
    component, potential = [None] * vertex_count, [None] * vertex_count
    parent, parent_edge = [None] * vertex_count, [None] * vertex_count
    tree_edges, components = set(), []
    for root in range(vertex_count):
        if component[root] is not None:
            continue
        label = len(components)
        component[root], potential[root] = label, 0
        queue, vertices = deque([root]), []
        while queue:
            u = queue.popleft()
            vertices.append(u)
            for v, change, index in adjacency[u]:
                if component[v] is None:
                    component[v], potential[v] = label, (potential[u] + change) % modulus
                    parent[v], parent_edge[v] = u, index
                    tree_edges.add(index)
                    queue.append(v)
        components.append(sorted(vertices))

    def tree_path(u, v):
        left, right = [u], [v]
        while parent[left[-1]] is not None:
            left.append(parent[left[-1]])
        while parent[right[-1]] is not None:
            right.append(parent[right[-1]])
        right_lookup = {node: i for i, node in enumerate(right)}
        left_index = next(i for i, node in enumerate(left) if node in right_lookup)
        right_index = right_lookup[left[left_index]]
        nodes = left[:left_index + 1] + list(reversed(right[:right_index]))
        result = []
        for source, target in zip(nodes, nodes[1:]):
            index = parent_edge[source] if parent[source] == target else parent_edge[target]
            edge = edges[index]
            difference = edge['delta'] if (source, target) == (edge['u'], edge['v']) else -edge['delta']
            result.append(dict(edge_index=index, source=source, target=target,
                               potential_difference_mod=difference % modulus))
        return result

    first, failures = None, 0
    for index, edge in enumerate(edges):
        residual = (potential[edge['u']] - potential[edge['v']] - edge['delta']) % modulus
        if residual:
            failures += 1
            if first is None:
                path = tree_path(edge['u'], edge['v'])
                implied = sum(step['potential_difference_mod'] for step in path) % modulus
                first = dict(closing_edge_index=index, required_delta=edge['delta'] % modulus,
                             tree_path=path, implied_delta=implied, residual=residual)
    c = len(components)
    return dict(compatible=failures == 0, vertex_count=vertex_count, edge_count=len(edges),
                components=components, component_labels=component, component_count=c,
                representative_potentials=potential,
                representative_scope='Within-component differences only; offsets between components remain free.',
                tree_edge_indices=sorted(tree_edges), independent_cycle_checks=len(edges) - vertex_count + c,
                failed_fundamental_cycles=failures, first_conflict=first,
                exact_key_assignments=0 if failures else modulus ** c)
