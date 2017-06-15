from collections import OrderedDict
import numpy as np

inf = np.inf


class RegionParameters(object):
    regionName = "Mrk600A"

    blueSpecFile = 'blue.fits'
    redSpecFile = 'red.fits'
    blueSpecError = 'blue_s_r_A_flux.fits'
    redSpecError = 'red_s_r_A_flux.fits'
    scaleFlux = 1e14                   

    # SPECTRAL LINE INFO FOR ALL EMISSION LINES
    emProfiles = OrderedDict([
       ('H1r_6563A', {'Colour': 'y', 'Order': 19, 'Filter': 'red', 'minI': 750, 'maxI': 830, 'restWavelength': 6562.82, 'ampList': [143.1812795, 22.0749222, 46.187506, 34.0532838], 'zone': 'low', 'sigmaT2': 164.96, 'compLimits': {'a': np.inf, 'c': np.inf, 's': np.inf}, 'copyFrom': None, 'numComps': 3}),
        ('O3_5007A', {'Colour': 'c', 'Order': 2, 'Filter': 'red', 'minI': 1650, 'maxI': 1760, 'restWavelength': 5006.84, 'ampList': [613.726918, 51.3242792, 66.0842939, 14.6123474], 'zone': 'high', 'sigmaT2': 10.39, 'compLimits': {'a': inf, 'c': 0.1, 's': 0.1}, 'copyFrom': None, 'numComps': 4}),
       #('OIII-4959A', {'Colour': 'g', 'Order': 2, 'Filter': 'red', 'minI': 995, 'maxI': 1065, 'restWavelength': 4958.91, 'ampList': 5, 'zone': 'high', 'sigmaT2': 10.39, 'compLimits': {'a': inf, 'c': inf, 's': inf}, 'copyFrom': ['OIII-5007A', 'OIII-5007A', 'OIII-5007A', 'H-Alpha'], 'numComps': 4}),
       #('H-Beta_Blue', {'Colour': 'b', 'Order': 3, 'Filter': 'blue', 'minI': 920, 'maxI': 1060, 'restWavelength': 4861.33, 'ampList': [9.9122054, 6.5330892, 6.8177404, 6], 'zone': 'low', 'sigmaT2': 164.96, 'compLimits': {'a': inf, 'c': 0.01, 's': 0.1}, 'copyFrom': 'H-Alpha', 'numComps': 4}),
       #('H-Beta_Red', {'Colour': 'r', 'Order': 1, 'Filter': 'red', 'minI': 920, 'maxI': 700, 'restWavelength': 4861.33, 'ampList': [73, 14, 22, 17], 'zone': 'low', 'sigmaT2': 164.96, 'compLimits': {'a': inf, 'c': inf , 's': 1}, 'copyFrom': 'H-Alpha', 'numComps': 4}),
       #('H-Gamma', {'Colour': 'r', 'Order': 12, 'Filter': 'blue', 'minI': 1220, 'maxI': 1370, 'restWavelength': 4340.47, 'ampList': [10, 2, 5, 4], 'zone': 'low', 'sigmaT2': 164.96, 'compLimits': {'a': inf, 'c': 0.001, 's': False}, 'copyFrom': 'H-Beta_Red', 'numComps': 4}),
       #('H-Delta', {'Colour': 'c', 'Order': 17, 'Filter': 'blue', 'minI': 1510, 'maxI': 1630, 'restWavelength': 4101.74, 'ampList': [5, 1, 2.5,2], 'zone': 'low', 'sigmaT2': 164.96, 'compLimits': {'a': inf, 'c': 0.001, 's': 1}, 'copyFrom': 'H-Beta_Red', 'numComps': 4}),
     ('N2_6584A', {'Colour': 'violet', 'Order': 19, 'Filter': 'red', 'minI': 870, 'maxI': 1085, 'restWavelength': 6583.41, 'ampList': [35.7953199, 5.5187305, 11.5468765, 8.4], 'zone': 'low', 'sigmaT2': 11.87, 'compLimits': {'a':[inf, inf, inf, (0,20)], 'c': [False, False, False, False], 's': [False, False, False, (9.5,10)]}, 'copyFrom': ['H1r_6563A', 'H1r_6563A', 'H1r_6563A', 'O3_5007A'], 'numComps': 4}),
       #('NII-6548A', {'Colour': 'violet', 'Order': 18, 'Filter': 'red', 'minI': 600, 'maxI': 670, 'restWavelength': 6548.03, 'ampList': [0.857228, 0.4910719, 0.525187], 'zone': 'low', 'sigmaT2': 11.87, 'compLimits': {'a': inf, 'c': 0.001, 's': False}, 'copyFrom': 'NII-6584A', 'numComps': 4}),
       #('SII-6717A', {'Colour': 'r', 'Order': 22, 'Filter': 'red', 'minI': 1820, 'maxI': 2010, 'restWavelength': 6716.47, 'ampList': [1.8877202, 1.261201, 2.1187628], 'zone': 'low', 'sigmaT2': 5.19, 'compLimits': {'a': inf, 'c': inf, 's': False}, 'copyFrom': 'NII-6584A', 'numComps': 4}),
       # ('OII-3729A', {'Colour': '#5D6D7E', 'Order': 24, 'Filter': 'blue', 'minI': 810, 'maxI': 900, 'restWavelength': 3728.82, 'ampList': [9, 0.1, 36, 12], 'zone': 'low', 'sigmaT2': 10.39, 'compLimits': {'a': False, 'c': 0.0005, 's': inf}, 'copyFrom': 'H-Alpha', 'numComps': 4}),
       #('OII-3726A', {'Colour': '#5D6D7E', 'Order': 24, 'Filter': 'blue', 'minI': 750, 'maxI': 810, 'restWavelength': 3726.03, 'ampList': [5, 0.0, 21, 8], 'zone': 'low', 'sigmaT2': 10.39, 'compLimits': {'a': inf, 'c': 0.0005, 's': False}, 'copyFrom': 'OII-3729A', 'numComps': 4}),
       #('HeI-5876A', {'Colour': '#641E16', 'Order': 15, 'Filter': 'red', 'minI': 1320, 'maxI': 1700, 'restWavelength': 5875.64, 'ampList': [0.9957378, 0.6740472, 0.8351281], 'zone': 'high', 'sigmaT2': 41.54, 'compLimits': {'a': inf, 'c': 0.001, 's': [inf, inf, False]}, 'copyFrom': 'OIII-5007A', 'numComps': 4}),
       #('HeI-4471A', {'Colour': '#78281F', 'Order': 30, 'Filter': 'blue', 'minI': 1750, 'maxI': 1900, 'restWavelength': 4471.48, 'ampList': [0.46284, 0.2947801, 0.0391113], 'zone': 'high', 'sigmaT2': 41.54, 'compLimits': {'a': inf, 'c': 0.001, 's': False}, 'copyFrom': 'HeI-5876A', 'numComps': 4}),
       #('HeI-6678A', {'Colour': '#D5D8DC', 'Order': 22, 'Filter': 'red', 'minI': 1050, 'maxI': 1240, 'restWavelength': 6678.15, 'ampList': [0.2301685, 0.2810127, 0.0476801], 'zone': 'high', 'sigmaT2': 41.54, 'compLimits': {'a': inf, 'c': 0.001, 's': False}, 'copyFrom': 'HeI-5876A', 'numComps': 4}),
       #('HeI-7065A', {'Colour': '#E8DAEF', 'Order': 24, 'Filter': 'red', 'minI': 3150, 'maxI': 3450, 'restWavelength': 7065.19, 'ampList': [0.1437774, 0.1282405, 0.0734699], 'zone': 'high', 'sigmaT2': 41.54, 'compLimits': {'a': inf, 'c': False, 's': False}, 'copyFrom': 'HeI-5876A', 'numComps': 4}),
       #('NeIII-3868A', {'Colour': 'r', 'Order': 18, 'Filter': 'blue', 'minI': 1430, 'maxI': 1650, 'restWavelength': 3868.75, 'ampList': [2.4413131, 1.7799793, 2.1882557], 'zone': 'high', 'sigmaT2': 8.24, 'compLimits': {'a': inf, 'c': False, 's': False}, 'copyFrom': 'OIII-5007A', 'numComps': 4}),
       #('NeIII-3970A', {'Colour': 'c', 'Order': 20, 'Filter': 'blue', 'minI': 2110, 'maxI': 2290, 'restWavelength': 3970.07, 'ampList': [1.2004104, 1.238606, 1.6775648], 'zone': 'high', 'sigmaT2': 8.24, 'compLimits': {'a': inf, 'c': False, 's': False}, 'copyFrom': 'OIII-5007A', 'numComps': 4}),
       #('OI-6300A', {'Colour': '#D35400', 'Order': 16, 'Filter': 'red', 'minI': 540, 'maxI': 600, 'restWavelength': 6300.3, 'ampList': [0.3964594, 0.0, 0.4723308, 0.0564203], 'zone': 'low', 'sigmaT2': 10.39, 'compLimits': {'a': inf, 'c': False, 's': False}, 'copyFrom': 'H-Alpha', 'numComps': 4}),
       #('OI-6364A', {'Colour': '#7D6608', 'Order': 19, 'Filter': 'red', 'minI': 2500, 'maxI': 2620, 'restWavelength': 6363.78, 'ampList': [0.0802379, 0.0, 0.2, 0.1], 'zone': 'low', 'sigmaT2': 10.39, 'compLimits': {'c': np.inf, 's': np.inf, 'a': np.inf}, 'copyFrom': 'H-Alpha', 'numComps': 4}),
       #('SIII-9069A', {'Colour': '#27AE60', 'Order': 35, 'Filter': 'red', 'minI': 1720, 'maxI': 1870, 'restWavelength': 9068.9, 'ampList': [1.3819041, 0.9362417, 0.7920365], 'zone': 'low', 'sigmaT2': 5.19, 'compLimits': {'a': inf, 'c': 0.001, 's': 1}, 'copyFrom': 'H-Alpha', 'numComps': 4}),
       ##('NeIII-3967A', {'Colour': 'm', 'Order': 20, 'Filter': 'blue', 'minI': 1950, 'maxI': 2135, 'restWavelength': 3967.46, 'ampList': [0.4933746, 0.2356542, 2.1809342], 'zone': 'high', 'sigmaT2': 8.24, 'compLimits': {'a': inf, 'c': False, 's': False}, 'copyFrom': 'NeIII-3970A', 'numComps': 4}),
       ##('HeIH8-3889A', {'Colour': '#5B2C6F', 'Order': 18, 'Filter': 'blue', 'minI': 2450, 'maxI': 2750, 'restWavelength': 3888.65, 'ampList': [0.0491376, 2.1000132, 4.4749628], 'zone': 'high', 'sigmaT2': 41.54, 'compLimits': {'a': inf, 'c': False, 's': False}, 'copyFrom': 'HeI-5876A', 'numComps': 4}),
       #('SII-6717A', {'Colour': '#58D68D', 'Order': 19, 'Filter': 'red', 'minI': 1010, 'maxI': 1100, 'restWavelength': 6716.4,'ampList': [0.7, 0.0, 4, 1], 'zone': 'low', 'sigmaT2': 5.19, 'compLimits': {'a': inf, 'c': False, 's': False},'copyFrom': 'H-Alpha', 'numComps': 4}),
       #('SII-6731A', {'Colour': '#58D68D', 'Order': 19, 'Filter': 'red', 'minI': 1150, 'maxI': 1270, 'restWavelength': 6730.85, 'ampList': [0.4, 0.0,  2, 0.5], 'zone': 'low', 'sigmaT2': 5.19, 'compLimits': {'a': inf, 'c': False, 's': False}, 'copyFrom': 'SII-6717A', 'numComps': 4}),
       ###('OII-7319A', {'Colour': '#F8C471', 'Order': 26, 'Filter': 'red', 'minI': 2252, 'maxI': 2330, 'restWavelength': 7318.39, 'ampList': [-1.0126892, -0.0315027, 3.5482043], 'zone': 'low', 'sigmaT2': 10.39, 'compLimits': {'a': inf, 'c': inf, 's': inf}, 'copyFrom': 'H-Alpha', 'numComps': 4}),
       ###('OII-7330A', {'Colour': '#7FB3D5', 'Order': 26, 'Filter': 'red', 'minI': 2420, 'maxI': 2520, 'restWavelength': 7330.0, 'ampList': [-1.0488879, -0.5248179, 8.5911851], 'zone': 'low', 'sigmaT2': 10.39, 'compLimits': {'a': inf, 'c': inf, 's': inf}, 'copyFrom': 'H-Alpha', 'numComps': 4}),
       ###('ArIII-7136A', {'Colour': '#0E6655', 'Order': 25, 'Filter': 'red', 'minI': 1713, 'maxI': 1790, 'restWavelength': 7135.78, 'ampList': [0.4554454, -0.2274418, 1.066718], 'zone': 'low', 'sigmaT2': 4.16, 'compLimits': {'c': np.inf, 's': np.inf, 'a': np.inf}, 'copyFrom': 'H-Alpha', 'numComps': 4}),
       ###('HeI-7281A', {'Colour': '#E8DAEF', 'Order': 26, 'Filter': 'red', 'minI': 1465, 'maxI': 1600, 'restWavelength': 7281.35, 'ampList': [0.6740428, 0.8351308, 0.9957380], 'zone': 'low', 'sigmaT2': 41.54, 'compLimits': {'c': np.inf, 's': np.inf, 'a': np.inf}, 'copyFrom': 'H-Alpha', 'numComps': 4}),
    ])

    # Information for the center, sigma and linear for the low (H-alpha) and high (OIII) zones
    centerList = {'low': [1023, 1026, 1037, 1056, 1056], 'high': [1019, 1039, 1060, 1131]}
    sigmaList = {'low': [19, 35.7, 12, 14, 14], 'high': [16, 10, 10, 9.5]}
    linSlope = {'low': 1.9393e-07, 'high': 2.6129e-02}
    linInt = {'low': 0.0761986, 'high':0.147}

    numComps = {'low': 3, 'high': 3}
    componentLabels = ['Narrow 1', 'Broad', 'Narrow 2',  'Narrow 3', 'Narrow 4']
    componentColours = ['b', 'r', 'g', 'c', 'm']
    plottingXRange = [930, 1200]  # velocities
    sigmaInstrBlue = 4.9
    sigmaInstrRed = 5.6
    distance = 4.289e25  # Distance to region in centimetres (same units as flux)

    emLinesForAvgVelCalc = [ 'OIII-5007A']#'H-Alpha', 'H-Beta_Blue', 'OIII-5007A']#, 'NII-6584A', 'SII-6717A']


""" NOTES ON HOW TO USE THE ABOVE TABLE
The limits in 'compLimits' can be in the following forms:
    - a list indicating the limits for each component
    - a single number indicating the limits for ALL components
    - inf: indicating that the component cannot vary

ampList
    - if not list it will be take the copyFrom amplitude List and divide by the ampList scalar

numComps:
    - If numComps is not listed in the emProfile dictionary, then the number of components will be taken from the
    numComps variable depending on the zone set in the emProfile dictionary
"""
