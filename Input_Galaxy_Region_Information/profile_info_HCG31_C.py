from collections import OrderedDict
import numpy as np
inf = np.inf


class RegionParameters(object):
    regionName = "HCG31-C"

    blueSpecFile = 'HCG31-C_B.fc.fits'
    redSpecFile = 'HCG31-C_R.fc.fits'
    blueSpecError = 'HCG31-C_B_ErrorFlux.fc.fits'
    redSpecError = 'HCG31-AC_R_ErrorFlux.fc.fits'  #
    scaleFlux = 1e14                               #

    # SPECTRAL LINE INFO FOR ALL EMISSION LINES
    emProfiles = OrderedDict([
        #4comp
        # ('H-Alpha', {'Colour': 'y', 'Order': 20, 'Filter': 'red', 'minI': 2931, 'maxI': 3360, 'restWavelength': 6562.82, 'ampList': [1.1393854, 0.9004322, 11.5124311, 4.8228556], 'zone': 'low', 'sigmaT2': 164.96, 'compLimits': {'a': inf, 'c': inf, 's': inf}, 'copyFrom': None}),
        # ('OIII-5007A', {'Colour': 'c', 'Order': 4, 'Filter': 'red', 'minI': 2300, 'maxI': 3440, 'restWavelength': 5006.84, 'ampList': [1.1548058, 1.3258621, 8.5919068, 4.2634018], 'zone': 'high', 'sigmaT2': 10.39, 'compLimits': {'a': inf, 'c': inf, 's': inf}, 'copyFrom': None}),
        # ('OIII-4959A', {'Colour': 'g', 'Order': 4, 'Filter': 'red', 'minI': 1080, 'maxI': 2000, 'restWavelength': 4958.91, 'ampList': [0.3902536, 0.4329626, 2.7844993, 1.3837819], 'zone': 'high', 'sigmaT2': 10.39, 'compLimits': {'a': inf, 'c': False, 's': False}, 'copyFrom': 'OIII-5007A'}),
        # ('H-Beta', {'Colour': 'b', 'Order': 36, 'Filter': 'blue', 'minI': 370, 'maxI': 1613, 'restWavelength': 4861.33, 'ampList': [0.3251339, 0.3796096, 3.0043634, 1.4684201], 'zone': 'low', 'sigmaT2': 164.96, 'compLimits': {'a': inf, 'c': 0.1, 's': 0.1}, 'copyFrom': 'H-Alpha'}),
        # ('H-Gamma', {'Colour': 'r', 'Order': 27, 'Filter': 'blue', 'minI': 1400, 'maxI': 2350, 'restWavelength': 4340.47, 'ampList': [0.1586482, 0.1974788, 1.2364239, 0.5180314], 'zone': 'low', 'sigmaT2': 164.96, 'compLimits': {'a': inf, 'c': False, 's': False}, 'copyFrom': 'H-Beta'}),
        # ('H-Delta', {'Colour': 'c', 'Order': 22, 'Filter': 'blue', 'minI': 2055, 'maxI': 3000, 'restWavelength': 4101.74, 'ampList': [0.0779094, 0.1001482, 0.6786677, 0.2037144], 'zone': 'low', 'sigmaT2': 164.96, 'compLimits': {'a': inf, 'c': False, 's': False}, 'copyFrom': 'H-Beta'}),
        # ('NII-6584A', {'Colour': 'violet', 'Order': 20, 'Filter': 'red', 'minI': 3361, 'maxI': 3885, 'restWavelength': 6583.41, 'ampList': [0.1004451, 0.0611695, 1.0586795, 0.5316711], 'zone': 'low', 'sigmaT2': 11.87, 'compLimits': {'a': inf, 'c': 0.1, 's': 0.1}, 'copyFrom': 'H-Alpha'}),
        # ('NII-6548A', {'Colour': 'violet', 'Order': 20, 'Filter': 'red', 'minI': 2563, 'maxI': 2930, 'restWavelength': 6548.03, 'ampList': [0.0324588, 0.0176375, 0.3615958, 0.1374342], 'zone': 'low', 'sigmaT2': 11.87, 'compLimits': {'a': inf, 'c': False, 's': False}, 'copyFrom': 'NII-6584A'}),
        # ('SII-6717A', {'Colour': 'r', 'Order': 22, 'Filter': 'red', 'minI': 508, 'maxI': 985, 'restWavelength': 6716.47, 'ampList': [0.0972848, 0.0417174, 0.7574605, 0.4679219], 'zone': 'low', 'sigmaT2': 5.19, 'compLimits': {'a': inf, 'c': 1, 's': 1}, 'copyFrom': 'H-Alpha'}),
        # ('SII-6731A', {'Colour': '#58D68D', 'Order': 22, 'Filter': 'red', 'minI': 986, 'maxI': 1290, 'restWavelength': 6730.85, 'ampList': [0.0324219, 0.0220474, 0.6733394, 0.2678776], 'zone': 'low', 'sigmaT2': 5.19, 'compLimits': {'a': inf, 'c': 1, 's': 1}, 'copyFrom': 'SII-6717A'}),
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
    #])
    # 3comp
    ('H-Alpha', {'Colour': 'y', 'Order': 20, 'Filter': 'red', 'minI': 2931, 'maxI': 3360, 'restWavelength': 6562.82, 'ampList': [1.1393854, 8.58, 4.8228556], 'zone': 'low', 'sigmaT2': 164.96, 'compLimits': {'a': inf, 'c': inf, 's': inf}, 'copyFrom': None}),
    ('OIII-5007A', {'Colour': 'c', 'Order': 4, 'Filter': 'red', 'minI': 2300, 'maxI': 3440, 'restWavelength': 5006.84, 'ampList': [1.1548058, 8.5919068, 4.2634018], 'zone': 'high', 'sigmaT2': 10.39, 'compLimits': {'a': inf, 'c': inf, 's': inf}, 'copyFrom': None}),
    ('OIII-4959A', {'Colour': 'g', 'Order': 4, 'Filter': 'red', 'minI': 1080, 'maxI': 2000, 'restWavelength': 4958.91, 'ampList': [0.3902536, 2.7844993, 1.3837819], 'zone': 'high', 'sigmaT2': 10.39, 'compLimits': {'a': inf, 'c': False, 's': False}, 'copyFrom': 'OIII-5007A'}),
    ('H-Beta', {'Colour': 'b', 'Order': 36, 'Filter': 'blue', 'minI': 370, 'maxI': 1613, 'restWavelength': 4861.33, 'ampList': [0.1402979, 3.2042614, 1.7970957], 'zone': 'low', 'sigmaT2': 164.96, 'compLimits': {'a': inf, 'c': 0.1, 's': 0.1}, 'copyFrom': 'H-Alpha'}),
    #('H-Gamma', {'Colour': 'r', 'Order': 27, 'Filter': 'blue', 'minI': 1400, 'maxI': 2350, 'restWavelength': 4340.47, 'ampList': [0.1586482, 1.2364239, 0.5180314], 'zone': 'low', 'sigmaT2': 164.96, 'compLimits': {'a': inf, 'c': False, 's': False}, 'copyFrom': 'H-Beta'}),
    #('H-Delta', {'Colour': 'c', 'Order': 22, 'Filter': 'blue', 'minI': 2055, 'maxI': 3000, 'restWavelength': 4101.74, 'ampList': [0.0779094, 0.6786677, 0.2037144], 'zone': 'low', 'sigmaT2': 164.96, 'compLimits': {'a': inf, 'c': False, 's': False}, 'copyFrom': 'H-Beta'}),
    ('NII-6584A', {'Colour': 'violet', 'Order': 20, 'Filter': 'red', 'minI': 3361, 'maxI': 3885, 'restWavelength': 6583.41, 'ampList': [0.1004451, 1.0586795, 0.5316711], 'zone': 'low', 'sigmaT2': 11.87, 'compLimits': {'a': inf, 'c': 0.1, 's': 0.1}, 'copyFrom': 'H-Alpha'}),
    ('NII-6548A', {'Colour': 'violet', 'Order': 20, 'Filter': 'red', 'minI': 2563, 'maxI': 2930, 'restWavelength': 6548.03, 'ampList': [0.0324588, 1.0586795, 0.5316711], 'zone': 'low', 'sigmaT2': 11.87, 'compLimits': {'a': inf, 'c': False, 's': False}, 'copyFrom': 'NII-6584A'}),
    ('SII-6717A', {'Colour': 'r', 'Order': 22, 'Filter': 'red', 'minI': 508, 'maxI': 985, 'restWavelength': 6716.47, 'ampList': [0.0972848, 0.7574605, 0.4679219], 'zone': 'low', 'sigmaT2': 5.19, 'compLimits': {'a': inf, 'c': 1, 's': 1}, 'copyFrom': 'H-Alpha'}),
    ('SII-6731A', {'Colour': '#58D68D', 'Order': 22, 'Filter': 'red', 'minI': 986, 'maxI': 1290, 'restWavelength': 6730.85, 'ampList': [0.0324219, 0.6733394, 0.2678776], 'zone': 'low', 'sigmaT2': 5.19, 'compLimits': {'a': inf, 'c': 1, 's': 1}, 'copyFrom': 'SII-6717A'}),
    ('H-Gamma', {'Colour': 'r', 'Order': 27, 'Filter': 'blue', 'minI': 1625, 'maxI': 2183, 'restWavelength': 4340.47, 'ampList': [0.1402979, 3.2042614, 1.7970957], 'zone': 'low', 'sigmaT2': 164.96, 'compLimits': {'a': inf, 'c': False, 's': False}, 'copyFrom': 'H-Beta'}),
    ('H-Delta', {'Colour': 'c', 'Order': 22, 'Filter': 'blue', 'minI': 2390, 'maxI': 2810, 'restWavelength': 4101.74, 'ampList': [0.1402979, 3.2042614, 1.7970957], 'zone': 'low', 'sigmaT2': 164.96, 'compLimits': {'a': inf, 'c': False, 's': False}, 'copyFrom': 'H-Beta'}),
    ('SIII-9069A', {'Colour': '#27AE60', 'Order': 35, 'Filter': 'red', 'minI': 485, 'maxI': 881, 'restWavelength': 9068.9, 'ampList': [0.0807574, 1.0986008, 0.5388915], 'zone': 'low', 'sigmaT2': 5.19, 'compLimits': {'a': inf, 'c': 0.001, 's': 0.1}, 'copyFrom': 'H-Alpha'}),
    # ('OIII-4363A', {'Colour': '#591E16', 'Order': 27, 'Filter': 'blue', 'minI': 2780, 'maxI': 3140, 'restWavelength': 4363.21, 'ampList': [0.1402979, 3.2042614, 1.7970957], 'zone': 'high', 'sigmaT2': 10.39, 'compLimits': {'a': inf, 'c': 0.001, 's': 0.001}, 'copyFrom': 'OIII-5007A'}),
    # ('NeIII-3868A', {'Colour': '#541E16', 'Order': 17, 'Filter': 'blue', 'minI': 2054, 'maxI': 2365, 'restWavelength': 3868.75, 'ampList': [0.1402979, 3.2042614, 1.7970957], 'zone': 'high', 'sigmaT2': 8.24, 'compLimits': {'a': inf, 'c': 0.001, 's': 0.001}, 'copyFrom': 'OIII-5007A'}),
    # # NeIII-3970A muy debil y pegada a HeI
    # ('NeIII-3970A', {'Colour': '#441E16', 'Order': 19, 'Filter': 'blue', 'minI': 2700, 'maxI': 2880, 'restWavelength': 3967.46, 'ampList': [0.1402979, 3.2042614, 1.7970957], 'zone': 'high', 'sigmaT2': 8.24, 'compLimits': {'a': inf, 'c': 0.001, 's': 0.001}, 'copyFrom': 'NeIII-3868A'}),
    # # ('H7', {'Colour': '#341E16', 'Order': 19, 'Filter': 'blue', 'minI': 2877, 'maxI': 3105, 'restWavelength': 3970.07, 'ampList': [4.2449498, 0.6039219,  1.5033578], 'zone': 'high', 'sigmaT2': 164.96, 'compLimits': {'a': inf, 'c': 0.001, 's': [inf, inf, False]}, 'copyFrom': 'H-Beta'}),
    # # ('HeI-4016A', {'Colour': '#241E16', 'Order': 22, 'Filter': 'blue', 'minI': 2375, 'maxI': 2783, 'restWavelength': 4023.98, 'ampList': [1.2004104, 1.238606, 1.6775648], 'zone': 'high', 'sigmaT2': 41.54, 'compLimits': {'a': inf, 'c': 0.001, 's': [inf, inf, False]}, 'copyFrom': 'OIII-5007A'}),
    # # ('NII-5755A', {'Colour': '#7D6608', 'Order': 14, 'Filter': 'red', 'minI': 2772, 'maxI': 3170, 'restWavelength': 5754.64, 'ampList': [1.9860777, 0.621677,  0.5682], 'zone': 'low', 'sigmaT2': 11.87, 'compLimits': {'c': np.inf, 's': np.inf, 'a': np.inf}, 'copyFrom': 'NII-6584A'}),
    # ('HeI-5876A', {'Colour': '#641E16', 'Order': 14, 'Filter': 'red', 'minI': 2772, 'maxI': 3170, 'restWavelength': 5875.64, 'ampList': [0.026215, 0.3960843, 0.2777223], 'zone': 'high', 'sigmaT2': 41.54, 'compLimits': {'a': inf, 'c': 0.001, 's': [inf, inf, False]}, 'copyFrom': 'OIII-5007A'}),
    # # ('HeI-4471A', {'Colour': '#78281F', 'Order': 29, 'Filter': 'blue', 'minI': 2684, 'maxI': 3042, 'restWavelength': 4471.48, 'ampList': [0.46284, 0.2947801, 0.0391113], 'zone': 'high', 'sigmaT2': 41.54, 'compLimits': {'a': inf, 'c': 0.001, 's': False}, 'copyFrom': 'HeI-5876A'}),
    # ('HeI-3887A', {'Colour': '#341E56', 'Order': 18, 'Filter': 'blue', 'minI': 866, 'maxI': 1202, 'restWavelength': 3888.65,  'ampList': [0.026215, 0.3960843, 0.2777223], 'zone': 'high', 'sigmaT2': 41.54, 'compLimits': {'a': inf, 'c': [0.1, 0.1, 1.0], 's': 0.1}, 'copyFrom': 'HeI-5876A'}),
    # ('HeI-6678A', {'Colour': '#D5D8DC', 'Order': 21, 'Filter': 'red', 'minI': 2751, 'maxI': 2936, 'restWavelength': 6678.15, 'ampList': [0.026215, 0.3960843, 0.2777223], 'zone': 'high', 'sigmaT2': 41.54, 'compLimits': {'a': inf, 'c': 0.1, 's': 0.1}, 'copyFrom': 'HeI-5876A'}),
    # ('HeI-7065A', {'Colour': '#E8DAEF', 'Order': 24, 'Filter': 'red', 'minI': 1936, 'maxI': 2520, 'restWavelength': 7065.19, 'ampList': [0.026215, 0.3960843, 0.2777223], 'zone': 'high', 'sigmaT2': 41.54,  'compLimits': {'a': inf, 'c': 0.1, 's': 0.1}, 'copyFrom': 'HeI-5876A'}),
    # ('OI-6300A', {'Colour': '#D35400', 'Order': 18, 'Filter': 'red', 'minI': 2537, 'maxI': 2813, 'restWavelength': 6300.3, 'ampList': [0.026215, 0.3960843, 0.2777223], 'zone': 'low', 'sigmaT2': 10.39, 'compLimits': {'a': inf, 'c': 0.1, 's': 0.1}, 'copyFrom': 'H-Beta'}),
    # ('OI-6354A', {'Colour': 'm', 'Order': 19, 'Filter': 'red', 'minI': 1380, 'maxI': 1600, 'restWavelength': 6363.78, 'ampList': [4.2449498, 0.6039219, 1.5033578], 'zone': 'low', 'sigmaT2': 10.39, 'compLimits': {'a': inf, 'c': False, 's': False}, 'copyFrom': 'OI-6300A'}),
    # ('ArIII-7136A', {'Colour': '#0E6655', 'Order': 25, 'Filter': 'red', 'minI': 477, 'maxI': 781, 'restWavelength': 7135.78, 'ampList': [0.1402979, 3.2042614, 1.7970957], 'zone': 'low', 'sigmaT2': 4.16, 'compLimits': {'a': inf, 'c': [0.1, 0.1, 1.0], 's': 0.1}, 'copyFrom': 'H-Alpha'}),
    # ('HeI-7281A', {'Colour': '#E8DAEF', 'Order': 26, 'Filter': 'red', 'minI': 352, 'maxI': 578, 'restWavelength': 7281.35, 'ampList': [0.605482, 0.0620069, 0.162767], 'zone': 'low', 'sigmaT2': 41.54, 'compLimits': {'c': False, 's': 0.001, 'a': inf}, 'copyFrom': 'HeI-5876A'}),
    # ('OII-3729A', {'Colour': '#5D6D7E', 'Order': 14, 'Filter': 'blue', 'minI': 1265, 'maxI': 1515, 'restWavelength': 3728.82, 'ampList': [0.1402979, 3.2042614, 1.7970957], 'zone': 'low', 'sigmaT2': 10.39, 'compLimits': {'a': [inf, inf, 0.01], 'c': False, 's': False}, 'copyFrom': 'H-Alpha'}),
    # ('OII-3726A', {'Colour': '#EC7063', 'Order': 14, 'Filter': 'blue', 'minI': 1004, 'maxI': 1265, 'restWavelength': 3726.03, 'ampList': [0.1402979, 3.2042614, 1.7970957], 'zone': 'low', 'sigmaT2': 10.39, 'compLimits': {'a': [inf, inf, 0.01], 'c': False, 's': False}, 'copyFrom': 'OII-3729A'}),
    # # OII-7319A se invierte el orden de las narrows
    # ('OII-7319A', {'Colour': '#F8C471', 'Order': 26, 'Filter': 'red', 'minI': 1036, 'maxI': 1320, 'restWavelength': 7318.39, 'ampList': [0.1402979, 3.2042614, 1.7970957], 'zone': 'low', 'sigmaT2': 10.39,  'compLimits': {'c': inf, 's': inf, 'a': np.inf}, 'copyFrom': 'OII-3729A'}),
    # # OII-7330A tiene un cr muy grande no ajusta bien la narrow 2
    # ('OII-7330A', {'Colour': '#7FB3D5', 'Order': 26, 'Filter': 'red', 'minI': 1319, 'maxI': 1530, 'restWavelength': 7329.66, 'ampList': [0.1402979, 3.2042614, 1.7970957], 'zone': 'low', 'sigmaT2': 10.39, 'compLimits': {'c': False, 's': False, 'a': np.inf}, 'copyFrom': 'OII-7319A'}),
    # # ArIII-7750A tiene un cr muy grande imposible ajustar bien
    # # ('ArIII-7750A', {'Colour': '#0E6653', 'Order': 28, 'Filter': 'red', 'minI': 2899, 'maxI': 3114, 'restWavelength': 7751.11, 'ampList': [0.1806011, 0.273026, 0.2617821], 'zone': 'low', 'sigmaT2': 4.16, 'compLimits': {'c': 0.001, 's': 0.001, 'a': inf}, 'copyFrom': 'ArIII-7136A'}),
    #('SIII-6312A', {'Colour': '#7D6608', 'Order': 18, 'Filter': 'red', 'minI': 2887, 'maxI': 3063, 'restWavelength': 6312.00, 'ampList': [0.0807574, 1.0986008, 0.5388915], 'zone': 'low', 'sigmaT2': 5.19, 'compLimits': {'a': inf, 'c': False, 's': False}, 'copyFrom': 'SIII-9069A'}),
     ])
    # Information for the center, sigma and linear for the low (H-alpha) and high (OIII) zones
    # 4comp
    # centerList = {'low': [3918.56152, 3969.72791, 3978.93476, 4009.07339], 'high': [3923.50164, 3970.63469, 3984.13367, 4013.03660]}
    # sigmaList = {'low': [17.1238691, 13.8686163, 45.2070274, 91.5798277],'high': [15.7405389, 12.8758934, 43.6674545, 88.1013490]}
    # linSlope = {'low': -5.2237e-08, 'high': -2.8976e-07}
    # linInt = {'low': 0.00139680, 'high': 0.00254310}
    ##
    #3comp
    centerList = {'low': [3918.56152, 3978.93476, 4009.07339], 'high': [3923.50164, 3984.13367, 4013.03660]}
    sigmaList = {'low': [15.7405389, 43.6674545, 88.1013490], 'high': [15.7405389, 43.6674545, 88.1013490]}
    linSlope = {'low': -4.0088e-08, 'high': -2.8976e-07}
    linInt = {'low': 0.00138487, 'high': 0.00254310}

    numComps = {'low': 3, 'high': 3}
    #4comp
    # componentLabels = ['Narrow 1', 'Narrow 2', 'Narrow 3', 'Broad', 'Label5']
    # componentColours = ['b', 'r', 'c', 'g','m']
    #3comp
    componentLabels = ['Narrow 1', 'Narrow 2', 'Broad']
    componentColours = ['r', 'c', 'g']
    plottingXRange = [3600, 4400]  # velocities
    sigmaInstrBlue = 5.0
    sigmaInstrRed = 6.2
    distance = 1.67e26  # Distance to region in centimetres (same units as flux)

    emLinesForAvgVelCalc = ['H-Alpha', 'H-Beta_Blue', 'OIII-5007A', 'NII-6584A', 'SII-6717A']
    plotResiduals = False  #True

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
