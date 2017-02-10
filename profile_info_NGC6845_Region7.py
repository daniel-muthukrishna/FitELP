from collections import OrderedDict
import numpy as np
inf = np.inf


class RegionParameters(object):
    regionName = "NGC6845 Region 7"

    blueSpecFile = 'NGC6845_7B.fc.fits'             #'NGC6845_7B_SPEC1.wc.fits'
    redSpecFile = 'NGC6845_7R.fc.fits'              #'NGC6845_7R_SPEC1.wc.fits'
    blueSpecError = 'NGC6845_7B_ErrorFlux.fc.fits'  #'NGC6845_7B_VAR4.wc.fits'
    redSpecError = 'NGC6845_7R_ErrorFlux.fc.fits'   #'NGC6845_7R_VAR4.wc.fits'
    scaleFlux = 1e14                                # 1

    # SPECTRAL LINE INFO FOR ALL EMISSION LINES
    emProfiles = OrderedDict([
        ('H-Alpha', {'Colour': 'y', 'Order': 21, 'Filter': 'red', 'minI': 1180, 'maxI': 1650, 'restWavelength': 6562.82, 'ampList': [25.9916388, 17.1349646, 15.3252213, 20, 20, 20, 20, 20], 'zone': 'low', 'sigmaT2': 164.96, 'compLimits': {'a': inf, 'c': inf, 's': inf}, 'copyFrom': None}),
        # ('OIII-5007A', {'Colour': 'c', 'Order': 5, 'Filter': 'red', 'minI': 1500, 'maxI': 2200, 'restWavelength': 5006.84, 'ampList': [27.2484028, 22.1761791, 26.5391571], 'zone': 'high', 'sigmaT2': 41.54, 'compLimits': {'a': inf, 'c': inf, 's': inf}, 'copyFrom': None}),
        # ('OIII-4959A', {'Colour': 'g', 'Order': 4, 'Filter': 'red', 'minI': 2300, 'maxI': 2800, 'restWavelength': 4958.91, 'ampList': 3, 'zone': 'high', 'sigmaT2': 10.39, 'compLimits': {'a': inf, 'c': 0.001, 's': 1}, 'copyFrom': 'OIII-5007A'}),
        # ('H-Beta_Blue', {'Colour': 'b', 'Order': 36, 'Filter': 'blue', 'minI': 2200, 'maxI': 2800, 'restWavelength': 4861.33, 'ampList': [9.9122054, 6.5330892, 6.8177404], 'zone': 'low', 'sigmaT2': 164.96, 'compLimits': {'a': inf, 'c': 0.01, 's': 0.1}, 'copyFrom': 'H-Alpha'}),
        # ('H-Beta_Red', {'Colour': 'r', 'Order': 3, 'Filter': 'red', 'minI': 1640, 'maxI': 2040, 'restWavelength': 4861.33, 'ampList': [9.9122054, 6.5330892, 6.8177404], 'zone': 'low', 'sigmaT2': 164.96, 'compLimits': {'a': inf, 'c': False, 's': False}, 'copyFrom': 'H-Beta_Blue'}),
        # ('H-Gamma', {'Colour': 'r', 'Order': 28, 'Filter': 'blue', 'minI': 700, 'maxI': 1200, 'restWavelength': 4340.47, 'ampList': [4.985869, 3.5976242, 4.4060826], 'zone': 'low', 'sigmaT2': 164.96, 'compLimits': {'a': inf, 'c': 0.001, 's': [inf, inf, False]}, 'copyFrom': 'H-Beta_Blue'}),
        # ('H-Delta', {'Colour': 'c', 'Order': 23, 'Filter': 'blue', 'minI': 1400, 'maxI': 2000, 'restWavelength': 4101.74, 'ampList': [2.9131725, 2.0446065, 2.5207195], 'zone': 'low', 'sigmaT2': 164.96, 'compLimits': {'a': inf, 'c': 0.001, 's': 1}, 'copyFrom': 'H-Beta_Blue'}),
        # ('NII-6584A', {'Colour': 'violet', 'Order': 21, 'Filter': 'red', 'minI': 1740, 'maxI': 2033, 'restWavelength': 6583.41, 'ampList': [2.3182037, 1.4977191, 2.0079195], 'zone': 'low', 'sigmaT2': 11.87, 'compLimits': {'a': inf, 'c': inf, 's': inf}, 'copyFrom': 'H-Alpha'}),
        # ('NII-6548A', {'Colour': 'violet', 'Order': 21, 'Filter': 'red', 'minI': 1030, 'maxI': 1300, 'restWavelength': 6548.03, 'ampList': [0.857228, 0.4910719, 0.525187], 'zone': 'low', 'sigmaT2': 11.87, 'compLimits': {'a': inf, 'c': 0.001, 's': False}, 'copyFrom': 'NII-6584A'}),
        # ('SII-6717A', {'Colour': 'r', 'Order': 22, 'Filter': 'red', 'minI': 1820, 'maxI': 2010, 'restWavelength': 6716.47, 'ampList': [1.8877202, 1.261201, 2.1187628], 'zone': 'low', 'sigmaT2': 5.19, 'compLimits': {'a': inf, 'c': inf, 's': False}, 'copyFrom': 'NII-6584A'}),
        # ('OII-3729A', {'Colour': '#5D6D7E', 'Order': 14, 'Filter': 'blue', 'minI': 2800, 'maxI': 3040, 'restWavelength': 3728.82, 'ampList': [15.5492234, 10.9045454, 11.3158249], 'zone': 'low', 'sigmaT2': 10.39, 'compLimits': {'a': False, 'c': 0.0005, 's': inf}, 'copyFrom': 'NII-6584A'}),
        # ('OII-3726A', {'Colour': '#EC7063', 'Order': 14, 'Filter': 'blue', 'minI': 2600, 'maxI': 2829, 'restWavelength': 3726.03, 'ampList': [9.6560836, 9.7755656, 6.3738786], 'zone': 'low', 'sigmaT2': 10.39, 'compLimits': {'a': inf, 'c': 0.0005, 's': False}, 'copyFrom': 'OII-3729A'}),
        # ('HeI-5876A', {'Colour': '#641E16', 'Order': 15, 'Filter': 'red', 'minI': 1320, 'maxI': 1700, 'restWavelength': 5875.64, 'ampList': [0.9957378, 0.6740472, 0.8351281], 'zone': 'high', 'sigmaT2': 41.54, 'compLimits': {'a': inf, 'c': 0.001, 's': [inf, inf, False]}, 'copyFrom': 'OIII-5007A'}),
        # ('HeI-4471A', {'Colour': '#78281F', 'Order': 30, 'Filter': 'blue', 'minI': 1750, 'maxI': 1900, 'restWavelength': 4471.48, 'ampList': [0.46284, 0.2947801, 0.0391113], 'zone': 'high', 'sigmaT2': 41.54, 'compLimits': {'a': inf, 'c': 0.001, 's': False}, 'copyFrom': 'HeI-5876A'}),
        # ('HeI-6678A', {'Colour': '#D5D8DC', 'Order': 22, 'Filter': 'red', 'minI': 1050, 'maxI': 1240, 'restWavelength': 6678.15, 'ampList': [0.2301685, 0.2810127, 0.0476801], 'zone': 'high', 'sigmaT2': 41.54, 'compLimits': {'a': inf, 'c': 0.001, 's': False}, 'copyFrom': 'HeI-5876A'}),
        # ('HeI-7065A', {'Colour': '#E8DAEF', 'Order': 24, 'Filter': 'red', 'minI': 3150, 'maxI': 3450, 'restWavelength': 7065.19, 'ampList': [0.1437774, 0.1282405, 0.0734699], 'zone': 'high', 'sigmaT2': 41.54, 'compLimits': {'a': inf, 'c': False, 's': False}, 'copyFrom': 'HeI-5876A'}),
        # ('NeIII-3868A', {'Colour': 'r', 'Order': 18, 'Filter': 'blue', 'minI': 1430, 'maxI': 1650, 'restWavelength': 3868.75, 'ampList': [2.4413131, 1.7799793, 2.1882557], 'zone': 'high', 'sigmaT2': 8.24, 'compLimits': {'a': inf, 'c': False, 's': False}, 'copyFrom': 'OIII-5007A'}),
        # ('NeIII-3970A', {'Colour': 'c', 'Order': 20, 'Filter': 'blue', 'minI': 2110, 'maxI': 2290, 'restWavelength': 3970.07, 'ampList': [1.2004104, 1.238606, 1.6775648], 'zone': 'high', 'sigmaT2': 8.24, 'compLimits': {'a': inf, 'c': False, 's': False}, 'copyFrom': 'OIII-5007A'}),
        # ('OI-6300A', {'Colour': '#D35400', 'Order': 19, 'Filter': 'red', 'minI': 1050, 'maxI': 1250, 'restWavelength': 6300.3, 'ampList': [0.3964594, 0.4723308, 0.0564203], 'zone': 'low', 'sigmaT2': 10.39, 'compLimits': {'a': inf, 'c': False, 's': False}, 'copyFrom': 'H-Alpha'}),
        # ('SIII-9069A', {'Colour': '#27AE60', 'Order': 35, 'Filter': 'red', 'minI': 1720, 'maxI': 1870, 'restWavelength': 9068.9, 'ampList': [1.3819041, 0.9362417, 0.7920365], 'zone': 'low', 'sigmaT2': 5.19, 'compLimits': {'a': inf, 'c': 0.001, 's': 1}, 'copyFrom': 'H-Alpha'}),
        ##('NeIII-3967A', {'Colour': 'm', 'Order': 20, 'Filter': 'blue', 'minI': 1950, 'maxI': 2135, 'restWavelength': 3967.46, 'ampList': [0.4933746, 0.2356542, 2.1809342], 'zone': 'high', 'sigmaT2': 8.24, 'compLimits': {'a': inf, 'c': False, 's': False}, 'copyFrom': 'NeIII-3970A'}),
        ##('HeIH8-3889A', {'Colour': '#5B2C6F', 'Order': 18, 'Filter': 'blue', 'minI': 2450, 'maxI': 2750, 'restWavelength': 3888.65, 'ampList': [0.0491376, 2.1000132, 4.4749628], 'zone': 'high', 'sigmaT2': 41.54, 'compLimits': {'a': inf, 'c': False, 's': False}, 'copyFrom': 'HeI-5876A'}),
        ###('SII-6731A', {'Colour': '#58D68D', 'Order': 22, 'Filter': 'red', 'minI': 2100, 'maxI': 2350, 'restWavelength': 6730.85, 'ampList': [0.7603333, 1.1618867, 1.6014093], 'zone': 'low', 'sigmaT2': 5.19, 'compLimits': {'a': inf, 'c': False, 's': False}, 'copyFrom': 'SII-6717A'}),
        ###('OII-7319A', {'Colour': '#F8C471', 'Order': 26, 'Filter': 'red', 'minI': 2252, 'maxI': 2330, 'restWavelength': 7318.39, 'ampList': [-1.0126892, -0.0315027, 3.5482043], 'zone': 'low', 'sigmaT2': 10.39, 'compLimits': {'a': inf, 'c': inf, 's': inf}, 'copyFrom': 'H-Alpha'}),
        ###('OII-7330A', {'Colour': '#7FB3D5', 'Order': 26, 'Filter': 'red', 'minI': 2420, 'maxI': 2520, 'restWavelength': 7330.0, 'ampList': [-1.0488879, -0.5248179, 8.5911851], 'zone': 'low', 'sigmaT2': 10.39, 'compLimits': {'a': inf, 'c': inf, 's': inf}, 'copyFrom': 'H-Alpha'}),
        ###('ArIII-7136A', {'Colour': '#0E6655', 'Order': 25, 'Filter': 'red', 'minI': 1713, 'maxI': 1790, 'restWavelength': 7135.78, 'ampList': [0.4554454, -0.2274418, 1.066718], 'zone': 'low', 'sigmaT2': 4.16, 'compLimits': {'c': np.inf, 's': np.inf, 'a': np.inf}, 'copyFrom': 'H-Alpha'}),
        ###('OI-6364A', {'Colour': '#7D6608', 'Order': 19, 'Filter': 'red', 'minI': 2500, 'maxI': 2620, 'restWavelength': 6363.78, 'ampList': [2.0802379, -308.5885481, -32.2254134], 'zone': 'low', 'sigmaT2': 10.39, 'compLimits': {'c': np.inf, 's': np.inf, 'a': np.inf}, 'copyFrom': 'H-Alpha'}),
        ###('HeI-7281A', {'Colour': '#E8DAEF', 'Order': 26, 'Filter': 'red', 'minI': 1465, 'maxI': 1600, 'restWavelength': 7281.35, 'ampList': [0.6740428, 0.8351308, 0.9957380], 'zone': 'low', 'sigmaT2': 41.54, 'compLimits': {'c': np.inf, 's': np.inf, 'a': np.inf}, 'copyFrom': 'H-Alpha'}),
    ])

    # Information for the center, sigma and linear for the low (H-alpha) and high (OIII) zones
    centerList = {'low': [6315.53629, 6349.20112, 6328.97812, 6330, 6330, 6330, 6330, 6330], 'high': [6314.57924, 6348.46578, 6333.03654]}
    sigmaList = {'low': [22.2648068, 19.2854733, 64.1691783, 70, 50, 50, 50, 50], 'high': [16.6297232, 15.9659592, 56.3789640]}
    linSlope = {'low': 1.9393e-07, 'high': 2.6129e-06}
    linInt = {'low': 0.00761986, 'high': -0.00147741}

    numComps = 8
    componentLabels = ['Narrow 1', 'Narrow 2', 'Broad 1', 'Broad 2', 'Comp 5', 'Comp6', 'c7', 'c8']
    componentColours = ['b', 'r', 'g', 'y', 'm', 'k', 'b', 'r']
    plottingXRange = [6150, 6500]  # velocities
    sigmaInstrBlue = 4.9
    sigmaInstrRed = 5.6
    distance = 2.83e26  # Distance to region in centimetres (same units as flux)

    emLinesForAvgVelCalc = ['H-Alpha', 'H-Beta_Blue', 'OIII-5007A', 'NII-6584A', 'SII-6717A']


""" NOTES ON HOW TO USE THE ABOVE TABLE
The limits in 'compLimits' can be in the following forms:
    - a list indicating the limits for each component
    - a single number indicating the limits for ALL components
    - inf: indicating that the component cannot vary

ampList
    - if not list it will be take the copyFrom amplitude List and divide by the ampList scalar
"""
