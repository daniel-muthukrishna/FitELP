import csv
import os
import sys
import matplotlib.pyplot as plt
import numpy as np
from label_tools import line_label
from read_spectra import GalaxyRegion
from fit_line_profiles import EmissionLineProfile, FittingProfile, plot_profiles
from make_latex_tables import average_velocities_table_to_latex, halpha_regions_table_to_latex, comp_table_to_latex
from bpt_plotting import calc_bpt_point, bpt_plot

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '../scripts'))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '../Input_Galaxy_Region_Information'))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '../Input_Data_Files'))

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../Output_Files')


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

def column(matrix, i):
    columnList = []
    for row in matrix:
        if i < len(row):
            columnList.append(row[i])

    return columnList


def calc_average_velocities(rpList):
    regionsAllLines = []
    componentLabelsAllEmLines = []

    for rp in rpList:
        numCompsFromVelCalcList = []
        centers = []
        sigmas = []
        for emName, emInfo in rp.emProfiles.items():
            if emName in rp.emLinesForAvgVelCalc:
                if 'numComps' in emInfo.keys():
                    numComps = emInfo['numComps']
                else:
                    zone = emInfo['zone']
                    numComps = rp.numComps[zone]
                numCompsFromVelCalcList.append(numComps)
                centers.append(emInfo['centerList'][0:numComps])
                sigmas.append(emInfo['sigIntList'][0:numComps])

        avgCentres = []
        avgSigmas = []
        stdCentres = []
        stdSigmas = []
        for i in range(10):  # Max number of numComps (number of rows in table)
            componentCentres = column(centers, i)
            componentSigmas = column(sigmas, i)
            if componentCentres != []:
                avgCentres.append(np.mean(componentCentres))
                stdCentres.append(np.std(componentCentres))
            else:
                avgCentres.append(None)
                stdCentres.append(None)
            if componentSigmas != []:
                avgSigmas.append(np.mean(componentSigmas))
                stdSigmas.append(np.std(componentSigmas))
            else:
                avgSigmas.append(None)
                stdSigmas.append(None)

        regionLines = []
        componentLabels = []
        for i in range(10):
            try:
                regionLines.append([r"%.1f $\pm$ %.1f" % (avgCentres[i], stdCentres[i]), r"%.1f $\pm$ %.1f" % (avgSigmas[i], stdSigmas[i])])
                componentLabels.append(rp.componentLabels[i])
            except (IndexError, TypeError):
                regionLines.append(["-", "-"])
                componentLabels.append("")

        regionsAllLines.append(regionLines)
        componentLabelsAllEmLines.append(componentLabels)

    allLinesInArray = []
    for i in range(10):
        lineInArray = [rp.componentLabels[i]] if i < numComps else ['']
        for j in range(len(regionsAllLines)):
            regionLine = regionsAllLines[j]
            componentLabel = componentLabelsAllEmLines[j]
            lineInArray += regionLine[i]

        for entry in lineInArray:
            if entry == '' or entry == '-':
                pass
            else:
                allLinesInArray.append(lineInArray)
                break

    return allLinesInArray


def calc_luminosity(rp):
    if 'H-Alpha' in rp.emProfiles:
        calcLuminosity = 4 * np.pi * rp.emProfiles['H-Alpha']['globalFlux'] * rp.distance**2 / rp.scaleFlux
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
    componentFluxesDict = dict((el, []) for el in rp.componentLabels)
    componentFluxesDict['global'] = []
    saveFilename = 'component_fluxes.csv'
    with open(os.path.join(OUTPUT_DIR, rp.regionName, saveFilename), 'w') as csvFile:
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
        with open(os.path.join(OUTPUT_DIR, rp.regionName, "{0}.csv".format(componentName)), 'w') as csvFile:
            writer = csv.writer(csvFile, delimiter=',')
            writer.writerow([componentName])
            writer.writerow(["Line_name", "Flux", "Flux_error"])
            for i in range(len(fluxInfo)):
                emName, flux, fluxErr, restWave, continuum, eW = fluxInfo[i]
                writer.writerow([emName, round(flux, 3), round(fluxErr, 3)])

    for componentName, fluxInfo in componentFluxesDict.items():
        fluxInfo = sorted(fluxInfo, key=lambda l:l[3])
        with open(os.path.join(OUTPUT_DIR, rp.regionName, "measurements_{0}".format(componentName)), 'w') as csvFile:
            writer = csv.writer(csvFile, delimiter='\t')
            writer.writerow(["# LINE", "ION", "Flux", "Err", "CONTINUUM", "EW"])
            for i in range(len(fluxInfo)):
                emName, flux, fluxErr, restWave, continuum, eW = fluxInfo[i]
                ionName, lambdaZero = line_label(emName, restWave)
                ionName = ionName.strip('$').replace("\\", "").replace('mathrm{', "").replace('}', '').split('_')[0]
                lambdaZero = lambdaZero.strip('$')
                writer.writerow([lambdaZero, ionName, round(flux, 3), round(fluxErr, 3), continuum, eW])


class RegionCalculations(object):
    def __init__(self, rp):
        galaxyRegion = GalaxyRegion(rp)  # Flux Calibrated
        # galaxyRegion.plot_order(21, filt='red', minIndex=1300, maxIndex=1600, title="")
        # plt.show()

        zoneNames = {zone: [] for zone in rp.centerList.keys()}
        ampListAll = []
        allModelComponents = []
        #fluxListInfo = []
        measurementInfo = []
        # Iterate through emission lines
        f = open(os.path.join(OUTPUT_DIR, rp.regionName, "%s_Log.txt" % rp.regionName), "w")
        f.write("LOG INFORMATION FOR %s\n" % rp.regionName)
        f.close()
        for emName, emInfo in rp.emProfiles.items():
            if 'numComps' in emInfo:
                numComps = emInfo['numComps']
            else:
                numComps = rp.numComps[emInfo['zone']]
                rp.emProfiles[emName]['numComps'] = numComps

            print("------------------ %s : %s ----------------" %(rp.regionName, emName))
            f = open(os.path.join(OUTPUT_DIR, rp.regionName, "%s_Log.txt" % rp.regionName), "a")
            f.write("------------------ %s : %s ----------------\n" % (rp.regionName, emName))
            f.close()
            wave1, flux1, wave1Error, flux1Error = galaxyRegion.mask_emission_line(emInfo['Order'], filt=emInfo['Filter'], minIndex=emInfo['minI'], maxIndex=emInfo['maxI'])
            emLineProfile = EmissionLineProfile(wave1, flux1, flux1Error, restWave=emInfo['restWavelength'], lineName=emName, rp=rp)
            vel1, flux1, flux1Error = emLineProfile.vel, emLineProfile.flux, emLineProfile.fluxError  # In velocity instead of wavelength units
            fittingProfile = FittingProfile(vel1, flux1, restWave=emInfo['restWavelength'], lineName=emName, fluxError=flux1Error, zone=emInfo['zone'], rp=rp)
            ion1, lambdaZero1 = line_label(emName, emInfo['restWavelength'])
            emLabel = (ion1 + ' ' + lambdaZero1)

            if emInfo['copyFrom'] is None:
                model1, comps = fittingProfile.lin_and_multi_gaussian(numComps, rp.centerList[emInfo['zone']], rp.sigmaList[emInfo['zone']], emInfo['ampList'], rp.linSlope[emInfo['zone']], rp.linInt[emInfo['zone']], emInfo['compLimits'])
                rp.emProfiles[emName]['centerList'] = []
                rp.emProfiles[emName]['sigmaList'] = []
                rp.emProfiles[emName]['ampList'] = []
                for idx in range(numComps):
                    rp.emProfiles[emName]['centerList'].append(model1.best_values['g%d_center' % (idx + 1)])
                    rp.emProfiles[emName]['sigmaList'].append(model1.best_values['g%d_sigma' % (idx + 1)])
                    rp.emProfiles[emName]['ampList'].append(model1.best_values['g%d_amplitude' % (idx + 1)])
            else:
                if type(emInfo['copyFrom']) is list:
                    copyAmpList, copyCenterList, copySigmaList = [], [], []
                    for copyIdx in range(len(emInfo['copyFrom'])):
                        copyAmpList.append(rp.emProfiles[emInfo['copyFrom'][copyIdx]]['ampList'][copyIdx])
                        copyCenterList.append(rp.emProfiles[emInfo['copyFrom'][copyIdx]]['centerList'][copyIdx])
                        copySigmaList.append(rp.emProfiles[emInfo['copyFrom'][copyIdx]]['sigmaList'][copyIdx])
                else:
                    copyAmpList = rp.emProfiles[emInfo['copyFrom']]['ampList']
                    copyCenterList = rp.emProfiles[emInfo['copyFrom']]['centerList']
                    copySigmaList = rp.emProfiles[emInfo['copyFrom']]['sigmaList']

                if type(rp.emProfiles[emName]['ampList']) is list:
                    ampListInit = emInfo['ampList']
                else:
                    ampListInit = [float(a) / emInfo['ampList'] for a in copyAmpList]  #Divide each copyAmplitude by number

                model1, comps = fittingProfile.lin_and_multi_gaussian(numComps, copyCenterList, copySigmaList, ampListInit, rp.linSlope[emInfo['zone']], rp.linInt[emInfo['zone']], emInfo['compLimits'])
                rp.emProfiles[emName]['centerList'] = []
                rp.emProfiles[emName]['sigmaList'] = []
                rp.emProfiles[emName]['ampList'] = []
                for idx in range(numComps):
                    rp.emProfiles[emName]['centerList'].append(model1.best_values['g%d_center' % (idx + 1)])
                    rp.emProfiles[emName]['sigmaList'].append(model1.best_values['g%d_sigma' % (idx + 1)])
                    rp.emProfiles[emName]['ampList'].append(model1.best_values['g%d_amplitude' % (idx + 1)])

            zoneNames[emInfo['zone']].append(emName)
            rp.emProfiles[emName]['plotInfo'] = [emName, vel1, flux1, model1.best_fit, emInfo['Colour'], comps, emLabel]

        #Print Amplitudes
            ampComponentList = []
            o = model1
            eMFList, fluxList, fluxListErr, globalFlux, globalFluxErr = calc_emf(model1, numComps)
            continuumList, globalContinuum = calc_continuum(model1, emName, rp)
            measurementInfo.append((emName, rp.componentLabels, fluxList, fluxListErr, globalFlux, globalFluxErr, emInfo['restWavelength'], continuumList, globalContinuum))
            rp.emProfiles[emName]['globalFlux'] = globalFlux
            rp.emProfiles[emName]['globalFluxErr'] = globalFluxErr
            rp.emProfiles[emName]['sigIntList'] = []
            for idx in range(numComps):
                ampComponentList.append(round(rp.emProfiles[emName]['ampList'][idx], 7))
                sigInt, sigIntErr = calc_vel_dispersion(o.params['g%d_sigma' % (idx + 1)].value, o.params['g%d_sigma' % (idx + 1)].stderr, emInfo['sigmaT2'], emInfo['Filter'], rp)
                rp.emProfiles[emName]['sigIntList'].append(sigInt)
                tableLine = [lambdaZero1, ion1, rp.componentLabels[idx], "%.1f $\pm$ %.1f" % (o.params['g%d_center' % (idx + 1)].value, o.params['g%d_center' % (idx + 1)].stderr), r"%.1f $\pm$ %.1f" % (sigInt, sigIntErr), "%.1f $\pm$ %.2f" % (fluxList[idx], fluxListErr[idx]), round(eMFList[idx], 1), "%.1f $\pm$ %.2f" % (globalFlux, globalFluxErr)]
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

        self.bptPoint = calc_bpt_point(rp)
        ratioNII, ratioNIIErr, ratioOIII, ratioOIIIErr = self.bptPoint
        luminosity, luminosityError, sfr, sfrError = calc_luminosity(rp)

        self.lineInArray = [rp.regionName, "%.2f $\pm$ %.3f" % (sfr, sfrError), "%.1f $\pm$ %.3f" % (luminosity, luminosityError), "%.2f $\pm$ %.3f" % (ratioNII, ratioNIIErr), "%.2f $\pm$ %.3f" % (ratioOIII, ratioOIIIErr)]

        # Combined Plots
        # plot_profiles(zoneNames['low'], rp, nameForComps='SII-6717A', title=rp.regionName + " Low Zone Profiles")
        # plot_profiles(zoneNames['high'], rp, nameForComps='NeIII-3868A', title=rp.regionName + " High Zone Profiles")
        plot_profiles(['OIII-5007A', 'H-Alpha', 'H-Beta', 'NII-6584A', 'SII-6717A'], rp, nameForComps='SII-6717A', title=rp.regionName + ' Strongest Emission Lines', sortedIndex=[0, 1, 2, 3, 4])

        # plot_profiles(['H-Beta_Blue', 'H-Beta_Red'], rp, nameForComps='H-Beta_Blue', title=rp.regionName + ' H-Beta comparison')
        # plot_profiles(['OIII-4959A_Blue', 'OIII-4959A_Red'], rp, nameForComps='OIII-4959A_Red', title=rp.regionName + ' OIII-4959 comparison')
        # plot_profiles(['OIII-5007A', 'NeIII-3868A'], rp, nameForComps='NeIII-3868A', title=' ')
        # plot_profiles(['OIII-5007A', 'NeIII-3868A'], rp, nameForComps='OIII-5007A', title='')


if __name__ == '__main__':

    from profile_info_Arp314_NED02_off import RegionParameters as Arp314_NED02_offParams
    from profile_info_Arp314_NED02 import RegionParameters as Arp314_NED02Params
    from profile_info_Obj1 import RegionParameters as Obj1
    # from Mrk600A import RegionParameters as Mrk600AParams
    from Mrk600B import RegionParameters as Mrk600B05Params
    # from IIZw33KnotB05 import RegionParameters as IIZw33KnotBParams
    # from profile_info_NGC6845_Region7 import RegionParameters as NGC6845Region7Params
    # from profile_info_NGC6845_Region26 import RegionParameters as NGC6845Region26Params
    # from profile_info_NGC6845_Region26_Counts import RegionParameters as NGC6845Region26Params

    regionsParameters = [Arp314_NED02Params, Obj1] # NGC6845Region7Params, NGC6845Region26Params]#, HCG31_AParams, HCG31_ACParams]#, Arp314_NED02_offParams, HCG31_CParams]

    regionArray = []
    bptPoints = []
    for regParam in regionsParameters:
        region = RegionCalculations(regParam)
        regionArray.append(region.lineInArray)
        bptPoints.append(region.bptPoint)

    bpt_plot(regionsParameters, bptPoints)
    halpha_regions_table_to_latex(regionArray, paperSize='a4', orientation='portrait', longTable=False)
    average_velocities_table_to_latex(regionsParameters, paperSize='a4', orientation='landscape', longTable=False)

    plt.show()
