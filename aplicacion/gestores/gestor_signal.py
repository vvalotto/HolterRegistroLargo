import sys
sys.path.append('../../')
from aplicacion.mapeadores.mapper_signalDTO import SignalMapper

class SignalManager:

    """Este gestor se encarga de administrar la transferencia de los datos
     y actualizaciones de los DTOs.
    """
    def __init__(self, signal_ecg, lock_monitor, event_monitor) -> None:

        if signal_ecg.type == 'monitor':
            self._mapper_signal = SignalMapper(signal_ecg)
        self._lock = lock_monitor
        self._event = event_monitor

        if signal_ecg.type == 'register':
            self._mapper_signal = SignalMapper(signal_ecg)

    def set_dto_channels(self, channels, repository):
        with self._lock:
            self._mapper_signal.monitor_channels(channels)
            self._event.set()
    
    def save_register_channels(self, register_data, page_samples, page_bytes, file_number):
        # mapper_signal podria tener un método que asigne register_data al atributo register_data del DTO, así 
        # usarlo directamente desde el dto.
        channels_not_decodified = self._mapper_signal.register_channels(self, register_data, page_samples, page_bytes)
        self._mapper_signal.decode_register_channels(self, register_data, channels_not_decodified)
        self._mapper_signal.save_data_csv(file_number)