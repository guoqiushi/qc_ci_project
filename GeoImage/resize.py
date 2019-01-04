import os
import cv2

path='/Users/guoqiushi/Documents/data/project/large_version/tiff_large'
jpg_path='/Users/guoqiushi/Documents/data/project/large_version/jpg_large'
for file in os.listdir(path):
   # print(file)
    index=os.path.splitext(file)[0]

    new_name=str(index)+'.jpg'
    os.rename(path+'/'+file,path+'/'+new_name)

for file in os.listdir(path):

    print(file)
    img=cv2.imread(os.path.join(path,file))

    img=cv2.resize(img,(256,256),interpolation=cv2.INTER_CUBIC)
    cv2.imwrite(os.path.join(jpg_path,file),img)
