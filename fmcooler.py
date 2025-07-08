#!/usr/bin/env python

# Libraries
from flamapy.core.discover import DiscoverMetamodels
from qubovert import boolean_var
from neal import SimulatedAnnealingSampler

import sys
import pandas as pd
import time
import os

# Constant fixing the number of decimal places considered in the weights
PRECISION = 8

# Solve the model using dwave-neal with a certain number of reads
def solve(model, num_reads):
    qubo = model.to_qubo()
    dwave_qubo = qubo.Q
    res = SimulatedAnnealingSampler().sample_qubo(dwave_qubo, num_reads=num_reads)
    qubo_solution = res.first.sample
    model_solution = model.convert_solution(qubo_solution)
    return model_solution, qubo

# Main function
def main():
    # Parse arguments
    args = sys.argv
    if len(args) != 6 or args[4] not in ["min", "max"]:
        print('[!] Input error\n')
        print('[1] The file of the Feature Model in UVL format must be specified as first parameter')
        print('[2] The file of weights must be specified as second parameter')
        print('[3] The number of the used column must be specified as third parameter')
        print('[4] The string "min" or "max" must be specified to MINIMIZE or MAXIMIZE as fourth parameter')
        print('[5] The number of reads must be specified as fifth parameter')
        exit(-1)
    print('[&] Reading model with flamapy and generating CNF to perfom restrictions in QUBO')
    uvl_path = args[1]
    csv_path = args[2]
    columns, rates_str = tuple(map(lambda x: x.split(','), args[3].split(':')))
    rates = list(map(float, rates_str))
    is_max = 0 if args[4] == "min" else 1
    num_reads = int(args[5])

    # Get clauses in CNF with flamapy
    dm = DiscoverMetamodels()
    feature_model = dm.use_transformation_t2m(uvl_path,'fm')
    sat_model = dm.use_transformation_m2m(feature_model,"pysat")
    clauses = sat_model.get_all_clauses()

    var_map = {k: v for k, v in sat_model.variables.items()}
    inv_map = {v: k for k, v in var_map.items()}

    # Load variable weights
    w = {}
    pairs = pd.read_csv(csv_path)[['features', *columns]].values.tolist()
    for feature, *values in pairs:
        w[feature] = 10 ** PRECISION * sum(rate * value for rate, value in zip(rates, values))

    # Implement the objective function g_w using the weights and qubovert
    x = {key: boolean_var(key) for key in var_map.keys()}
    model = 0
    for key in var_map.keys():
        # is_max set the negative sign for the weights
        model += (- 1) ** is_max * w[key] * x[key]

    # Implement the restriction function h_r using the clauses
    LAM = 10 ** (PRECISION + 5)
    for clause in clauses:
        readable = [f'(1 - x["{inv_map[abs(lit)]}"])' if lit > 0 else f'x["{inv_map[abs(lit)]}"]' for lit in clause]
        model.add_constraint_NAND(*[eval(y) for y in readable], lam=LAM)

    # Run the experiment and get results
    print(f'[&] Solving {uvl_path} instance ({len(x)} variables)...')
    start_time = time.time()
    model_solution, qubo = solve(model, num_reads)
    end_time = time.time()
    success_msg = '[*] Valid result generated!' if model.is_solution_valid(model_solution) else '[!] No valid solution was found'
    model_value = (- 1) ** is_max * model.value(model_solution) / 10 ** PRECISION

    # Print results
    print(success_msg, f'[{10 ** 3 * (end_time - start_time)} ms]\n')
    print('Results:')
    print('=======')
    print('Constraints apply' if model.is_solution_valid(model_solution) else 'No solution found with restrictions')
    print("Model value:", model_value)
    print('Number of input variables:', len(x))
    print('Number of auxiliary variables:', len(qubo) - len(x))
    print('Number of total variables:', len(qubo))
    print("Variable assignment:", {k: int(v) for k, v in model_solution.items()})

    # Write the solution configuration
    if not os.path.exists('./output'):
        os.mkdir('./output')
    output_path = f'./output/{uvl_path.split('/')[-1].split('.')[0]}_{'-'.join(columns)}:{'-'.join(rates_str)}_{args[4]}_{num_reads}.config'
    with open(output_path, 'w') as f:
        f.write('\n'.join(list(filter(lambda x: x != None, [(k if v else None) for k, v in model_solution.items()]))))
    
    print("\nThe solution configuration can be found in:", output_path)

if __name__ == "__main__":
    main()
