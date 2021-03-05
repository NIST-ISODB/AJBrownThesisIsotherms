# AJ Brown Thesis Isotherms

Repository containing adsorption isotherm data from

**The Thermodynamics and Hystersis of Adsorption**

by A. J. Brown

A Thesis submitted for the degree of Doctor of Philosophy

University of Bristol

October 1963.

Repository Contents:
1. Boundary (equilibrium) Isotherms of Xenon, Krypton, and Carbon Dioxide adsorption on Vycor Glass
2. Scanning Isotherms of Xenon on Vycor Glass at 151 K, including:
- Primary adsorption and desorption scanning isotherms
- Reversals inside the boundary isotherm
- Closed loops inside the boundary isotherm
- Subsidiary closed loops with secondary adsorption and desorption scanning isotherms inside the closed loops
3. Edited versions of (1) and (2) that correct obvious typographic errors
4. Python functions to:
- Extract specific isotherms (boundary or scanning) from the master source data
- Process isotherms to a standardized form, where the adsorption measurement is normalized again adsorbent mass and pressure is converted to nominal units
- Preserve _significant figures_ in all numerical conversions
- Convert the isotherms to the NIST JSON Isotherm format
6. Jupyter notebooks that demonstrate usage of the Python functions in (4) and show example plots of
- Boundary isotherms
- Select sets of scanning isotherms 
