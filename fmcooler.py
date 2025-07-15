#!/usr/bin/env python

import sys
from operator import itemgetter
import os
from src.utils import *

# Main function
def main():
    # Parse arguments
    args = sys.argv
    if len(args) != 5:
        print('[!] Input error\n')
        print('[1] The file of the Feature Model in UVL format must be specified as first parameter')
        print('[2] The file of weights must be specified as second parameter')
        print('[3] vars:rates:min must be specified as third parameter, where:')
        print('    - vars are the used columns (separted by commas)')
        print('    - rates are the weights for each varaible in multi-criteria (separted by commas)')
        print('    - min are the strings "min" or "max", to MINIMIZE or MAXIMIZE (separted by commas)')
        print('[4] The number of reads must be specified as fifth parameter')
        exit(-1)
    print('[&] Reading model with flamapy and generating CNF to perfom restrictions in QUBO')
    uvl_path = args[1]
    csv_path = args[2]
    columns, rates_str, mins_str = tuple(map(lambda x: x.split(','), args[3].split(':')))
    rates = list(map(float, rates_str))
    mins = list(map(lambda x: 1 if x == 'min' else -1, mins_str))
    num_reads = int(args[4])

    # Get clauses in CNF with flamapy
    clauses, var_map, inv_map = get_cnf(uvl_path)
    # Load variable weights
    w = load_weights(csv_path, columns, rates, mins)
    # Create model
    model, x = build_model(var_map, inv_map, w, clauses)
    # Run the experiment and get results
    print(f'[&] Solving {uvl_path} instance ({len(x)} variables)...')
    solution = run(model, num_reads, csv_path, columns, rates)
    model_solution, qubo, model_value, total_time, conf = itemgetter('model_solution', 'qubo', 'model_value', 'total_time', 'conf')(solution)

    # Print results
    success_msg = '[*] Valid result generated!' if model.is_solution_valid(model_solution) else '[!] No valid solution was found'
    print(success_msg, f'[{10 ** 3 * total_time} ms]\n')
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
        f.write('\n'.join(conf))
    
    print("\nThe solution configuration can be found in:", output_path)

if __name__ == "__main__":
    main()
