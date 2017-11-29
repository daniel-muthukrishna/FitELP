from collections import OrderedDict
import numpy as np

inf = np.inf


class RegionParameters(object):
    regionName = "Obj1" #SDSS J232539.22+004507.2 (=J2325), z = 0.277), vel sistem=83310km/s

    blueSpecFile = 'obj1b_fcal_SPEC1.fits'
    redSpecFile = 'obj1r_fcal_SPEC1.fits'
    blueSpecError = 'obj1b_fcal_VAR4.fits'
    redSpecError = 'obj1r_fcal_SPEC1.fits'
    scaleFlux = 1e15                               # 1

    # SPECTRAL LINE INFO FOR ALL EMISSION LINES
    emProfiles = OrderedDict([
        ('H-Alpha', {'Colour': 'y', 'Order': 1, 'Filter': 'red', 'minI': 840, 'maxI': 960, 'restWavelength': 6562.82, 'ampList': [0.0029185695, 0.0172351619, 0.0128834810], 'zone': 'low', 'sigmaT2': 164.96, 'compLimits': {'a': inf, 'c': inf, 's': inf}, 'numComps': 3, 'copyFrom': None}),
        ('NII-6584A', {'Colour': 'violet', 'Order': 1, 'Filter': 'red', 'minI': 967, 'maxI': 1055, 'restWavelength': 6583.41, 'ampList': [0.0325443, 0.0430167, 0.0249222], 'zone': 'low', 'sigmaT2': 11.87, 'compLimits': {'a': inf, 'c': False, 's': False}, 'numComps': 3, 'copyFrom': 'H-Alpha'}),
        ('NII-6548A', {'Colour': 'm', 'Order': 1, 'Filter': 'red', 'minI': 790, 'maxI': 839, 'restWavelength': 6548.03, 'ampList': 0.339, 'zone': 'low', 'sigmaT2': 11.87, 'compLimits': {'a': False, 'c': False, 's': False}, 'numComps': 3, 'copyFrom': 'NII-6584A'}),
        ('NII-6548A+H-Alpha+NII-6584A', {'Lines': ['H-Alpha', 'NII-6584A', 'NII-6548A'], 'Order': 1, 'Filter': 'red', 'minI': 760, 'maxI': 1100, 'zone': 'low', 'numComps': 3, 'restWavelength': 6562.82}),
        ('OIII-5007A', {'Colour': 'c', 'Order': 1, 'Filter': 'blue', 'minI': 2200, 'maxI': 2700, 'restWavelength': 5006.84, 'ampList': [2.4103179, 0.3954945, 0.986373], 'zone': 'high', 'sigmaT2': 10.39,  'compLimits': {'a': inf, 'c': inf, 's': inf}, 'copyFrom': None}),
        #OIII-4959A_Red:
        ('OIII-4959A', {'Colour': 'g', 'Order': 1, 'Filter': 'blue', 'minI': 1600, 'maxI': 2020, 'restWavelength': 4958.91, 'ampList': [0.7744249, 0.1533179, 0.4454696], 'zone': 'high', 'sigmaT2': 10.39, 'compLimits': {'a': inf, 'c': False, 's': 0.01}, 'copyFrom': 'OIII-5007A'}),
        #('OIII-4959A_Blue', {'Colour': '#78281F', 'Order': 37, 'Filter': 'blue', 'minI': 1600, 'maxI': 2250, 'restWavelength': 4958.91, 'ampList': 3, 'zone': 'high', 'sigmaT2': 10.39, 'compLimits': {'a': inf, 'c': False, 's': False}, 'copyFrom': 'OIII-4959A_Red'}),
        #H-Beta_Blue:
        ('H-Beta', {'Colour': 'b', 'Order': 1, 'Filter': 'blue', 'minI': 300, 'maxI': 600, 'restWavelength': 4861.33, 'ampList': [2.4103179, 0.3954945, 0.986373], 'zone': 'high', 'sigmaT2': 164.96, 'compLimits': {'a': inf, 'c': 0.01, 's': 0.01}, 'copyFrom': None}),
        #('H-Beta_Red', {'Colour': 'r', 'Order': 2, 'Filter': 'red', 'minI': 2004, 'maxI': 3000, 'restWavelength': 4861.33, 'ampList': [9.9122054, 6.5330892, 6.8177404], 'zone': 'low', 'sigmaT2': 164.96, 'compLimits': {'a': inf, 'c': False, 's': False}, 'copyFrom': 'H-Beta_Blue'}),
        # ('H-Gamma', {'Colour': 'r', 'Order': 28, 'Filter': 'blue', 'minI': 700, 'maxI': 1200, 'restWavelength': 4340.47, 'ampList': [4.985869, 3.5976242, 4.4060826], 'zone': 'low', 'sigmaT2': 164.96, 'compLimits': {'a': inf, 'c': 0.001, 's': [inf, inf, False]}, 'copyFrom': 'H-Beta_Blue'}),
        # ('H-Delta', {'Colour': 'c', 'Order': 23, 'Filter': 'blue', 'minI': 1400, 'maxI': 2000, 'restWavelength': 4101.74, 'ampList': [2.9131725, 2.0446065, 2.5207195], 'zone': 'low', 'sigmaT2': 164.96, 'compLimits': {'a': inf, 'c': 0.001, 's': 1}, 'copyFrom': 'H-Beta_Blue'}),
        #('NII-6584A', {'Colour': 'violet', 'Order': 1, 'Filter': 'red', 'minI': 967, 'maxI': 1055, 'restWavelength': 6583.41, 'ampList': [0.0325443, 0.0430167, 0.0249222], 'zone': 'low', 'sigmaT2': 11.87, 'compLimits': {'a': False, 'c': 0.01, 's': 0.01}, 'copyFrom': 'H-Alpha'}),
        ('SII-6717A', {'Colour': 'r', 'Order': 1, 'Filter': 'red', 'minI': 1650, 'maxI': 1760, 'restWavelength': 6716.47, 'ampList': [0.0293627, 0.1365011, 0.1315035], 'zone': 'low', 'sigmaT2': 5.19, 'compLimits': {'a': 0.001, 'c': False, 's': 0.01}, 'copyFrom': 'H-Alpha'}),
        #('SII-6731A', {'Colour': '#58D68D', 'Order': 1, 'Filter': 'red', 'minI': 1745, 'maxI': 1821, 'restWavelength': 6730.85, 'ampList': [0.7744249, 0.1533179, 0.4454696], 'zone': 'low', 'sigmaT2': 5.19,'compLimits': {'a': inf, 'c': 0.01, 's': 0.01}, 'copyFrom': 'SII-6717A'}),
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
    centerList = {'low': [82960.6915, 82960.0779, 82943.8265], 'high': [83027.8400, 83025.0079, 83000.3505]}
    #centerList = {'low': [350, 349.9221, 366.1735], 'high': [283, 284.9921, 309.6495]}
    sigmaList = {'low': [20.1, 70.8, 184.0], 'high': [22.0881779, 72.8603209, 190.948440]}
    linSlope = {'low': 4.6406e-08, 'high': 8.1196e-08}
    linInt = {'low': -0.0097977, 'high': -0.00651050}

    numComps = {'low': 3, 'high': 3}
    componentLabels = ['Narrow 1', 'Narrow 2', 'Broad']
    componentColours = ['b', 'r', 'g', 'c', 'm']
    sigmaInstrBlue = 10.2
    sigmaInstrRed = 10.2
    distance = 1.63e26  # Distance to region in centimetres (same units as flux)

    showSystemicVelocity = True  # Assumed False if not defined
    systemicVelocity = 83310  # Required only if showSystemicVelocity is True
    # plottingXRange = [82200, 83800]  # xrange of velocities or delta velocities

    emLinesForAvgVelCalc = ['H-Beta', 'OIII-5007A', 'H-Alpha', 'NII-6584A', 'SII-6717A']


""" NOTES ON HOW TO USE THE ABOVE TABLE
The limits in 'compLimits' can be in the following forms:
    - a list indicating the limits for each component
    - a single number indicating the percentage limits for ALL components
    - a tuple (minValue, maxValue) indicating the min and max not in a percentage
    - inf: indicating that the component can vary
    - False: indicating that the value is fixed

ampList
    - if not list it will take the copyFrom amplitude List and divide by the ampList scalar

numComps:
    - If numComps is not listed in the emProfile dictionary, then the number of components will be taken from the
    numComps variable depending on the zone set in the emProfile dictionary
"""
