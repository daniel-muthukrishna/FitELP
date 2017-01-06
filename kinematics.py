import os
import numpy as np
from lmfit.models import GaussianModel, LinearModel, PolynomialModel, VoigtModel
from lmfit import Parameters
import matplotlib.pyplot as plt
import astropy.units as u
from specutils.io import read_fits
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

        if not os.path.exists('Figures/'):
            os.makedirs('Figures/')

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
        plt.savefig('Figures/' + title)

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
        plt.savefig('Figures/' + self.lineName + title)


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
            if self.lineName == 'H-Alpha':
                varyCentre = True
                varySigma = True
                varyAmp = True
            elif self.lineName in ['NII-6548A', 'NII-6584A', 'SII-6717A', 'SII-6731A', 'OII-3726A', 'OII-3729A', 'SIII-9069A']:
                varyCentre = False
                varySigma = True
                varyAmp = True
            else:
                varyCentre = False
                varySigma = False
                varyAmp = True
                # cMin = c - c*0.01
                # cMax = c + c*0.01
                # sMin = s - s*0.03
                # sMax = s + s*0.03
        elif self.zone == 'high':
            if self.lineName == 'OIII-5007A':
                varyCentre = True
                varySigma = True
                varyAmp = True
            else:
                varyCentre = False
                varySigma = False
                varyAmp = True
                # cMin = c - c*0.01
                # cMax = c + c*0.01
                # sMin = s - s*0.03
                # sMax = s + s*0.03

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
        print "######## %s Linear and Multi-gaussian Model ##########" %self.lineName
        print (out.fit_report())
        components = out.eval_components()

        plt.figure(self.lineName + " %d Component Linear-Gaussian Model" % numOfComponents)
        plt.title(self.lineName + " %d Component Linear-Gaussian Model" % numOfComponents)
        plt.plot(self.vel, self.flux, label='Original')
        for i in range(numOfComponents):
            plt.plot(self.vel, components['g%d_' % (i+1)], label='g%d_' % (i+1))
        plt.plot(self.vel, components['lin_'], label='lin_')
        plt.plot(self.vel, out.best_fit, label='Combined')
        plt.plot(self.vel, init, label='init')
        plt.legend(loc='upper left')
        plt.savefig('Figures/' + self.lineName + " %d Component Linear-Gaussian Model" % numOfComponents)

        self._get_amplitude(numOfComponents, out)

        return out, components




if __name__ == '__main__':
    galaxyRegion = GalaxyRegion('NGC6845_7B.fc.fits', 'NGC6845_7R.fc.fits', specFileBlueError='NGC6845_7B_ErrorFlux.fc.fits', specFileRedError='NGC6845_7R_ErrorFlux.fc.fits', scaleFlux=1e14)  # Flux Calibrated
    #galaxyRegion = GalaxyRegion('NGC6845_7B_SPEC1.wc.fits', 'NGC6845_7R_SPEC1.wc.fits', specFileBlueError='NGC6845_7B_VAR4.wc.fits', specFileRedError='NGC6845_7R_VAR4.wc.fits', scaleFlux=1)  # Counts (ADUS) Calibrated
    # galaxyRegion.plot_order(24, filt='red', maxIndex=-10, title="")
    # plt.show()
    numOfComponents = 3
    lowZoneProfiles = []
    highZoneProfiles = []

    # SPECTRAL LINE INFO FOR ALL EMISSION LINES
    emProfiles = OrderedDict([
        ('H-Alpha', {'Colour': 'b', 'Order': 21, 'Filter': 'red', 'minI': 1180, 'maxI': 1650, 'restWavelength': 6562.82, 'ampList': [17.1348548, 15.3253165, 25.9916416], 'zone': 'low'}),
        ('OIII-5007A', {'Colour': 'b', 'Order': 5, 'Filter': 'red', 'minI': 1600, 'maxI': 2100, 'restWavelength': 5006.84, 'ampList': [22.1758318, 26.5388225, 27.2491339], 'zone': 'high'}),
        ('H-Beta', {'Colour': 'g', 'Order': 36, 'Filter': 'blue', 'minI': 2150, 'maxI': 2800, 'restWavelength': 4861.33, 'ampList': [7.1034076, 6.9433785, 9.0872374], 'zone': 'low'}),
        ('H-Gamma', {'Colour': 'r', 'Order': 28, 'Filter': 'blue', 'minI': 700, 'maxI': 1200, 'restWavelength': 4340.47, 'ampList': [3.5975999, 4.4061048, 4.9858671], 'zone': 'low'}),
        ('H-Delta', {'Colour': 'c', 'Order': 23, 'Filter': 'blue', 'minI': 1400, 'maxI': 2000, 'restWavelength': 4101.74, 'ampList': [2.0445931, 2.5207302, 2.9131719], 'zone': 'low'}),
        ('NII-6548A', {'Colour': 'm', 'Order': 21, 'Filter': 'red', 'minI': 1000, 'maxI': 1300, 'restWavelength': 6548.03, 'ampList': [0.7751841, 0.28759, 0.7934139], 'zone': 'low'}),
        ('NII-6584A', {'Colour': 'y', 'Order': 21, 'Filter': 'red', 'minI': 1750, 'maxI': 2050, 'restWavelength': 6583.41, 'ampList': [2.3677107, 1.2368296, 2.1863502], 'zone': 'low'}),
        ('SII-6717A', {'Colour': 'k', 'Order': 22, 'Filter': 'red', 'minI': 1850, 'maxI': 2000, 'restWavelength': 6716.47, 'ampList': [2.0078135, 1.3327135, 1.8721066], 'zone': 'low'}),
        ('SII-6731A', {'Colour': '#58D68D', 'Order': 22, 'Filter': 'red', 'minI': 2100, 'maxI': 2350, 'restWavelength': 6730.85, 'ampList': [1.161882, 1.601409, 0.760334], 'zone': 'low'}),
        ('OII-3729A', {'Colour': '#5D6D7E', 'Order': 14, 'Filter': 'blue', 'minI': 2800, 'maxI': 3000, 'restWavelength': 3728.82, 'ampList': [14.5939116, 5.8093067, 15.9000253], 'zone': 'low'}),
        ('OII-3726A', {'Colour': '#EC7063', 'Order': 14, 'Filter': 'blue', 'minI': 2660, 'maxI': 2829, 'restWavelength': 3726.03, 'ampList': [9.7755148, 6.3739026, 9.6560968], 'zone': 'low'}),
        #('OII-7319A', {'Colour': '#F8C471', 'Order': 26, 'Filter': 'red', 'minI': 2420, 'maxI': 2520, 'restWavelength': 7318.39, 'ampList': [2.3677108, 1.2368295, 2.1863500], 'zone': 'low'}),
        #('OII-7330A', {'Colour': '#7FB3D5', 'Order': 26, 'Filter': 'red', 'minI': 2420, 'maxI': 2520, 'restWavelength': 7330.0, 'ampList': [2.3677108, 1.2368295, 2.1863500], 'zone': 'low'}),
        ('OI-6300A', {'Colour': '#D35400', 'Order': 19, 'Filter': 'red', 'minI': 1050, 'maxI': 1250, 'restWavelength': 6300.3, 'ampList': [0.4723283, 0.0564225, 0.3964603], 'zone': 'low'}),
        #('OI-6364A', {'Colour': '#7D6608', 'Order': 19, 'Filter': 'red', 'minI': 2550, 'maxI': 2580, 'restWavelength': 6363.78, 'ampList': [2.0802379, -308.5885481, -32.2254134], 'zone': 'low'}),
        ('SIII-9069A', {'Colour': '#27AE60', 'Order': 35, 'Filter': 'red', 'minI': 1720, 'maxI': 1870, 'restWavelength': 9068.9, 'ampList': [0.9362367, 0.7920392, 1.3819049], 'zone': 'low'}),
        ('ArIII-7136A', {'Colour': '#0E6655', 'Order': 25, 'Filter': 'red', 'minI': 1713, 'maxI': 1790, 'restWavelength': 7135.78, 'ampList': [0.4505865, -0.1636273, 1.0718457], 'zone': 'low'}),
        ('HeIH8-3889A', {'Colour': '#5B2C6F', 'Order': 18, 'Filter': 'blue', 'minI': 2450, 'maxI': 2750, 'restWavelength': 3888.65, 'ampList': [2.1000007, 4.4749611, 0.0491403], 'zone': 'low'}),
        ('HeI-4471A', {'Colour': '#78281F', 'Order': 30, 'Filter': 'blue', 'minI': 1750, 'maxI': 1900, 'restWavelength': 4471.48, 'ampList': [0.2947784, 0.0391132, 0.4628403], 'zone': 'low'}),
        ('HeI-5876A', {'Colour': '#641E16', 'Order': 15, 'Filter': 'red', 'minI': 1320, 'maxI': 1700, 'restWavelength': 5875.64, 'ampList': [0.6740428, 0.8351308, 0.995738], 'zone': 'low'}),
        ('HeI-6678A', {'Colour': '#D5D8DC', 'Order': 22, 'Filter': 'red', 'minI': 1050, 'maxI': 1240, 'restWavelength': 6678.15, 'ampList': [0.2719279, -0.0142197, 0.3160476], 'zone': 'low'}),
        ('HeI-7065A', {'Colour': '#E8DAEF', 'Order': 24, 'Filter': 'red', 'minI': 3150, 'maxI': 3450, 'restWavelength': 7065.19, 'ampList': [0.1282397, 0.0734707, 0.1437775], 'zone': 'low'}),
        #('HeI-7281A', {'Colour': '#E8DAEF', 'Order': 26, 'Filter': 'red', 'minI': 1350, 'maxI': 1560, 'restWavelength': 7281.35, 'ampList': [0.6740428, 0.8351308, 0.9957380], 'zone': 'low'}),
        ('OIII-4959A', {'Colour': 'g', 'Order': 4, 'Filter': 'red', 'minI': 2300, 'maxI': 2800, 'restWavelength': 4958.91, 'ampList': [6.8087453, 12.5480994, 8.2404803], 'zone': 'high'}),
        ('NeIII-3868A', {'Colour': 'r', 'Order': 18, 'Filter': 'blue', 'minI': 1430, 'maxI': 1650, 'restWavelength': 3868.75, 'ampList': [1.7799466, 2.1882363, 2.4413757], 'zone': 'high'}),
        ('NeIII-3970A', {'Colour': 'c', 'Order': 20, 'Filter': 'blue', 'minI': 2110, 'maxI': 2290, 'restWavelength': 3970.07, 'ampList': [1.238593, 1.6775326, 1.2004526], 'zone': 'high'}),
        ('NeIII-3967A', {'Colour': 'm', 'Order': 20, 'Filter': 'blue', 'minI': 1950, 'maxI': 2135, 'restWavelength': 3967.46, 'ampList': [0.235651, 2.1809473, 0.4933877], 'zone': 'high'}),
    ])

    # Information for the center, sigma and linear for the low (H-alpha) and high (OIII) zones
    centerListLowZone = [6349.20126, 6328.97820, 6315.53639]
    sigmaListLowZone = [19.2852694, 64.1684056, 22.2647170]
    linSlopeLowZone = 1.9393e-07
    linIntLowZone = 0.00761986
    centerListHighZone = [6348.46630, 6333.03711, 6314.57965]
    sigmaListHighZone = [15.9660139, 56.3804782, 16.6302799]
    linSlopeHighZone = 2.6129e-06
    linIntHighZone = -0.00147764

    ampListAll = []
    allModelComponents = []
    # Iterate through emission lines
    print emProfiles
    for emName, emInfo in emProfiles.items():
        print "------------------ %s ----------------" %emName
        wave1, flux1, wave1Error, flux1Error = galaxyRegion.mask_emission_line(emInfo['Order'], filt=emInfo['Filter'], minIndex=emInfo['minI'], maxIndex=emInfo['maxI'])
        emLineProfile = EmissionLineProfile(wave1, flux1, restWave=emInfo['restWavelength'], lineName=emName)
        vel1 = emLineProfile.vel
        fittingProfile = FittingProfile(vel1, flux1, restWave=emInfo['restWavelength'], lineName=emName, fluxError=flux1Error, zone=emInfo['zone'])

        if emInfo['zone'] == 'low':
            if emName == 'H-Alpha':
                modelLinearMultiGaussian, comps = fittingProfile.lin_and_multi_gaussian(numOfComponents, centerListLowZone, sigmaListLowZone, emInfo['ampList'], linSlopeLowZone, linIntLowZone)
                gCenterListLowZone = []
                gSigmaListLowZone = []
                for idx in range(numOfComponents):
                    gCenterListLowZone.append(modelLinearMultiGaussian.best_values['g%d_center' % (idx + 1)])
                    gSigmaListLowZone.append(modelLinearMultiGaussian.best_values['g%d_sigma' % (idx+1)])
                emInfo['centerList'] = gCenterListLowZone
                emInfo['sigmaList'] = gSigmaListLowZone
            else:
                modelLinearMultiGaussian, comps = fittingProfile.lin_and_multi_gaussian(numOfComponents, gCenterListLowZone, gSigmaListLowZone, emInfo['ampList'], linSlopeLowZone, linIntLowZone)
            lowZoneProfiles.append([emName, vel1, flux1, modelLinearMultiGaussian.best_fit, emInfo['Colour'], comps])

        elif emInfo['zone'] == 'high':
            if emName == 'OIII-5007A':
                modelLinearMultiGaussian, comps = fittingProfile.lin_and_multi_gaussian(numOfComponents, centerListHighZone, sigmaListHighZone, emInfo['ampList'], linSlopeHighZone, linIntHighZone)
                gSigmaListHighZone = []
                gCenterListHighZone = []
                for idx in range(numOfComponents):
                    gSigmaListHighZone.append(modelLinearMultiGaussian.best_values['g%d_sigma' % (idx + 1)])
                    gCenterListHighZone.append(modelLinearMultiGaussian.best_values['g%d_center' % (idx + 1)])
            else:
                modelLinearMultiGaussian, comps = fittingProfile.lin_and_multi_gaussian(numOfComponents, gCenterListHighZone, gSigmaListHighZone, emInfo['ampList'], linSlopeHighZone, linIntHighZone)
            highZoneProfiles.append([emName, vel1, flux1, modelLinearMultiGaussian.best_fit, emInfo['Colour'], comps])

    #Print Amplitudes
        ampComponentList = []
        for idx in range(numOfComponents):
            ampComponentList.append(round(modelLinearMultiGaussian.best_values['g%d_amplitude' % (idx + 1)], 7))
            o = modelLinearMultiGaussian
            allModelComponents.append([emName, 'g%d' % (idx + 1), round(o.params['g%d_center' % (idx + 1)].value, 2), round(o.params['g%d_center' % (idx + 1)].stderr, 2), round(o.params['g%d_sigma' % (idx + 1)].value, 2), round(o.params['g%d_sigma' % (idx + 1)].stderr, 2), round(o.params['g%d_amplitude' % (idx + 1)].value, 2), round(o.params['g%d_amplitude' % (idx + 1)].stderr, 2), round(o.params['g%d_height' % (idx + 1)].value, 3), round(o.params['g%d_height' % (idx + 1)].stderr, 3)])
        ampListAll.append([emName, ampComponentList])

    print "--- List all Amplitudes ----"
    for ampComps in ampListAll:
        #print ampComps[0], ampComps[1]
        ampCompsList = ampComps[1]
        #print "# {" + "'Name': '" + emInfo['Name'] + "',   " + "'Colour': '" + eL['Colour'] + "', " + "'Order': " + str(eL['Order']) + ", " + "'Filter': '" + eL['Filter'] + "', " + "'minI': " + str(eL['minI']) + ", " + "'maxI': " + str(eL['maxI']) + ", " + "'restWavelength': " + str(eL['restWavelength']) + ", " + "'ampList': " + str(ampCompsList) + ", " + "'zone': '" + eL['zone'] + "'},"


    for mod in allModelComponents:
        print mod

    print emProfiles

    # Combined Plots
    plt.figure("Low Zone Profiles")
    plt.title("Recombination Emission Lines")
    plt.xlabel("Velocity ($\mathrm{km s^{-1}}$)")
    plt.ylabel("Flux ($\mathrm{10^{-14} \ erg s^{-1} \ cm^{-2} \ \AA^{-1}}$)")
    for profile in lowZoneProfiles:
        name, x, y, mod, col, comps = profile
        plt.plot(x, y, color=col, label=name)
        plt.plot(x, mod, color=col, linestyle='--')
        if name == 'H-Delta':
            for idx in range(numOfComponents):
                plt.plot(x, comps['g%d_' % (idx + 1)], color=col, linestyle=':')
    plt.xlim([6150, 6500])
    plt.legend()

    plt.figure("High Zone Profiles")
    plt.title("High Zone Profiles")
    plt.xlabel("Velocity ($\mathrm{km \ s^{-1}}$)")
    plt.ylabel("Flux ($\mathrm{10^{-14} \ erg s^{-1} \ cm^{-2} \ \AA^{-1}}$)")
    for profile in highZoneProfiles:
        name, x, y, mod, col, comps = profile
        plt.plot(x, y, color=col, label=name)
        plt.plot(x, mod, color=col, linestyle='--')
        for idx in range(numOfComponents):
            if name == 'OIII-4959A':
                for idx in range(numOfComponents):
                    plt.plot(x, comps['g%d_' % (idx + 1)], color=col, linestyle=':')
        plt.xlim([6150, 6500])
    plt.legend()
    plt.show()
