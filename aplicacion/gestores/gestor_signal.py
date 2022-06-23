import sys
sys.path.append('../../')
from aplicacion.mapeadores.mapper_signalDTO import SignalMapper

class SignalManager:

    """Este gestor se encarga de administrar la transferencia de los datos
     y actualizaciones de los DTOs.
    """
    def __init__(self, monitor_ecg, lock_monitor, event_monitor) -> None:

        if monitor_ecg.type == 'monitor':
            self._map_out = SignalMapper(monitor_ecg)
        self._lock = lock_monitor
        self._event = event_monitor

    def set_dto_channels(self, channels):
        with self._lock:
            self._map_out.monitor_channels(channels)
            self._event.set()