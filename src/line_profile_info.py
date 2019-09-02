from collections import OrderedDict
import numpy as np
inf = np.inf


class RegionParameters(object):

    def __init__(self, region_name, blue_spec_file, red_spec_file, blue_spec_error_file, red_spec_error_file, scale_flux,
                 center_list, sigma_list, lin_slope, lin_int, num_comps, component_labels, component_colors,
                 plotting_x_range, sigma_instr_blue, sigma_inst_red, distance, em_lines_for_avg_vel_calc,
                 plot_residuals=True, show_systemic_velocity=False, systemic_velocity=None):
        """ List information about a region containing multiple emission lines

        Parameters
        ----------
        region_name : str
            Name of galaxy region. Do not use underscores in name, as this may affect latex compiling.
        blue_spec_file : str
            FITS file path of the blue spectrum
        red_spec_file : str
            FITS file path of the red spectrum
        blue_spec_error_file : str
            FITS file path of the blue spectrum error
        red_spec_error_file : str
            FITS file path of the red spectrum
        scale_flux : float
            scale the fluxes form the files by this factor during fitting
        center_list : dict
            The center values of the gaussians for the low (H-Alpha) and high (OIII) zones of each gaussian.
            E.g. centerList = {'low': [3918.56, 3969.72, 3978.93], 'high': [3923.50, 3970.63, 3984.13]}
        sigma_list : dict
            The sigma values of the gaussians for the low (H-Alpha) and high (OIII) zones of each gaussian.
            E.g. sigmaList = {'low': [17.123, 13.868, 45.207],'high': [15.740, 12.875, 43.667]}
        lin_slope : dict
            The linear slope values representing the continuum for the low (H-Alpha) and high (OIII) zones.
            E.g. lin_slope = {'low': -5.2237e-08, 'high': -2.8976e-07}
        lin_int : dict
            The linear intercept values representing the continuum for the low (H-Alpha) and high (OIII) zones.
            E.g. lin_int = {'low': 0.00139680, 'high': 0.00254310}
        num_comps : dict
            The number of components for the low (H-Alpha) and high (OIII).
            This should be the length of the lists of the center and sigma of each of the guassian components
            E.g. num_comps = {'low': 3, 'high': 3}
        component_labels : list
            Labels for each of the components in the order that they are presented in all other lists.
            E.g. component_labels = ['Narrow 1', 'Narrow 2', 'Broad']
        component_colors : list
            Colour to plot each of the components in the order that they appear in component_labels.
            E.g. componentColours = ['r', 'c', 'g']
        plotting_x_range: list
            The wavelength (or velocity) range to plot each of the emission line gaussians.
            E.g. plotting_x_range = [3600, 4400]
        sigma_instr_blue : float
            The instrument sigma in the blue arm.
        sigma_inst_red : float
            The instrument sigma in the blue arm.
        distance : float
            The distance to the region in centimetres (same units that distance appears in the input flux)
        em_lines_for_avg_vel_calc : list
            The emission lines to use to calculate the average velocity.
            E.g. emLinesForAvgVelCalc = ['H-Alpha', 'H-Beta', 'OIII-5007A', 'NII-6584A', 'SII-6717A']
        plot_residuals : bool
            Whether to plot the residuals of the fit in an extra panel below the gaussian
            Default is True.
        show_systemic_velocity : bool
            Assumed False if it is not defined. If True, the xAxis is plotted
            as the measured velocity minus the systemicVelocity: (velocity - systemicVelocity)
        systemic_velocity : float
            Required if show_systemic_velocity is True.
        """

        self.regionName = region_name
        self.blueSpecFile = blue_spec_file
        self.blueSpecError = blue_spec_error_file
        self.redSpecFile = red_spec_file
        self.redSpecError = red_spec_error_file
        self.scaleFlux = scale_flux
        self.centerList = center_list
        self.sigmaList = sigma_list
        self.linSlope = lin_slope
        self.linInt = lin_int
        self.numComps = num_comps
        self.componentLabels = component_labels
        self.componentColours = component_colors
        self.plottingXRange = plotting_x_range
        self.sigmaInstrBlue = sigma_instr_blue
        self.sigmaInstrRed = sigma_inst_red
        self.distance = distance
        self.emLinesForAvgVelCalc = em_lines_for_avg_vel_calc
        self.plotResiduals = plot_residuals
        self.showSystemicVelocity = show_systemic_velocity
        self.systemicVelocity = systemic_velocity

        self.emProfiles = OrderedDict()

    def add_em_line(self, name, plot_color, order, filter, min_idx, max_idx, rest_wavelength, amp_list, zone, sigma_tsquared, comp_limits, copy_from):
        """ Emission line info

        Parameters
        ----------
        name : str
            Name of emission line. E.g. 'H-Alpha' or NII-6584A. This name must be in the appropriate format.
        plot_color : str
            The color that this emission line should appear in each of the plots.
        order : int
            The order that this emission line appears in the Echelee FITS files.
        filter : str
            'red' or 'blue'. Indicating the filter that this emission line appears in the echelle spectra.
        min_idx : int
            Minimum index of the region in the echelle spectra that includes this emission line.
        max_idx : int
            Maximum index of the region in the echelle spectra that includes this emission line.
        rest_wavelength : float
            The rest wavelength of this emission line.
        amp_list: list or float
            The list of amplitudes for each of the components that are included.
            This must be a list with the same number of elements as 'num_comps'.
            If this is a float, then the amplitudes from the emission line listed in the copy_from parameter will be
            used and divided by this value.
        zone : str
            'low' or 'high'.
        sigma_tsquared : float
            sigma of the temperature squared
        comp_limits : dict
            The limits in 'compLimits' can be in the following forms:
            - a list indicating the limits for each component
            - a single number indicating the percentage limits for ALL components
            - a tuple (minValue, maxValue) indicating the min and max not in a percentage
            - inf: indicating that the component cannot vary
            - False: indicating that the value is fixed
        copy_from : str or None
            The name of the emission line top copy from. If None, it will not copy any information

        """
        self.emProfiles[name] = {'Colour': plot_color, 'Order': order, 'Filter': filter,
                                 'minI': min_idx, 'maxI': max_idx, 'restWavelength': rest_wavelength,
                                 'ampList': amp_list, 'zone': zone, 'sigmaT2': sigma_tsquared,
                                 'compLimits': comp_limits, 'copyFrom': copy_from}


