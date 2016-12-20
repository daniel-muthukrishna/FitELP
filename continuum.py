import numpy as np
from scipy.signal import medfilt
import matplotlib.pyplot as plt
from specutils.io import read_fits


class ContinuumRemoval(object):
    def __init__(self, x, y, tuner=2):
        """ Decrease tuner to lower continuum line (must be greater than 1)"""
        self.x = x
        self.y = y
        self.tuner = tuner
        self.continuumRemoved, self.continuum = self._get_continuum()

    def _get_continuum(self):
        # significantly filter profile to remove emission lines
        self.medFilt = medfilt(self.y, kernel_size=int(len(self.y) // self.tuner * 2 + 1))  # Rounds to nearest odd number

        # Fit Linear slope to filtered profile
        polyCoeff = np.polyfit(self.x, self.medFilt, 1)
        p = np.poly1d(polyCoeff)
        continuum = p(self.x)

        # Subtract continuum
        newFlux = self.y - continuum

        return newFlux, continuum

    def plot_continuum(self, title=''):
        plt.figure(title + "Continuum Removal")
        plt.title(title + "Continuum Removal")
        plt.plot(self.x, self.y, label='Original')
        plt.plot(self.x, self.medFilt, label='Median Filtered')
        plt.plot(self.x, self.continuum, label='Continuum')
        plt.plot(self.x, self.continuumRemoved, label='Continuum Removed')
        plt.legend(loc='upper left')
        plt.savefig('Figures/' + title + "Continuum Removal")

    def save_continuum(self, continuumRemoved="continuum_removed.txt", continuum="continuum.txt"):
        np.savetxt('Figures/' + continuumRemoved, np.c_[self.x, self.continuumRemoved, self.continuum])
        #np.savetxt('Figures/' + continuum, np.c_[self.x, self.continuum])


if __name__ == '__main__':
    spectrum = read_fits.read_fits_spectrum1d('celesteB.ms.fits')
    wave1, flux1 = spectrum.dispersion, spectrum.flux
    cR = ContinuumRemoval(wave1, flux1, tuner=20)
    cR.plot_continuum('celesteB')
    cR.save_continuum(continuumRemoved='celesteB_ContinuumRemoved.txt')
    plt.show()