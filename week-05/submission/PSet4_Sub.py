"""
Write a Python Script Using Functions to Process the Data

In class, we wrote one function to calculate the Normalized Difference Vegetation Index and one function to estimate surface emissivity.

Build on these functions, writing six other functions, using the code we used in the workshop. Note that when you're working with the downloaded Landsat data, you'll need to either...

1. Use the much longer Landsat-provided file names. I recommend doing this, as it will allow you to much more easily use these scripts across multiple Landsat scenes.
2. Rename your files, making them shorter and more... well, appealing I guess.
"""
## Code from Class

import sys
sys.path.insert(0,'/Library/Frameworks/GDAL.framework/Versions/2.2/Python/3.6/site-packages')


from osgeo import gdal
import matplotlib.pyplot as plt
import numpy as np
import os
%matplotlib inline

# Mac Users: If you're having issues importing GDAL,
# you may have to add GDAL to your Python path again
# sys.path.insert(0,'/Library/Frameworks/GDAL.framework/Versions/2.2/Python/3.6/site-packages')

def process_string (st):
    """
    Parses Landsat metadata
    """
    return float(st.split(' = ')[1].strip('\n'))

def ndvi_calc(red, nir):
    """
    Calculate NDVI
    """
    return (nir - red) / (nir + red)

def emissivity_calc (pv, ndvi):
    """
    Calculates an estimate of emissivity
    """
    ndvi_dest = ndvi.copy()
    ndvi_dest[np.where(ndvi < 0)] = 0.991
    ndvi_dest[np.where((0 <= ndvi) & (ndvi < 0.2)) ] = 0.966
    ndvi_dest[np.where((0.2 <= ndvi) & (ndvi < 0.5)) ] = (0.973 * pv[np.where((0.2 <= ndvi) & (ndvi < 0.5)) ]) + (0.966 * (1 - pv[np.where((0.2 <= ndvi) & (ndvi < 0.5)) ]) + 0.005)
    ndvi_dest[np.where(ndvi >= 0.5)] = 0.973
    return ndvi_dest

def array2tif(raster_file, new_raster_file, array):
    """
    Writes 'array' to a new tif, 'new_raster_file',
    whose properties are given by a reference tif,
    here called 'raster_file.'
    """
    # Invoke the GDAL Geotiff driver
    raster = gdal.Open(raster_file)

    driver = gdal.GetDriverByName('GTiff')
    out_raster = driver.Create(new_raster_file,
                        raster.RasterXSize,
                        raster.RasterYSize,
                        1,
                        gdal.GDT_Float32)
    out_raster.SetProjection(raster.GetProjection())
    # Set transformation - same logic as above.
    out_raster.SetGeoTransform(raster.GetGeoTransform())
    # Set up a new band.
    out_band = out_raster.GetRasterBand(1)
    # Set NoData Value
    out_band.SetNoDataValue(-1)
    # Write our Numpy array to the new band!
    out_band.WriteArray(array)

DATA = "/Users/charlotteong/Dropbox (MIT)/Spring 2018/Big Data/Week5-landsat"

# Your Functions!
# We recommend reading carefully through the goals for all functions before starting the first function.


def tif2array(location):
    """
    Should:
    1. Use gdal.open to open a connection to a file.
    2. Get band 1 of the raster
    3. Read the band as a numpy array
    4. Convert the numpy array to type 'float32'
    5. Return the numpy array.
    """

    # Load in TIRS Band
    tirs_data = gdal.Open(location)
    tirs_band = tirs_data.GetRasterBand(1)
    tirs = tirs_band.ReadAsArray()
    tirs_float = tirs.astype(np.float32)
    return tirs_float

meta_text = "/Users/charlotteong/Dropbox (MIT)/Spring 2018/Big Data/Week5-landsat/MTL.txt"

def retrieve_meta(meta_text):
    """
    Retrieve variables from the Landsat metadata *_MTL.txt file
    Should return a list of length 4.
    'meta_text' should be the location of your metadata file
    Use the process_string function we created in the workshop.
    """
    with open(meta_text) as f:
        meta = f.readlines()
    # Define terms to match
    matches = ['RADIANCE_MULT_BAND_10', 'RADIANCE_ADD_BAND_10', 'K1_CONSTANT_BAND_10', 'K2_CONSTANT_BAND_10']
    [s for s in meta if any(xs in s for xs in matches)]
    matching = [process_string(s) for s in meta if any(xs in s for xs in matches)]
    rad_mult_b10, rad_add_b10, k1_b10, k2_b10 = matching
    return matching


def rad_calc(tirs_float, var_list):
    """
    Calculate Top of Atmosphere Spectral Radiance
    Note that you'll have to access the metadata variables by
    their index number in the list, instead of naming them like we did in class.
    """
    rad = var_list[0] * tirs_float + var_list[1]
    return rad

def bt_calc(rad, var_list):
    """
    Calculate Brightness Temperature
    Again, you'll have to access appropriate metadata variables
    by their index number.
    """
    ## rad from rad_calc; var_list from retrieve_meta
    bt = var_list[3] / np.log((var_list[2]/rad) + 1) - 273.15
    return bt

def pv_calc(ndvi, ndvi_s, ndvi_v):
    """
    Calculate Proportional Vegetation
    """
    pv = (ndvi - ndvi_s) / (ndvi_v - ndvi_s) ** 2
    """
    for future use:
    assume ndvi_s = 0.2
    assume ndvi_v = 0.5
    """
    return pv

def lst_calc(location):
    """
    Calculate Estimate of Land Surface Temperature.
    Your output should
    ---
    Note that this should take as its input ONLY the location
    of a directory in your file system. That means it will have
    to call your other functions. It should:
    1. Define necessary constants
    2. Read in appropriate tifs (using tif2array)
    3. Retrieve needed variables from metadata (retrieve_meta)
    4. Calculate ndvi, rad, bt, pv, emis using appropriate functions
    5. Calculate land surface temperature and return it.
    Your LST function may return strips of low-values around the raster...
    This is a processing artifact that you're not expected to account for.
    Nothing to worry about!
    """
    ## DEFINE CONSTANTS
    wave = 10.8E-06
    # PLANCK'S CONSTANT
    h = 6.626e-34
    # SPEED OF LIGHT
    c = 2.998e8
    # BOLTZMANN's CONSTANT
    s = 1.38e-23
    p = h * c / s

    #READ TIFS
    red_path = tif2array(os.path.join(DATA, 'B4.TIF'))
    nir_path = tif2array(os.path.join(DATA, 'B5.TIF'))
    tirs_path = tif2array(os.path.join(DATA, 'B10.TIF'))
    var_list = retrieve_meta(os.path.join(DATA, 'MTL.txt'))

    ## calculate rad, bt, ndvi, pv, emis
    rad_ans = rad_calc(tirs_path, var_list)
    bt_ans = bt_calc(rad_ans, var_list)
    ndvi_ans = ndvi_calc(red_path, nir_path)
    ndvi_s = 0.2
    ndvi_v = 0.5
    pv_ans = pv_calc(ndvi_ans, ndvi_s, ndvi_v)
    emis = emissivity_calc(pv_ans, ndvi_ans)

    lst = bt_ans / (1 + (wave * bt_ans / p) * np.log(emis))

    plt.imshow(lst, cmap='RdYlGn')
    plt.colorbar()

    return lst

lst_filter = lst_calc(DATA)


##Use these functions to generate an Normalized Difference Vegetation Index and a Land Surface Temperature Estimate for your downloaded Landsat data.

## Remove Clouds

Your Landsat data contains another band, whose filename ends with `_BQA.tif`. this is the so-called 'quality assessment band', which contains estimates of where there are clouds in our image. You'll need to read this `tif` in: try using your new `tif2array` function!

According to the [USGS Landsat documentation](https://landsat.usgs.gov/collectionqualityband), these values are where we can be highly confident that the image is clear and, additionally, where there are clouds and cloud shadows:

| Attribute               | Pixel Value                                                                                    |
|-------------------------|------------------------------------------------------------------------------------------------|
| Clear                   | 2720, 2724, 2728, 2732                                                                         |
| Cloud Confidence - High | 2800, 2804, 2808, 2812, 6896, 6900, 6904, 6908                                                 |
| Cloud Shadow - High     | 2976, 2980, 2984, 2988, 3008, 3012, 3016, 3020, 7072, 7076, 7080, 7084, 7104, 7108, 7112, 7116 |

Write a function that reclassifies an input Numpy array based on values stored in the BQA. The function should reclassify input data in such a way that pixels, *except for those that are clear* (for example, 2720), are assigned a value of `nan`. Use the `emissivity_calc` function as a model! We're doing something similar here! Your code will look like this:
"""
def cloud_filter(array, bqa):
    array_dest = array.copy()
    array_dest[np.where((bqa != <a certain value>) & (bqa != <another certain value>)) ] = 'nan'
    return array_dest
"""

You should simply be able to revise the above function, making your criteria test for `bqa` values not equal to 2720, 2724, 2728, 2732.

```python
def cloud_filter(array, bqa):
    """
    Filters out clouds and cloud shadows using values of BQA.
    """
    array_dest = array.copy()
    array_dest[np.where((bqa != 2720) & (bqa != 2724) & (bqa != 2728) & (bqa != 2732)) ] = 'nan'
    return array_dest

bqa_path = tif2array(os.path.join(DATA, 'BQA.TIF'))

red_path2 = tif2array(os.path.join(DATA, "B4.TIF"))
nir_path2 = tif2array(os.path.join(DATA, "B5.TIF"))
tirs_path2 = tif2array(os.path.join(DATA, "B10.TIF"))

new_ndvi = ndvi_calc(red, nir)
plt.imshow(new_ndvi, cmap = 'RdYlGn')
plt.colorbar()

cloudless = cloud_filter(new_ndvi, bqa_path)
plt.imshow(cloudless, cmap = 'RdYlGn')
plt.colorbar()

```

## Write Your Filtered Arrays as `.tifs`

You should now be able to write your NDVI and LST arrays as GeoTIFFs. For example, to write your filtered LST to a `tif` consistent with the naming convention we've requested, you would write this code (assuming you're storing your LST in a variable called `lst_filter`).

```python

tirs_path = os.path.join(DATA, 'B10.TIF')
out_path = os.path.join(DATA, 'ong_lst_20130619.tif')
array2tif(tirs_path, out_path, lst_filter)

red_path = os.path.join(DATA, 'B4.TIF')
out_path = os.path.join(DATA, 'ong_ndvi_20130619.tif')
array2tif(tirs_path, out_path, new_ndvi)

```

The reason you have to specify the `tirs_path` is that GDAL looks to another raster file to obtain dimensions, etc. We could use any of our input rasters - the TIRS band was chosen somewhat arbitrarily.

Once you've written these, you should compress each of them into a zip file - two separate ZIP files! This is to ensure that the files come in under Stellar's file submission size limit. Name sure they are named correctly e.g., `yourlastname_ndvi_imagerydate.tif`, where `yourlastname` is your last name and `imagerydate` is the date the imagery was captured reported in the format `YYYYMMDD`.
