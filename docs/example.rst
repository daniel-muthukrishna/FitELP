=======
Example
=======

Example script of fitting multiple gaussian components in the emission line profiles of a star forming region.

.. code-block:: python

    import os
    import sys
    import numpy as np
    import matplotlib.pyplot as plt
    import scripts.constants as constants
    from scripts.make_latex_tables import average_velocities_table_to_latex, halpha_regions_table_to_latex
    from scripts.bpt_plotting import bpt_plot
    from scripts.kinematics_calculations import RegionCalculations
    from scripts.fit_line_profiles import plot_profiles
    from scripts.line_profile_info import RegionParameters

    # Path to the directory you wish to save the ouput plots, tables and results.
    constants.OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Output_Files')

    # Path to the directory containing your input data files (Optional).
    constants.DATA_FILES = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Input_Data_Files')

    # Set up example region to simultaneously fit multiple emission lines
    example_region_1 = RegionParameters(region_name='example-region-1',
                                        blue_spec_file='HCG31-C_B.fc.fits',
                                        red_spec_file='HCG31-C_R.fc.fits',
                                        blue_spec_error_file='HCG31-C_B_ErrorFlux.fc.fits',
                                        red_spec_error_file='HCG31-AC_R_ErrorFlux.fc.fits',
                                        scale_flux=1e14, 
                                        center_list={'low': [3913.84913, 3974.23343, 4008.05142],
                                                     'high': [3917.96597, 3975.09343, 4008.40610]},
                                        sigma_list={'low': [12.7749777, 42.8190718, 86.5794988],
                                                    'high': [10.4442012, 38.0769644, 78.1337966]},
                                        lin_slope={'low': -4.0088e-08, 'high':-2.8765e-07},
                                        lin_int={'low':  0.00138487, 'high': 0.00254777},
                                        num_comps={'low': 3, 'high': 3},
                                        component_labels=['Narrow 1', 'Narrow 2', 'Broad'],
                                        component_colors=['b', 'r', 'g'],
                                        plotting_x_range=[3600, 4400], # velocities range
                                        sigma_instr_blue=5.0, #intrumental dispersion in the blue arm
                                        sigma_inst_red=6.2, #intrumental dispersion in the red arm
                                        distance=1.67e26, # Distance to region in centimetres
                                        em_lines_for_avg_vel_calc=['H-Alpha', 'H-Beta_Blue', 'OIII-5007A', 'NII-6584A', 'SII-6717A'],
                                        plot_residuals=False, # or True
                                        show_systemic_velocity=False, # Assumed False if not defined
                                        systemic_velocity=4074 # Required only if showSystemicVelocity is True
                                        )

    # Add emission lines to fit
    example_region_1.add_em_line(name='H-Alpha', plot_color='y', order=20, filter='red', min_idx=2931, max_idx=3360, rest_wavelength=6562.82, amp_list=[0.578836, 12.2318292, 5.5107925], zone='low', sigma_tsquared=164.96, comp_limits={'a': np.inf, 'c': np.inf, 's': np.inf}, copy_from=None)
    example_region_1.add_em_line(name='OIII-5007A', plot_color='c', order=4, filter='red', min_idx=2300, max_idx=3440, rest_wavelength=5006.84, amp_list=[0.4929977, 8.9210534, 5.8227902], zone='high',sigma_tsquared=10.39, comp_limits={'a': np.inf, 'c': np.inf, 's': np.inf}, copy_from=None)
    example_region_1.add_em_line(name='OIII-4959A', plot_color='g', order=4, filter='red', min_idx=1080, max_idx=2000, rest_wavelength=4958.91, amp_list=[0.1641313, 2.9082207, 1.8938379], zone='high',sigma_tsquared=10.39, comp_limits={'a': np.inf, 'c': False, 's': False}, copy_from='OIII-5007A')
    example_region_1.add_em_line(name='H-Beta', plot_color='b', order=36, filter='blue', min_idx=370, max_idx=1613, rest_wavelength=4861.33, amp_list=[0.1964884, 3.1738928, 1.7306038], zone='low',sigma_tsquared=164.96, comp_limits={'a': np.inf, 'c': False, 's': False}, copy_from='H-Alpha')
    example_region_1.add_em_line(name='NII-6584A', plot_color='violet', order=20, filter='red', min_idx=3361, max_idx=3885, rest_wavelength=6583.41, amp_list=[0.0436704, 1.0825264, 0.5998283], zone='low',sigma_tsquared=11.87, comp_limits={'a': np.inf, 'c': False, 's': False}, copy_from='H-Alpha')
    example_region_1.add_em_line(name='NII-6548A', plot_color='#441E16', order=20, filter='red', min_idx=2563, max_idx=2930, rest_wavelength=6548.03, amp_list=0.0133341, 0.3745197, 0.1492923], zone='low',sigma_tsquared=11.87, comp_limits={'a': np.inf, 'c': False, 's': False}, copy_from='NII-6584A')
    example_region_1.add_em_line(name='SII-6717A', plot_color='r', order=22, filter='red', min_idx=508, max_idx=985, rest_wavelength=6716.47, amp_list=[0.0576321, 0.7924302, 0.4728445], zone='low',sigma_tsquared=5.19, comp_limits={'a': np.inf, 'c': [(3913.8,3917.9),(3974.2,3975.1),(4008.1,4008.4)], 's': [(10.4,12.8),(38.1,42.8),(78.1,86.6)]}, copy_from='H-Alpha')
    example_region_1.add_em_line(name='SII-6731A', plot_color='#58D68D', order=22, filter='red', min_idx=986, max_idx=1290, rest_wavelength=6730.85, amp_list=[0.0350009, 0.6037486, 0.3466657], zone='low',sigma_tsquared=5.19, comp_limits={'a': np.inf, 'c': False, 's': False}, copy_from='SII-6717A')
    example_region_1.add_em_line(name='H-Gamma', plot_color='r', order=27, filter='blue', min_idx=1400, max_idx=2350, rest_wavelength=4340.47, amp_list=[0.0922511, 1.3853307, 0.5964586], zone='low',sigma_tsquared=164.96, comp_limits={'a': np.inf, 'c': False, 's': False}, copy_from='H-Beta')
    example_region_1.add_em_line(name='H-Delta', plot_color='c', order=22, filter='blue', min_idx=2055, max_idx=3000, rest_wavelength=4101.74, amp_list=[0.0922511, 1.3853307, 0.5964586], zone='low',sigma_tsquared=164.96, comp_limits={'a': np.inf, 'c': False, 's': False}, copy_from='H-Beta')
    example_region_1.add_em_line(name='SIII-9069A', plot_color='#27AE60', order=35, filter='red', min_idx=485, max_idx=881, rest_wavelength=9068.9, amp_list=[0.0323302, 1.2445037, 0.4540262], zone='low',sigma_tsquared=5.19, comp_limits={'a': np.inf, 'c': False, 's': False}, copy_from='H-Alpha')

    # You may fit multiple regions by adding extra region objects to this list
    regions_parameters = [example_region_1,]

    region_array = []
    rp_bpt_points, rp_bpt_points_s, rp_bpt_points_o, rp_bpt_points_p = [], [], [], []
    for rp in regions_parameters:
        region = RegionCalculations(rp, xAxis='vel', initVals='vel')
        region_array.append(region.lineInArray)
        rp_bpt_points.append(region.bptPoints)
        rp_bpt_points_s.append(region.bptPoints_s)
        rp_bpt_points_o.append(region.bptPoints_o)
        rp_bpt_points_p.append(region.bptPoints_p)

        plot_profiles(['H-Alpha', 'OIII-5007A', 'H-Beta', 'NII-6584A', 'SII-6717A'], rp, nameForComps='SII-6717A',
                      title=rp.regionName + ' Strongest Emission Lines', sortedIndex=[0, 1, 2, 3, 4], logscale=True,
                      ymin=None)

    bpt_plot(regions_parameters, rp_bpt_points, plot_type='n')
    bpt_plot(regions_parameters, rp_bpt_points_s, plot_type='s')
    bpt_plot(regions_parameters, rp_bpt_points_o, plot_type='o')
    bpt_plot(regions_parameters, rp_bpt_points_p, plot_type='p')
    halpha_regions_table_to_latex(region_array, paperSize='a4', orientation='portrait', longTable=False)
    average_velocities_table_to_latex(regions_parameters, paperSize='a4', orientation='landscape', longTable=False)

    plt.show()


