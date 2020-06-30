import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd


def simulate_causal_graph():

    alpha_D = 1
    alpha_Y = 1
    alpha_M = 1
    alpha_N = 1

    beta_G = -0.7
    beta_F = 0.2
    beta_A = 0.8
    beta_B = 0.7
    beta_C = 0.9
    beta_DM = 0.4
    beta_DN = 0.5
    beta_YM = 0.5
    beta_YN = 0.6

    # distributional assumptions
    get_unobservable = np.random.normal
    get_observable = np.random.uniform

    num_agents = 10000
    data = np.tile(np.nan, (num_agents, 9))
    for i in range(num_agents):
        G = get_observable()
        F = get_observable()
        A = get_observable()
        B = get_observable()
        C = get_observable()
        D = alpha_D + beta_A * A + beta_B * B + beta_C * C + get_unobservable()
        M = alpha_M + beta_DM * D + get_unobservable()
        N = alpha_N + beta_DN * D + get_unobservable()
        Y = alpha_Y + beta_YM * M + beta_YN * N + beta_F * F + beta_G * G + get_unobservable()
        data[i, :] = [Y, D, G, F, A, B, C, M, N]

    df = pd.DataFrame(data, columns=["Y", "D", "G", "F", "A", "B", "C", "M", "N"])
    return df


def plot_choices(df, label):

    fig, ax = plt.subplots()

    df.groupby("Period")["Choice"].value_counts(normalize=True).loc[:10].unstack().plot.bar(
        stacked=True, ax=ax
    )

    ax.xaxis.set_tick_params(rotation=0)

    ax.set_title(label)
    ax.legend(loc="lower center", bbox_to_anchor=(0.5, -0.275), ncol=5)

    plt.show()


def plot_wage_distribution(df_sim, df_pol):

    for label, df in [("Simulated", df_sim), ("Policy", df_pol)]:
        fig, ax = plt.subplots()

        sns.distplot(df.loc[(slice(None), 49), "Wage"], ax=ax, hist=True)

        ax.set_ylim([0, 0.000002])
        ax.set_xlim([0, 2500000])

        ax.set_title(label)

        plt.show()


def plot_final_human_capital(df_sim, df_pol):

    columns = [
        "Experience_Blue_Collar",
        "Experience_Military",
        "Experience_White_Collar",
        "Experience_School",
    ]

    x = [
        "Blue Collar",
        "Military",
        "White Collar",
        "School",
    ]

    for label, df in [("Simulated", df_sim), ("Policy", df_pol)]:

        fig, ax = plt.subplots()

        ax.bar(x, df.groupby("Identifier").last()[columns].mean())
        ax.set_ylim([0, 32])
        ax.set_title(label)

        plt.show()
