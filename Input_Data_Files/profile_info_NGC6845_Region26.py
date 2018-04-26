from collections import OrderedDict
import numpy as np
inf = np.inf


class RegionParameters(object):
    regionName = "NGC6845-26"

    blueSpecFile =  'NGC6845_26B.fc.fits'             #'NGC6845_26B_SPEC1.wc.fits'
    redSpecFile = 'NGC6845_26R.fc.fits'              #'NGC6845_26R_SPEC1.wc.fits'
    blueSpecError = 'NGC6845_26B_ErrorFlux.fc.fits'  #'NGC6845_26B_VAR4.wc.fits'
    redSpecError = 'NGC6845_26R_ErrorFlux.fc.fits'   #'NGC6845_26R_VAR4.wc.fits'
    scaleFlux = 1e14                                # 1

    # SPECTRAL LINE INFO FOR ALL EMISSION LINES
    emProfiles = OrderedDict([
        ('H-Alpha', {'Colour': 'y', 'Order': 21, 'Filter': 'red', 'minI': 1180, 'maxI': 1700, 'restWavelength': 6562.82, 'ampList': [0.4629591, 2.328812, 0.9343802], 'zone': 'low', 'sigmaT2': 164.96, 'compLimits': {'c': np.inf, 's': np.inf, 'a': np.inf}, 'copyFrom': None}),
        ('OIII-5007A', {'Colour': 'c', 'Order': 5, 'Filter': 'red', 'minI': 1600, 'maxI': 2100, 'restWavelength': 5006.84, 'ampList': [0.039014, 0.0912511, 0.2074293], 'zone': 'high', 'sigmaT2': 10.39, 'compLimits': {'c': np.inf, 's': np.inf, 'a': np.inf}, 'copyFrom': None}),
        #('OIII-4959A', {'Colour': 'g', 'Order': 4, 'Filter': 'red', 'minI': 2300, 'maxI': 2700, 'restWavelength': 4958.91, 'ampList': [0.0080434, 0.0391648, 0.0678399], 'zone': 'high', 'sigmaT2': 10.39, 'compLimits': {'c': 0.01, 's': 0.05, 'a': np.inf}, 'copyFrom': 'OIII-5007A'}),
        #H-Beta_Blue:
        #('H-Beta', {'Colour': 'b', 'Order': 36, 'Filter': 'blue', 'minI': 2000, 'maxI': 2700, 'restWavelength': 4861.33, 'ampList': [0.1092102, 0.5498035, 0.1678219], 'zone': 'low', 'sigmaT2': 164.96, 'compLimits': {'c': 0.01, 's': 0.01, 'a': np.inf}, 'copyFrom': 'H-Alpha'}),
        #('H-Beta_Red', {'Colour': 'r', 'Order': 3, 'Filter': 'red', 'minI': 1640, 'maxI': 2040, 'restWavelength': 4861.33, 'ampList': [9.9122054, 6.5330892, 6.8177404], 'zone': 'low', 'sigmaT2': 164.96, 'compLimits': {'a': inf, 'c': False, 's': False}, 'copyFrom': 'H-Beta_Blue'}),
        #('H-Gamma', {'Colour': 'c', 'Order': 28, 'Filter': 'blue', 'minI': 600, 'maxI': 1100, 'restWavelength': 4340.47, 'ampList': [0.0529313, 0.2030545, 0.070263], 'zone': 'low', 'sigmaT2': 164.96, 'compLimits': {'c':False, 's': False, 'a': np.inf}, 'copyFrom': 'H-Beta'}),
        #('H-Delta', {'Colour': 'c', 'Order': 23, 'Filter': 'blue', 'minI': 1450, 'maxI': 1950, 'restWavelength': 4101.74, 'ampList': [0.0529313, 0.2030545, 0.070263], 'zone': 'low', 'sigmaT2': 164.96, 'compLimits': {'c': False, 's': False, 'a': [inf, inf, 0.001]}, 'copyFrom': 'H-Gamma'}),
        #('NII-6584A', {'Colour': 'violet', 'Order': 21, 'Filter': 'red', 'minI': 1650, 'maxI': 2100, 'restWavelength': 6583.41, 'ampList': [0.2009536, 0.802822, 0.2450041], 'zone': 'low', 'sigmaT2': 11.87, 'compLimits': {'c': np.inf, 's': np.inf, 'a': np.inf}, 'copyFrom': None}),
        #('NII-6548A', {'Colour': 'violet', 'Order': 21, 'Filter': 'red', 'minI': 900, 'maxI': 1210, 'restWavelength': 6548.03, 'ampList': [0.0599905, 0.2410469, 0.0819148], 'zone': 'low', 'sigmaT2': 11.87, 'compLimits': {'c': np.inf, 's': np.inf, 'a': np.inf}, 'copyFrom': 'NII-6584A'}),
        #('SII-6717A', {'Colour': 'r', 'Order': 22, 'Filter': 'red', 'minI': 1700, 'maxI': 2006, 'restWavelength': 6716.47, 'ampList': [0.0507236, 0.2176797, 0.121686], 'zone': 'low', 'sigmaT2': 5.19, 'compLimits': {'c': np.inf, 's': np.inf, 'a': np.inf}, 'copyFrom': None}),
        # ('SII-6731A', {'Colour': '#58D68D', 'Order': 22, 'Filter': 'red', 'minI': 2068, 'maxI': 2273, 'restWavelength': 6730.85, 'ampList': [1.3593845, 5.9234259, 7.3026765], 'zone': 'low', 'sigmaT2': 5.19, 'compLimits': {'c': np.inf, 's': np.inf, 'a': np.inf}, 'copyFrom': 'SII-6717A'}),
        #('HeI-5876A', {'Colour': '#641E16', 'Order': 15, 'Filter': 'red', 'minI': 1350, 'maxI': 1650, 'restWavelength': 5875.64, 'ampList': [0.4850817, 0.1915922, 4.6927829], 'zone': 'low', 'sigmaT2': 41.54, 'compLimits': {'c': np.inf, 's': np.inf, 'a': np.inf}, 'copyFrom': None}),
        #('OII-3729A', {'Colour': '#5D6D7E', 'Order': 14, 'Filter': 'blue', 'minI': 2720, 'maxI': 3000, 'restWavelength': 3728.82, 'ampList': [5.0112717, -22679.7862692, -5.7298895], 'zone': 'low', 'sigmaT2': 10.39, 'compLimits': {'c': np.inf, 's': np.inf, 'a': np.inf}, 'copyFrom': None}),
        #('OII-3726A', {'Colour': '#EC7063', 'Order': 14, 'Filter': 'blue', 'minI': 2400, 'maxI': 2720, 'restWavelength': 3726.03, 'ampList': [-77.5325889, 42081.6972815, -36.5274502], 'zone': 'low', 'sigmaT2': 10.39, 'compLimits': {'c': np.inf, 's': np.inf, 'a': np.inf}, 'copyFrom': 'OII-3729A'}),
        #V('OII-7319A', {'Colour': '#F8C471', 'Order': 26, 'Filter': 'red', 'minI': 2264, 'maxI': 2321, 'restWavelength': 7318.39, 'ampList': [133570.7269853, -58921.5577832, 50738.7676701], 'zone': 'low', 'sigmaT2': 10.39, 'compLimits': {'c': np.inf, 's': np.inf, 'a': np.inf}, 'copyFrom': 'H-Alpha'}),
        #V('OII-7330A', {'Colour': '#7FB3D5', 'Order': 26, 'Filter': 'red', 'minI': 2444, 'maxI': 2513, 'restWavelength': 7329.66, 'ampList': [-23.2055153, 18.8989013, -7.1261496], 'zone': 'low', 'sigmaT2': 10.39, 'compLimits': {'c': np.inf, 's': np.inf, 'a': np.inf}, 'copyFrom': 'H-Alpha'}),
        #NO('OII-7331A', {'Colour': '#7FB3D5', 'Order': 26, 'Filter': 'red', 'minI': 2444, 'maxI': 2513, 'restWavelength': 7330.73, 'ampList': [-23.2055153, 18.8989013, -7.1261496], 'zone': 'low', 'sigmaT2': 10.39, 'compLimits': {'c': np.inf, 's': np.inf, 'a': np.inf}, 'copyFrom': 'H-Alpha'}),
        #('NII-5755A', {'Colour': '#7D6608', 'Order': 14, 'Filter': 'red', 'minI': 933, 'maxI': 1133, 'restWavelength': 5754.64, 'ampList': [0.2383146, -0.0193955, 1.3228768], 'zone': 'low', 'sigmaT2': 11.87, 'compLimits': {'c': np.inf, 's': np.inf, 'a': np.inf}, 'copyFrom': 'H-Alpha'}),
        #('NII-5755A', {'Colour': '#7D6608', 'Order': 13, 'Filter': 'red', 'minI': 3369, 'maxI': 3600, 'restWavelength': 5754.64, 'ampList': [0.2383146, -0.0193955, 1.3228768], 'zone': 'low', 'sigmaT2': 11.87, 'compLimits': {'c': np.inf, 's': np.inf, 'a': np.inf}, 'copyFrom': 'H-Alpha'}),
        #('OI-6300A', {'Colour': '#D35400', 'Order': 19, 'Filter': 'red', 'minI': 960, 'maxI': 1180, 'restWavelength': 6300.3, 'ampList': [0.2383146, -0.0193955, 1.3228768], 'zone': 'low', 'sigmaT2': 10.39, 'compLimits': {'c': np.inf, 's': np.inf, 'a': np.inf}, 'copyFrom': 'H-Alpha'}),
        #('SIII-6312A', {'Colour': '#7D6608', 'Order': 19, 'Filter': 'red', 'minI': 1226, 'maxI': 1425, 'restWavelength': 6310.20, 'ampList': [-287.7876259, 376.2168992, 82.087405], 'zone': 'low', 'sigmaT2': 5.19, 'compLimits': {'c': np.inf, 's': np.inf, 'a': np.inf}, 'copyFrom': 'H-Alpha'}),
        #('SIII-9069A', {'Colour': '#27AE60', 'Order': 35, 'Filter': 'red', 'minI': 1720, 'maxI': 1870, 'restWavelength': 9068.9, 'ampList': [3.8421937, -32687.0427018, 14.1817539], 'zone': 'low', 'sigmaT2': 5.19, 'compLimits': {'c': np.inf, 's': np.inf, 'a': np.inf}, 'copyFrom': 'H-Alpha'}),
        #NO('ArIII-7136A', {'Colour': '#0E6655', 'Order': 25, 'Filter': 'red', 'minI': 1713, 'maxI': 1790, 'restWavelength': 7135.78, 'ampList': [34222774.7678904, 43.1422347, -13.5573009], 'zone': 'low', 'sigmaT2': 4.16, 'compLimits': {'c': np.inf, 's': np.inf, 'a': np.inf}, 'copyFrom': 'H-Alpha'}),
        #NO('HeIH8-3889A', {'Colour': '#5B2C6F', 'Order': 18, 'Filter': 'blue', 'minI': 2250, 'maxI': 2750, 'restWavelength': 3888.65, 'ampList': [-1.3803811, 8.6389436, 5.0423933], 'zone': 'low', 'sigmaT2': 41.54, 'compLimits': {'c': np.inf, 's': np.inf, 'a': np.inf}, 'copyFrom': 'H-Alpha'}),
        #NO('HeI-4471A', {'Colour': '#78281F', 'Order': 30, 'Filter': 'blue', 'minI': 1750, 'maxI': 1900, 'restWavelength': 4471.48, 'ampList': [14.2789684, 4.0344708, -0.4933927], 'zone': 'low', 'sigmaT2': 41.54, 'compLimits': {'c': np.inf, 's': np.inf, 'a': np.inf}, 'copyFrom': 'HeI-5876A'}),
        #('HeI-6678A', {'Colour': '#D5D8DC', 'Order': 22, 'Filter': 'red', 'minI': 955, 'maxI': 1200, 'restWavelength': 6678.15, 'ampList': [0.2025295, 0.4079972, 0.8613764], 'zone': 'low', 'sigmaT2': 41.54, 'compLimits': {'c': np.inf, 's': np.inf, 'a': np.inf}, 'copyFrom': 'HeI-5876A'}),
        #NOsky('HeI-7065A', {'Colour': '#E8DAEF', 'Order': 24, 'Filter': 'red', 'minI': 3150, 'maxI': 3450, 'restWavelength': 7065.19, 'ampList': [0.186136, 1.4569275, 0.1330531], 'zone': 'low', 'sigmaT2': 41.54, 'compLimits': {'c': np.inf, 's': np.inf, 'a': np.inf}, 'copyFrom': 'HeI-5876A'}),
        #NO('HeI-7281A', {'Colour': '#E8DAEF', 'Order': 26, 'Filter': 'red', 'minI': 1465, 'maxI': 1600, 'restWavelength': 7281.35, 'ampList': [0.1519096, 1.1724037, -0.5370049], 'zone': 'low', 'sigmaT2': 41.54, 'compLimits': {'c': np.inf, 's': np.inf, 'a': np.inf}, 'copyFrom': 'HeI-5876A'}),
        #('NeIII-3868A', {'Colour': 'r', 'Order': 18, 'Filter': 'blue', 'minI': 1250, 'maxI': 1700, 'restWavelength': 3868.75, 'ampList': [3.5213033, 2.0376126, -0.8161938], 'zone': 'high', 'sigmaT2': 8.24, 'compLimits': {'c': np.inf, 's': np.inf, 'a': np.inf}, 'copyFrom': 'OIII-5007A'}),
        ##NO('NeIII-3970A', {'Colour': 'c', 'Order': 20, 'Filter': 'blue', 'minI': 2110, 'maxI': 2290, 'restWavelength': 3970.07, 'ampList': [15340.9535303, -86633.7394279, -71288.2036669], 'zone': 'high', 'sigmaT2': 8.24, 'compLimits': {'c': np.inf, 's': np.inf, 'a': np.inf}, 'copyFrom': 'OIII-5007A'}),
        #('NeIII-3967A', {'Colour': 'm', 'Order': 20, 'Filter': 'blue', 'minI': 2000, 'maxI': 2250, 'restWavelength': 3967.46, 'ampList': [2312.1030516, -33720.7186745, 30544.3475245], 'zone': 'high', 'sigmaT2': 8.24, 'compLimits': {'c': np.inf, 's': np.inf, 'a': np.inf}, 'copyFrom': 'OIII-5007A'}),
    ])

    # Information for the center, sigma and linear for the low (H-alpha) and high (OIII) zones
    centerList = {'low': [6166.71813, 6185.74770, 6181.76075], 'high': [6166.62035, 6185.57998, 6182.25494]}
    sigmaList = {'low': [17.1698066, 47.3986436, 114.509244], 'high': [16.5832838, 41.5415825, 83.1871940]}
    linSlope = {'low': -9.3542e-08, 'high': 1.6230e-08}
    linInt = {'low': 0.00162017, 'high': 0.00108596}

    numComps = {'low': 3, 'high': 3}
    componentLabels = ['Narrow 1', 'Narrow 2', 'Broad', 'Label4', 'Label5']
    componentColours = ['b', 'r', 'g', 'c', 'm']
    plottingXRange = [5800, 6500]  # velocities
    sigmaInstrBlue = 5.1
    sigmaInstrRed = 5.7
    distance = 2.68e26  # Distance to region in centimetres (same units as flux)

    emLinesForAvgVelCalc = ['H-Alpha', 'H-Beta', 'OIII-5007A', 'NII-6584A', 'SII-6717A']


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
