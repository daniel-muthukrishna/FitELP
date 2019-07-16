import csv
import os
import sys
import numpy as np
from src.label_tools import line_name_to_pyneb_format

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../Output_Files')


def read_fluxes_file(regionName):
    fluxListInfo = []

    with open(os.path.join(OUTPUT_DIR, regionName, "component_fluxes.csv")) as csvFile:
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
