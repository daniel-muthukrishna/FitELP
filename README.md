# EmissionLineAnalysis
Fit emission profiles with multiple gaussian components. Takes echelle data as an input

Currently this project was designed for the analysis of the internal kinematics of giant star forming regions in interacting galaxies. Data is from the MIKE spectrograph.
However, it can be used to model any emission lines in echelle spectra.

## NOTES ON HOW TO MAKE THE INPUT GALAXY REGION INFORMATION TABLES
If using long slit data, set the 'Order' to 1.

The limits in 'compLimits' can be in the following forms:
    
    - a list indicating the limits for each component
    - a single number indicating the percentage limits for ALL components
    - a tuple (minValue, maxValue) indicating the min and max not in a percentage
    - inf: indicating that the component cannot vary
    - False: indicating that the value is fixed

ampList
    
    - if not list it will be take the copyFrom amplitude List and divide by the ampList scalar

numComps:
    
    - If numComps is not listed in the emProfile dictionary, then the number of components will be taken from the
    numComps variable depending on the zone set in the emProfile dictionary
    
showSystemicVelocity

    - Optional Variable. Assumed False if it is not defined. If True, the xAxis is plotted as the measured velocity minus the systemicVelocity
      velocity - systemicVelocity
    
systemicVelocity
    
    - Required if showSystemicVelocity is True.
 
