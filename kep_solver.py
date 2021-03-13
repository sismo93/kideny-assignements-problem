#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Fränk Plein

import kep_ip as ip
import kep_algo as algo
import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CLI for solving kidney exchange problems.")

    subparsers = parser.add_subparsers(title='Methods', description='Method to be used to solve the problem.')

    # sub parser for the IP options
    ip_parser = subparsers.add_parser('ip', help='Solve using IP formulation.')
    ip_parser.set_defaults(solve_call=ip.solve)
    ip_parser.add_argument('-M', dest='cycle_limit', action='store_const', const=True, default=False,
                           help='Limit maximum number of exchanges per transplant cycle.')
    ip_parser.add_argument('-v', dest='verbose', action='store_const', const=True, default=False,
                           help='Verbose, ouputting solver log.')

    # sub parser for the algo options
    algo_parser = subparsers.add_parser('algo', help='Solve using positive cycle elimination.')
    algo_parser.set_defaults(solve_call=algo.solve)

    parser.add_argument('instance')

    args = parser.parse_args()

    # solve call returns a list of arcs in the solution
    solution = args.solve_call(args)
    print(solution)
