import glob
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def comparison_calculations(dataset, title):
    latency = dataset[['Edge Latency', 'Cloud Latency']]
    throughput = dataset[['Edge Throughput', 'Cloud Throughput']]

    ax = sns.histplot(data=latency, element='step')
    graph_title = f'{title} Average Latency Comparison'
    ax.set(xlabel='Latency Times (sec)', title=graph_title)
    plt.tight_layout()
    plt.savefig(f'graphs/{graph_title}_latency.png')
    plt.clf()

    ax = sns.histplot(data=throughput, element='step')
    graph_title = f'{title} Average Throughput Comparison'
    ax.set(xlabel='Throughput (Mbps)', title=graph_title)
    plt.tight_layout()
    plt.savefig(f'graphs/{graph_title}_throughput.png')
    plt.clf()    

for type in ['Cloud ', 'Fish ']:
    light_data = [[], [], []]
    dark_data = [[], [], []]

    for file in glob.glob(f'calculations/{type}*'):
        with open(file, 'r') as f:
            lines = f.readlines()
            if 'light' in file:
                light_data[0].append(float(lines[0].split(':')[1]))
                light_data[1].append(float(lines[1].split(':')[1]))
                light_data[2].append(float(lines[2].split(':')[1]))
            else:
                dark_data[0].append(float(lines[0].split(':')[1]))
                dark_data[1].append(float(lines[1].split(':')[1]))
                dark_data[2].append(float(lines[2].split(':')[1]))
    
    if type == 'Cloud ':
        cloud_light = light_data
        cloud_dark = dark_data
    else:
        edge_light = light_data
        edge_dark = dark_data

light_comp = edge_light
light_comp.extend(cloud_light)
light_comp_df = pd.DataFrame(light_comp).T
light_comp_df = light_comp_df.set_axis(['Edge Latency', 'edge_std', 'Edge Throughput', 'Cloud Latency', 'cloud_std', 'Cloud Throughput'], axis=1, inplace=False)

dark_comp = edge_dark
dark_comp.extend(cloud_dark)
dark_comp_df = pd.DataFrame(dark_comp).T
dark_comp_df = dark_comp_df.set_axis(['Edge Latency', 'edge_std', 'Edge Throughput', 'Cloud Latency', 'cloud_std', 'Cloud Throughput'], axis=1, inplace=False)

comparison_calculations(light_comp_df, 'Light')
comparison_calculations(dark_comp_df, 'Dark')