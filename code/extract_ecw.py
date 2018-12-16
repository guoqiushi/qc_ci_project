import subprocess



input_path='/ds/images/remote_sensing/data/NetherlandsGeo/ECW/2016_Perceel3_Blok03.ecw'
output_path='/b_test/guo/Task_2/tiff/'
Boundary=[116000,478078,129960,492400]

def crop_ecw(path_in,path_out,coordinates):
    subprocess.call('gdal_translate -of GTIFF -srcwin '+coordinates+path_in+' '+path_out)

def generate_srcwin(step,boundary,width,N):
    x_min=boundary[0]
    y_min=boundary[1]
    coordinates_list_srcwin=[]
    for i in range(N):
        for j in range(N):
            cord_xmin=x_min+step*j
            cord_ymin=y_min+step*i
            coordinate=str(cord_xmin)+' '+str(cord_ymin)+' '+str(width)+' '+str(width)+' '
            coordinates_list_srcwin.append((coordinate,str(i)+'_'+str(j)))
    return coordinates_list_srcwin

coordinates_list=generate_srcwin(100,[116000,478078,129960,492400],100,50)
#crop_ecw(input_path,output_path+coordinates_list[1][-1]+'.tif',coordinates_list[1][0])

#print('.......croping from ecw.........')
print('gdal_translate -of GTIFF -srcwin '+coordinates_list[1][0]+input_path+' '+output_path+coordinates_list[1][-1]+'.tif')

#for i in range(len(coordinates_list)):
#   crop_ecw(input_path,output_path+coordinates_list[i][-1]+'.tif',coordinates_list[i][0])

