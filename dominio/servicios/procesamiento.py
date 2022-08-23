# -*- coding: utf-8 -*-
"""

Monitor Holter

"""
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import threading
import serial
import argparse
import time
from scipy import signal
from abc import abstractmethod, ABCMeta, ABC
from datetime import date, datetime

class ABSFilter(metaclass=ABCMeta):
    def __init__(self):
        self._f0 = None
        self._n = None
        self._fc1 = None
        self._fc2 = None
        self._num = None
        self._den = None
        self._q = None
        self._fs= None

    @abstractmethod
    def filter():
        pass

class BandpassMonitorFilter(ABSFilter,ABC):
    
    #Parameter initializations 
    _n = 4
    _fc1 = 0.67
    _fc2 = 40
    _fs = 263
    _num, _den = signal.butter(_n, [_fc1, _fc2], btype='bandpass', fs=_fs)       
    
    def filter(self, channel_1):
        
        #Transitory state array
        self.tran_channel_1 = np.zeros(np.max([len(self._num), len(self._den)])-1)
        
        #Channel by channel filtering 
        self.channel_1_filt, self.tran_channel_1 = signal.lfilter(self._num, self._den, 
                                                    channel_1, zi=self.tran_channel_1)
        
        return self.channel_1_filt
    
class NotchMonitorFilter(ABSFilter,ABC):
    _q = 30
    _f0 = 20
    _fs = 263
    _num, _den = signal.iirnotch(_f0, _q, fs=_fs)
         
    def filtrar(self, channel_1):
        #Transitory state array    
        self.tran_channel1 = np.zeros(np.max([len(self._num), len(self._den)])-1)
        
        #Channel filtering    
        self.channel_1_filt, self.tran_channel_1 = signal.lfilter(self._num, self._den, 
                                                    channel_1, zi=self.tran_channel_1)
        
        return self.channel_1_filt