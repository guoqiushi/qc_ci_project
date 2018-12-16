import subprocess

path='/Users/guoqiushi/Documents/data/shape'
path_in= '/home/guo/code/shapefile/WONINGWAARDE_2002_region.shp'
path_out='/b_test/guo/Task_2/shape/'
coordinates=str(126529)+' '+str(478375)+' '+str(128084)+' '+str(479062)+' '


def clip_shape(input_path,output_path,coor,EPSG):
    subprocess.call('ogr2ogr  -t_srs EPSG:'+str(EPSG)+' -clipdst '+coor+output_path+' '+input_path ,shell=True)

Boundary=[116000,478078,129960,492400]
x_min,y_min,x_max,y_max=116001,478079,117001,479079
step=100
coordinates_list=[]

for i in range(50):
    for j in range(50):
        cord_xmin=x_min+step*j
        cord_ymin=y_min+step*i
        cord_xmax=x_max+step*j
        cord_ymax=y_max+step*i
        cordinate=str(cord_xmin)+' '+str(cord_ymin)+' '+str(cord_xmax)+' '+str(cord_ymax)+' '
        coordinates_list.append((cordinate,str(i)+'_'+str(j)))

print('.......croping shapefile.........')


for i in range(len(coordinates_list)):
    clip_shape(path_in,path_out+coordinates_list[i][-1]+'.shp',coordinates_list[i][0],28992)
