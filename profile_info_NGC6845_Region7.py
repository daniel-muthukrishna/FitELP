from collections import OrderedDict
import numpy as np


class RegionParameters(object):
    regionName = "NGC6845 Region 7"

    blueSpecFile = 'NGC6845_7B.fc.fits'             #'NGC6845_7B_SPEC1.wc.fits'
    redSpecFile = 'NGC6845_7R.fc.fits'              #'NGC6845_7R_SPEC1.wc.fits'
    blueSpecError = 'NGC6845_7B_ErrorFlux.fc.fits'  #'NGC6845_7B_VAR4.wc.fits'
    redSpecError = 'NGC6845_7R_ErrorFlux.fc.fits'   #'NGC6845_7R_VAR4.wc.fits'
    scaleFlux = 1e14                                # 1

    # SPECTRAL LINE INFO FOR ALL EMISSION LINES
    emProfiles = OrderedDict([
        ('H-Alpha', {'Colour': 'y', 'Order': 21, 'Filter': 'red', 'minI': 1180, 'maxI': 1650, 'restWavelength': 6562.82, 'ampList': [17.1349099, 25.9916747, 15.3252368], 'zone': 'low', 'sigmaT2': 164.96, 'compLimits': {'c': np.inf, 's': np.inf, 'a': np.inf}, 'copyFrom': None}),
        ('OIII-5007A', {'Colour': 'c', 'Order': 5, 'Filter': 'red', 'minI': 1600, 'maxI': 2100, 'restWavelength': 5006.84, 'ampList': [22.1758318, 26.5388225, 27.2491339], 'zone': 'high', 'sigmaT2': 41.54, 'compLimits': {'c': np.inf, 's': np.inf, 'a': np.inf}, 'copyFrom': None}),
        ('OIII-4959A', {'Colour': 'g', 'Order': 4, 'Filter': 'red', 'minI': 2300, 'maxI': 2800, 'restWavelength': 4958.91, 'ampList': [6.6607105, 8.1226648, 12.7680311], 'zone': 'high', 'sigmaT2': 10.39, 'compLimits': {'c': np.inf, 's': np.inf, 'a': np.inf}, 'copyFrom': 'OIII-5007A'}),
        ('H-Beta', {'Colour': 'b', 'Order': 36, 'Filter': 'blue', 'minI': 2150, 'maxI': 2800, 'restWavelength': 4861.33, 'ampList': [8.118223, 7.1703008, 7.7547112], 'zone': 'low', 'sigmaT2': 164.96, 'compLimits': {'c': np.inf, 's': np.inf, 'a': np.inf}, 'copyFrom': 'H-Alpha'}),
        ('H-Gamma', {'Colour': 'r', 'Order': 28, 'Filter': 'blue', 'minI': 700, 'maxI': 1200, 'restWavelength': 4340.47, 'ampList': [4.9858755, 3.5976132, 4.4060858], 'zone': 'low', 'sigmaT2': 164.96, 'compLimits': {'c': np.inf, 's': np.inf, 'a': np.inf}, 'copyFrom': 'H-Alpha'}),
        ('H-Delta', {'Colour': 'c', 'Order': 23, 'Filter': 'blue', 'minI': 1400, 'maxI': 2000, 'restWavelength': 4101.74, 'ampList': [2.433627, 1.603022, 3.289772], 'zone': 'low', 'sigmaT2': 164.96, 'compLimits': {'c': 0.01, 's': 0.05, 'a': np.inf}, 'copyFrom': 'H-Alpha'}),
        ('NII-6584A', {'Colour': 'violet', 'Order': 21, 'Filter': 'red', 'minI': 1750, 'maxI': 2050, 'restWavelength': 6583.41, 'ampList': [1.5251595, 1.9724935, 2.2863879], 'zone': 'low', 'sigmaT2': 11.87, 'compLimits': {'c': np.inf, 's': np.inf, 'a': np.inf}, 'copyFrom': None}),
        ('NII-6548A', {'Colour': 'violet', 'Order': 21, 'Filter': 'red', 'minI': 1000, 'maxI': 1300, 'restWavelength': 6548.03, 'ampList': [0.5323997, 0.6269895, 0.7363674], 'zone': 'low', 'sigmaT2': 11.87, 'compLimits': {'c': np.inf, 's': np.inf, 'a': np.inf}, 'copyFrom': 'NII-6584A'}),
        ('SII-6717A', {'Colour': 'r', 'Order': 22, 'Filter': 'red', 'minI': 1850, 'maxI': 2000, 'restWavelength': 6716.47, 'ampList': [1.2806282, 1.6193469, 2.2161406], 'zone': 'low', 'sigmaT2': 5.19, 'compLimits': {'c': np.inf, 's': np.inf, 'a': np.inf}, 'copyFrom': None}),
        ('SII-6731A', {'Colour': '#58D68D', 'Order': 22, 'Filter': 'red', 'minI': 2100, 'maxI': 2350, 'restWavelength': 6730.85, 'ampList': [1.0147012, 1.8904696, 0.4226622], 'zone': 'low', 'sigmaT2': 5.19, 'compLimits': {'c': 0.01, 's': 0.05, 'a': np.inf}, 'copyFrom': 'SII-6717A'}),
        ('OII-3729A', {'Colour': '#5D6D7E', 'Order': 14, 'Filter': 'blue', 'minI': 2800, 'maxI': 3000, 'restWavelength': 3728.82, 'ampList': [7.9383342, 21.2342271, 6.6933551], 'zone': 'low', 'sigmaT2': 10.39, 'compLimits': {'c': np.inf, 's': np.inf, 'a': np.inf}, 'copyFrom': None}),
        ('OII-3726A', {'Colour': '#EC7063', 'Order': 14, 'Filter': 'blue', 'minI': 2660, 'maxI': 2829, 'restWavelength': 3726.03, 'ampList': [5.1740013, 14.9580542, 3.9498718], 'zone': 'low', 'sigmaT2': 10.39, 'compLimits': {'c': np.inf, 's': np.inf, 'a': np.inf}, 'copyFrom': 'OII-3729A'}),
        ('OI-6300A', {'Colour': '#D35400', 'Order': 19, 'Filter': 'red', 'minI': 1050, 'maxI': 1250, 'restWavelength': 6300.3, 'ampList': [0.4723283, 0.0564224, 0.3964603], 'zone': 'low', 'sigmaT2': 10.39, 'compLimits': {'c': np.inf, 's': np.inf, 'a': np.inf}, 'copyFrom': 'H-Alpha'}),
        ('SIII-9069A', {'Colour': '#27AE60', 'Order': 35, 'Filter': 'red', 'minI': 1720, 'maxI': 1870, 'restWavelength': 9068.9, 'ampList': [0.6978967, 1.8054558, 0.9086645], 'zone': 'low', 'sigmaT2': 5.19, 'compLimits': {'c': np.inf, 's': np.inf, 'a': np.inf}, 'copyFrom': None}),
        ('HeIH8-3889A', {'Colour': '#5B2C6F', 'Order': 18, 'Filter': 'blue', 'minI': 2450, 'maxI': 2750, 'restWavelength': 3888.65, 'ampList': [2.1000008, 4.4749598, 0.0491407], 'zone': 'low', 'sigmaT2': 41.54, 'compLimits': {'c': np.inf, 's': np.inf, 'a': np.inf}, 'copyFrom': 'H-Alpha'}),
        ('HeI-5876A', {'Colour': '#641E16', 'Order': 15, 'Filter': 'red', 'minI': 1320, 'maxI': 1700, 'restWavelength': 5875.64, 'ampList': [0.6507063, 1.1013801, 0.857102], 'zone': 'low', 'sigmaT2': 41.54, 'compLimits': {'c': np.inf, 's': np.inf, 'a': np.inf}, 'copyFrom': None}),
        ('HeI-4471A', {'Colour': '#78281F', 'Order': 30, 'Filter': 'blue', 'minI': 1750, 'maxI': 1900, 'restWavelength': 4471.48, 'ampList': [0.2630987, 0.3833942, 0.3665488], 'zone': 'low', 'sigmaT2': 41.54, 'compLimits': {'c': 0.01, 's': 0.03, 'a': np.inf}, 'copyFrom': 'HeI-5876A'}),
        ('HeI-6678A', {'Colour': '#D5D8DC', 'Order': 22, 'Filter': 'red', 'minI': 1050, 'maxI': 1240, 'restWavelength': 6678.15, 'ampList': [0.2486772, 0.0866339, 0.2718688], 'zone': 'low', 'sigmaT2': 41.54, 'compLimits': {'c': np.inf, 's': np.inf, 'a': np.inf}, 'copyFrom': 'HeI-5876A'}),
        ('HeI-7065A', {'Colour': '#E8DAEF', 'Order': 24, 'Filter': 'red', 'minI': 3150, 'maxI': 3450, 'restWavelength': 7065.19, 'ampList': [0.1232987, 0.1179755, 0.1180976], 'zone': 'low', 'sigmaT2': 41.54, 'compLimits': {'c': 0.01, 's': 0.05, 'a': np.inf}, 'copyFrom': 'HeI-5876A'}),
        ('NeIII-3868A', {'Colour': 'r', 'Order': 18, 'Filter': 'blue', 'minI': 1430, 'maxI': 1650, 'restWavelength': 3868.75, 'ampList': [1.7808936, 7.5984469, 2.6727271], 'zone': 'high', 'sigmaT2': 8.24, 'compLimits': {'c': np.inf, 's': np.inf, 'a': np.inf}, 'copyFrom': 'OIII-5007A'}),
        ('NeIII-3970A', {'Colour': 'c', 'Order': 20, 'Filter': 'blue', 'minI': 2110, 'maxI': 2290, 'restWavelength': 3970.07, 'ampList': [1.238593, 1.6775335, 1.2004524], 'zone': 'high', 'sigmaT2': 8.24, 'compLimits': {'c': np.inf, 's': np.inf, 'a': np.inf}, 'copyFrom': 'OIII-5007A'}),
        ('NeIII-3967A', {'Colour': 'm', 'Order': 20, 'Filter': 'blue', 'minI': 1950, 'maxI': 2135, 'restWavelength': 3967.46, 'ampList': [0.1400479, 2.1556011, 0.3788218], 'zone': 'high', 'sigmaT2': 8.24, 'compLimits': {'c': np.inf, 's': np.inf, 'a': np.inf}, 'copyFrom': 'OIII-5007A'}),
        # ('ArIII-7136A', {'Colour': '#0E6655', 'Order': 25, 'Filter': 'red', 'minI': 1713, 'maxI': 1790, 'restWavelength': 7135.78, 'ampList': [0.4554454, -0.2274418, 1.066718], 'zone': 'low', 'sigmaT2': 4.16, 'compLimits': {'c': np.inf, 's': np.inf, 'a': np.inf}, 'copyFrom': 'H-Alpha'}),
        # ('OII-7319A', {'Colour': '#F8C471', 'Order': 26, 'Filter': 'red', 'minI': 2252, 'maxI': 2330, 'restWavelength': 7318.39, 'ampList': [2.3677108, 1.2368295, 2.1863500], 'zone': 'low', 'sigmaT2': 10.39, 'compLimits': {'c': np.inf, 's': np.inf, 'a': np.inf}, 'copyFrom': 'H-Alpha'}),
        # ('OII-7330A', {'Colour': '#7FB3D5', 'Order': 26, 'Filter': 'red', 'minI': 2420, 'maxI': 2520, 'restWavelength': 7330.0, 'ampList': [2.3677108, 1.2368295, 2.1863500], 'zone': 'low', 'sigmaT2': 10.39, 'compLimits': {'c': np.inf, 's': np.inf, 'a': np.inf}, 'copyFrom': 'H-Alpha'}),
        # ('OI-6364A', {'Colour': '#7D6608', 'Order': 19, 'Filter': 'red', 'minI': 2500, 'maxI': 2620, 'restWavelength': 6363.78, 'ampList': [2.0802379, -308.5885481, -32.2254134], 'zone': 'low', 'sigmaT2': 10.39, 'compLimits': {'c': np.inf, 's': np.inf, 'a': np.inf}, 'copyFrom': 'H-Alpha'}),
        # ('HeI-7281A', {'Colour': '#E8DAEF', 'Order': 26, 'Filter': 'red', 'minI': 1465, 'maxI': 1600, 'restWavelength': 7281.35, 'ampList': [0.6740428, 0.8351308, 0.9957380], 'zone': 'low', 'sigmaT2': 41.54, 'compLimits': {'c': np.inf, 's': np.inf, 'a': np.inf}, 'copyFrom': 'H-Alpha'}),
    ])

    # Information for the center, sigma and linear for the low (H-alpha) and high (OIII) zones
    centerList = {'low': [6315.53639, 6349.20126, 6328.97820], 'high': [6314.57965, 6348.46630, 6333.03711]}
    sigmaList = {'low': [22.2647170, 19.2852694, 64.1684056], 'high': [16.6302799, 15.9660139, 56.3804782]}
    linSlope = {'low': 1.9393e-07, 'high': 3.7183e-06}
    linInt = {'low': 0.00761986, 'high': 0.04636879}

    numComps = 3
    componentLabels = ['Narrow 1', 'Narrow 2', 'Broad']
    componentColours = ['b', 'r', 'g']
    plottingXRange = [6150, 6500]  # velocities
    sigmaInstrBlue = 4.9
    sigmaInstrRed = 5.6
    distance = 2.68e26  # Distance to region in centimetres (same units as flux)
