# FitELP 
FitELP is a tool specifically designed to perform spectral emission-line fits with multiple gaussian components in echelle or long-slit data. The actual fitting procedure is based on the Non-Linear Least-Square Minimization and Curve-Fitting (LMFIT) package, https://lmfit.github.io/lmfit-py/ (Newville et al. 2014, https://doi.org/10.5281/zenodo.11813).

This Python code was designed for the analysis of the internal kinematics of star-forming regions using echelle data. However, it can be used to model any emission-lines in both in echelle and longslit spectroscopy.

For full documentation, please go to https://fitelp.readthedocs.io/

# Installation
```bash
    git clone https://github.com/daniel-muthukrishna/fitelp.git
    cd FitELP
    python setup.py install
```
