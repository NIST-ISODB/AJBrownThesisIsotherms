# -*- coding: utf-8 -*-
"""Functions to provide the saturation pressure of Xenon and Krypton"""
# pylint: disable-msg=invalid-name   #because I use snake_case
# pylint: disable-msg=no-else-return

from .pressure_units import torr_conversion, bar_conversion


def xenon_psat(T, output_units='bar'):
    """
        Compute the Vapor-(Solid/Liquid) Equilibrium Pressure of Xenon
        Valid Temperature Ranges:
           Solid-Vapour: 110 K < T < 160.56 K
           Liquid-Vapour: 160.56 K < T < 166.2 K
           Liquid-Vapour: 161.70 K < T < 184.70 K
        T: Temperature in Kelvin
        output_units: specify mmHg, bar, atm, Pa, or kPa

        110 K < T < 160.56 K:
        log_10(p_sat/mmHg) = 7.7371 - 779.1/(T/K)

        160.56 K < T < 166.2 K:
        log_10(p_sat/mmHg) = 7.2488 - 720.7/(T/K)

        Reference: M.P. Freeman and G.D. Halsey, J. Phys. Chem. 1956, 60(8), 1119–1125.

        161.70 K < T < 184.70 K

        log_10(p_sat/bar) = 3.80675 - 577.661/(T/K-13.0)

        Reference: A. Michels and T. Wassenaar, Physica (Amsterdam), 1950, 16, 3, 253-256.
        Antoine coefficients were determined by NIST from data in referenced article and supplied
        by the NIST Chemistry WebBook (https://webbook.nist.gov/cgi/cbook.cgi?ID=C7440633)
        on March 2, 2021.
    """

    # Antoine Correlation
    if 110. < T < 160.56:
        conversion_factor = torr_conversion(output_units)
        logPsat = 7.7371 - 799.1 / float(T)
        Psat = (10.**logPsat) * conversion_factor
        return Psat
    elif 160.56 < T < 166.2:
        conversion_factor = torr_conversion(output_units)
        logPsat = 7.24881 - 720.7 / float(T)
        Psat = (10.**logPsat) * conversion_factor
        return Psat
    elif 161.70 < T < 184.70:
        conversion_factor = bar_conversion(output_units)
        logPsat = 3.80675 - 577.661 / (float(T) - 13.)
        Psat = (10.**logPsat) * conversion_factor
        return Psat
    else:
        raise ValueError('Temperature out of range: 110 K < T < 184.70 K')


def krypton_psat(T, output_units='bar'):
    """
        Compute the Vapor-Solid Equilibrium Pressure of Krypton
        Valid Temperature Ranges:
        Solid-Vapour: 115.56 K < T < 121.0 K
        Liquid-Vapour: 87.2 K < T < 115.56 K
        T: Temperature in Kelvin
        output_units: specify mmHg, bar, atm, Pa, or kPa

        115.56 K < T < 121.0 K:
        log_10(p_sat/mmHg) = 6.9861 - 491.9/(T/K)

        87.2 K < T < 115.56 K:
        log_10(p_sat/mmHg) = 7.7447 - 579.6/(T/K)

        Reference: M.P. Freeman and G.D. Halsey, J. Phys. Chem. 1956, 60(8), 1119–1125.
    """

    conversion_factor = torr_conversion(output_units)

    # Antoine Correlation
    if 115.56 < T < 121.0:
        logPsat = 6.9861 - 491.9 / float(T)
        Psat = (10.**logPsat) * conversion_factor
        return Psat
    elif 87.2 < T < 115.56:
        logPsat = 7.7447 - 579.6 / float(T)
        Psat = (10.**logPsat) * conversion_factor
        return Psat
    else:
        raise ValueError('Temperature out of range: 87.2 K < T < 121.0 K')


def saturation_pressure(species, T, output_units='bar'):
    """
    Wrapper function to call species-specific function
    to compute the saturation pressure at a specified temperature

    species: string to identify gas species. Valid values are
             Xe, Xenon, Kr, and Krypton
    T: Temperature in Kelvin
    output_units: specify mmHg, bar, atm, Pa, or kPa
    """

    if species in ('Xe', 'Xenon'):
        return xenon_psat(float(T), output_units)
    elif species in ('Kr', 'Krypton'):
        return krypton_psat(float(T), output_units)
    else:
        raise Exception('ERROR: unknown species for Psat correlation; ' +
                        species)
