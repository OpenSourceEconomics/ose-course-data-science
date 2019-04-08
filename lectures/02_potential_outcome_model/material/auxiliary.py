import matplotlib

import matplotlib.pyplot as plt
import scipy.stats as ss
import pandas as pd
import numpy as np

from matplotlib.ticker import MaxNLocator


def plot_individual_specific_effects(with_parameters=None):
    fig, ax = plt.subplots(1, 1)
    x = np.linspace(-5, 5, 5000)
    pdf = ss.norm.pdf(x, 0, 1)
    ax.plot(x, pdf)
    
    ax.set_xlabel('$\delta$')
    ax.set_ylabel('Density')
    ax.set_xticklabels(['', '', '', 0, '', '', ''])
    ax.set_xlim([-3, 3])
    ax.set_ylim([0, 0.5])
    
    ax.yaxis.set_major_locator(MaxNLocator(prune='both'))
    
    if with_parameters:
        pos = with_parameters
        ax.axvline(x=pos[0], linewidth=3, label='ATE', color='red')
        ax.axvline(x=pos[2], linewidth=3, label='ATT', color='orange')
        ax.axvline(x=pos[1], linewidth=3, label='ATC', color='green')
        ax.legend()        
    
    
    
def get_illustrative_lalonde_data():
    df = pd.read_pickle('../../datasets/processed/angrist_pischke/nswre74.pkl')

    np.random.seed(123)
    df = df[['treat', 're78']].sample(frac=1)
    np.random.seed(None)
    
    is_treated = df['treat'] == 1

    df['Y'] = df['re78']
    df['Y_0'] = df.loc[~is_treated, 're78']
    df['Y_1'] = df.loc[is_treated, 're78']

    df['D'] = 0
    df.loc[is_treated, 'D'] = 1

    return df