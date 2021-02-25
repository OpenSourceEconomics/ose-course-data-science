import matplotlib.pyplot as plt
import numpy as np

def plot_educ_against_yob(df):

    mean_educ = df.groupby(['YOB', 'QOB'])['EDUC'].mean()

    df_index = mean_educ.index.to_frame().reset_index(drop = True)
    x_values = df_index.apply(lambda x: x[0] + x[1] * 0.25 - 0.25, axis = 1)

    y_values = mean_educ.values

    _, ax = plt.subplots(1, 1, figsize = (10, 5))
    ax.plot(x_values, y_values, color = '0.5')

    colors = ['b', 'g', 'r', 'c']

    for i in range(4):

        points = np.array(list(zip(x_values, y_values)))[i::4]

        ax.scatter(points[:, 0], points[:, 1], marker = 's', s = 34, color = colors[i], label = i + 1)

    ax.set_xlabel('Year of Birth')
    ax.set_ylabel('Years Of Completed Education')

    ax.legend(title = "Quarter")

def plot_bar_detrended_educ(df):

    df_index = df.index.to_frame().reset_index(drop = True)

    x_values = df_index.apply(lambda x: x[0] + x[1] * 0.25 - 0.25, axis = 1).to_numpy()
    y_values = df['DTRND'][:len(x_values)].to_numpy()

    _, ax = plt.subplots(1,1)

    colors= ['b', 'g', 'r', 'c']

    for i in range(4):
        
        points = np.array(list(zip(x_values, y_values)))[i::4]

        ax.bar(points[:, 0], points[:, 1], width = 0.25, color= colors[i], label = i + 1)

    ax.set_xlabel('Year of Birth')
    ax.set_ylabel('Schooling Differential')

    ax.legend(title = "Quarter")

def plot_log_wkly_earnings_by_qob(df):

    mean_lwklywge = df.groupby(['YOB', 'QOB'])['LWKLYWGE'].mean()

    df_index = mean_lwklywge.index.to_frame().reset_index(drop = True)
    x_values = df_index.apply(lambda x: x[0] + x[1] * 0.25 - 0.25, axis = 1)

    y_values = mean_lwklywge.values

    _, ax = plt.subplots(1, 1)
    ax.plot(x_values, y_values, color = '0.5')  

    colors = ['b', 'g', 'r', 'c']

    for i in range(4):

        points = np.array(list(zip(x_values, y_values)))[i::4]
        ax.scatter(points[:, 0], points[:, 1], marker = 's', s = 34, color = colors[i], label = i + 1)

    ax.set_xlabel('Year of Birth')
    ax.set_ylabel('Log Weekly Earnings')

    ax.legend(title = "Quarter")
