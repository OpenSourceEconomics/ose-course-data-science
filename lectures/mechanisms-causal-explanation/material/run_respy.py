import pandas as pd
import respy as rp


# TODO: Add to CI, set up debug
params, options, df_obs = rp.get_example_model("kw_97_basic")
params = pd.read_pickle("params_revised.pkl")

simulate_func = rp.get_simulate_func(params, options)
df_sim = simulate_func(params)
df_sim.to_pickle("df_sim.pkl")

params_pol = params.copy()
params_pol.loc[("nonpec_school", "hs_graduate"), "value"] += 2000
df_pol = simulate_func(params_pol)
df_pol.to_pickle("df_pol.pkl")



