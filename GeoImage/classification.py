import shutil
import os
import fiona
import numpy as np

#path = '/Users/guoqiushi/Documents/data/project/classification_shape'
path = '/Users/guoqiushi/Documents/data/project/large_version/price_shape'
label_list = []


def label(path):
    price_list = []
    feature = fiona.open(path)
    for i in range(len(feature)):
        x = feature[i]['properties']['SELECTIE']
        price_list.append(int(x))
    if len(price_list) == 0:
        label = 0
    else:
        label = np.mean(np.array(price_list))
    return (os.path.split(path)[1], label)


for file in os.listdir(path):
    if str(file) != '.DS_Store' and os.path.splitext(file)[-1] == '.shp':
        if len(fiona.open(os.path.join(path, file))) != 0:
            label_list.append(list(label(os.path.join(path, file))))

for item in label_list:
    if item[1] < 3000:
        item[1] = 'low'
    else:
        item[1] = 'high'

_path='/Users/guoqiushi/Documents/data/project/large_version'

for item in label_list:
    if int(os.path.splitext(item[0])[0])<1000:
        if item[1]=='high':
            shutil.copy(os.path.join(_path, 'color_large', os.path.splitext(item[0])[0] + '.jpg'),
                    os.path.join(_path, 'classification/high_color', os.path.splitext(item[0])[0] + '.jpg'))
        else:
            shutil.copy(os.path.join(_path, 'color_large', os.path.splitext(item[0])[0]+'.jpg'), os.path.join(_path, 'classification/low_color', os.path.splitext(item[0])[0]+'.jpg'))