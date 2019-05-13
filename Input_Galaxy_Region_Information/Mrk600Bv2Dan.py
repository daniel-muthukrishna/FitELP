from collections import OrderedDict
import numpy as np
inf = np.inf


class RegionParameters(object):
    regionName = "Mrk600-Bscale2"

    blueSpecFile = 'mb_b2.fits'
    redSpecFile = 'red_MrkB.fits'
    blueSpecError = 'blue_Err_flux_MrkB.fits'
    redSpecError = 'red_Err_flux_MrkB.fits'
    scaleFlux = 1e17

    # SPECTRAL LINE INFO FOR ALL EMISSION LINES
    emProfiles = OrderedDict([
#        ('H1r_6563A-P', {'Colour': 'y', 'Order': 19, 'Filter': 'red', 'minI': 760, 'maxI': 830, 'restWavelength': 6562.82, 'ampList': [80, 50], 'zone': 'low', 'sigmaT2': 164.96, 'compLimits': {'a': np.inf, 'c': np.inf, 's': inf}, 'copyFrom': None, 'numComps': 1}),
#        ('H1r_6563A', {'Colour': 'y', 'Order': 19, 'Filter': 'red', 'minI': 760, 'maxI': 830, 'restWavelength': 6562.82, 'ampList': [80, 50], 'zone': 'low', 'sigmaT2': 164.96, 'compLimits': {'a': np.inf, 'c': False, 's': False}, 'copyFrom': 'H1r_6563A-P', 'numComps': 1}),

        ('H1r_6563A-P', {'Colour': 'y', 'Order': 19, 'Filter': 'red', 'minI': 760, 'maxI': 830, 'restWavelength': 6562.82, 'ampList': [70, 70], 'zone': 'low', 'sigmaT2': 164.96, 'compLimits': {'a': np.inf, 'c': np.inf, 's': inf}, 'copyFrom': None, 'numComps': 2}),
        ('H1r_6563A', {'Colour': 'y', 'Order': 19, 'Filter': 'red', 'minI': 760, 'maxI': 830, 'restWavelength': 6562.82, 'ampList': [70, 70], 'zone': 'low', 'sigmaT2': 164.96, 'compLimits': {'a': np.inf, 'c': False, 's': False}, 'copyFrom': 'H1r_6563A-P', 'numComps': 2}),

#        ('H1r_6563A-P', {'Colour': 'y', 'Order': 19, 'Filter': 'red', 'minI': 760, 'maxI': 830, 'restWavelength': 6562.82, 'ampList': [60, 45, 40], 'zone': 'low', 'sigmaT2': 164.96, 'compLimits': {'a': [(0.000001,inf), (0.0000001,inf), (0.0000001,inf)], 'c': np.inf, 's': [(0.000001,inf), (0.0000001,inf), (0.0000001,inf)]}, 'copyFrom': None, 'numComps': 3}),
#        ('H1r_6563A', {'Colour': 'y', 'Order': 19, 'Filter': 'red', 'minI': 760, 'maxI': 830, 'restWavelength': 6562.82, 'ampList': 3, 'zone': 'low', 'sigmaT2': 164.96, 'compLimits': {'a': [(0.000001,inf), (0.0000001,inf), (0.0000001,inf)], 'c': False, 's': [(0.000001,inf), (0.0000001,inf), (0.0000001,inf)]}, 'copyFrom': 'H1r_6563A-P', 'numComps': 3}),
        ####
        # PROPONIENDO ESTE AJUSTE, CHOCA CON LOS LIMITES DEL SIGMA MINIMO: EL AJUSTE ES MEJOR EN EL ORDEN 2, CON RESPECTO AL ORDEN 3 #
        #####
        ('O3_5007A-P', {'Colour': 'c', 'Order': 3, 'Filter': 'red', 'minI':630, 'maxI': 706, 'restWavelength': 5006.84, 'ampList': [70, 70,10], 'zone': 'high', 'sigmaT2': 10.39, 'compLimits': {'a': [(0.000015,inf),(0.000015,inf), (0.000015,inf),inf], 'c': inf, 's': inf}, 'copyFrom': None, 'numComps': 3}),
        ('O3_5007A', {'Colour': 'c', 'Order': 3, 'Filter': 'red', 'minI': 630, 'maxI': 706, 'restWavelength': 5006.84, 'ampList': 3, 'zone': 'high', 'sigmaT2': 10.39, 'compLimits': {'a': [(0.000015,inf),(0.000015,inf), (0.000015,inf),inf], 'c': False, 's': False}, 'copyFrom': 'O3_5007A-P', 'numComps': 3}),
        #####

#        ('O3_4959A-p', {'Colour': 'g', 'Order': 2, 'Filter': 'red', 'minI': 995, 'maxI': 1065, 'restWavelength': 4958.91, 'ampList': 2, 'zone': 'high', 'sigmaT2': 10.39, 'compLimits': {'a': [(0.000015,inf),(0.000015,inf),(0.00015,inf),(0.00015,inf)], 'c': False, 's': False}, 'copyFrom': 'O3_5007A', 'numComps': 2}),
#        ('O3_4959A', {'Colour': 'g', 'Order': 2, 'Filter': 'red', 'minI': 995, 'maxI': 1065, 'restWavelength': 4958.91, 'ampList': 2, 'zone': 'high', 'sigmaT2': 10.39, 'compLimits': {'a': [(0.000015,inf),(0.000015,inf),(0.00015,inf),(0.00015,inf)], 'c': False, 's': False}, 'copyFrom': 'O3_4959A-p', 'numComps': 2}),

#        ('O3_4363Ap', {'Colour': 'g', 'Order': 11, 'Filter': 'blue', 'minI': 540, 'maxI': 640, 'restWavelength': 4363.182, 'ampList': 2, 'zone': 'high', 'sigmaT2': 10.39, 'compLimits': {'a': [(0.000015,inf),(0.000015,inf),(0.00015,inf),(0.00015,inf)], 'c': 0.002, 's': 0.002}, 'copyFrom': 'O3_4959A', 'numComps': 2}),
#        ('O3_4363A', {'Colour': 'g', 'Order': 11, 'Filter': 'blue', 'minI': 540, 'maxI': 640, 'restWavelength': 4363.182, 'ampList': 2, 'zone': 'high', 'sigmaT2': 10.39, 'compLimits': {'a': [(0.000015,inf),(0.000015,inf),(0.00015,inf),(0.00015,inf)], 'c': False, 's': False}, 'copyFrom': 'O3_4363Ap', 'numComps': 2}),
        ### VAMOS A AJUSTAR LAS 2 COMPONENTES, SIN LA ANCHA#
        ('H1r_4861Ap', {'Colour': 'b', 'Order': 3, 'Filter': 'blue', 'minI': 940, 'maxI': 1050, 'restWavelength': 4861.374, 'ampList': 2, 'zone': 'low', 'sigmaT2': 164.96, 'compLimits': {'a': [(0.000015,inf),(0.000015,inf),(0.00015,inf)], 'c': 0.002, 's': 0.002}, 'copyFrom': 'H1r_6563A', 'numComps': 2}),
        ('H1r_4861A', {'Colour': 'b', 'Order': 3, 'Filter': 'blue', 'minI': 940, 'maxI': 1050, 'restWavelength': 4861.374, 'ampList': 2, 'zone': 'low', 'sigmaT2': 164.96, 'compLimits': {'a': [(0.000015,inf),(0.000015,inf),(0.00015,inf)], 'c': False, 's': False}, 'copyFrom': 'H1r_4861Ap', 'numComps': 2}),

        ('H1r_4341Ap', {'Colour': 'r', 'Order': 12, 'Filter': 'blue', 'minI': 1260, 'maxI': 1350, 'restWavelength': 4340.49, 'ampList': 2, 'zone': 'low', 'sigmaT2': 164.96, 'compLimits': {'a': [(0.000015,inf),(0.000015,inf),(0.00015,inf)], 'c': 0.0031, 's': 0.001}, 'copyFrom': 'H1r_6563A', 'numComps': 2}),#
        ('H1r_4341A', {'Colour': 'r', 'Order': 12, 'Filter': 'blue', 'minI': 1260, 'maxI': 1350, 'restWavelength': 4340.49, 'ampList': 2, 'zone': 'low', 'sigmaT2': 164.96, 'compLimits': {'a': [(0.000015,inf),(0.000015,inf),(0.00015,inf)], 'c': False, 's': False}, 'copyFrom': 'H1r_4341Ap', 'numComps': 2}),#

#        ('H1r_4102Ap', {'Colour': 'c', 'Order': 17, 'Filter': 'blue', 'minI': 1510, 'maxI': 1630, 'restWavelength': 4101.76, 'ampList': 2, 'zone': 'low', 'sigmaT2': 164.96, 'compLimits': {'a': [(0.000015,inf),(0.000015,inf),(0.00015,inf)], 'c': 0.0031, 's': 0.001}, 'copyFrom': 'H1r_6563A', 'numComps': 2}),
#        ('H1r_4102A', {'Colour': 'c', 'Order': 17, 'Filter': 'blue', 'minI': 1510, 'maxI': 1630, 'restWavelength': 4101.76, 'ampList': 2, 'zone': 'low', 'sigmaT2': 164.96, 'compLimits': {'a': [(0.000015,inf),(0.000015,inf),(0.00015,inf)], 'c': False, 's': False}, 'copyFrom': 'H1r_4102Ap', 'numComps': 2}),

        #('H1r_3970A', {'Colour': 'c', 'Order': 19, 'Filter': 'blue', 'minI': 540, 'maxI': 630, 'restWavelength': 3970.07, 'ampList': 2, 'zone': 'low', 'sigmaT2': 164.96, 'compLimits': {'a': [(0.000015,inf),(0.000015,inf)], 'c':inf, 's': False}, 'copyFrom': 'H1r_6563A',  'numComps': 2}),
        #('H1r_3770A', {'Colour': 'c', 'Order': 24, 'Filter': 'blue', 'minI': 868, 'maxI': 962, 'restWavelength': 3770.69, 'ampList': 2, 'zone': 'low', 'sigmaT2': 164.96, 'compLimits': {'a': [(0.000015,inf),(0.000015,inf)], 'c': 0.1, 's': 0.01 }, 'copyFrom': 'H1r_6563A', 'numComps': 2}),
        #('H1r_3798A', {'Colour': 'c', 'Order': 23, 'Filter': 'blue', 'minI': 515, 'maxI': 604, 'restWavelength': 3797.9201, 'ampList': 2, 'zone': 'low', 'sigmaT2': 164.96, 'compLimits': {'a': [(0.000015,inf),(0.000015,inf)], 'c': False, 's': False}, 'copyFrom': 'O3_5007A', 'numComps': 2}),
        #('H1r_3835A', {'Colour': 'c', 'Order': 23, 'Filter': 'blue', 'minI': 1505, 'maxI': 1598, 'restWavelength': 3835.42, 'ampList': 2, 'zone': 'low', 'sigmaT2': 164.96, 'compLimits': {'a': [(0.000015,inf),(0.000015,inf)], 'c': 0.01, 's': 0.12}, 'copyFrom': 'H1r_6563A', 'numComps': 2}),
        #('H1r_9229A', {'Colour': 'c', 'Order': 34, 'Filter': 'red', 'minI': 790, 'maxI': 880, 'restWavelength': 9229.01, 'ampList': 2, 'zone': 'low', 'sigmaT2': 164.96, 'compLimits': {'a': [(0.000015,inf),(0.000015,inf),(0.00015,inf)], 'c': False, 's': False}, 'copyFrom': 'H1r_6563A', 'numComps': 2}),
        #('H1r_3734A', {'Colour': 'c', 'Order': 25, 'Filter': 'blue', 'minI': 957, 'maxI': 1070, 'restWavelength': 3734.37, 'ampList': 2, 'zone': 'low', 'sigmaT2': 164.96, 'compLimits': {'a': [(0.000015,inf),(0.000015,inf),(0.00015,inf)], 'c': False, 's': False}, 'copyFrom': 'H1r_4861A', 'numComps': 2}),


        #('H1r_3889A', {'Colour': '#5B2C6F', 'Order': 21, 'Filter': 'blue', 'minI': 700, 'maxI': 800, 'restWavelength': 3888.9, 'ampList': 2, 'zone': 'high', 'sigmaT2': 41.54, 'compLimits': {'a': [(0.000015,inf),(0.000015,inf),(0.00015,inf)], 'c': False, 's': False}, 'copyFrom': 'O3_5007A', 'numComps': 2}),
        # ('H1r_3889A', {'Colour': '#5B2C6F', 'Order': 21, 'Filter': 'blue', 'minI': 700, 'maxI': 800, 'restWavelength': 3888.9, 'ampList': 2, 'zone': 'high', 'sigmaT2': 41.54, 'compLimits': {'a': [(0.000015,inf),(0.000015,inf),(0.00015,inf)], 'c': False, 's': False}, 'copyFrom': 'O3_5007A', 'numComps': 2}),

        # COPIO SOLUCION 5007 #
        ('N2_6584A', {'Colour': 'violet', 'Order': 19, 'Filter': 'red', 'minI': 980, 'maxI': 1050, 'restWavelength': 6583.415, 'ampList': 2, 'zone': 'low', 'sigmaT2': 11.87, 'compLimits': {'a': [(0.000001,inf),(0.000001,inf)], 'c': False, 's': False}, 'copyFrom': 'O3_5007A', 'numComps': 2}),
        #('N2_6584A', {'Colour': 'violet', 'Order': 19, 'Filter': 'red', 'minI': 980, 'maxI': 1050, 'restWavelength': 6583.415, 'ampList': 2, 'zone': 'low', 'sigmaT2': 11.87, 'compLimits': {'a': [(0.000001,inf),(0.000001,inf)], 'c': False, 's': False}, 'copyFrom': 'N2_6584Ap', 'numComps': 2}),

#        ('N2_6584A-ha', {'Colour': 'violet', 'Order': 19, 'Filter': 'red', 'minI': 980, 'maxI': 1050, 'restWavelength': 6583.415, 'ampList': 2, 'zone': 'low', 'sigmaT2': 11.87, 'compLimits': {'a': [(0.000001,inf),(0.000001,inf)], 'c': inf, 's': inf}, 'copyFrom': 'H1r_6563A', 'numComps': 2}),
#        ('N2_6548A', {'Colour': 'violet', 'Order': 19, 'Filter': 'red', 'minI': 606, 'maxI': 665, 'restWavelength': 6548.011, 'ampList': 2, 'zone': 'low', 'sigmaT2': 11.87, 'compLimits': {'a': [(0.00001,inf),(0.000001,inf)], 'c':False, 's': False}, 'copyFrom': 'H1r_6563A', 'numComps': 2}),
        #('N2_6548A', {'Colour': 'violet', 'Order': 19, 'Filter': 'red', 'minI': 606, 'maxI': 665, 'restWavelength': 6548.011, 'ampList': 2, 'zone': 'low', 'sigmaT2': 11.87, 'compLimits': {'a': [(0.00001,inf),(0.000001,inf)], 'c':False, 's': False}, 'copyFrom': 'N2_6548Ap', 'numComps': 2}),

        #copio 5007#
        ('S2_6716Ap', {'Colour': '#58D68D', 'Order': 20, 'Filter': 'red', 'minI': 1030, 'maxI': 1090, 'restWavelength': 6716.4, 'ampList': 2, 'zone': 'low', 'sigmaT2': 5.19, 'compLimits': {'a':[(0.000001,inf),(0.000001,inf),(0.000001, inf)], 'c': 0.0003, 's': False},'copyFrom': 'O3_5007A', 'numComps': 2}),
 #       ('S2_6716A', {'Colour': '#58D68D', 'Order': 20, 'Filter': 'red', 'minI': 1030, 'maxI': 1090, 'restWavelength': 6716.4, 'ampList': 2, 'zone': 'low', 'sigmaT2': 5.19, 'compLimits': {'a':[(0.000001,inf),(0.000001,inf),(0.000001, inf)], 'c': False, 's': False},'copyFrom': 'S2_6716Ap', 'numComps': 2}),

#        ('S2_6731A', {'Colour': '#58D68D', 'Order': 20, 'Filter': 'red', 'minI': 1150, 'maxI': 1270, 'restWavelength': 6730.77, 'ampList': 2, 'zone': 'low', 'sigmaT2': 5.19, 'compLimits': {'a': [(0.000001,inf),(0.000001,inf),(0.000001, inf)], 'c': False, 's': False}, 'copyFrom': 'S2_6716A', 'numComps': 2}),
        #('S2_6731A', {'Colour': '#58D68D', 'Order': 20, 'Filter': 'red', 'minI': 1150, 'maxI': 1270, 'restWavelength': 6730.77, 'ampList': 2, 'zone': 'low', 'sigmaT2': 5.19, 'compLimits': {'a': [(0.000001,inf),(0.000001,inf),(0.000001, inf)], 'c': False, 's': False}, 'copyFrom': 'S2_6731Ap', 'numComps': 2}),
        #copio Ha #
#        ('S2_6716A-h', {'Colour': '#58D68D', 'Order': 20, 'Filter': 'red', 'minI': 1030, 'maxI': 1090, 'restWavelength': 6716.47, 'ampList': 2, 'zone': 'low', 'sigmaT2': 5.19, 'compLimits': {'a':[(0.000001,inf),(0.000001,inf),(0.000001, inf)], 'c': [False, inf], 's': False},'copyFrom': 'H1r_6563A', 'numComps': 2}),
#        ('S2_6731A-h', {'Colour': '#58D68D', 'Order': 20, 'Filter': 'red', 'minI': 1150, 'maxI': 1270, 'restWavelength': 6730.8, 'ampList': 2, 'zone': 'low', 'sigmaT2': 5.19, 'compLimits': {'a': [(0.000001,inf),(0.000001,inf),(0.000001, inf)], 'c': False, 's': False}, 'copyFrom': 'S2_6716A-h', 'numComps': 2}),
###        ('S2_4068A', {'Colour': '#58D68D', 'Order': 17, 'Filter': 'blue', 'minI': 721, 'maxI': 804, 'restWavelength': 4068.61, 'ampList': 2, 'zone': 'low', 'sigmaT2': 5.19, 'compLimits': {'a': [(0.000001,inf),(0.000001,inf)], 'c': [False, inf], 's': False}, 'copyFrom': 'O3_5007A', 'numComps': 2}),

#        ('O2_3729Ap', {'Colour': '#5D6D7E', 'Order': 25, 'Filter': 'blue', 'minI': 810, 'maxI': 900, 'restWavelength': 3728.81, 'ampList': 2, 'zone': 'low', 'sigmaT2': 10.39, 'compLimits': {'a': [(0.000015,inf),(0.000015,inf),(0.00015,inf),(0.00015,inf)], 'c': inf, 's': inf}, 'copyFrom': 'H1r_6563A', 'numComps': 2}),
#        ('O2_3729A', {'Colour': '#5D6D7E', 'Order': 25, 'Filter': 'blue', 'minI': 810, 'maxI': 900, 'restWavelength': 3728.81, 'ampList': 2, 'zone': 'low', 'sigmaT2': 10.39, 'compLimits': {'a': [(0.000015,inf),(0.000015,inf),(0.00015,inf),(0.00015,inf)], 'c': False, 's': False}, 'copyFrom': 'O2_3729Ap', 'numComps': 2}),

#        ('O2_3726A', {'Colour': '#5D6D7E', 'Order': 25, 'Filter': 'blue', 'minI': 738, 'maxI': 813, 'restWavelength': 3726.05, 'ampList': 2, 'zone': 'low', 'sigmaT2': 10.39, 'compLimits': {'a': [(0.000015,inf),(0.000015,inf),(0.00015,inf),(0.00015,inf)], 'c': False, 's': False}, 'copyFrom': 'O2_3729A', 'numComps': 2}),
        #('O2_3726A', {'Colour': '#5D6D7E', 'Order': 25, 'Filter': 'blue', 'minI': 738, 'maxI': 813, 'restWavelength': 3726.05, 'ampList': 2, 'zone': 'low', 'sigmaT2': 10.39, 'compLimits': {'a': [(0.000015,inf),(0.000015,inf),(0.00015,inf),(0.00015,inf)], 'c': False, 's': False}, 'copyFrom': 'O2_3726Ap', 'numComps': 2}),
 #       ('He1r_5876A', {'Colour': '#641E16', 'Order': 13, 'Filter': 'red', 'minI': 650, 'maxI': 750, 'restWavelength': 5875.5025, 'ampList': 2,  'zone': 'high', 'sigmaT2': 41.54, 'compLimits': {'a': [(0.000015,inf),(0.000015,inf),(0.00015,inf)], 'c': [inf, False], 's': False}, 'copyFrom': 'O3_5007A', 'numComps': 2}),
        #('He1r_5876A', {'Colour': '#641E16', 'Order': 13, 'Filter': 'red', 'minI': 650, 'maxI': 750, 'restWavelength': 5875.5025, 'ampList': 2,  'zone': 'high', 'sigmaT2': 41.54, 'compLimits': {'a': [(0.000015,inf),(0.000015,inf),(0.00015,inf)], 'c': [inf, False], 's': False}, 'copyFrom': 'He1r_5876Ap', 'numComps': 2}),
 #       ('He1r_4471A', {'Colour': '#78281F', 'Order': 9, 'Filter': 'blue', 'minI': 454, 'maxI': 600, 'restWavelength': 4471.48, 'ampList': 2, 'zone': 'high', 'sigmaT2': 41.54, 'compLimits': {'a': [(0.000015,inf),(0.000015,inf)], 'c': False, 's':False}, 'copyFrom': 'O3_5007A', 'numComps': 2}),
        #('He1r_4471A', {'Colour': '#78281F', 'Order': 9, 'Filter': 'blue', 'minI': 454, 'maxI': 600, 'restWavelength': 4471.48, 'ampList': 2, 'zone': 'high', 'sigmaT2': 41.54, 'compLimits': {'a': [(0.000015,inf),(0.000015,inf)], 'c': False, 's':False}, 'copyFrom': 'He1r_4471A', 'numComps': 2}),
 #       ('He2r_4686A', {'Colour': '#78281F', 'Order': 6, 'Filter': 'blue', 'minI': 1305, 'maxI': 1390, 'restWavelength': 4685.948, 'ampList': 2, 'zone': 'high', 'sigmaT2': 41.54, 'compLimits': {'a': [(0.000015,inf),(0.000015,inf)], 'c': [inf, False], 's': False}, 'copyFrom': 'O3_5007A', 'numComps': 2}),
        #('He2r_4686A', {'Colour': '#78281F', 'Order': 6, 'Filter': 'blue', 'minI': 1305, 'maxI': 1390, 'restWavelength': 4685.948, 'ampList': 2, 'zone': 'high', 'sigmaT2': 41.54, 'compLimits': {'a': [(0.000015,inf),(0.000015,inf)], 'c': [inf, False], 's': False}, 'copyFrom': 'He2r_4686Ap', 'numComps': 2}),

 #       ('He1r_6678AP', {'Colour': '#D5D8DC', 'Order': 20, 'Filter': 'red', 'minI': 620, 'maxI': 700, 'restWavelength': 6678.15, 'ampList': 2, 'zone': 'high', 'sigmaT2': 41.54, 'compLimits': {'a': [(0.000015,inf),(0.000015,inf),(0.00015,inf)], 'c': 0.0031, 's': False}, 'copyFrom': 'O3_5007A', 'numComps': 2}),
 #       ('He1r_6678A', {'Colour': '#D5D8DC', 'Order': 20, 'Filter': 'red', 'minI': 620, 'maxI': 700, 'restWavelength': 6678.15, 'ampList': 2, 'zone': 'high', 'sigmaT2': 41.54, 'compLimits': {'a': [(0.000015,inf),(0.000015,inf),(0.00015,inf)], 'c': False, 's': False}, 'copyFrom': 'He1r_6678AP', 'numComps': 2}),

 #       ('He1r_7065Ap', {'Colour': '#E8DAEF', 'Order': 23, 'Filter': 'red', 'minI': 300, 'maxI': 380, 'restWavelength': 7065.24319, 'ampList': 2, 'zone': 'high', 'sigmaT2': 41.54, 'compLimits': {'a': [(0.000015,inf),(0.00015,inf)], 'c': [inf, False], 's': False}, 'copyFrom': 'O3_5007A', 'numComps': 2}),
 #       ('He1r_7065A', {'Colour': '#E8DAEF', 'Order': 23, 'Filter': 'red', 'minI': 300, 'maxI': 380, 'restWavelength': 7065.24319, 'ampList': 2, 'zone': 'high', 'sigmaT2': 41.54, 'compLimits': {'a': [(0.000015,inf),(0.00015,inf)], 'c': False, 's': False}, 'copyFrom': 'He1r_7065Ap', 'numComps': 2}),

###        ('He1r_7281A', {'Colour': '#E8DAEF', 'Order': 24, 'Filter': 'red', 'minI': 962, 'maxI': 1024, 'restWavelength': 7281.35, 'ampList': 2, 'zone': 'low', 'sigmaT2': 41.54, 'compLimits': {'c': [False, inf], 's': False, 'a': [(0.000015,inf),(0.000015,inf)]}, 'copyFrom': 'O3_5007A', 'numComps': 2}),

 #       ('Ne3_3868Ap', {'Colour': 'r', 'Order': 22, 'Filter': 'blue', 'minI': 1280, 'maxI': 1360, 'restWavelength': 3868.75, 'ampList': 2, 'zone': 'high', 'sigmaT2': 8.24, 'compLimits': {'a': [(0.000015,inf),(0.000015,inf),(0.00015,inf)], 'c': 0.001, 's': False}, 'copyFrom': 'O3_5007A', 'numComps': 2}),
 #       ('Ne3_3868A', {'Colour': 'r', 'Order': 22, 'Filter': 'blue', 'minI': 1280, 'maxI': 1360, 'restWavelength': 3868.75, 'ampList': 2, 'zone': 'high', 'sigmaT2': 8.24, 'compLimits': {'a': [(0.000015,inf),(0.000015,inf),(0.00015,inf)], 'c': False, 's': False}, 'copyFrom': 'Ne3_3868Ap', 'numComps': 2}),

        #('Ne3_3968A', {'Colour': 'c', 'Order': 19, 'Filter': 'blue', 'minI': 470, 'maxI': 540, 'restWavelength': 3967.46, 'ampList': 2, 'zone': 'high', 'sigmaT2': 8.24, 'compLimits': {'a': [(0.000015,inf),(0.000015,inf),(0.00015,inf)], 'c': 0.01, 's': False}, 'copyFrom': 'O3_5007A', 'numComps': 2}),

#        ('O1_6300Ap', {'Colour': '#D35400', 'Order': 17, 'Filter': 'red', 'minI': 555, 'maxI': 600, 'restWavelength': 6300.318152, 'ampList': 2, 'zone': 'low', 'sigmaT2': 10.39, 'compLimits': {'a': [(0.000000000000015,inf),(0.0000000015,inf),(0.00015,inf)], 'c': inf, 's': inf}, 'copyFrom': 'H1r_6563A', 'numComps': 2}),
#        ('O1_6300A', {'Colour': '#D35400', 'Order': 17, 'Filter': 'red', 'minI': 555, 'maxI': 600, 'restWavelength': 6300.318152, 'ampList': 2, 'zone': 'low', 'sigmaT2': 10.39, 'compLimits': {'a': [(0.000000000000015,inf),(0.0000000015,inf),(0.00015,inf)], 'c': False, 's': False}, 'copyFrom': 'O1_6300Ap', 'numComps': 2}),
#        ('O1_6364Ap', {'Colour': '#7D6608', 'Order': 17, 'Filter': 'red', 'minI': 1250, 'maxI': 1340, 'restWavelength': 6363.98, 'ampList': 2, 'zone': 'low', 'sigmaT2': 10.39, 'compLimits': {'c': 0.001, 's': False, 'a': [(0.000015,inf),(0.000015,inf),(0.00015,inf)]}, 'copyFrom': 'H1r_6563A', 'numComps': 2}),
#        ('O1_6364A', {'Colour': '#7D6608', 'Order': 17, 'Filter': 'red', 'minI': 1250, 'maxI': 1340, 'restWavelength': 6363.98, 'ampList': 2, 'zone': 'low', 'sigmaT2': 10.39, 'compLimits': {'c': False, 's': False, 'a': [(0.000015,inf),(0.000015,inf),(0.00015,inf)]}, 'copyFrom': 'O1_6364Ap', 'numComps': 2}),

        #####('S3_6312A', {'Colour': 'r', 'Order': 17, 'Filter': 'red', 'minI': 678, 'maxI': 742, 'restWavelength': 6312.0109,'ampList': 2, 'zone': 'high', 'sigmaT2': 5.19,'compLimits': {'a': [(0.000015,inf),(0.000015,inf),(0.00015,inf)], 'c': False, 's': False}, 'copyFrom': 'O3_5007A', 'numComps': 2}),
        ('S3_9069Ap', {'Colour': '#27AE60', 'Order': 33, 'Filter': 'red', 'minI': 1455, 'maxI': 1520, 'restWavelength': 9068.9753, 'ampList': 3, 'zone': 'low', 'sigmaT2': 5.19, 'compLimits': {'a': [(0.000015,inf),(0.000015,inf),(0.00015,inf)], 'c': [0.01,False,inf], 's': False}, 'copyFrom': 'O3_5007A', 'numComps': 3}),
        ('S3_9069A', {'Colour': '#27AE60', 'Order': 33, 'Filter': 'red', 'minI': 1455, 'maxI': 1520, 'restWavelength': 9068.9753, 'ampList': 3, 'zone': 'low', 'sigmaT2': 5.19, 'compLimits': {'a': [(0.000015,inf),(0.000015,inf),(0.00015,inf)], 'c': False, 's': False}, 'copyFrom': 'S3_9069Ap', 'numComps': 3}),
        ############3('S3_9069A', {'Colour': '#27AE60', 'Order': 33, 'Filter': 'red', 'minI': 1455, 'maxI': 1520, 'restWavelength': 9068.9753, 'ampList': 3, 'zone': 'low', 'sigmaT2': 5.19, 'compLimits': {'a': [(0.000015,inf),(0.000015,inf),(0.00015,inf)], 'c': [inf,inf, False], 's': inf}, 'copyFrom': ['H1r_6563A','H1r_6563A','O3_5007A'], 'numComps': 3}),
        ('S3_6312A', {'Colour': 'r', 'Order': 17, 'Filter': 'red', 'minI': 678, 'maxI': 742, 'restWavelength': 6312.0109,'ampList': 2, 'zone': 'high', 'sigmaT2': 5.19,'compLimits': {'a': [(0.000015,inf),(0.000015,inf),(0.00015,inf)], 'c': False, 's': False}, 'copyFrom': 'S3_9069A', 'numComps': 2}),
        #('S3_6312A', {'Colour': 'r', 'Order': 17, 'Filter': 'red', 'minI': 678, 'maxI': 742, 'restWavelength': 6312.0109,'ampList': 2, 'zone': 'high', 'sigmaT2': 5.19,'compLimits': {'a': [(0.000015,inf),(0.000015,inf),(0.00015,inf)], 'c': False, 's': False}, 'copyFrom': 'S3_6312Ap', 'numComps': 2}),

        ###('O2_7319A', {'Colour': '#F8C471', 'Order': 24, 'Filter': 'red', 'minI': 1320, 'maxI': 1400, 'restWavelength': 7319.79, 'ampList':2, 'zone': 'high', 'sigmaT2': 10.39, 'compLimits': {'a': [(0.000015,inf),(0.000015,inf),(0.00015,inf),(0.00015,inf)], 'c':inf, 's': False}, 'copyFrom': 'H1r_6563A', 'numComps': 2}),
        ###('O2_7330A', {'Colour': '#7FB3D5', 'Order': 24, 'Filter': 'red', 'minI': 1400, 'maxI': 1520, 'restWavelength': 7329.95, 'ampList': 2, 'zone': 'high', 'sigmaT2': 10.39, 'compLimits': {'a': [(0.000015,inf),(0.000015,inf),(0.00015,inf)], 'c': inf, 's': 0.01}, 'copyFrom': 'H1r_6563A', 'numComps': 2}),

        ###########('Ar3_7136A', {'Colour': '#0E6655', 'Order': 23, 'Filter': 'red', 'minI': 1015, 'maxI': 1080, 'restWavelength': 7135.780, 'ampList': 2, 'zone': 'low', 'sigmaT2': 4.16, 'compLimits': {'c': 0.1, 's': False, 'a': [(0.000015,inf),(0.00015,inf)]}, 'copyFrom': 'H1r_6563A', 'numComps': 2}),
#        ('Ar3_7136Ap', {'Colour': '#0E6655', 'Order': 23, 'Filter': 'red', 'minI': 1015, 'maxI': 1080, 'restWavelength': 7135.780, 'ampList': 2, 'zone': 'low', 'sigmaT2': 4.16, 'compLimits': {'c': inf, 's': 0.001, 'a': [(0.000015,inf),(0.00015,inf)]}, 'copyFrom': 'O3_5007A', 'numComps': 2}),
#        ('Ar3_7136A', {'Colour': '#0E6655', 'Order': 23, 'Filter': 'red', 'minI': 1015, 'maxI': 1080, 'restWavelength': 7135.780, 'ampList': 2, 'zone': 'low', 'sigmaT2': 4.16, 'compLimits': {'c': False, 's': False, 'a': [(0.000015,inf),(0.00015,inf)]}, 'copyFrom': 'Ar3_7136Ap', 'numComps': 2}),
        ####('Ar3_7751A', {'Colour': '#0E6655', 'Order': 27, 'Filter': 'red', 'minI': 712, 'maxI': 780, 'restWavelength': 7751.13, 'ampList': 2, 'zone': 'low', 'sigmaT2': 4.16, 'compLimits': {'c': False, 's': False, 'a': [(0.000015,inf),(0.000015,inf),(0.00015,inf)]}, 'copyFrom': 'H1r_6563A', 'numComps': 2}),

    ])

    # Information for the center, sigma and linear for the low (H-alpha) and high (OIII) zones
    #1026
    centerList = {'low': [1043, 1045,1045,1065], 'high': [1045, 1045, 1144]}
    sigmaList = {'low': [16, 22,18,15], 'high': [15, 25, 15]}
    linSlope = {'low': 0.0, 'high': 0.0}
    linInt = {'low': 0.0761986, 'high': 0.004}

    numComps = {'low': 2, 'high': 3}
    componentLabels = ['Narrow 1', 'Broad', 'Bullet','add']
    componentColours = ['b', 'r','g','k']
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
