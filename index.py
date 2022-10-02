# imports
from calendar import EPOCH
from spacepy import pycdf
from dtw import *
import numpy as np
import pandas as pd
import requests
import datetime
import os
os.environ['CDF_LIB'] = 'C:/Program Files/CDF_Distribution/cdf38_1-dist/lib'

# function to get single date data

# epoch = tiempo. Formato: 2021-01-01T00:00:00.000Z
# bx = campo magnético en x (nT)
# by = campo magnético en y (nT)
# bz = campo magnético en z (nT)
# sx = campo elíptico en x (nT)
# sy = campo elíptico en y (nT)
# sz = campo elíptico en z (nT)


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

    for key in cdf_pycdf.keys():
        if dataset == 'wind' and key == 'Epoch1':
            epoch = []
            iterate = cdf_pycdf[key][...]
            for i in range(10):
                epoch.append(iterate[i][0])
        elif key == 'Epoch1':
            epoch = []
            iterate = cdf_pycdf[key][...]
            for i in range(10):
                epoch.append(iterate[i])
        if key == 'BGSE' or key == 'B1GSE':
            sx = []
            sy = []
            sz = []
            iterate = cdf_pycdf[key][...]
            for i in range(10):
                sx.append(iterate[i][0])
                sy.append(iterate[i][1])
                sz.append(iterate[i][2])
        if key == 'BGSM' or key == 'B1SDGSE':
            bx = []
            by = []
            bz = []
            iterate = cdf_pycdf[key][...]
            for i in range(10):
                bx.append(iterate[i][0])
                by.append(iterate[i][1])
                bz.append(iterate[i][2])

    return {'epoch': epoch, 'bx': bx, 'by': by}


# function to get data from a date array


def data_iterator(dates, dataset):
    data = []
    for i in range(len(dates)):
        year = dates[i][0:4]
        month = dates[i][5:7]
        day = dates[i][8:10]
        data.append(get_data(year, month, day, dataset))

    return data

# query = data_iterator(['2022-01-01', '2022-01-02'], 'dscovr')
# template = data_iterator(['2022-01-01', '2022-01-02'], 'wind')

# for i in query:
#     print(i['epoch'])


# with open('persons.csv', 'wb') as csvfile:
#     filewriter = csv.writer(csvfile, delimiter=',',
#                             quotechar='|', quoting=csv.QUOTE_MINIMAL)
#     for i in query:
#         filewriter.writerow(['Epoch', i['epoch']])
#         filewriter.writerow(['BX', i['bx']])
#         filewriter.writerow(['BY', i['by']]))
# date_array = ['2022-01-01', '2022-01-02']


# query = get_data('2022', '01', '01', 'dscovr')['epoch']
# template = get_data('2022', '01', '01', 'wind')['epoch']


# query = np.array(query)
# template = np.array(template)
# timedate = datetime.datetime(2022, 1, 1, 0, 0).timestamp()
# Find the best match with the canonical recursion formula
# alignment = dtw(int(timedate), int(timedate), keep_internals=True)
# print(alignment)

# Align and plot with the Rabiner-Juang type VI-c unsmoothed recursion
# dtw(query, template, keep_internals=True,
#     step_pattern=rabinerJuangStepPattern(6, "c"))\
#     .plot(type="twoway", offset=-2)

# See the recursion relation, as formula and diagram
# print(rabinerJuangStepPattern(6, "c"))
# rabinerJuangStepPattern(6, "c").plot()
