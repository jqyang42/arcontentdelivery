import pandas as pd
import numpy as np
import glob

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
    'gltf' : {'light' : 709.804736, 'dark' : 101.5808}
}

for filename in glob.glob(f'raw_data/*k.csv'):
    file = filename[filename.index('/') + 1 : filename.index('.')]
    data = pd.read_csv(filename)
    data['throughput'] = file_model_Mb[file] / data['light']
    std = np.std(data['throughput'])
    print(f'{file} throughput std: {std}')