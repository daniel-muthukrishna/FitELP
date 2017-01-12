from collections import OrderedDict

blueSpecFile = 'NGC6845_26B.fc.fits'             #'NGC6845_26B_SPEC1.wc.fits'
redSpecFile = 'NGC6845_26R.fc.fits'              #'NGC6845_26R_SPEC1.wc.fits'
blueSpecError = 'NGC6845_26B_ErrorFlux.fc.fits'  #'NGC6845_26B_VAR4.wc.fits'
redSpecError = 'NGC6845_26R_ErrorFlux.fc.fits'   #'NGC6845_26R_VAR4.wc.fits'
scaleFlux = 1e14                                # 1

# SPECTRAL LINE INFO FOR ALL EMISSION LINES
emProfiles = OrderedDict([
    ('H-Alpha', {'Colour': 'b', 'Order': 21, 'Filter': 'red', 'minI': 1180, 'maxI': 1650, 'restWavelength': 6562.82, 'ampList': [3.9e5, 9.5e4, 44.5836051], 'zone': 'low', 'sigmaT2': 164.96}),
    ('OIII-5007A', {'Colour': 'b', 'Order': 5, 'Filter': 'red', 'minI': 1600, 'maxI': 2100, 'restWavelength': 5006.84, 'ampList': [22.1758322, 26.5388225, 27.2491337], 'zone': 'high', 'sigmaT2': 41.54}),
    ('H-Beta', {'Colour': 'g', 'Order': 36, 'Filter': 'blue', 'minI': 2150, 'maxI': 2800, 'restWavelength': 4861.33, 'ampList': [7.1034076, 6.9433769, 9.0872379], 'zone': 'low', 'sigmaT2': 164.96}),
    ('H-Gamma', {'Colour': 'r', 'Order': 28, 'Filter': 'blue', 'minI': 700, 'maxI': 1200, 'restWavelength': 4340.47, 'ampList': [3.5975998, 4.4061048, 4.9858672], 'zone': 'low', 'sigmaT2': 164.96}),
    ('H-Delta', {'Colour': 'c', 'Order': 23, 'Filter': 'blue', 'minI': 1400, 'maxI': 2000, 'restWavelength': 4101.74, 'ampList': [2.044593, 2.5207303, 2.9131719], 'zone': 'low', 'sigmaT2': 164.96}),
    ('NII-6584A', {'Colour': 'y', 'Order': 21, 'Filter': 'red', 'minI': 1750, 'maxI': 2050, 'restWavelength': 6583.41, 'ampList': [1.9724283, 2.2865144, 1.5250645], 'zone': 'low', 'sigmaT2': 11.87}),
    ('NII-6548A', {'Colour': 'm', 'Order': 21, 'Filter': 'red', 'minI': 1000, 'maxI': 1300, 'restWavelength': 6548.03, 'ampList': [0.6269642, 0.7364259, 0.5323627], 'zone': 'low', 'sigmaT2': 11.87}),
    ('SII-6717A', {'Colour': 'k', 'Order': 22, 'Filter': 'red', 'minI': 1850, 'maxI': 2000, 'restWavelength': 6716.47, 'ampList': [1.6193481, 2.2161351, 1.2806343], 'zone': 'low', 'sigmaT2': 5.19}),
    ('SII-6731A', {'Colour': '#58D68D', 'Order': 22, 'Filter': 'red', 'minI': 2100, 'maxI': 2350, 'restWavelength': 6730.85, 'ampList': [1.0146995, 1.8904713, 0.4226594], 'zone': 'low', 'sigmaT2': 5.19}),
    ('OII-3729A', {'Colour': '#5D6D7E', 'Order': 14, 'Filter': 'blue', 'minI': 2800, 'maxI': 3000, 'restWavelength': 3728.82, 'ampList': [16.666917, -2.4780989, 19.0953365], 'zone': 'low', 'sigmaT2': 10.39}),
    ('OII-3726A', {'Colour': '#EC7063', 'Order': 14, 'Filter': 'blue', 'minI': 2660, 'maxI': 2829, 'restWavelength': 3726.03, 'ampList': [11.3620053, -1.5491075, 12.0488916], 'zone': 'low', 'sigmaT2': 10.39}),
    ('OII-7319A', {'Colour': '#F8C471', 'Order': 26, 'Filter': 'red', 'minI': 2252, 'maxI': 2330, 'restWavelength': 7318.39, 'ampList': [2.3677108, 1.2368295, 2.1863500], 'zone': 'low', 'sigmaT2': 10.39}),
    ('OII-7330A', {'Colour': '#7FB3D5', 'Order': 26, 'Filter': 'red', 'minI': 2420, 'maxI': 2520, 'restWavelength': 7330.0, 'ampList': [2.3677108, 1.2368295, 2.1863500], 'zone': 'low', 'sigmaT2': 10.39}),
    ('OI-6300A', {'Colour': '#D35400', 'Order': 19, 'Filter': 'red', 'minI': 1050, 'maxI': 1250, 'restWavelength': 6300.3, 'ampList': [0.4723283, 0.0564226, 0.3964602], 'zone': 'low', 'sigmaT2': 10.39}),
    ('OI-6364A', {'Colour': '#7D6608', 'Order': 19, 'Filter': 'red', 'minI': 2500, 'maxI': 2620, 'restWavelength': 6363.78, 'ampList': [2.0802379, -308.5885481, -32.2254134], 'zone': 'low', 'sigmaT2': 10.39}),
    ('SIII-9069A', {'Colour': '#27AE60', 'Order': 35, 'Filter': 'red', 'minI': 1720, 'maxI': 1870, 'restWavelength': 9068.9, 'ampList': [0.9362368, 0.7920389, 1.3819049], 'zone': 'low', 'sigmaT2': 5.19}),
    ('ArIII-7136A', {'Colour': '#0E6655', 'Order': 25, 'Filter': 'red', 'minI': 1713, 'maxI': 1790, 'restWavelength': 7135.78, 'ampList': [0.4554454, -0.227442, 1.066718], 'zone': 'low', 'sigmaT2': 4.16}),
    ('HeIH8-3889A', {'Colour': '#5B2C6F', 'Order': 18, 'Filter': 'blue', 'minI': 2450, 'maxI': 2750, 'restWavelength': 3888.65, 'ampList': [2.1000007, 4.4749605, 0.0491404], 'zone': 'low', 'sigmaT2': 41.54}),
    ('HeI-5876A', {'Colour': '#641E16', 'Order': 15, 'Filter': 'red', 'minI': 1320, 'maxI': 1700, 'restWavelength': 5875.64, 'ampList': [0.6740428, 0.8351308, 0.995738], 'zone': 'low', 'sigmaT2': 41.54}),
    ('HeI-4471A', {'Colour': '#78281F', 'Order': 30, 'Filter': 'blue', 'minI': 1750, 'maxI': 1900, 'restWavelength': 4471.48, 'ampList': [0.2947782, 0.0391142, 0.4628401], 'zone': 'low', 'sigmaT2': 41.54}),
    ('HeI-6678A', {'Colour': '#D5D8DC', 'Order': 22, 'Filter': 'red', 'minI': 1050, 'maxI': 1240, 'restWavelength': 6678.15, 'ampList': [0.2719279, -0.0142201, 0.3160476], 'zone': 'low', 'sigmaT2': 41.54}),
    ('HeI-7065A', {'Colour': '#E8DAEF', 'Order': 24, 'Filter': 'red', 'minI': 3150, 'maxI': 3450, 'restWavelength': 7065.19, 'ampList': [0.1282397, 0.0734707, 0.1437775], 'zone': 'low', 'sigmaT2': 41.54}),
    ('HeI-7281A', {'Colour': '#E8DAEF', 'Order': 26, 'Filter': 'red', 'minI': 1465, 'maxI': 1600, 'restWavelength': 7281.35, 'ampList': [0.6740428, 0.8351308, 0.9957380], 'zone': 'low', 'sigmaT2': 41.54}),
    ('OIII-4959A', {'Colour': 'g', 'Order': 4, 'Filter': 'red', 'minI': 2300, 'maxI': 2800, 'restWavelength': 4958.91, 'ampList': [6.8087454, 12.5480993, 8.2404803], 'zone': 'high', 'sigmaT2': 10.39}),
    ('NeIII-3868A', {'Colour': 'r', 'Order': 18, 'Filter': 'blue', 'minI': 1430, 'maxI': 1650, 'restWavelength': 3868.75, 'ampList': [1.7799479, 2.1882309, 2.4413756], 'zone': 'high', 'sigmaT2': 8.24}),
    ('NeIII-3970A', {'Colour': 'c', 'Order': 20, 'Filter': 'blue', 'minI': 2110, 'maxI': 2290, 'restWavelength': 3970.07, 'ampList': [1.238593, 1.6775335, 1.2004524], 'zone': 'high', 'sigmaT2': 8.24}),
    ('NeIII-3967A', {'Colour': 'm', 'Order': 20, 'Filter': 'blue', 'minI': 1950, 'maxI': 2135, 'restWavelength': 3967.46, 'ampList': [0.2356511, 2.1809468, 0.4933878], 'zone': 'high', 'sigmaT2': 8.24}),
])

# Information for the center, sigma and linear for the low (H-alpha) and high (OIII) zones
centerListLowZone = [6329.27, 6326.9, 6190.34511]
sigmaListLowZone = [28.9, 69.4, 44.5836051]
linSlopeLowZone = 1.9393e-07
linIntLowZone = 0.00761986
centerListHighZone = [6348.46630, 6333.03711, 6314.57965]
sigmaListHighZone = [15.9660139, 56.3804782, 16.6302799]
linSlopeHighZone = 2.6129e-06
linIntHighZone = -0.00147764

numComps = 3
plottingXRange = [5800, 6800]
