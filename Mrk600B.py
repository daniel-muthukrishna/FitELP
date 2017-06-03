from collections import OrderedDict
import numpy as np
inf = np.inf


class RegionParameters(object):
    regionName = "Mrk600B05"

    blueSpecFile = 'b2_Mrkb.fits'
    redSpecFile = 'red_MrkB.fits'
    blueSpecError = 'blue_Err_flux_MrkB.fits'
    redSpecError = 'red_Err_flux_MrkB.fits'
    scaleFlux = 1e14

    # SPECTRAL LINE INFO FOR ALL EMISSION LINES
    emProfiles = OrderedDict([
        ('H1r_6563A-P', {'Colour': 'y', 'Order': 19, 'Filter': 'red', 'minI': 760, 'maxI': 830, 'restWavelength': 6562.82, 'ampList': [160, 100], 'zone': 'low', 'sigmaT2': 164.96, 'compLimits': {'a': np.inf, 'c': np.inf, 's': inf}, 'copyFrom': None, 'numComps': 2}),
        ('H1r_6563A', {'Colour': 'y', 'Order': 19, 'Filter': 'red', 'minI': 760, 'maxI': 830, 'restWavelength': 6562.82, 'ampList': [160, 100], 'zone': 'low', 'sigmaT2': 164.96, 'compLimits': {'a': np.inf, 'c': False, 's': False}, 'copyFrom': 'H1r_6563A-P', 'numComps': 2}),
        ####
        # PROPONIENDO ESTE AJUSTE, CHOCA CON LOS LIMITES DEL SIGMA MINIMO: EL AJUSTE ES MEJOR EN EL ORDEN 2, CON RESPECTO AL ORDEN 3 #
        #####
        ('O3_5007A-P', {'Colour': 'c', 'Order': 2, 'Filter': 'red', 'minI': 1675, 'maxI': 1760, 'restWavelength': 5006.84, 'ampList': [100, 100,40], 'zone': 'high', 'sigmaT2': 10.39, 'compLimits': {'a': [(0.000015,inf),(0.000015,inf), (0.000015,inf),inf], 'c': inf, 's': inf}, 'copyFrom': None, 'numComps': 3}),
        ('O3_5007A', {'Colour': 'c', 'Order': 2, 'Filter': 'red', 'minI': 1675, 'maxI': 1760, 'restWavelength': 5006.84, 'ampList': [100, 100,40], 'zone': 'high', 'sigmaT2': 10.39, 'compLimits': {'a': [(0.000015,inf),(0.000015,inf), (0.000015,inf),inf], 'c': False, 's': False}, 'copyFrom': 'O3_5007A-P', 'numComps': 3}),
        #####

        ('O3_4959A', {'Colour': 'g', 'Order': 2, 'Filter': 'red', 'minI': 995, 'maxI': 1065, 'restWavelength': 4958.91, 'ampList': 3, 'zone': 'high', 'sigmaT2': 10.39, 'compLimits': {'a': [(0.000015,inf),(0.000015,inf),(0.00015,inf),(0.00015,inf)], 'c': False, 's': False}, 'copyFrom': 'O3_5007A', 'numComps': 3}),
        ('O3_4363A', {'Colour': 'g', 'Order': 11, 'Filter': 'blue', 'minI': 530, 'maxI': 640, 'restWavelength': 4363.2, 'ampList': 2, 'zone': 'high', 'sigmaT2': 10.39, 'compLimits': {'a': [(0.000015,inf),(0.000015,inf),(0.00015,inf),(0.00015,inf)], 'c': False, 's': False}, 'copyFrom': 'O3_4959A', 'numComps': 2}),
        ### VAMOS A AJUSTAR LAS 2 COMPONENTES, SIN LA ANCHA#
        ('H1r_4861A', {'Colour': 'b', 'Order': 3, 'Filter': 'blue', 'minI': 940, 'maxI': 1050, 'restWavelength': 4861.33, 'ampList': 2, 'zone': 'low', 'sigmaT2': 164.96, 'compLimits': {'a': [(0.000015,inf),(0.000015,inf),(0.00015,inf)], 'c': inf, 's': False}, 'copyFrom': 'H1r_6563A', 'numComps': 2}),
        ##('H-Beta_Blue', {'Colour': 'b', 'Order': 3, 'Filter': 'blue', 'minI': 920, 'maxI': 1060, 'restWavelength': 4861.33, 'ampList': 4, 'zone': 'low', 'sigmaT2': 164.96, 'compLimits': {'a': [(0.000015,inf),(0.000015,inf),(0.00015,inf),(0.00015,inf)], 'c': inf, 's': False}, 'copyFrom': 'H-Alpha', 'numComps': 4}),
        ####('H-Beta_Red', {'Colour': 'r', 'Order': 1, 'Filter': 'red', 'minI': 920, 'maxI': 700, 'restWavelength': 4861.33, 'ampList': [73, 14, 22, 17], 'zone': 'low', 'sigmaT2': 164.96, 'compLimits': {'a': inf, 'c': inf , 's': 1}, 'copyFrom': 'H-Alpha', 'numComps': 4}),
        ##('H-Gamma', {'Colour': 'r', 'Order': 12, 'Filter': 'blue', 'minI': 1220, 'maxI': 1370, 'restWavelength': 4340.47, 'ampList': 4, 'zone': 'low', 'sigmaT2': 164.96, 'compLimits': {'a': [(0.000015,inf),(0.000015,inf),(0.00015,inf),(0.00015,inf)], 'c': False, 's': False}, 'copyFrom': 'H-Beta_Blue', 'numComps': 4}),
        ('H1r_4341A', {'Colour': 'r', 'Order': 12, 'Filter': 'blue', 'minI': 1260, 'maxI': 1350, 'restWavelength': 4340.47, 'ampList': 2, 'zone': 'low', 'sigmaT2': 164.96, 'compLimits': {'a': [(0.000015,inf),(0.000015,inf),(0.00015,inf)], 'c': False, 's': False}, 'copyFrom': 'H1r_4861A', 'numComps': 2}),
        ('H1r_4102A', {'Colour': 'c', 'Order': 17, 'Filter': 'blue', 'minI': 1510, 'maxI': 1630, 'restWavelength': 4101.74, 'ampList': 2, 'zone': 'low', 'sigmaT2': 164.96, 'compLimits': {'a': [(0.000015,inf),(0.000015,inf),(0.00015,inf)], 'c': False, 's': False}, 'copyFrom': 'H1r_4861A', 'numComps': 2}),
        ('H1r_3970A', {'Colour': 'c', 'Order': 19, 'Filter': 'blue', 'minI': 540, 'maxI': 630, 'restWavelength': 3970.07, 'ampList': 2, 'zone': 'low', 'sigmaT2': 164.96, 'compLimits': {'a': [(0.000015,inf),(0.000015,inf)], 'c':inf, 's': False}, 'copyFrom': 'H1r_6563A',  'numComps': 2}),
        #### NO PUEDO AJUSTAR######('HI11-11', {'Colour': 'c', 'Order': 24, 'Filter': 'blue', 'minI': 865, 'maxI': 965, 'restWavelength': 3770.63, 'ampList': 2, 'zone': 'low', 'sigmaT2': 164.96, 'compLimits': {'a': [(0.000015,inf),(0.000015,inf)], 'c': 0.5, 's':0.01 }, 'copyFrom': 'H-Alpha', 'numComps': 2}),
        #### NO PUEDO AJUSTAR######('HI10-10', {'Colour': 'c', 'Order': 23, 'Filter': 'blue', 'minI': 510, 'maxI': 610, 'restWavelength': 3798.00, 'ampList': 2, 'zone': 'low', 'sigmaT2': 164.96, 'compLimits': {'a': [(0.000015,inf),(0.000015,inf)], 'c': 0.1, 's': 0.1}, 'copyFrom': 'H-Alpha', 'numComps': 2}),
        #### NO PUEDO AJUSTARLA####('HI9-3835A', {'Colour': 'c', 'Order': 23, 'Filter': 'blue', 'minI': 1500, 'maxI': 1600, 'restWavelength': 3835.39, 'ampList': 2, 'zone': 'low', 'sigmaT2': 164.96, 'compLimits': {'a': [(0.000015,inf),(0.000015,inf)], 'c': [0.01,0.01], 's': 0.1}, 'copyFrom': 'HI-3970A', 'numComps': 2}),
        ('H1r_9229A', {'Colour': 'c', 'Order': 34, 'Filter': 'red', 'minI': 790, 'maxI': 880, 'restWavelength': 9229.01, 'ampList': 2, 'zone': 'low', 'sigmaT2': 164.96, 'compLimits': {'a': [(0.000015,inf),(0.000015,inf),(0.00015,inf)], 'c': False, 's': False}, 'copyFrom': 'H1r_6563A', 'numComps': 2}),
        #('HI13-3734A', {'Colour': 'c', 'Order': 25, 'Filter': 'blue', 'minI': 957, 'maxI': 1070, 'restWavelength': 3734.37, 'ampList': 2, 'zone': 'low', 'sigmaT2': 164.96, 'compLimits': {'a': [(0.000015,inf),(0.000015,inf),(0.00015,inf)], 'c': False, 's': False}, 'copyFrom': 'H-Beta_Blue', 'numComps': 2}),

        ('N2_6584A', {'Colour': 'violet', 'Order': 19, 'Filter': 'red', 'minI': 980, 'maxI': 1050, 'restWavelength': 6583.435, 'ampList': [2,1.2], 'zone': 'high', 'sigmaT2': 11.87, 'compLimits': {'a': [(0.000001,inf),(0.000001,inf)], 'c': inf, 's': inf}, 'copyFrom': None, 'numComps': 2}),
        ('N2_6548A', {'Colour': 'violet', 'Order': 19, 'Filter': 'red', 'minI': 606, 'maxI': 665, 'restWavelength': 6548.1, 'ampList': 2, 'zone': 'low', 'sigmaT2': 11.87, 'compLimits': {'a': [(0.00001,inf),(0.000001,inf)], 'c': 0.001, 's': False}, 'copyFrom': 'N2_6584A', 'numComps': 2}),

        ('S2_6717A', {'Colour': '#58D68D', 'Order': 20, 'Filter': 'red', 'minI': 1010, 'maxI': 1100, 'restWavelength': 6716.35, 'ampList': 2, 'zone': 'low', 'sigmaT2': 5.19, 'compLimits': {'a':[(0.000001,inf),(0.000001,inf),(0.000001, inf)], 'c': inf, 's': inf},'copyFrom': 'O3_5007A', 'numComps': 2}),
        ('S2_6731A', {'Colour': '#58D68D', 'Order': 20, 'Filter': 'red', 'minI': 1150, 'maxI': 1270, 'restWavelength': 6730.85, 'ampList': 2, 'zone': 'low', 'sigmaT2': 5.19, 'compLimits': {'a': [(0.000001,inf),(0.000001,inf),(0.000001, inf)], 'c': 0.01, 's': False}, 'copyFrom': 'S2_6717A', 'numComps': 2}),
        ('S2_4068A', {'Colour': '#58D68D', 'Order': 17, 'Filter': 'blue', 'minI': 715, 'maxI': 810, 'restWavelength': 4068.6, 'ampList': 2, 'zone': 'low', 'sigmaT2': 5.19, 'compLimits': {'a': [(0.000001,inf),(0.000001,inf)], 'c': 0.0001, 's': False}, 'copyFrom': 'O3_5007A', 'numComps': 2}),

        ('O2_3729A', {'Colour': '#5D6D7E', 'Order': 25, 'Filter': 'blue', 'minI': 810, 'maxI': 900, 'restWavelength': 3728.82, 'ampList': 2, 'zone': 'low', 'sigmaT2': 10.39, 'compLimits': {'a': [(0.000015,inf),(0.000015,inf),(0.00015,inf),(0.00015,inf)], 'c': inf, 's': inf}, 'copyFrom': 'O3_5007A', 'numComps': 2}),
        ('O2_3726A', {'Colour': '#5D6D7E', 'Order': 25, 'Filter': 'blue', 'minI': 738, 'maxI': 813, 'restWavelength': 3726.03, 'ampList': 2, 'zone': 'low', 'sigmaT2': 10.39, 'compLimits': {'a': [(0.000015,inf),(0.000015,inf),(0.00015,inf),(0.00015,inf)], 'c': inf, 's': inf}, 'copyFrom': 'O2_3729A', 'numComps': 2}),
        #('HeIH8-3889A', {'Colour': '#5B2C6F', 'Order': 21, 'Filter': 'blue', 'minI': 700, 'maxI': 800, 'restWavelength': 3889, 'ampList': 2, 'zone': 'high', 'sigmaT2': 41.54, 'compLimits': {'a': [(0.000015,inf),(0.000015,inf),(0.00015,inf)], 'c': inf, 's': inf}, 'copyFrom': 'OIII-5007A', 'numComps': 2}),

        ('He1r_5876A', {'Colour': '#641E16', 'Order': 13, 'Filter': 'red', 'minI': 650, 'maxI': 750, 'restWavelength': 5875.64, 'ampList': 2,  'zone': 'high', 'sigmaT2': 41.54, 'compLimits': {'a': [(0.000015,inf),(0.000015,inf),(0.00015,inf)], 'c': 0.01, 's': 0.01}, 'copyFrom': 'O3_5007A', 'numComps': 2}),
        ####NO PUEDO AJUSTAR####('HeI-4471A', {'Colour': '#78281F', 'Order': 9, 'Filter': 'blue', 'minI': 450, 'maxI': 600, 'restWavelength': 4471.48, 'ampList': 2, 'zone': 'high', 'sigmaT2': 41.54, 'compLimits': {'a': [(0.000015,inf),(0.000015,inf)], 'c': 0.01, 's': 0.01}, 'copyFrom': 'OIII-5007A', 'numComps': 2}),
        ('He1r_4686A', {'Colour': '#78281F', 'Order': 6, 'Filter': 'blue', 'minI': 1305, 'maxI': 1376, 'restWavelength': 4685.9, 'ampList': 2, 'zone': 'high', 'sigmaT2': 41.54, 'compLimits': {'a': [(0.000015,inf),(0.000015,inf)], 'c': 0.01, 's': False}, 'copyFrom': 'O3_5007A', 'numComps': 2}),
        ('He1r_6678A', {'Colour': '#D5D8DC', 'Order': 20, 'Filter': 'red', 'minI': 450, 'maxI': 740, 'restWavelength': 6678.15, 'ampList': 2, 'zone': 'high', 'sigmaT2': 41.54, 'compLimits': {'a': [(0.000015,inf),(0.000015,inf),(0.00015,inf)], 'c': 0.01, 's': False}, 'copyFrom': 'O3_5007A', 'numComps': 2}),
        ('He1r_7065A', {'Colour': '#E8DAEF', 'Order': 23, 'Filter': 'red', 'minI': 150, 'maxI': 450, 'restWavelength': 7065.19, 'ampList': 2, 'zone': 'high', 'sigmaT2': 41.54, 'compLimits': {'a': [(0.000015,inf),(0.000015,inf),(0.00015,inf)], 'c': 0.01, 's': False}, 'copyFrom': 'O3_5007A', 'numComps': 2}),
        ('He1r_7062A', {'Colour': '#E8DAEF', 'Order': 23, 'Filter': 'red', 'minI': 250, 'maxI': 290, 'restWavelength': 7058, 'ampList': 2, 'zone': 'high', 'sigmaT2': 41.54, 'compLimits': {'a': [(0.000015,inf),(0.000015,inf),(0.00015,inf)], 'c': 0.01, 's': False}, 'copyFrom': 'O3_5007A', 'numComps': 2}),
        ('He1r_7281A', {'Colour': '#E8DAEF', 'Order': 24, 'Filter': 'red', 'minI': 962, 'maxI': 1024, 'restWavelength': 7281.35, 'ampList': 2, 'zone': 'low', 'sigmaT2': 41.54, 'compLimits': {'c': inf, 's': False, 'a': [(0.000015,inf),(0.000015,inf),(0.00015,inf)]}, 'copyFrom': 'O3_5007A', 'numComps': 2}),

        ('Ne3_3868A', {'Colour': 'r', 'Order': 22, 'Filter': 'blue', 'minI': 1280, 'maxI': 1360, 'restWavelength': 3868.75, 'ampList': 2, 'zone': 'high', 'sigmaT2': 8.24, 'compLimits': {'a': [(0.000015,inf),(0.000015,inf),(0.00015,inf)], 'c': 0.01, 's': False}, 'copyFrom': 'O3_5007A', 'numComps': 2}),
        ('Ne3_3967A', {'Colour': 'c', 'Order': 19, 'Filter': 'blue', 'minI': 470, 'maxI': 540, 'restWavelength': 3967.46, 'ampList': 2, 'zone': 'high', 'sigmaT2': 8.24, 'compLimits': {'a': [(0.000015,inf),(0.000015,inf),(0.00015,inf)], 'c': 0.01, 's': False}, 'copyFrom': 'O3_5007A', 'numComps': 2}),

        ('O1_6300A', {'Colour': '#D35400', 'Order': 17, 'Filter': 'red', 'minI': 555, 'maxI': 600, 'restWavelength': 6300.152, 'ampList': 2, 'zone': 'low', 'sigmaT2': 10.39, 'compLimits': {'a': [(0.000000000000015,inf),(0.0000000015,inf),(0.00015,inf)], 'c': 0.01, 's': False}, 'copyFrom': 'O3_5007A', 'numComps': 2}),
        ('O1_6364A', {'Colour': '#7D6608', 'Order': 17, 'Filter': 'red', 'minI': 1240, 'maxI': 1320, 'restWavelength': 6363.78, 'ampList': 2, 'zone': 'low', 'sigmaT2': 10.39, 'compLimits': {'c': 0.01, 's': False, 'a': [(0.000015,inf),(0.000015,inf),(0.00015,inf)]}, 'copyFrom': 'H1r_6563A', 'numComps': 2}),

        ('S3_6312A', {'Colour': 'r', 'Order': 17, 'Filter': 'red', 'minI': 678, 'maxI': 742, 'restWavelength': 6311.97,'ampList': 2, 'zone': 'high', 'sigmaT2': 5.19,'compLimits': {'a': [(0.000015,inf),(0.000015,inf),(0.00015,inf)], 'c': 0.001, 's': False}, 'copyFrom': 'O3_5007A', 'numComps': 2}),
        ('S3_9069A', {'Colour': '#27AE60', 'Order': 33, 'Filter': 'red', 'minI': 1455, 'maxI': 1520, 'restWavelength': 9068.9, 'ampList': 3, 'zone': 'low', 'sigmaT2': 5.19, 'compLimits': {'a': [(0.000015,inf),(0.000015,inf),(0.00015,inf)], 'c': 0.01, 's': False}, 'copyFrom': 'O3_5007A', 'numComps': 3}),

        ('O2_7319A', {'Colour': '#F8C471', 'Order': 24, 'Filter': 'red', 'minI': 1300, 'maxI': 1410, 'restWavelength': 7319.49, 'ampList': 2, 'zone': 'low', 'sigmaT2': 10.39, 'compLimits': {'a': [(0.000015,inf),(0.000015,inf),(0.00015,inf)], 'c': inf, 's': inf}, 'copyFrom': 'O3_5007A', 'numComps': 2}),
        ('O2_7330A', {'Colour': '#7FB3D5', 'Order': 24, 'Filter': 'red', 'minI': 1400, 'maxI': 1520, 'restWavelength': 7329.71, 'ampList': 2, 'zone': 'low', 'sigmaT2': 10.39, 'compLimits': {'a': [(0.000015,inf),(0.000015,inf),(0.00015,inf)], 'c': inf, 's': inf}, 'copyFrom': 'O3_5007A', 'numComps': 2}),

        ('Ar3_7136A', {'Colour': '#0E6655', 'Order': 23, 'Filter': 'red', 'minI': 1015, 'maxI': 1080, 'restWavelength': 7135.780, 'ampList': 2, 'zone': 'low', 'sigmaT2': 4.16, 'compLimits': {'c': 0.01, 's': 0.1, 'a': [(0.000015,inf),(0.00015,inf)]}, 'copyFrom': 'O3_5007A', 'numComps': 2}),
        ('Ar3_7751A', {'Colour': '#0E6655', 'Order': 27, 'Filter': 'red', 'minI': 715, 'maxI': 768, 'restWavelength': 7751.071, 'ampList': 2, 'zone': 'low', 'sigmaT2': 4.16, 'compLimits': {'c': 0.01, 's': False, 'a': [(0.000015,inf),(0.000015,inf),(0.00015,inf)]}, 'copyFrom': 'O3_5007A', 'numComps': 2}),

    ])

    # Information for the center, sigma and linear for the low (H-alpha) and high (OIII) zones
    centerList = {'low': [1045, 1045, 1045], 'high': [1045, 1045, 1144, 1135]}
    sigmaList = {'low': [15, 25, 15], 'high': [15, 25, 15, 15]}
    linSlope = {'low': 0.0, 'high': 0.0}
    linInt = {'low': 0.0761986, 'high': 0.004}

    numComps = {'low': 2, 'high': 3}
    componentLabels = ['Narrow 1', 'Broad', 'Bullet']
    componentColours = ['b', 'r','g']
    plottingXRange = [950, 1200]  # velocities
    sigmaInstrBlue = 4.9
    sigmaInstrRed = 5.6
    distance =  4.32e25  # Distance to region in centimetres (same units as flux)

    #emLinesForAvgVelCalc = ['H-Alpha', 'H-Beta_Blue', 'OIII-5007A', 'NII-6584A', 'SII-6717A']
    emLinesForAvgVelCalc = ['H1r_6563A', 'H1r_4861A', 'O3_5007A', 'N2_6584A', 'S2_6717A']
 #   emLinesForAvgVelCalc = ['H-Alpha', 'H-Beta_Red', 'OIII-5007A','OIII-4959A']
    #emLinesForAvgVelCalc = ['H-Alpha','OIII-5007A']

""" NOTES ON HOW TO USE THE ABOVE TABLE
The limits in 'compLimits' can be in the following forms:
    - a list indicating the limits for each component
    - a single number indicating the limits for ALL components
    - inf: indicating that the component cannot vary

ampList
    - if not list it will be take the copyFrom amplitude List and divide by the ampList scalar
"""
