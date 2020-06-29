import os

import pandas as pd
import respy as rp


params, options, df_obs = rp.get_example_model("kw_97_basic")
params = pd.read_pickle("params_revised.pkl")
label = ("nonpec_school", "hs_graduate")

# We need to save on memory when running the script under CI.
if "CI" in os.environ:
    params, options, df_obs = rp.get_example_model("kw_94_one")
    label = ("nonpec_edu", "at_least_twelve_exp_edu")

simulate_func = rp.get_simulate_func(params, options)
df_sim = simulate_func(params)
df_sim.to_pickle("df_sim.pkl")

params_pol = params.copy()
params_pol.loc[label, "value"] += 2000
df_pol = simulate_func(params_pol)
df_pol.to_pickle("df_pol.pkl")
