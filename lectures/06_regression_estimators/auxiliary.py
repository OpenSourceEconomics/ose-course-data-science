import numpy as np
import pandas as pd
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
    return df