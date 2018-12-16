import os

import shutil
import subprocess
import gdal

shp_path='/ds/images/remote_sensing/data/NetherlandsGeo/land/MutatiereeksBBG1996-2012.shp'
input_path='/ds/images/remote_sensing/data/NetherlandsGeo/output'
output_path='/b_test/guo/Task_1/'

coor_list=[]

def show_file_abspath(path,type):
    list = []
    g = os.walk(path)
    for path, dir_list, file_list in g:
        for file_name in file_list:
            if os.path.splitext(file_name)[-1] == type:
                list.append(os.path.join(path, file_name))
    return list


def copy_arial_image(input,output,type):
    for file in os.listdir(input):
        if os.path.splitext(file)[-1] == type:
            shutil.copy(os.path.join(input_path, file), os.path.join(output_path, file))


def get_the_coordinate(file_path):
    src = gdal.Open(file_path)

    ulx, xres, xskew, uly, yskew, yres = src.GetGeoTransform()
    lrx = ulx + (src.RasterXSize * xres)
    lry = uly + (src.RasterYSize * yres)
    x_min=min(ulx,lrx)
    x_max=max(ulx,lrx)
    y_min=min(uly,lry)
    y_max=max(uly,lry)
    coordinate = str(x_min)+' '+str(y_min)+' '+str(x_max)+' '+str(y_max)+' '

    return coordinate

def show_file_abspath(path,type):
    list=[]
    g = os.walk(path)
    for path, dir_list, file_list in g:
        for file_name in file_list:
            if os.path.splitext(file_name)[-1] == type:
                list.append(os.path.join(path, file_name))
    return list

def clip_shape(input_path,output_path,coor,EPSG):
    subprocess.call('ogr2ogr  -t_srs EPSG:'+str(EPSG)+' -clipdst '+coor+output_path+' '+input_path+' '+'-skipfailures' ,shell=True)

file_list=show_file_abspath(input_path,'.tiff')
number_image=10

for i in range(number_image):
    coor_list.append(get_the_coordinate((file_list[i])))


for i in range(1,number_image):
    clip_shape(shp_path,output_path+'{}_.shp'.format(i),coor_list[i],28992)
