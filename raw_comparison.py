import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def comparison_calculations(dataset, title):
    ax = sns.histplot(data=dataset, element='step', kde=True)
    graph_title = f'{title} Average Latency Comparison'
    ax.set(xlabel='Latency Times (sec)', title=graph_title)
    plt.tight_layout()
    plt.savefig(f'graphs/{graph_title}_latency.png')
    plt.clf()

glb = pd.read_csv('raw_data/Default.csv')
gltf = pd.read_csv('raw_data/gltf.csv')

combined = pd.DataFrame()
combined['GLB'] = glb['light']
combined['GLTF'] = gltf['light']

comparison_calculations(combined, 'File Type')