import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import statsmodels.formula.api as smf


def get_sample_demonstration_1(num_agents):
    data = np.tile(np.nan, (num_agents, 5))
    for i in range(num_agents):
        u = np.random.uniform()

        if 0.00 <= u < 0.36:
            s, d = 1, 0
        elif 0.36 <= u < 0.48:
            s, d = 2, 0
        elif 0.48 <= u < 0.60:
            s, d = 3, 0
        elif 0.60 <= u < 0.68:
            s, d = 1, 1
        elif 0.68 <= u < 0.80:
            s, d = 2, 1
        else:
            s, d = 3, 1

        # get potential outcomes
        def get_potential_outcomes(s):
            if s == 1:
                y_1, y_0 = 4, 2
            elif s == 2:
                y_1, y_0 = 8, 6
            elif s == 3:
                y_1, y_0 = 14, 10
            else:
                raise AssertionError
            
            # We want some randomness
            y_1 += np.random.normal()
            y_0 += np.random.normal()
                
            return y_1, y_0

        y_1, y_0 = get_potential_outcomes(s)
        y = d * y_1 + (1 - d) * y_0  



        data[i, :] = y, d, s, y_1, y_0

    df = pd.DataFrame(data, columns=['Y', 'D', 'S', 'Y_1', 'Y_0'])
    df = df.astype({'D': np.int, 'S': np.int})

    return df

def plot_conditional_expectation_demonstration_1(df):

    fig, ax = plt.subplots(1, 1)
    rslt = df[df['D'] == 1].groupby('S')['Y'].mean().to_dict()
    x, y = rslt.keys(), rslt.values()
    ax.plot(x, y, label='Treated')

    rslt = df[df['D'] == 0].groupby('S')['Y'].mean().to_dict()
    x, y = rslt.keys(), rslt.values()
    ax.plot(x, y, label='Control')

    ax.set_title('Conditional Expectations')
    ax.set_xticks([1, 2, 3])    
    ax.set_ylim([0, 16])

    ax.legend()
    
def get_predictions_demonstration_1(df):
    
    df_extend = df.join(pd.get_dummies(df['S'], prefix='S'))
    df_extend['predict_1'] = smf.ols(formula='Y ~ D + S', data = df_extend).fit().predict()
    df_extend['predict_2'] = smf.ols(formula='Y ~ D + S_2 + S_3', data = df_extend).fit().predict()
    df_extend['predict_3'] = smf.ols(formula='Y ~ D + S_2 + S_3 + S_2 * D + S_3 * D', data = df_extend).fit().predict()

    rslt = dict()
    rslt['observed'] = dict()
    rslt['predict_1'] = dict()
    rslt['predict_2'] = dict()
    rslt['predict_3'] = dict()


    for key_, d in [('treated', 1), ('control', 0)]:
        df_subset = df_extend[df_extend['D'] == d]

        # observed outcomes
        rslt['observed'][key_] = df_subset.groupby(['S'])['Y'].mean().to_dict()

        # predicted, model 1
        rslt['predict_1'][key_] = df_subset.groupby(['S'])['predict_1'].mean().to_dict()
        rslt['predict_2'][key_] = df_subset.groupby(['S'])['predict_2'].mean().to_dict()
        rslt['predict_3'][key_] = df_subset.groupby(['S'])['predict_3'].mean().to_dict()

    return rslt

def plot_predictions_demonstration_1(df):
    rslt = get_predictions_demonstration_1(df)

    y = np.array([1, 2, 3])
    fig, (ax1, ax2) = plt.subplots(1, 2)
    for label, ax in [('treated', ax1), ('control', ax2)]:

        ax.bar(y - 0.3, rslt['observed'][label].values(), width=0.2, label='actual')
        ax.bar(y - 0.1, rslt['predict_1'][label].values(), width=0.2, label='first prediction')
        ax.bar(y + 0.1, rslt['predict_2'][label].values(), width=0.2, label='second prediction')
        ax.bar(y + 0.3, rslt['predict_3'][label].values(), width=0.2, label='third prediction')

        ax.set_title(label.title())
        ax.set_ylim([0, 22])
        ax.legend()