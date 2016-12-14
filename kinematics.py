import numpy as np
from lmfit.models import GaussianModel, LinearModel, PolynomialModel, VoigtModel
from lmfit import Parameters
from scipy.signal import medfilt
# import sys
# import math
import matplotlib.pyplot as plt
# from astropy.io import fits
import astropy.units as u
from astropy import constants as const
from specutils.io import read_fits


class GalaxyRegion(object):
    def __init__(self, specFileBlue, specFileRed):
        self.xBlue, self.yBlue = self.read_spectra(specFileBlue)
        self.xRed, self.yRed = self.read_spectra(specFileRed)

    def read_spectra(self, filename):
        """ Reads spectra from input FITS File
        Stores the wavelength (in Angstroms) in a vector 'x'
        and the fluxes scaled by 10**14 in a vector 'y'
        x and y are an array of the wavelengths and fluxes of each of the orders"""
        x = []
        y = []
        spectra = read_fits.read_fits_spectrum1d(
            filename)  # , dispersion_unit=u.angstrom, flux_unit=u.cgs.erg/u.angstrom/u.cm**2/u.s)
        for spectrum in spectra:
            x.append(spectrum.dispersion / u.angstrom)
            y.append(spectrum.flux * 1e14)
        x = np.array(x)
        y = np.array(y)

        return x, y

    def plot_order(self, orderNum, filter='red', minIndex=0, maxIndex=-1, title=''):
        """Plots the wavelength vs flux for a particular order. orderNum starts from 0"""

        x, y = self._filter_argument(filter)

        plt.figure(title)
        plt.plot(x[orderNum][minIndex:maxIndex], y[orderNum][minIndex:maxIndex])
        plt.xlabel("Wavelength ($\AA$)")
        plt.ylabel("Flux")
        plt.title(title)

    def mask_emission_line(self, orderNum, filter='red', minIndex=0, maxIndex=-1):
        x, y = self._filter_argument(filter)

        return x[orderNum][minIndex:maxIndex], y[orderNum][minIndex:maxIndex]

    def _filter_argument(self, filter):
        try:
            if filter == 'red':
                x, y = self.xRed, self.yRed
            elif filter == 'blue':
                x, y = self.xBlue, self.yBlue

            return x, y

        except NameError:
            print("Error: Invalid argument. Choose 'red' or 'blue' for the filter argument")
            exit()


class EmissionLineProfile(object):
    def __init__(self, wave, flux, restWave=6562.82, lineName=''):
        """wave and flux are for vectors representing only the given emission line
        labWave is the wavelength of the emission line if it were at rest (stationary)
        default is for H-alpha emission line"""
        self.restWave = restWave
        self.wave = wave
        self.flux = flux
        self.vel = self._velocity(wave)
        if lineName == 'Halpha':
            self.restWave = 6562.82  # angstroms

        #self.fittingProfile = FittingProfile(self.vel, self.flux)
        #self.fluxWithoutContinuum = self.fittingProfile.continuum_removal()

    def _velocity(self, wave):
        return ((wave - self.restWave) / self.restWave) * 300000 #(const.c/(u.m/u.s)) / 1000

    def plot_emission_line(self, xaxis='vel', title=''):
        """Choose whether the x axis is 'vel' or 'wave'"""
        plt.figure(title)
        if xaxis == 'wave':
            plt.plot(self.wave, self.flux)
            plt.xlabel("Wavelength ($\AA$)")
        elif xaxis == 'vel':
            plt.plot(self.vel, self.flux)
            plt.xlabel("Velocity ($\mathrm{km \ s}^{-1}$)")
        plt.ylabel("Flux")
        plt.title(title)


class FittingProfile(object):
    def __init__(self, vel, flux):
        """The input vel and flux must be limited to a single emission line profile"""
        self.vel = vel
        self.flux = flux
        self.fluxCR = self.continuum_removal() #flux with Continuum Removed
        self.gaussParams = Parameters()

    def continuum_removal(self):
        # significantly filter profile to remove emission lines
        medFilt = medfilt(self.flux, kernel_size=int(round(len(self.flux)) // 2 * 2 + 1)) # Rounds to nearest odd number

        # Fit Linear slope to filtered profile
        polyCoeff = np.polyfit(self.vel, medFilt, 1)
        p = np.poly1d(polyCoeff)
        continuum = p(self.vel)

        # Subtract continuum
        newFlux = self.flux - continuum

        #Plot
        plt.figure()
        plt.title("Continuum Removal")
        plt.plot(self.vel, self.flux, label='Original')
        plt.plot(self.vel, medFilt, label='Median Filtered')
        plt.plot(self.vel, continuum, label='Continuum')
        plt.plot(self.vel, newFlux, label='Continuum Removed')
        plt.legend(loc='upper left')

        return newFlux

    def _gaussian_component(self, pars, prefix, c, cMin, cMax, s, sMin, sMax, a, aMin, aMax):
        """Fits a gaussian with given parameters.
        pars is the lmfit Parameters for the fit, prefix is the label of the gaussian, c is the center, s is sigma,
        a is amplitude. Returns the Gaussian model"""
        g = GaussianModel(prefix=prefix)
        pars.update(g.make_params())
        pars[prefix+'center'].set(c, min=cMin, max=cMax)
        pars[prefix + 'sigma'].set(s, min=sMin, max=sMax)
        pars[prefix + 'amplitude'].set(a, min=aMin, max=aMax)

        return g

    def multi_gaussian(self, cList, cMinList, cMaxList, sList, sMinList, sMaxList, aList, aMinList, aMaxList):
        """All lists should be the same length"""
        numOfComponents = len(cList)
        gList = []

        for i in range(numOfComponents):
            gList.append(self._gaussian_component(self.gaussParams,'g%d_' % (i+1), cList[i], cMinList[i], cMaxList[i], sList[i], sMinList[i], sMaxList[i], aList[i], aMinList[i], aMaxList[i]))
            print gList
        gList = np.array(gList)
        mod = gList.sum()

        init = mod.eval(self.gaussParams, x=self.vel)
        out = mod.fit(self.fluxCR, self.gaussParams, x=self.vel)
        print (out.fit_report())
        components = out.eval_components()

        plt.figure()
        plt.title("Multi Component Gaussian Model")
        plt.plot(self.vel, self.fluxCR, label='Original')
        for i in range(numOfComponents):
            plt.plot(self.vel, components['g%d_' % (i+1)], label='g%d_' % (i+1))
        plt.plot(self.vel, out.best_fit, label='Combined')
        plt.plot(self.vel, init, label='init')
        plt.legend(loc='upper left')

        return out.best_fit



    def model_profile(self, mod=VoigtModel()):
        pars = mod.guess(self.fluxCR, x=self.vel)
        pars['gamma'].set(value=0.7, vary=True, expr='')
        out = mod.fit(self.fluxCR, pars, x=self.vel)
        print(out.fit_report(min_correl=0.25))

        plt.figure()
        plt.title('Models')
        plt.plot(self.vel, self.fluxCR,label = 'Emission Line')
        plt.plot(self.vel, out.best_fit, label='VoigtModel')
        plt.xlabel("Velocity ($\mathrm{km \ s}^{-1}$)")
        plt.ylabel("Flux")
        plt.legend(loc='upper left')

        return out.best_fit



if __name__ == '__main__':
    ngc6845_7 = GalaxyRegion('NGC6845_7B.fc.fits', 'NGC6845_7R.fc.fits')
    #ngc6845_7.plot_order(20, filter='red', maxIndex=-10, title="NGC6845_7_red Order 21")

    # SPECTRAL LINE INFO FOR H_ALPHA
    order = 20
    filt = 'red'
    minI = 1180
    maxI = 1650
    restWavelength = 6562.82
    wave1, flux1 = ngc6845_7.mask_emission_line(20, filter=filt, minIndex=minI, maxIndex=maxI)
    HAlphaLine = EmissionLineProfile(wave1, flux1, restWave=restWavelength)
    #HAlphaLine.plot_emission_line(xaxis='vel', title='H-alpha emission line for NGC6845_7')
    vel1 = HAlphaLine.vel

    # FIT VOIGT MODEL
    fittingProfile = FittingProfile(vel1, flux1)
    model = fittingProfile.model_profile()

    # FIT MULTI-COMPONENT GAUSSIAN
    centerList = [6170.61571, 6187.03025, 6190.34511]
    centerMinList = [6169, -np.inf, -np.inf]
    centerMaxList = [6173, np.inf, np.inf]
    sigmaList = [17.1169513, 90, 44.5836051]
    sigmaMinList = [-np.inf, -np.inf, -np.inf]
    sigmaMaxList = [np.inf, np.inf, np.inf]
    amplitudeList = [20.8830725, 56.2511526, 44.5836051]
    amplitudeMinList = [-np.inf, -np.inf, -np.inf]
    amplitudeMaxList = [np.inf, np.inf, np.inf]
    modelMultiGaussian = fittingProfile.multi_gaussian(centerList,centerMinList,centerMaxList,sigmaList,sigmaMinList,sigmaMaxList,amplitudeList,amplitudeMinList,amplitudeMaxList)

    plt.show()
