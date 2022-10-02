# imports
from spacepy import pycdf
from dtw import *
import numpy as np
import pandas as pd
import requests
import datetime
import os
os.environ['CDF_LIB'] = 'C:/Program Files/CDF_Distribution/cdf38_1-dist/lib'

#! parametrizar variables de directorios por variables de entorno

# function to get single date data


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
        if key == 'Epoch1':
            # if dataset == 'wind' and key == 'Epoch1':
            epoch = []
            iterate = cdf_pycdf[key][...]
            for i in range(10):
                date = datetime.datetime.fromtimestamp(iterate[i]).strftime('%S')
                date *= 1000
                epoch.append(date)
        if key == 'BGSE' or key == 'B1GSE':
            bx = []
            iterate = cdf_pycdf[key][...]
            for i in range(10):
                bx.append(iterate[i])
        if key == 'BGSM' or key == 'B1SDGSE':
            by = []
            iterate = cdf_pycdf[key][...]
            for i in range(10):
                by.append(iterate[i])

    return {'epoch': epoch, 'bx': bx, 'by': by}

# df = get_data('2022', '01', '01', 'dscovr')
# print(df)

# function to get data from a date array


def data_iterator(dates, dataset):
    # year, month, day
    data = []
    for i in range(len(dates)):
        year = dates[i][0:4]
        month = dates[i][5:7]
        day = dates[i][8:10]
        data.append(get_data(year, month, day, dataset))

    return data


query = data_iterator(['2022-01-01', '2022-01-02'], 'dscovr')
template = data_iterator(['2022-01-01', '2022-01-02'], 'wind')

# for i in query:
#     print(i['epoch'])

# with open('persons.csv', 'wb') as csvfile:
#     filewriter = csv.writer(csvfile, delimiter=',',
#                             quotechar='|', quoting=csv.QUOTE_MINIMAL)
#     for i in query:
#         filewriter.writerow(['Epoch', i['epoch']])
#         filewriter.writerow(['BX', i['bx']])
#         filewriter.writerow(['BY', i['by']])

query = get_data('2022', '01', '01', 'dscovr')['epoch']
template = get_data('2022', '01', '01', 'wind')['epoch']
query = np.array(query)
template = np.array(template)
# Find the best match with the canonical recursion formula
alignment = dtw(query, template, keep_internals=True)
print(template)

# Display the warping curve, i.e. the alignment curve
# alignment.plot(type="threeway")


# Align and plot with the Rabiner-Juang type VI-c unsmoothed recursion
# dtw(query, template, keep_internals=True,
#     step_pattern=rabinerJuangStepPattern(6, "c"))\
#     .plot(type="twoway", offset=-2)

# See the recursion relation, as formula and diagram
# print(rabinerJuangStepPattern(6, "c"))
# rabinerJuangStepPattern(6, "c").plot()
