from collections import OrderedDict
import numpy as np
inf = np.inf


class RegionParameters(object):
    regionName = "Mrk600-A"

    blueSpecFile = 'blue_MrkA.fits'
    redSpecFile = 'red_MrkA.fits'
    blueSpecError = 'blue_Err_flux_MrkA.fits'
    redSpecError = 'red_Err_flux_MrkA.fits'
    scaleFlux = 1e14

    # SPECTRAL LINE INFO FOR ALL EMISSION LINES
    emProfiles = OrderedDict([
        ('H1r_6563A-P', {'Colour': 'y', 'Order': 19, 'Filter': 'red', 'minI': 740, 'maxI': 840, 'restWavelength': 6562.82, 'ampList': [30, 30, 40, 3], 'zone': 'low', 'sigmaT2': 164.96, 'compLimits': {'a': [(0.000015,inf),(0.000015,inf),(0.00015,inf),(0.00015,inf),(0.00015,inf)], 'c': inf, 's': [(11,inf),(11,inf), (11,inf),inf]}, 'copyFrom': None, 'numComps': 4}),
        ('H1r_6563A', {'Colour': 'y', 'Order': 19, 'Filter': 'red', 'minI': 740, 'maxI': 840, 'restWavelength': 6562.82, 'ampList': 4, 'zone': 'low', 'sigmaT2': 164.96, 'compLimits': {'a': [(0.000015,inf),(0.000015,inf),(0.00015,inf),(0.00015,inf)], 'c': False, 's': False}, 'copyFrom': 'H1r_6563A-P', 'numComps': 4}),
        #('H1r_6563A-P5', {'Colour': 'y', 'Order': 19, 'Filter': 'red', 'minI': 740, 'maxI': 840, 'restWavelength': 6562.82, 'ampList': [30, 30, 30, 10, 3], 'zone': 'low', 'sigmaT2': 164.96, 'compLimits': {'a': [(0.000015,inf),(0.000015,inf),(0.00015,inf),(0.00015,inf),(0.00015,inf)], 'c': inf, 's':  0.001}, 'copyFrom': None, 'numComps': 5}),


        ('O3_5007A-P', {'Colour': 'c', 'Order': 2, 'Filter': 'red', 'minI': 1650, 'maxI': 1760, 'restWavelength': 5006.84, 'ampList': [25, 65, 35, 12, 5,4], 'zone': 'high', 'sigmaT2': 10.39, 'compLimits': {'a': [(0.000015,inf),(0.000015,inf),(0.00015,inf),(0.00015,inf), inf, inf], 'c': inf, 's': inf}, 'copyFrom': None, 'numComps': 6}),
        ('O3_5007A', {'Colour': 'c', 'Order': 2, 'Filter': 'red', 'minI': 1650, 'maxI': 1760, 'restWavelength': 5006.84, 'ampList': 6, 'zone': 'high', 'sigmaT2': 10.39, 'compLimits': {'a': [(0.000015,inf),(0.000015,inf),(0.00015,inf),(0.00015,inf), inf, inf], 'c': False, 's': False}, 'copyFrom': 'O3_5007A-P', 'numComps': 6}),
      #   ('O3_5007A-P2', {'Colour': 'c', 'Order': 2, 'Filter': 'red', 'minI': 1650, 'maxI': 1760, 'restWavelength': 5006.84, 'ampList': 3, 'zone': 'high', 'sigmaT2': 10.39, 'compLimits': {'a': [(0.000015,inf),(0.000015,inf),(0.00015,inf),(0.00015,inf), inf, inf], 'c': 0.1, 's': 0.1}, 'copyFrom': 'O3_5007A-P', 'numComps': 3}),

        ('O3_4959A', {'Colour': 'g', 'Order': 2, 'Filter': 'red', 'minI': 995, 'maxI': 1065, 'restWavelength': 4958.91, 'ampList': 6, 'zone': 'high', 'sigmaT2': 10.39, 'compLimits': {'a': inf, 'c': False, 's': False}, 'copyFrom': 'O3_5007A', 'numComps': 6}),
        ('O3_4363A', {'Colour': 'g', 'Order': 11, 'Filter': 'blue', 'minI': 532, 'maxI': 625, 'restWavelength': 4363.26, 'ampList': 4, 'zone': 'high', 'sigmaT2': 10.39, 'compLimits': {'a': [(0.000015,inf),(0.000015,inf),(0.00015,inf),(0.00015,inf), inf, inf], 'c': False, 's': False}, 'copyFrom': 'O3_4959A', 'numComps': 4}),
       ### VAMOS A AJUSTAR LAS 3 COMPONENTES ANGOSTAS, SIN LA ANCHA#

        ('H1r_4861A', {'Colour': 'b', 'Order': 3, 'Filter': 'blue', 'minI': 920, 'maxI': 1060, 'restWavelength': 4861.33, 'ampList': 4, 'zone': 'low', 'sigmaT2': 164.96, 'compLimits': {'a': [(0.000015,inf),(0.000015,inf),(0.00015,inf), (0.00015,inf)], 'c': inf, 's': False}, 'copyFrom': 'H1r_6563A', 'numComps': 4}),
        ('H1r_4341A', {'Colour': 'r', 'Order': 12, 'Filter': 'blue', 'minI': 1220, 'maxI': 1370, 'restWavelength': 4340.47, 'ampList': 4, 'zone': 'low', 'sigmaT2': 164.96, 'compLimits': {'a': [(0.000015,inf),(0.000015,inf),(0.00015,inf), (0.00015,inf)], 'c': False, 's': False}, 'copyFrom': 'H1r_4861A', 'numComps': 3}),
        ('H1r_4102A', {'Colour': 'c', 'Order': 17, 'Filter': 'blue', 'minI': 1510, 'maxI': 1620, 'restWavelength': 4101.74, 'ampList': 4, 'zone': 'low', 'sigmaT2': 164.96, 'compLimits': {'a': [(0.000015,inf),(0.000015,inf),(0.00015,inf), (0.00015,inf)], 'c': False, 's': False}, 'copyFrom': 'H1r_4861A', 'numComps': 3}),


        #('H1r_3970A', {'Colour': 'c', 'Order': 19, 'Filter': 'blue', 'minI': 540, 'maxI': 605, 'restWavelength': 3970.07, 'ampList': 3, 'zone': 'low', 'sigmaT2': 8.24, 'compLimits': {'a': [(0.000015,inf),(0.000015,inf),(0.00015,inf)], 'c':0.03, 's': False}, 'copyFrom': 'H1r_4861A',  'numComps': 3}),
      ##NO ESTA##('HI-11', {'Colour': 'c', 'Order': 24, 'Filter': 'blue', 'minI': 450, 'maxI': 1530, 'restWavelength': 3770.63, 'ampList': 3, 'zone': 'low', 'sigmaT2': 164.96, 'compLimits': {'a': [(0.000015,inf),(0.000015,inf),(0.00015,inf)], 'c': 0.01, 's': False}, 'copyFrom': 'H-Alpha', 'numComps': 3}),
        #('H1r_3798A', {'Colour': 'c', 'Order': 23, 'Filter': 'blue', 'minI': 513, 'maxI': 577, 'restWavelength': 3798.00, 'ampList': 3, 'zone': 'low', 'sigmaT2': 164.96, 'compLimits': {'a': [(0.000015,inf),(0.000015,inf),(0.00015,inf)], 'c': False, 's': False}, 'copyFrom': 'H1r_4861A', 'numComps': 3}),
        #('H1r_3835A', {'Colour': 'c', 'Order': 23, 'Filter': 'blue', 'minI': 1500, 'maxI': 1580, 'restWavelength': 3835.39, 'ampList': 3, 'zone': 'low', 'sigmaT2': 164.96, 'compLimits': {'a': [(0.000015,inf),(0.000015,inf),(0.00015,inf)], 'c': False, 's': False}, 'copyFrom': 'H1r_4861A', 'numComps': 3}),
        #('H1r_9229A', {'Colour': 'c', 'Order': 34, 'Filter': 'red', 'minI': 790, 'maxI': 880, 'restWavelength': 9229.01, 'ampList': 3, 'zone': 'low', 'sigmaT2': 164.96, 'compLimits': {'a': [(0.000015,inf),(0.000015,inf),(0.00015,inf)], 'c': False, 's': False}, 'copyFrom': 'H1r_6563A', 'numComps': 3}),
        #('H1r_3734A', {'Colour': 'c', 'Order': 25, 'Filter': 'blue', 'minI': 957, 'maxI': 1070, 'restWavelength': 3734.20, 'ampList': 3, 'zone': 'low', 'sigmaT2': 164.96, 'compLimits': {'a': [(0.000015,inf),(0.000015,inf),(0.00015,inf)], 'c': 0.01, 's': 0.01}, 'copyFrom': 'H1r_4861A', 'numComps': 3}),
        ####DUDA_vER###
        #('H1r_3889A', {'Colour': '#5B2C6F', 'Order': 21, 'Filter': 'blue', 'minI': 690, 'maxI': 800, 'restWavelength': 3888.9, 'ampList': 4, 'zone': 'high', 'sigmaT2': 41.54, 'compLimits': {'a': [(0.000015,inf),(0.000015,inf),(0.00015,inf), inf], 'c': False, 's': False}, 'copyFrom': 'O3_5007A', 'numComps': 4}),

### O3_5007A
        ('N2_6584A', {'Colour': 'violet', 'Order': 19, 'Filter': 'red', 'minI': 970, 'maxI': 1060, 'restWavelength': 6583.24, 'ampList': 4, 'zone': 'low', 'sigmaT2': 11.87, 'compLimits': {'a': [(0.000001,inf),(0.000001,inf),(0.000001, inf),(0.000001, inf)], 'c': False, 's': False}, 'copyFrom': 'O3_5007A', 'numComps': 3}),
        ('N2_6548A', {'Colour': 'violet', 'Order': 19, 'Filter': 'red', 'minI': 590, 'maxI': 660, 'restWavelength': 6547.85, 'ampList': 4, 'zone': 'low', 'sigmaT2': 11.87, 'compLimits': {'a': [(0.000001,inf),(0.000001,inf),(0.000001, inf),(0.0001, inf)], 'c': False, 's': 0.5}, 'copyFrom': 'O3_5007A', 'numComps': 3}),
### H1r_6564A
        #('N2_6584A', {'Colour': 'violet', 'Order': 19, 'Filter': 'red', 'minI': 970, 'maxI': 1060, 'restWavelength': 6583.24, 'ampList': 4, 'zone': 'low', 'sigmaT2': 11.87, 'compLimits': {'a': [(0.000001,inf),(0.000001,inf),(0.000001, inf),(0.000001, inf)], 'c': [0.0001,inf,False,0.0001], 's': 0.0001}, 'copyFrom': 'H1r_6563A', 'numComps': 4}),
        #('N2_6548A', {'Colour': 'violet', 'Order': 19, 'Filter': 'red', 'minI': 606, 'maxI': 654, 'restWavelength': 6547.85, 'ampList': 4, 'zone': 'low', 'sigmaT2': 11.87, 'compLimits': {'a': [(0.000000000001,inf),(0.000000000001,inf),(0.000001, inf),(0.0000000001, inf)], 'c': False, 's': False}, 'copyFrom': 'H1r_6563A', 'numComps': 4}),

## NO USAMOS ESTE AJUSTE ###
### H1r_6564A

#   USAMOS ESTE AJUSTE
### O3_5007A
        ('S2_6716A', {'Colour': '#58D68D', 'Order': 20, 'Filter': 'red', 'minI': 1010, 'maxI': 1100, 'restWavelength': 6716.30, 'ampList': 4, 'zone': 'low', 'sigmaT2': 5.19, 'compLimits': {'a':[(0.000001,inf),(0.000001,inf),(0.000001, inf),(0.000001, inf)], 'c': [False,False,0.01, False], 's': False}, 'copyFrom': 'O3_5007A', 'numComps': 4}),
        ('S2_6731A', {'Colour': '#58D68D', 'Order': 20, 'Filter': 'red', 'minI': 1140, 'maxI': 1280, 'restWavelength': 6730.69, 'ampList': 4, 'zone': 'low', 'sigmaT2': 5.19, 'compLimits': {'a': [(0.000001,inf),(0.000001,inf),(0.000001, inf),(0.000001, inf)], 'c': [False,False,0.001, .001], 's': False}, 'copyFrom': 'S2_6716A', 'numComps': 3}),
         ##NO ESTA ###('SII-4068A', {'Colour': '#58D68D', 'Order': 17, 'Filter': 'blue', 'minI': 700, 'maxI': 810, 'restWavelength': 4068.6, 'ampList': 3, 'zone': 'low', 'sigmaT2': 5.19, 'compLimits': {'a': [(0.000001,inf),(0.000001,inf),(0.000001,inf)], 'c': 0.0001, 's': False}, 'copyFrom': 'OIII-5007A', 'numComps': 3}),

        ('O2_3729A', {'Colour': '#5D6D7E', 'Order': 25, 'Filter': 'blue', 'minI': 810, 'maxI': 900, 'restWavelength': 3728.81, 'ampList': 4, 'zone': 'low', 'sigmaT2': 10.39, 'compLimits': {'a': [(0.000015,inf),(0.000015,inf),(0.000015,inf),(0.00015,inf),(0.00015,0.0001)], 'c': False, 's': False}, 'copyFrom': 'H1r_6563A', 'numComps': 3}),
        ('O2_3726A', {'Colour': '#5D6D7E', 'Order': 25, 'Filter': 'blue', 'minI': 738, 'maxI': 813, 'restWavelength': 3726.03, 'ampList': 4, 'zone': 'low', 'sigmaT2': 10.39, 'compLimits': {'a': [(0.000015,inf),(0.000015,inf),(0.000015,inf),(0.00015,inf),(0.00015,0.01)], 'c': 0.01, 's': False}, 'copyFrom': 'O2_3729A', 'numComps': 3}),

        ('He1r_5876A', {'Colour': '#641E16', 'Order': 13, 'Filter': 'red', 'minI': 665, 'maxI': 740, 'restWavelength': 5875.55, 'ampList': 4,  'zone': 'high', 'sigmaT2': 41.54, 'compLimits': {'a': [(0.000015,inf),(0.000015,inf),(0.000015,inf),(0.00015,0.0152)], 'c': False, 's': 0.01}, 'copyFrom': 'O3_5007A', 'numComps': 3}),
        ('He1r_4471A', {'Colour': '#78281F', 'Order': 9, 'Filter': 'blue', 'minI': 450, 'maxI': 600, 'restWavelength': 4471.55, 'ampList': 4, 'zone': 'high', 'sigmaT2': 41.54, 'compLimits': {'a': [(0.000015,inf),(0.000015,inf),(0.000015,inf),(0.00015,inf)], 'c': False, 's': False}, 'copyFrom': 'He1r_5876A', 'numComps': 3}),
        ('He1r_6678A', {'Colour': '#D5D8DC', 'Order': 20, 'Filter': 'red', 'minI': 620, 'maxI': 680, 'restWavelength': 6678.05, 'ampList': 4, 'zone': 'high', 'sigmaT2': 41.54, 'compLimits': {'a': [(0.000015,inf),(0.000015,inf),(0.000015,inf),(0.00015,inf)], 'c': False, 's': False}, 'copyFrom': 'O3_5007A', 'numComps': 3}),
        ('He1r_7065A', {'Colour': '#E8DAEF', 'Order': 23, 'Filter': 'red', 'minI': 310, 'maxI': 370, 'restWavelength': 7065.0, 'ampList': 4, 'zone': 'high', 'sigmaT2': 41.54, 'compLimits': {'a': [(0.000015,inf),(0.000015,inf),(0.000015,inf),(0.00015,0.001)], 'c': False, 's': False}, 'copyFrom': 'O3_5007A', 'numComps': 3}),
        ####('He1r_7281A', {'Colour': '#E8DAEF', 'Order': 24, 'Filter': 'red', 'minI': 950, 'maxI': 1024, 'restWavelength': 7281.2, 'ampList': 4, 'zone': 'high', 'sigmaT2': 41.54, 'compLimits': {'c': False, 's': 0.01, 'a': [(0.000015,inf),(0.000015,inf),(0.000015,inf),(0.00015,0.001)]}, 'copyFrom': 'O3_5007A', 'numComps': 3}),

        ('Ne3_3869A', {'Colour': 'r', 'Order': 22, 'Filter': 'blue', 'minI': 1280, 'maxI': 1355, 'restWavelength': 3868.80, 'ampList': 4, 'zone': 'high', 'sigmaT2': 8.24, 'compLimits': {'a': [(0.000015,inf),(0.000015,inf),(0.000015,inf),(0.00015,0.01)], 'c': False, 's': False}, 'copyFrom': 'O3_5007A', 'numComps': 3}),
        ('Ne3_3968A', {'Colour': 'c', 'Order': 19, 'Filter': 'blue', 'minI': 470, 'maxI': 540, 'restWavelength': 3967.46, 'ampList': 4, 'zone': 'high', 'sigmaT2': 8.24, 'compLimits': {'a': [(0.000015,inf),(0.000015,inf),(0.00015,inf),(0.000015,inf)], 'c': False, 's': False}, 'copyFrom': 'O3_5007A', 'numComps': 3}),

        ('O1_6300A', {'Colour': '#D35400', 'Order': 17, 'Filter': 'red', 'minI': 550, 'maxI': 600, 'restWavelength': 6300.3, 'ampList': 3, 'zone': 'low', 'sigmaT2': 10.39, 'compLimits': {'a': [(0.000015,inf),(0.000015,inf),(0.00015,inf)], 'c': 0.01, 's': False}, 'copyFrom': 'O3_5007A', 'numComps': 3}),
       ##RUIUDOSO##    ('O1_6364A', {'Colour': '#7D6608', 'Order': 17, 'Filter': 'red', 'minI': 1240, 'maxI': 1330, 'restWavelength': 6363.78, 'ampList': 3, 'zone': 'low', 'sigmaT2': 10.39, 'compLimits': {'c': False, 's': False, 'a': [(0.000015,inf),(0.000015,inf),(0.00015,inf)]}, 'copyFrom': 'O3_5007A', 'numComps': 2}),

        ('S3_6312A', {'Colour': 'r', 'Order': 17, 'Filter': 'red', 'minI': 681, 'maxI': 740, 'restWavelength': 6311.95,'ampList': 3, 'zone': 'high', 'sigmaT2': 5.19,'compLimits': {'a': [(0.000015,inf),(0.000015,inf),(0.00015,inf),(0.00015,inf)], 'c': False, 's': False}, 'copyFrom': 'O3_5007A', 'numComps': 3}),
        ##('S3_6312A-2', {'Colour': 'r', 'Order': 17, 'Filter': 'red', 'minI': 681, 'maxI': 740, 'restWavelength': 6312.,'ampList': 3, 'zone': 'high', 'sigmaT2': 5.19,'compLimits': {'a': [(0.000015,inf),(0.000015,inf),(0.00015,inf),(0.00015,inf)], 'c': False, 's': False}, 'copyFrom': 'H1r_6563A', 'numComps': 3}),
        ('S3_9069A', {'Colour': '#27AE60', 'Order': 33, 'Filter': 'red', 'minI': 1450, 'maxI': 1515, 'restWavelength': 9068.78, 'ampList': 4, 'zone': 'low', 'sigmaT2': 5.19, 'compLimits': {'a': [(0.000015,inf),(0.000015,inf),(0.00015,inf),(0.00015,inf), inf], 'c': False, 's':False}, 'copyFrom': 'O3_5007A', 'numComps': 3}),

        ('O2_7319A', {'Colour': '#F8C471', 'Order': 24, 'Filter': 'red', 'minI': 1300, 'maxI': 1410, 'restWavelength': 7319.9, 'ampList': 3, 'zone': 'low', 'sigmaT2': 10.39, 'compLimits': {'a': [(0.000015,inf),(0.000015,inf),(0.00015,inf),(0.00015,0.005)], 'c': False, 's': False}, 'copyFrom': 'O3_5007A', 'numComps': 3}),
        ('O2_7330A', {'Colour': '#7FB3D5', 'Order': 24, 'Filter': 'red', 'minI': 1400, 'maxI': 1520, 'restWavelength': 7330.0, 'ampList': 3, 'zone': 'low', 'sigmaT2': 10.39, 'compLimits': {'a': [(0.000015,inf),(0.000015,inf),(0.00015,inf),(0.00015,0.005)], 'c': False, 's': False}, 'copyFrom': 'O3_5007A', 'numComps': 3}),

        ('Ar3_7136A', {'Colour': '#0E6655', 'Order': 23, 'Filter': 'red', 'minI': 980, 'maxI': 1100, 'restWavelength': 7135.7, 'ampList': 4, 'zone': 'low', 'sigmaT2': 4.16, 'compLimits': {'c': False, 's': False, 'a': [(0.000015,inf),(0.000015,inf),(0.000015,inf),(0.00015,inf)]}, 'copyFrom': 'H1r_6563A', 'numComps': 3}),
        ('Ar3_7751A', {'Colour': '#0E6655', 'Order': 27, 'Filter': 'red', 'minI': 713, 'maxI': 765, 'restWavelength': 7751.07, 'ampList': 4, 'zone': 'low', 'sigmaT2': 4.16, 'compLimits': {'c': False, 's': False, 'a': [(0.000015,inf),(0.000015,inf),(0.000015,inf),(0.00015,inf)]}, 'copyFrom': 'H1r_6563A', 'numComps': 3}),

    ])

    # Information for the center, sigma and linear for the low (H-alpha) and high (OIII) zones
    centerList = {'low': [1015, 1033, 1045, 1021, 1021], 'high': [1018, 1050, 1057, 1035, 1130, 1130]}
    sigmaList = {'low': [15, 15, 15, 17, 17], 'high': [13, 13, 13, 30, 13, 13]}
    #centerList = {'low': [1015, 1033, 1045, 1021], 'high': [1013, 1037, 1045, 1023, 1130]}
    #sigmaList = {'low': [14.2, 14.2, 14.2, 17], 'high': [12.2, 12.2, 12.2, 30, 15]}
    linSlope = {'low': 0, 'high': 0}
    linInt = {'low': 0.0761986, 'high':0.147}

    numComps = {'low': 4,'high': 6}
    componentLabels = ['Narrow1', 'Narrow2',  'Narrow3', 'Broad', 'Bullet1', 'Bullet2']
    componentColours = ['b', 'g', 'r', 'k','y','y']
    plottingXRange = [900, 1200]  # velocities
    sigmaInstrBlue = 4.9
    sigmaInstrRed = 5.6
    distance = 4.32e25  # Distance to region in centimetres (same units as flux)

    #emLinesForAvgVelCalc = [ 'OIII-5007A','H-Alpha', 'H-Beta_Blue', 'NII-6584A', 'SII-6717A']
    emLinesForAvgVelCalc = [ 'O3_5007A','H1r_6563A', 'H1r_4861A', 'N2_6584A', 'S2_6716A']


""" NOTES ON HOW TO USE THE ABOVE TABLE
The limits in 'compLimits' can be in the following forms:
    - a list indicating the limits for each component
    - a single number indicating the limits for ALL components
    - inf: indicating that the component cannot vary

ampList
    - if not list it will be take the copyFrom amplitude List and divide by the ampList scalar
"""
