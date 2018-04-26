from collections import OrderedDict
import numpy as np
inf = np.inf


class RegionParameters(object):
    regionName = "HCG31-AC"

    blueSpecFile = 'HCG31-AC_B.fc.fits'
    redSpecFile = 'HCG31-AC_R.fc.fits'
    blueSpecError = 'HCG31-AC_B_ErrorFlux.fc.fits'
    redSpecError = 'HCG31-AC_R_ErrorFlux.fc.fits'
    scaleFlux = 1e14                               # 1

    # SPECTRAL LINE INFO FOR ALL EMISSION LINES
    emProfiles = OrderedDict([
        ('H-Alpha', {'Colour': 'y', 'Order': 20, 'Filter': 'red', 'minI': 2931, 'maxI': 3360, 'restWavelength': 6562.82, 'ampList': [1.1046484, 1.7833584, 12.3510137, 6.3829617], 'zone': 'low', 'sigmaT2': 164.96,'compLimits': {'a': inf, 'c': inf, 's': inf}, 'copyFrom': None}),
        ('OIII-5007A', {'Colour': 'c', 'Order': 4, 'Filter': 'red', 'minI': 2300, 'maxI': 3440, 'restWavelength': 5006.84,'ampList': [0.8782459, 1.5048018, 11.6733837, 6.0130845], 'zone': 'high', 'sigmaT2': 10.39,'compLimits': {'a': inf, 'c': inf, 's': inf}, 'copyFrom': None}),
        # OIII-4959A_Red:
         ('OIII-4959A', {'Colour': 'g', 'Order': 4, 'Filter': 'red', 'minI': 1080, 'maxI': 2000, 'restWavelength': 4958.91, 'ampList': [0.3177392, 0.4852143, 3.8463164, 1.9312422], 'zone': 'high', 'sigmaT2': 10.39, 'compLimits': {'a': inf, 'c': False, 's': False}, 'copyFrom': 'OIII-5007A'}),
        # ('OIII-4959A_Blue', {'Colour': '#78281F', 'Order': 37, 'Filter': 'blue', 'minI': 1600, 'maxI': 2250, 'restWavelength': 4958.91, 'ampList': 3, 'zone': 'high', 'sigmaT2': 10.39, 'compLimits': {'a': inf, 'c': False, 's': False}, 'copyFrom': 'OIII-4959A_Red'}),
        # H-Beta_Blue:
        ('H-Beta', {'Colour': 'b', 'Order': 36, 'Filter': 'blue', 'minI': 370, 'maxI': 1613, 'restWavelength': 4861.33,'ampList': [0.2488174, 0.4748407, 3.7794498, 2.0702787], 'zone': 'low', 'sigmaT2': 164.96,'compLimits': {'a': inf, 'c': 0.1, 's': 0.1}, 'copyFrom':'H-Alpha'}),
        # H-Beta_Red: no da bien la Narrow 1
        # ('H-Beta_Red', {'Colour': 'r', 'Order': 2, 'Filter': 'red', 'minI': 2250, 'maxI': 3300, 'restWavelength': 4861.33, 'ampList': [0.0560847, 3.3116124, 0.5651499, 2.3527601], 'zone': 'low', 'sigmaT2': 164.96, 'compLimits': {'a': inf, 'c': 0.001, 's': 0.001}, 'copyFrom': 'H-Beta_Blue'}),
        ('H-Gamma', {'Colour': 'r', 'Order': 27, 'Filter': 'blue', 'minI': 1400, 'maxI': 2350, 'restWavelength': 4340.47, 'ampList': [0.1540919, 0.2417972, 1.7440522, 0.6647593], 'zone': 'low', 'sigmaT2': 164.96,'compLimits': {'a': inf, 'c': False, 's': False}, 'copyFrom': 'H-Beta'}),
        ('H-Delta',{'Colour': 'c', 'Order': 22, 'Filter': 'blue', 'minI': 2055, 'maxI': 3000, 'restWavelength': 4101.74, 'ampList': [0.0833496, 0.1263432, 0.9708821, 0.2602185], 'zone': 'low', 'sigmaT2': 164.96, 'compLimits': {'a': inf, 'c': False, 's': False}, 'copyFrom': 'H-Beta'}),
        ('NII-6584A', {'Colour': 'violet', 'Order': 20, 'Filter': 'red', 'minI': 3361, 'maxI': 3885, 'restWavelength': 6583.41, 'ampList': [0.0983902, 0.2332231, 0.9984201, 0.6106288], 'zone': 'low', 'sigmaT2': 11.87, 'compLimits': {'a': inf, 'c': 0.1, 's': 0.1}, 'copyFrom': 'H-Alpha'}),
        ('NII-6548A', {'Colour': 'violet', 'Order': 20, 'Filter': 'red', 'minI': 2563, 'maxI': 2930, 'restWavelength': 6548.03, 'ampList': [0.0394559, 0.0798065, 0.3313166, 0.1667593], 'zone': 'low', 'sigmaT2': 11.87, 'compLimits': {'a': inf, 'c': False, 's': False}, 'copyFrom': 'NII-6584A'}),
        ('SII-6717A', {'Colour': 'r', 'Order': 22, 'Filter': 'red', 'minI': 508, 'maxI': 985, 'restWavelength': 6716.47, 'ampList': [0.0644916, 0.1415714, 0.605027, 0.6710964], 'zone': 'low', 'sigmaT2': 5.19, 'compLimits': {'a': inf, 'c': 1, 's': 1}, 'copyFrom': 'H-Alpha'}),
        ('SII-6731A', {'Colour': '#58D68D', 'Order': 22, 'Filter': 'red', 'minI': 986, 'maxI': 1290, 'restWavelength': 6730.85, 'ampList': [0.0562764, 0.1017221, 0.4416212, 0.4717391], 'zone': 'low', 'sigmaT2': 5.19,'compLimits': {'a': inf, 'c': 1, 's': 1}, 'copyFrom': 'SII-6717A'}),
        # ('OII-3729A', {'Colour': '#5D6D7E', 'Order': 14, 'Filter': 'blue', 'minI': 2800, 'maxI': 3040, 'restWavelength': 3728.82, 'ampList': [15.5492234, 10.9045454, 11.3158249], 'zone': 'low', 'sigmaT2': 10.39, 'compLimits': {'a': False, 'c': 0.0005, 's': inf}, 'copyFrom': 'NII-6584A'}),
        # ('OII-3726A', {'Colour': '#EC7063', 'Order': 14, 'Filter': 'blue', 'minI': 2600, 'maxI': 2829, 'restWavelength': 3726.03, 'ampList': [9.6560836, 9.7755656, 6.3738786], 'zone': 'low', 'sigmaT2': 10.39, 'compLimits': {'a': inf, 'c': 0.0005, 's': False}, 'copyFrom': 'OII-3729A'}),
        # ('HeI-5876A', {'Colour': '#641E16', 'Order': 15, 'Filter': 'red', 'minI': 1320, 'maxI': 1700, 'restWavelength': 5875.64, 'ampList': [0.9957378, 0.6740472, 0.8351281], 'zone': 'high', 'sigmaT2': 41.54, 'compLimits': {'a': inf, 'c': 0.001, 's': [inf, inf, False]}, 'copyFrom': 'OIII-5007A'}),
        # ('HeI-4471A', {'Colour': '#78281F', 'Order': 30, 'Filter': 'blue', 'minI': 1750, 'maxI': 1900, 'restWavelength': 4471.48, 'ampList': [0.46284, 0.2947801, 0.0391113], 'zone': 'high', 'sigmaT2': 41.54, 'compLimits': {'a': inf, 'c': 0.001, 's': False}, 'copyFrom': 'HeI-5876A'}),
        # ('HeI-6678A', {'Colour': '#D5D8DC', 'Order': 22, 'Filter': 'red', 'minI': 1050, 'maxI': 1240, 'restWavelength': 6678.15, 'ampList': [0.2301685, 0.2810127, 0.0476801], 'zone': 'high', 'sigmaT2': 41.54, 'compLimits': {'a': inf, 'c': 0.001, 's': False}, 'copyFrom': 'HeI-5876A'}),
        # ('HeI-7065A', {'Colour': '#E8DAEF', 'Order': 24, 'Filter': 'red', 'minI': 3150, 'maxI': 3450, 'restWavelength': 7065.19, 'ampList': [0.1437774, 0.1282405, 0.0734699], 'zone': 'high', 'sigmaT2': 41.54, 'compLimits': {'a': inf, 'c': False, 's': False}, 'copyFrom': 'HeI-5876A'}),
        # ('NeIII-3868A', {'Colour': 'r', 'Order': 18, 'Filter': 'blue', 'minI': 1430, 'maxI': 1650, 'restWavelength': 3868.75, 'ampList': [2.4413131, 1.7799793, 2.1882557], 'zone': 'high', 'sigmaT2': 8.24, 'compLimits': {'a': inf, 'c': False, 's': False}, 'copyFrom': 'OIII-5007A'}),
        # ('NeIII-3970A', {'Colour': 'c', 'Order': 20, 'Filter': 'blue', 'minI': 2110, 'maxI': 2290, 'restWavelength': 3970.07, 'ampList': [1.2004104, 1.238606, 1.6775648], 'zone': 'high', 'sigmaT2': 8.24, 'compLimits': {'a': inf, 'c': False, 's': False}, 'copyFrom': 'OIII-5007A'}),
        # ('OI-6300A', {'Colour': '#D35400', 'Order': 19, 'Filter': 'red', 'minI': 1050, 'maxI': 1250, 'restWavelength': 6300.3, 'ampList': [0.3964594, 0.4723308, 0.0564203], 'zone': 'low', 'sigmaT2': 10.39, 'compLimits': {'a': inf, 'c': False, 's': False}, 'copyFrom': 'H-Beta_Blue'}),
        # ('SIII-9069A', {'Colour': '#27AE60', 'Order': 35, 'Filter': 'red', 'minI': 1720, 'maxI': 1870, 'restWavelength': 9068.9, 'ampList': [1.3819041, 0.9362417, 0.7920365], 'zone': 'low', 'sigmaT2': 5.19, 'compLimits': {'a': inf, 'c': 0.001, 's': 1}, 'copyFrom': 'H-Alpha'}),
        ##('NeIII-3967A', {'Colour': 'm', 'Order': 20, 'Filter': 'blue', 'minI': 1950, 'maxI': 2135, 'restWavelength': 3967.46, 'ampList': [0.4933746, 0.2356542, 2.1809342], 'zone': 'high', 'sigmaT2': 8.24, 'compLimits': {'a': inf, 'c': False, 's': False}, 'copyFrom': 'NeIII-3970A'}),
        ##('HeIH8-3889A', {'Colour': '#5B2C6F', 'Order': 18, 'Filter': 'blue', 'minI': 2450, 'maxI': 2750, 'restWavelength': 3888.65, 'ampList': [0.0491376, 2.1000132, 4.4749628], 'zone': 'high', 'sigmaT2': 41.54, 'compLimits': {'a': inf, 'c': False, 's': False}, 'copyFrom': 'HeI-5876A'}),
        ###('OII-7319A', {'Colour': '#F8C471', 'Order': 26, 'Filter': 'red', 'minI': 2252, 'maxI': 2330, 'restWavelength': 7318.39, 'ampList': [-1.0126892, -0.0315027, 3.5482043], 'zone': 'low', 'sigmaT2': 10.39, 'compLimits': {'a': inf, 'c': inf, 's': inf}, 'copyFrom': 'H-Alpha'}),
        ###('OII-7330A', {'Colour': '#7FB3D5', 'Order': 26, 'Filter': 'red', 'minI': 2420, 'maxI': 2520, 'restWavelength': 7330.0, 'ampList': [-1.0488879, -0.5248179, 8.5911851], 'zone': 'low', 'sigmaT2': 10.39, 'compLimits': {'a': inf, 'c': inf, 's': inf}, 'copyFrom': 'H-Alpha'}),
        ###('ArIII-7136A', {'Colour': '#0E6655', 'Order': 25, 'Filter': 'red', 'minI': 1713, 'maxI': 1790, 'restWavelength': 7135.78, 'ampList': [0.4554454, -0.2274418, 1.066718], 'zone': 'low', 'sigmaT2': 4.16, 'compLimits': {'c': np.inf, 's': np.inf, 'a': np.inf}, 'copyFrom': 'H-Alpha'}),
        ###('OI-6364A', {'Colour': '#7D6608', 'Order': 19, 'Filter': 'red', 'minI': 2500, 'maxI': 2620, 'restWavelength': 6363.78, 'ampList': [2.0802379, -308.5885481, -32.2254134], 'zone': 'low', 'sigmaT2': 10.39, 'compLimits': {'c': np.inf, 's': np.inf, 'a': np.inf}, 'copyFrom': 'H-Alpha'}),
        ###('HeI-7281A', {'Colour': '#E8DAEF', 'Order': 26, 'Filter': 'red', 'minI': 1465, 'maxI': 1600, 'restWavelength': 7281.35, 'ampList': [0.6740428, 0.8351308, 0.9957380], 'zone': 'low', 'sigmaT2': 41.54, 'compLimits': {'c': np.inf, 's': np.inf, 'a': np.inf}, 'copyFrom': 'H-Alpha'}),
    ])

    # Information for the center, sigma and linear for the low (H-alpha) and high (OIII) zones
    centerList = {'low': [3909.90983, 3962.62266, 4001.71844, 3988.40713], 'high': [3910.67030, 3966.47756, 4000.24559, 3995.04269]}
    sigmaList = {'low': [23.8772895, 15.6120818, 40.2420043, 98.1856858], 'high': [20.1094056, 12.7580492, 39.1248199, 100.523249]}
    linSlope = {'low': -3.0665e-07, 'high': -3.1810e-07}
    linInt = {'low': 0.00273304, 'high': 0.00286121}

    numComps = {'low': 4, 'high': 4}
    componentLabels = ['Narrow 1', 'Narrow 2', 'Narrow 3', 'Broad', 'Label5']
    componentColours = ['b', 'r', 'c', 'g','m']
    plottingXRange = [3600, 4400]  # velocities
    sigmaInstrBlue = 5.2
    sigmaInstrRed = 5.9
    distance = 1.67e26  # Distance to region in centimetres (same units as flux)

    emLinesForAvgVelCalc = ['H-Alpha']#, 'H-Beta_Blue', 'OIII-5007A', 'NII-6584A', 'SII-6717A']


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