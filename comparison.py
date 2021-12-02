import glob
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

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

def comparison_calculations(dataset, title):
    for context in ['edge', 'cloud']:
        mean = np.mean(dataset[context])
        std = np.std(dataset[context])
        with open(f'calculations/{title}_{context}.txt', 'w') as f:
            f.write(f'mean: {mean}\n')
            f.write(f'std: {std}\n')
            f.write(f'throughput: {file_model_Mb[title] / mean}\n')

    ax = sns.histplot(data=dataset, element='step')
    graph_title = f'{title} Model Latency'
    ax.set(xlabel='Latency Times', title=graph_title)
    plt.tight_layout()
    plt.savefig(f'graphs/{graph_title}.png')
    plt.clf()

for type in ['Cloud ', 'Fish ']:
    light = []
    dark = []
    for file in glob.glob(f'calculations/{type}*'):
        with open(file, 'r') as f:
            lines = f.readlines()
            for line in lines:
                values = line.split(':')
                if 'light' in values[0]:
                    light.append(float(values[3]))
                else:
                    dark.append(float(values[3]))
    
    if type == 'Cloud ':
        cloud_light_np = np.array(light)
        cloud_dark_np = np.array(dark)
    else:
        edge_light_np = np.array(light)
        edge_dark_np = np.array(dark)

light_comp = pd.DataFrame(np.hstack((edge_light_np[:,None], cloud_light_np[:,None])), columns=['edge', 'cloud'])
dark_comp = pd.DataFrame(np.hstack((edge_dark_np[:,None], cloud_dark_np[:,None])), columns=['edge', 'cloud'])
comparison_calculations(light_comp, 'Light Comparison')