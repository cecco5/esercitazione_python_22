"""
SHAPEFILE CREATOR - automating geographic analysis stuff

This script allows the user to do the following tasks:
    1) Shapefile re-projection to DEM srs
    2) Sample DEM to get coord_x, coord_y and height values, adding them as new fields to ESRI Shapefile

This tool accepts raster files (.tif) and ESRI Shapefile (.shp)

This script requires that `gdal` be installed within the Python
environment you are running this script in.

This file can also be imported as a module and contains the following
functions:

    * sample - the sample function + add new fields to shapefile
    * main function: apply sample to shapefiles
"""


from osgeo import gdal
from osgeo import ogr
from osgeo import osr
from math import floor
import glob
import os

os.chdir('C:/esercitazione_python_22')  # setting wd


def sample(input_raster, input_shp):
    """Set shapefile srs + Sample dem to calculate map x, map y and h + add x,y,h fields to shapefile"""

    # INPUT RASTER
    dem = gdal.Open(input_raster)                   # open raster
    dem_band = dem.GetRasterBand(1)                 # get the band of raster
    gt_forward = dem.GetGeoTransform()              # get geotransform
    gt_reverse = gdal.InvGeoTransform(gt_forward)   # get inverted geotransform
    

    # OUTPUT_SHAPEFILE (.shp)
    driver = ogr.GetDriverByName('ESRI Shapefile')          # get ESRI driver
    shape_name = input_shp.split(".")[0] + '_QUOTA_ED50rp.shp'     # new name for the output_shapefile
    data_source = driver.CreateDataSource(shape_name)       # initialization of shapefile

    # EXTRACTION OF DEM SRS
    srs = osr.SpatialReference(wkt=dem.GetProjection())    # wkt = "well-known-text" for representing geometries of vectors on a map
    # dem srs extracted
    # creation of the layer of shapefile in GIS with the srs extracted
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
    dataset = ogr.Open(input_shp)           # open shapefile
    input_layer = dataset.GetLayer()        # get access to layer

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

        height = float(dem_band.ReadAsArray(px, py, 1, 1))  # HEIGHT VALUE OF FEATURE

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

        output_feature.SetField('X_COORD', mx)     # X_COORDINATE
        output_feature.SetField('Y_COORD', my)     # Y_COORDINATE
        output_feature.SetField('HEIGHT', height)  # HEIGHT

        # FIELDS CREATED

        # DEFINITION OF SHAPEFILE GEOMETRY (so, definition of geometry of each feature)
        # wkt = "well-known-text" for representing geometries of vectors on a map
        wkt = 'POINT(%f %f)' % (output_feature.GetField('X_COORD'), output_feature.GetField('Y_COORD'))
        # print(wkt)

        point = ogr.CreateGeometryFromWkt(wkt)      # creation of geometry from the wkt string
        output_feature.SetGeometry(point)           # setting geometry to the feature

        layer.CreateFeature(output_feature)         # creation of the feature with set geometry inside the layer

        # CLOSE FEATURE
        output_feature = None

        # end of cycle

    # CLOSE DATA SOURCE
    data_source = None

    # CLOSE RASTER
    dem = None


def main():
    """
     sample: to sample the reprojected raster and to create new shapefiles with coordinates and height values
    """
    for shapefile in glob.glob('shapefile/*.shp'):
        sample("dem_lombardia_100m_ED32N.tif", shapefile)
        print(f'{shapefile} done!')
        #print("Done!")


