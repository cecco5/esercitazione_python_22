"""
SHAPEFILE CREATOR - automating geographic analysis stuff

This script allows the user to add COORDDX, COORDY and HEIGHT values (got from DEM values) to a list of shapefiles
    1) DEM raster re-projection (from Geographic rs to Projected rs)
    2) Sample DEM to get coord_x, coord_y and height values, adding them as new fields to ESRI Shapefile

This tool accepts raster files (.tif) and ESRI Shapefiles (.shp)

This script requires that `gdal` be installed within the Python
environment you are running this script in.

This file can also be imported as a module and contains the following
functions:

    * sample - the sample function + add new fields to shapefile
    * main function: reprojection + apply sample to shapefiles

"""
from osgeo import gdal
from osgeo import osr
from osgeo import ogr
from math import floor
import glob
import os

# setting working directory
os.chdir('C:/esercitazione_python_22')


def sample(input_shp, input_raster):
    """ Function to sample the raster and add height values to ESRI shapefile"""

    #  INPUT RASTER:
    dem = gdal.Open(input_raster)  # open raster
    raster_band = dem.GetRasterBand(1)
    gt_forward = dem.GetGeoTransform()                     # get geotransform
    gt_reverse = gdal.InvGeoTransform(gt_forward)          # get inverted geotransform

    # OUTPUT_SHAPEFILE (.shp)
    driver = ogr.GetDriverByName('ESRI Shapefile')        # get ESRI driver
    shape_name = input_shp.split(".")[0] + '_QUOTA.shp'   # new name for the output_shapefile
    data_source = driver.CreateDataSource(shape_name)     # initialization of shapefile

    # import reference system:
    srs = osr.SpatialReference()  # import SR from EPSG
    srs.ImportFromEPSG(32632)

    # creation of the layer of shapefile in GIS
    layer = data_source.CreateLayer(shape_name, srs, ogr.wkbPoint)  # point shapefile in this case

    # DEFINITION OF OUTPUT SHAPEFILE FIELDS
    # fields = [COD_REG,COD_CM,COD_PRO,PRO_COM,COMUNE,NOME_TED,FLAG_CM,SHAPE_Leng,SHAPE_Area,xcoord,ycoord,height]
    layer.CreateField(ogr.FieldDefn('COD_REG', ogr.OFTInteger64))
    layer.CreateField(ogr.FieldDefn('COD_CM', ogr.OFTInteger64))
    layer.CreateField(ogr.FieldDefn('COD_PRO', ogr.OFTInteger64))
    layer.CreateField(ogr.FieldDefn('PRO_COM', ogr.OFTInteger64))

    comune_field_name = ogr.FieldDefn('COMUNE', ogr.OFTString)  # OFTString is the field format -> string
    comune_field_name.SetWidth(100)  # length of the field
    layer.CreateField(comune_field_name)

    nome_ted_field_name = ogr.FieldDefn('NOME_TED', ogr.OFTString)  # OFTString is the field format -> string
    nome_ted_field_name.SetWidth(100)  # length of the field
    layer.CreateField(nome_ted_field_name)

    layer.CreateField(ogr.FieldDefn('FLAG_CM', ogr.OFTInteger))
    layer.CreateField(ogr.FieldDefn('SHAPE_Leng', ogr.OFTReal))
    layer.CreateField(ogr.FieldDefn('SHAPE_Area', ogr.OFTReal))
    layer.CreateField(ogr.FieldDefn('X_COORD', ogr.OFTReal))
    layer.CreateField(ogr.FieldDefn('Y_COORD', ogr.OFTReal))
    layer.CreateField(ogr.FieldDefn('HEIGHT', ogr.OFTReal))

    # INPUT SHAPEFILE:
    dataset = ogr.Open(input_shp)
    input_layer = dataset.GetLayer()

    # Iterating in the input_shapefile features in order to:
    # 1) extract map coord_x, coord_y and calculate height (from pixel coords). Then add them to relative output_shapefile fields
    # 2) extract input_shapefile fields values and add them to relative output_shapefile fields
    for input_feature in input_layer:
        geom = input_feature.GetGeometryRef()
        mx, my = geom.GetX(), geom.GetY()  # COORDINATES IN MAP UNITS TO ADD TO OUTPUT_SHAPEFILE

        # Convert from map to pixel coordinates.
        px, py = gdal.ApplyGeoTransform(gt_reverse, mx, my)
        px = floor(px)  # x pixel
        py = floor(py)  # y pixel

        height = float(raster_band.ReadAsArray(px, py, 1, 1))   # HEIGHT VALUE OF FEATURE

        # definition of layer attribute of output_shapefile (element of attribute table in Qgis)
        output_feature = ogr.Feature(layer.GetLayerDefn())

        # setting feature fields from input_shapefile fields
        output_feature.SetField('COD_REG', input_feature.GetField('COD_REG'))
        output_feature.SetField('COD_CM', input_feature.GetField('COD_CM'))
        output_feature.SetField('COD_PRO', input_feature.GetField('COD_PRO'))
        output_feature.SetField('PRO_COM', input_feature.GetField('PRO_COM'))
        output_feature.SetField('COMUNE', input_feature.GetField('COMUNE'))
        output_feature.SetField('NOME_TED', input_feature.GetField('NOME_TED'))
        output_feature.SetField('FLAG_CM', input_feature.GetField('FLAG_CM'))
        output_feature.SetField('SHAPE_Leng', input_feature.GetField('SHAPE_Leng'))
        output_feature.SetField('SHAPE_Area', input_feature.GetField('SHAPE_Area'))

        output_feature.SetField('X_COORD', mx)          # X_COORDINATE
        output_feature.SetField('Y_COORD', my)          # Y_COORDINATE
        output_feature.SetField('HEIGHT', height)       # HEIGHT

        #print(type(output_feature.GetField('X_COORD')), type(output_feature.GetField('Y_COORD')), type(output_feature.GetField('HEIGHT')))
        #print(output_feature.GetField('X_COORD'), output_feature.GetField('Y_COORD'), output_feature.GetField('HEIGHT'))
        #break

        # FIELDS CREATED

        # DEFINITION OF SHAPEFILE GEOMETRY (so, definition of geometry of each feature)
        # wkt = "well-known-text" for representing geometries of vectors on a map
        wkt = 'POINT(%f %f)' % (output_feature.GetField('X_COORD'), output_feature.GetField('Y_COORD'))
        # print(wkt)

        point = ogr.CreateGeometryFromWkt(wkt)  # creation of geometry from the wkt string
        output_feature.SetGeometry(point)       # setting geometry to the feature

        layer.CreateFeature(output_feature)  # creation of the feature with set geometry inside the layer

        # CLOSE FEATURE
        output_feature = None

        # end of cycle

    # CLOSE DATA SOURCE
    data_source = None

    # CLOSE RASTER
    dem = None


def main():
    """ Two functions:
       1) Warp: reprojection of raster
       2) sample: to sample the reprojected raster and to create new shapefiles with coordinates and height values
    """
    #   gdal.Warp("dem_lombardia_100m_WGS32N.tif", "dem_lombardia_100m_ED32N.tif", dstSRS='EPSG:32632')
    for shapefile in glob.glob('shapefile/*.shp'):
        sample(shapefile, "dem_lombardia_100m_WGS32N.tif")
        print(f'{shapefile} done!')

