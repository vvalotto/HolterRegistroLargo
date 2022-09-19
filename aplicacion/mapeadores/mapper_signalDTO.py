from atexit import register
import numpy as np

class SignalMapper:

    def __init__(self, signal_DTO ) -> None:     
        self._signal = signal_DTO

    def monitor_channels(self, channels):
        if not (self._signal.channel_1 == channels[0]   or self._signal.channel_2 == channels[1] 
                                                        or self._signal.channel_3 == channels[2]): # condición de verificación -> mejorar
            self._signal.channel_1 = channels[0].copy()
            self._signal.channel_2 = channels[1].copy()
            self._signal.channel_3 = channels[2].copy()

    def data_register_to_dto(self, register_data, channels_undecoder, channels):
        self._signal.channel_1 = channels[0].copy()
        self._signal.channel_2 = channels[1].copy()
        self._signal.channel_3 = channels[2].copy()
        self._signal.channels_undecoded = channels_undecoder.copy()
        self._signal.register_data = register_data.copy()

    def eventos():
        pass