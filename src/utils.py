#!/usr/bin/env python

# Libraries
from flamapy.core.discover import DiscoverMetamodels
from qubovert import boolean_var
from neal import SimulatedAnnealingSampler

import time
import pandas as pd

# Constant fixing the number of decimal places considered in the weights
PRECISION = 8

# Get clauses in CNF with flamapy
def get_cnf(uvl_path):
    dm = DiscoverMetamodels()
    feature_model = dm.use_transformation_t2m(uvl_path,'fm')
    sat_model = dm.use_transformation_m2m(feature_model,"pysat")
    clauses = sat_model.get_all_clauses()

    var_map = {k: v for k, v in sat_model.variables.items()}
    inv_map = {v: k for k, v in var_map.items()}
    return clauses, var_map, inv_map

# Load variable weights
def load_weights(csv_path, columns, rates, mins):
    w = {}
    df = pd.read_csv(csv_path)[[*columns]]
    normalised_df = (df - df.min()) / (df.sum() - df.min())
    normalised_df.insert(loc=0, column='features', value=pd.read_csv(csv_path)[['features']])
    pairs = normalised_df.values.tolist()
    for feature, *values in pairs:
        w[feature] = 10 ** PRECISION * sum(min_coef * rate * value for rate, value, min_coef in zip(rates, values, mins))
    return w

# Create model
def build_model(var_map, inv_map, w, clauses):
    # Implement the objective function g_w using the weights and qubovert
    model = 0
    x = {key: boolean_var(key) for key in var_map.keys()}
    for key in var_map.keys():
        # is_max set the negative sign for the weights
        model += w[key] * x[key]

    # Implement the restriction function h_r using the clauses
    LAM = 10 ** (PRECISION + 5)
    for clause in clauses:
        readable = [f'(1 - x["{inv_map[abs(lit)]}"])' if lit > 0 else f'x["{inv_map[abs(lit)]}"]' for lit in clause]
        model.add_constraint_NAND(*[eval(y) for y in readable], lam=LAM)
    return model, x

# Run the experiment and get results
def run(model, num_reads, csv_path, columns, rates):
    start_time = time.time()
    model_solution, qubo = solve(model, num_reads)
    end_time = time.time()
    total_time = end_time - start_time

    conf = list(filter(lambda x: x != None, [(k if v else None) for k, v in model_solution.items()]))
    model_value = 0
    df_not_normalised = pd.read_csv(csv_path)[['features', *columns]]
    for feature in conf:
        for i, column in enumerate(columns):
            model_value += df_not_normalised[column][df_not_normalised['features'] == feature].values[0] * rates[i]
    
    solution = dict()
    solution['model_solution'] = model_solution
    solution['qubo'] = qubo
    solution['model_value'] = model_value
    solution['total_time'] = total_time
    solution['conf'] = conf
    return solution

# Solve the model using dwave-neal with a certain number of reads
def solve(model, num_reads):
    qubo = model.to_qubo()
    dwave_qubo = qubo.Q
    res = SimulatedAnnealingSampler().sample_qubo(dwave_qubo, num_reads=num_reads)
    qubo_solution = res.first.sample
    model_solution = model.convert_solution(qubo_solution)
    return model_solution, qubo
