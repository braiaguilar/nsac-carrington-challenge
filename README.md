We are provided with links to the databases that we must consume to obtain the variety of
Measurement of these satellites and that the content of this database is cdf files that we download and parse
To get your variables.
We have 3 databases provided: 2 with measurements of the electromagnetic field obtained one by the DSCOVR and the other by the WIND and 1 database with measurements of the properties of the solar winds obtained by the WIND satellite. In all 3 cases we have cdf files. Only with different variables for the MFI measurements with respect to those of the solar winds.
Each cdf file contains monitoring data for one day,
stored in variables with unintuitive names that must be interpreted and formatted in order to
be used

After carrying out this process, we filter and keep the significant variables for the solution of the problem in each case.
for the MFI measurements of WIND and DSCOVR, we get 7 variables:
- epochMFI = type datetime (time). Format: 2021-01-01T00:00:00.000Z
- bx = magnetic field at x (nT)
- by = magnetic field at y (nT)
- bz = magnetic field at z (nT)
- sx = elliptic field at x (nT)
- sy = elliptic field in y (nT)
- sz = elliptic field in z (nT)
Corresponding the different variables b and s (x, y, z) to vector coordinates

When we filter out the significant variables for the solar wind measurements taken by WIND we get 4 variables:
- epochION = type datetime (time). Format: 2021-01-01T00:00:00.000Z
- dens = density. type float(32)
- vel = speed. type float(32)
- temp = temperature. type float(32)

The unit of measurement for all variables of the solar wind is nanotesla ((10^−9) of a tesla tesla)

Taking these variables into account, we have a common datum between both measurements, which is the time variable. This helps us to establish a relationship that we will later use when training our neural network.
Before using the time variable, we will parse it to milliseconds, in order to treat it as an integer and avoid later data type compatibility problems with the libraries we will use.

The neural network expects a dataset that we will make up of a series of dataframes, which is a data type similar to a table, with rows and columns that in our case will represent measured days and variable values ​​for those days, respectively.

Here's an example of the final dataFrame format:
https://colab.research.google.com/drive/1vjyx-FwlHfLesrHUPRXbgrwCHrYlMi-I?usp=sharing

These dataframes will be obtained using the variables we have and parsing them through the Pandas Python library. Specifically using using the property (function) of pandas:
pandas.DataFrame(data=None, index=None, columns=None, dtype=None, copy=None)