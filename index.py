# imports
from spacepy import pycdf
import pandas as pd
import requests
import os
os.environ['CDF_LIB'] = 'C:/Program Files/CDF_Distribution/cdf38_1-dist/lib'

#! parametrizar variables de directorios por variables de entorno


def get_data(year, month, day, dataset):
    if (year != '2022'):
        version = '_v05'
    elif (int(month) <= 9 and int(day) < 8):
        version = '_v04'
    else:
        version = '_v03'

    if len(month) == 1:
        month = '0' + month
    if len(day) == 1:
        day = '0' + day

    dscovrMFI_URL = 'https://cdaweb.gsfc.nasa.gov/pub/data/dscovr/h0/mag/' + \
        str(year) + '/'
    windMFI_URL = 'https://cdaweb.gsfc.nasa.gov/pub/data/wind/mfi/mfi_h2/' + \
        str(year) + '/'
    windION_URL = 'https://cdaweb.gsfc.nasa.gov/pub/data/wind/swe/swe_h1/' + \
        str(year) + '/'

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

    output_directory = 'C:/Users/Brian/Documents/NASA/nsac-carrington-challenge/assets/' + assetFolder + '/'
    file_path = os.path.join(output_directory, filename)

    if not os.path.exists(file_path):
        r = requests.get(url, allow_redirects=True)

        with open(file_path, 'wb') as output_file:
            output_file.write(r.content)

    cdf_pycdf = pycdf.CDF('./assets/' + assetFolder + '/' + filename)

    print(cdf_pycdf)


get_data('2022', '09', '11', 'wind')
