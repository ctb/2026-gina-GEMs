import sys
import pandas as pd
import os
from cobra.core.configuration import Configuration
from cobra.io import load_json_model, save_json_model
from imatpy.parse_gpr import gene_to_rxn_weights
from imatpy.model_creation import generate_model
import argparse

def main():
    p = argparse.ArgumentParser()
    p.add_argument('input_csv', help='threshold CSV')
    p.add_argument('-o', '--output-model', help='save optimized model here')

    os.environ['GRB_LICENSE_FILE'] = '/home/ctbrown/.gurobi.lic'
    Configuration().solver = "gurobi"

    base_model = load_json_model("STM_v1_0.json")

    stm_threshold = pd.read_csv(args.input_csv)
    stm_set = set(stm_threshold["genes"].astype(str).str.strip())
    print(len(stm_set))

    model_genes = set([g.id for g in base_model.genes ])

    overlap = stm_set.intersection(model_genes)
    print(len(overlap))

    model_xxx = stm_threshold[stm_threshold["genes"].isin(model_genes)]

    subset_weights = model_xxx.set_index("genes")["threshold_category"].reindex(model_genes, fill_value=0)

    rxn_weights = gene_to_rxn_weights(base_model, subset_weights)

    print(len(rxn_weights))

    print('generating new model with imat generate_model')
    new_model = generate_model(model=base_model, rxn_weights=rxn_weights, method="imat_restrictions")

    save_json_model(new_model, args.output_model)

    print('running FBA on original model')
    old_fba = base_model.optimize()
    print(old_fba.objective_value)

    print('running FBA on new model')
    new_fba = new_model.optimize()
    print(new_fba.objective_value)


if __name__ == '__main__':
    sys.exit(main())
