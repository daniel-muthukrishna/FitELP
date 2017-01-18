import os
import numpy as np
from lmfit.models import GaussianModel, LinearModel, PolynomialModel, VoigtModel
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
    spectra = read_fits.read_fits_spectrum1d(filename)  # , dispersion_unit=u.angstrom, flux_unit=u.cgs.erg/u.angstrom/u.cm**2/u.s)
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

    totalSigmaSquared = sigmaObs**2 - sigmaInstr**2 - sigmaTemp2
    totalSigmaSquaredError = 2 * sigmaObs * sigmaObsError
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
        sigmaObsError = model.params['g%d_height' % (i + 1)].stderr
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
    else:
        ion = r"$\mathrm{[%s]}$" % emLineName.split('-')[0]
        lambdaZero = '$%s$' % emLineName.split('-')[1][:-1]

    return ion, lambdaZero


def halpha_regions_table_to_latex(regionInfoArray, directory="."):
    saveFileName = 'RegionInfo'
    headings = [r'Region Name', r'SFR', r'$\mathrm{SFR_{err}}$', r'$\mathrm{L(H}\alpha)$', r'$\mathrm{L(H}\alpha)_{\mathrm{err}}$', r'$\mathrm{NII/H}\alpha$', r'$\mathrm{OIII/H}\beta$']
    table_to_latex(regionInfoArray, headings, saveFileName, directory)

def comp_table_to_latex(componentArray, rp):
    saveFileName = 'ComponentTable'
    headings = [r'$\mathrm{\lambda_0}$', r'$\mathrm{Ion}$', r'$\mathrm{Comp.}$', r'$\mathrm{v_r}$',
                r'$\mathrm{{v_r}_{err}}$', r'$\mathrm{\sigma_{int}}$', r'$\mathrm{{\sigma_{int}}_{err}}$',
                r'$\mathrm{Flux}$', r'$\mathrm{Flux_{err}}$', r'$\mathrm{EM_f}$', r'$\mathrm{GlobalFlux}$',
                r'$\mathrm{GlobalFlux_{err}}$']
    table_to_latex(componentArray, headings, saveFileName, rp.regionName)


def table_to_latex(tableArray, headings, saveFileName, directory):
    texFile = open(directory + '/' + saveFileName + '.tex', 'w')
    texFile.write('\\documentclass{article}\n')
    texFile.write('\\usepackage[landscape, margin=0.5in]{geometry}\n')
    # texFile.write('\\usepackage[LGRgreek]{mathastext}\n')
    # texFile.write('\\usepackage[utf8]{inputenc}\n')
    texFile.write('\\begin{document}\n')
    texFile.write('\n')
    texFile.write('\\begin{table}[tbp]\n')
    texFile.write('\\centering\n')
    texFile.write('\\begin{tabular}{%s}\n' % ('l' * len(headings[0])))
    texFile.write('\\hline\n')
    texFile.write(' & '.join(str(e) for e in headings) + ' \\\\ \\hline\n')
    for line in tableArray:
        texFile.write(' & '.join(str(e) for e in line) + ' \\\\ \n')
    texFile.write('\\hline\n')
    texFile.write('\\end{tabular}\n')
    texFile.write('\\end{table}\n')
    texFile.write('\n')
    texFile.write('\\end{document}\n')

    texFile.close()

    os.system("pdflatex ./'" + directory + "'/" + saveFileName + ".tex")
    if directory != ".":
        os.system("mv " + saveFileName + ".pdf ./'" + directory + "'")
        os.system("rm " + saveFileName + ".*")


def calc_luminosity(rp):
    calcLuminosity = 4 * np.pi * rp.emProfiles['H-Alpha']['globalFlux'] * rp.distance**2
    calcLuminosityError = 4 * np.pi * rp.distance**2 * rp.emProfiles['H-Alpha']['globalFluxErr']
    starFormRate = 5.5e-42 * calcLuminosity
    starFormRateError = 5.5e-42 * calcLuminosityError

    return calcLuminosity, calcLuminosityError, starFormRate, starFormRateError


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
        ax2 = ax1.twiny()
        ax1.plot(y[orderNum][minIndex:maxIndex], label='Spectrum')
        plt.xlim([0,4000])
        ax1Ticks = ax1.get_xticks()
        ax2Ticks = ax1Ticks
        ax2.set_xticks(ax2Ticks)
        ax2.set_xbound(ax1.get_xbound())
        ax2.set_xticklabels("%.2f" % z for z in (x[orderNum][minIndex:maxIndex][t] for t in ax2Ticks[:-2]))
        #ax2.plot(y[orderNum][minIndex:maxIndex])
        if yE is not None:
            pass #plt.plot(xE[orderNum][minIndex:maxIndex], yE[orderNum][minIndex:maxIndex], label='Spectrum Error')
        plt.legend()
        plt.xlabel("Wavelength ($\AA$)")
        plt.ylabel("Flux")
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

    def _gaussian_component(self, pars, prefix, c, s, a, cMin=-np.inf, cMax=np.inf, sMin=-np.inf, sMax=np.inf, aMin=-np.inf, aMax=np.inf):
        """Fits a gaussian with given parameters.
        pars is the lmfit Parameters for the fit, prefix is the label of the gaussian, c is the center, s is sigma,
        a is amplitude. Returns the Gaussian model"""
        if self.zone == 'low':
            if self.lineName == 'H-Alpha':  # Find solutions
                varyCentre = True
                varySigma = True
                varyAmp = True
            elif self.lineName in ['SII-6717A', 'NII-6584A', 'OII-3729A', 'HeI-5876A', 'SIII-9069A']:  # Copy center from Halpha, others vary
                varyCentre = False
                varySigma = True
                varyAmp = True
            elif self.lineName in ['SII-6731A', 'NII-6548A', 'NII-5755A', 'OII-3726A', 'HeI-6678A', 'HeI-7065A', 'HeI-4471A', 'SIII-6312A']:  # Copy center from Halpha, sigma from above
                varyCentre = False
                varySigma = False
                varyAmp = True
            elif self.lineName in ['H-Gamma', 'OI-6300A', 'ArIII-7136A', 'HeIH8-3889A', 'NeIII-3976A', 'NeIII-3970A', 'NeIII-3868A']:  # Copy center and sigma from Halpha
                varyCentre = False
                varySigma = False
                varyAmp = True
            else:               # Copy center from Halpha, others vary
                varyCentre = False
                varySigma = True
                varyAmp = True
                # cMin = c - c*0.01
                # cMax = c + c*0.01
                # sMin = s - s*0.03
                # sMax = s + s*0.03
        elif self.zone == 'high':
            if self.lineName == 'OIII-5007A':  # Find solutions
                varyCentre = True
                varySigma = True
                varyAmp = True
            else:                               # Copy center from OIII-5007 (all others vary)
                varyCentre = False
                varySigma = True
                varyAmp = True

        g = GaussianModel(prefix=prefix)
        pars.update(g.make_params())
        pars[prefix+'center'].set(c, min=cMin, max=cMax, vary=varyCentre)
        pars[prefix + 'sigma'].set(s, min=sMin, max=sMax, vary=varySigma)
        pars[prefix + 'amplitude'].set(a, min=aMin, max=aMax, vary=varyAmp)

        return g

    def lin_and_multi_gaussian(self, numOfComponents, cList, sList, aList, lS, lI):
        """All lists should be the same length"""
        gList = []

        lin = LinearModel(prefix='lin_')
        self.linGaussParams = lin.guess(self.flux, x=self.vel)
        self.linGaussParams.update(lin.make_params())
        self.linGaussParams['lin_slope'].set(lS)
        self.linGaussParams['lin_intercept'].set(lI)

        for i in range(numOfComponents):
            gList.append(self._gaussian_component(self.linGaussParams,'g%d_' % (i+1), cList[i], sList[i], aList[i]))
        gList = np.array(gList)
        mod = lin + gList.sum()

        init = mod.eval(self.linGaussParams, x=self.vel)
        out = mod.fit(self.flux, self.linGaussParams, x=self.vel, weights=self.weights)
        print "######## %s Linear and Multi-gaussian Model ##########" % self.lineName
        print (out.fit_report())
        components = out.eval_components()

        ion, lambdaZero = line_label(self.lineName, self.restWave, self.rp)
        plt.figure("%s %s %s" % (self.rp.regionName, ion, lambdaZero))
        plt.title("%s %s" % (ion, lambdaZero))
        plt.xlabel(r"$\mathrm{Velocity \ (km s^{-1}}$)")
        plt.ylabel(r"$\mathrm{Flux \ (10^{-14} \ erg s^{-1} \ cm^{-2} \ \AA^{-1}}$)")
        plt.plot(self.vel, self.flux, label='Data')
        for i in range(numOfComponents):
            labelComp = ['Narrow 1', 'Broad', 'Narrow 2']  # 'g%d_' % (i+1)
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
        # galaxyRegion.plot_order(26, filt='red', maxIndex=-10, title="")
        # plt.show()

        lowZoneProfiles = []
        highZoneProfiles = []
        ampListAll = []
        allModelComponents = []
        # Iterate through emission lines
        for emName, emInfo in rp.emProfiles.items():
            print "------------------ %s ----------------" %emName
            wave1, flux1, wave1Error, flux1Error = galaxyRegion.mask_emission_line(emInfo['Order'], filt=emInfo['Filter'], minIndex=emInfo['minI'], maxIndex=emInfo['maxI'])
            emLineProfile = EmissionLineProfile(wave1, flux1, restWave=emInfo['restWavelength'], lineName=emName, rp=rp)
            vel1 = emLineProfile.vel
            fittingProfile = FittingProfile(vel1, flux1, restWave=emInfo['restWavelength'], lineName=emName, fluxError=flux1Error, zone=emInfo['zone'], rp=rp)
            ion1, lambdaZero1 = line_label(emName, emInfo['restWavelength'], rp)
            emLabel = (ion1 + ' ' + lambdaZero1)

            if emInfo['zone'] == 'low':
                if emName == 'H-Alpha':
                    model1, comps = fittingProfile.lin_and_multi_gaussian(rp.numComps , rp.centerListLowZone, rp.sigmaListLowZone, emInfo['ampList'], rp.linSlopeLowZone, rp.linIntLowZone)
                    rp.emProfiles[emName]['centerList'] = []
                    rp.emProfiles[emName]['sigmaList'] = []
                    for idx in range(rp.numComps ):
                        rp.emProfiles[emName]['centerList'].append(model1.best_values['g%d_center' % (idx + 1)])
                        rp.emProfiles[emName]['sigmaList'].append(model1.best_values['g%d_sigma' % (idx + 1)])

                elif emName in ['SII-6717A', 'NII-6584A', 'OII-3729A', 'HeI-5876A', 'SIII-9069A']:
                    rp.emProfiles[emName]['centerList'] = rp.emProfiles['H-Alpha']['centerList']
                    model1, comps = fittingProfile.lin_and_multi_gaussian(rp.numComps , rp.emProfiles['H-Alpha']['centerList'], rp.emProfiles['H-Alpha']['sigmaList'], emInfo['ampList'], rp.linSlopeLowZone, rp.linIntLowZone)
                    rp.emProfiles[emName]['sigmaList'] = []
                    for idx in range(rp.numComps ):
                        rp.emProfiles[emName]['sigmaList'].append(model1.best_values['g%d_sigma' % (idx + 1)])
                else:
                    rp.emProfiles[emName]['centerList'] = rp.emProfiles['H-Alpha']['centerList']
                    if emName in ['NII-6548A', 'NII-5755A']:
                        rp.emProfiles[emName]['sigmaList'] = rp.emProfiles['NII-6584A']['sigmaList']
                    elif emName == 'SII-6731A':
                        rp.emProfiles[emName]['sigmaList'] = rp.emProfiles['SII-6717A']['sigmaList']
                    elif emName == 'OII-3726A':
                        rp.emProfiles[emName]['sigmaList'] = rp.emProfiles['OII-3729A']['sigmaList']
                    elif emName in ['HeI-6678A', 'HeI-7065A', 'HeI-4471A']:
                        rp.emProfiles[emName]['sigmaList'] = rp.emProfiles['HeI-5876A']['sigmaList']
                    elif emName == 'SIII-6312A':
                        rp.emProfiles[emName]['sigmaList'] = rp.emProfiles['SIII-9069A']['sigmaList']
                    else:
                        rp.emProfiles[emName]['sigmaList'] = rp.emProfiles['H-Alpha']['sigmaList']
                    model1, comps = fittingProfile.lin_and_multi_gaussian(rp.numComps , rp.emProfiles[emName]['centerList'], rp.emProfiles[emName]['sigmaList'], emInfo['ampList'], rp.linSlopeLowZone, rp.linIntLowZone)
                lowZoneProfiles.append([emName, vel1, flux1, model1.best_fit, emInfo['Colour'], comps, emLabel])

            elif emInfo['zone'] == 'high':
                if emName == 'OIII-5007A':
                    model1, comps = fittingProfile.lin_and_multi_gaussian(rp.numComps , rp.centerListHighZone, rp.sigmaListHighZone, emInfo['ampList'], rp.linSlopeHighZone, rp.linIntHighZone)
                    rp.emProfiles[emName]['centerList'] = []
                    rp.emProfiles[emName]['sigmaList'] = []
                    for idx in range(rp.numComps ):
                        rp.emProfiles[emName]['centerList'].append(model1.best_values['g%d_center' % (idx + 1)])
                        rp.emProfiles[emName]['sigmaList'].append(model1.best_values['g%d_sigma' % (idx + 1)])
                else:
                    rp.emProfiles[emName]['centerList'] = rp.emProfiles['OIII-5007A']['centerList']
                    rp.emProfiles[emName]['sigmaList'] = rp.emProfiles['OIII-5007A']['sigmaList']
                    model1, comps = fittingProfile.lin_and_multi_gaussian(rp.numComps , rp.emProfiles[emName]['centerList'], rp.emProfiles[emName]['sigmaList'], emInfo['ampList'], rp.linSlopeHighZone, rp.linIntHighZone)
                highZoneProfiles.append([emName, vel1, flux1, model1.best_fit, emInfo['Colour'], comps, emLabel])

        #Print Amplitudes
            ampComponentList = []
            o = model1
            eMFList, fluxList, fluxListErr, globalFlux, globalFluxErr = calculate_em_f(model1, rp.numComps)
            rp.emProfiles[emName]['globalFlux'] = globalFlux
            rp.emProfiles[emName]['globalFluxErr'] = globalFluxErr
            for idx in range(rp.numComps ):
                ampComponentList.append(round(model1.best_values['g%d_amplitude' % (idx + 1)], 7))
                sigInt, sigIntErr = vel_dispersion(o.params['g%d_sigma' % (idx + 1)].value, o.params['g%d_sigma' % (idx + 1)].stderr, emInfo['sigmaT2'], emInfo['Filter'], rp)
                tableLine = [lambdaZero1, ion1, rp.componentLabels[idx], round(o.params['g%d_center' % (idx + 1)].value, 1), round(o.params['g%d_center' % (idx + 1)].stderr, 1), round(sigInt, 1), round(sigIntErr, 1), round(fluxList[idx], 2), round(fluxListErr[idx], 2), round(eMFList[idx], 1), round(globalFlux, 2), round(globalFluxErr, 2)]
                if idx != 0:
                    tableLine[0:2] = ['', '']
                    tableLine[-2:] = ['', '']
                allModelComponents.append(tableLine)
            ampListAll.append([emName, ampComponentList, emInfo, emName])
        comp_table_to_latex(allModelComponents, rp)

        print "------------ List all Amplitudes -------"
        for ampComps in ampListAll:
            #print ampComps[0], ampComps[1]
            ampCompsList, emInfo, emName = ampComps[1:4]
            print "# ('" + emName + "', {'Colour': '" + emInfo['Colour'] + "', " + "'Order': " + str(emInfo['Order']) + ", " + "'Filter': '" + emInfo['Filter'] + "', " + "'minI': " + str(emInfo['minI']) + ", " + "'maxI': " + str(emInfo['maxI']) + ", " + "'restWavelength': " + str(emInfo['restWavelength']) + ", " + "'ampList': " + str(ampCompsList) + ", " + "'zone': '" + emInfo['zone'] + "', " + "'sigmaT2': " + str(emInfo['sigmaT2']) + "}),"

        print "------------ Component information ------------"
        for mod in allModelComponents:
            print mod

        try:
            ratioNII = (rp.emProfiles['NII-6584A']['globalFlux'] + rp.emProfiles['NII-6548A']['globalFlux'])/(rp.emProfiles['H-Alpha']['globalFlux'])
            ratioOIII = (rp.emProfiles['OIII-5007A']['globalFlux'] + rp.emProfiles['OIII-4959A']['globalFlux']) / (rp.emProfiles['H-Beta']['globalFlux'])
        except KeyError:
            ratioNII, ratioOIII = ('', '')
            print "NII or OIII are not defined"

        luminosity, luminosityError, sfr, sfrError = calc_luminosity(rp)

        self.lineInArray = [rp.regionName, "%.2E" % sfr, "%.0E" % sfrError, "%.0E" % luminosity, "%.0E" % luminosityError, round(ratioNII, 2), round(ratioOIII, 2)]

        # Combined Plots
        plt.figure(rp.regionName + " Low Zone Profiles")
        plt.title("Low Zone Profiles")  #Recombination Emission Lines")
        plt.xlabel(r"$\mathrm{Velocity \ (km s^{-1}}$)")
        plt.ylabel(r"$\mathrm{Flux \ (10^{-14} \ erg s^{-1} \ cm^{-2} \ \AA^{-1}}$)")
        for profile in lowZoneProfiles:
            name, x, y, mod, col, comps, lab = profile
            plt.plot(x, y, color=col, label=lab)
            plt.plot(x, mod, color=col, linestyle='--')
            if name == 'H-Delta':
                for idx in range(rp.numComps ):
                    plt.plot(x, comps['g%d_' % (idx + 1)]+comps['lin_'], color=rp.componentColours[idx], linestyle=':')
        plt.xlim(rp.plottingXRange)
        plt.legend()
        plt.savefig(rp.regionName + '/' + 'LowZoneProfiles.png')

        plt.figure(rp.regionName + " High Zone Profiles")
        plt.title("High Zone Profiles")
        plt.xlabel(r"$\mathrm{Velocity \ (km s^{-1}}$)")
        plt.ylabel(r"$\mathrm{Flux \ (10^{-14} \ erg s^{-1} \ cm^{-2} \ \AA^{-1}}$)")
        for profile in highZoneProfiles:
            name, x, y, mod, col, comps, lab = profile
            plt.plot(x, y, color=col, label=lab)
            plt.plot(x, mod, color=col, linestyle='--')
            if name == 'OIII-4959A':
                for idx in range(rp.numComps ):
                    plt.plot(x, comps['g%d_' % (idx + 1)]+comps['lin_'], color=rp.componentColours[idx], linestyle=':')
        plt.xlim(rp.plottingXRange)
        plt.savefig(rp.regionName + '/' + 'HighZoneProfiles.png')
        plt.legend()

        plt.figure(rp.regionName)
        ax = plt.subplot(1,1,1)
        plt.title(rp.regionName)
        plt.xlabel(r"$\mathrm{Velocity \ (km s^{-1}}$)")
        plt.ylabel(r"$\mathrm{Flux \ (10^{-14} \ erg s^{-1} \ cm^{-2} \ \AA^{-1}}$)")
        for profile in (lowZoneProfiles + highZoneProfiles):
            name, x, y, mod, col, comps, lab = profile
            if name in ['H-Alpha', 'OIII-5007A', 'H-Beta', 'NII-6584A', 'SII-6717A']:
                ax.plot(x, y, color=col, label=lab)
                ax.plot(x, mod, color=col, linestyle='--')
                if name == 'SII-6717A':
                    for idx in range(rp.numComps ):
                        ax.plot(x, comps['g%d_' % (idx + 1)]+comps['lin_'], color=rp.componentColours[idx], linestyle=':')
        plt.xlim(rp.plottingXRange)
        handles, labels = ax.get_legend_handles_labels()
        sortedIndex = [1, 4, 0, 2, 3]
        handles2 = [handles[idx] for idx in sortedIndex]
        labels2 = [labels[idx] for idx in sortedIndex]
        ax.legend(handles2, labels2)
        plt.savefig(rp.regionName + '/' + 'StrongestEmissionLines.png')











if __name__ == '__main__':
    from profile_info_NGC6845_Region7 import RegionParameters as NGC6845Region7Params
    from profile_info_NGC6845_Region26 import RegionParameters as NGC6845Region26Params

    regionsParameters = [NGC6845Region7Params, NGC6845Region26Params]

    regionArray = []
    for regParam in regionsParameters:
        region = RegionCalculations(regParam)
        regionArray.append(region.lineInArray)

    halpha_regions_table_to_latex(regionArray)
    #test

    plt.show()
