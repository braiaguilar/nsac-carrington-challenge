# imports
from spacepy import pycdf
from dtw import *
import requests
import os
# you must download and install CDF Software Distribution. You can get it from:
# https://cdf.gsfc.nasa.gov/html/sw_and_docs.html
# after installing the software, you must replace the next line with the path to the cdf library
# format example for Windows: C:/Program Files/CDF_Distribution/cdf38_1-dist/lib
# (if you installed it in the default location, this same path should work)
os.environ['CDF_LIB'] = 'INSERT YOUR CDF LIBRARY PATH HERE'


# function to get single date data
def get_data(year, month, day, dataset):
    # the WIND satellite's MFI CDF files change version values without a clear pattern
    if (year != '2022'):
        version = '_v05'
    elif (int(month) >= 9 and int(day) > 7):
        version = '_v03'
    else:
        version = '_v04'

    # date format
    if len(month) == 1:
        month = '0' + month
    if len(day) == 1:
        day = '0' + day

    # parametic database url by year
    dscovrMFI_URL = 'https://cdaweb.gsfc.nasa.gov/pub/data/dscovr/h0/mag/' + \
        str(year) + '/'
    windMFI_URL = 'https://cdaweb.gsfc.nasa.gov/pub/data/wind/mfi/mfi_h2/' + \
        str(year) + '/'
    windION_URL = 'https://cdaweb.gsfc.nasa.gov/pub/data/wind/swe/swe_h1/' + \
        str(year) + '/'

    # parametic file name and set file download url
    if dataset == 'dscovr':
        assetFolder = 'dscovrMFI'
        filename = 'dscovr_h0_mag_' + year + month + day + '_v01.cdf'
        url = dscovrMFI_URL + filename
    elif dataset == 'wind':
        assetFolder = 'windMFI'
        filename = 'wi_h2_mfi_' + year + month + day + version + '.cdf'
        url = windMFI_URL + filename
    else:
        assetFolder = 'windION'
        filename = 'wi_h1_swe_' + year + month + day + '_v01.cdf'
        url = windION_URL + filename

    # establish local file path
    output_directory = 'C:/Users/Brian/Documents/NASA/nsac-carrington-challenge/assets/' + assetFolder + '/'
    file_path = os.path.join(output_directory, filename)

    # download file if it doesn't exist
    if not os.path.exists(file_path):
        r = requests.get(url, allow_redirects=True)

        with open(file_path, 'wb') as output_file:
            output_file.write(r.content)

    # open CDF file with library
    cdf_pycdf = pycdf.CDF('./assets/' + assetFolder + '/' + filename)

    dens = []
    vel = []
    temp = []
    epoch = []
    sx = []
    sy = []
    sz = []
    bx = []
    by = []
    bz = []
    returnData = {}

    for key in cdf_pycdf.keys():
        if dataset == 'wind' and key == 'Epoch1':
            epoch.append(cdf_pycdf[key][...][0])
            returnData['epoch'] = epoch[0]
        elif key == 'Epoch1':
            epoch.append(cdf_pycdf[key][...])
            returnData['epoch'] = epoch[0]
        if dataset == 'wION' and key == 'Epoch':
            epoch.append(cdf_pycdf[key][...])
            returnData['epoch'] = epoch[0]
        if key == 'BGSE' or key == 'B1GSE':
            sx.append(cdf_pycdf[key][...])
            returnData['sx'] = sx[0]
            sy.append(cdf_pycdf[key][...])
            returnData['sy'] = sy[0]
            sz.append(cdf_pycdf[key][...])
            returnData['sz'] = sz[0]
        if key == 'BGSM' or key == 'B1SDGSE':
            bx.append(cdf_pycdf[key][...])
            returnData['bx'] = bx[0]
            by.append(cdf_pycdf[key][...])
            returnData['by'] = by[0]
            bz.append(cdf_pycdf[key][...])
            returnData['bz'] = bz[0]
        if key == 'Proton_Np_moment':  # density
            dens.append(cdf_pycdf[key][...])
            returnData['dens'] = dens[0]
        if key == 'Proton_V_moment':  # velocity
            vel.append(cdf_pycdf[key][...])
            returnData['vel'] = vel[0]
        if key == 'Proton_W_moment':  # temperature
            temp.append(cdf_pycdf[key][...])
            returnData['temp'] = temp[0]
    return returnData

# Variables guide:
# ----------------
# epoch = timedate. Format: 2021-01-01T00:00:00.000Z
# bx = MFI Bx GSE (nT)
# by = MFI By GSE (nT)
# bz = MFI Bz GSE (nT)
# sx = MFI Vx GSE (km/s)
# sy = MFI Vy GSE (km/s)
# sz = MFI Vz GSE (km/s)
# dens = ION density (cm^-3)
# vel = ION velocity (km/s)
# temp = ION temperature (K)
# ----------------


# function to get data from a date array
def data_iterator(dates, dataset):
    data = []
    for i in range(len(dates)):
        year = dates[i][0:4]
        month = dates[i][5:7]
        day = dates[i][8:10]
        print(year, month, day, dataset)
        data.append(get_data(year, month, day, dataset))
    return data


# dataset_dates is a sample array of dates. It can be replaced with any array of dates and data_iterator will return an array of data for each date
dataset_dates = ['2022-01-01', '2022-01-02', '2022-01-03', '2022-01-04', '2022-01-05', '2022-01-06', '2022-01-07', '2022-01-08', '2022-01-09', '2022-01-10', '2022-01-11', '2022-01-12', '2022-01-13', '2022-01-14', '2022-01-15',
                 '2022-01-16', '2022-01-17', '2022-01-18', '2022-01-19', '2022-01-20', '2022-01-21', '2022-01-22', '2022-01-23', '2022-01-24', '2022-01-25', '2022-01-26', '2022-01-27', '2022-01-28', '2022-01-29', '2022-01-30', '2022-01-31']
dataset_dates = list(dict.fromkeys(dataset_dates))

# Variables: epoch, bx, by, bz, sx, sy, sz
dscovrMFI_data = data_iterator(dataset_dates, 'dscovr')
# Variables: epoch, bx, by, bz, sx, sy, sz
windMFI_data = data_iterator(dataset_dates, 'wind')
# Variables: epoch, dens, vel, temp
windION_data = data_iterator(dataset_dates, 'wION')

# You can now access the data from the arrays.
# For example, to access the density data from the first date in the dataset_dates array, you would use windION_data[0]['dens']

# print(dscovrMFI_data)
# print(windMFI_data)
# print(windION_data)

# this is the data we would use to generate the dataFrames for the models
# we would use transfer learning to train the models (mapping WIND data) and get ION data based on the MFI data
