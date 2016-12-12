import numpy as np 
# from lmfit.models import GaussianModel, LinearModel, PolynomialModel
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
		x and y are an array of the wavelengths and fluxes of each of the orders
		"""
		x = []
		y = []
		spectra =  read_fits.read_fits_spectrum1d(filename)#, dispersion_unit=u.angstrom, flux_unit=u.cgs.erg/u.angstrom/u.cm**2/u.s)
		for spectrum in spectra:
			x.append(spectrum.dispersion/u.angstrom)
			y.append(spectrum.flux*1e14)
		x = np.array(x)
		y = np.array(y)

		return x, y

	def plot_order(self, orderNum, filter='red', minIndex=0, maxIndex=-1, title=''):
		"""Plots the wavelength vs flux for a particular order.
		orderNum starts from 0"""

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
		labWave is the wavelenght of the emission line if it were at rest (stationary)
		default is for H-alpha emission line"""
		self.restWave = restWave
		self.wave = wave
		self.flux = flux
		self.vel = self._velocity(wave)
		if lineName == 'Halpha':
			self.restWave = 6562.82 #angstroms

	def _velocity(self, wave):
		return ((wave - self.restWave)/self.restWave) * const.c/1000

	def plot_emission_line(self, xaxis='vel', title=''):
		"""Choose whether the x axis is 'vel' or 'wave'"""
		plt.figure(title)
		if xaxis == wave:
			plt.plot(self.wave,flux)
			plt.xlabel("Wavelength ($\AA$)")
		elif xaxis == 'vel':
			plt.plot(self.vel, flux)
			plt.xlabel("Velocity ($km s^{-1}$)")
		plt.ylabel("Flux")
		plt.title(title)




			




if __name__ == '__main__':
	ngc6845_7 = GalaxyRegion('NGC6845_7B.fc.fits', 'NGC6845_7R.fc.fits')
	#ngc6845_7.plot_order(20, filter='red', maxIndex=-10, title="NGC6845_7_red Order 21")

	####Spectral Line Info - for H-alpha####
	orderNum = 20
	filter = 'red'
	minIndex = 1180
	maxIndex = 1650
	wave, flux = ngc6845_7.mask_emission_line(20, filter=filter, minIndex=minIndex, maxIndex=maxIndex)

	HAlphaLine = EmissionLineProfile(wave, flux, lineName='Halpha')
	HAlphaLine.plot_emission_line(xaxis='vel', title='H-alpha emission line for NGC6845_7')

	plt.show()