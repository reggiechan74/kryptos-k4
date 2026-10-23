#!/usr/bin/env python3
"""Exact modular graph audit for the source-frozen unanchored IPA relaxation.

Standard library only. No probabilistic or floating-point feasibility decisions.
The protocol JSON is an input, never modified by this program.
"""
from __future__ import annotations

import argparse
from collections import deque
import hashlib
import itertools
import json
import math
from pathlib import Path
import random


def glyph_node(g):
    return "f:" + g


def phase_node(j):
    return "q:" + str(j)


def reverse_step(s, modulus):
    return {"from": s["to"], "to": s["from"], "delta": -s["delta"] % modulus,
            "equation_id": s["equation_id"]}


def graph_solve(glyphs, period, equations, modulus=26):
    """All equality solutions: x_v = potential_v + gauge_component mod m."""
    nodes = [glyph_node(g) for g in glyphs] + [phase_node(j) for j in range(period)]
    adjacency = {v: [] for v in nodes}
    for e in equations:
        f, q = glyph_node(e["glyph"]), phase_node(e["phase"])
        step = {"from": f, "to": q, "delta": -e["c"] % modulus,
                "equation_id": e["id"]}
        adjacency[f].append(step)
        adjacency[q].append(reverse_step(step, modulus))
    potentials, components, parent, component_of = {}, [], {}, {}

    def root_path(node):
        path = []
        while node in parent:
            step = parent[node]
            path.append(step)
            node = step["from"]
        return list(reversed(path))

    def tree_path(a, b):
        pa, pb = root_path(a), root_path(b)
        shared = 0
        while shared < min(len(pa), len(pb)) and pa[shared] == pb[shared]:
            shared += 1
        return ([reverse_step(s, modulus) for s in reversed(pa[shared:])]
                + pb[shared:])

    first_cycle = None
    for root in nodes:
        if root in potentials:
            continue
        cid = len(components)
        potentials[root] = 0
        component_of[root] = cid
        queue = deque([root])
        cnodes = []
        while queue:
            u = queue.popleft()
            cnodes.append(u)
            for step in adjacency[u]:
                v = step["to"]
                candidate = (potentials[u] + step["delta"]) % modulus
                if v not in potentials:
                    potentials[v] = candidate
                    component_of[v] = cid
                    parent[v] = step
                    queue.append(v)
                elif potentials[v] != candidate and first_cycle is None:
                    walk = tree_path(v, u) + [step]
                    first_cycle = {"type": "nonzero_cycle", "walk": walk,
                                   "residual": sum(s["delta"] for s in walk) % modulus}
        components.append({"id": cid, "root": root, "nodes": sorted(cnodes),
                           "potentials": {v: potentials[v] for v in sorted(cnodes)},
                           "glyph_potentials": {v[2:]: potentials[v] for v in cnodes if v.startswith("f:")}})
    collision = None
    for comp in components:
        seen = {}
        for g, val in comp["glyph_potentials"].items():
            if val in seen and collision is None:
                a, b = seen[val], g
                walk = tree_path(glyph_node(a), glyph_node(b))
                collision = {"type": "forced_glyph_collision", "glyphs": [a, b],
                             "walk": walk, "residual": sum(s["delta"] for s in walk) % modulus}
            seen[val] = g
    certificate = first_cycle or collision
    return {"equality_consistent": first_cycle is None,
            "within_component_injective": collision is None,
            "certificate": certificate, "components": components,
            "component_of": component_of, "modulus": modulus,
            "equation_count": len(equations), "node_count": len(nodes),
            "component_count": len(components),
            "cycle_rank": len(equations) - len(nodes) + len(components)}


def verify_certificate(certificate, equations, modulus):
    if certificate is None:
        return True
    by_id = {e["id"]: e for e in equations}
    walk = certificate["walk"]
    if not walk:
        return False
    for i, step in enumerate(walk):
        e = by_id[step["equation_id"]]
        f, q = glyph_node(e["glyph"]), phase_node(e["phase"])
        if (step["from"], step["to"]) == (f, q):
            expected = -e["c"] % modulus
        elif (step["from"], step["to"]) == (q, f):
            expected = e["c"] % modulus
        else:
            return False
        if expected != step["delta"] or (i and walk[i-1]["to"] != step["from"]):
            return False
    residual = sum(s["delta"] for s in walk) % modulus
    if residual != certificate["residual"]:
        return False
    if certificate["type"] == "nonzero_cycle":
        return walk[0]["from"] == walk[-1]["to"] and residual != 0
    a, b = certificate["glyphs"]
    return (a != b and walk[0]["from"] == glyph_node(a)
            and walk[-1]["to"] == glyph_node(b) and residual == 0)


def shortest_collision_certificate(equations, pair, modulus=26):
    """A short equality path for a specified distinct-glyph collision."""
    adjacency = {}
    for e in equations:
        f, q = glyph_node(e["glyph"]), phase_node(e["phase"])
        step = {"from": f, "to": q, "delta": -e["c"] % modulus, "equation_id": e["id"]}
        adjacency.setdefault(f, []).append(step)
        adjacency.setdefault(q, []).append(reverse_step(step, modulus))
    start, end = map(glyph_node, pair)
    parent = {start: None}
    queue = deque([start])
    while queue and end not in parent:
        u = queue.popleft()
        for step in adjacency.get(u, []):
            if step["to"] not in parent:
                parent[step["to"]] = step
                queue.append(step["to"])
    assert end in parent
    walk, node = [], end
    while node != start:
        step = parent[node]
        walk.append(step)
        node = step["from"]
    walk.reverse()
    cert = {"type": "forced_glyph_collision", "glyphs": pair, "walk": walk,
            "residual": sum(s["delta"] for s in walk) % modulus}
    assert verify_certificate(cert, equations, modulus)
    return cert


def make_equations(ciphertext, alphabet, windows, period):
    out = []
    for window in windows:
        for offset, glyph in enumerate(window["glyphs"]):
            position = window["one_based_start"] + offset
            out.append({"id": position, "position": position, "glyph": glyph,
                        "phase": (position - 1) % period,
                        "cipher_letter": ciphertext[position - 1],
                        "c": alphabet.index(ciphertext[position - 1])})
    return out


def component_constraint_record(graph, gauge_glyph="i"):
    if graph["certificate"]:
        return {"empty": True, "reason": graph["certificate"]["type"]}
    anchor_component = graph["component_of"][glyph_node(gauge_glyph)]
    anchor_potential = graph["components"][anchor_component]["potentials"][glyph_node(gauge_glyph)]
    return {
        "empty": False,
        "representation": "Each node value is its stored potential plus t[component] modulo m. All glyph values are pairwise distinct. This finite constraint set is exactly all solutions, with no representative selected.",
        "component_gauges": {str(comp["id"]): list(range(graph["modulus"])) for comp in graph["components"]},
        "gauge_fix": {"component": anchor_component, "value": -anchor_potential % graph["modulus"], "meaning": "f(" + gauge_glyph + ")=0 is global-shift gauge only"},
        "cross_component_condition": "For every pair of components a!=b and each glyph g in a, h in b: t[a]+potential[g] != t[b]+potential[h] modulo m.",
        "ungauged_multiplier": graph["modulus"]
    }


def falling(n, k):
    return math.prod(range(n-k+1, n+1)) if 0 <= k <= n else 0


def count_gauge_orbits(graph, gauge_glyph="i", max_nodes=2_000_000):
    """Count injective solutions exactly, factoring labelled singleton placements.

    Duplicate masks from different shifts remain distinct: rotational symmetries
    of a component set do not identify the assignments of its labelled glyphs.
    Empty-glyph components are independent unobserved key-phase freedoms.
    """
    if graph["certificate"]:
        return {"exact": True, "gauge_orbits": 0, "raw_assignments": 0, "search_nodes": 0}
    m = graph["modulus"]
    anchor = graph["component_of"][glyph_node(gauge_glyph)]
    anchor_comp = graph["components"][anchor]
    anchor_shift = -anchor_comp["potentials"][glyph_node(gauge_glyph)] % m
    occupied = sum(1 << ((v+anchor_shift) % m) for v in anchor_comp["glyph_potentials"].values())
    singleton_count = 0
    key_only_count = 0
    multis = []
    for comp in graph["components"]:
        if comp["id"] == anchor:
            continue
        vals = list(comp["glyph_potentials"].values())
        if not vals:
            key_only_count += 1
        elif len(vals) == 1:
            singleton_count += 1
        else:
            masks = [sum(1 << ((v+t) % m) for v in vals) for t in range(m)]
            multis.append((len(vals), masks))
    multis.sort(key=lambda pair: -pair[0])
    visited = 0

    def visit(depth, used):
        nonlocal visited
        visited += 1
        if visited > max_nodes:
            raise RuntimeError("exact counter search-node bound reached")
        if depth == len(multis):
            return falling(m-used.bit_count(), singleton_count) * m**key_only_count
        return sum(visit(depth+1, used | mask) for mask in multis[depth][1] if not (used & mask))

    try:
        n = visit(0, occupied)
    except RuntimeError as exc:
        return {"exact": False, "gauge_orbits": None, "raw_assignments": None,
                "search_nodes": visited, "bound": max_nodes, "reason": str(exc)}
    return {"exact": True, "gauge_orbits": n, "raw_assignments": m*n,
            "search_nodes": visited, "factored_singletons": singleton_count,
            "key_only_components": key_only_count,
            "enumerated_multiglyph_components": len(multis)}


def summarize_first_stage_checks(graph, equations, first_glyphs):
    rows = []
    for e in equations:
        fg, qj = glyph_node(e["glyph"]), phase_node(e["phase"])
        a, b = graph["component_of"][fg], graph["component_of"][qj]
        pf = graph["components"][a]["potentials"][fg]
        pq = graph["components"][b]["potentials"][qj]
        row = {"position": e["position"], "glyph": e["glyph"], "actual_c": e["c"],
               "status": "new_glyph_value" if e["glyph"] not in first_glyphs else "gauge_dependent",
               "glyph_component": a, "phase_component": b}
        if a == b:
            row.update(status="linearly_forced", predicted_c=(pf-pq) % graph["modulus"],
                       matches=(pf-pq) % graph["modulus"] == e["c"])
        else:
            row["constraint"] = {"left_gauge": a, "right_gauge": b,
                                 "required_difference": (e["c"]-pf+pq) % graph["modulus"]}
        rows.append(row)
    return rows


def run_initial(spec):
    glyphs = list(dict.fromkeys("".join(w["glyphs"] for w in spec["windows"])))
    assert len(spec["ciphertext"]) == 97 and len(glyphs) == 14
    assert [len(w["glyphs"]) for w in spec["windows"]] == [13, 11]
    rows = []
    for name, alphabet in spec["alphabets"].items():
        assert len(alphabet) == 26 and len(set(alphabet)) == 26
        for period in spec["periods"]:
            eqs = make_equations(spec["ciphertext"], alphabet, spec["windows"], period)
            first, full = graph_solve(glyphs, period, eqs[:13]), graph_solve(glyphs, period, eqs)
            assert verify_certificate(first["certificate"], eqs[:13], 26)
            assert verify_certificate(full["certificate"], eqs, 26)
            first_only = graph_solve(list(dict.fromkeys(spec["windows"][0]["glyphs"])), period, eqs[:13])
            first_count = count_gauge_orbits(first_only)
            extended_count = count_gauge_orbits(first)
            assert first_count["exact"] and extended_count["exact"]
            assert extended_count["gauge_orbits"] == first_count["gauge_orbits"] * falling(18, 6)
            check_status = None
            if not first["certificate"]:
                check_status = summarize_first_stage_checks(first, eqs[13:], set(spec["windows"][0]["glyphs"]))
                for check, e in zip(check_status, eqs[13:]):
                    allowed = []
                    for candidate in range(26):
                        hypothetical = {**e, "c": candidate}
                        extended_graph = graph_solve(glyphs, period, eqs[:13]+[hypothetical])
                        count = count_gauge_orbits(extended_graph)
                        assert count["exact"]
                        if count["gauge_orbits"]:
                            allowed.append(candidate)
                    check["exact_allowed_c_values_before_any_Berlin_data"] = allowed
                    check["exact_domain_size"] = len(allowed)
                    check["fully_forced_before_Berlin"] = len(allowed) == 1
                    check["actual_c_individually_allowed"] = e["c"] in allowed
                    assert len(allowed) > 0
                    assert check["fully_forced_before_Berlin"] == (check["status"] == "linearly_forced")
            primary = first["certificate"] or full["certificate"]
            if primary is not None:
                assert not verify_certificate({**primary, "residual": (primary["residual"]+1) % 26}, eqs, 26)
            preferred_collision_pairs = {("AZ", 11): ["ɪ", "n"], ("KRYPTOS", 11): ["b", "t"],
                                         ("KRYPTOS", 12): ["b", "θ"]}
            extra_certificate = (shortest_collision_certificate(eqs, preferred_collision_pairs[(name, period)])
                                 if (name, period) in preferred_collision_pairs else None)
            rows.append({"alphabet": name, "period": period, "equations": eqs,
                         "fit_graph": first, "full_graph": full,
                         "fit_solution_set": component_constraint_record(first),
                         "full_solution_set": component_constraint_record(full),
                         "first_8_glyph_count": first_count,
                         "first_stage_14_glyph_extension_count": extended_count,
                         "full_count": count_gauge_orbits(full),
                         "primary_rejection_stage": ("fit" if first["certificate"] else "Berlin_check") if primary else None,
                         "primary_certificate": primary,
                         "single_segment_collision_certificate": extra_certificate,
                         "Berlin_first_stage_status": check_status})
    return {"glyphs": glyphs, "structures": rows}


def synthetic_controls(spec):
    glyphs = list(dict.fromkeys("".join(w["glyphs"] for w in spec["windows"])))
    rng = random.Random(20261023002)
    records = []
    for name, alphabet in spec["alphabets"].items():
        for period in spec["periods"]:
            values = rng.sample(range(26), len(glyphs))
            mapping = dict(zip(glyphs, values))
            key = [rng.randrange(26) for _ in range(period)]
            # Every control uses a new random stream containing all 14 symbols.
            stream = glyphs[:] + [rng.choice(glyphs) for _ in range(83)]
            rng.shuffle(stream)
            cipher = "".join(alphabet[(mapping[g]+key[i % period]) % 26] for i, g in enumerate(stream))
            equations = [{"id": i+1, "position": i+1, "glyph": g, "phase": i % period,
                          "cipher_letter": cipher[i], "c": alphabet.index(cipher[i])}
                         for i, g in enumerate(stream)]
            graph = graph_solve(glyphs, period, equations)
            assert graph["certificate"] is None
            assignment = {glyph_node(g): mapping[g] for g in glyphs}
            assignment.update({phase_node(j): -key[j] % 26 for j in range(period)})
            gauges = {}
            for comp in graph["components"]:
                ts = {(assignment[v]-p) % 26 for v, p in comp["potentials"].items()}
                assert len(ts) == 1
                gauges[str(comp["id"])] = next(iter(ts))
            # Check all 26 global shifts preserve equations and injectivity;
            # exactly one sets f(i)=0, and true Beaufort is f -> -f.
            gauge_fix_hits = 0
            for shift in range(26):
                shifted = {g: (v+shift) % 26 for g, v in mapping.items()}
                shifted_key = [(k-shift) % 26 for k in key]
                assert len(set(shifted.values())) == 14
                assert all((shifted[e["glyph"]]+shifted_key[e["phase"]]) % 26 == e["c"] for e in equations)
                gauge_fix_hits += shifted["i"] == 0
            assert gauge_fix_hits == 1
            assert all((key[e["phase"]]-(-mapping[e["glyph"]])) % 26 == e["c"] for e in equations)
            window_equations = []
            for window in spec["windows"]:
                for offset, g in enumerate(window["glyphs"]):
                    pos = window["one_based_start"]+offset
                    phase = (pos-1) % period
                    c = (mapping[g]+key[phase]) % 26
                    window_equations.append({"id": pos, "glyph": g, "phase": phase, "c": c})
            window_graph = graph_solve(glyphs, period, window_equations)
            assert window_graph["certificate"] is None
            window_count = count_gauge_orbits(window_graph)
            assert window_count["exact"] and window_count["gauge_orbits"] > 0
            records.append({"alphabet": name, "period": period, "stream": "".join(stream),
                            "ciphertext": cipher, "glyph_map": mapping, "key": key,
                            "component_gauges": gauges, "all_26_gauge_shifts_verified": True,
                            "true_Beaufort_equivalence_verified": True,
                            "same_window_geometry_control": {"equations": window_equations,
                                                              "gauge_fixed_count": window_count["gauge_orbits"],
                                                              "passed": True},
                            "passed": True})
    return {"seed": 20261023002, "count": len(records), "records": records}


def brute_force_count(glyphs, period, equations, modulus):
    # Intentionally independent: directly loop f and k, no graph potentials,
    # singleton factoring, modular divisions or component data.
    count = 0
    for tail in itertools.permutations(range(1, modulus), len(glyphs)-1):
        mapping = dict(zip(glyphs, (0,)+tail))
        for key in itertools.product(range(modulus), repeat=period):
            if all((mapping[e["glyph"]]+key[e["phase"]]) % modulus == e["c"] for e in equations):
                count += 1
    return count


def tiny_ring_controls():
    rng = random.Random(20261023003)
    records = []
    # Positive, adversarial/random and unconstrained cases include empty graphs,
    # unused key phases, isolated glyphs, composite rings and rotational symmetry.
    for modulus in [3, 4, 5, 6]:
        for nglyphs in range(1, min(4, modulus)+1):
            glyphs = [chr(ord("a")+j) for j in range(nglyphs)]
            for period in [1, 2, 3]:
                for case in range(5):
                    mapping = dict(zip(glyphs, rng.sample(range(modulus), nglyphs)))
                    key = [rng.randrange(modulus) for _ in range(period)]
                    equations = []
                    for i in range(0 if case == 0 else 1+case*2):
                        g, phase = rng.choice(glyphs), rng.randrange(period)
                        c = ((mapping[g]+key[phase]) % modulus if case in [1, 2]
                             else rng.randrange(modulus))
                        equations.append({"id": i+1, "glyph": g, "phase": phase, "c": c})
                    graph = graph_solve(glyphs, period, equations, modulus)
                    result = count_gauge_orbits(graph, glyphs[0])
                    direct = brute_force_count(glyphs, period, equations, modulus)
                    assert result["exact"] and result["gauge_orbits"] == direct
                    assert verify_certificate(graph["certificate"], equations, modulus)
                    records.append({"modulus": modulus, "glyph_count": nglyphs,
                                    "period": period, "case": case, "equations": equations,
                                    "graph_count": result["gauge_orbits"], "direct_count": direct,
                                    "passed": True})
    return {"seed": 20261023003, "count": len(records), "records": records}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--spec", default=str(Path(__file__).with_name("protocol.json")))
    parser.add_argument("--output", default=str(Path(__file__).with_name("results.json")))
    args = parser.parse_args()
    spec_bytes = Path(args.spec).read_bytes()
    spec = json.loads(spec_bytes)
    results = run_initial(spec)
    results["validation"] = {"synthetic": synthetic_controls(spec), "tiny_rings": tiny_ring_controls()}
    results["protocol_sha256"] = hashlib.sha256(spec_bytes).hexdigest()
    Path(args.output).write_text(json.dumps(results, ensure_ascii=False, indent=2) + "\n")
    for row in results["structures"]:
        fit, full = row["fit_graph"], row["full_graph"]
        reason = lambda g: g["certificate"]["type"] if g["certificate"] else "consistent"
        print(row["alphabet"], row["period"], reason(fit), reason(full),
              "components", fit["component_count"], full["component_count"])


if __name__ == "__main__":
    main()
