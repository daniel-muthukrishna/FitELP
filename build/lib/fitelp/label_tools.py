

def line_name_to_pyneb_format(lineName):
    """ Takes a line name in the form similar to OIII-5007A or H-Alpha
    and returns the pyneb format: H1r_6563A.
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


def line_label(emLineName, emRestWave):
    if 'I' in emLineName or 'H-' in emLineName:
        ion, lambdaZero = line_label_roman_numeral_format(emLineName, emRestWave)
    else:
        ion, lambdaZero = line_label_pyneb_format(emLineName)

    return ion, lambdaZero


def line_label_roman_numeral_format(emLineName, emRestWave):
    if emLineName in ['H-Alpha', 'H-Beta', 'H-Gamma', 'H-Delta']:
        lambdaZero = '$%s$' % str(int(round(emRestWave)))
        if emLineName == 'H-Alpha':
            ion = r"$\mathrm{H}\alpha$"
        elif emLineName == 'H-Beta':
            ion = r"$\mathrm{H}\beta$"
        elif emLineName == 'H-Gamma':
            ion = r"$\mathrm{H}\gamma$"
        elif emLineName == 'H-Delta':
            ion = r"$\mathrm{H}\delta$"
    elif emLineName == 'H-Beta_Blue':
        lambdaZero = '$%s$' % str(int(round(emRestWave)))
        ion = r"$\mathrm{H}\beta$ - Blue"
    elif emLineName == 'H-Beta_Red':
        lambdaZero = '$%s$' % str(int(round(emRestWave)))
        ion = r"$\mathrm{H}\beta$ - Red"
    elif 'He' in emLineName:
        lambdaZero = '$%s$' % emLineName.split('-')[1][:-1]
        ion = r"$\mathrm{%s}$" % emLineName.split('-')[0]
    else:
        lambdaZero = '$%s$' % emLineName.split('-')[1][:-1]
        ion = r"$\mathrm{[%s]}$" % emLineName.split('-')[0]

    return ion, lambdaZero


def line_label_pyneb_format(emLineName):
    ion, lambdaZero = emLineName.split('_')
    if 'H1r_6563A' in emLineName:
        ion = r"$\mathrm{H}\alpha$"
    elif 'H1r_4861A' in emLineName:
        ion = r"$\mathrm{H}\beta$"
    elif 'H1r_4341A' in emLineName:
        ion = r"$\mathrm{H}\gamma$"
    elif 'H1r_4102A' in emLineName:
        ion = r"$\mathrm{H}\delta$"
    else:
        ion = ion.strip('r')
        atomName, ionNumber = ion[:-1], ion[-1]
        if int(ionNumber) == 4:
            romanNumeral = 'IV'
        else:
            romanNumeral = 'I' * int(ionNumber)
        ion = r"$\mathrm{[{%s}{%s}]}$" % (atomName, romanNumeral)
    lambdaZero = lambdaZero.strip('A')

    return ion, lambdaZero
