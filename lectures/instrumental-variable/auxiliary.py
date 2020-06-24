import matplotlib.pyplot as plt


def get_shares_latent_groups():
    labels = ["Compliers", "Always takers", "Never takers"]

    fig, (ax1, ax2) = plt.subplots(1, 2)
    ax1.pie([0.089, 0.111, 0.8], labels=labels, autopct="%1.1f%%")
    ax1.set_title("Z = 0")
    ax2.pie([0.089, 0.111, 0.8], labels=labels, autopct="%1.1f%%")
    ax2.set_title("Z = 1")
    fig.tight_layout()


def get_outcome_latent_groups():

    fig, (ax1, ax2) = plt.subplots(1, 2)

    x_pos = range(3)

    ax1.bar(x_pos, [50, 60, 50])
    ax1.set_xticks(x_pos)
    ax1.set_xticklabels(["Compliers", "Always takers", "Never takers"], rotation="vertical")
    ax1.set_ylim([0, 80])

    for i, info in enumerate([("$Y^0$", (0, 55)), ("$Y^1$", (1, 65)), ("$Y^0$", (2, 55))]):
        text, point = info
        color = "black"
        if i == 0:
            color = "red"

        ax1.annotate(text, point, ha="center", size=15, color=color)
    ax1.set_title("Z = 0")

    ax2.bar(x_pos, [55.5, 60, 50])
    ax2.set_xticks(x_pos)
    ax2.set_xticklabels(["Compliers", "Always takers", "Never takers"], rotation="vertical")
    ax2.set_ylim([0, 80])

    for i, info in enumerate([("$Y^1$", (0, 60.5)), ("$Y^1$", (1, 65)), ("$Y^0$", (2, 55))]):
        text, point = info

        color = "black"
        if i == 0:
            color = "red"

        ax2.annotate(text, point, ha="center", size=15, color=color)

    ax2.set_title("Z = 1")

    plt.tight_layout()
