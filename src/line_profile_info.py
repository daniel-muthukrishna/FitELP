from collections import OrderedDict
import numpy as np
inf = np.inf


class RegionParameters(object):

    def __init__(self, region_name, blue_spec_file, red_spec_file, blue_spec_error_file, red_spec_error_file, scale_flux,
                 center_list, sigma_list, lin_slope, lin_int, num_comps, component_labels, component_colors,
                 sigma_instr_blue, sigma_inst_red, distance, em_lines_for_avg_vel_calc, plotting_x_range=None,
                 plot_residuals=True, show_systemic_velocity=False, systemic_velocity=None):
        """ List information about a region containing multiple emission lines

        Parameters
        ----------
        region_name : str
            Name of object. Do not use underscores in name, as this may affect latex compiling.
        blue_spec_file : str
            FITS file path of the blue spectrum
        red_spec_file : str
            FITS file path of the red spectrum
        blue_spec_error_file : str
            FITS file path of the blue spectrum error
        red_spec_error_file : str
            FITS file path of the red spectrum error
        scale_flux : float
            scales the fluxes from the files by this factor during fitting.            
        center_list : dict
            The center values of the gaussian components for the low-ionization (e.g H-Alpha) and high-ionization (e.g [OIII]5007) zones 
            of each gaussian. These values will depend on the type of fit, if it is in velocity or wavelength.
            E.g. centerList = {'low': [3918.56, 3969.72, 3978.93], 'high': [3923.50, 3970.63, 3984.13]}
        sigma_list : dict
            The sigma values of the gaussian components for the low-ionization (e.g H-Alpha) and high-ionization (e.g [OIII]5007) zones 
            of each gaussian. These values will depend on the type of fit, if it is in velocity or wavelength.
            E.g. sigmaList = {'low': [17.123, 13.868, 45.207],'high': [15.740, 12.875, 43.667]}
        lin_slope : dict
            The linear slope values representing the continuum for the low-ionization (e.g H-Alpha) and high-ionization (e.g [OIII]5007) 
            zones. This value will depend on the type of fit, if it is in velocity or wavelength.
            E.g. lin_slope = {'low': -5.2237e-08, 'high': -2.8976e-07}
        lin_int : dict
            The linear intercept values representing the continuum the low-ionization (e.g H-Alpha) and high-ionization (e.g [OIII]5007) 
            zones. This value will depend on the type of fit, if it is in velocity or wavelength.
            E.g. lin_int = {'low': 0.00139680, 'high': 0.00254310}
        num_comps : dict
            The number of gaussian components for the low-ionization (e.g H-Alpha) and high-ionization (e.g [OIII]5007) zones.
            This should be the length of the lists of the center and sigma of each of the gaussian components
            E.g. num_comps = {'low': 3, 'high': 3} or num_comps = {'low': 3, 'high': 5}
        component_labels : list
            Labels for each of the gaussian components in the order that they are presented in all other lists.
            E.g. component_labels = ['Narrow 1', 'Narrow 2', 'Broad']
        component_colors : list
            Colour to plot each of the gaussian components in the order that they appear in component_labels.
            E.g. componentColours = ['r', 'c', 'g']
        sigma_instr_blue : float
            The instrumental profile (σi) in the blue-arm of the spectrograph. It is well approximated by a single Gaussian function.
        sigma_inst_red : float
            The instrumental profile (σi) in the red-arm of the spectrograph. It is well approximated by a single Gaussian function.
        distance : float
            The distance to the region in centimetres (same units that distance appears in the input flux)
        em_lines_for_avg_vel_calc : list
            The emission lines to use to calculate the average velocity.
            E.g. emLinesForAvgVelCalc = ['H-Alpha', 'H-Beta', 'OIII-5007A', 'NII-6584A', 'SII-6717A']
        plotting_x_range: list or None
            The wavelength (or velocity) range to plot each of the emission line gaussians.
            E.g. plotting_x_range = [3600, 4400]
        plot_residuals : bool
            Whether to plot the residuals of the fit in an extra panel below the gaussian
            Default is True.
        show_systemic_velocity : bool
            Assumed False if it is not defined. If True, the xAxis is plotted
            as the measured velocity minus the systemicVelocity: (velocity - systemicVelocity)
        systemic_velocity : float or None
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

    def add_em_line(self, name, plot_color, order, filter, min_idx, max_idx, rest_wavelength, amp_list, zone, sigma_tsquared, comp_limits, copy_from, num_comps=None):
        """ Emission line info

        Parameters
        ----------
        name : str
            Name of emission line. E.g. 'H-Alpha' or NII-6584A. This name must be in the appropriate format.
            This name must be in the appropriate format (see ALL_IONS list in constants.py).
        plot_color : str
            The color that this emission line should appear in each of the plots.
        order : int
            The order that this emission line appears in the Echelle FITS files or 1 for Longslit FIT file.
        filter : str
            'red' or 'blue'. Indicating the red-arm or blue-arm of the spectrograph where the emission line appears in the spectrum.
        min_idx : int
            Minimum index of the region in the spectra that includes this emission line.
        max_idx : int
            Maximum index of the region in the spectra that includes this emission line.
        rest_wavelength : float
            The rest wavelength of this emission line.
        num_comps : int (optional)
            The number of Gaussian components to fit the emission line.
            This overrides the num_comps set in RegionParameters for this emission line only.
        amp_list: list or float
            The list of amplitudes for each of the components that are included.
            This must be a list with the same number of elements as 'num_comps'.
            If this is a float, then the amplitudes from the emission line listed in the copy_from parameter will be
            used and divided by this value.
        zone : str
            'low' or 'high' ionization zone. Two-ionization-zone scheme is assumed: the low-ionization zone where
            the hydrogen recombination lines and [OI], [OII], [NII], [SII] forbidden lines are emitted, and the
            high-ionization zone where the helium recombination lines and [OIII], [SIII], [ArIII], [NeIII]
            forbidden lines are emitted (Hägele et al., 2012).
        sigma_tsquared : float
            squared of the random thermal motion (σt). In the example, the thermal contribution was derived from the
            Boltzmann’s equation, assuming a typical kinetic temperature T≃10^4K and the atomic mass of the
            corresponding element.
        comp_limits : dict
            The limits in 'compLimits' can be in the following forms:
            - a list indicating the limits for each component
            - a single number indicating the percentage limits for ALL components
            - a tuple (minValue, maxValue) indicating the min and max not in a percentage
            - inf: indicating that the component can vary
            - False: indicating that the value is fixed
        copy_from : str or None or list
            The name of the emission line to copy from. If None, it will not copy any information.
            If it is a list, it must be the length of the number of components you have (as defined in num_comps in
            RegionParameters). Each element of the list must be a string indicating which emission line to
            copy for each component.

        """

        self.emProfiles[name] = {'Colour': plot_color, 'Order': order, 'Filter': filter,
                                 'minI': min_idx, 'maxI': max_idx, 'restWavelength': rest_wavelength,
                                 'numComps': num_comps, 'ampList': amp_list, 'zone': zone,
                                 'sigmaT2': sigma_tsquared, 'compLimits': comp_limits, 'copyFrom': copy_from}


