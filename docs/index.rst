.. EmissionLineAnalysis documentation master file, created by
   sphinx-quickstart on Fri Jun 14 15:02:56 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

EmissionLineAnalysis
====================
EmissionLineAnalysis is a powerful Python code to perform spectral emission line fits with multiple gaussian components in echelle or long-slit data. The fitting procedure is based around the code lmfit, https://lmfit.github.io/lmfit-py/.

Currently this project was designed for the analysis of the internal kinematics of star forming regions using MIKE echelle spectrograph data of Las Campanas Observatory, Chile. However, it can be used to model any emission lines in echelle or long-slit spectroscopy.

The code is currently still in development, and there may be many issues present. Contact the authors for assistance.

An example fit to an emission line is shown below.

.. image:: Figures/example_emission_line_fit.png

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
Federico Campuzano Castro,
`Verónica Firpo <http://www.gemini.edu/sciops/gemini-research-staff/staff-list#vfirpo>`_
