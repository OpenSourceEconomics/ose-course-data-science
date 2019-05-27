import matplotlib.pyplot as plt
from scipy.stats import logistic


def get_plot_probability(version, grid, probs):
    fig, ax = plt.subplots(1, 1)
    ax.yaxis.get_major_ticks()[0].set_visible(False)

    ax.plot(grid, probs)
    plt.plot((0.25, 0.25), (0, 1), '--', color='grey')
    
    ax.set_title('{:} design'.format(version.capitalize()), fontsize=25)
    ax.set_xlabel('Z')
    ax.set_ylabel('Probability')
    ax.set_ylim([0.00, 1.09])
    ax.set_xlim([0, 1])
    
    
def get_treatment_probability(version, grid):
    """This function assigns a probability of treatment assignment around
    the example's cutoff.
    """
    probs = list()
    for z in grid:
        if version=='sharp':
            if z > 0.25:
                rslt = 1
            else:
                rslt = 0
                
        elif version=='fuzzy':
            rslt = logistic.cdf((z - 0.25) * 20) 
            if z > 0.25:
                rslt = min(rslt + 0.1, 1.0)
            elif z <= 0.25:
                rslt = max(rslt - 0.1, 0.0)
        probs.append(rslt)  
        
    return probs

def observed_outcome(grid, version):
    outcome_treated = get_potential_outcomes(grid, 'treated')
    outcome_control = get_potential_outcomes(grid, 'control')

    rslt = []
    for i, prob in enumerate(get_treatment_probability(version, grid)):
        rslt += [prob * outcome_treated[i] + (1 - prob) * outcome_control[i]]

    return rslt

def get_potential_outcomes(grid, group):
    if group == 'treated':
        y_values = 0.2 + grid * 0.2
    else:
        y_values = -0.2 + grid * 0.2

    return y_values


def plot_outcomes(version, grid):
    ax = plt.figure().add_subplot(111)
    ax.yaxis.get_major_ticks()[0].set_visible(False)

    y_values = get_potential_outcomes(grid, 'treated')
    ax.plot(grid, y_values, label='Treated')

    y_values = get_potential_outcomes(grid, 'control')
    ax.plot(grid, y_values, label='Control')

    y_values = observed_outcome(grid, version)
    ax.plot(grid, y_values, label='Observed', linestyle='--', color='black')
    ax.legend()
    ax.set_title('{:} design'.format(version.capitalize()), fontsize=25)

    ax.set_xlabel('Z')
    ax.set_ylabel('Outcomes')
