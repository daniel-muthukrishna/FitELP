.. EmissionLineAnalysis documentation master file, created by
   sphinx-quickstart on Fri Jun 14 15:02:56 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

EmissionLineAnalysis Documentation
==================================
EmissionLineAnalysis is a tool specifically designed to perform spectral emission-line fits with multiple gaussian components in echelle or long-slit data. The actual fitting procedure is based on the Non-Linear Least-Square Minimization and Curve-Fitting (LMFIT) package, https://lmfit.github.io/lmfit-py/ (Newville et al. 2014, https://doi.org/10.5281/zenodo.11813).

The Python code was designed for the analysis of the internal kinematics of star-forming regions using echelle data. However, it can be used to model any emission-lines in both in echelle and longslit spectroscopy.

EmissionLineAnalysis allows you to:

* Modelling all individual emission-lines profiles with multiple-gaussian components. 

* Visualise the individual fit of the emission-lines profiles with/without residuals.

* Perform an kinematic analysis of each target.

* Produces pdf and latex tables with the results for each ion on each gaussian component:

   - radial velocities, velocity dispersion, fluxes, emission measure (EM), and global flux, with the corresponding errors.
   
   - Average of radial velocities and velocity dispersion with the corresponding errors.
   
   - H-alpha luminosity and the corresponding Star Formation Rate (SFR) base on ... equation, abscissa and ordinate values of the BPT-NII diagnostic diagram.
   
* Visualise the different BPT diagnostic diagrams. 

* Produces latex tables with the flux, continuum, equivalent width, with the corresponding errors and for each ion.



.. note:: The code is currently still in development, and there may be many issues present. Contact the authors for assistance.


.. toctree::
   :maxdepth: 3
   :caption: Contents:

   installation
   usage
   example
   api

Contribute
----------

- Issue Tracker: https://github.com/daniel-muthukrishna/EmissionLineAnalysis/issues
- Source Code: https://github.com/daniel-muthukrishna/EmissionLineAnalysis

Support
-------

If you are having issues, please let us know by submitting a GitHub issue at https://github.com/daniel-muthukrishna/EmissionLineAnalysis/issues

License
-------

The project is licensed under the MIT license.

Authors
-------
`Daniel Muthukrishna <http://www.danielmuthukrishna.com>`_,
`Verónica Firpo <http://www.gemini.edu/sciops/gemini-research-staff/staff-list#vfirpo>`_
