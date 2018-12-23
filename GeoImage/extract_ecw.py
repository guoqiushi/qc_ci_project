import subprocess

ecw_path='/ds/images/remote_sensing/data/NetherlandsGeo/ECW/2016_Perceel3_Blok00.ecw'
output_path='/b_test/guo/Task_2/tiff/'

ecw_boundary=[81000,500000,141000,466000]
shape_boundary=[117787,488285,121214,484267]
def crop_ecw(in_path,out_path,coordinates):
    subprocess.call('gdal_translate -of GTIFF -srcwin '+coordinates+in_path+' '+out_path)

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


coordinate_list=generate_srcwin(1000,20,shape_boundary,ecw_boundary,200)

for i in range(len(coordinate_list)):
    print('croping the {} image'.format(i))
    crop_ecw(ecw_path,output_path+str(i)+'.tif',coordinate_list[i])

