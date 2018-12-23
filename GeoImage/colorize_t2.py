import numpy as np
import cv2
import os

dict_map={255:[255,255,0],230:[0,0,255],205:[0,0,0],180:[0,255,255],
      165:[255,0,255],140:[0,255,0],115:[255,0,0],90:[255,255,255],
      65:[0,0,0]
      }
'''
img=cv2.imread('/Users/guoqiushi/Documents/rast/0.tif')
height,width=img.shape[0],img.shape[1]
img_re=np.reshape(img,(height*width,3))

hist=np.histogram(img.ravel(), 256, [0, 256])
color_index=np.where(hist[0]!=0)[0]
value_index=[hist[0][x] for x in color_index]
print(color_index)
print(value_index)

color_number=dict(zip(color_index,value_index))
print(color_number)
value_list = [i for i in list(dict_map.keys()) if i in color_index]

for color in value_list:
    img_re[img_re == [color, color, color]] = dict_map[color]*int((color_number[color]/3))

result=np.reshape(img_re,(height,width,3))
cv2.imwrite('/Users/guoqiushi/Documents/0.jpg',result)
'''
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

path='/Users/guoqiushi/Documents/rast'


for file in os.listdir(path):
    if file!='.DS_Store':
        file_path=os.path.join(path,file)
        jpg_path=os.path.join('/Users/guoqiushi/Documents/color_2',os.path.splitext(file)[0]+'.jpg')
        print(file_path)
        print(jpg_path)
        grey_to_color_1(file_path, jpg_path)


    #jpg_path=os.path.join('/Users/guoqiushi/Documents/color_2',os.path.splitext(fil))
    #print(file_path)
#grey_to_color_1('/Users/guoqiushi/Documents/rast/3.tif','/Users/guoqiushi/Documents/3.jpg')