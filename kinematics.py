import numpy as np
from lmfit.models import GaussianModel, LinearModel, PolynomialModel, VoigtModel
from lmfit import Parameters
from scipy.signal import medfilt
import matplotlib.pyplot as plt
import astropy.units as u
from astropy import constants as const
from specutils.io import read_fits

SpOfLi = 300000. #km/s

class GalaxyRegion(object):
    def __init__(self, specFileBlue, specFileRed, specFileBlueError, specFileRedError):
        """ x is wavelength arrays, y is flux arrays """
        self.xBlue, self.yBlue = self.read_spectra(specFileBlue)
        self.xRed, self.yRed = self.read_spectra(specFileRed)
        self.xBlueError, self.yBlueError = self.read_spectra(specFileBlueError)
        self.xRedError, self.yRedError = self.read_spectra(specFileRedError)

    def read_spectra(self, filename):
        """ Reads spectra from input FITS File
        Stores the wavelength (in Angstroms) in a vector 'x'
        and the fluxes scaled by 10**14 in a vector 'y'
        x and y are an array of the wavelengths and fluxes of each of the orders"""
        x = []
        y = []
        spectra = read_fits.read_fits_spectrum1d(filename)  # , dispersion_unit=u.angstrom, flux_unit=u.cgs.erg/u.angstrom/u.cm**2/u.s)
        for spectrum in spectra:
            x.append(spectrum.dispersion / u.angstrom)
            y.append(spectrum.flux * 1e14)
        x = np.array(x)
        y = np.array(y)

        return x, y

    def plot_order(self, orderNum, filter='red', minIndex=0, maxIndex=-1, title=''):
        """Plots the wavelength vs flux for a particular order. orderNum starts from 0"""

        x, y, xE, yE = self._filter_argument(filter)

        plt.figure(title)
        plt.title(title)
        plt.plot(x[orderNum][minIndex:maxIndex], y[orderNum][minIndex:maxIndex], label='Spectrum')
        plt.plot(xE[orderNum][minIndex:maxIndex], yE[orderNum][minIndex:maxIndex], label='Spectrum Error')
        plt.legend()
        plt.xlabel("Wavelength ($\AA$)")
        plt.ylabel("Flux")
        plt.savefig('Figures/' + title)

    def mask_emission_line(self, orderNum, filter='red', minIndex=0, maxIndex=-1):
        x, y, xE, yE = self._filter_argument(filter)

        return x[orderNum][minIndex:maxIndex], y[orderNum][minIndex:maxIndex], xE[orderNum][minIndex:maxIndex], yE[orderNum][minIndex:maxIndex]

    @staticmethod
    def weights(error):
        return 1/error

    def _filter_argument(self, filter):
        try:
            if filter == 'red':
                x, y, xE, yE = self.xRed, self.yRed, self.xRedError, self.yRedError
            elif filter == 'blue':
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
    def __init__(self, vel, flux, restWave, lineName):
        """The input vel and flux must be limited to a single emission line profile"""
        self.vel = vel
        self.flux = flux
        self.restWave = restWave
        self.lineName = lineName
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
        plt.figure(self.lineName + "Continuum Removal")
        plt.title(self.lineName + "Continuum Removal")
        plt.plot(self.vel, self.flux, label='Original')
        plt.plot(self.vel, medFilt, label='Median Filtered')
        plt.plot(self.vel, continuum, label='Continuum')
        plt.plot(self.vel, newFlux, label='Continuum Removed')
        plt.legend(loc='upper left')
        plt.savefig('Figures/' + self.lineName + "Continuum Removal")

        return newFlux

    def _gaussian_component(self, pars, prefix, c, cMin, cMax, s, sMin, sMax, a, aMin, aMax):
        """Fits a gaussian with given parameters.
        pars is the lmfit Parameters for the fit, prefix is the label of the gaussian, c is the center, s is sigma,
        a is amplitude. Returns the Gaussian model"""
        if 'H-Alpha' in self.lineName:
            vary = True
        else:
            vary = False

        g = GaussianModel(prefix=prefix)
        pars.update(g.make_params())
        pars[prefix+'center'].set(c, min=cMin, max=cMax, vary=vary)
        pars[prefix + 'sigma'].set(s, min=sMin, max=sMax, vary=vary)
        pars[prefix + 'amplitude'].set(a, min=aMin, max=aMax)

        return g

    def multi_gaussian(self, numOfComponents, cList, cMinList, cMaxList, sList, sMinList, sMaxList, aList, aMinList, aMaxList):
        """All lists should be the same length"""
        gList = []

        for i in range(numOfComponents):
            gList.append(self._gaussian_component(self.gaussParams,'g%d_' % (i+1), cList[i], cMinList[i], cMaxList[i], sList[i], sMinList[i], sMaxList[i], aList[i], aMinList[i], aMaxList[i]))
        gList = np.array(gList)
        mod = gList.sum()

        init = mod.eval(self.gaussParams, x=self.vel)
        out = mod.fit(self.fluxCR, self.gaussParams, x=self.vel)
        print (out.fit_report())
        components = out.eval_components()

        plt.figure(self.lineName + "%d Component Gaussian Model" % numOfComponents)
        plt.title(self.lineName + "%d Component Gaussian Model" % numOfComponents)
        plt.plot(self.vel, self.fluxCR, label='Original')
        for i in range(numOfComponents):
            plt.plot(self.vel, components['g%d_' % (i+1)], label='g%d_' % (i+1))
        plt.plot(self.vel, out.best_fit, label='Combined')
        plt.plot(self.vel, init, label='init')
        plt.legend(loc='upper left')
        plt.savefig('Figures/' + self.lineName + "%d Component Gaussian Model" % numOfComponents)

        amplitudeTotal = 0.
        for i in range(numOfComponents):
            amplitudeTotal = amplitudeTotal + out.best_values['g%d_amplitude' % (i+1)]
        print "Amplitude Total is %f" % amplitudeTotal
        amplitudeFinal = (amplitudeTotal/SpOfLi) * self.restWave
        print "Amplitude Final is %f" % amplitudeFinal

        return out

    def voigt_model_profile(self, c=6000, s=20, g=0.7):
        mod = VoigtModel()
        pars = mod.guess(self.fluxCR, x=self.vel)
        if 'H-Alpha' in self.lineName:
            vary = True
        else:
            vary = False
        pars['center'].set(c, vary=vary)
        pars['sigma'].set(s, vary=vary)
        pars['gamma'].set(g, vary=vary)

        out = mod.fit(self.fluxCR, pars, x=self.vel)
        print(out.fit_report(min_correl=0.25))

        plt.figure(self.lineName + 'Voigt Model')
        plt.title(self.lineName + 'Voigt Model')
        plt.plot(self.vel, self.fluxCR,label = 'Emission Line')
        plt.plot(self.vel, out.best_fit, label='VoigtModel')
        plt.xlabel("Velocity ($\mathrm{km \ s}^{-1}$)")
        plt.ylabel("Flux")
        plt.legend(loc='upper left')
        plt.savefig('Figures/' + self.lineName + 'Voigt Model')

        return out




if __name__ == '__main__':
    ngc6845_7 = GalaxyRegion('NGC6845_7B.fc.fits', 'NGC6845_7R.fc.fits', 'NGC6845_7B.fc.fits', 'NGC6845_7R_ErrorFlux.fc.fits')
    # ngc6845_7.plot_order(20, filter='red', maxIndex=-10, title="NGC6845_7_red Order 21")

    # SPECTRAL LINE INFO FOR [H_ALPHA, H_BETA, H_GAMMA, H_DELTA]
    lineNames = ['H-Alpha: ', 'H-Beta: ', 'H-Gamma: ', 'H-Delta: ']
    order = [20, 35, 27, 22]
    filt = ['red', 'blue', 'blue', 'blue']
    minI = [1180, 2150, 500, 1300]
    maxI = [1650, 2800, 1200, 2000]
    restWavelength = [6562.82, 4861.33, 4340.47, 4101.74]

    # Iterate through emission lines
    for el in range(len(lineNames)):
        wave1, flux1, wave1Error, flux1Error = ngc6845_7.mask_emission_line(order[el], filter=filt[el], minIndex=minI[el], maxIndex=maxI[el])
        weights = ngc6845_7.weights(flux1Error)
        HAlphaLine = EmissionLineProfile(wave1, flux1, restWave=restWavelength[el], lineName=lineNames[el])
        HAlphaLineError = EmissionLineProfile(wave1Error, flux1Error, restWave=restWavelength[el], lineName=lineNames[el])
        vel1, vel1Error = HAlphaLine.vel, HAlphaLineError.vel
        fittingProfile = FittingProfile(vel1, flux1, restWave=restWavelength[el], lineName=lineNames[el])

        # FIT VOIGT MODEL
        if 'H-Alpha' in lineNames[el]:
            modelVoigt = fittingProfile.voigt_model_profile()
            vCenter = modelVoigt.best_values['center']
            vSigma = modelVoigt.best_values['sigma']
            vGamma = modelVoigt.best_values['gamma']
        else:
            modelVoigt = fittingProfile.voigt_model_profile(c=vCenter, s=vSigma, g=vGamma)

        # FIT MULTI-COMPONENT GAUSSIAN
        numOfComponentsList = [2, 2, 2, 2] # Number of components used for each emission line
        centerList = [6329.27891, 6320, 6190.34511] # information for each of the three components
        centerMinList = [-np.inf, -np.inf, -np.inf]
        centerMaxList = [np.inf, np.inf, np.inf]
        sigmaList = [17.1169513, 90, 44.5836051]
        sigmaMinList = [-np.inf, -np.inf, -np.inf]
        sigmaMaxList = [np.inf, np.inf, np.inf]
        amplitudeList = [[20.8830725, 56.2511526, 44.5836051], [0.9, 0.5, 0.5], [0.9, 0.5, 0.5], [0.9, 0.5, 0.5]]
        amplitudeMinList = [[-np.inf, -np.inf, -np.inf], [-np.inf, -np.inf, -np.inf], [-np.inf, -np.inf, -np.inf], [-np.inf, -np.inf, -np.inf]]
        amplitudeMaxList = [[np.inf, np.inf, np.inf], [np.inf, np.inf, np.inf], [np.inf, np.inf, np.inf], [np.inf, np.inf, np.inf]]
        if 'H-Alpha' in lineNames[el]:
            modelMultiGaussian = fittingProfile.multi_gaussian(numOfComponentsList[el], centerList,centerMinList,centerMaxList,sigmaList,sigmaMinList,sigmaMaxList,amplitudeList[el],amplitudeMinList[el],amplitudeMaxList[el])
            gSigmaList = []
            gCenterList = []
            for i in range(numOfComponentsList[el]):
                gSigmaList.append(modelMultiGaussian.best_values['g%d_sigma' % (i+1)])
                gCenterList.append(modelMultiGaussian.best_values['g%d_center' % (i + 1)])
            print gSigmaList
            print gCenterList
        else:
            modelMultiGaussian = fittingProfile.multi_gaussian(numOfComponentsList[el], gCenterList, centerMinList,
                                                               centerMaxList, sigmaList, gSigmaList, sigmaMaxList,
                                                               amplitudeList[el], amplitudeMinList[el],
                                                               amplitudeMaxList[el])
    plt.show()
