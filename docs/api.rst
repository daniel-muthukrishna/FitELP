===
API
===

An application programming interface (API) defines a set of routines to provides access to functions of a software without using a user interface.
FitELP (Fit Emission-Line Profiles) has a few entry points into the API. Following we show the more important classes and methods.

Basic Classes and Methods
-------------------------

* :class:`fitelp.line_profile_info.RegionParameters` - Setup object properties
* :func:`fitelp.line_profile_info.RegionParameters.add_em_line` - Add an emission-line
* :class:`fitelp.kinematics_calculations.RegionCalculations` - Calculate object kinematics


Plotting Methods
----------------

* :func:`fitelp.bpt_plotting.bpt_plot` - Make different types of BPT plots
* :func:`fitelp.fit_line_profiles.plot_profiles` - Plot emission-line profiles and Gaussian fits


Latex Tables Methods
--------------------

* :func:`fitelp.make_latex_tables.average_velocities_table_to_latex` - Make line profile radial velocities and velocity dispersion table
* :func:`fitelp.make_latex_tables.halpha_regions_table_to_latex` - Make object information summary table
* :func:`fitelp.make_latex_tables.comp_table_to_latex` - Make table detailing Gaussian components of each emission-line



The full documentation can be found below.

Full Documentation
------------------

.. autoclass:: fitelp.line_profile_info.RegionParameters
    :members:


------


.. autoclass:: fitelp.kinematics_calculations.RegionCalculations
    :members:


------


.. autofunction:: fitelp.bpt_plotting.bpt_plot


------


.. autofunction:: fitelp.fit_line_profiles.plot_profiles


------


.. autofunction:: fitelp.make_latex_tables.average_velocities_table_to_latex


------


.. autofunction:: fitelp.make_latex_tables.halpha_regions_table_to_latex


------


.. autofunction:: fitelp.make_latex_tables.comp_table_to_latex


