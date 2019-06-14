import os
import matplotlib.pyplot as plt
import numpy as np
import warnings
from uncertainties import ufloat, umath, unumpy
import scripts.constants as constants

constants.init()


def get_bpt_fluxes(rp, plot_type='n'):
    fluxes = {}
    if 'H-Alpha' in rp.emProfiles:
        if plot_type == 's':
            ionNameKeys = ['H-Alpha', 'OIII-5007A', 'H-Beta', 'SII-6717A']
        elif plot_type == 'o':
            ionNameKeys = ['H-Alpha', 'OIII-5007A', 'H-Beta', 'OI-6300A']
        elif plot_type == 'p':
            ionNameKeys = ['H-Alpha', 'SII-6717A', 'H-Alpha','NII-6584A']
        else:
            ionNameKeys = ['NII-6584A', 'H-Alpha', 'OIII-5007A', 'H-Beta']
        ionNames = ionNameKeys
    else:
        if plot_type == 's':
            ionNameKeys = ['H-Alpha', 'OIII-5007A', 'H-Beta', 'SII-6717A']
            ionNames = ['H1r_6563A', 'O3_5007A', 'H1r_4861A', 'S2_6717A']
        elif plot_type == 'o':
            ionNameKeys = ['H-Alpha', 'OIII-5007A', 'H-Beta', 'OI-6300A']
            ionNames = ['H1r_6563A', 'O3_5007A', 'H1r_4861A', 'O1_6300A']
        elif plot_type == 'p':
            ionNameKeys = ['H-Alpha', 'SII-6717A', 'H-Alpha','NII-6584A']
            ionNames = ['H1r_6563A', 'S2_6717A', 'H1r_6563A', 'N2_6584A']
        else:
            ionNameKeys = ['NII-6584A', 'H-Alpha', 'OIII-5007A', 'H-Beta']
            ionNames = ['N2_6584A', 'H1r_6563A', 'O3_5007A', 'H1r_4861A']

    for ionNameKey, ionName in zip(ionNameKeys, ionNames):
        fluxes[ionNameKey] = {}
        fluxes[ionNameKey]['global'] = ufloat(rp.emProfiles[ionName]['globalFlux'], rp.emProfiles[ionName]['globalFluxErr'])
        for i in range(len(rp.emProfiles[ionName]['compFluxList'])):
            fluxes[ionNameKey][rp.componentLabels[i]] = ufloat(rp.emProfiles[ionName]['compFluxList'][i], rp.emProfiles[ionName]['compFluxListErr'][i])

    return fluxes


def calc_bpt_points(rp, plot_type='n'):
    bptPoints = {}
    try:
        fluxes = get_bpt_fluxes(rp, plot_type)
    except (KeyError, ValueError):
        print("Ion not defined for BPT plot:", plot_type)
        bptPoints['global'] = {'x': 0, 'xErr': 0, 'y': 0, 'yErr': 0}
        return bptPoints

    if plot_type == 'n':
        xNumerator = fluxes['NII-6584A']
        xDenominator = fluxes['H-Alpha']
        yNumerator = fluxes['OIII-5007A']
        yDenominator = fluxes['H-Beta']
    elif plot_type == 's':
        xNumerator = fluxes['SII-6717A']
        xDenominator = fluxes['H-Alpha']
        yNumerator = fluxes['OIII-5007A']
        yDenominator = fluxes['H-Beta']
    elif plot_type == 'o':
        xNumerator = fluxes['OI-6300A']
        xDenominator = fluxes['H-Alpha']
        yNumerator = fluxes['OIII-5007A']
        yDenominator = fluxes['H-Beta']
    elif plot_type == 'p':
        xNumerator = fluxes['SII-6717A']
        xDenominator = fluxes['H-Alpha']
        yNumerator = fluxes['NII-6584A']
        yDenominator = fluxes['H-Alpha']
    else:
        warnings.warn("Invalid BPT plot_type {}, using plot_type 'n' instead.".format(plot_type))
        xNumerator = fluxes['NII-6584A']

    compList = ['global'] + list(fluxes['H-Alpha'].keys())
    for comp in compList:
        ratioX = umath.log10(xNumerator[comp] / xDenominator[comp])
        ratioY = umath.log10(yNumerator[comp] / yDenominator[comp])
        bptPoints[comp] = {}
        bptPoints[comp]['x'] = ratioX.nominal_value
        bptPoints[comp]['xErr'] = ratioX.std_dev
        bptPoints[comp]['y'] = ratioY.nominal_value
        bptPoints[comp]['yErr'] = ratioY.std_dev

    return bptPoints


def bpt_plot(rpList, rpBptPoints, globalOnly=False, plot_type='n'):
    if plot_type == 'n':
        bpt_plot_n(rpList, rpBptPoints, globalOnly)
    elif plot_type == 's':
        bpt_plot_s(rpList, rpBptPoints, globalOnly)
    elif plot_type == 'o':
        bpt_plot_o(rpList, rpBptPoints, globalOnly)
    elif plot_type == 'p':
        bpt_plot_p(rpList, rpBptPoints, globalOnly)
    else:
        warnings.warn("Invalid BPT plot_type {}, using plot_type 'n' instead.".format(plot_type))
        bpt_plot_n(rpList, rpBptPoints, globalOnly)


def bpt_plot_n(rpList, rpBptPoints, globalOnly=False, compNames={'Narrow1': 'N1', 'Narrow2': 'N2', 'Broad1': 'B1', 'Broad': 'B'}):
    plot_lines_and_other_points_n()

    # PLOT BPT POINTS
    colours = ['b', 'r', 'g', 'm', 'c', 'violet', 'y', '#5D6D7E']
    markers = ['o', 's', 'x', 'p', '*', 'D', '8', '>']

    for i in range(len(rpList)):
        bptPoints = rpBptPoints[i]
        if globalOnly:
            compList = ['global']
        else:
            compList = list(bptPoints.keys())

        for j, comp in enumerate(compList):
            x, xErr, y, yErr = bptPoints[comp]['x'], bptPoints[comp]['xErr'], bptPoints[comp]['y'], bptPoints[comp]['yErr']
            if (x, y) != (0, 0):
                try:
                    label = "{0}_{1}".format(rpList[i].regionName, compNames[comp])
                except KeyError:
                    label = "{0}_{1}".format(rpList[i].regionName, comp)
                plt.scatter(x, y, marker=markers[i], label=label)#, color=colours[j])
                plt.errorbar(x=x, y=y, xerr=xErr, yerr=yErr)#, ecolor=colours[j])
                # plt.annotate(label, xy=(x, y), xytext=(30, 5), textcoords='offset points', ha='right', va='bottom', color=colours[j], fontsize=8)

    # PLOT AND SAVE FIGURE
    plt.xlim(-1.5, 0.5)
    plt.ylim(-1, 1.5)
    plt.xlabel(r"$\log(\mathrm{[NII]6584\AA / H\alpha})$")
    plt.ylabel(r"$\log(\mathrm{[OIII]5007\AA / H\beta}$")
    plt.legend(fontsize=9)
    plt.savefig(os.path.join(constants.OUTPUT_DIR, 'bpt_plot_N.png'))


def bpt_plot_s(rpList, rpBptPoints, globalOnly=False, compNames={'Narrow1': 'N1', 'Narrow2': 'N2', 'Broad1': 'B1', 'Broad': 'B'}):
    plot_lines_and_other_points_s()

    # PLOT BPT POINTS
    colours = ['b', 'r', 'g', 'm', 'c', 'violet', 'y', '#5D6D7E']
    markers = ['o', 's', 'x', 'p', '*', 'D', '8', '>']

    for i in range(len(rpList)):
        bptPoints = rpBptPoints[i]
        if globalOnly:
            compList = ['global']
        else:
            compList = list(bptPoints.keys())

        for j, comp in enumerate(compList):
            x, xErr, y, yErr = bptPoints[comp]['x'], bptPoints[comp]['xErr'], bptPoints[comp]['y'], bptPoints[comp]['yErr']
            if (x, y) != (0, 0):
                try:
                    label = "{0}_{1}".format(rpList[i].regionName, compNames[comp])
                except KeyError:
                    label = "{0}_{1}".format(rpList[i].regionName, comp)
                plt.scatter(x, y, marker=markers[i], label=label)#, color=colours[j])
                plt.errorbar(x=x, y=y, xerr=xErr, yerr=yErr)#, ecolor=colours[j])
                # plt.annotate(label, xy=(x, y), xytext=(30, 5), textcoords='offset points', ha='right', va='bottom', color=colours[j], fontsize=8)

    # PLOT AND SAVE FIGURE
    plt.xlim(-1.5, 0.5)
    plt.ylim(-1, 1.5)
    plt.xlabel(r"$\log(\mathrm{[SII]6716\AA / H\alpha})$")
    plt.ylabel(r"$\log(\mathrm{[OIII]5007\AA / H\beta}$")
    plt.legend(fontsize=9)
    plt.savefig(os.path.join(constants.OUTPUT_DIR, 'bpt_plot_S.png'))


def bpt_plot_o(rpList, rpBptPoints, globalOnly=False, compNames={'Narrow1': 'N1', 'Narrow2': 'N2', 'Broad1': 'B1', 'Broad': 'B'}):
    plot_lines_and_other_points_o()

    # PLOT BPT POINTS
    colours = ['b', 'r', 'g', 'm', 'c', 'violet', 'y', '#5D6D7E']
    markers = ['o', 's', 'x', 'p', '*', 'D', '8', '>']

    for i in range(len(rpList)):
        bptPoints = rpBptPoints[i]
        if globalOnly:
            compList = ['global']
        else:
            compList = list(bptPoints.keys())

        for j, comp in enumerate(compList):
            x, xErr, y, yErr = bptPoints[comp]['x'], bptPoints[comp]['xErr'], bptPoints[comp]['y'], bptPoints[comp]['yErr']
            if (x, y) != (0, 0):
                try:
                    label = "{0}_{1}".format(rpList[i].regionName, compNames[comp])
                except KeyError:
                    label = "{0}_{1}".format(rpList[i].regionName, comp)
                plt.scatter(x, y, marker=markers[i], label=label)#, color=colours[j])
                plt.errorbar(x=x, y=y, xerr=xErr, yerr=yErr)#, ecolor=colours[j])
                # plt.annotate(label, xy=(x, y), xytext=(30, 5), textcoords='offset points', ha='right', va='bottom', color=colours[j], fontsize=8)

    # PLOT AND SAVE FIGURE
    plt.xlim(-1.5, 0.5)
    plt.ylim(-0.5, 1.5)
    plt.xlabel(r"$\log(\mathrm{[OI]6300\AA / H\alpha})$")
    plt.ylabel(r"$\log(\mathrm{[OIII]5007\AA / H\beta}$")
    plt.legend(fontsize=9)
    plt.savefig(os.path.join(constants.OUTPUT_DIR, 'bpt_plot_O.png'))


def bpt_plot_p(rpList, rpBptPoints, globalOnly=False, compNames={'Narrow1': 'N1', 'Narrow2': 'N2', 'Broad1': 'B1', 'Broad': 'B'}):
    plot_lines_and_other_points_p()

    # PLOT BPT POINTS
    colours = ['b', 'r', 'g', 'm', 'c', 'violet', 'y', '#5D6D7E']
    markers = ['o', 's', 'x', 'p', '*', 'D', '8', '>']

    for i in range(len(rpList)):
        bptPoints = rpBptPoints[i]
        if globalOnly:
            compList = ['global']
        else:
            compList = list(bptPoints.keys())

        for j, comp in enumerate(compList):
            x, xErr, y, yErr = bptPoints[comp]['x'], bptPoints[comp]['xErr'], bptPoints[comp]['y'], bptPoints[comp]['yErr']
            if (x, y) != (0, 0):
                try:
                    label = "{0}_{1}".format(rpList[i].regionName, compNames[comp])
                except KeyError:
                    label = "{0}_{1}".format(rpList[i].regionName, comp)
                plt.scatter(x, y, marker=markers[i], label=label)#, color=colours[j])
                plt.errorbar(x=x, y=y, xerr=xErr, yerr=yErr)#, ecolor=colours[j])
                # plt.annotate(label, xy=(x, y), xytext=(30, 5), textcoords='offset points', ha='right', va='bottom', color=colours[j], fontsize=8)

    # PLOT AND SAVE FIGURE
    # plt.xlim(-1.5, 0.5)
    # plt.ylim(-0.5, 1.5)
    plt.xlabel(r"$\log(\mathrm{[SII]6717\AA / H\alpha})$")
    plt.ylabel(r"$\log(\mathrm{[NII]6584\AA / H\alpha}$")
    plt.legend(fontsize=9)
    plt.savefig(os.path.join(constants.OUTPUT_DIR, 'bpt_plot_P.png'))


def plot_lines_and_other_points_n():
    # PLOT LINES
    plt.figure('BPT Plot OIII/NII')
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
    # Olave et al., 2015 (regions of NGC6845)
    hBetaAbs = [0.025, 0.033, 0.007, 0.084, 0.632, 0.075, 0.015, 0.082, 0.013, 0.038, 0.078, 0.055, 0.008, 0.021, 0.894, 0.408, 0.052, 0.009, 0.024, 0.007, 0.012]
    hBetaErr = [0.011, 0.027, 0.003, 0.019, 0.03, 0.022, 0.009, 0.017, 0.004, 0.017, 0.019, 0.016, 0.006, 0.013, 0.08, 0.026, 0.014, 0.004, 0.014, 0.003, 0.008]
    oIII5007Abs = [0.035, 0.092, 0.036, 0.473, 4.651, 0.134, 0.021, 0.183, 0.02, 0.068, 0.135, 0.082, 0.018, 0.014, 0.672, 0.503, 0.038, 0.008, 0.036, 0.013, 0.028]
    oIII5007Err = [0.012, 0.025, 0.029, 0.247, 0.698, 0.027, 0.013, 0.015, 0.007, 0.018, 0.023, 0.018, 0.007, 0.008, 0.072, 0.028, 0.006, 0.004, 0.014, 0.007, 0.016]
    hAlphaAbs = [0.069, 0.102, 0.032, 0.377, 3.011, 0.224, 0.05, 0.256, 0.046, 0.111, 0.246, 0.172, 0.027, 0.062, 3.3, 1.66, 0.161, 0.013, 0.062, 0.015, 0.035]
    hAlphaErr = [0.01, 0.025, 0.011, 0.029, 0.452, 0.032, 0.015, 0.034, 0.019, 0.024, 0.035, 0.027, 0.013, 0.019, 0.204, 0.14, 0.02, 0.01, 0.017, 0.008, 0.012]
    nII6584Abs = [0.011, 0.014, 0.007, 0.04, 0.227, 0.036, 0.009, 0.033, 0.01, 0.022, 0.041, 0.036, 0.006, 0.021, 1.064, 0.48, 0.056, 0.003, 0.011, 0.003, 0.004]
    nII6584Err = [0.005, 0.009, 0.006, 0.016, 0.024, 0.017, 0.007, 0.013, 0.004, 0.011, 0.016, 0.012, 0.003, 0.012, 0.062, 0.033, 0.014, 0.002, 0.007, 0.003, 0.003]
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

    plt.scatter(x, y, marker='s', color='grey', alpha=0.3, label="Olave et al. 2015")
    plt.errorbar(x, y, xerr=xErr, yerr=yErr, color='grey', ecolor='grey', elinewidth=0.5, fmt='none', alpha=0.3)


def plot_lines_and_other_points_s():
    # https://sites.google.com/site/agndiagnostics/home/bpt

    # PLOT LINES
    plt.figure('BPT Plot OIII/SII')
    # y1: log([OIII]/Hb) = 0.72 / (log([SII]/Ha) - 0.32) + 1.30    (main AGN line)
    # y2: log([OIII]/Hb) = 1.89 log([SII]/Ha) + 0.76   (LINER/Sy2 line)
    x1 = np.arange(-2, 0.02, 0.01)
    y1 = 0.72 / (x1 - 0.32) + 1.30
    x2 = np.arange(-0.314613, 0.44, 0.01)
    y2 = 1.89 * x2 + 0.76
    plt.plot(x1, y1, 'k--')
    plt.plot(x2, y2, 'k--')

    # AREA LABELS
    plt.text(-1, -0.8, r'HII-Like Objects', fontsize=12)
    plt.text(0.1, 0., r'LINERs', fontsize=12)
    plt.text(-0.5, 0.55, r'AGNs', fontsize=12)


def plot_lines_and_other_points_o():
    # PLOT LINES
    plt.figure('BPT Plot OIII/OI')
    # y1: log([OIII]/Hb) = 0.73 / (log([OI]/Ha) + 0.59) + 1.33    (main AGN line)
    # y2: log([OIII]/Hb) = 1.18 log([OI]/Ha) + 1.30  (LINER/Sy2 line)
    x1 = np.arange(-2, 0.25, 0.01)
    y1 = 0.73 / (x1 - 0.59) + 1.33
    x2 = np.arange(-0.53, 0.44, 0.01)
    y2 = 1.18 * x2 + 1.30
    plt.plot(x1, y1, 'k--')
    plt.plot(x2, y2, 'k--')

    # AREA LABELS
    plt.text(-1, 0., r'HII-Like Objects', fontsize=12)
    plt.text(0., 0.5, r'LINERs', fontsize=12)
    plt.text(-0.6, 1., r'AGNs', fontsize=12)


def plot_lines_and_other_points_p():
    # PLOT LINES
    plt.figure('BPT Plot SII/HI')
