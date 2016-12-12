import numpy as np 
# from lmfit.models import GaussianModel, LinearModel, PolynomialModel
# import sys
# import math
import matplotlib.pyplot as plt 
# from astropy.io import fits 
import astropy.units as u 
from specutils.io import read_fits


class GalaxyRegion(object):
	def __init__(self, specFileBlue, specFileRed):
		self.xBlue, self.yBlue = self.read_spectra(specFileBlue)
		self.xRed, self.yRed = self.read_spectra(specFileRed)

	def read_spectra(self, filename):
		""" Reads spectra from input FITS File
		Stores the wavelength (in Angstroms) in a vector 'x'
		and the fluxes scaled by 10**14 in a vector 'y'
		x and y are an array of the wavelengths and fluxes of each of the orders
		"""
		x = []
		y = []

		spectra =  read_fits.read_fits_spectrum1d(filename)

		for spectrum in spectra:
			x.append(spectrum.dispersion/u.angstrom)
			y.append(spectrum.flux*1e14)

		x = np.array(x)
		y = np.array(y)

		return x, y

	def plot_order(self, orderNum, filter='red', minIndex=0, maxIndex=-1):
		"""Plots the wavelength vs flux for a particular order.
		orderNum starts from 0"""

		x, y = self._filter_argument(filter)

		plt.plot(x[orderNum][minIndex:maxIndex], y[orderNum][minIndex:maxIndex])
		plt.show()

	def mask_emission_line(self, orderNum, filter='red', minIndex=0, maxIndex=-1):
		x, y = self._filter_argument(filter)

		return x[minIndex:maxIndex], y[minIndex:maxIndex]

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
			



try:
	pass
except Exception as e:
	raise e



if __name__ == '__main__':
	ngc6845_7 = GalaxyRegion('NGC6845_7B.fc.fits', 'NGC6845_7R.fc.fits')
	ngc6845_7.plot_order(20, filter=4, minIndex=1180, maxIndex=1650)

