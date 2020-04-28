import scipy.stats as stats
import seaborn as sns


def get_joint_distribution(df):
    sns.jointplot("SAT", "motivation", df)
    print(
        "The Pearson correlation coefficient is {:7.3f}".format(
            stats.pearsonr(df["SAT"], df["motivation"])[0]
        )
    )
