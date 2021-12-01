import glob
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

light_times = []
dark_times = []
for filename in glob.glob('fish_200kTrials/*.txt'):
    with open(filename, 'r') as f:
        lines = f.readlines()
        for line in lines:
            values = line.split(':')
            if 'light' in values[0]:
                light_times.append(float(values[3]))
            else:
                dark_times.append(float(values[3]))

light_times = np.array(light_times)
dark_times = np.array(dark_times)

def latency_calculations(dataset, title):
    mean = np.mean(dataset)
    std = np.std(dataset)
    with open(f'calculations/{title}.txt', 'w') as f:
        f.write(f'mean: {mean}\n')
        f.write(f'std: {std}\n')

    ax = sns.histplot(data=dataset, kde=True)
    graph_title = f'{title} Latency'
    ax.set(xlabel='Latency Times', title=graph_title)
    plt.savefig(f'graphs/{graph_title}.png')
    plt.clf()

latency_calculations(dark_times, 'Fish 200k Dark Model')
latency_calculations(light_times, 'Fish 200k Light Model')
