import subprocess

shape_path='/Users/guoqiushi/Documents/DFKI_Project/land/MutatiereeksBBG1996-2012.shp'
path_out='/Users/guoqiushi/Documents/mul_shape/'

def clip_shape(shape_path,output_path,coor,EPSG):
    subprocess.call('ogr2ogr  -t_srs EPSG:' + str(EPSG) + ' -clipdst ' + coor + output_path+ ' ' + shape_path,
                    shell=True)

shape_boundary=[117787,488285,121214,484267]
ecw_boundary=[81000,500000,141000,466000]

def generate_coor(width,N,step,shp_boundary):
    coordinates_list=[]
    x_min,y_min=shp_boundary[0],shp_boundary[1]
    x_max=x_min+width
    y_max=y_min+width
    for i in range(N):
        for j in range(N):
            cord_xmin = x_min + step * j
            cord_ymin = y_min + step * i
            cord_xmax = x_max + step * j
            cord_ymax = y_max + step * i
            coordinates=str(cord_xmin)+' '+str(cord_ymin)+' '+str(cord_xmax)+' '+str(cord_ymax)+' '
            coordinates_list.append(coordinates)
    return coordinates_list

def generate_srcwin(width,N,sha_boundary,ecw_boundary,step):
    x_min=(sha_boundary[0]-ecw_boundary[0])*10
    y_min=(ecw_boundary[1]-sha_boundary[1])*10
    coor_list=[]
    for i in range(N):
        for j in range(N):
            x_coor=x_min+j*step
            y_coor=y_min+i*step
            coordinate=str(x_coor)+' '+str(y_coor)+' '+str(width)+' '+str(width)+' '
            coor_list.append(coordinate)
    return coor_list


#coordinate_list_src=generate_srcwin(100,20,shape_boundary,ecw_boundary,200)
coordinate_list_shp=generate_coor(1000,20,200,shape_boundary)
#print(coordinate_list_src)
#print(coordinate_list_shp)







for i in range(len(coordinate_list_shp)):
    print('the {} clipping'.format(i))
    clip_shape(shape_path, path_out+str(i)+'.shp', coordinate_list_shp[i], 28992)
