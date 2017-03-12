import os
import numpy as np
from lmfit.models import GaussianModel, LinearModel
from lmfit import Parameters
import matplotlib.pyplot as plt
import astropy.units as u
from specutils.io import read_fits

SpOfLi = 300000.  # km/s


def read_spectra(filename, scaleFlux):
    """ Reads spectra from input FITS File
    Stores the wavelength (in Angstroms) in a vector 'x'
    and the fluxes scaled by 10**14 in a vector 'y'
    x and y are an array of the wavelengths and fluxes of each of the orders"""
    x = []
    y = []
    spectra = read_fits.read_fits_spectrum1d(filename)
    for spectrum in spectra:
        x.append(spectrum.dispersion / u.angstrom)
        y.append(spectrum.flux * scaleFlux)
    x = np.array(x)
    y = np.array(y)

    return x, y


def vel_dispersion(sigmaObs, sigmaObsError, sigmaTemp2, filter, rp):
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


def calculate_flux(height, sigmaObs, heightError, sigmaObsError):
    insideSqrt = 2 * np.pi * sigmaObs**2
    insideSqrtError = 2 * sigmaObs * sigmaObsError
    sqrt = np.sqrt(insideSqrt)
    sqrtError = 0.5 * insideSqrt**(-0.5) * insideSqrtError

    calcFlux = height * sqrt
    calcFluxError = calcFlux * np.sqrt((heightError/height)**2 + (sqrtError/sqrt)**2)

    return calcFlux, calcFluxError


def calculate_em_f(model, numComponents):
    componentFluxes = []
    componentFluxErrors = []
    for i in range(numComponents):
        height = model.params['g%d_height' % (i + 1)].value
        sigmaObs = model.params['g%d_sigma' % (i + 1)].value
        heightError = model.params['g%d_height' % (i + 1)].stderr
        sigmaObsError = model.params['g%d_sigma' % (i + 1)].stderr
        amplitude = model.params['g%d_amplitude' % (i + 1)].value
        amplitudeError = model.params['g%d_amplitude' % (i + 1)].stderr
        calcFlux, calcFluxError = amplitude, amplitudeError  # calculate_flux(height, sigmaObs, heightError, sigmaObsError)

        componentFluxes.append(calcFlux)
        componentFluxErrors.append(calcFluxError)
    componentFluxes = np.array(componentFluxes)
    componentFluxErrors = np.array(componentFluxErrors)
    totalFlux = sum(componentFluxes)
    totalFluxError = np.sqrt(sum([s**2 for s in componentFluxErrors]))

    calcEMF = componentFluxes/sum(componentFluxes) * 100

    return calcEMF, componentFluxes, componentFluxErrors, totalFlux, totalFluxError


def line_label(emLineName, emRestWave, rp):
    if emLineName in ['H-Alpha', 'H-Beta', 'H-Gamma', 'H-Delta']:
        lambdaZero = '$%s$' % str(int(round(emRestWave)))
        if emLineName == 'H-Alpha':
            ion = r"$\mathrm{H}\alpha$"
        elif emLineName == 'H-Beta':
            ion = r"$\mathrm{H}\beta$"
        elif emLineName == 'H-Gamma':
            ion = r"$\mathrm{H}\gamma$"
        elif emLineName == 'H-Delta':
            ion = r"$\mathrm{H}\delta$"
    elif emLineName == 'H-Beta_Blue':
        lambdaZero = '$%s$' % str(int(round(emRestWave)))
        ion = r"$\mathrm{H}\beta$ - Blue"
    elif emLineName == 'H-Beta_Red':
        lambdaZero = '$%s$' % str(int(round(emRestWave)))
        ion = r"$\mathrm{H}\beta$ - Red"
    elif 'He' in emLineName:
        lambdaZero = '$%s$' % emLineName.split('-')[1][:-1]
        ion = r"$\mathrm{%s}$" % emLineName.split('-')[0]
    else:
        lambdaZero = '$%s$' % emLineName.split('-')[1][:-1]
        ion = r"$\mathrm{[%s]}$" % emLineName.split('-')[0]

    return ion, lambdaZero


def calc_average_velocities(rpList):
    regionsAllLines = []
    numCompsList = [min(rp.numComps['low'], rp.numComps['high']) for rp in rpList]
    for rp in rpList:
        numComps = min(rp.numComps['low'], rp.numComps['high'])
        centres = []
        sigmas = []
        for emName, emInfo in rp.emProfiles.items():
            if emName in rp.emLinesForAvgVelCalc:
                centres.append(emInfo['centerList'][0:numComps])
                sigmas.append(emInfo['sigIntList'][0:numComps])
        centres = np.array(centres)
        sigmas = np.array(sigmas)
        avgCentres = np.zeros(numComps)
        avgSigmas = np.zeros(numComps)
        stdCentres = np.zeros(numComps)
        stdSigmas = np.zeros(numComps)
        for i in range(numComps):
            avgCentres[i] = np.mean(centres[:,i])
            avgSigmas[i] = np.mean(sigmas[:, i])
            stdCentres[i] = np.std(centres[:, i])
            stdSigmas[i] = np.std(sigmas[:, i])

        regionLines = []
        for i in range(max(numCompsList)):
            try:
                regionLines.append([r"%.1f $\pm$ %.1f" % (avgCentres[i], stdCentres[i]), r"%.1f $\pm$ %.1f" % (avgSigmas[i], stdSigmas[i])])
            except IndexError:
                regionLines.append(["-", "-"])

        regionsAllLines.append(regionLines)

    allLinesInArray = []
    for i in range(numComps):
        lineInArray = [rp.componentLabels[i]]
        for regionLine in regionsAllLines:
            lineInArray += regionLine[i]

        allLinesInArray.append(lineInArray)

    return allLinesInArray


def average_velocities_table_to_latex(rpList, directory="."):
    saveFileName = 'AverageVelocitiesTable'
    velArray = calc_average_velocities(rpList)
    regionHeadings = ['']
    headings = ['']
    headingUnits = ['']
    for rp in rpList:
        regionHeadings += ["\multicolumn{2}{c}{%s}" % rp.regionName]
        headings += [r'$\mathrm{v_r}$', r'$\mathrm{\sigma}$']
        headingUnits += [r'$\mathrm{(km \ s^{-1})}$', r'$\mathrm{(km \ s^{-1})}$']

    headingLines = [regionHeadings, headings, headingUnits]
    caption = "Average radial velocities and velocity dispersions for all regions"
    nCols = len(headings)
    centering = 'l' + 'c' * (nCols-1)
    table_to_latex(velArray, headingLines, saveFileName, directory, caption, centering)


def halpha_regions_table_to_latex(regionInfoArray, directory="."):
    saveFileName = 'RegionInfo'
    headings = [r'Region Name', r'SFR', r'$\mathrm{log(L(H}\alpha))$', r'$\mathrm{log([NII]/H}\alpha)$', r'$\mathrm{log([OIII]/H}\beta)$']
    headingUnits = ['', r'$(\mathrm{M_{\odot} \ yr^{-1}})$', '', '', '']
    headingLines = [headings, headingUnits]
    caption = 'Region Information'
    nCols = len(headings)
    centering = 'l' + 'c' * (nCols-1)
    table_to_latex(regionInfoArray, headingLines, saveFileName, directory, caption, centering)


def comp_table_to_latex(componentArray, rp):
    saveFileName = 'ComponentTable'
    directory = rp.regionName
    headings = [r'$\mathrm{\lambda_0}$', r'$\mathrm{Ion}$', r'$\mathrm{Comp.}$', r'$\mathrm{v_r}$',
                r'$\mathrm{\sigma_{int}}$', r'$\mathrm{Flux}$', r'$\mathrm{EM_f}$', r'$\mathrm{GlobalFlux}$']
    headingUnits = [r'$(\mathrm{\AA})$', '', '', r'$(\mathrm{km \ s^{-1}})$',
                    r'$(\mathrm{km \ s^{-1}})$', r'$(\mathrm{10^{-14} \ erg \ s^{-1} \ cm^{-2} \ \AA^{-1}})$',
                    '', r'$(\mathrm{10^{-14} \ erg \ s^{-1} \ cm^{-2} \ \AA^{-1}})$']
    headingLines = [headings, headingUnits]
    caption = rp.regionName
    nCols = len(headings)
    centering = 'lllccccc'
    table_to_latex(componentArray, headingLines, saveFileName, directory, caption, centering)


def table_to_latex(tableArray, headingLines, saveFileName, directory, caption, centering):
    texFile = open(directory + '/' + saveFileName + '.tex', 'w')
    texFile.write('\\documentclass{article}\n')
    texFile.write('\\usepackage[a3paper, portrait, margin=0.5in]{geometry}\n')
    texFile.write('\\usepackage{booktabs}\n')
    # texFile.write('\\usepackage[LGRgreek]{mathastext}\n')
    # texFile.write('\\usepackage[utf8]{inputenc}\n')
    texFile.write('\\begin{document}\n')
    texFile.write('\n')
    texFile.write('\\begin{table}[tbp]\n')
    texFile.write('\\centering\n')
    texFile.write('\\begin{tabular}{%s}\n' % (centering))
    texFile.write('\\hline\n')
    for heading in headingLines:
        texFile.write(' & '.join(str(e) for e in heading) + ' \\\\ \n')
    texFile.write('\\hline\n')
    for line in tableArray:
        texFile.write(' & '.join(str(e) for e in line) + ' \\\\ \n')
    texFile.write('\\hline\n')
    texFile.write('\\end{tabular}\n')
    texFile.write('\\caption{%s}\n' % caption)
    texFile.write('\\end{table}\n')
    texFile.write('\n')
    texFile.write('\\end{document}\n')

    texFile.close()

    os.system("pdflatex ./'" + directory + "'/" + saveFileName + ".tex")
    if directory != ".":
        os.system("mv " + saveFileName + ".pdf ./'" + directory + "'")
        os.system("rm " + saveFileName + ".*")


def calc_luminosity(rp):
    calcLuminosity = 4 * np.pi * rp.emProfiles['H-Alpha']['globalFlux'] * rp.distance**2 / rp.scaleFlux
    calcLuminosityError = 4 * np.pi * rp.distance**2 * rp.emProfiles['H-Alpha']['globalFluxErr'] / rp.scaleFlux
    starFormRate = 5.5e-42 * calcLuminosity
    starFormRateError = 5.5e-42 * calcLuminosityError

    logLuminosity = np.log10(calcLuminosity)
    logLuminosityError = 0.434 * calcLuminosityError/calcLuminosity

    return logLuminosity, logLuminosityError, starFormRate, starFormRateError


def plot_profiles(lineNames, rp, nameForComps='', title='', sortedIndex=None):
    plt.figure(title)
    ax = plt.subplot(1, 1, 1)
    plt.title(title)  # Recombination Emission Lines")
    plt.xlabel(r"$\mathrm{Velocity \ (km s^{-1}}$)")
    plt.ylabel(r"$\mathrm{Flux \ (10^{-14} \ erg \ s^{-1} \ cm^{-2} \ \AA^{-1}})$")
    for i in range(len(lineNames)):
        name, x, y, mod, col, comps, lab = rp.emProfiles[lineNames[i]]['plotInfo']
        ax.plot(x, y, color=col, label=lab)
        ax.plot(x, mod, color=col, linestyle='--')
        if name == nameForComps:
            for idx in range(rp.numComps[lineNames[i]['zone']]):
                plt.plot(x, comps['g%d_' % (idx + 1)] + comps['lin_'], color=rp.componentColours[idx], linestyle=':')
    plt.xlim(rp.plottingXRange)
    if sortedIndex is not None:
        handles, labels = ax.get_legend_handles_labels()
        handles2 = [handles[idx] for idx in sortedIndex]
        labels2 = [labels[idx] for idx in sortedIndex]
        ax.legend(handles2, labels2)
    else:
        ax.legend()
    plt.savefig(rp.regionName + '/' + title.strip(' ') + '.png')


class GalaxyRegion(object):
    def __init__(self, rp):
        """ x is wavelength arrays, y is flux arrays """
        self.xBlue, self.yBlue = read_spectra(rp.blueSpecFile, rp.scaleFlux)
        self.xRed, self.yRed = read_spectra(rp.redSpecFile, rp.scaleFlux)
        self.rp = rp
        if rp.blueSpecError is None:
            self.xBlueError, self.yBlueError = (None, None)
        else:
            self.xBlueError, self.yBlueError = read_spectra(rp.blueSpecError, rp.scaleFlux)
        if rp.redSpecError is None:
            self.xRedError, self.yRedError = (None, None)
        else:
            self.xRedError, self.yRedError = read_spectra(rp.redSpecError, rp.scaleFlux)

        if not os.path.exists(rp.regionName + '/'):
            os.makedirs(rp.regionName + '/')

    def plot_order(self, orderNum, filt='red', minIndex=0, maxIndex=-1, title=''):
        """Plots the wavelength vs flux for a particular order. orderNum starts from 0"""
        orderNum -= 1
        x, y, xE, yE = self._filter_argument(filt)

        fig = plt.figure(self.rp.regionName + " Order Plot " + title)
        plt.title(title)
        ax1 = fig.add_subplot(111)
        ax1.plot(x[orderNum][minIndex:maxIndex], y[orderNum][minIndex:maxIndex], label='Spectrum')
        # ax1Ticks = ax1.get_xticks()
        # ax2Ticks = ax1Ticks
        # ax2.set_xticks(ax2Ticks)
        # ax2.set_xbound(ax1.get_xbound())
        # ax2.set_xticklabels("%.2f" % z for z in (x[orderNum][minIndex:maxIndex][t] for t in ax2Ticks[:-2]))
        #ax2.plot(y[orderNum][minIndex:maxIndex])
        if yE is not None:
            pass #plt.plot(xE[orderNum][minIndex:maxIndex], yE[orderNum][minIndex:maxIndex], label='Spectrum Error')
        plt.legend()
        plt.xlabel("Wavelength ($\AA$)")
        plt.ylabel(r"$\mathrm{Flux \ (10^{-14} \ erg \ s^{-1} \ cm^{-2} \ \AA^{-1}})$")
        plt.savefig(self.rp.regionName + '/' + title)

    def mask_emission_line(self, orderNum, filt='red', minIndex=0, maxIndex=-1):
        orderNum -= 1
        x, y, xE, yE = self._filter_argument(filt)
        xMask, yMask = x[orderNum][minIndex:maxIndex], y[orderNum][minIndex:maxIndex]
        if yE is None:
            xEMask, yEMask = None, None
        else:
            xEMask, yEMask = xE[orderNum][minIndex:maxIndex], yE[orderNum][minIndex:maxIndex]

        return xMask, yMask, xEMask, yEMask

    def _filter_argument(self, filt):
        try:
            if filt == 'red':
                x, y, xE, yE = self.xRed, self.yRed, self.xRedError, self.yRedError
            elif filt == 'blue':
                x, y, xE, yE = self.xBlue, self.yBlue, self.xBlueError, self.yBlueError

            return x, y, xE, yE

        except NameError:
            print("Error: Invalid argument. Choose 'red' or 'blue' for the filter argument")
            exit()


class EmissionLineProfile(object):
    def __init__(self, wave, flux, rp, restWave=6562.82, lineName=''):
        """wave and flux are for vectors representing only the given emission line
        labWave is the wavelength of the emission line if it were at rest (stationary)
        default is for H-alpha emission line"""
        self.restWave = restWave
        self.lineName = lineName
        self.wave = wave
        self.flux = flux
        self.vel = self._velocity(wave)
        self.rp = rp

    def _velocity(self, wave):
        return ((wave - self.restWave) / self.restWave) * SpOfLi #(const.c/(u.m/u.s)) / 1000

    def plot_emission_line(self, xaxis='vel', title=''):
        """Choose whether the x axis is 'vel' or 'wave'"""
        plt.figure(self.rp.regionName + self.lineName + title)
        plt.title(self.lineName + title)
        if xaxis == 'wave':
            plt.plot(self.wave, self.flux)
            plt.xlabel("Wavelength ($\AA$)")
        elif xaxis == 'vel':
            plt.plot(self.vel, self.flux)
            plt.xlabel("Velocity ($\mathrm{km \ s}^{-1}$)")
        plt.ylabel("Flux")
        plt.savefig(self.rp.regionName + '/' + self.lineName + title)


class FittingProfile(object):
    def __init__(self, vel, flux, restWave, lineName, zone, rp, fluxError=None):
        """The input vel and flux must be limited to a single emission line profile"""
        self.vel = vel
        self.flux = flux
        self.fluxError = fluxError
        self.restWave = restWave
        self.lineName = lineName
        self.zone = zone
        self.weights = self._weights()
        self.rp = rp

        self.linGaussParams = Parameters()

    def _weights(self):
        if self.fluxError is None:
            return None
        else:
            fluxErrorCR = self.fluxError# - self.continuum
            return 1./fluxErrorCR

    def _get_amplitude(self, numOfComponents, modelFit):
        amplitudeTotal = 0.
        for i in range(numOfComponents):
            amplitudeTotal = amplitudeTotal + modelFit.best_values['g%d_amplitude' % (i+1)]
        print "Amplitude Total is %f" % amplitudeTotal
        amplitudeFinal = (amplitudeTotal/SpOfLi) * self.restWave
        print "Amplitude Final is %f" % amplitudeFinal

        return amplitudeFinal

    def _gaussian_component(self, pars, prefix, c, s, a, limits):
        """Fits a gaussian with given parameters.
        pars is the lmfit Parameters for the fit, prefix is the label of the gaussian, c is the center, s is sigma,
        a is amplitude. Returns the Gaussian model"""
        varyCentre = True
        varySigma = True
        varyAmp = True

        if limits['c'] == False:
            varyCentre = False
            cMin, cMax = -np.inf, np.inf
        else:
            cMin = c - c*limits['c']
            cMax = c + c*limits['c']

        if limits['s'] == False:
            varySigma = False
            sMin, sMax = -np.inf, np.inf
        else:
            sMin = s - s * limits['s']
            sMax = s + s * limits['s']

        if limits['a'] == False:
            varyAmp = False
            aMin, aMax = -np.inf, np.inf
        else:
            aMin = a - a * limits['a']
            aMax = a + a * limits['a']

        g = GaussianModel(prefix=prefix)
        pars.update(g.make_params())
        pars[prefix+'center'].set(c, min=cMin, max=cMax, vary=varyCentre)
        pars[prefix + 'sigma'].set(s, min=sMin, max=sMax, vary=varySigma)
        pars[prefix + 'amplitude'].set(a, min=aMin, max=aMax, vary=varyAmp)

        return g

    def lin_and_multi_gaussian(self, numOfComponents, cList, sList, aList, lS, lI, limits):
        """All lists should be the same length"""
        gList = []

        lin = LinearModel(prefix='lin_')
        self.linGaussParams = lin.guess(self.flux, x=self.vel)
        self.linGaussParams.update(lin.make_params())
        self.linGaussParams['lin_slope'].set(lS, vary=True)
        self.linGaussParams['lin_intercept'].set(lI, vary=True)

        for i in range(numOfComponents):
            if type(limits['c']) is list:
                cLimit = limits['c'][i]
            else:
                cLimit = limits['c']
            if type(limits['s']) is list:
                sLimit = limits['s'][i]
            else:
                sLimit = limits['s']
            if type(limits['a']) is list:
                aLimit = limits['a'][i]
            else:
                aLimit = limits['a']
            lims = {'c': cLimit, 's': sLimit, 'a': aLimit}
            gList.append(self._gaussian_component(self.linGaussParams,'g%d_' % (i+1), cList[i], sList[i], aList[i], lims))
        gList = np.array(gList)
        mod = lin + gList.sum()

        init = mod.eval(self.linGaussParams, x=self.vel)
        out = mod.fit(self.flux, self.linGaussParams, x=self.vel, weights=self.weights)
        f = open(self.rp.regionName + '/' + "%s_Log.txt" % self.rp.regionName, "a")
        print "######## %s %s Linear and Multi-gaussian Model ##########\n" % (self.rp.regionName, self.lineName)
        print (out.fit_report())
        f.write("######## %s %s Linear and Multi-gaussian Model ##########\n" % (self.rp.regionName, self.lineName))
        f.write(out.fit_report())
        f.close()
        components = out.eval_components()

        ion, lambdaZero = line_label(self.lineName, self.restWave, self.rp)
        plt.figure("%s %s %s" % (self.rp.regionName, ion, lambdaZero))
        plt.title("%s %s" % (ion, lambdaZero))
        plt.xlabel(r"$\mathrm{Velocity \ (km s^{-1}}$)")
        plt.ylabel(r"$\mathrm{Flux \ (10^{-14} \ erg \ s^{-1} \ cm^{-2} \ \AA^{-1}})$")
        plt.plot(self.vel, self.flux, label='Data')
        for i in range(numOfComponents):
            labelComp = self.rp.componentLabels  # 'g%d_' % (i+1)
            plt.plot(self.vel, components['g%d_' % (i+1)]+components['lin_'], color=self.rp.componentColours[i], linestyle=':', label=labelComp[i])
        # plt.plot(self.vel, components['lin_'], label='lin_')
        plt.plot(self.vel, out.best_fit, color='black', linestyle='--', label='Fit')
        # plt.plot(self.vel, init, label='init')
        plt.xlim(self.rp.plottingXRange)
        plt.legend(loc='upper left')
        plt.savefig(self.rp.regionName + '/' + self.lineName + " %d Component Linear-Gaussian Model" % numOfComponents)

        self._get_amplitude(numOfComponents, out)

        return out, components


class RegionCalculations(object):
    def __init__(self, rp):
        galaxyRegion = GalaxyRegion(rp)  # Flux Calibrated
        # galaxyRegion.plot_order(21, filt='red', minIndex=1300, maxIndex=1600, title="")
        # plt.show()

        zoneNames = {'low': [], 'high': []}
        ampListAll = []
        allModelComponents = []
        # Iterate through emission lines
        f = open(rp.regionName + '/' + "%s_Log.txt" % rp.regionName, "w")
        f.write("LOG INFORMATION FOR %s\n" % rp.regionName)
        f.close()
        for emName, emInfo in rp.emProfiles.items():
            numComps = rp.numComps[emInfo['zone']]
            print "------------------ %s : %s ----------------" %(rp.regionName, emName)
            f = open(rp.regionName + '/' + "%s_Log.txt" % rp.regionName, "a")
            f.write("------------------ %s : %s ----------------\n" % (rp.regionName, emName))
            f.close()
            wave1, flux1, wave1Error, flux1Error = galaxyRegion.mask_emission_line(emInfo['Order'], filt=emInfo['Filter'], minIndex=emInfo['minI'], maxIndex=emInfo['maxI'])
            emLineProfile = EmissionLineProfile(wave1, flux1, restWave=emInfo['restWavelength'], lineName=emName, rp=rp)
            vel1 = emLineProfile.vel
            fittingProfile = FittingProfile(vel1, flux1, restWave=emInfo['restWavelength'], lineName=emName, fluxError=flux1Error, zone=emInfo['zone'], rp=rp)
            ion1, lambdaZero1 = line_label(emName, emInfo['restWavelength'], rp)
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
                if type(rp.emProfiles[emName]['ampList']) is list:
                    ampListInit = emInfo['ampList']
                else:
                    ampListInit = [a / emInfo['ampList'] for a in rp.emProfiles[emInfo['copyFrom']]['ampList']]  #Multiply elements in list by 3
                model1, comps = fittingProfile.lin_and_multi_gaussian(numComps, rp.emProfiles[emInfo['copyFrom']]['centerList'], rp.emProfiles[emInfo['copyFrom']]['sigmaList'], ampListInit, rp.linSlope[emInfo['zone']], rp.linInt[emInfo['zone']], emInfo['compLimits'])
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
            eMFList, fluxList, fluxListErr, globalFlux, globalFluxErr = calculate_em_f(model1, numComps)
            rp.emProfiles[emName]['globalFlux'] = globalFlux
            rp.emProfiles[emName]['globalFluxErr'] = globalFluxErr
            rp.emProfiles[emName]['sigIntList'] = []
            for idx in range(numComps):
                ampComponentList.append(round(rp.emProfiles[emName]['ampList'][idx], 7))
                sigInt, sigIntErr = vel_dispersion(o.params['g%d_sigma' % (idx + 1)].value, o.params['g%d_sigma' % (idx + 1)].stderr, emInfo['sigmaT2'], emInfo['Filter'], rp)
                rp.emProfiles[emName]['sigIntList'].append(sigInt)
                tableLine = [lambdaZero1, ion1, rp.componentLabels[idx], "%.1f $\pm$ %.1f" % (o.params['g%d_center' % (idx + 1)].value, o.params['g%d_center' % (idx + 1)].stderr), r"%.1f $\pm$ %.1f" % (sigInt, sigIntErr), "%.1f $\pm$ %.2f" % (fluxList[idx], fluxListErr[idx]), round(eMFList[idx], 1), "%.1f $\pm$ %.2f" % (globalFlux, globalFluxErr)]
                if idx != 0:
                    tableLine[0:2] = ['', '']
                    tableLine[-1] = ''
                allModelComponents.append(tableLine)
            allModelComponents.append([''] * len(tableLine))
            ampListAll.append([emName, ampComponentList, emInfo, emName])
        comp_table_to_latex(allModelComponents, rp)

        print "------------ List all Amplitudes  %s ----------" % rp.regionName
        for ampComps in ampListAll:
            #print ampComps[0], ampComps[1]
            ampCompsList, emInfo, emName = ampComps[1:4]
            print "# ('" + emName + "', {'Colour': '" + emInfo['Colour'] + "', " + "'Order': " + str(emInfo['Order']) + ", " + "'Filter': '" + emInfo['Filter'] + "', " + "'minI': " + str(emInfo['minI']) + ", " + "'maxI': " + str(emInfo['maxI']) + ", " + "'restWavelength': " + str(emInfo['restWavelength']) + ", " + "'ampList': " + str(ampCompsList) + ", " + "'zone': '" + emInfo['zone'] + "', " + "'sigmaT2': " + str(emInfo['sigmaT2']) + ", " + "'compLimits': " + str(emInfo['compLimits']) + ", " + "'copyFrom': '" + str(emInfo['copyFrom']) + "'}),"

        print "------------ Component information %s ------------"  % rp.regionName
        for mod in allModelComponents:
            print mod

        try:
            # ratioNII = (rp.emProfiles['NII-6584A']['globalFlux'] + rp.emProfiles['NII-6548A']['globalFlux']) / (rp.emProfiles['H-Alpha']['globalFlux'])
            # ratioOIII = (rp.emProfiles['OIII-5007A']['globalFlux'] + rp.emProfiles['OIII-4959A']['globalFlux']) / (rp.emProfiles['H-Beta_Blue']['globalFlux'])
            ratioNII = (rp.emProfiles['NII-6584A']['globalFlux']) /( rp.emProfiles['H-Alpha']['globalFlux'])
            ratioOIII = (rp.emProfiles['OIII-5007A']['globalFlux']) / (rp.emProfiles['H-Beta_Blue']['globalFlux'])
            ratioNII = np.log10(ratioNII)
            ratioOIII = np.log10(ratioOIII)
        except KeyError:
            ratioNII, ratioOIII = (0, 0)
            print "NII or OIII are not defined"

        luminosity, luminosityError, sfr, sfrError = calc_luminosity(rp)

        self.lineInArray = [rp.regionName, "%.2f $\pm$ %.2f" % (sfr, sfrError), "%.1f $\pm$ %.3f" % (luminosity, luminosityError), round(ratioNII, 3), round(ratioOIII, 3)]

        # Combined Plots
        # plot_profiles(zoneNames['low'], rp, nameForComps='SII-6717A', title=rp.regionName + " Low Zone Profiles")
        # plot_profiles(zoneNames['high'], rp, nameForComps='NeIII-3868A', title=rp.regionName + " High Zone Profiles")
        # plot_profiles(['OIII-5007A', 'H-Alpha', 'H-Beta_Blue', 'NII-6584A', 'SII-6717A'], rp, nameForComps='SII-6717A', title=rp.regionName + ' StrongestEmissionLines', sortedIndex=[0, 1, 2, 3, 4])

        # plot_profiles(['H-Beta_Blue', 'H-Beta_Red'], rp, nameForComps='H-Beta_Blue', title=rp.regionName + ' H-Beta comparison')
        # plot_profiles(['OIII-5007A', 'NeIII-3868A'], rp, nameForComps='NeIII-3868A', title=' ')
        # plot_profiles(['OIII-5007A', 'NeIII-3868A'], rp, nameForComps='OIII-5007A', title='')




if __name__ == '__main__':
    from Mrk600A import RegionParameters as Mrk600AParams
    from profile_info_NGC6845_Region7 import RegionParameters as NGC6845Region7Params
    from profile_info_NGC6845_Region26 import RegionParameters as NGC6845Region26Params
    # from profile_info_NGC6845_Region26_Counts import RegionParameters as NGC6845Region26Params

    regionsParameters = [Mrk600AParams]#,NGC6845Region7Params]#, NGC6845Region26Params]

    regionArray = []
    for regParam in regionsParameters:
        region = RegionCalculations(regParam)
        regionArray.append(region.lineInArray)

    halpha_regions_table_to_latex(regionArray)
    average_velocities_table_to_latex(regionsParameters)

    plt.show()
