class SignalMapper:

    def __init__(self, signal_DTO ) -> None:     
        self._signal = signal_DTO

    def monitor_channels(self, channels):
        if not self._signal.channel_1 == channels[0]: # condición de verificación -> mejorar
            self._signal.channel_1 = channels[0].copy()
            self._signal.channel_2 = channels[1].copy()
            self._signal.channel_3 = channels[2].copy()
    
    def eventos():
        pass
    def registro():
        pass