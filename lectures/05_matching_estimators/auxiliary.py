from collections import OrderedDict

from mpl_toolkits.mplot3d import Axes3D
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def get_potential_outcomes(a, b):
    """ Get potential outcomes.
    
    This function calculates the potential outcomes based on the 
    functional from as described in our textbook on p. 153.
    
    Args:
        a: a float
        b: a float
    
    Returns:
        A list with the individuals potential outcomes.
    """
    v_0, v_1 = np.random.normal(0, 5, size=2)
    y_0 = 100.0 + 3.0 * a + 2.0 * b + v_0
    y_1 = 102.0 + 6.0 * a + 4.0 * b + v_1
    return [y_1, y_0]
    

def get_propensity_score_3(df, specification='true'):
    assert specification in ['correct', 'misspecified', 'true']
    if specification == 'true':
        
        p = df['p']
    elif specification == 'correct':
        p = smf.logit(formula='d ~ a + b + a * b', data=df).fit().predict()
    elif specification == 'misspecified':
        p = smf.logit(formula='d ~ a + b', data=df).fit().predict()
    
    return p
    
def get_sample_matching_demonstration_3(a_grid, b_grid):
    sample = list()

    counts = np.tile(np.nan, (3, 100, 100))
    
    for i, a in enumerate(a_grid):
        for j, b in enumerate(b_grid):

            prob = get_propensity_score(a, b)

            # Now we determine the number of observed individuals
            for k, is_treat in enumerate([True, False]):
                if is_treat:
                    lambda_ = prob
                else:
                    lambda_ = 1.0 - prob

                num_sample = np.random.poisson(lambda_)
                counts[k, i, j] = num_sample
                
                for _ in range(num_sample):
                    d = np.random.choice([1, 0], p=[prob, 1 - prob])
                    y_1, y_0 = get_potential_outcomes(a, b)
                    y = d * y_1 + (1 - d) * y_0

                    sample += [[a, b, d, y, y_1, y_0, prob]]
            counts[2, i, j] = np.sum(counts[:2, i, j])
            
    df = pd.DataFrame(sample, columns=['a', 'b', 'd', 'y', 'y_1', 'y_0', 'p'])
    return df, counts

def get_propensity_score(a, b):
    """ Get probensity score.
    
    This function calculates the propensity based on the
    functional form as described in our textbook on p. 153.
    
    Args:
        a: a float
        b: a float
    
    Returns:
        A float with the individuals propensity score.
    """
    index = 0
    index += -2.0 + 3.0 * a - 3.0 * (a - 0.1) + 2.0 * (a - 0.3)
    index += -2.0 * (a - 0.5) + 4.0 * (a - 0.7) - 4.0 * (a - 0.9)
    index += +1.0 * b - 1.0 * (b - 0.1) + 2.0 * (b - 0.7)
    index += -2.0 * (b - 0.9)  + 3.0 * (a - 0.5) * (b - 0.5)
    index += -3.0 * (a - 0.7) * (b - 0.7)
    
    prob = np.exp(index) / (1.0 + np.exp(index))
    
    return prob

def plot_propensity_score(a_grid, b_grid):

    X, Y = np.meshgrid(*(a_grid, b_grid))
    Z = get_propensity_score(X, Y)

    fig = plt.figure()
    ax = plt.axes(projection='3d')
    ax.contour3D(X, Y, Z, 500)
    ax.set_xlabel('a')
    ax.set_ylabel('b')
    ax.set_zlim([0, 1])
    ax.set_zlabel('Propensity Score');
    
    
def get_sample_matching_demonstration_2(num_agents):
    def get_potential_outcomes(s):
        if s == 1:
            y_1, y_0 = -99, 2
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

        
    data = np.tile(np.nan, (num_agents, 5))
    for i in range(num_agents):
        u = np.random.uniform()

        if 0.00 <= u < 0.40:
            s, d = 1, 0
        elif 0.40 <= u < 0.50:
            s, d = 2, 0
        elif 0.50 <= u < 0.60:
            s, d = 3, 0
        elif 0.60 <= u < 0.73:
            s, d = 2, 1
        else:
            s, d = 3, 1


        y_1, y_0 = get_potential_outcomes(s)
        y = d * y_1 + (1 - d) * y_0  
        
        data[i, :] = y, d, s, y_1, y_0

    info = OrderedDict()
    info['Y'] = np.float
    info['D'] = np.int
    info['S'] = np.int
    info['Y_1'] = np.float
    info['Y_0'] = np.float
    
    df = pd.DataFrame(data, columns=info.keys())
    df = df.astype(info)
    df.replace(-99, np.nan, inplace=True)
    
    return df


def get_sample_matching_demonstration_4():
    # This allows to run it locally but also check out the files from an online 
    # repository.
    try:
        df = pd.read_csv('../../datasets/processed/morgan_winship/mw_cath1.csv')
    except:
        url = 'https://raw.githubusercontent.com/HumanCapitalAnalysis/microeconometrics/master/datasets/processed/morgan_winship/mw_cath1.csv'
        df = pd.read_csv(url)
    return df

def get_propensity_scores_matching_demonstration_4(df, specification='complete'):
    assert specification in ['complete', 'incomplete']
    def get_columns_for_estimation(specification):
        columns = df.columns.to_list()
        
        labels_removed = ['y', 'yt', 'yc', 'dshock', 'd', 'treat']
        if specification == 'incomplete':
            labels_removed += ['test', 'testsq']
        
        for label in labels_removed:
            columns.remove(label)
        
        return columns
                
    # complete specification
    columns = get_columns_for_estimation(specification)
    formula = 'treat ~ {:}'.format(' + '.join(columns))      
    prob = smf.logit(formula=formula, data=df).fit().predict()   

    return prob

def get_sparsity_pattern_overall(counts):
    fig, ax = plt.subplots(1, 1)
    ax.spy(counts[2, :, :])
    ax.set_title('Sparsity pattern', pad=15)
    
def get_sparsity_pattern_by_treatment(counts):
    fig, (ax1, ax2) = plt.subplots(1, 2)
    ax1.spy(counts[0, :, :])
    ax1.set_title('Treated', pad=15)

    ax2.spy(counts[1, :, :])
    ax2.set_title('Untreated', pad=15)

    fig.suptitle('Sparsity pattern')
    
def get_common_support(df, label='d'):

    
    prob = df['p']

    prob_untreated = df['p'][df[label] == 0]
    prob_treated = df['p'][df[label] == 1]

    fig, ax = plt.subplots(1, 1)
    bins = np.linspace(0.01, 1.00, 100)
    ax.hist([prob_untreated, prob_treated], bins=bins, label=['control', 'treated'])
    ax.set_xlim([0, 1])
    ax.set_xlabel('Propensity score')
    ax.legend();
    
def get_lalonde_data():
    df = pd.read_csv('../../datasets/processed/angrist_pischke/nswre74.csv')

    df['Y'] = df['re78']
    df['Y_0'] = df.loc[df['treat'] == 0, 're78']
    df['Y_1'] = df.loc[df['treat'] == 1, 're78']

    df['D'] = 0
    df.loc[df['treat'] == 1, 'D'] = 1
    
    return df

def plot_weights():
    
    x_grid = np.linspace(0.01, 0.99, 100)
    inv_odds_grid = list()
    odds_grid = list()
    for x in x_grid:
        odds_grid.append(get_odds(x))
        inv_odds_grid.append(get_inv_odds(x))

    fig, ax = plt.subplots(1, 1)
    ax.plot(x_grid, odds_grid, label='ATT') 
    ax.plot(x_grid, inv_odds_grid, label='ATC') 
    ax.set_xlim([0, 1])
    ax.set_ylabel('Weight')
    ax.set_xlabel('Propensity score')
    ax.legend()
    
def get_odds(p):
    return p / (1 - p)

def get_inv_odds(p):
    return (1 - p) / p