import matplotlib.pyplot as plt
import seaborn as sns


def plot_choices(df, label):

    fig, ax = plt.subplots()

    df.groupby("Period")["Choice"].value_counts(normalize=True).loc[
        :10
    ].unstack().plot.bar(stacked=True, ax=ax)

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
