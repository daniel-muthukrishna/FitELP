from collections import OrderedDict

blueSpecFile = 'NGC6845_26B.fc.fits'             #'NGC6845_26B_SPEC1.wc.fits'
redSpecFile = 'NGC6845_26R.fc.fits'              #'NGC6845_26R_SPEC1.wc.fits'
blueSpecError = 'NGC6845_26B_ErrorFlux.fc.fits'  #'NGC6845_26B_VAR4.wc.fits'
redSpecError = 'NGC6845_26R_ErrorFlux.fc.fits'   #'NGC6845_26R_VAR4.wc.fits'
scaleFlux = 1e14                                # 1

# SPECTRAL LINE INFO FOR ALL EMISSION LINES
emProfiles = OrderedDict([
    ('H-Alpha', {'Colour': 'b', 'Order': 21, 'Filter': 'red', 'minI': 1180, 'maxI': 1650, 'restWavelength': 6562.82, 'ampList': [-31.0993102, 154.3044548, 42.5186764], 'zone': 'low', 'sigmaT2': 164.96}),
    ('OIII-5007A', {'Colour': 'b', 'Order': 5, 'Filter': 'red', 'minI': 1600, 'maxI': 2100, 'restWavelength': 5006.84, 'ampList': [23.8152977, 2193.0954435, -6.4845846], 'zone': 'high', 'sigmaT2': 41.54}),
    ('H-Beta', {'Colour': 'g', 'Order': 36, 'Filter': 'blue', 'minI': 2150, 'maxI': 2800, 'restWavelength': 4861.33, 'ampList': [-8.9652968, 45.0756444, 13.3564509], 'zone': 'low', 'sigmaT2': 164.96}),
    ('H-Gamma', {'Colour': 'r', 'Order': 28, 'Filter': 'blue', 'minI': 700, 'maxI': 1200, 'restWavelength': 4340.47, 'ampList': [-3.4619304, 19.8876053, 6.5649142], 'zone': 'low', 'sigmaT2': 164.96}),
    ('H-Delta', {'Colour': 'c', 'Order': 23, 'Filter': 'blue', 'minI': 1400, 'maxI': 2000, 'restWavelength': 4101.74, 'ampList': [-1257.1549502, 3.4931502, 6.7304031], 'zone': 'low', 'sigmaT2': 164.96}),
    ('NII-6584A', {'Colour': 'y', 'Order': 21, 'Filter': 'red', 'minI': 1750, 'maxI': 2050, 'restWavelength': 6583.41, 'ampList': [8.3399406, -47.9964097, 15.251975], 'zone': 'low', 'sigmaT2': 11.87}),
    ('NII-6548A', {'Colour': 'm', 'Order': 21, 'Filter': 'red', 'minI': 1000, 'maxI': 1300, 'restWavelength': 6548.03, 'ampList': [3.1826265, -16.2921006, 4.8428042], 'zone': 'low', 'sigmaT2': 11.87}),
    ('SII-6717A', {'Colour': 'k', 'Order': 22, 'Filter': 'red', 'minI': 1850, 'maxI': 2000, 'restWavelength': 6716.47, 'ampList': [-8.8060893, 40.8422933, 3.1189683], 'zone': 'low', 'sigmaT2': 5.19}),
    ('SII-6731A', {'Colour': '#58D68D', 'Order': 22, 'Filter': 'red', 'minI': 2100, 'maxI': 2350, 'restWavelength': 6730.85, 'ampList': [-2.5690966, 16.2736236, 2.4601185], 'zone': 'low', 'sigmaT2': 5.19}),
    ('OII-3729A', {'Colour': '#5D6D7E', 'Order': 14, 'Filter': 'blue', 'minI': 2800, 'maxI': 3000, 'restWavelength': 3728.82, 'ampList': [-1.1183154, -921.4483795, 3.9877515], 'zone': 'low', 'sigmaT2': 10.39}),
    ('OII-3726A', {'Colour': '#EC7063', 'Order': 14, 'Filter': 'blue', 'minI': 2660, 'maxI': 2829, 'restWavelength': 3726.03, 'ampList': [-17.4820714, 128.4904484, -1.0303192], 'zone': 'low', 'sigmaT2': 10.39}),
    ('OII-7319A', {'Colour': '#F8C471', 'Order': 26, 'Filter': 'red', 'minI': 2252, 'maxI': 2330, 'restWavelength': 7318.39, 'ampList': [137004.7761759, -368980.7151574, 135219.0603322], 'zone': 'low', 'sigmaT2': 10.39}),
    ('OII-7330A', {'Colour': '#7FB3D5', 'Order': 26, 'Filter': 'red', 'minI': 2420, 'maxI': 2520, 'restWavelength': 7330.0, 'ampList': [-1.259268, 1.2621321, -0.2768209], 'zone': 'low', 'sigmaT2': 10.39}),
    ('OI-6300A', {'Colour': '#D35400', 'Order': 19, 'Filter': 'red', 'minI': 1050, 'maxI': 1250, 'restWavelength': 6300.3, 'ampList': [-0.398422, 1.7749372, 0.4813801], 'zone': 'low', 'sigmaT2': 10.39}),
    ('OI-6364A', {'Colour': '#7D6608', 'Order': 19, 'Filter': 'red', 'minI': 2500, 'maxI': 2620, 'restWavelength': 6363.78, 'ampList': [-2.9831397, 3.2003117, 2.7289397], 'zone': 'low', 'sigmaT2': 10.39}),
    ('SIII-9069A', {'Colour': '#27AE60', 'Order': 35, 'Filter': 'red', 'minI': 1720, 'maxI': 1870, 'restWavelength': 9068.9, 'ampList': [-2.6854656, -3.2376033, 2.6272907], 'zone': 'low', 'sigmaT2': 5.19}),
    ('ArIII-7136A', {'Colour': '#0E6655', 'Order': 25, 'Filter': 'red', 'minI': 1713, 'maxI': 1790, 'restWavelength': 7135.78, 'ampList': [4.4538392, -8.425445, 8750.3032878], 'zone': 'low', 'sigmaT2': 4.16}),
    ('HeIH8-3889A', {'Colour': '#5B2C6F', 'Order': 18, 'Filter': 'blue', 'minI': 2450, 'maxI': 2750, 'restWavelength': 3888.65, 'ampList': [-2.5342761, 11.9148404, -1.4761733], 'zone': 'low', 'sigmaT2': 41.54}),
    ('HeI-5876A', {'Colour': '#641E16', 'Order': 15, 'Filter': 'red', 'minI': 1320, 'maxI': 1700, 'restWavelength': 5875.64, 'ampList': [-0.8536296, 5.1449484, 1.251355], 'zone': 'low', 'sigmaT2': 41.54}),
    ('HeI-4471A', {'Colour': '#78281F', 'Order': 30, 'Filter': 'blue', 'minI': 1750, 'maxI': 1900, 'restWavelength': 4471.48, 'ampList': [0.1765063, 1.4450822, 1.9573911], 'zone': 'low', 'sigmaT2': 41.54}),
    ('HeI-6678A', {'Colour': '#D5D8DC', 'Order': 22, 'Filter': 'red', 'minI': 1050, 'maxI': 1240, 'restWavelength': 6678.15, 'ampList': [-0.1440218, 1.1776992, 0.3785992], 'zone': 'low', 'sigmaT2': 41.54}),
    ('HeI-7065A', {'Colour': '#E8DAEF', 'Order': 24, 'Filter': 'red', 'minI': 3150, 'maxI': 3450, 'restWavelength': 7065.19, 'ampList': [-0.2040654, 1.2253885, 0.2591682], 'zone': 'low', 'sigmaT2': 41.54}),
    ('HeI-7281A', {'Colour': '#E8DAEF', 'Order': 26, 'Filter': 'red', 'minI': 1465, 'maxI': 1600, 'restWavelength': 7281.35, 'ampList': [0.9749919, 0.2172607, 0.0538293], 'zone': 'low', 'sigmaT2': 41.54}),
    ('OIII-4959A', {'Colour': 'g', 'Order': 4, 'Filter': 'red', 'minI': 2300, 'maxI': 2800, 'restWavelength': 4958.91, 'ampList': [9.3962825, 34.1797722, -2.3071007], 'zone': 'high', 'sigmaT2': 10.39}),
        ('NeIII-3868A', {'Colour': 'r', 'Order': 18, 'Filter': 'blue', 'minI': 1430, 'maxI': 1650, 'restWavelength': 3868.75, 'ampList': [1.7808936, 7.5984469, 2.6727271], 'zone': 'high', 'sigmaT2': 8.24}),
    ('NeIII-3970A', {'Colour': 'c', 'Order': 20, 'Filter': 'blue', 'minI': 2110, 'maxI': 2290, 'restWavelength': 3970.07, 'ampList': [1.238593, 1.6775335, 1.2004524], 'zone': 'high', 'sigmaT2': 8.24}),
    ('NeIII-3967A', {'Colour': 'm', 'Order': 20, 'Filter': 'blue', 'minI': 1950, 'maxI': 2135, 'restWavelength': 3967.46, 'ampList': [0.1400479, 2.1556011, 0.3788218], 'zone': 'high', 'sigmaT2': 8.24}),
])

# Information for the center, sigma and linear for the low (H-alpha) and high (OIII) zones
centerListLowZone = [6170.97557, 6185.89437, 6190.04683]
sigmaListLowZone = [17.1864991, 114.190155, 47.3997052]
linSlopeLowZone = -3.9251e-06
linIntLowZone = 0.07198545
centerListHighZone = [6170.97557, 6185.89437, 6190.04683]
sigmaListHighZone = [17.1864991, 114.190155, 47.3997052]
linSlopeHighZone = 2.6129e-06
linIntHighZone = -0.00147764

numComps = 3
plottingXRange = [5700, 6700]
