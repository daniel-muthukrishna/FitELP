import os
import sys
import matplotlib.pyplot as plt
from make_latex_tables import average_velocities_table_to_latex, halpha_regions_table_to_latex
from bpt_plotting import bpt_plot
from kinematics_calculations import RegionCalculations
import constants

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Input_Galaxy_Region_Information'))


def main():
    from Input_Galaxy_Region_Information.profile_info_Obj1 import RegionParameters as Obj1Params

    regionsParameters = [Obj1Params]

    constants.OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Output_Files_Green_Peas')
    constants.DATA_FILES = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Input_Data_Files')

    regionArray = []
    rpBptPoints = []
    for regParam in regionsParameters:
        region = RegionCalculations(regParam, xAxis='wave')
        regionArray.append(region.lineInArray)
        rpBptPoints.append(region.bptPoints)

    bpt_plot(regionsParameters, rpBptPoints)
    halpha_regions_table_to_latex(regionArray, paperSize='a4', orientation='portrait', longTable=False)
    average_velocities_table_to_latex(regionsParameters, paperSize='a4', orientation='landscape', longTable=False)

    plt.show()

if __name__ == '__main__':
    main()
