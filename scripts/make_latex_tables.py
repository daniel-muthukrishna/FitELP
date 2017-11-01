import os

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../Output_Files')


def table_to_latex(tableArray, headingLines, saveFileName, directory, caption, centering, papersize='a4', orientation='portrait', longTable=False):
    texFile = open(os.path.join(directory, saveFileName + '.tex'), 'w')
    texFile.write('\\documentclass{article}\n')
    texFile.write('\\usepackage[%spaper, %s, margin=0.5in]{geometry}\n' % (papersize, orientation))
    texFile.write('\\usepackage{booktabs}\n')
    texFile.write('\\usepackage{longtable}\n')
    texFile.write('\\begin{document}\n')
    texFile.write('\n')
    texFile.write('\\begin{longtable}{%s}\n' % (centering))
    texFile.write('\\hline\n')
    for heading in headingLines[:-1]:
        texFile.write(' & '.join(str(e) for e in heading) + ' \\\\ \n')
    texFile.write(' & '.join("\\scriptsize " + str(e) for e in headingLines[-1]) + ' \\\\ \n')
    texFile.write('\\hline\n')
    if longTable:
        texFile.write('\\endhead\n')
    for line in tableArray:
        texFile.write(' & '.join(str(e) for e in line) + ' \\\\ \n')
    texFile.write('\\hline\n')
    texFile.write('\\caption{%s}\n' % caption)
    texFile.write('\\end{longtable}\n')
    texFile.write('\n')
    texFile.write('\\end{document}\n')

    texFile.close()

    run_bash_command("pdflatex '" + os.path.join(directory, saveFileName + ".tex'"))
    if directory != ".":
        run_bash_command("mv " + saveFileName + ".pdf '" + directory + "'")
        run_bash_command("rm " + saveFileName + ".*")


def average_velocities_table_to_latex(rpList, directory=OUTPUT_DIR, paperSize='a4', orientation='portrait', longTable=False):
    saveFileName = 'AverageVelocitiesTable'
    velArray = calc_average_velocities(rpList)
    regionHeadings = ['']
    headings = ['']
    headingUnits = ['']
    for rp in rpList:
        regionHeadings += ["\multicolumn{2}{c}{%s}" % rp.regionName]  # Was 2 instead of 3 when i didn;t have separate component Labels
        headings += [r'$\mathrm{v_r}$', r'$\mathrm{\sigma}$']
        headingUnits += [r'$\mathrm{(km \ s^{-1})}$', r'$\mathrm{(km \ s^{-1})}$']

    headingLines = [regionHeadings, headings, headingUnits]
    caption = "Average radial velocities and velocity dispersions for all regions"
    nCols = len(headings)
    centering = 'l' + 'c' * (nCols-1)
    table_to_latex(velArray, headingLines, saveFileName, directory, caption, centering, paperSize, orientation, longTable)


def halpha_regions_table_to_latex(regionInfoArray, directory=OUTPUT_DIR, paperSize='a4', orientation='portrait', longTable=False):
    saveFileName = 'RegionInfo'
    headings = [r'Region Name', r'SFR', r'$\mathrm{log(L(H}\alpha))$', r'$\mathrm{log([NII]/H}\alpha)$', r'$\mathrm{log([OIII]/H}\beta)$']
    headingUnits = ['', r'$(\mathrm{M_{\odot} \ yr^{-1}})$', '', '', '']
    headingLines = [headings, headingUnits]
    caption = 'Region Information'
    nCols = len(headings)
    centering = 'l' + 'c' * (nCols-1)
    table_to_latex(regionInfoArray, headingLines, saveFileName, directory, caption, centering, paperSize, orientation, longTable)


def comp_table_to_latex(componentArray, rp, paperSize='a4', orientation='portrait', longTable=True):
    saveFileName = 'ComponentTable'
    directory = os.path.join(OUTPUT_DIR, rp.regionName)
    headings = [r'$\mathrm{\lambda_0}$', r'$\mathrm{Ion}$', r'$\mathrm{Comp.}$', r'$\mathrm{v_r}$',
                r'$\mathrm{\sigma_{int}}$', r'$\mathrm{Flux}$', r'$\mathrm{EM_f}$', r'$\mathrm{GlobalFlux}$']
    headingUnits = [r'$(\mathrm{\AA})$', '', '', r'$(\mathrm{km \ s^{-1}})$',
                    r'$(\mathrm{km \ s^{-1}})$', r'$(\mathrm{10^{-14} \ erg \ s^{-1} \ cm^{-2} \ (km \ s^{-1})^{-1}})$',
                    '', r'$(\mathrm{10^{-14} \ erg \ s^{-1} \ cm^{-2} \ (km \ s^{-1})^{-1}})$']
    headingLines = [headings, headingUnits]
    caption = rp.regionName
    nCols = len(headings)
    centering = 'lllccccc'
    table_to_latex(componentArray, headingLines, saveFileName, directory, caption, centering, paperSize, orientation, longTable)


def run_bash_command(bashCommandStr):
    os.system(bashCommandStr)
    # process = subprocess.Popen(bashCommandStr.split(), stdout=subprocess.PIPE)
    # output, error = process.communicate(input='\n')
