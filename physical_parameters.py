import os
import numpy as np
import csv
import re


def read_fluxes_file(regionName):
    fluxListInfo = []

    with open(os.path.join(regionName, "component_fluxes.csv")) as csvFile:
        reader = csv.reader(csvFile)
        rowNum = 0
        for row in reader:
            if rowNum != 0:
                fluxListInfo.append(row)
            rowNum += 1

    print(np.array(fluxListInfo))
    return fluxListInfo


def get_component_fluxes(fluxListInfo, componentName):
    componentFluxes = []
    for i in range(len(fluxListInfo)):
        emName, componentLabel, flux, fluxErr = fluxListInfo[i]
        if componentName == componentLabel:
            componentFluxes.append((emName, flux, fluxErr))

    return componentFluxes


def line_name_to_pyneb_format(lineName):
    """ Takes a line name in the form similar to OIII-5007A or H-Alpha
    and returns the pyneb format: H1e_6563A.
    This function is basic and assumes tha the letter 'I' in the lineName are used only for roman numerals
    """

    if 'H-Alpha' in lineName:
        atomName, ionNumber, restWave = 'H', '1r', '6563A'
    elif 'H-Beta' in lineName:
        atomName, ionNumber, restWave = 'H', '1r', '4861A'
    elif 'H-Gamma' in lineName:
        atomName, ionNumber, restWave = 'H', '1r', '4341A'
    elif 'H-Delta' in lineName:
        atomName, ionNumber, restWave = 'H', '1r', '4102A'
    elif 'HeIH8' in lineName:
        atomName, ionNumber, restWave = 'He', '1r', lineName.split('-')
    elif 'I-' in lineName or 'IV-' in lineName:
        ionName, restWave = lineName.split('-')
        ionNumber = '4' if 'IV' in ionName else str(ionName.count('I'))
        atomName = ionName.split('I')[0]
        restWave = restWave.split('_')[0]
    else:
        print("Unknown lineName type: %s" % lineName)
        return("XX_XXXXX")

    pynebName = "{0}{1}_{2}".format(atomName, ionNumber, restWave)

    return pynebName


def normalise_to_hbeta():
    pass


if __name__ == '__main__':
    fluxList = read_fluxes_file("Mrk600A")
    fluxesNarrow1 = get_component_fluxes(fluxList, 'Narrow 1')
    print("\n")
    print(np.array(fluxesNarrow1))

    print(line_name_to_pyneb_format("H-Alpha"))
    print(line_name_to_pyneb_format("OIII-4959A_Red"))
    print(line_name_to_pyneb_format("NII-6584A"))
