from copy import deepcopy
from itertools import product

import networkx as nx


def find_nlets(lst, n, given_sum):
    def valid(val):
        return sum(val) == given_sum

    return list(filter(valid, list(product(lst, repeat=n))))


def edge_in_path(e, p):
    for e1 in zip(p[:-1], p[1:]):
        if e1 == e:
            return True
    return False


def expected_cost(flow, costs):
    return sum([f * c for f, c in zip(flow, costs)])


def eval_flow_costs(G, v0, v1, impossible_paths=[]):
    possible_paths = []
    for path in nx.all_simple_paths(G, v0, v1):
        if path in impossible_paths:
            continue
        possible_paths += [path]

    results = []
    for flow_division in find_nlets(list(range(11)), len(possible_paths), 10):
        costs = {}
        for e in G.edges:
            edge_flow = 0
            for flow, path in zip(flow_division, possible_paths):
                if edge_in_path(e, path):
                    edge_flow += flow
            costs[e] = G.get_edge_data(*e)['cost'](edge_flow)
        path_costs = [0] * len(possible_paths)
        for i, path in enumerate(possible_paths):
            for e in zip(path[:-1], path[1:]):
                try:
                    path_costs[i] += costs[e]
                except KeyError:
                    path_costs[i] += costs[(e[1], e[0])]
        results += [{'flow': flow_division,
                     'costs': path_costs}]
    return results

def check_for_ne(flow, results):
    is_ne = True
    costs = [r for r in results if r['flow'] == tuple(flow)][0]['costs']
    for i in range(len(flow)):
        for j in range(len(flow)):
            # we take one from i-th position and add one to j-th position
            if flow[i] == 0 or j == i:
                continue
            new_flow = deepcopy(flow)
            new_flow[i] -= 1
            new_flow[j] += 1
            possible_results = [r for r in results if r['flow'] == tuple(new_flow)]
            if possible_results[0]['costs'][j] < costs[i]:
                # Has incentive to change"
                is_ne = False
                break
        if is_ne is False:
            break
    return is_ne