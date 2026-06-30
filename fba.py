from cobra.io import load_model, load_json_model
from cobra.summary import model_summary

# load the input S.Tm LT2 GEM
base_model = load_json_model("STM_v1_0.json")

# load the stm models generated in `comparing_model_0513.ipynb`
stm1090_model = load_json_model("stm1090_imat_restrictions.json")
# run FBA
fba_base = base_model.optimize()
fba_stm1090 = stm1090_model.optimize()

# see results
print(fba_base.objective_value)
print(fba_stm1090.objective_value)

# "~/stm_model_test/comparing_models_0513.ipynb" is the notebook we worked on together and I got different FBA results for each model 
# I loaded the models from the "~/stm_model_test/meeting_052026.ipynb" 
