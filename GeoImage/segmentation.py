import os
import cv2
import numpy as np









def convert(img_path,output):
    img=cv2.imread(img_path)
    img=cv2.resize(img,(256,256),interpolation=cv2.INTER_CUBIC)
    for i in range(256):
        for j in range(256):
            if (img[i][j]==(0,0,254)).all():
                img[i][j] = (0, 255, 0)
            else:
                img[i][j] = (0, 0, 0)
    cv2.imwrite(output,img)

for image in os.listdir('/Users/guoqiushi/Documents/data/project/large_version/classification/high_color'):
    if image!='.DS_Store':
        print('convert the {} image'.format(str(image)))
        image_path=os.path.join('/Users/guoqiushi/Documents/data/project/large_version/classification/high_color',image)
        output_path=os.path.join('/Users/guoqiushi/Documents/data/project/large_version/classification/high_label',image)
        convert(image_path,output_path)

#convert('/Users/guoqiushi/Documents/data/project/low/333.jpg','/Users/guoqiushi/Documents/data/project/segmentation/low/333.jpg')
