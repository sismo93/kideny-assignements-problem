#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author:wassim kezai 
# ID: insert ulb id (000357375)

from pyomo.environ import *

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


def find_out_of_limit_cycles(arcs, cycle_limit):
    source = set([arc[0] for arc in arcs])
    target_dict = dict(arcs)
    result = []

    while source:
        start = source.pop()
        cycle = [start]
        node = target_dict[start]

        while node != start:
            cycle.append(node)
            node = target_dict[node]

        if len(cycle) > cycle_limit:
            result.append(cycle)

        source -= set(cycle)

    return result


def create_model(nodes_set, arcs_set, arcs_cost, cycle_limit):
    model = AbstractModel()

    model.node_set = Set(initialize=nodes_set)
    model.arc_set = Set(initialize=arcs_set, dimen=2)

    model.X = Var(model.arc_set, domain=Binary if cycle_limit else PercentFraction)

    def obj_expression(_model):
        return sum(_model.X[arc] * arcs_cost[arc] for arc in arcs_set)

    model.OBJ = Objective(rule=obj_expression, sense=maximize)

    def constraint_rule(_model, node):
        source = (arc[0] for arc in arcs_set if arc[1] == node)
        target = (arc[1] for arc in arcs_set if arc[0] == node)

        return sum(_model.X[(node, t)] for t in target) - sum(_model.X[(s, node)] for s in source) == 0

    model.Constraint1 = Constraint(model.node_set, rule=constraint_rule)

    if cycle_limit:
        model.cycle_pool = Set(dimen=1)

        def cycle_constraint_rule(_model, cycle):
            return sum(_model.X[arc] for arc in cycle) <= (len(cycle) - 1)

        model.Constraint2 = Constraint(model.cycle_pool, rule=cycle_constraint_rule)

    return model


def solve(args):
    opt = SolverFactory('glpk')
    number_of_patient_donor_pairs, _, maximum_number_of_exchanges, di_pj_arcs = read_csv(args.instance)
    cycle_limit = maximum_number_of_exchanges * 2 if args.cycle_limit else 0

    pi_di_arcs = [[patient(i), donor(i), 0.0] for i in range(number_of_patient_donor_pairs)]

    arcs_cost = dict((tuple(arc[:2]), arc[2]) for arc in di_pj_arcs + pi_di_arcs)

    nodes_set = set([donor(i) for i in range(number_of_patient_donor_pairs)]
                    + [patient(i) for i in range(number_of_patient_donor_pairs)])

    arcs_set = set(arcs_cost.keys())

    model = create_model(nodes_set, arcs_set, arcs_cost, cycle_limit)

    while True:
        instance = model.create_instance()
        opt.solve(instance)

        if not cycle_limit:
            break

        limit_cycles = find_out_of_limit_cycles([arc for arc in instance.X if value(instance.X[arc])], cycle_limit)

        if not limit_cycles:
            break

        for elem in [frozenset(zip(cycle, cycle[1:] + cycle[:1])) for cycle in limit_cycles]:
            model.cycle_pool.add(elem)

    return [arc for arc in instance.X if value(instance.X[arc])]
