===
API
===

EmissionLineAnalysis has a few important classes and methods.

Basic Classes and Methods
-------------------------

* :class:`src.line_profile_info.RegionParameters` - Setup region properties
* :func:`src.line_profile_info.RegionParameters.add_em_line` - Add an emission line
* :class:`src.kinematics_calculations.RegionCalculations` - Calculate region kinematics


Plotting Methods
----------------

* :func:`src.bpt_plotting.bpt_plot` - Make different types of BPT plots
* :func:`src.fit_line_profiles.plot_profiles` - Plot emission line profiles and Gaussian fits


Latex Tables Methods
--------------------
* :func:`src.make_latex_tables.average_velocities_table_to_latex` - Make line profile velocities table
* :func:`src.make_latex_tables.halpha_regions_table_to_latex` - Make region information summary table
* :func:`src.make_latex_tables.comp_table_to_latex` - Make table detailing gaussian components of each emission line



The full documentation can be found below.

Full Documentation
------------------

.. autoclass:: src.kinematics_calculations.RegionCalculations
    :members:


------


.. autoclass:: src.line_profile_info.RegionParameters
    :members:


------


.. autofunction:: src.bpt_plotting.bpt_plot


------


.. autofunction:: src.fit_line_profiles.plot_profiles


------


.. autofunction:: src.make_latex_tables.average_velocities_table_to_latex


------


.. autofunction:: src.make_latex_tables.halpha_regions_table_to_latex


------


.. autofunction:: src.make_latex_tables.comp_table_to_latex




