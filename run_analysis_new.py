import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import src.constants as constants
from src.make_latex_tables import average_velocities_table_to_latex, halpha_regions_table_to_latex
from src.bpt_plotting import bpt_plot
from src.kinematics_calculations import RegionCalculations
from src.fit_line_profiles import plot_profiles
from src.line_profile_info import RegionParameters


sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Input_Galaxy_Region_Information'))
constants.OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Output_Files')
constants.DATA_FILES = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Input_Data_Files')


example_region_1 = RegionParameters(region_name='example-region-1',
                                    blue_spec_file='HCG31-C_B.fc.fits',
                                    red_spec_file='HCG31-C_R.fc.fits',
                                    blue_spec_error_file='HCG31-C_B_ErrorFlux.fc.fits',
                                    red_spec_error_file='HCG31-AC_R_ErrorFlux.fc.fits',
                                    scale_flux=1e14,
                                    center_list={'low': [3918.56152, 3978.93476, 4009.07339],
                                                 'high': [3923.50164, 3984.13367, 4013.03660]},
                                    sigma_list={'low': [15.7405389, 43.6674545, 88.1013490],
                                                'high': [15.7405389, 43.6674545, 88.1013490]},
                                    lin_slope={'low': -4.0088e-08, 'high': -2.8976e-07},
                                    lin_int={'low': 0.00138487, 'high': 0.00254310},
                                    num_comps={'low': 3, 'high': 3},
                                    component_labels=['Narrow 1', 'Narrow 2', 'Broad'],
                                    component_colors=['r', 'c', 'g'],
                                    plotting_x_range=[3600, 4400],
                                    sigma_instr_blue=5.0,
                                    sigma_inst_red=6.2,
                                    distance=1.67e26,
                                    em_lines_for_avg_vel_calc=['H-Alpha', 'H-Beta_Blue', 'OIII-5007A', 'NII-6584A', 'SII-6717A'],
                                    plot_residuals=False,
                                    show_systemic_velocity=False,
                                    systemic_velocity=4000
                                    )

example_region_1.add_em_line(name='H-Alpha', plot_color='y', order=20, filter='red', min_idx=2931, max_idx=3360, rest_wavelength=6562.82, amp_list=[1.1393854, 8.58, 4.8228556], zone='low', sigma_tsquared=164.96, comp_limits={'a': np.inf, 'c': np.inf, 's': np.inf}, copy_from=None)
example_region_1.add_em_line(name='OIII-5007A', plot_color='c', order=4, filter='red', min_idx=2300, max_idx=3440, rest_wavelength=5006.84, amp_list=[1.1548058, 8.5919068, 4.2634018], zone='high',sigma_tsquared=10.39, comp_limits={'a': np.inf, 'c': np.inf, 's': np.inf}, copy_from=None)
example_region_1.add_em_line(name='OIII-4959A', plot_color='g', order=4, filter='red', min_idx=1080, max_idx=2000, rest_wavelength=4958.91, amp_list=[0.3902536, 2.7844993, 1.3837819], zone='high',sigma_tsquared=10.39, comp_limits={'a': np.inf, 'c': False, 's': False}, copy_from='OIII-5007A')
example_region_1.add_em_line(name='H-Beta', plot_color='b', order=36, filter='blue', min_idx=370, max_idx=1613, rest_wavelength=4861.33, amp_list=[0.1402979, 3.2042614, 1.7970957], zone='low',sigma_tsquared=164.96, comp_limits={'a': np.inf, 'c': 0.1, 's': 0.1}, copy_from='H-Alpha')
example_region_1.add_em_line(name='NII-6584A', plot_color='violet', order=20, filter='red', min_idx=3361, max_idx=3885, rest_wavelength=6583.41, amp_list=[0.1004451, 1.0586795, 0.5316711], zone='low',sigma_tsquared=11.87, comp_limits={'a': np.inf, 'c': 0.1, 's': 0.1}, copy_from='H-Alpha')
example_region_1.add_em_line(name='NII-6548A', plot_color='violet', order=20, filter='red', min_idx=2563, max_idx=2930, rest_wavelength=6548.03, amp_list=[0.0324588, 1.0586795, 0.5316711], zone='low',sigma_tsquared=11.87, comp_limits={'a': np.inf, 'c': False, 's': False}, copy_from='NII-6584A')
example_region_1.add_em_line(name='SII-6717A', plot_color='r', order=22, filter='red', min_idx=508, max_idx=985, rest_wavelength=6716.47, amp_list=[0.0972848, 0.7574605, 0.4679219], zone='low',sigma_tsquared=5.19, comp_limits={'a': np.inf, 'c': 1, 's': 1}, copy_from='H-Alpha')
example_region_1.add_em_line(name='SII-6731A', plot_color='#58D68D', order=22, filter='red', min_idx=986, max_idx=1290, rest_wavelength=6730.85, amp_list=[0.0324219, 0.6733394, 0.2678776], zone='low',sigma_tsquared=5.19, comp_limits={'a': np.inf, 'c': 1, 's': 1}, copy_from='SII-6717A')
example_region_1.add_em_line(name='H-Gamma', plot_color='r', order=27, filter='blue', min_idx=1625, max_idx=2183, rest_wavelength=4340.47, amp_list=[0.1402979, 3.2042614, 1.7970957], zone='low',sigma_tsquared=164.96, comp_limits={'a': np.inf, 'c': False, 's': False}, copy_from='H-Beta')
example_region_1.add_em_line(name='H-Delta', plot_color='c', order=22, filter='blue', min_idx=2390, max_idx=2810, rest_wavelength=4101.74, amp_list=[0.1402979, 3.2042614, 1.7970957], zone='low',sigma_tsquared=164.96, comp_limits={'a': np.inf, 'c': False, 's': False}, copy_from='H-Beta')
example_region_1.add_em_line(name='SIII-9069A', plot_color='#27AE60', order=35, filter='red', min_idx=485, max_idx=881, rest_wavelength=9068.9, amp_list=[0.0807574, 1.0986008, 0.5388915], zone='low',sigma_tsquared=5.19, comp_limits={'a': np.inf, 'c': 0.001, 's': 0.1}, copy_from='H-Alpha')


def main():
    regions_parameters = [example_region_1]

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


if __name__ == '__main__':
    main()
