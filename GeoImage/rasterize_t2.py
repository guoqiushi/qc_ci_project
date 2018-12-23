import gdal
import ogr
from classesmap_netherlands import classmap
import os

def rast(shape_path, tiff_path, output_path):
    print("clip shape")

    shape_crop = shape_path
    inputfile = tiff_path

    classes_file = shape_crop

    m_info = gdal.Info(inputfile).split("\n")
    for line in m_info:
        if line.startswith("Pixel Size"):
            p_size_x = float(line.split("(")[1].split(",")[0])
            p_size_y = float(line.split("(")[1].split(",")[1][0:len(line.split("(")[1].split(",")[1]) - 1])

    cropped_size = [y.strip(",") for y in
                    ([x for x in gdal.Info(inputfile).split("\n") if x.startswith("Size is")][0]).split() if
                    y.strip(",").isdigit()]
    outshape = [int(x) for x in cropped_size]

    print("rasterize")
    # assign values to classes
    file = ogr.Open(classes_file)
    layer = file.GetLayer(0)

    m_drv = ogr.GetDriverByName('Memory')
    m_ds = m_drv.CreateDataSource('wrk')
    m_ds.CopyLayer(layer, 'ColouredClasses')
    layerCopy = m_ds.GetLayer(0)

    layerCopy.CreateField(ogr.FieldDefn("FEATVAR", ogr.OFTInteger))

    colormap = {
        "Traffic area": 255,
        "Buildings": 230,
        "Semi-built terrain": 205,
        "Recreatieterrein": 180,
        "Agrarisch terrein": 155,
        "Overig agrarisch terrein": 130,
        "Binnenwater": 105,
        "Buitenwater": 80,
        "Buitenland": 55,
        'high':0,
        "low":240
    }



    for cnt in range(layerCopy.GetFeatureCount()):
        feat = layerCopy.GetFeature(cnt)
        clss = feat.GetFieldAsString('wordt2012')

        feat.SetField("FEATVAR", colormap[classmap[clss]])
        layerCopy.SetFeature(feat)

    layerCopy.ResetReading()

    # Rasterize with GDAL
    # Define pixel_size and NoData value of new raster
    pixel_size_x = p_size_x
    pixel_size_y = p_size_y
    NoData_value = -9999

    # Filename of input OGR file
    vector_fn = classes_file

    # Filename of the raster Tiff that will be created
    raster_fn = output_path

    # Open the data source and read in the extent
    source_ds = ogr.Open(vector_fn)
    source_layer = layerCopy
    x_min, x_max, y_min, y_max = source_layer.GetExtent()

    # Create the destination data source
    x_res = outshape[0]
    y_res = outshape[1]

    target_ds = gdal.GetDriverByName('GTiff').Create(raster_fn, x_res, y_res, 1, gdal.GDT_Byte)
    target_ds.SetGeoTransform((x_min, pixel_size_x, 0, y_max, 0, pixel_size_y))
    target_ds.SetProjection(layer.GetSpatialRef().ExportToWkt())
    band = target_ds.GetRasterBand(1)
    band.SetNoDataValue(NoData_value)

    # Rasterize
    print("Rasterize")
    gdal.RasterizeLayer(target_ds, [1], source_layer, burn_values=[255], options=["ATTRIBUTE=FEATVAR"])

    del file
    del source_ds


#rast('/Users/guoqiushi/Documents/data/test_shape/7_.shp','/Users/guoqiushi/Downloads/output/r_25gz2.tif/arial_image_27.tiff','/Users/guoqiushi/Documents/data/7.tif')
tiff_path='/Users/guoqiushi/Documents/tiff'
sha_path='/Users/guoqiushi/Documents/shapefile'

def show_file_abspath(path,type):
    list=[]
    g = os.walk(path)
    for path, dir_list, file_list in g:
        for file_name in file_list:
            if os.path.splitext(file_name)[-1] == type:
                list.append(os.path.join(path, file_name))
    return list




arial_image_list=show_file_abspath(tiff_path,'.tif')
sha_list=show_file_abspath(sha_path,'.shp')
print(len(sha_list))
print(len(arial_image_list))


for i in range(100):
    rast('/Users/guoqiushi/Documents/mul_shape/{}.shp'.format(i),'/Users/guoqiushi/Documents/tiff_1000/{}.tif'.format(i),'/Users/guoqiushi/Documents/rast/{}.tif'.format(i))
