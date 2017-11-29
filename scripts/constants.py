import os

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../Output_Files')
DATA_FILES = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../Input_Data_Files')

FLUX_VEL_AXIS_LABEL = r"$\mathrm{Flux \ (10^{-14} \ erg \ s^{-1} \ cm^{-2} \ (km \ s^{-1})^{-1})}$"
FLUX_WAVE_AXIS_LABEL = r"$\mathrm{Flux \ (10^{-14} \ erg \ s^{-1} \ cm^{-2})}$"
VEL_AXIS_LABEL = r"$\mathrm{Velocity \ (km \ s^{-1}})$"
DELTA_VEL_AXIS_LABEL = r"$\mathrm{\Delta Velocity \ (km \ s^{-1}})$"
WAVE_AXIS_LABEL = r"$\mathrm{Wavelength (\AA)}$"


def init():
    global OUTPUT_DIR
    global DATA_FILES
    global FLUX_VEL_AXIS_LABEL
    global FLUX_WAVE_AXIS_LABEL
    global VEL_AXIS_LABEL
    global DELTA_VEL_AXIS_LABEL
    global WAVE_AXIS_LABEL
