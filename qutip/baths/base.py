""" Base classes for environmental baths. """

from enum import StrEnum


class BathStatistics(StrEnum):
    """
    An enumeration of bath statistics.
    """

    BOSONIC = "bosonic"
    FERMIONIC = "fermionic"


class Bath:
    """
    Base class for representing environment baths.

    Parameters
    ----------
    T : float
        The temperature of the bath.

    Attributes
    ----------
    T : float
        The temperature of the bath.
    statistics: BathStatistics
        The statistics of the bath. Either `BOSONIC` or `FERMIONIC`.
    """

    def __init__(self, T):
        self.T = T

    @property
    def statistics(self):
        raise NotImplementedError(
            "Sub-classes of Bath should provide a .statistics property."
        )

    def spectral_density(self, w):
        """
        Return the spectral density of the bath.

        Parameters
        ----------
        w : array-like or float
            The angular frequencies at which to evaluate the specral density.

        Returns
        -------
        spectral_density: array-like or float
            The spectral density values for each ``w``.

        Notes
        -----
        Note that various conventions for the definition of the spectral
        density exist. We follow the convention:

        XXX: We want to give the integral form here, or perhaps both the
             discrete and integral forms, but definitely not just a
             discrete for in terms of Dirac deltas which makes a bit no
             sense.

        $$
            J(\omega) = \pi \sum_k \left| g_k \right|2 \delta \left( \omega − \omega_k \right).
        $$
        """
        raise NotImplementedError(
            "Sub-classes of Bath should implement .spectral_density()."
        )

    def correlation_function(self, t):
        """
        Return the single-time correlation function of the bath.

        Parameters
        ----------
        t : array-like or float
            The times at which to evaluate the correlation function.

        Returns
        -------
        correlations: array-like or float
            The correlation function values for each ``t``.
        """
        raise NotImplementedError(
            "Sub-classes of Bath should implement .correlation_function()."
        )

    def power_spectrum(self, w):
        """
        Return the power spectrum of the bath.

        Parameters
        ----------
        w : array-like or float
            The energy of each mode for which to evaluate the power spectrum.

        Returns
        -------
        spectrum: array-like or float
            The power spectrum for each mode ``w``.
        """
        raise NotImplementedError(
            "Sub-classes of Bath should implement .power_spectrum()."
        )


class BosonicBath:
    """
    Base class for representing bosonic environments.

    Parameters
    ----------
    T : float
        The temperature of the bath.

    Attributes
    ----------
    T : float
        The temperature of the bath.
    statistics: BathStatistics
        The statistics of the bath, i.e. `BOSONIC`.
    """

    @property
    def statistics(self):
        return BathStatistics.BOSONIC


class FermionicBath:
    """
    Base class for representing fermionic environments.

    Parameters
    ----------
    T : float
        The temperature of the bath.

    Attributes
    ----------
    T : float
        The temperature of the bath.
    statistics: BathStatistics
        The statistics of the bath, i.e. `FERMIONIC`.
    """

    @property
    def statistics(self):
        return BathStatistics.FERMIONIC
