import numpy as np
import matplotlib.pyplot as plt


def plot_logistic(df_left, df_right, probs):

    # draw the plot
    fig, ax = plt.subplots()
    ax.set_xlim(-0.25, 0.25)
    ax.set_xticks(np.arange(-0.25, 0.251, step=0.05))
    ax.set_ylim(0.0, 1.0)
    ax.set_yticks(np.arange(0.0, 1.01, step=0.1))

    ax.axvline(0.0, linestyle=":")
    ax.plot(df_left["difshare"], probs["left"], label="Logit fit")
    ax.plot(df_right["difshare"], probs["right"], label="Logit fit")
    ax.set_xlabel("Vote Share Margin of Victory, Election t")
    ax.set_ylabel("Probability of Winning Election t+1")
    ax.legend()
