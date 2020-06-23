import matplotlib.pyplot as plt
import seaborn as sns, numpy as np
import pandas as pd

def plot_wage_distribution(df_sim, df_pol):

    for label, df in [("Simulated", df_sim), ("Policy", df_pol)]:
        fig, ax = plt.subplots()

        sns.distplot(df.loc[(slice(None), 49), "Wage"], ax=ax, hist=True)

        ax.set_ylim([0, 0.000002])
        ax.set_xlim([0, 2500000])

        ax.set_title(label)

        plt.show()

        
def plot_final_human_capital(df_sim, df_pol):
    
    for label, df in [("Simulated", df_sim), ("Policy", df_pol)]:
        fig, ax = plt.subplots()

        df_pol.groupby("Identifier").last()[columns].mean().plot.bar(ax=ax)
        
        ax.set_title(label)

        plt.show()