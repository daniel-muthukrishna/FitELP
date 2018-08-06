import os
import matplotlib.pyplot as plt
import numpy as np
from uncertainties import ufloat, umath, unumpy
import scripts.constants as constants

constants.init()


def get_bpt_fluxes(rp):
    fluxes = {}
    ionNameKeys = ['NII-6584A', 'H-Alpha', 'OIII-5007A', 'H-Beta']
    if 'H-Alpha' in rp.emProfiles:
        ionNames = ionNameKeys
    else:
        ionNames = ['N2_6584A', 'H1r_6563A', 'O3_5007A', 'H1r_4861A']

    for ionNameKey, ionName in zip(ionNameKeys, ionNames):
        fluxes[ionNameKey] = {}
        fluxes[ionNameKey]['global'] = ufloat(rp.emProfiles[ionName]['globalFlux'], rp.emProfiles[ionName]['globalFluxErr'])
        for i in range(len(rp.emProfiles[ionName]['compFluxList'])):
            fluxes[ionNameKey][rp.componentLabels[i]] = ufloat(rp.emProfiles[ionName]['compFluxList'][i], rp.emProfiles[ionName]['compFluxListErr'][i])

    return fluxes


def calc_bpt_points(rp):
    bptPoints = {}
    try:
        fluxes = get_bpt_fluxes(rp)
    except (KeyError, ValueError):
        print("NII or OIII are not defined")
        bptPoints['global'] = {'x': 0, 'xErr': 0, 'y': 0, 'yErr': 0}
        return bptPoints

    compList = ['global'] + list(fluxes['H-Alpha'].keys())

    for comp in compList:
        ratioNII = umath.log10(fluxes['NII-6584A'][comp] / fluxes['H-Alpha'][comp])
        ratioOIII = umath.log10(fluxes['OIII-5007A'][comp] / fluxes['H-Beta'][comp])
        bptPoints[comp] = {}
        bptPoints[comp]['x'] = ratioNII.nominal_value
        bptPoints[comp]['xErr'] = ratioNII.std_dev
        bptPoints[comp]['y'] = ratioOIII.nominal_value
        bptPoints[comp]['yErr'] = ratioOIII.std_dev

    return bptPoints


def bpt_plot(rpList, rpBptPoints, globalOnly=False):
    plot_lines_and_other_points()

    # PLOT BPT POINTS
    colours = ['g', 'black', 'r', 'c', 'b', 'y', 'm', '#5D6D7E']
    markers = ['o', 'o', 'o', 'o', 'o', 'o', 'o', 'o']
    j = 0
    for i in range(len(rpList)):
        bptPoints = rpBptPoints[i]
        if globalOnly:
            compList = ['global']
        else:
            compList = list(bptPoints.keys())

        for comp in compList:
            x, xErr, y, yErr = bptPoints[comp]['x'], bptPoints[comp]['xErr'], bptPoints[comp]['y'], bptPoints[comp]['yErr']
            if (x, y) != (0, 0):
                label = "{0}_{1}".format(rpList[i].regionName, comp)
                plt.scatter(x, y, marker=markers[j], color=colours[j], label=label)
                plt.errorbar(x=x, y=y, xerr=xErr, yerr=yErr, ecolor=colours[j])
                # plt.annotate(label, xy=(x, y), xytext=(30, 5), textcoords='offset points', ha='right', va='bottom', color=colours[j])
                j += 1

    # PLOT AND SAVE FIGURE
    plt.xlim(-1.5, 0.5)
    plt.ylim(-1, 1.5)
    plt.xlabel(r"$\log(\mathrm{[NII]6584\AA / H\alpha})$")
    plt.ylabel(r"$\log(\mathrm{[OIII]5007\AA / H\beta}$")
    plt.legend()
    plt.savefig(os.path.join(constants.OUTPUT_DIR, 'bpt_plot.png'))
    plt.show()


def plot_lines_and_other_points():
    # PLOT LINES
    plt.figure('BPT Plot')
    # y1: log([OIII]5007/Hbeta) = 0.61 / (log([NII]6584/Halpha) - 0.05) + 1.3  (curve of Kauffmann+03 line)
    # y2: log([OIII]5007/Hbeta) = 0.61 / (log([NII]6584/Halpha) - 0.47) + 1.19    (curve of Kewley+01 line)
    x1 = np.arange(-2, 0.02, 0.01)
    y1 = 0.61 / (x1 - 0.05) + 1.3
    x2 = np.arange(-2, 0.44, 0.01)
    y2 = 0.61 / (x2 - 0.47) + 1.19
    plt.plot(x1, y1, 'k--')
    plt.plot(x2, y2, 'k--')
    # AREA LABELS
    plt.text(-1, -0.8, r'Starburst', fontsize=12)
    plt.text(-0.22, -0.75, r'Transition', fontsize=12)
    plt.text(-0.18, -0.9, r'Objects', fontsize=12)
    plt.text(0.16, -0.5, r'LINERs', fontsize=12)
    plt.text(0.05, 0.55, r'Seyferts', fontsize=12)
    plt.text(-1.46, 1.1, r'Extreme Starburst Line', fontsize=12)

    # OTHER POINTS FROM PAPER
    # Mora et al., 2018 (regions of Arp142)
    hBetaAbs = [0.25,0.33,0.07,0.84,6.32,0.75,0.15,0.82,0.13,0.38,0.78,0.55,0.08,0.21,8.94,4.08,0.52,0.09,0.24,0.07,0.12]
    hBetaErr = [0.11,0.27,0.03,0.19,0.3,0.22,0.09,0.17,0.04,0.17,0.19,0.16,0.06,0.13,0.8,0.26,0.14,0.04,0.14,0.03,0.08]
    oIII5007Abs = [0.35,0.92,0.36,4.73,46.51,1.34,0.21,1.83,0.2,0.68,1.35,0.82,0.18,0.14,6.72,5.03,0.38,0.08,0.36,0.13,0.28]
    oIII5007Err = [0.12,0.25,0.29,2.47,6.98,0.27,0.13,0.15,0.07,0.18,0.23,0.18,0.07,0.08,0.72,0.28,0.06,0.04,0.14,0.07,0.16]
    hAlphaAbs = [0.69,1.02,0.32,3.77,30.11,2.24,0.5,2.56,0.46,1.11,2.46,1.72,0.27,0.62,33,16.6,1.61,0.13,0.62,0.15,0.35]
    hAlphaErr = [0.1,0.25,0.11,0.29,4.52,0.32,0.15,0.34,0.19,0.24,0.35,0.27,0.13,0.19,2.04,1.4,0.2,0.1,0.17,0.08,0.12]
    nII6584Abs = [0.11,0.14,0.07,0.4,2.27,0.36,0.09,0.33,0.1,0.22,0.41,0.36,0.06,0.21,10.64,4.8,0.56,0.03,0.11,0.03,0.04]
    nII6584Err = [0.05,0.09,0.06,0.16,0.24,0.17,0.07,0.13,0.04,0.11,0.16,0.12,0.03,0.12,0.62,0.33,0.14,0.02,0.07,0.03,0.03]
    #
    # Olave et al., 2015 (regions of NGC6845)
    # hBetaAbs = [0.025, 0.033, 0.007, 0.084, 0.632, 0.075, 0.015, 0.082, 0.013, 0.038, 0.078, 0.055, 0.008, 0.021, 0.894, 0.408, 0.052, 0.009, 0.024, 0.007, 0.012]
    # hBetaErr = [0.011, 0.027, 0.003, 0.019, 0.03, 0.022, 0.009, 0.017, 0.004, 0.017, 0.019, 0.016, 0.006, 0.013, 0.08, 0.026, 0.014, 0.004, 0.014, 0.003, 0.008]
    # oIII5007Abs = [0.035, 0.092, 0.036, 0.473, 4.651, 0.134, 0.021, 0.183, 0.02, 0.068, 0.135, 0.082, 0.018, 0.014, 0.672, 0.503, 0.038, 0.008, 0.036, 0.013, 0.028]
    # oIII5007Err = [0.012, 0.025, 0.029, 0.247, 0.698, 0.027, 0.013, 0.015, 0.007, 0.018, 0.023, 0.018, 0.007, 0.008, 0.072, 0.028, 0.006, 0.004, 0.014, 0.007, 0.016]
    # hAlphaAbs = [0.069, 0.102, 0.032, 0.377, 3.011, 0.224, 0.05, 0.256, 0.046, 0.111, 0.246, 0.172, 0.027, 0.062, 3.3, 1.66, 0.161, 0.013, 0.062, 0.015, 0.035]
    # hAlphaErr = [0.01, 0.025, 0.011, 0.029, 0.452, 0.032, 0.015, 0.034, 0.019, 0.024, 0.035, 0.027, 0.013, 0.019, 0.204, 0.14, 0.02, 0.01, 0.017, 0.008, 0.012]
    # nII6584Abs = [0.011, 0.014, 0.007, 0.04, 0.227, 0.036, 0.009, 0.033, 0.01, 0.022, 0.041, 0.036, 0.006, 0.021, 1.064, 0.48, 0.056, 0.003, 0.011, 0.003, 0.004]
    # nII6584Err = [0.005, 0.009, 0.006, 0.016, 0.024, 0.017, 0.007, 0.013, 0.004, 0.011, 0.016, 0.012, 0.003, 0.012, 0.062, 0.033, 0.014, 0.002, 0.007, 0.003, 0.003]
    hBeta = (unumpy.uarray(hBetaAbs, hBetaErr))
    oIII5007 = unumpy.uarray(oIII5007Abs, oIII5007Err)
    hAlpha = unumpy.uarray(hAlphaAbs, hAlphaErr)
    nII6584 = unumpy.uarray(nII6584Abs, nII6584Err)

    ratioNII = unumpy.log10(nII6584/hAlpha)
    ratioOIII = unumpy.log10(oIII5007/hBeta)
    x = unumpy.nominal_values(ratioNII)
    xErr = unumpy.std_devs(ratioNII)
    y = unumpy.nominal_values(ratioOIII)
    yErr = unumpy.std_devs(ratioOIII)

    plt.scatter(x, y, marker='s', color='grey', alpha=0.3, label="Mora et al. 2018")#label="Olave et al. 2015")
    plt.errorbar(x, y, xerr=xErr, yerr=yErr, color='grey', ecolor='grey', elinewidth=0.5, fmt=None, alpha=0.3)
