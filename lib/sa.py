"""
Driver for SignalHound USB SA-124B
"""
import numpy as np
from sadevice.sa_api import *

class SpectrumAnalyzer:
    """Driver for SignalHound Spectrum Analuzer
    """
    def __init__(self):
        self.handle = sa_open_device()["handle"]
        self.averaging = 1
        sa_set_timebase(self.handle, SA_REF_INTERNAL_OUT)

    def setup(self, rbw, vbw):
        """Performs the setup for the SA.

        Arguments:
            rbw (float): Resolution bandwidth.
            vbw (float) Video bandwidth.
        """
        sa_config_acquisition(self.handle, SA_AVERAGE, SA_LOG_SCALE)
        sa_config_gain_atten(self.handle, SA_AUTO_GAIN, SA_AUTO_ATTEN, 0)
        sa_config_sweep_coupling(self.handle, rbw, vbw, True)

    def set_power(self, power):
        """Sets the power reference level.
        
        Arguments:
            power (float): Ref level in dBm.
        """
        sa_config_level(self.handle, power)

    def fetch_xarray(self):
        """Fetches the frequencies measured.

        Returns:
            frequencies (np.array): Array of frequencies at which the SA has measured in Hz.
        """
        query = sa_query_sweep_info(self.handle)

        sweep_length = query["sweep_length"]
        start_freq = query["start_freq"]
        bin_size = query["bin_size"]
        return np.array([start_freq + i * bin_size for i in range(sweep_length)])

    def scan(self, center_frequency, span):
        """Performs a scan of the SA about a center frequency with a given span.

        Arguments:
            center_frequency (float): Center frequency of the scan in Hz.
            span (float): Frequency span of the scan.

        Returns:
            res (np.array): Array of power detected at each frequency scanned in dBm.
        """

        sa_config_center_span(self.handle, center_frequency, span)
        res = sa_get_sweep_32f(self.handle)["max"]
        return res

    def close(self):
        sa_close_device(self.handle)
