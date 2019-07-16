import csv
import os
import sys
import numpy as np
from src.label_tools import line_label
from src.read_spectra import GalaxyRegion
from src.fit_line_profiles import FittingProfile, plot_profiles, vel_to_wave, wave_to_vel
from src.make_latex_tables import average_velocities_table_to_latex, halpha_regions_table_to_latex, comp_table_to_latex
from src.bpt_plotting import calc_bpt_points, bpt_plot
import src.constants as constants

constants.init()
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '../scripts'))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '../Input_Galaxy_Region_Information'))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '../Input_Data_Files'))


def calc_vel_dispersion(sigmaObs, sigmaObsError, sigmaTemp2, filter, rp):
    # Assuming negligible error in temp or instrument
    if filter == 'blue':
        sigmaInstr = rp.sigmaInstrBlue
    elif filter == 'red':
        sigmaInstr = rp.sigmaInstrRed

    #Old version (added by Vero)
    # totalSigmaSquared = sigmaObs ** 2 - sigmaInstr ** 2 - sigmaTemp2
    # totalSigmaSquaredError = 2 * sigmaObs * sigmaObsError
    # try:
    #     intrinsic = np.sqrt(totalSigmaSquared)
    #     intrinsicError = 0.5 * totalSigmaSquared ** (-0.5) * totalSigmaSquaredError
    # except ValueError:
    #     "ERROR: INVALID SIGMA"
    #     intrinsic = 0
    #     intrinsicError = 0
    #
    # Last version (added by Vero)
    #if sigmaObs**2 > sigmaTemp2:
        # totalSigmaSquared = sigmaObs ** 2 - sigmaInstr ** 2 - sigmaTemp2
        # totalSigmaSquaredError = 2 * sigmaObs * sigmaObsError
    # else:
    #     totalSigmaSquared = (sigmaInstr + np.sqrt(sigmaTemp2))**2
    #     totalSigmaSquaredError = 0
    # intrinsic = np.sqrt(totalSigmaSquared)
    # intrinsicError = 0.5 * totalSigmaSquared ** (-0.5) * totalSigmaSquaredError
    #
    if sigmaObs**2 > (sigmaTemp2 + sigmaInstr**2):
        totalSigmaSquared = sigmaObs**2 - sigmaInstr**2 - sigmaTemp2
        totalSigmaSquaredError = 2 * sigmaObs * sigmaObsError
    else:
        print("ERROR: INVALID SIGMA")
        totalSigmaSquared = 1e-99
        totalSigmaSquaredError = 0
    intrinsic = np.sqrt(totalSigmaSquared)
    intrinsicError = 0.5 * totalSigmaSquared**(-0.5) * totalSigmaSquaredError

    return intrinsic, intrinsicError


def calc_flux(height, sigmaObs, heightError, sigmaObsError):
    insideSqrt = 2 * np.pi * sigmaObs**2
    insideSqrtError = 2 * sigmaObs * sigmaObsError
    sqrt = np.sqrt(insideSqrt)
    sqrtError = 0.5 * insideSqrt**(-0.5) * insideSqrtError

    calcFlux = height * sqrt
    calcFluxError = calcFlux * np.sqrt((heightError/height)**2 + (sqrtError/sqrt)**2)

    return calcFlux, calcFluxError


def calc_emf(model, numComponents):
    componentFluxes = []
    componentFluxErrors = []
    for i in range(numComponents):
        height = model.params['g%d_height' % (i + 1)].value
        sigmaObs = model.params['g%d_sigma' % (i + 1)].value
        heightError = model.params['g%d_height' % (i + 1)].stderr
        sigmaObsError = model.params['g%d_sigma' % (i + 1)].stderr
        amplitude = model.params['g%d_amplitude' % (i + 1)].value
        amplitudeError = model.params['g%d_amplitude' % (i + 1)].stderr
        calcFlux, calcFluxError = amplitude, amplitudeError

        componentFluxes.append(calcFlux)
        componentFluxErrors.append(calcFluxError)
    componentFluxes = np.array(componentFluxes)
    componentFluxErrors = np.array(componentFluxErrors)
    totalFlux = sum(componentFluxes)
    totalFluxError = np.sqrt(sum([s**2 for s in componentFluxErrors]))

    calcEMF = componentFluxes/sum(componentFluxes) * 100

    return calcEMF, componentFluxes, componentFluxErrors, totalFlux, totalFluxError


def calc_continuum(model, emName, rp):
    continuumList = model.best_values['lin_slope'] * np.array(rp.emProfiles[emName]['centerList']) + model.best_values['lin_intercept']
    globalContinuum = model.best_values['lin_slope'] * np.mean(rp.emProfiles[emName]['centerList']) + model.best_values['lin_intercept']

    return continuumList, globalContinuum


def calc_luminosity(rp):
    if 'H-Alpha' in rp.emProfiles:
        calcLuminosity = 4 * np.pi * rp.emProfiles['H-Alpha']['globalFlux'] * rp.distance**2 / rp.scaleFlux
        calcLuminosityError = 4 * np.pi * rp.distance**2 * rp.emProfiles['H-Alpha']['globalFluxErr'] / rp.scaleFlux
        calcLuminosityError = 4 * np.pi * rp.distance**2 * rp.emProfiles['H-Alpha']['globalFluxErr'] / rp.scaleFlux
    else:
        calcLuminosity = 4 * np.pi * rp.emProfiles['H1r_6563A']['globalFlux'] * rp.distance**2 / rp.scaleFlux
        calcLuminosityError = 4 * np.pi * rp.distance**2 * rp.emProfiles['H1r_6563A']['globalFluxErr'] / rp.scaleFlux
    starFormRate = 5.5e-42 * calcLuminosity
    starFormRateError = 5.5e-42 * calcLuminosityError

    logLuminosity = np.log10(calcLuminosity)
    logLuminosityError = 0.434 * calcLuminosityError/calcLuminosity

    return logLuminosity, logLuminosityError, starFormRate, starFormRateError


def save_measurements(measurementInfo, rp):
    np.set_printoptions(suppress=False)
    componentFluxesDict = dict((el, []) for el in rp.componentLabels)
    componentFluxesDict['global'] = []
    saveFilename = 'component_fluxes.csv'
    with open(os.path.join(constants.OUTPUT_DIR, rp.regionName, saveFilename), 'w') as csvFile:
        writer = csv.writer(csvFile, delimiter=',')
        writer.writerow(["Line_name", "Component", "Flux", "Flux_error"])
        for i in range(len(measurementInfo)):
            emName, components, fluxList, fluxErrList, globalFlux, globalFluxErr, restWave, continuum, globalContinuum = measurementInfo[i]
            for j in range(len(fluxList)):
                eW = abs(fluxList[j]) / continuum[j]
                writer.writerow([emName, components[j], fluxList[j], fluxErrList[j]])
                componentFluxesDict[components[j]].append([emName, fluxList[j], fluxErrList[j], restWave, continuum[j], eW])
            globalEW = abs(globalFlux) / globalContinuum
            componentFluxesDict['global'].append([emName, globalFlux, globalFluxErr, restWave, globalContinuum, globalEW])

    for componentName, fluxInfo in componentFluxesDict.items():
        fluxInfo = sorted(fluxInfo, key=lambda l:l[3])
        with open(os.path.join(constants.OUTPUT_DIR, rp.regionName, "{0}.csv".format(componentName)), 'w') as csvFile:
            writer = csv.writer(csvFile, delimiter=',')
            writer.writerow([componentName])
            writer.writerow(["Line_name", "Flux", "Flux_error"])
            for i in range(len(fluxInfo)):
                emName, flux, fluxErr, restWave, continuum, eW = fluxInfo[i]
                writer.writerow([emName, round(flux, 3), round(fluxErr, 3)])

    for componentName, fluxInfo in componentFluxesDict.items():
        if len(fluxInfo) == 0:
            continue
        fluxInfo = np.array(sorted(fluxInfo, key=lambda l:l[3]))
        with open(os.path.join(constants.OUTPUT_DIR, rp.regionName, "measurements_{0}".format(componentName)), 'w') as csvFile:
            writer = csv.writer(csvFile, delimiter='\t')
            writer.writerow(["# LINE", "ION", "FLUX", "ERR", "CONTINUUM", "EW"])
            fluxInfoIdx = 0
            for i, (getEmName, getRestWave, getIonName) in enumerate(constants.ALL_IONS):
                if getEmName in fluxInfo[:, 0]:# or ((fluxInfoIdx < len(fluxInfo) and getRestWave > fluxInfo[:, 3].astype(float)[fluxInfoIdx] + 1)):
                    # if getEmName in fluxInfo[:, 0]:
                    idx = np.where(fluxInfo[:, 0] == getEmName)[0][0]
                    # else:
                    #     idx = fluxInfoIdx
                    emName, flux, fluxErr, restWave, continuum, eW = fluxInfo[idx]
                    try:
                        flux = np.format_float_scientific(float(flux) / rp.scaleFlux, precision=2)
                        fluxErr = np.format_float_scientific(float(fluxErr) / rp.scaleFlux, precision=2)
                        continuum = np.format_float_scientific(float(continuum) / rp.scaleFlux, precision=2)
                        eW = np.format_float_scientific(float(eW) / rp.scaleFlux, precision=2)
                    except AttributeError:
                        print("Cannot convert floats to scientific notation because you are using an old "
                              "version of Numpy. Please update numpy.")
                        from decimal import Decimal
                        flux = '%.2E' % Decimal(str(float(flux) / rp.scaleFlux))
                        fluxErr = '%.2E' % Decimal(str(float(fluxErr) / rp.scaleFlux))
                        continuum = '%.2E' % Decimal(str(float(continuum) / rp.scaleFlux))
                        eW = '%.2E' % Decimal(str(float(eW) / rp.scaleFlux))
                    ionName, lambdaZero = line_label(emName, float(restWave))
                    ionName = ionName.strip('$').replace("\\", "").replace('mathrm{', "").replace('}', '').split('_')[0]
                    lambdaZero = lambdaZero.strip('$')
                    fluxInfoIdx += 1
                else:
                    emName = getEmName
                    lambdaZero = getRestWave
                    ionName = getIonName
                    flux = 99999.00
                    fluxErr = 9999
                    continuum = 9999
                    eW = 9999

                writer.writerow([lambdaZero, ionName, flux, fluxErr, continuum, eW])
            writer.writerow(["0000", "NO", "0.00", "0", "0", "0.00"])


def fit_profiles(rp, xAxis, initVals):
    galaxyRegion = GalaxyRegion(rp)  # Flux Calibrated
    # galaxyRegion.plot_order(21, filt='red', minIndex=1300, maxIndex=1600, title="")
    # plt.show()

    # Iterate through emission lines
    f = open(os.path.join(constants.OUTPUT_DIR, rp.regionName, "%s_Log.txt" % rp.regionName), "w")
    f.write("LOG INFORMATION FOR %s\n" % rp.regionName)
    f.close()

    for emName, emInfo in rp.emProfiles.items():
        if 'numComps' in emInfo:
            numComps = emInfo['numComps']
        else:
            numComps = rp.numComps[emInfo['zone']]
            rp.emProfiles[emName]['numComps'] = numComps

        print("------------------ %s : %s ----------------" % (rp.regionName, emName))
        f = open(os.path.join(constants.OUTPUT_DIR, rp.regionName, "%s_Log.txt" % rp.regionName), "a")
        f.write("------------------ %s : %s ----------------\n" % (rp.regionName, emName))
        f.close()
        wave, flux, waveError, fluxError = galaxyRegion.mask_emission_line(emInfo['Order'], filt=emInfo['Filter'],
                                                                           minIndex=emInfo['minI'],
                                                                           maxIndex=emInfo['maxI'])

        if len(emName.split('+')) > 1:
            fittingProfile = FittingProfile(wave, flux, restWave=emInfo['restWavelength'], lineName=emName, fluxError=fluxError, zone=emInfo['zone'], rp=rp, xAxis=xAxis)
            model, comps = fittingProfile.multiple_close_emission_lines(lineNames=emInfo['Lines'], cListInit=rp.centerList[emInfo['zone']], sListInit=rp.sigmaList[emInfo['zone']], lS=rp.linSlope[emInfo['zone']], lI=rp.linInt[emInfo['zone']])

            for line in emInfo['Lines']:
                lineShort = line.replace('-', '')
                rp.emProfiles[line]['centerList'] = []
                rp.emProfiles[line]['sigmaList'] = []
                rp.emProfiles[line]['ampListNew'] = []
                for idx in range(numComps):
                    rp.emProfiles[line]['centerList'].append(model.best_values['g{0}{1}_center'.format(lineShort, (idx + 1))])
                    rp.emProfiles[line]['sigmaList'].append(model.best_values['g{0}{1}_sigma'.format(lineShort, (idx + 1))])
                    rp.emProfiles[line]['ampListNew'].append(model.best_values['g{0}{1}_amplitude'.format(lineShort, (idx + 1))])

        else:
            fittingProfile = FittingProfile(wave, flux, restWave=emInfo['restWavelength'], lineName=emName, fluxError=fluxError, zone=emInfo['zone'], rp=rp, xAxis=xAxis, initVals=initVals)

            if emInfo['copyFrom'] is None:
                model, comps = fittingProfile.lin_and_multi_gaussian(numComps, rp.centerList[emInfo['zone']], rp.sigmaList[emInfo['zone']], emInfo['ampList'], rp.linSlope[emInfo['zone']], rp.linInt[emInfo['zone']], emInfo['compLimits'])
                rp.emProfiles[emName]['centerList'] = []
                rp.emProfiles[emName]['sigmaList'] = []
                rp.emProfiles[emName]['ampListNew'] = []
                for idx in range(numComps):
                    rp.emProfiles[emName]['centerList'].append(model.best_values['g%d_center' % (idx + 1)])
                    rp.emProfiles[emName]['sigmaList'].append(model.best_values['g%d_sigma' % (idx + 1)])
                    rp.emProfiles[emName]['ampListNew'].append(model.best_values['g%d_amplitude' % (idx + 1)])
            else:
                if type(emInfo['copyFrom']) is list:
                    copyAmpList, copyCenterList, copySigmaList = [], [], []
                    for copyIdx in range(len(emInfo['copyFrom'])):
                        copyAmpList.append(rp.emProfiles[emInfo['copyFrom'][copyIdx]]['ampListNew'][copyIdx])
                        copyCenterList.append(rp.emProfiles[emInfo['copyFrom'][copyIdx]]['centerList'][copyIdx])
                        copySigmaList.append(rp.emProfiles[emInfo['copyFrom'][copyIdx]]['sigmaList'][copyIdx])
                else:
                    copyAmpList = rp.emProfiles[emInfo['copyFrom']]['ampListNew']
                    copyCenterList = rp.emProfiles[emInfo['copyFrom']]['centerList']
                    copySigmaList = rp.emProfiles[emInfo['copyFrom']]['sigmaList']

                if type(rp.emProfiles[emName]['ampList']) is list:
                    ampListInit = emInfo['ampList']
                else:
                    ampListInit = [float(a) * emInfo['ampList'] for a in copyAmpList]  # Multiply each copyAmplitude by number

                if xAxis == 'wave':
                    velCopyCenterList = wave_to_vel(rp.emProfiles[emInfo['copyFrom']]['restWavelength'], wave=np.array(copyCenterList), flux=0)[0]
                    velCopySigmaList = wave_to_vel(rp.emProfiles[emInfo['copyFrom']]['restWavelength'], wave=np.array(copySigmaList), flux=0, delta=True)[0]
                    velAmpListInit = wave_to_vel(rp.emProfiles[emInfo['copyFrom']]['restWavelength'], wave=0, flux=np.array(ampListInit))[1]
                else:
                    velCopyCenterList, velCopySigmaList, velAmpListInit = copyCenterList, copySigmaList, ampListInit
                model, comps = fittingProfile.lin_and_multi_gaussian(numComps, velCopyCenterList, velCopySigmaList, velAmpListInit, rp.linSlope[emInfo['zone']], rp.linInt[emInfo['zone']], emInfo['compLimits'])

                rp.emProfiles[emName]['centerList'] = []
                rp.emProfiles[emName]['sigmaList'] = []
                rp.emProfiles[emName]['ampListNew'] = []
                for idx in range(numComps):
                    rp.emProfiles[emName]['centerList'].append(model.best_values['g%d_center' % (idx + 1)])
                    rp.emProfiles[emName]['sigmaList'].append(model.best_values['g%d_sigma' % (idx + 1)])
                    rp.emProfiles[emName]['ampListNew'].append(model.best_values['g%d_amplitude' % (idx + 1)])
        rp.emProfiles[emName]['model'] = model
        rp.emProfiles[emName]['comps'] = comps
        rp.emProfiles[emName]['x'] = fittingProfile.x
        rp.emProfiles[emName]['flux'] = fittingProfile.flux
        rp.emProfiles[emName]['fluxError'] = fittingProfile.fluxError

    emProfiles = rp.emProfiles
    return emProfiles


class RegionCalculations(object):
    def __init__(self, rp, xAxis='vel', initVals='vel'):
        """ Compute kinematics of a region.

        Parameters
        ----------
        rp : RegionParameters object
            An instance of the RegionParameters class.
        xAxis : str
            Plots the x axis in velocity space if xAxis='vel' and in wavelength space if xAxis='wave'. Default is 'vel'.
        initVals : str
            Interprets the initial values from all the parameters (i.e. center, sigma, amplitude)
            as velocities if initVals='vel' or as wavelengths if initVals='wave'
        """

        zoneNames = {zone: [] for zone in rp.centerList.keys()}
        ampListAll = []
        allModelComponents = []
        measurementInfo = []

        emProfiles = fit_profiles(rp, xAxis, initVals)

        for emName, emInfo in emProfiles.items():
            if len(emName.split('+')) > 1:
                continue

            model = emProfiles[emName]['model']
            comps = emProfiles[emName]['comps']
            numComps = emProfiles[emName]['numComps']
            x = rp.emProfiles[emName]['x']
            flux = rp.emProfiles[emName]['flux']
            fluxError = rp.emProfiles[emName]['fluxError']

            ion1, lambdaZero1 = line_label(emName, emInfo['restWavelength'])
            emLabel = (ion1 + ' ' + lambdaZero1)
            zoneNames[emInfo['zone']].append(emName)

            rp.emProfiles[emName]['plotInfo'] = [emName, x, flux, model.best_fit, emInfo['Colour'], comps, emLabel]

            ampComponentList = []
            o = model
            eMFList, fluxList, fluxListErr, globalFlux, globalFluxErr = calc_emf(model, numComps)
            continuumList, globalContinuum = calc_continuum(model, emName, rp)
            measurementInfo.append((emName, rp.componentLabels, fluxList, fluxListErr, globalFlux, globalFluxErr, emInfo['restWavelength'], continuumList, globalContinuum))
            rp.emProfiles[emName]['globalFlux'] = globalFlux
            rp.emProfiles[emName]['globalFluxErr'] = globalFluxErr
            rp.emProfiles[emName]['compFluxList'] = fluxList
            rp.emProfiles[emName]['compFluxListErr'] = fluxListErr
            rp.emProfiles[emName]['sigIntList'] = []
            for idx in range(numComps):
                ampComponentList.append(round(rp.emProfiles[emName]['ampListNew'][idx], 7))

                sigma = o.params['g%d_sigma' % (idx + 1)].value
                sigmaError = o.params['g%d_sigma' % (idx + 1)].stderr
                vel = o.params['g%d_center' % (idx + 1)].value
                velError = o.params['g%d_center' % (idx + 1)].stderr
                if xAxis == 'wave':
                    sigma, sigmaError, velError = wave_to_vel(emInfo['restWavelength'], wave=np.array((sigma, sigmaError, velError)), flux=0, delta=True)[0]
                    vel = wave_to_vel(emInfo['restWavelength'], wave=vel, flux=0)[0]

                sigInt, sigIntErr = calc_vel_dispersion(sigma, sigmaError, emInfo['sigmaT2'], emInfo['Filter'], rp)
                rp.emProfiles[emName]['sigIntList'].append(sigInt)
                if hasattr(rp, 'showSystemicVelocity') and rp.showSystemicVelocity is True:
                    tableVel = vel - rp.systemicVelocity
                else:
                    tableVel = vel
                tableLine = [lambdaZero1, ion1, rp.componentLabels[idx], "%.1f $\pm$ %.1f" % (tableVel, velError), r"%.1f $\pm$ %.1f" % (sigInt, sigIntErr), "%.2f $\pm$ %.3f" % (fluxList[idx], fluxListErr[idx]), round(eMFList[idx], 1), "%.2f $\pm$ %.3f" % (globalFlux, globalFluxErr)]
                if idx != 0:
                    tableLine[0:2] = ['', '']
                    tableLine[-1] = ''
                allModelComponents.append(tableLine)
            allModelComponents.append([''] * len(tableLine))
            ampListAll.append([emName, ampComponentList, emInfo, emName])

        save_measurements(measurementInfo, rp)
        # Create Component Table
        comp_table_to_latex(allModelComponents, rp, paperSize='a4', orientation='portrait', longTable=True)

        print("------------ List all Amplitudes  %s ----------" % rp.regionName)
        for ampComps in ampListAll:
            ampCompsList, emInfo, emName = ampComps[1:4]
            print("# ('" + emName + "', {'Colour': '" + emInfo['Colour'] + "', " + "'Order': " + str(emInfo['Order']) + ", " + "'Filter': '" + emInfo['Filter'] + "', " + "'minI': " + str(emInfo['minI']) + ", " + "'maxI': " + str(emInfo['maxI']) + ", " + "'restWavelength': " + str(emInfo['restWavelength']) + ", " + "'ampList': " + str(ampCompsList) + ", " + "'zone': '" + emInfo['zone'] + "', " + "'sigmaT2': " + str(emInfo['sigmaT2']) + ", " + "'compLimits': " + str(emInfo['compLimits']) + ", " + "'copyFrom': '" + str(emInfo['copyFrom']) + ", " + "'numComps': " + str(emInfo['numComps']) + "'}),")

        print("------------ Component information %s ------------"  % rp.regionName)
        for mod in allModelComponents:
            print(mod)

        self.bptPoints = calc_bpt_points(rp, plot_type='n')
        self.bptPoints_s = calc_bpt_points(rp, plot_type='s')
        self.bptPoints_o = calc_bpt_points(rp, plot_type='o')
        self.bptPoints_p = calc_bpt_points(rp, plot_type='p')

        ratioNII, ratioNIIErr, ratioOIII, ratioOIIIErr = self.bptPoints['global']['x'], self.bptPoints['global']['xErr'], self.bptPoints['global']['y'], self.bptPoints['global']['yErr']
        luminosity, luminosityError, sfr, sfrError = calc_luminosity(rp)

        self.lineInArray = [rp.regionName, "%.2f $\pm$ %.3f" % (sfr, sfrError), "%.1f $\pm$ %.3f" % (luminosity, luminosityError), "%.2f $\pm$ %.3f" % (ratioNII, ratioNIIErr), "%.2f $\pm$ %.3f" % (ratioOIII, ratioOIIIErr)]
