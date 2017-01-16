from collections import OrderedDict

blueSpecFile = 'NGC6845_26B.fc.fits'             #'NGC6845_26B_SPEC1.wc.fits'
redSpecFile = 'NGC6845_26R.fc.fits'              #'NGC6845_26R_SPEC1.wc.fits'
blueSpecError = 'NGC6845_26B_ErrorFlux.fc.fits'  #'NGC6845_26B_VAR4.wc.fits'
redSpecError = 'NGC6845_26R_ErrorFlux.fc.fits'   #'NGC6845_26R_VAR4.wc.fits'
scaleFlux = 1e14                                # 1

# SPECTRAL LINE INFO FOR ALL EMISSION LINES
emProfiles = OrderedDict([
    ('H-Alpha', {'Colour': 'b', 'Order': 21, 'Filter': 'red', 'minI': 1180, 'maxI': 1700, 'restWavelength': 6562.82, 'ampList': [21.1703448, 42.7999296, 106.280233], 'zone': 'low', 'sigmaT2': 164.96}),
    ('OIII-5007A', {'Colour': 'b', 'Order': 5, 'Filter': 'red', 'minI': 1600, 'maxI': 2100, 'restWavelength': 5006.84, 'ampList': [2.3401689, 12.4310292, 5.4627831], 'zone': 'high', 'sigmaT2': 41.54}),
    ('OIII-4959A', {'Colour': 'g', 'Order': 4, 'Filter': 'red', 'minI': 2300, 'maxI': 2700, 'restWavelength': 4958.91, 'ampList': [1.0459424, 11312.2429713, 4.5869075], 'zone': 'high', 'sigmaT2': 10.39}),
    ('H-Beta', {'Colour': 'g', 'Order': 3, 'Filter': 'red', 'minI': 1550, 'maxI': 2100, 'restWavelength': 4861.33, 'ampList': [6.7150469, 6.5487836, 36.9434462], 'zone': 'low', 'sigmaT2': 164.96}),
    ('H-Beta', {'Colour': 'g', 'Order': 36, 'Filter': 'blue', 'minI': 2000, 'maxI': 2700, 'restWavelength': 4861.33, 'ampList': [6.7150469, 6.5487836, 36.9434462], 'zone': 'low', 'sigmaT2': 164.96}),
    ('H-Gamma', {'Colour': 'r', 'Order': 28, 'Filter': 'blue', 'minI': 600, 'maxI': 1100, 'restWavelength': 4340.47, 'ampList': [3.4050631, 3.7182938, 14.5396967], 'zone': 'low', 'sigmaT2': 164.96}),
    ('H-Delta', {'Colour': 'c', 'Order': 23, 'Filter': 'blue', 'minI': 1550, 'maxI': 1850, 'restWavelength': 4101.74, 'ampList': [2.291273, -52494.8724727, -8.2103357], 'zone': 'low', 'sigmaT2': 164.96}),
    ('NII-6584A', {'Colour': 'y', 'Order': 21, 'Filter': 'red', 'minI': 1650, 'maxI': 2100, 'restWavelength': 6583.41, 'ampList': [7.1498691, 16.3987917, 36.2316252], 'zone': 'low', 'sigmaT2': 11.87}),
    ('NII-6548A', {'Colour': 'm', 'Order': 21, 'Filter': 'red', 'minI': 900, 'maxI': 1210, 'restWavelength': 6548.03, 'ampList': [2.3155066, 6.75341, 11.6409182], 'zone': 'low', 'sigmaT2': 11.87}),
    ('SII-6717A', {'Colour': 'k', 'Order': 22, 'Filter': 'red', 'minI': 1700, 'maxI': 2006, 'restWavelength': 6716.47, 'ampList': [2.6482785, 38.2404963, 13.78796], 'zone': 'low', 'sigmaT2': 5.19}),
    ('SII-6731A', {'Colour': '#58D68D', 'Order': 22, 'Filter': 'red', 'minI': 2068, 'maxI': 2273, 'restWavelength': 6730.85, 'ampList': [1.3593845, 5.9234259, 7.3026765], 'zone': 'low', 'sigmaT2': 5.19}),
    ('HeI-5876A', {'Colour': '#641E16', 'Order': 15, 'Filter': 'red', 'minI': 1350, 'maxI': 1650, 'restWavelength': 5875.64, 'ampList': [0.4850817, 0.1915922, 4.6927829], 'zone': 'low', 'sigmaT2': 41.54}),
    #('OII-3729A', {'Colour': '#5D6D7E', 'Order': 14, 'Filter': 'blue', 'minI': 2720, 'maxI': 3000, 'restWavelength': 3728.82, 'ampList': [5.0112717, -22679.7862692, -5.7298895], 'zone': 'low', 'sigmaT2': 10.39}),
    #('OII-3726A', {'Colour': '#EC7063', 'Order': 14, 'Filter': 'blue', 'minI': 2400, 'maxI': 2720, 'restWavelength': 3726.03, 'ampList': [-77.5325889, 42081.6972815, -36.5274502], 'zone': 'low', 'sigmaT2': 10.39}),
    #V('OII-7319A', {'Colour': '#F8C471', 'Order': 26, 'Filter': 'red', 'minI': 2264, 'maxI': 2321, 'restWavelength': 7318.39, 'ampList': [133570.7269853, -58921.5577832, 50738.7676701], 'zone': 'low', 'sigmaT2': 10.39}),
    #V('OII-7330A', {'Colour': '#7FB3D5', 'Order': 26, 'Filter': 'red', 'minI': 2444, 'maxI': 2513, 'restWavelength': 7329.66, 'ampList': [-23.2055153, 18.8989013, -7.1261496], 'zone': 'low', 'sigmaT2': 10.39}),
    #NO('OII-7331A', {'Colour': '#7FB3D5', 'Order': 26, 'Filter': 'red', 'minI': 2444, 'maxI': 2513, 'restWavelength': 7330.73, 'ampList': [-23.2055153, 18.8989013, -7.1261496], 'zone': 'low', 'sigmaT2': 10.39}),
    #('NII-5755A', {'Colour': '#7D6608', 'Order': 14, 'Filter': 'red', 'minI': 933, 'maxI': 1133, 'restWavelength': 5754.64, 'ampList': [0.2383146, -0.0193955, 1.3228768], 'zone': 'low', 'sigmaT2': 11.87}),
    #('NII-5755A', {'Colour': '#7D6608', 'Order': 13, 'Filter': 'red', 'minI': 3369, 'maxI': 3600, 'restWavelength': 5754.64, 'ampList': [0.2383146, -0.0193955, 1.3228768], 'zone': 'low', 'sigmaT2': 11.87}),
    #('OI-6300A', {'Colour': '#D35400', 'Order': 19, 'Filter': 'red', 'minI': 960, 'maxI': 1180, 'restWavelength': 6300.3, 'ampList': [0.2383146, -0.0193955, 1.3228768], 'zone': 'low', 'sigmaT2': 10.39}),
    #('SIII-6312A', {'Colour': '#7D6608', 'Order': 19, 'Filter': 'red', 'minI': 1226, 'maxI': 1425, 'restWavelength': 6310.20, 'ampList': [-287.7876259, 376.2168992, 82.087405], 'zone': 'low', 'sigmaT2': 5.19}),
    #('SIII-9069A', {'Colour': '#27AE60', 'Order': 35, 'Filter': 'red', 'minI': 1720, 'maxI': 1870, 'restWavelength': 9068.9, 'ampList': [3.8421937, -32687.0427018, 14.1817539], 'zone': 'low', 'sigmaT2': 5.19}),
    #NO('ArIII-7136A', {'Colour': '#0E6655', 'Order': 25, 'Filter': 'red', 'minI': 1713, 'maxI': 1790, 'restWavelength': 7135.78, 'ampList': [34222774.7678904, 43.1422347, -13.5573009], 'zone': 'low', 'sigmaT2': 4.16}),
    #NO('HeIH8-3889A', {'Colour': '#5B2C6F', 'Order': 18, 'Filter': 'blue', 'minI': 2250, 'maxI': 2750, 'restWavelength': 3888.65, 'ampList': [-1.3803811, 8.6389436, 5.0423933], 'zone': 'low', 'sigmaT2': 41.54}),
    #NO('HeI-4471A', {'Colour': '#78281F', 'Order': 30, 'Filter': 'blue', 'minI': 1750, 'maxI': 1900, 'restWavelength': 4471.48, 'ampList': [14.2789684, 4.0344708, -0.4933927], 'zone': 'low', 'sigmaT2': 41.54}),
    #('HeI-6678A', {'Colour': '#D5D8DC', 'Order': 22, 'Filter': 'red', 'minI': 955, 'maxI': 1200, 'restWavelength': 6678.15, 'ampList': [0.2025295, 0.4079972, 0.8613764], 'zone': 'low', 'sigmaT2': 41.54}),
    #NOsky('HeI-7065A', {'Colour': '#E8DAEF', 'Order': 24, 'Filter': 'red', 'minI': 3150, 'maxI': 3450, 'restWavelength': 7065.19, 'ampList': [0.186136, 1.4569275, 0.1330531], 'zone': 'low', 'sigmaT2': 41.54}),
    #NO('HeI-7281A', {'Colour': '#E8DAEF', 'Order': 26, 'Filter': 'red', 'minI': 1465, 'maxI': 1600, 'restWavelength': 7281.35, 'ampList': [0.1519096, 1.1724037, -0.5370049], 'zone': 'low', 'sigmaT2': 41.54}),
    #('NeIII-3868A', {'Colour': 'r', 'Order': 18, 'Filter': 'blue', 'minI': 1250, 'maxI': 1700, 'restWavelength': 3868.75, 'ampList': [3.5213033, 2.0376126, -0.8161938], 'zone': 'high', 'sigmaT2': 8.24}),
    ##NO('NeIII-3970A', {'Colour': 'c', 'Order': 20, 'Filter': 'blue', 'minI': 2110, 'maxI': 2290, 'restWavelength': 3970.07, 'ampList': [15340.9535303, -86633.7394279, -71288.2036669], 'zone': 'high', 'sigmaT2': 8.24}),
    #('NeIII-3967A', {'Colour': 'm', 'Order': 20, 'Filter': 'blue', 'minI': 2000, 'maxI': 2250, 'restWavelength': 3967.46, 'ampList': [2312.1030516, -33720.7186745, 30544.3475245], 'zone': 'high', 'sigmaT2': 8.24}),
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
componentColours = ['m', 'r', 'g']
plottingXRange = [5700, 6700]  # velocities