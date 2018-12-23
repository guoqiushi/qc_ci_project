import cv2
import os
import numpy as np

dict_map={255:[255,255,0],230:[0,0,255],205:[0,0,0],180:[0,255,255],
      165:[255,0,255],140:[0,255,0],115:[255,0,0],90:[255,255,255],
      65:[0,0,0]
      }

def grey_to_color_1(input,output):
    img = cv2.imread(input)
    height, width = img.shape[0], img.shape[1]
    img_re = np.reshape(img, (height * width, 3))

    hist = np.histogram(img.ravel(), 256, [0, 256])
    color_index = np.where(hist[0] != 0)[0]
    value_index = [hist[0][x] for x in color_index]
    print(color_index)
    print(value_index)

    color_number = dict(zip(color_index, value_index))
    print(color_number)
    value_list = [i for i in list(dict_map.keys()) if i in color_index]

    for color in value_list:
        img_re[img_re == [color, color, color]] = dict_map[color] * int((color_number[color] / 3))

    result = np.reshape(img_re, (height, width, 3))
    cv2.imwrite(output, result)



def grey_to_color(input,output):

    img=cv2.imread(input)
    height,width=img.shape[0],img.shape[1]
    img_re=np.reshape(img,(height*width,3))
    hist, bins = np.histogram(img.ravel(), 256, [0, 256])
    gray_value = np.unique(img)
    value_list = [i for i in list(dict.keys()) if i in gray_value]

    for color in value_list:
        img_re[img_re == [color, color, color]] = dict[color] * int((hist[color] / 3))

    result=np.reshape(img_re,(height,width,3))
    cv2.imwrite(output,result)

#grey_to_color('/Users/guoqiushi/Documents/data/shit/20.tiff','/Users/guoqiushi/Documents/20.jpg')


path='/Users/guoqiushi/Documents/tiff'
for file in os.listdir(path):
    if file!='.DS_Store':
        in_path=os.path.join(path,file)
        out_name=os.path.splitext(file)[0]
        out_path=os.path.join('/Users/guoqiushi/Documents/color',out_name+'.jpg')
        print('colorizing the {} image'.format(out_name))
        grey_to_color_1(in_path,out_path)