import os
import numpy as np

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../Output_Files')
DATA_FILES = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../Input_Data_Files')

VEL_AXIS_LABEL = r"$\mathrm{Velocity \ (km \ s^{-1}})$"
DELTA_VEL_AXIS_LABEL = r"$\mathrm{\Delta Velocity \ (km \ s^{-1}})$"
WAVE_AXIS_LABEL = r"$\mathrm{Wavelength (\AA)}$"


class FluxUnitsLabels(object):
    def __init__(self, scale_flux):
        _FLUX_UNITS = fr"10^{{{int(np.log10(scale_flux))}}} \ erg \ s^{{{-1}}} \ cm^{{{-2}}}"
        _FLUX_UNITS_WAVE = _FLUX_UNITS + r" \ \AA^{-1}"
        _FLUX_UNITS_VEL = _FLUX_UNITS + r" \ km \ s^{-1}"
        self.FLUX_UNITS_HEADER_WAVE = r"$(\mathrm{" + _FLUX_UNITS_WAVE + r"})$"
        self.FLUX_UNITS_HEADER_VEL = r"$(\mathrm{" + _FLUX_UNITS_VEL + r"})$"
        self.FLUX_VEL_AXIS_LABEL = r"$\mathrm{Flux \ (" + _FLUX_UNITS_VEL + r")}$"
        self.FLUX_WAVE_AXIS_LABEL = r"$\mathrm{Flux \ (" + _FLUX_UNITS_WAVE + r")}$"


ALL_IONS = (('OII-3726A', 3726, '[OII]dob'),
            ('OII-3729A', 3729, '[OII]dob'),
            ('H9-3835A', 3835, 'H9'),
            ('NeIII-3868A', 3868, '[NeIII]'),
            ('H8+HeI-3888A', 3888, 'H8+HeI'),
            ('NeIII+H7-3967A', 3967, '[NeIII]+H7'),
            ('NeIII+Hep-3970A', 3970, '[NeIII]+Hep'),
            ('SII-4068A', 4068, '[SII]'),
            ('H-Delta', 4102, 'Hdelta'),
            ('H-Gamma', 4340, 'Hgamma'),
            ('OIII-4363A', 4363, '[OIII]'),
            ('HeI-4471A', 4471, 'HeI'),
            ('FeIII-4658A', 4658, '[FeIII]'),
            ('HeII-4686A', 4686, 'HeII'),
            ('ArIV+HeI-4713A', 4713, '[ArIV]+HeI'),
            ('ArIV-4740A', 4740, '[ArIV]'),
            ('H-Beta', 4861, 'Hbeta'),
            ('OIII-4959A', 4959, '[OIII]'),
            ('OIII-5007A', 5007, '[OIII]'),
            ('NI-5198A', 5198, '[NI]'),
            ('ClIII-5518A', 5518, '[ClIII]'),
            ('ClIII-5538A', 5538, '[ClIII]'),
            ('NII-5755A', 5755, '[NII]'),
            ('HeI-5876A', 5876, 'HeI'),
            ('OI-6300A', 6300, '[OI]'),
            ('SIII-6312A', 6312, '[SIII]'),
            ('OI-6364A', 6364, '[OI]'),
            ('NII-6548A', 6548, '[NII]'),
            ('H-Alpha', 6563, 'Halpha'),
            ('NII-6584A', 6584, '[NII]'),
            ('HeI-6678A', 6678, 'HeI'),
            ('SII-6717A', 6717, '[SII]'),
            ('SII-6731A', 6731, '[SII]'),
            ('HeI-7065A', 7065, 'HeI'),
            ('ArIII-7136A', 7136, '[ArIII]'),
            ('PI-7250A', 7250, 'PI'),
            ('HeI-7281A', 7281, 'HeI'),
            ('OII-7319A', 7319, '[OII]dob'),
            ('OII-7330A', 7330, '[OII]dob'),
            ('ArIII-7751A', 7751, '[ArIII]'),
            ('P10-9014A', 9014, 'P10'),
            ('SIII-9069A', 9069, '[SIII]'),
            ('SIII-9532A', 9532, '[SIII]'),
            ('Pa5-3-10282A', 10282, 'Pa5-3'))


def init():
    global OUTPUT_DIR
    global DATA_FILES
    global VEL_AXIS_LABEL
    global DELTA_VEL_AXIS_LABEL
    global WAVE_AXIS_LABEL
    global ALL_IONS
