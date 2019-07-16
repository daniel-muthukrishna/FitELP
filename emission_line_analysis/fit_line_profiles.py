import os
import matplotlib.pyplot as plt
import numpy as np
from lmfit import Parameters
from lmfit.models import GaussianModel, LinearModel
from astropy.constants import c
from emission_line_analysis.label_tools import line_label
import emission_line_analysis.constants as constants

constants.init()


def vel_to_wave(restWave, vel, flux, fluxError=None, delta=False):
    if delta is True:
        wave = (vel / c.to('km/s').value) * restWave
    else:
        wave = (vel / c.to('km/s').value) * restWave + restWave
    flux = flux / (restWave / c.to('km/s').value)
    if fluxError is not None:
        fluxError = fluxError / (restWave / c.to('km/s').value)
        return vel, flux, fluxError
    else:
        return wave, flux


def wave_to_vel(restWave, wave, flux, fluxError=None, delta=False):
    if delta is True:
        vel = (wave / restWave) * c.to('km/s').value
    else:
        vel = ((wave - restWave) / restWave) * c.to('km/s').value
    flux = flux * (restWave / c.to('km/s').value)
    if fluxError is not None:
        fluxError = fluxError * (restWave / c.to('km/s').value)
        return vel, flux, fluxError
    else:
        return vel, flux


class FittingProfile(object):
    def __init__(self, wave, flux, restWave, lineName, zone, rp, fluxError=None, xAxis='vel', initVals='vel'):
        """The input vel and flux must be limited to a single emission line profile"""
        self.flux = flux
        self.fluxError = fluxError
        self.restWave = restWave
        self.lineName = lineName
        self.zone = zone
        self.weights = self._weights()
        self.rp = rp
        self.xAxis = xAxis
        self.initVals = initVals

        if xAxis == 'vel':
            if fluxError is None:
                vel, self.flux = wave_to_vel(restWave, wave, flux)
            else:
                vel, self.flux, self.fluxError = wave_to_vel(restWave, wave, flux, fluxError)
            self.x = vel
        else:
            self.x = wave

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

        if limits['c'] is False:
            varyCentre = False
            cMin, cMax = -np.inf, np.inf
        elif type(limits['c']) is tuple:
            cMin = limits['c'][0]
            cMax = limits['c'][1]
        else:
            cMin = c - c*limits['c']
            cMax = c + c*limits['c']

        if limits['s'] is False:
            varySigma = False
            sMin, sMax = -np.inf, np.inf
        elif type(limits['s']) is tuple:
            sMin = limits['s'][0]
            sMax = limits['s'][1]
        else:
            sMin = s - s * limits['s']
            sMax = s + s * limits['s']

        if limits['a'] is False:
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
        if isinstance(c, str):
            pars[prefix + 'center'].set(expr=c, min=cMin, max=cMax, vary=varyCentre)
        else:
            pars[prefix + 'center'].set(c, min=cMin, max=cMax, vary=varyCentre)
        if isinstance(s, str):
            pars[prefix + 'sigma'].set(expr=s, min=sMin, max=sMax, vary=varySigma)
        else:
            pars[prefix + 'sigma'].set(s, min=sMin, max=sMax, vary=varySigma)
        if isinstance(a, str):
            pars[prefix + 'amplitude'].set(expr=a, min=aMin, max=aMax, vary=varyAmp)
        else:
            pars[prefix + 'amplitude'].set(a, min=aMin, max=aMax, vary=varyAmp)

        return g

    def multiple_close_emission_lines(self, lineNames, cListInit, sListInit, lS, lI):
        """All lists should be the same length"""
        gList = []

        # Assume initial parameters are in velocity

        lin = LinearModel(prefix='lin_')
        self.linGaussParams = lin.guess(self.flux, x=self.x)
        self.linGaussParams.update(lin.make_params())
        self.linGaussParams['lin_slope'].set(lS, vary=True)
        self.linGaussParams['lin_intercept'].set(lI, vary=True)

        for j, lineName in enumerate(lineNames):
            numComps = self.rp.emProfiles[lineName]['numComps']
            restWave = self.rp.emProfiles[lineName]['restWavelength']
            copyFrom = self.rp.emProfiles[lineName]['copyFrom']
            if copyFrom is not None:
                copyFromRestWave = self.rp.emProfiles[copyFrom]['restWavelength']

                cList = ['g{0}{1}_center*{2}'.format(copyFrom.replace('-', ''), (i + 1), (restWave / copyFromRestWave)) for i in range(numComps)]
                sList = ['g{0}{1}_sigma'.format(copyFrom.replace('-', ''), i + 1) for i in range(numComps)]

                if type(self.rp.emProfiles[lineName]['ampList']) is list:
                    aList = self.rp.emProfiles[lineName]['ampList']
                    if self.xAxis == 'vel':
                        aList = vel_to_wave(restWave, vel=0, flux=np.array(aList))[1]
                else:
                    ampRatio = self.rp.emProfiles[lineName]['ampList']
                    aList = ['g{0}{1}_amplitude*{2}'.format(copyFrom.replace('-', ''), i + 1, ampRatio) for i in range(numComps)]

            else:
                cList = vel_to_wave(restWave, vel=np.array(cListInit), flux=0)[0]
                sList = vel_to_wave(restWave, vel=np.array(sListInit), flux=0, delta=True)[0]
                aListInit = self.rp.emProfiles[lineName]['ampList']
                aList = vel_to_wave(restWave, vel=0, flux=np.array(aListInit))[1]

            limits = self.rp.emProfiles[lineName]['compLimits']
            for i in range(numComps):
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
                if len(lineNames) == 1:
                    prefix = 'g{0}_'.format(i + 1)
                else:
                    prefix = 'g{0}{1}_'.format(lineName.replace('-', ''), i + 1)
                gList.append(self._gaussian_component(self.linGaussParams, prefix, cList[i], sList[i], aList[i], lims))
        gList = np.array(gList)
        mod = lin + gList.sum()

        init = mod.eval(self.linGaussParams, x=self.x)
        out = mod.fit(self.flux, self.linGaussParams, x=self.x, weights=self.weights)
        f = open(os.path.join(constants.OUTPUT_DIR, self.rp.regionName, "{0}_Log.txt".format(self.rp.regionName)), "a")
        print("######## %s %s Linear and Multi-gaussian Model ##########\n" % (self.rp.regionName, self.lineName))
        print(out.fit_report())
        f.write("######## %s %s Linear and Multi-gaussian Model ##########\n" % (self.rp.regionName, self.lineName))
        f.write(out.fit_report())
        f.close()
        components = out.eval_components()

        if not hasattr(self.rp, 'plotResiduals'):
            self.rp.plotResiduals = True
        numComps = self.rp.emProfiles[lineName]['numComps']
        self.plot_emission_line(numComps, components, out, self.rp.plotResiduals, lineNames, init=init)

        return out, components

    def lin_and_multi_gaussian(self, numOfComponents, cList, sList, aList, lS, lI, limits):
        """All lists should be the same length"""
        gList = []

        if self.xAxis == 'wave' and self.initVals == 'vel':
            cList = vel_to_wave(self.restWave, vel=np.array(cList), flux=0)[0]
            sList = vel_to_wave(self.restWave, vel=np.array(sList), flux=0, delta=True)[0]
            aList = vel_to_wave(self.restWave, vel=0, flux=np.array(aList))[1]
        elif self.xAxis == 'vel' and self.initVals == 'wave':
            cList = wave_to_vel(self.restWave, wave=np.array(cList), flux=0)[0]
            sList = wave_to_vel(self.restWave, wave=np.array(sList), flux=0, delta=True)[0]
            aList = wave_to_vel(self.restWave, wave=0, flux=np.array(aList))[1]

        lin = LinearModel(prefix='lin_')
        self.linGaussParams = lin.guess(self.flux, x=self.x)
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
            prefix = 'g{0}_'.format(i+1)
            gList.append(self._gaussian_component(self.linGaussParams, prefix, cList[i], sList[i], aList[i], lims))
        gList = np.array(gList)
        mod = lin + gList.sum()

        init = mod.eval(self.linGaussParams, x=self.x)
        out = mod.fit(self.flux, self.linGaussParams, x=self.x, weights=self.weights)
        f = open(os.path.join(constants.OUTPUT_DIR, self.rp.regionName, "{0}_Log.txt".format(self.rp.regionName)), "a")
        print("######## %s %s Linear and Multi-gaussian Model ##########\n" % (self.rp.regionName, self.lineName))
        print(out.fit_report())
        f.write("######## %s %s Linear and Multi-gaussian Model ##########\n" % (self.rp.regionName, self.lineName))
        f.write(out.fit_report())
        f.close()
        components = out.eval_components()

        if not hasattr(self.rp, 'plotResiduals'):
            self.rp.plotResiduals = True
        self.plot_emission_line(numOfComponents, components, out, self.rp.plotResiduals, init=init)

        self._get_amplitude(numOfComponents, out)

        return out, components

    def plot_emission_line(self, numOfComponents, components, out, plotResiduals=True, lineNames=None, init=None):
        ion, lambdaZero = line_label(self.lineName, self.restWave)
        fig = plt.figure("%s %s %s" % (self.rp.regionName, ion, lambdaZero))
        if plotResiduals is True:
            frame1 = fig.add_axes((.1, .3, .8, .6))

        plt.title("%s %s" % (ion, lambdaZero))

        if self.xAxis == 'wave':
            x = self.x
            xLabel = constants.WAVE_AXIS_LABEL
            yLabel = constants.FLUX_WAVE_AXIS_LABEL
        elif self.xAxis == 'vel':
            if hasattr(self.rp, 'showSystemicVelocity') and self.rp.showSystemicVelocity is True:
                x = self.x - self.rp.systemicVelocity
                xLabel = constants.DELTA_VEL_AXIS_LABEL
            else:
                x = self.x
                xLabel = constants.VEL_AXIS_LABEL
            if hasattr(self.rp, 'rp.plottingXRange'):
                plt.xlim(self.rp.plottingXRange)
            yLabel = constants.FLUX_VEL_AXIS_LABEL
        else:
            raise Exception("Invalid xAxis argument. Must be either 'wave' or 'vel'. ")

        plt.plot(x, self.flux, label='Data')
        for i in range(numOfComponents):
            labelComp = self.rp.componentLabels
            if lineNames is None:
                plt.plot(x, components['g%d_' % (i+1)]+components['lin_'], color=self.rp.componentColours[i], linestyle=':', label=labelComp[i])
            else:
                for j, lineName in enumerate(lineNames):
                    plt.plot(x, components['g{0}{1}_'.format(lineName.replace('-', ''), i + 1)] + components['lin_'], color=self.rp.componentColours[i], linestyle=':', label=labelComp[i])
        # plt.plot(x, components['lin_'], label='lin_')
        plt.plot(x, out.best_fit, color='black', linestyle='--', label='Fit')
        # plt.plot(x, init, label='init')
        plt.legend(loc='upper left')
        plt.ylabel(yLabel)

        if plotResiduals is True:
            frame1 = plt.gca()
            frame1.axes.get_xaxis().set_visible(False)
            frame2 = fig.add_axes((.1, .1, .8, .2))
            plt.plot(x, self.flux - out.best_fit)
            plt.axhline(y=0, linestyle='--', color='black')
            plt.ylabel('Residuals')
            plt.locator_params(axis='y', nbins=3)
        plt.xlabel(xLabel)

        plt.savefig(os.path.join(constants.OUTPUT_DIR, self.rp.regionName, self.lineName + " {0} Component Linear-Gaussian Model".format(numOfComponents)), bbox_inches='tight')


def plot_profiles(lineNames, rp, nameForComps='', title='', sortedIndex=None, plotAllComps=False, xAxis='vel', logscale=False, ymin=None):
    try:
        plt.figure(title)
        ax = plt.subplot(1, 1, 1)
        plt.title(title)  # Recombination Emission Lines")

        if xAxis == 'wave':
            xLabel = constants.WAVE_AXIS_LABEL
            yLabel = constants.FLUX_WAVE_AXIS_LABEL
        elif xAxis == 'vel':
            if hasattr(rp, 'showSystemicVelocity') and rp.showSystemicVelocity is True:
                xLabel = constants.DELTA_VEL_AXIS_LABEL
            else:
                xLabel = constants.VEL_AXIS_LABEL
            if hasattr(rp, 'rp.plottingXRange'):
                plt.xlim(rp.plottingXRange)
            yLabel = constants.FLUX_VEL_AXIS_LABEL
        else:
            raise Exception("Invalid xAxis argument. Must be either 'wave' or 'vel'. ")
        plt.xlabel(xLabel)
        plt.ylabel(yLabel)

        for i in range(len(lineNames)):
            name, x, flux, mod, col, comps, lab = rp.emProfiles[lineNames[i]]['plotInfo']
            if xAxis == 'vel' and hasattr(rp, 'showSystemicVelocity') and rp.showSystemicVelocity is True:
                x = x - rp.systemicVelocity
            ax.plot(x, flux, color=col, label=lab)
            ax.plot(x, mod, color=col, linestyle='--')
            if plotAllComps is True:
                for idx in range(rp.emProfiles[lineNames[i]]['numComps']):
                    plt.plot(x, comps['g%d_' % (idx + 1)] + comps['lin_'], color=rp.componentColours[idx], linestyle=':')
            else:
                if name == nameForComps:
                    for idx in range(rp.emProfiles[lineNames[i]]['numComps']):
                        plt.plot(x, comps['g%d_' % (idx + 1)] + comps['lin_'], color=rp.componentColours[idx], linestyle=':')
        if sortedIndex is not None:
            handles, labels = ax.get_legend_handles_labels()
            handles2 = [handles[idx] for idx in sortedIndex]
            labels2 = [labels[idx] for idx in sortedIndex]
            ax.legend(handles2, labels2)
        else:
            ax.legend()

        if logscale is True:
            ax.set_yscale('log')
        if ymin is not None:
            ax.set_ylim(bottom=ymin)

        plt.savefig(os.path.join(constants.OUTPUT_DIR, rp.regionName, title.strip(' ') + '.png'), bbox_inches='tight')
    except KeyError:
        print("SOME IONS IN {0} HAVE NOT BEEN DEFINED.".format(lineNames))
