import os
import sys
import astropy.units as u
import matplotlib.pyplot as plt
import numpy as np
from specutils.io import read_fits
import emission_line_analysis.constants as constants

constants.init()
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '../Input_Data_Files'))


def read_spectra(filename, scaleFlux):
    """ Reads spectra from input FITS File
    Stores the wavelength (in Angstroms) in a vector 'x'
    and the fluxes scaled by 10**14 in a vector 'y'
    x and y are an array of the wavelengths and fluxes of each of the orders"""
    x = []
    y = []
    try:
        spectra = read_fits.read_fits_spectrum1d(filename)
    except (OSError, IOError):
        spectra = read_fits.read_fits_spectrum1d(os.path.join(constants.DATA_FILES, filename))

    if isinstance(spectra, list):
        for spectrum in spectra:
            x.append(spectrum.dispersion / u.angstrom)
            y.append(spectrum.flux * scaleFlux)
        x = np.array(x)
        y = np.array(y)
    else:
        x = np.array([spectra.dispersion / u.angstrom])
        y = np.array([spectra.flux * scaleFlux])

    return x, y


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

        if not os.path.exists(os.path.join(constants.OUTPUT_DIR, rp.regionName)):
            os.makedirs(os.path.join(constants.OUTPUT_DIR, rp.regionName))

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
        plt.xlabel(constants.WAVE_AXIS_LABEL)
        plt.ylabel(constants.FLUX_AXIS_LABEL)
        plt.savefig(os.path.join(constants.OUTPUT_DIR, self.rp.regionName, title))

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
