import os
import matplotlib.pyplot as plt
import numpy as np
from lmfit import Parameters
from lmfit.models import GaussianModel, LinearModel
from astropy.constants import c
from label_tools import line_label
import constants

constants.init()


class EmissionLineProfile(object):
    def __init__(self, wave, flux, fluxError, rp, restWave, lineName=''):
        """wave and flux are for vectors representing only the given emission line
        labWave is the wavelength of the emission line if it were at rest (stationary)
        default is for H-alpha emission line"""
        self.restWave = restWave
        self.lineName = lineName
        self.wave = wave
        self.vel, self.flux, self.fluxError = self.velocity(wave, flux, fluxError)
        self.rp = rp

    def velocity(self, wave, flux, fluxError):
        vel = ((wave - self.restWave) / self.restWave) * c.to('km/s').value
        flux = flux * (self.restWave / c.to('km/s').value)
        fluxError = fluxError * (self.restWave / c.to('km/s').value)

        return vel, flux, fluxError

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
    def __init__(self, vel, flux, wave, restWave, lineName, zone, rp, fluxError=None, xAxis='vel'):
        """The input vel and flux must be limited to a single emission line profile"""
        self.vel = vel
        self.flux = flux
        self.fluxError = fluxError
        self.wave = wave
        self.restWave = restWave
        self.lineName = lineName
        self.zone = zone
        self.weights = self._weights()
        self.rp = rp
        self.xAxis = xAxis

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
        print("Amplitude Total is %f" % amplitudeTotal)

        return amplitudeTotal

    def _gaussian_component(self, pars, prefix, c, s, a, limits):
        """Fits a gaussian with given parameters.
        pars is the lmfit Parameters for the fit, prefix is the label of the gaussian, c is the center, s is sigma,
        a is amplitude. Returns the Gaussian model"""
        varyCentre = True
        varySigma = True
        varyAmp = True

        if limits['c'] == False:
            varyCentre = False
            cMin, cMax = -np.inf, np.inf
        elif type(limits['c']) is tuple:
            cMin = limits['c'][0]
            cMax = limits['c'][1]
        else:
            cMin = c - c*limits['c']
            cMax = c + c*limits['c']

        if limits['s'] == False:
            varySigma = False
            sMin, sMax = -np.inf, np.inf
        elif type(limits['s']) is tuple:
            sMin = limits['s'][0]
            sMax = limits['s'][1]
        else:
            sMin = s - s * limits['s']
            sMax = s + s * limits['s']

        if limits['a'] == False:
            varyAmp = False
            aMin, aMax = -np.inf, np.inf
        elif type(limits['a']) is tuple:
            aMin = limits['a'][0]
            aMax = limits['a'][1]
        else:
            aMin = a - a * limits['a']
            aMax = a + a * limits['a']

        g = GaussianModel(prefix=prefix)
        pars.update(g.make_params())
        pars[prefix + 'center'].set(c, min=cMin, max=cMax, vary=varyCentre)
        pars[prefix + 'sigma'].set(s, min=sMin, max=sMax, vary=varySigma)
        pars[prefix + 'amplitude'].set(a, min=aMin, max=aMax, vary=varyAmp)

        return g

    def lin_and_multi_gaussian(self, numOfComponents, cList, sList, aList, lS, lI, limits):
        """All lists should be the same length"""
        gList = []

        lin = LinearModel(prefix='lin_')
        self.linGaussParams = lin.guess(self.flux, x=self.vel)
        self.linGaussParams.update(lin.make_params())
        self.linGaussParams['lin_slope'].set(lS, vary=True)
        self.linGaussParams['lin_intercept'].set(lI, vary=True)

        for i in range(numOfComponents):
            if type(limits['c']) is list:
                cLimit = limits['c'][i]
            else:
                cLimit = limits['c']
            if type(limits['s']) is list:
                sLimit = limits['s'][i]
            else:
                sLimit = limits['s']
            if type(limits['a']) is list:
                aLimit = limits['a'][i]
            else:
                aLimit = limits['a']
            lims = {'c': cLimit, 's': sLimit, 'a': aLimit}
            gList.append(self._gaussian_component(self.linGaussParams,'g%d_' % (i+1), cList[i], sList[i], aList[i], lims))
        gList = np.array(gList)
        mod = lin + gList.sum()

        init = mod.eval(self.linGaussParams, x=self.vel)
        out = mod.fit(self.flux, self.linGaussParams, x=self.vel, weights=self.weights)
        f = open(os.path.join(constants.OUTPUT_DIR, self.rp.regionName, "{0}_Log.txt".format(self.rp.regionName)), "a")
        print("######## %s %s Linear and Multi-gaussian Model ##########\n" % (self.rp.regionName, self.lineName))
        print(out.fit_report())
        f.write("######## %s %s Linear and Multi-gaussian Model ##########\n" % (self.rp.regionName, self.lineName))
        f.write(out.fit_report())
        f.close()
        components = out.eval_components()

        self.plot_emission_line(numOfComponents, components, out)

        self._get_amplitude(numOfComponents, out)

        return out, components

    def plot_emission_line(self, numOfComponents, components, out):
        ion, lambdaZero = line_label(self.lineName, self.restWave)
        plt.figure("%s %s %s" % (self.rp.regionName, ion, lambdaZero))
        plt.title("%s %s" % (ion, lambdaZero))

        if self.xAxis == 'wave':
            x = self.wave
            xLabel = r"$\mathrm{Wavelength (\AA)}$"
        elif self.xAxis == 'vel':
            x = self.vel
            xLabel = r"$\mathrm{Velocity \ (km \ s^{-1}})$"
            plt.xlim(self.rp.plottingXRange)

        plt.xlabel(xLabel)
        plt.ylabel(r"$\mathrm{Flux \ (10^{-14} \ erg \ s^{-1} \ cm^{-2} \ (km \ s^{-1})^{-1})}$")
        plt.plot(x, self.flux, label='Data')
        for i in range(numOfComponents):
            labelComp = self.rp.componentLabels  # 'g%d_' % (i+1)
            plt.plot(x, components['g%d_' % (i+1)]+components['lin_'], color=self.rp.componentColours[i], linestyle=':', label=labelComp[i])
        # plt.plot(x, components['lin_'], label='lin_')
        plt.plot(x, out.best_fit, color='black', linestyle='--', label='Fit')
        # plt.plot(x, init, label='init')
        plt.legend(loc='upper left')
        plt.savefig(os.path.join(constants.OUTPUT_DIR, self.rp.regionName, self.lineName + " {0} Component Linear-Gaussian Model".format(numOfComponents)))


def plot_profiles(lineNames, rp, nameForComps='', title='', sortedIndex=None):
    try:
        plt.figure(title)
        ax = plt.subplot(1, 1, 1)
        plt.title(title)  # Recombination Emission Lines")
        plt.xlabel(r"$\mathrm{Velocity \ (km \ s^{-1})}$")
        plt.ylabel(r"$\mathrm{Flux \ (10^{-14} \ erg \ s^{-1} \ cm^{-2} \ (km \ s^{-1})^{-1})}$")
        for i in range(len(lineNames)):
            name, x, y, mod, col, comps, lab = rp.emProfiles[lineNames[i]]['plotInfo']
            ax.plot(x, y, color=col, label=lab)
            ax.plot(x, mod, color=col, linestyle='--')
            if name == nameForComps:
                for idx in range(rp.emProfiles[lineNames[i]]['numComps']):
                    plt.plot(x, comps['g%d_' % (idx + 1)] + comps['lin_'], color=rp.componentColours[idx], linestyle=':')
        plt.xlim(rp.plottingXRange)
        if sortedIndex is not None:
            handles, labels = ax.get_legend_handles_labels()
            handles2 = [handles[idx] for idx in sortedIndex]
            labels2 = [labels[idx] for idx in sortedIndex]
            ax.legend(handles2, labels2)
        else:
            ax.legend()
        plt.savefig(os.path.join(constants.OUTPUT_DIR, rp.regionName, title.strip(' ') + '.png'))
    except KeyError:
        print("SOME IONS IN {0} HAVE NOT BEEN DEFINED.".format(lineNames))
