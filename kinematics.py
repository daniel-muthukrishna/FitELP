import os
import numpy as np
from lmfit.models import GaussianModel, LinearModel, PolynomialModel, VoigtModel
from lmfit import Parameters
import matplotlib.pyplot as plt
import astropy.units as u
from specutils.io import read_fits
import pandas as pd
from collections import OrderedDict

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


def vel_dispersion(sigmaObs, sigmaObsError, sigmaTemp2, filter):
    # Assuming negligible error in temp or instrument
    if filter == 'blue':
        sigmaInstr = 4.9
    elif filter == 'red':
        sigmaInstr = 5.6

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
        height = model.params['g%d_height' % (i + 1)]
        sigmaObs = model.params['g%d_sigma' % (i + 1)]
        heightError = model.params['g%d_height' % (i + 1)].stderr
        sigmaObsError = model.params['g%d_height' % (i + 1)].stderr
        calcFlux, calcFluxError = calculate_flux(height, sigmaObs, heightError, sigmaObsError)

        componentFluxes.append(calcFlux)
        componentFluxErrors.append(calcFluxError)
    componentFluxes = np.array(componentFluxes)
    componentFluxErrors = np.array(componentFluxErrors)

    calcEMF = componentFluxes/sum(componentFluxes) * 100

    return calcEMF, componentFluxes, componentFluxErrors


def line_label(emLineName, emRestWave):
    if emLineName in ['H-Alpha', 'H-Beta', 'H-Gamma', 'H-Delta']:
        lambdaZero = '$%s$' % str(int(round(emRestWave)))
        if emLineName == 'H-Alpha':
            ion = r"$\mathrm{H\alpha}$"
        elif emLineName == 'H-Beta':
            ion = r"$\mathrm{H\beta}$"
        elif emLineName == 'H-Gamma':
            ion = r"$\mathrm{H\gamma}$"
        elif emLineName == 'H-Delta':
            ion = r"$\mathrm{H\delta}$"
    else:
        ion = r"$\mathrm{[%s]}$" % emName.split('-')[0]
        lambdaZero = '$%s$' % emLineName.split('-')[1][:-1]

    return ion, lambdaZero


class GalaxyRegion(object):
    def __init__(self, specFileBlue, specFileRed, specFileBlueError=None, specFileRedError=None, scaleFlux=1e14):
        """ x is wavelength arrays, y is flux arrays """
        self.xBlue, self.yBlue = read_spectra(specFileBlue, scaleFlux)
        self.xRed, self.yRed = read_spectra(specFileRed, scaleFlux)
        if specFileBlueError is None:
            self.xBlueError, self.yBlueError = (None, None)
        else:
            self.xBlueError, self.yBlueError = read_spectra(specFileBlueError, scaleFlux)
        if specFileRedError is None:
            self.xRedError, self.yRedError = (None, None)
        else:
            self.xRedError, self.yRedError = read_spectra(specFileRedError, scaleFlux)

        if not os.path.exists(regionName + '/'):
            os.makedirs(regionName + '/')

    def plot_order(self, orderNum, filt='red', minIndex=0, maxIndex=-1, title=''):
        """Plots the wavelength vs flux for a particular order. orderNum starts from 0"""
        orderNum -= 1
        x, y, xE, yE = self._filter_argument(filt)

        fig = plt.figure(title)
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
        plt.savefig(regionName + '/' + title)

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
    def __init__(self, wave, flux, restWave=6562.82, lineName=''):
        """wave and flux are for vectors representing only the given emission line
        labWave is the wavelength of the emission line if it were at rest (stationary)
        default is for H-alpha emission line"""
        self.restWave = restWave
        self.lineName = lineName
        self.wave = wave
        self.flux = flux
        self.vel = self._velocity(wave)

    def _velocity(self, wave):
        return ((wave - self.restWave) / self.restWave) * SpOfLi #(const.c/(u.m/u.s)) / 1000

    def plot_emission_line(self, xaxis='vel', title=''):
        """Choose whether the x axis is 'vel' or 'wave'"""
        plt.figure(self.lineName + title)
        plt.title(self.lineName + title)
        if xaxis == 'wave':
            plt.plot(self.wave, self.flux)
            plt.xlabel("Wavelength ($\AA$)")
        elif xaxis == 'vel':
            plt.plot(self.vel, self.flux)
            plt.xlabel("Velocity ($\mathrm{km \ s}^{-1}$)")
        plt.ylabel("Flux")
        plt.savefig(regionName + '/' + self.lineName + title)


class FittingProfile(object):
    def __init__(self, vel, flux, restWave, lineName, zone, fluxError=None):
        """The input vel and flux must be limited to a single emission line profile"""
        self.vel = vel
        self.flux = flux
        self.fluxError = fluxError
        self.restWave = restWave
        self.lineName = lineName
        self.zone = zone
        self.weights = self._weights()

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

        ion, lambdaZero = line_label(self.lineName, self.restWave)
        plt.figure("%s %s" % (ion, lambdaZero))
        plt.title("%s %s" % (ion, lambdaZero))
        plt.xlabel(r"$\mathrm{Velocity \ (km s^{-1}}$)")
        plt.ylabel(r"$\mathrm{Flux \ (10^{-14} \ erg s^{-1} \ cm^{-2} \ \AA^{-1}}$)")
        plt.plot(self.vel, self.flux, label='Data')
        for i in range(numOfComponents):
            labelComp = ['Narrow 1', 'Broad', 'Narrow 2']  # 'g%d_' % (i+1)
            plt.plot(self.vel, components['g%d_' % (i+1)]+components['lin_'], color=componentColours[i], linestyle=':', label=labelComp[i])
        # plt.plot(self.vel, components['lin_'], label='lin_')
        plt.plot(self.vel, out.best_fit, color='black', linestyle='--', label='Fit')
        # plt.plot(self.vel, init, label='init')
        plt.xlim(plottingXRange)
        plt.legend(loc='upper left')
        plt.savefig(regionName + '/' + self.lineName + " %d Component Linear-Gaussian Model" % numOfComponents)

        self._get_amplitude(numOfComponents, out)

        return out, components


def table_to_latex(componentArray):
    texFile = open(regionName + '/' + 'componentTable.tex', 'w')
    texFile.write('\\documentclass{article}\n')
    texFile.write('\\usepackage[LGRgreek]{mathastext}\n')
    texFile.write('\\usepackage[utf8]{inputenc}\n')
    texFile.write('\\begin{document}\n')
    texFile.write('\n')
    texFile.write('\\begin{table}[]\n')
    texFile.write('\\centering\n')
    texFile.write('\\begin{tabular}{%s}\n' % ('l'*len(componentArray[0])))
    headings = ['$\lambda_0$', '$Ion$', '$Comp.$', '$Centre$', '$Centre_{Error}$', '$\sigma_{int}$', '${\sigma_{int}}_{Error}$',
                '$Amp$', '$Amp_{Error}$', '$Height$', '$Height_{Error}$', '$Flux$', '$Flux_{Error}$', '$EM_f$']
    texFile.write('\\hline\n')
    texFile.write(' & '.join(str(e) for e in headings) + ' \\\\ \\hline\n')
    for line in componentArray:
        texFile.write(' & '.join(str(e) for e in line) + ' \\\\ \n')

    texFile.write('\\end{tabular}\n')
    texFile.write('\\end{table}\n')
    texFile.write('\n')
    texFile.write('\\end{document}\n')

    texFile.close()


if __name__ == '__main__':
    # ONLY CHANGE THIS IMPORT LINE TO THE APPROPRIATE REGION
    from profile_info_NGC6845_Region7 import *

    galaxyRegion = GalaxyRegion(blueSpecFile, redSpecFile, blueSpecError, redSpecError, scaleFlux)  # Flux Calibrated
    # galaxyRegion.plot_order(26, filt='red', maxIndex=-10, title="")
    # plt.show()

    lowZoneProfiles = []
    highZoneProfiles = []
    ampListAll = []
    allModelComponents = []
    # Iterate through emission lines
    for emName, emInfo in emProfiles.items():
        print "------------------ %s ----------------" %emName
        wave1, flux1, wave1Error, flux1Error = galaxyRegion.mask_emission_line(emInfo['Order'], filt=emInfo['Filter'], minIndex=emInfo['minI'], maxIndex=emInfo['maxI'])
        emLineProfile = EmissionLineProfile(wave1, flux1, restWave=emInfo['restWavelength'], lineName=emName)
        vel1 = emLineProfile.vel
        fittingProfile = FittingProfile(vel1, flux1, restWave=emInfo['restWavelength'], lineName=emName, fluxError=flux1Error, zone=emInfo['zone'])
        ion1, lambdaZero1 = line_label(emName, emInfo['restWavelength'])
        emLabel = (ion1 + ' ' + lambdaZero1)

        if emInfo['zone'] == 'low':
            if emName == 'H-Alpha':
                model1, comps = fittingProfile.lin_and_multi_gaussian(numComps, centerListLowZone, sigmaListLowZone, emInfo['ampList'], linSlopeLowZone, linIntLowZone)
                emProfiles[emName]['centerList'] = []
                emProfiles[emName]['sigmaList'] = []
                for idx in range(numComps):
                    emProfiles[emName]['centerList'].append(model1.best_values['g%d_center' % (idx + 1)])
                    emProfiles[emName]['sigmaList'].append(model1.best_values['g%d_sigma' % (idx + 1)])

            elif emName in ['SII-6717A', 'NII-6584A', 'OII-3729A', 'HeI-5876A', 'SIII-9069A']:
                emProfiles[emName]['centerList'] = emProfiles['H-Alpha']['centerList']
                model1, comps = fittingProfile.lin_and_multi_gaussian(numComps, emProfiles['H-Alpha']['centerList'], emProfiles['H-Alpha']['sigmaList'], emInfo['ampList'], linSlopeLowZone, linIntLowZone)
                emProfiles[emName]['sigmaList'] = []
                for idx in range(numComps):
                    emProfiles[emName]['sigmaList'].append(model1.best_values['g%d_sigma' % (idx + 1)])
            else:
                emProfiles[emName]['centerList'] = emProfiles['H-Alpha']['centerList']
                if emName in ['NII-6548A', 'NII-5755A']:
                    emProfiles[emName]['sigmaList'] = emProfiles['NII-6584A']['sigmaList']
                elif emName == 'SII-6731A':
                    emProfiles[emName]['sigmaList'] = emProfiles['SII-6717A']['sigmaList']
                elif emName == 'OII-3726A':
                    emProfiles[emName]['sigmaList'] = emProfiles['OII-3729A']['sigmaList']
                elif emName in ['HeI-6678A', 'HeI-7065A', 'HeI-4471A']:
                    emProfiles[emName]['sigmaList'] = emProfiles['HeI-5876A']['sigmaList']
                elif emName == 'SIII-6312A':
                    emProfiles[emName]['sigmaList'] = emProfiles['SIII-9069A']['sigmaList']
                else:
                    emProfiles[emName]['sigmaList'] = emProfiles['H-Alpha']['sigmaList']
                model1, comps = fittingProfile.lin_and_multi_gaussian(numComps, emProfiles[emName]['centerList'], emProfiles[emName]['sigmaList'], emInfo['ampList'], linSlopeLowZone, linIntLowZone)
            lowZoneProfiles.append([emName, vel1, flux1, model1.best_fit, emInfo['Colour'], comps, emLabel])

        elif emInfo['zone'] == 'high':
            if emName == 'OIII-5007A':
                model1, comps = fittingProfile.lin_and_multi_gaussian(numComps, centerListHighZone, sigmaListHighZone, emInfo['ampList'], linSlopeHighZone, linIntHighZone)
                emProfiles[emName]['centerList'] = []
                emProfiles[emName]['sigmaList'] = []
                for idx in range(numComps):
                    emProfiles[emName]['centerList'].append(model1.best_values['g%d_center' % (idx + 1)])
                    emProfiles[emName]['sigmaList'].append(model1.best_values['g%d_sigma' % (idx + 1)])
            else:
                emProfiles[emName]['centerList'] = emProfiles['OIII-5007A']['centerList']
                emProfiles[emName]['sigmaList'] = emProfiles['OIII-5007A']['sigmaList']
                model1, comps = fittingProfile.lin_and_multi_gaussian(numComps, emProfiles[emName]['centerList'], emProfiles[emName]['sigmaList'], emInfo['ampList'], linSlopeHighZone, linIntHighZone)
            highZoneProfiles.append([emName, vel1, flux1, model1.best_fit, emInfo['Colour'], comps, emLabel])

    #Print Amplitudes
        ampComponentList = []
        o = model1
        eMFList, fluxList, fluxListErr = calculate_em_f(model1, numComps)
        for idx in range(numComps):
            ampComponentList.append(round(model1.best_values['g%d_amplitude' % (idx + 1)], 7))
            sigInt, sigIntErr = vel_dispersion(o.params['g%d_sigma' % (idx + 1)].value, o.params['g%d_sigma' % (idx + 1)].stderr, emInfo['sigmaT2'], emInfo['Filter'])
            labelComponent = ['Narrow 1', 'Broad', 'Narrow 2']  # 'g%d_' % (i+1)
            allModelComponents.append([lambdaZero1, ion1, labelComponent[idx], round(o.params['g%d_center' % (idx + 1)].value, 1), round(o.params['g%d_center' % (idx + 1)].stderr, 1), round(sigInt, 1), round(sigIntErr, 1), round(o.params['g%d_amplitude' % (idx + 1)].value, 2), round(o.params['g%d_amplitude' % (idx + 1)].stderr, 2), round(o.params['g%d_height' % (idx + 1)].value, 3), round(o.params['g%d_height' % (idx + 1)].stderr, 3), round(fluxList[idx], 2), round(fluxListErr[idx], 2), round(eMFList[idx], 1)])
        ampListAll.append([emName, ampComponentList, emInfo, emName])

    print "------------ List all Amplitudes -------"
    for ampComps in ampListAll:
        #print ampComps[0], ampComps[1]
        ampCompsList, emInfo, emName = ampComps[1:4]
        print "# ('" + emName + "', {'Colour': '" + emInfo['Colour'] + "', " + "'Order': " + str(emInfo['Order']) + ", " + "'Filter': '" + emInfo['Filter'] + "', " + "'minI': " + str(emInfo['minI']) + ", " + "'maxI': " + str(emInfo['maxI']) + ", " + "'restWavelength': " + str(emInfo['restWavelength']) + ", " + "'ampList': " + str(ampCompsList) + ", " + "'zone': '" + emInfo['zone'] + "', " + "'sigmaT2': " + str(emInfo['sigmaT2']) + "}),"

    print "------------ Component information ------------"
    for mod in allModelComponents:
        print mod
    table_to_latex(allModelComponents)

    # Combined Plots
    plt.figure("Low Zone Profiles")
    plt.title("Low Zone Profiles") #Recombination Emission Lines")
    plt.xlabel(r"$\mathrm{Velocity \ (km s^{-1}}$)")
    plt.ylabel(r"$\mathrm{Flux \ (10^{-14} \ erg s^{-1} \ cm^{-2} \ \AA^{-1}}$)")
    for profile in lowZoneProfiles:
        name, x, y, mod, col, comps, lab = profile
        plt.plot(x, y, color=col, label=lab)
        plt.plot(x, mod, color=col, linestyle='--')
        if name == 'H-Delta':
            for idx in range(numComps):
                plt.plot(x, comps['g%d_' % (idx + 1)]+comps['lin_'], color=componentColours[idx], linestyle=':')
    plt.xlim(plottingXRange)
    plt.legend()
    plt.savefig(regionName + '/' + 'LowZoneProfiles.png')

    plt.figure("High Zone Profiles")
    plt.title("High Zone Profiles")
    plt.xlabel(r"$\mathrm{Velocity \ (km s^{-1}}$)")
    plt.ylabel(r"$\mathrm{Flux \ (10^{-14} \ erg s^{-1} \ cm^{-2} \ \AA^{-1}}$)")
    for profile in highZoneProfiles:
        name, x, y, mod, col, comps, lab = profile
        plt.plot(x, y, color=col, label=lab)
        plt.plot(x, mod, color=col, linestyle='--')
        if name == 'OIII-4959A':
            for idx in range(numComps):
                plt.plot(x, comps['g%d_' % (idx + 1)]+comps['lin_'], color=componentColours[idx], linestyle=':')
    plt.xlim(plottingXRange)
    plt.savefig(regionName + '/' + 'HighZoneProfiles.png')
    plt.legend()

    plt.figure(regionName)
    ax = plt.subplot(1,1,1)
    plt.title(regionName)
    plt.xlabel(r"$\mathrm{Velocity \ (km s^{-1}}$)")
    plt.ylabel(r"$\mathrm{Flux \ (10^{-14} \ erg s^{-1} \ cm^{-2} \ \AA^{-1}}$)")
    for profile in (lowZoneProfiles + highZoneProfiles):
        name, x, y, mod, col, comps, lab = profile
        if name in ['H-Alpha', 'OIII-5007A', 'H-Beta', 'NII-6584A', 'SII-6717A']:
            ax.plot(x, y, color=col, label=lab)
            ax.plot(x, mod, color=col, linestyle='--')
            if name == 'SII-6717A':
                for idx in range(numComps):
                    ax.plot(x, comps['g%d_' % (idx + 1)]+comps['lin_'], color=componentColours[idx], linestyle=':')
    plt.xlim(plottingXRange)
    handles, labels = ax.get_legend_handles_labels()
    sortedIndex = [1, 4, 0, 2, 3]
    handles2 = [handles[idx] for idx in sortedIndex]
    labels2 = [labels[idx] for idx in sortedIndex]
    ax.legend(handles2, labels2)
    plt.savefig(regionName + '/' + 'StrongestEmissionLines.png')
    plt.show()
