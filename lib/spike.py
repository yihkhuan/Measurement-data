


"""
Driver for SignalHound USB SA-124B
"""
import numpy as np
from sadevice.sa_api import *
import matplotlib.pyplot as plt

class SpectrumAnalyzer:
    """Driver for SignalHound Spectrum Analuzer
    """
    def __init__(self):
        self.handle = sa_open_device()["handle"]
        try:
            sa_attach_tg()
        except:
            pass
        
    def setup(self, centre, span, level):
        sa_config_center_span(self.handle, centre, span)
        # sa_config_gain_atten(self.handle, SA_AUTO_ATTEN, SA_AUTO_GAIN)
        sa_config_level(self.handle, level)
        sa_config_sweep_coupling(self.handle, 10e3, 10e3, False)
        sa_config_acquisition(self.handle, SA_MIN_MAX, SA_LOG_SCALE)

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
    
    def scan(self, parameters:tuple = None):
        """Performs a scan of the SA about a center frequency with a given span.

        Arguments:
            parameter[0] = center_frequency (float): Center frequency of the scan in Hz.
            parameter1] = span (float): Frequency span of the scan.

        Returns:
            res (np.array): Array of power detected at each frequency scanned in dBm.
        """
        if parameters:
            sa_config_center_span(self.handle, *parameters)

        res = sa_get_sweep_32f(self.handle)["min"]
        return res
    
    def stor_thru(self, flag: int):
        sa_store_tg_thru(self.handle, flag)

    def tg_sweep_points(self, number_of_points):
        sa_config_tg_sweep(self.handle, number_of_points, True, True)
        sa_initiate(self.handle, SA_TG_SWEEP, 0)
    
    def close(self):
        sa_close_device(self.handle)

    def level(self, level):
        sa_config_level(self.handle, level)