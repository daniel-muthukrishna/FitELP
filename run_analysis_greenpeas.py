import os
import sys
import matplotlib.pyplot as plt
from emission_line_analysis.make_latex_tables import average_velocities_table_to_latex, halpha_regions_table_to_latex
from emission_line_analysis.bpt_plotting import bpt_plot
from emission_line_analysis.kinematics_calculations import RegionCalculations
from emission_line_analysis.fit_line_profiles import plot_profiles
import emission_line_analysis.constants as constants

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Input_Galaxy_Region_Information'))


def main():
    from Input_Galaxy_Region_Information.profile_info_Obj1 import RegionParameters as Obj1Params

    regionsParameters = [Obj1Params]

    constants.OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Output_Files_Green_Peas')
    constants.DATA_FILES = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Input_Data_Files')

    regionArray = []
    rpBptPoints = []
    for rp in regionsParameters:
        region = RegionCalculations(rp, xAxis='vel', initVals='vel')
        regionArray.append(region.lineInArray)
        rpBptPoints.append(region.bptPoints)

        plot_profiles(['OIII-5007A', 'H-Alpha', 'H-Beta', 'NII-6584A', 'SII-6717A'], rp, nameForComps='SII-6717A', title=rp.regionName + ' Strongest Emission Lines', sortedIndex=[0, 1, 2, 3, 4], xAxis='wave')

    bpt_plot(regionsParameters, rpBptPoints)
    halpha_regions_table_to_latex(regionArray, paperSize='a4', orientation='portrait', longTable=False)
    average_velocities_table_to_latex(regionsParameters, paperSize='a4', orientation='landscape', longTable=False)

    plt.show()

if __name__ == '__main__':
    main()
