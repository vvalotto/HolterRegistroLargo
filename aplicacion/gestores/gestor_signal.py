import sys
sys.path.append('../../')
from aplicacion.mapeadores.mapper_signalDTO import SignalMapper

class SignalManager:

    """Este gestor se encarga de administrar la transferencia de los datos
     y actualizaciones de los DTOs.
    """
    def __init__(self, signal_ecg_dto, lock_monitor, event_monitor) -> None:
        self._signal_ecg_dto = signal_ecg_dto

        if signal_ecg_dto.type == 'monitor':
            self._mapper_signal = SignalMapper(signal_ecg_dto)
        self._lock = lock_monitor
        self._event = event_monitor

        if signal_ecg_dto.type == 'register':
            self._mapper_signal = SignalMapper(signal_ecg_dto)

    def set_dto_channels(self, channels):
        with self._lock:
            self._mapper_signal.monitor_channels(channels)
            self._event.set()

    def set_register_dto(self, register_data,channels_undecoded, channels):
        self._mapper_signal.data_register_to_dto(register_data,channels_undecoded, channels)
        

    # def save_register_channels(self, register_data, page_samples, page_bytes, file_number):
    #     # mapper_signal podria tener un método que asigne register_data al atributo register_data del DTO, así 
    #     # usarlo directamente desde el dto.
    #     channels_not_decodified = self._mapper_signal.register_channels(self, register_data, page_samples, page_bytes) # Ya hecho con channel splitter. 
    #     self._mapper_signal.decode_register_channels(self, register_data, channels_not_decodified)
    #     self._mapper_signal.save_data_csv(file_number)