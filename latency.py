import glob
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd

file_model_Mb = {
    'Default' : 148.00352,
    'Fish 100k' : 45.472128,
    'Fish 200k' : 64.0528,
    'Fish 400k' : 148.00352,
    'Fish 2k' : 24.807808,
    'Fish 20k' : 29.271456,
    'Busy Network' : 0,
    'Cloud 100k' : 45.472128,
    'Cloud 200k' : 64.0528,
    'Cloud 400k' : 148.00352,
    'Cloud 2k' : 24.807808,
    'Cloud 20k' : 29.271456, 
}

def latency_calculations(dataset, title):
    for context in ['light', 'dark']:
        mean = np.mean(dataset[context])
        std = np.std(dataset[context])
        with open(f'calculations/{title}_{context}.txt', 'w') as f:
            f.write(f'mean: {mean}\n')
            f.write(f'std: {std}\n')
            f.write(f'throughput: {file_model_Mb[title] / mean}\n')

    ax = sns.histplot(data=dataset, element='step')
    graph_title = f'{title} Model Latency'
    ax.set(xlabel='Latency Times (sec)', ylabel='Count', title=graph_title)
    plt.tight_layout()
    plt.savefig(f'graphs/{graph_title}.png')
    plt.clf()

for folder in glob.glob(f'trials/*'):
    light_times = []
    dark_times = []

    for filename in glob.glob(f'{folder}/*.txt'):
        with open(filename, 'r') as f:
            lines = f.readlines()
            for line in lines:
                values = line.split(':')
                if 'light' in values[0]:
                    light_times.append(float(values[3]))
                else:
                    dark_times.append(float(values[3]))

    light_times_np = np.array(light_times)
    dark_times_np = np.array(dark_times)
    times = pd.DataFrame(np.hstack((light_times_np[:,None], dark_times_np[:,None])), columns=['light', 'dark'])
    latency_calculations(times, folder[7:])
