import matplotlib.pyplot as plt


def plot_conditional_distribution(df):

    fig, (ax1, ax2) = plt.subplots(1, 2)
    fig.suptitle("Conditional distribution")
    ax1.hist(df.query("D == 1")["Y"], density=True)
    ax2.hist(df.query("D == 0")["Y"], density=True)

    ax1.set_xlabel("$Y | D = 1$")
    ax2.set_xlabel("$Y | D = 0$")

    ax1.set_xlim([0, 3])
    ax2.set_xlim([0, 3])

    ax1.set_ylabel("Density")


def plot_interventional_distribution(Y_do_1, Y_do_0):

    fig, (ax1, ax2) = plt.subplots(1, 2)
    fig.suptitle("Interventional distribution")

    ax1.hist(Y_do_1, density=True)
    ax2.hist(Y_do_0, density=True)

    ax1.set_xlabel(r"$Y \mid do(D = 1)$")
    ax2.set_xlabel(r"$Y \mid do(D = 0)$")

    ax1.set_xlim([0, 3])
    ax2.set_xlim([0, 3])

    ax1.set_ylabel("Density")
