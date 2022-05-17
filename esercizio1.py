"""
SHAPEFILE CREATOR - automating geographic analysis stuff

This script allows the user to create ESRI Shapefiles (point vector) from DEM raster and csv files:
    1) DEM raster re-projection (from Geographic rs to Projected rs)
    2) Sample DEM to get height information pixel-by-pixel, adding it to csv files as a field
    3) Create ESRI shapefiles from csv files

This tool accepts comma separated value files (.csv) and raster files (.tif)

This script requires that `gdal` be installed within the Python
environment you are running this script in.

This file can also be imported as a module and contains the following
functions:

    * sample - the sample function
    * main -> re-projection of dem + sample to all csv files in the wd
"""

import os
import glob
import csv
from osgeo import gdal
from osgeo import ogr   # for vector manipulation
from osgeo import osr   # for SR manipulation

# setting working directory
os.chdir('C:/esercitazione_python_22')


def sample(input_csv, input_raster):
    """ Function to sample the raster and create ESRI shapefile"""

    # RASTER: cycle on it to get the values
    dem = gdal.Open(input_raster)    # open raster
    band = dem.GetRasterBand(1)      # get band 1 of dem to represent it as a matrix of values (peak heights)
    gt = dem.GetGeoTransform()       # get geotransform to read each value

    # CSV:
    my_csv = open(input_csv, 'r')                   # open csv
    reader = csv.DictReader(my_csv, delimiter=',')  # each row of csv is considered as a dictionary {'key','value}

    # ESRI SHAPEFILE (.shp)
    driver = ogr.GetDriverByName('ESRI Shapefile')        # get ESRI driver
    shape_name = input_csv.split(".")[0]+'.shp'           # initialization of shapefile
    data_source = driver.CreateDataSource(shape_name)

    # import reference system:
    srs = osr.SpatialReference()    # import SR from EPSG
    srs.ImportFromEPSG(32632)

    # creation of the layer of shapefile in GIS
    layer = data_source.CreateLayer(shape_name, srs, ogr.wkbPoint)      # point shapefile in this case

    # definition of shapefile fields
    field_name = ogr.FieldDefn('name', ogr.OFTString)   # OFTString is the field format -> string
    field_name.SetWidth(100)                            # length of the field
    layer.CreateField(field_name)

    layer.CreateField(ogr.FieldDefn('xcoord', ogr.OFTReal))     # -> number fields don't need width specification
    layer.CreateField(ogr.FieldDefn('ycoord', ogr.OFTReal))
    layer.CreateField(ogr.FieldDefn('height', ogr.OFTReal))

    # APPENDING ALL THE ROWS INSIDE A LIST L FOR THE CREATION OF NEW CSV FILE WITH HEIGHT FIELD
    L = []

    # header of new csv with added height field
    header = ['COD_REG', 'COD_CM', 'COD_PRO', 'PRO_COM', 'COMUNE', 'NOME_TED', 'FLAG_CM', 'SHAPE_Leng', 'SHAPE_Area', 'xcoord', 'ycoord', 'height']

    # CYCLE THROUGH INPUT CSV ROWS IN ORDER TO ASSIGN VALUES TO SHAPEFILE FIELDS
    for row in reader:
        list_row = []                               # New list to contain the row fields
        utm_x = float(row['xcoord'])                # get values of utm coordinates
        utm_y = float(row['ycoord'])
        px = int((utm_x - gt[0]) / gt[1])           # from raster coordinates to pixel coordinates
        py = int((utm_y - gt[3]) / gt[5])
        height = band.ReadAsArray(px, py, 1, 1)     # get height from pixel coordinates on the raster values matrix
        h = float(height)

        # adding the values of the corresponding fields (as keys in dictionary) of csv in the list
        list_row.append(row['COD_REG'])
        list_row.append(row['COD_CM'])
        list_row.append(row['COD_PRO'])
        list_row.append(row['PRO_COM'])
        list_row.append(row['COMUNE'])
        list_row.append(row['NOME_TED'])
        list_row.append(row['FLAG_CM'])
        list_row.append(row['SHAPE_Leng'])
        list_row.append(row['SHAPE_Area'])
        list_row.append(row['xcoord'])
        list_row.append(row['ycoord'])
        list_row.append(h)              # added height value

        L.append(list_row)              # added the entire row to the L list

        # definition of layer attribute (element of attribute table in Qgis)
        feature = ogr.Feature(layer.GetLayerDefn())
        # setting feature fields from csv values, reading them from keys
        feature.SetField('name', row['COMUNE'])
        feature.SetField('xcoord', row['xcoord'])
        feature.SetField('ycoord', row['ycoord'])
        feature.SetField('height', h)                   # height field <- height read from raster sampling

        # fields created

        # DEFINITION OF SHAPEFILE GEOMETRY (so, definition of geometry of each feature)
        # wkt = "well-known-text" for representing geometries of vectors on a map
        wkt = 'POINT(%f %f)' % (float(row['xcoord']), float(row['ycoord']))

        point = ogr.CreateGeometryFromWkt(wkt)         # creation of geometry from the wkt string
        feature.SetGeometry(point)                     # setting geometry to the feature

        layer.CreateFeature(feature)                   # creation of the feature with set geometry inside the layer

        # CLOSE FEATURE
        feature = None

        # end of cycle

    output_csv_name = input_csv.split('.')[0]+'_QUOTA.csv'      # set new name for output_csv with height values
    csv_output = open(output_csv_name, 'w')                     # new output csv file

    # ADD HEADER AND ALL THE VALUES TO OUTPUT CSV
    writer = csv.writer(csv_output, delimiter=',')
    writer.writerow(header)
    writer.writerows(L)

    # CLOSE FILES
    my_csv.close()
    csv_output.close()

    # CLOSE RASTER
    dem = None

    # CLOSE DATA SOURCE
    data_source = None


def main():
    """ Two functions:
    1) Warp: reprojection of raster
    2) sample: to sample the reprojected raster
    """
    #   gdal.Warp("dem_lombardia_100m_WGS32N.tif", "dem_lombardia_100m_ED32N.tif", dstSRS='EPSG:32632')
    for csv_file in glob.glob('csv/*.csv'):
        #sample(csv_file, 'dem_lombardia_100m_WGS32N.tif')
        print("Done!")





