# -*- coding: utf-8 -*-
"""

Monitor Holter

"""
import numpy as np
from scipy import signal
from abc import abstractmethod, ABC

class ABSFilter(ABC):

    @abstractmethod
    def filter():
        pass

class BandpassMonitorFilter(ABSFilter):
    
    #Initialization
    def __init__(self,fc1,fc2,fs,n): 
        self.fc1 = fc1#0.67
        self.fc2 = fc2#40
        self.fs = fs#263
        self.n = n#4
        self.num, self.den = signal.butter(self.n, [self.fc1, self.fc2], btype='bandpass', fs=self.fs)       
        #Transitory state array
        self.tran_channel_1 = np.zeros(np.max([len(self.num), len(self.den)])-1)
        
    def filter(self, channel_1):
        
        #Channel by channel filtering 
        self.channel_1_filt, self.tran_channel_1 = signal.lfilter(self.num, self.den, 
                                                    channel_1, zi=self.tran_channel_1)
        
        return self.channel_1_filt
    
class NotchMonitorFilter(ABSFilter):
    
    def __init__(self,q,f0,fs): 
        self.q = q#30
        self.f0 = f0#20
        self.fs = fs#263
        self.num, self.den = signal.iirnotch(self.f0, self.q, fs=self.fs)       
        #Transitory state array    
        self.tran_channel1 = np.zeros(np.max([len(self.num), len(self.den)])-1)
         
    def filtrar(self, channel_1):

        #Channel filtering    
        self.channel_1_filt, self.tran_channel_1 = signal.lfilter(self.num, self.den, 
                                                    channel_1, zi=self.tran_channel_1)
        
        return self.channel_1_filt