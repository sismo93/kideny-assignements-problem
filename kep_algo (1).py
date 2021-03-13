#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author:wassim kezai 
# ID: insert ulb id (000357375)

from networkx import DiGraph, simple_cycles

# naming convention
patient = lambda i: "p_{{{}}}".format(i)
donor = lambda i: "d_{{{}}}".format(i)


# insert any auxiliary code
def read_csv(file):
    with open(file, 'r') as f:
        row = f.readline().split(';')
        number_of_patient_donor_pairs = int(row[0])
        number_of_compatibilities = int(row[1])
        maximum_number_of_exchanges = int(row[2])

        di_pj_arcs = []
        for _ in range(number_of_compatibilities):
            row = f.readline().split(';')
            di_pj_arcs.append([donor(row[0]), patient(row[1]), float(row[2])])

        return number_of_patient_donor_pairs, number_of_compatibilities, maximum_number_of_exchanges, di_pj_arcs


def get_cycle_weight(nodes, weights_dict):
    result = 0.0
    current = nodes[-1]

    for next_node in nodes:
        result += weights_dict[(current, next_node)]
        current = next_node

    return round(result, 9)


def solve(args):
    number_of_patient_donor_pairs, _, _, di_pj_arcs = read_csv(args.instance)

    pi_di_arcs = [[patient(i), donor(i), 0.0] for i in range(number_of_patient_donor_pairs)]

    arcs_cost = dict((tuple(arc[:2]), arc[2]) for arc in di_pj_arcs + pi_di_arcs)
    X_dict = dict((tuple(arc[:2]), 0) for arc in di_pj_arcs + pi_di_arcs)

    while True:
        forward_arcs_set = set((pair[0] for pair in X_dict.items() if pair[1] == 0))
        backward_arcs_set = set((pair[0][::-1] for pair in X_dict.items() if pair[1] == 1))
        backward_arcs_set -= forward_arcs_set.intersection(backward_arcs_set)

        residual_cost_data = dict(((arc, arcs_cost[arc]) for arc in forward_arcs_set))
        residual_cost_data.update(dict(((arc, -1 * arcs_cost[arc[::-1]]) for arc in backward_arcs_set)))

        cycles_nodes = simple_cycles(DiGraph(iter(residual_cost_data.keys())))

        for cycle_nodes in cycles_nodes:
            cycle_weight = get_cycle_weight(cycle_nodes, residual_cost_data)

            if cycle_weight > 0:
                cycle_arcs = list(zip(cycle_nodes, cycle_nodes[1:] + cycle_nodes[:1]))

                forward_arcs_to_update = forward_arcs_set.intersection(cycle_arcs)
                backward_arcs_to_update = backward_arcs_set.intersection(cycle_arcs)

                for arc in forward_arcs_to_update:
                    X_dict[arc] += 1

                for arc in backward_arcs_to_update:
                    X_dict[arc[::-1]] -= 1

                break

        else:
            break

    return [pair[0] for pair in X_dict.items() if pair[1] == 1]
