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