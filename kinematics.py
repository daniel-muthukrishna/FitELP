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

        x, y, xE, yE = self._filter_argument(filt)

        plt.figure(title)
        plt.title(title)
        plt.plot(x[orderNum][minIndex:maxIndex], y[orderNum][minIndex:maxIndex], label='Spectrum')
        #plt.plot(y[orderNum][minIndex:maxIndex])
        if yE is not None:
            pass #plt.plot(xE[orderNum][minIndex:maxIndex], yE[orderNum][minIndex:maxIndex], label='Spectrum Error')
        plt.legend()
        plt.xlabel("Wavelength ($\AA$)")
        plt.ylabel("Flux")
        plt.savefig('Figures/' + title)

    def mask_emission_line(self, orderNum, filt='red', minIndex=0, maxIndex=-1):
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
    def __init__(self, vel, flux, restWave, lineName, fluxError=None):
        """The input vel and flux must be limited to a single emission line profile"""
        self.vel = vel
        self.flux = flux
        self.fluxError = fluxError
        self.restWave = restWave
        self.lineName = lineName
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

    def _gaussian_component(self, pars, prefix, c, cMin, cMax, s, sMin, sMax, a, aMin, aMax):
        """Fits a gaussian with given parameters.
        pars is the lmfit Parameters for the fit, prefix is the label of the gaussian, c is the center, s is sigma,
        a is amplitude. Returns the Gaussian model"""
        if self.lineName == 'H-Alpha ':
            varyCentre = True
            varySigma = True
            varyAmp = True
        elif self.lineName in ['H-Beta ', 'H-Gamma ', 'H-Delta ']:
            varyCentre = False
            varySigma = True
            varyAmp = True
            # cMin = c - c*0.01
            # cMax = c + c*0.01
            # sMin = s - s*0.03
            # sMax = s + s*0.03
        elif self.lineName in ['NII-6548A ', 'NII-6584A ', 'SII-6717A ', 'SII-6731A ', 'OII-3717A ', 'OII-3729A ', 'OII-7919A ', 'OII-7330A ', 'OI-6300A ', 'OI-6364A ', 'SIII-6312A ', 'SIII-9069A ', 'SIII-9535A ', 'ArIII-7136A ', 'ArIII-7751A ', 'He1H8-3889A ', 'HeI-4471A ', 'HeI-5876A ', 'HeI-6678A ', 'HeI-7065A ', 'HeI-7281A ']:
            varyCentre = False
            varySigma = True
            varyAmp = True
            # cMin = c - c*0.01
            # cMax = c + c*0.01
            # sMin = s - s*0.03
            # sMax = s + s*0.03
        elif self.lineName == 'OIII-5007 ':
            varyCentre = True
            varySigma = True
            varyAmp = True
        elif self.lineName in ['OIII-5007A ', 'OIII-4959A ', 'OIII-4363A ']:
            varyCentre = False
            varySigma = True
            varyAmp = True
            # cMin = c - c*0.01
            # cMax = c + c*0.01
            # sMin = s - s*0.03
            # sMax = s + s*0.03
        elif self.lineName in ['NeIII-3868A  ', 'NeIII-3970A ']:
            varyCentre = False
            varySigma = True
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

    def lin_and_multi_gaussian(self, numOfComponents, cList, cMinList, cMaxList, sList, sMinList, sMaxList, aList, aMinList, aMaxList, lS, lSMin, lSMax, lI, lIMin, lIMax):
        """All lists should be the same length"""
        gList = []

        lin = LinearModel(prefix='lin_')
        self.linGaussParams = lin.guess(self.flux, x=self.vel)
        self.linGaussParams.update(lin.make_params())
        self.linGaussParams['lin_slope'].set(lS, min=lSMin, max=lSMax)
        self.linGaussParams['lin_intercept'].set(lI, min=lIMin, max=lIMax)

        for i in range(numOfComponents):
            gList.append(self._gaussian_component(self.linGaussParams,'g%d_' % (i+1), cList[i], cMinList[i], cMaxList[i], sList[i], sMinList[i], sMaxList[i], aList[i], aMinList[i], aMaxList[i]))
        gList = np.array(gList)
        mod = lin + gList.sum()

        init = mod.eval(self.linGaussParams, x=self.vel)
        out = mod.fit(self.flux, self.linGaussParams, x=self.vel, weights=self.weights)
        print "######## %s Linear and Multi-gaussian Model ##########" %self.lineName
        print (out.fit_report())
        components = out.eval_components()

        plt.figure(self.lineName + "%d Component Linear-Gaussian Model" % numOfComponents)
        plt.title(self.lineName + "%d Component Linear-Gaussian Model" % numOfComponents)
        plt.plot(self.vel, self.flux, label='Original')
        for i in range(numOfComponents):
            plt.plot(self.vel, components['g%d_' % (i+1)], label='g%d_' % (i+1))
        plt.plot(self.vel, components['lin_'], label='lin_')
        plt.plot(self.vel, out.best_fit, label='Combined')
        plt.plot(self.vel, init, label='init')
        plt.legend(loc='upper left')
        plt.savefig('Figures/' + self.lineName + "%d Component Linear-Gaussian Model" % numOfComponents)

        self._get_amplitude(numOfComponents, out)

        return out




if __name__ == '__main__':
    galaxyRegion = GalaxyRegion('NGC6845_7B.fc.fits', 'NGC6845_7R.fc.fits', specFileBlueError='NGC6845_7B_ErrorFlux.fc.fits', specFileRedError='NGC6845_7R_ErrorFlux.fc.fits', scaleFlux=1e14)  # Flux Calibrated
    #galaxyRegion = GalaxyRegion('NGC6845_7B_SPEC1.wc.fits', 'NGC6845_7R_SPEC1.wc.fits', specFileBlueError='NGC6845_7B_VAR4.wc.fits', specFileRedError='NGC6845_7R_VAR4.wc.fits', scaleFlux=1)  # Counts (ADUS) Calibrated
    #galaxyRegion.plot_order(3, filt='blue', maxIndex=-10, title="NGC6845_7_red Order 21")

    # SPECTRAL LINE INFO FOR [H_ALPHA, H_BETA, H_GAMMA, H_DELTA]
    lineNames = ['H-Alpha ', 'H-Beta ', 'H-Gamma ', 'H-Delta ']#, 'NII-6548A ', 'NII-6584A ', 'SII-6717A ', 'SII-6731A ', 'OII-3717A ', 'OII-3729A ', 'OII-7919A ', 'OII-7330A ', 'OI-6300A ', 'OI-6364A ', 'SIII-6312A ', 'SIII-9069A ', 'SIII-9535A ', 'ArIII-7136A ', 'ArIII-7751A ', 'He1H8-3889A ', 'HeI-4471A ', 'HeI-5876A ', 'HeI-6678A ', 'HeI-7065A ', 'HeI-7281A ', 'OIII-5007A ', 'OIII-4959A ', 'OIII-4363A ', 'NeIII-3868A  ', 'NeIII-3970A ']
    emProfiles = [
        {'Name': 'H-Alpha ',    'Colour': 'b', 'Order': 20, 'Filter': 'red',  'minI': 1180, 'maxI': 1650, 'restWavelength': 6562.82, 'ampList': [17.1354, 15.3248335, 25.9915929], 'ampMinList': [-np.inf, -np.inf, -np.inf], 'ampMaxList': [np.inf, np.inf, np.inf]},
        {'Name': 'H-Beta ',     'Colour': 'g', 'Order': 35, 'Filter': 'blue', 'minI': 2150, 'maxI': 2800, 'restWavelength': 4861.33, 'ampList': [19.7000, 4.40000000, 5.00000000], 'ampMinList': [-np.inf, -np.inf, -np.inf], 'ampMaxList': [np.inf, np.inf, np.inf]},
        {'Name': 'H-Gamma ',    'Colour': 'r', 'Order': 27, 'Filter': 'blue', 'minI': 700,  'maxI': 1200, 'restWavelength': 4340.47, 'ampList': [3.18400, 7.70360000, 4.44400000], 'ampMinList': [-np.inf, -np.inf, -np.inf], 'ampMaxList': [np.inf, np.inf, np.inf]},
        {'Name': 'H-Delta ',    'Colour': 'c', 'Order': 22, 'Filter': 'blue', 'minI': 1300, 'maxI': 2000, 'restWavelength': 4101.74, 'ampList': [5.60000, 1.75000000, 5.00000000], 'ampMinList': [-np.inf, -np.inf, -np.inf], 'ampMaxList': [np.inf, np.inf, np.inf]},
        {'Name': 'OIII-5007A ', 'Colour': 'm', 'Order': 4,  'Filter': 'red',  'minI': 1600, 'maxI': 2100, 'restWavelength': 5007.00, 'ampList': [5.60000, 1.75000000, 5.00000000], 'ampMinList': [-np.inf, -np.inf, -np.inf], 'ampMaxList': [np.inf, np.inf, np.inf]},
        {'Name': 'OIII-4959A ', 'Colour': 'y', 'Order': 3,  'Filter': 'red',  'minI': 2300, 'maxI': 2800, 'restWavelength': 4959.00, 'ampList': [5.60000, 1.75000000, 5.00000000], 'ampMinList': [-np.inf, -np.inf, -np.inf], 'ampMaxList': [np.inf, np.inf, np.inf]},


    ]
    colour = ['b', 'g', 'r', 'c', 'm', 'y', 'k', '#D35400', '#58D68D', '#EC7063', '#5D6D7E', '#F8C471', '#7FB3D5']
    order = [20, 35, 27, 22]#, 4, 3]
    filt = ['red', 'blue', 'blue', 'blue', 'red', 'red']
    minI = [1180, 2150, 700, 1300, 1600, 2300]
    maxI = [1650, 2800, 1200, 2000, 2100, 2800]
    restWavelength = [6562.82, 4861.33, 4340.47, 4101.74, 5007, 4959]
    numOfComponents = 3

    # Information for each of the three components
    centerList = [6349.2, 6328.978, 6314.2879]
    centerMinList = [-np.inf, -np.inf, -np.inf]
    centerMaxList = [np.inf, np.inf, np.inf]
    sigmaList = [19.2858, 61.11, 21.3885036]
    sigmaMinList = [-np.inf, -np.inf, -np.inf]
    sigmaMaxList = [np.inf, np.inf, np.inf]
    linSlope = 1.3796e-5
    linSlopeMin = -np.inf
    linSlopeMax = np.inf
    linInt = -0.07987
    linIntMin = -np.inf
    linIntMax = np.inf

    allProfiles = []
    # Iterate through emission lines
    for eL in emProfiles:
        print "#################### %s ##################" %eL['Name']
        wave1, flux1, wave1Error, flux1Error = galaxyRegion.mask_emission_line(eL['Order'], filt=eL['Filter'], minIndex=eL['minI'], maxIndex=eL['maxI'])
        HAlphaLine = EmissionLineProfile(wave1, flux1, restWave=eL['restWavelength'], lineName=eL['Name'])
        vel1 = HAlphaLine.vel
        fittingProfile = FittingProfile(vel1, flux1, restWave=eL['restWavelength'], lineName=eL['Name'], fluxError=flux1Error)

        if 'H-Alpha' in eL['Name']:
            modelLinearMultiGaussian = fittingProfile.lin_and_multi_gaussian(numOfComponents, centerList, centerMinList,centerMaxList, sigmaList, sigmaMinList, sigmaMaxList, eL['ampList'], eL['ampMinList'], eL['ampMaxList'], linSlope, linSlopeMin, linSlopeMax, linInt, linIntMin, linIntMax)
            gSigmaList = []
            gCenterList = []
            for idx in range(numOfComponents):
                gSigmaList.append(modelLinearMultiGaussian.best_values['g%d_sigma' % (idx+1)])
                gCenterList.append(modelLinearMultiGaussian.best_values['g%d_center' % (idx+1)])
            print gSigmaList
            print gCenterList
        else:
            modelLinearMultiGaussian = fittingProfile.lin_and_multi_gaussian(numOfComponents, gCenterList, centerMinList, centerMaxList, gSigmaList, sigmaMinList, sigmaMaxList, eL['ampList'], eL['ampMinList'], eL['ampMaxList'], linSlope, linSlopeMin, linSlopeMax, linInt, linIntMin, linIntMax)

        allProfiles.append([eL['Name'], vel1, flux1, modelLinearMultiGaussian.best_fit, eL['Colour']])

    # Combined Plot
    plt.figure("Combined Profiles")
    plt.xlabel("Velocity (km/s)")
    plt.ylabel("Flux")
    for profile in allProfiles:
        name, x, y, mod, col = profile
        plt.plot(x, y, color=col, label=name)
        plt.plot(x, mod, color=col, linestyle='--')
    plt.legend()
    plt.show()
