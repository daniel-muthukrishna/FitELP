import os
import sys
import matplotlib.pyplot as plt
from scripts.make_latex_tables import average_velocities_table_to_latex, halpha_regions_table_to_latex
from scripts.bpt_plotting import bpt_plot
from scripts.kinematics_calculations import RegionCalculations
from scripts.fit_line_profiles import plot_profiles
import scripts.constants as constants

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Input_Galaxy_Region_Information'))


def main():
    from Input_Galaxy_Region_Information.profile_info_HCG31_A import RegionParameters as HCG31_AParams
    from Input_Galaxy_Region_Information.profile_info_HCG31_C import RegionParameters as HCG31_CParams
    from Input_Galaxy_Region_Information.profile_info_HCG31_AC import RegionParameters as HCG31_ACParams
    from Input_Galaxy_Region_Information.profile_info_NGC6845_Region26NewDisp import RegionParameters as NGC6845Region26NewDispParams
    from Input_Galaxy_Region_Information.profile_info_NGC6845_Region26_35 import RegionParameters as NGC6845Region26_35Params
    from Input_Galaxy_Region_Information.profile_info_NGC6845_Region26_37 import RegionParameters as NGC6845Region26_37Params
    from Input_Galaxy_Region_Information.profile_info_NGC6845_Region26_39 import RegionParameters as NGC6845Region26_39Params
    from Input_Galaxy_Region_Information.profile_info_Arp314_NED02_off import RegionParameters as Arp314_NED02_offParams
    from Input_Galaxy_Region_Information.profile_info_Arp314_NED02 import RegionParameters as Arp314_NED02Params
    #from Input_Galaxy_Region_Information.profile_info_Obj1 import RegionParameters as Obj1
    # from Input_Galaxy_Region_Information.IMrk600A import RegionParameters as Mrk600AParams
    # from Input_Galaxy_Region_Information.Mrk600B import RegionParameters as Mrk600B05Params
    # from Input_Galaxy_Region_Information.IIZw33KnotB05 import RegionParameters as IIZw33KnotBParams
    # from Input_Galaxy_Region_Information.profile_info_NGC6845_Region7 import RegionParameters as NGC6845Region7Params
    # from Input_Galaxy_Region_Information.profile_info_NGC6845_Region26 import RegionParameters as NGC6845Region26Params
    # from Input_Galaxy_Region_Information.profile_info_NGC6845_Region26_Counts import RegionParameters as NGC6845Region26Params

    regionsParameters = [HCG31_ACParams]#, HCG31_CParams, HCG31_AParams]#[Arp314_NED02Params,Arp314_NED02_offParams]#[NGC6845Region26NewDispParams], NGC6845Region26_37Params, NGC6845Region26_39Params, NGC6845Region26NewDispParams], # NGC6845Region7Params, NGC6845Region26Params]#

    constants.OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Output_Files')
    constants.DATA_FILES = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Input_Data_Files')

    regionArray = []
    rpBptPoints = []
    for rp in regionsParameters:
        region = RegionCalculations(rp)
        regionArray.append(region.lineInArray)
        rpBptPoints.append(region.bptPoints)

        plot_profiles(['H-Alpha', 'OIII-5007A', 'H-Beta', 'NII-6584A', 'SII-6717A'], rp, nameForComps='SII-6717A', title=rp.regionName + ' Strongest Emission Lines', sortedIndex=[0, 1, 2, 3, 4])
        #plot_profiles(['H-Beta', 'H-Beta_Red'], rp, nameForComps='H-Beta', title=rp.regionName + 'Hbeta Emission Lines', sortedIndex=[0, 1])

    bpt_plot(regionsParameters, rpBptPoints)
    halpha_regions_table_to_latex(regionArray, paperSize='a4', orientation='portrait', longTable=False)
    average_velocities_table_to_latex(regionsParameters, paperSize='a4', orientation='landscape', longTable=False)

    plt.show()

if __name__ == '__main__':
    main()
