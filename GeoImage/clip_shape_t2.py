import subprocess

shape_path='//Users/guoqiushi/Documents/data/MutatiereeksBBG1996-2012.shp'
path_out='/Users/guoqiushi/Documents/data/project/tiff_large/color_shape/'

def clip_shape(shape_path,output_path,coor,EPSG):
    subprocess.call('ogr2ogr  -t_srs EPSG:' + str(EPSG) + ' -clipdst ' + coor + output_path+ ' ' + shape_path,
                    shell=True)

shape_boundary=[113077,488630,124987,483814]
ecw_boundary=[81000,500000,141000,466000]

def generate_coor(width,N_x,N_y,step,shp_boundary):
    coordinates_list=[]
    x_min,y_min=shp_boundary[0],shp_boundary[3]
    x_max=x_min+width
    y_max=y_min+width
    for i in range(N_y):
        for j in range(N_x):
            cord_xmin = x_min + step * j
            cord_ymin = y_min + step * i
            cord_xmax = x_max + step * j
            cord_ymax = y_max + step * i
            coordinates=str(cord_xmin)+' '+str(cord_ymin)+' '+str(cord_xmax)+' '+str(cord_ymax)+' '
            coordinates_list.append(coordinates)
    return coordinates_list

def generate_srcwin(width,N_x,N_y,sha_boundary,ecw_boundary,step):
    x_min=(sha_boundary[0]-ecw_boundary[0])*10
    y_min=(ecw_boundary[1]-sha_boundary[1])*10
    coor_list_str=[]
    origin=[]
    for i in range(N_y):
        for j in range(N_x):
            x_coor=x_min+j*step
            y_coor=y_min+i*step
            coordinate_str=str(x_coor)+' '+str(y_coor)+' '+str(width)+' '+str(width)+' '
            origin.append((x_coor,y_coor))
            coor_list_str.append(coordinate_str)
    return coor_list_str,origin

a,b=generate_srcwin(1000,100,40,shape_boundary,ecw_boundary,1000)
ogr_list=[]
def transform(origin,width):

    x_min=int(origin[0]/10)+81000
    y_min=500000-int(origin[1]/10)-width
    x_max=x_min+width
    y_max=y_min+width
    coordinates = str(x_min) + ' ' + str(y_min) + ' ' + str(x_max) + ' ' + str(y_max) + ' '
    return coordinates

for item in b:
    ogr_list.append(transform(item,100))


#coordinate_list_src=generate_srcwin(100,20,shape_boundary,ecw_boundary,200)
#coordinate_list_shp=generate_coor(100,40,20,shape_boundary)
#print(coordinate_list_src)
#print(coordinate_list_shp)







for i in range(len(ogr_list)):
    print('the {} clipping'.format(i))
    clip_shape(shape_path, path_out+str(i)+'.shp', ogr_list[i], 28992)
