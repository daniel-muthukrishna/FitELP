from collections import OrderedDict
import numpy as np
inf = np.inf


class RegionParameters(object):
    regionName = "IIZw33KnotB"

    blueSpecFile = 'blue_cut_IIZw33B_.fits'
    redSpecFile = 'red_zwB.fits'
    blueSpecError = 'blue_Err_flux_zwb.fits'
    redSpecError = 'red_Err_flux_zwb.fits'
    scaleFlux = 1e14

    # SPECTRAL LINE INFO FOR ALL EMISSION LINES
    emProfiles = OrderedDict([
    ('H-Alpha', {'Colour': 'y', 'Order': 19, 'Filter': 'red', 'minI': 1120, 'maxI': 1310, 'restWavelength': 6562.82,'ampList': [32, 100, 11], 'zone': 'low', 'sigmaT2': 164.96, 'compLimits': {'a': inf, 'c': [0.0011, 0.001, 0.001], 's': inf}, 'copyFrom': None}),
      #('H-Alpha-2', {'Colour': 'y', 'Order': 19, 'Filter': 'red', 'minI': 1120, 'maxI': 1310, 'restWavelength': 6562.82, 'ampList': [25, 90, 7, 5], 'zone': 'low2', 'sigmaT2': 164.96, 'compLimits': {'a': inf, 'c': [False, False, False, 0.01], 's': inf}, 'copyFrom': None}),
    #('OIII-5007A', {'Colour': 'c', 'Order': 3, 'Filter': 'red', 'minI': 1030, 'maxI': 1140, 'restWavelength': 5006.84, 'ampList': [80, 65, 23], 'zone': 'high', 'sigmaT2': 41.54, 'compLimits': {'a': inf, 'c': 0.1, 's': 0.1}, 'copyFrom': None}),
    ('OIII-5007A-2', {'Colour': 'c', 'Order': 3, 'Filter': 'red', 'minI': 1030, 'maxI': 1140, 'restWavelength': 5006.84,'ampList': [25, 80, 11, 5], 'zone': 'high2', 'sigmaT2': 41.54, 'compLimits': {'a': inf, 'c': inf, 's': inf}, 'copyFrom': None}),
   # ('H-Alpha-2', {'Colour': 'y', 'Order': 19, 'Filter': 'red', 'minI': 1120, 'maxI': 1310, 'restWavelength': 6562.82, 'ampList': [25, 90, 7, 5], 'zone': 'low2', 'sigmaT2': 164.96, 'compLimits': {'a': inf, 'c': inf, 's': inf}, 'copyFrom': 'OIII-5007A-2'}),
      #('OIII-4959A', {'Colour': 'c', 'Order': 2, 'Filter': 'red', 'minI': 1410, 'maxI': 1490, 'restWavelength': 4958.91, 'ampList': [10, 30, 21], 'zone': 'high', 'sigmaT2': 41.54, 'compLimits': {'a': inf, 'c': False, 's': False}, 'copyFrom': 'OIII-5007A'}),
      #('OIII-4959A-2', {'Colour': 'c', 'Order': 2, 'Filter': 'red', 'minI': 1410, 'maxI': 1490, 'restWavelength': 4958.91, 'ampList': [10, 30, 4.5, 0.5], 'zone': 'high2', 'sigmaT2': 41.54, 'compLimits': {'a': inf, 'c': False, 's': False}, 'copyFrom': 'OIII-5007A-2'}),
      #'OIII-4363A', {'Colour': 'c', 'Order': 11, 'Filter': 'blue', 'minI': 1118, 'maxI': 1210, 'restWavelength': 4363.2, 'ampList': [0.51,0.52,0.53], 'zone': 'high', 'sigmaT2': 41.54, 'compLimits': {'a': inf, 'c': False, 's': False}, 'copyFrom': 'OIII-5007A'}),
      #('H-Beta_Blue', {'Colour': 'b', 'Order': 3, 'Filter': 'blue', 'minI': 1500, 'maxI': 1640, 'restWavelength': 4861.33, 'ampList': 4, 'zone': 'high2', 'sigmaT2': 164.96, 'compLimits': {'a': inf, 'c': [inf,inf,inf,False], 's': [inf,inf,inf, False]}, 'copyFrom': 'OIII-5007A-2'}),
    #('H-Beta_Blue', {'Colour': 'b', 'Order': 3, 'Filter': 'blue', 'minI': 1500, 'maxI': 1640, 'restWavelength': 4861.33, 'ampList': 4, 'zone': ['low','low','low','high2'], 'sigmaT2': 164.96, 'compLimits': {'a': inf, 'c': [inf,inf,inf,False], 's': [inf,inf,inf, False]}, 'copyFrom': ['H-Alpha','H-Alpha','H-Alpha', 'OIII-5007A-2']}),
      #('H-Beta_Blue', {'Colour': 'b', 'Order': 3, 'Filter': 'blue', 'minI': 1500, 'maxI': 1640, 'restWavelength': 4861.33, 'ampList':  [110, 33, 4], 'zone': 'low', 'sigmaT2': 164.96, 'compLimits': {'a': inf, 'c': False, 's': False},'copyFrom': 'H-Alpha'}),
      #('H-Beta_Red', {'Colour': 'r', 'Order': 1, 'Filter': 'red', 'minI': 550, 'maxI': 700, 'restWavelength': 4861.33, 'ampList': [73, 14, 22, 17], 'zone': 'low', 'sigmaT2': 164.96, 'compLimits': {'a': inf, 'c': 0.05, 's': 0.05}, 'copyFrom': 'H-Alpha'}),
      #('H-Gamma', {'Colour': 'r', 'Order': 11, 'Filter': 'blue', 'minI': 550, 'maxI': 760, 'restWavelength': 4340.47,'ampList': 3, 'zone': 'low', 'sigmaT2': 164.96, 'compLimits': {'a': inf, 'c': False, 's': False}, 'copyFrom': 'H-Beta_Blue'}),
      #('H-Delta', {'Colour': 'c', 'Order': 16, 'Filter': 'blue', 'minI': 920, 'maxI': 1080, 'restWavelength': 4101.74, 'ampList': 3, 'zone': 'low', 'sigmaT2': 164.96, 'compLimits': {'a': inf, 'c': False, 's': False}, 'copyFrom': 'H-Beta_Blue'}),
    #('H-7', {'Colour': 'c', 'Order': 19, 'Filter': 'blue', 'minI': 1104, 'maxI': 1230, 'restWavelength': 3970.07, 'ampList': 3, 'zone': 'low', 'sigmaT2': 164.96, 'compLimits': {'a': inf, 'c': False, 's': False}, 'copyFrom': 'H-Beta_Blue'}),
    #('H-11', {'Colour': 'c', 'Order': 23, 'Filter': 'blue', 'minI': 1410, 'maxI': 1570, 'restWavelength': 3770.63, 'ampList': 3, 'zone': 'low', 'sigmaT2': 164.96, 'compLimits': {'a': inf, 'c': False, 's': False}, 'copyFrom': 'H-Beta_Blue'}),
      #('H-10', {'Colour': 'c', 'Order': 23, 'Filter': 'blue', 'minI': 1030, 'maxI': 1230, 'restWavelength': 3798.00, 'ampList': 3, 'zone': 'low', 'sigmaT2': 164.96, 'compLimits': {'a': inf, 'c': 0.05, 's': 0.1, 'copyFrom': 'H-Beta_Blue'}),
      #('H-9', {'Colour': 'c', 'Order': 22, 'Filter': 'blue', 'minI': 970, 'maxI': 1090, 'restWavelength': 3835.39, 'ampList': 3, 'zone': 'low', 'sigmaT2': 164.96, 'compLimits': {'a': inf, 'c': False, 's': False}, 'copyFrom': 'H-Beta_Blue'}),
      #('H-13', {'Colour': 'c', 'Order': 24, 'Filter': 'blue', 'minI': 457, 'maxI': 570, 'restWavelength': 3734.37, 'ampList': 3, 'zone': 'low', 'sigmaT2': 164.96, 'compLimits': {'a': inf, 'c': False, 's': False}, 'copyFrom': 'H-Beta_Blue'}),
      ('NII-6584A', {'Colour': 'violet', 'Order': 19, 'Filter': 'red', 'minI': 1370, 'maxI': 1485, 'restWavelength': 6583.41, 'ampList': 4, 'zone': 'low', 'sigmaT2': 11.87, 'compLimits': {'a': inf, 'c':[inf,inf,inf,False], 's': [inf,inf,inf, False]}, 'copyFrom': ['H-Alpha','H-Alpha','H-Alpha', 'OIII-5007A-2']}),
      #('NII-6548A', {'Colour': 'violet', 'Order': 19, 'Filter': 'red', 'minI': 980, 'maxI': 1100, 'restWavelength': 6548.03, 'ampList': [1, 1, 1], 'zone': 'low', 'sigmaT2': 11.87, 'compLimits': {'a': inf, 'c': 0.04, 's': 0.1}, 'copyFrom': 'NII-6584A'}),
      #('SII-6717A', {'Colour': 'r', 'Order': 20, 'Filter': 'red', 'minI': 1420, 'maxI': 1520, 'restWavelength': 6716.47, 'ampList': [2,2, 2], 'zone': 'low', 'sigmaT2': 5.19, 'compLimits': {'a': inf, 'c': inf, 's': False}, 'copyFrom': 'NII-6584A'}),
      #('SII-6730A', {'Colour': 'r', 'Order': 20, 'Filter': 'red', 'minI': 1580, 'maxI': 1675, 'restWavelength': 6730.8,'ampList': [1, 1, 1], 'zone': 'low', 'sigmaT2': 5.19,'compLimits': {'a': inf, 'c': 0.004, 's': False}, 'copyFrom': 'SII-6717A'}),
      #('SII-6312A', {'Colour': 'r', 'Order': 17, 'Filter': 'red', 'minI': 1000, 'maxI': 1000, 'restWavelength': 6312.3,'ampList': [0.51, 0.51, 0.51], 'zone': 'low', 'sigmaT2': 5.19,'compLimits': {'a': inf, 'c': 0.01, 's': 0.01}, 'copyFrom': 'OIII-5007A-2'}),
      #('OII-3729A', {'Colour': '#5D6D7E', 'Order': 25, 'Filter': 'blue', 'minI': 1400, 'maxI': 1490, 'restWavelength': 3728.82, 'ampList': [7, 7,7], 'zone': 'low', 'sigmaT2': 10.39, 'compLimits': {'a': False, 'c': False, 's': False}, 'copyFrom': 'H-Alpha'}),
      #('OII-3726A', {'Colour': '#5D6D7E', 'Order': 25, 'Filter': 'blue', 'minI': 1320, 'maxI': 1405, 'restWavelength': 3726.032, 'ampList': [5, 5, 5], 'zone': 'low', 'sigmaT2': 10.39, 'compLimits': {'a': inf, 'c': False, 's': False}, 'copyFrom': 'OII-3729A'}),
      #('HeI-5876A', {'Colour': '#641E16', 'Order': 15, 'Filter': 'red', 'minI': 1320, 'maxI': 1700, 'restWavelength': 5875.64, 'ampList': [8, 6,4], 'zone': 'high', 'sigmaT2': 41.54, 'compLimits': {'a': inf, 'c': 0.01, 's': 0.01}, 'copyFrom': 'OIII-5007A-2'}),
      #('HeI-4471A', {'Colour': '#78281F', 'Order': 30, 'Filter': 'blue', 'minI': 1750, 'maxI': 1900, 'restWavelength': 4471.48, 'ampList': [0.46284, 0.2947801, 0.0391113], 'zone': 'high', 'sigmaT2': 41.54, 'compLimits': {'a': inf, 'c': 0.001, 's': False}, 'copyFrom': 'HeI-5876A'}),
        # ('HeI-6678A', {'Colour': '#D5D8DC', 'Order': 22, 'Filter': 'red', 'minI': 1050, 'maxI': 1240, 'restWavelength': 6678.15, 'ampList': [0.2301685, 0.2810127, 0.0476801], 'zone': 'high', 'sigmaT2': 41.54, 'compLimits': {'a': inf, 'c': 0.001, 's': False}, 'copyFrom': 'HeI-5876A'}),
        # ('HeI-7065A', {'Colour': '#E8DAEF', 'Order': 24, 'Filter': 'red', 'minI': 3150, 'maxI': 3450, 'restWavelength': 7065.19, 'ampList': [0.1437774, 0.1282405, 0.0734699], 'zone': 'high', 'sigmaT2': 41.54, 'compLimits': {'a': inf, 'c': False, 's': False}, 'copyFrom': 'HeI-5876A'}),
        # ('NeIII-3868A', {'Colour': 'r', 'Order': 18, 'Filter': 'blue', 'minI': 1430, 'maxI': 1650, 'restWavelength': 3868.75, 'ampList': [2.4413131, 1.7799793, 2.1882557], 'zone': 'high', 'sigmaT2': 8.24, 'compLimits': {'a': inf, 'c': False, 's': False}, 'copyFrom': 'OIII-5007A'}),
        # ('NeIII-3970A', {'Colour': 'c', 'Order': 20, 'Filter': 'blue', 'minI': 2110, 'maxI': 2290, 'restWavelength': 3970.07, 'ampList': [1.2004104, 1.238606, 1.6775648], 'zone': 'high', 'sigmaT2': 8.24, 'compLimits': {'a': inf, 'c': False, 's': False}, 'copyFrom': 'OIII-5007A'}),
       #('OI-6300A', {'Colour': '#D35400', 'Order': 17, 'Filter': 'red', 'minI': 954, 'maxI': 1030, 'restWavelength': 6300.3, 'ampList': [1, 1, 1], 'zone': 'low', 'sigmaT2': 10.39, 'compLimits': {'a': inf, 'c': False, 's': False}, 'copyFrom': 'H-Alpha'}),
       #('OI-6364A', {'Colour': '#D35400', 'Order': 17, 'Filter': 'red', 'minI': 1570, 'maxI': 1800, 'restWavelength': 6363.78, 'ampList': [0.41, 0.41, 0.41], 'zone': 'low', 'sigmaT2': 10.39, 'compLimits': {'c': False, 's': False, 'a': inf}, 'copyFrom': 'H-Alpha'}),
        # ('SIII-9069A', {'Colour': '#27AE60', 'Order': 35, 'Filter': 'red', 'minI': 1720, 'maxI': 1870, 'restWavelength': 9068.9, 'ampList':3, 'zone': 'low', 'sigmaT2': 5.19, 'compLimits': {'a': inf, 'c': 0.001, 's': 1}, 'copyFrom': 'H-Alpha'}),
        ##('NeIII-3967A', {'Colour': 'm', 'Order': 20, 'Filter': 'blue', 'minI': 1950, 'maxI': 2135, 'restWavelength': 3967.46, 'ampList': [0.4933746, 0.2356542, 2.1809342], 'zone': 'high', 'sigmaT2': 8.24, 'compLimits': {'a': inf, 'c': False, 's': False}, 'copyFrom': 'NeIII-3970A'}),
        ##('HeIH8-3889A', {'Colour': '#5B2C6F', 'Order': 18, 'Filter': 'blue', 'minI': 2450, 'maxI': 2750, 'restWavelength': 3888.65, 'ampList': [0.0491376, 2.1000132, 4.4749628], 'zone': 'high', 'sigmaT2': 41.54, 'compLimits': {'a': inf, 'c': False, 's': False}, 'copyFrom': 'HeI-5876A'}),
        ###('OII-7319A', {'Colour': '#F8C471', 'Order': 26, 'Filter': 'red', 'minI': 2252, 'maxI': 2330, 'restWavelength': 7318.39, 'ampList': [-1.0126892, -0.0315027, 3.5482043], 'zone': 'low', 'sigmaT2': 10.39, 'compLimits': {'a': inf, 'c': inf, 's': inf}, 'copyFrom': 'H-Alpha'}),
        ###('OII-7330A', {'Colour': '#7FB3D5', 'Order': 26, 'Filter': 'red', 'minI': 2420, 'maxI': 2520, 'restWavelength': 7330.0, 'ampList': [-1.0488879, -0.5248179, 8.5911851], 'zone': 'low', 'sigmaT2': 10.39, 'compLimits': {'a': inf, 'c': inf, 's': inf}, 'copyFrom': 'H-Alpha'}),
        ###('ArIII-7136A', {'Colour': '#0E6655', 'Order': 25, 'Filter': 'red', 'minI': 1713, 'maxI': 1790, 'restWavelength': 7135.78, 'ampList': [0.4554454, -0.2274418, 1.066718], 'zone': 'low', 'sigmaT2': 4.16, 'compLimits': {'c': np.inf, 's': np.inf, 'a': np.inf}, 'copyFrom': 'H-Alpha'}),
        ###('HeI-7281A', {'Colour': '#E8DAEF', 'Order': 26, 'Filter': 'red', 'minI': 1465, 'maxI': 1600, 'restWavelength': 7281.35, 'ampList': [0.6740428, 0.8351308, 0.9957380], 'zone': 'low', 'sigmaT2': 41.54, 'compLimits': {'c': np.inf, 's': np.inf, 'a': np.inf}, 'copyFrom': 'H-Alpha'}),
    ])

    # Information for the center, sigma and linear for the low (H-alpha) and high (OIII) zones
    centerList = {'low': [2791, 2795, 2804],'low2': [2791, 2795, 2804, 2880], 'high': [2796, 2797, 2805], 'high2': [2791, 2796, 2805, 2900]}
    sigmaList = {'low': [34, 24, 14],'low2': [20, 20, 21, 15], 'high': [40, 15, 20], 'high2': [20, 10, 18, 15]}
    linSlope = {'low': 0.0,'low2': 0.0, 'high': 0.0, 'high2': 0.0}
    linInt = {'low': 0.1,'low2': 0.1, 'high': 0.01, 'high2': 0.0041}

    #numComps = 4
    numComps = {'low': 3,'low2': 4, 'high': 3, 'high2': 4}
    componentLabels = ['g1', 'g2', 'g3','g4']
    componentColours = ['b', 'r','y', 'g']
    plottingXRange = [2600, 3000]  # velocities
    sigmaInstrBlue = 4.9
    sigmaInstrRed = 5.6
    distance = 4.289e25  # Distance to region in centimetres (same units as flux)

#   emLinesForAvgVelCalc = ['H-Alpha', 'H-Beta_Blue', 'OIII-5007A', 'NII-6584A', 'SII-6717A']
 #  emLinesForAvgVelCalc = ['H-Alpha', 'H-Beta_Red', 'OIII-5007A','OIII-4959A']
 #  emLinesForAvgVelCalc = ['H-Alpha']


""" NOTES ON HOW TO USE THE ABOVE TABLE
The limits in 'compLimits' can be in the following forms:
    - a list indicating the limits for each component
    - a single number indicating the percentage limits for ALL components
    - a tuple (minValue, maxValue) indicating the min and max not in a percentage
    - inf: indicating that the component cannot vary
    - False: indicating that the value is fixed

ampList
    - if not list it will be take the copyFrom amplitude List and divide by the ampList scalar

numComps:
    - If numComps is not listed in the emProfile dictionary, then the number of components will be taken from the
    numComps variable depending on the zone set in the emProfile dictionary
"""