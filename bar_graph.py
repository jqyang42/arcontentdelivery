import glob
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd

def graph_bar(data, title, units):
    light_data = data[data['model'] == 'light']
    ax = sns.barplot(data=light_data, x='triangle', y=title)
    graph_title = f'Compression Average {title} Comparison'
    ax.set(xlabel='Fish Model by Triangle Count', ylabel=f'{title} ({units})', title=graph_title)
    plt.tight_layout()
    plt.savefig(f'graphs/{graph_title}_barplot.png')
    plt.clf()

latency = [[], [], []]
throughput = [[], [], []]
data = [latency, throughput]
for file in glob.glob(f'calculations/Fish*'):
    with open(file, 'r') as f:
        lines = f.readlines()
        for i in range(len(data)):
            data[i][0].append(int(file[(file.index('Fish ') + 5):(file.index('k'))]))
            data[i][1].append(file[(file.index('_') + 1):(file.index('.txt'))])
            data[i][2].append(float(lines[i * 2].split(':')[1]))

latency_df = pd.DataFrame(data[0]).T
latency_df = latency_df.set_axis(['triangle', 'model', 'Latency'], axis=1, inplace=False)
latency_df = latency_df.sort_values('triangle')
latency_df['triangle'] = latency_df['triangle'].astype(str)
latency_df['triangle'] += 'k'

throughput_df = pd.DataFrame(data[1]).T
throughput_df = throughput_df.set_axis(['triangle', 'model', 'Throughput'], axis=1, inplace=False)
throughput_df = throughput_df.sort_values('triangle')
throughput_df['triangle'] = throughput_df['triangle'].astype(str)
throughput_df['triangle'] += 'k'

graph_bar(latency_df, 'Latency', 'sec')
graph_bar(throughput_df, 'Throughput', 'Mbps')