# This Python file uses the following encoding: utf-8
import os
from pathlib import Path
import sys

sys.path.append('../../')

# procesamiento de monitoreo 
from dominio.servicios.procesamiento import BandpassMonitorFilter, NotchMonitorFilter

from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import QObject, Slot, Signal, QPointF
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from PySide6.QtCharts import QAbstractSeries 

from aplicacion.gestores.gestor_vinculo import GestorVinculo
from aplicacion.gestores.gestor_operacion import GestorOperacion
from aplicacion.gestores.manager_logging_init import LoggingManager
from aplicacion.gestores.manager_download import DownloadManager

from infraestructura.interop.comando import Invocador
from infraestructura.interop import configurador_vinculo

from presentacion.monitoreo.download_configurator import DownloadConfigurator

from aplicacion.DTOs.monitor_DTO import MonitorDTO

""" Implementación Patrón observer y Threding para caso de Monitoreo """
from dominio.servicios.observer import *
from threading import Thread
from threading import Lock
from threading import Event

gestor_vinculo = None
monitor_ecg = None
manager_logging_init = None
manager_download = None
invocador = None
gestor_operacion = None

t_1 = []
t_2 = []

class Plotter(QObject):

    send = Signal(bool)
    _view_buffer_data = []
    _buffer_data = []

    def __init__(self):
        super().__init__()

        self._channel_1 = [] # Channel 1 = channel general
        #generar buffer
        self._ADCmax = 0xF30000
        self._Vref = 2.4
        self._new_data = []
        self.__generate_buffer_data()

        # Filtros
        self._band_pass_m=BandpassMonitorFilter(0.67,40,263,4)
        self._notch_m=NotchMonitorFilter(30,20,263)


    def filter(self):
        #filtrar datos en self._channel_1
        pass

    def data_update(self):
        self._new_data = []
        #def filter
        data_to_filter = []

        for i in range (0, len(self._channel_1)):
            dato_int = self._channel_1[i][0]*65536+self._channel_1[i][1]*256+self._channel_1[i][2]
            dato = ((dato_int/self._ADCmax-0.5)*2*self._Vref/3.5)*1000
            data_to_filter.append(dato)
            # self._new_data.append(QPointF(i,dato))
        
        bandpass_filtered=self._band_pass_m.filter(data_to_filter)
        notch_filtered=self._notch_m.filter(bandpass_filtered)

        for i in range(0,len(notch_filtered)):    
            self._new_data.append(QPointF(i,notch_filtered[i]))


    def __generate_buffer_data(self, time_view = 1600):
        self._buffer_data = [QPointF(i,0) for i in range(0,time_view)]

    def refresh_buffer(self):
        self._buffer_data = self._buffer_data[len(self._new_data):]
        self._buffer_data.extend(self._new_data)

        for point in range(len(self._buffer_data)):
            self._buffer_data[point].setX(point)

    def update_buffer_data(self):

        self._view_buffer_data = self._buffer_data
        self.send.emit(True)

    @Slot(QAbstractSeries)
    def get_series(self, series):
        series.replace(self._view_buffer_data)

    def change_time_axis(self):
        pass


class DeviceConnectorMode(QObject):
    global gestor_vinculo
    global gestor_operacion
    global monitor_ecg
    global manager_logging_init
    # global manager_download
    holter_connected = Signal(bool)
    total_files = Signal (int)
    downloaded_files = Signal(int)

    def __init__(self, event) -> None:
        super().__init__()
        self._signal_to_connect = event
        self._flag = False

    @Slot(bool, int)
    def holter_connect(self, flag, conection_type):
        print (conection_type)
        self._flag = flag
        if flag:
            aplication_init(conection_type)
            gestor_vinculo.parar_holter()
            self.holter_connected.emit(True)
        else:     
            gestor_vinculo.desenlazar_holter()
            self.holter_connected.emit(False)           

    @property
    def flag(self):
        return self._flag

    @Slot(bool)
    def monitor_mode(self, on_off):
        monitor_ecg.state = on_off
        if on_off:
            iniciar_monitoreo()   
        else:
            gestor_vinculo.parar_holter()
            global t_1
            global t_2
            t_2.join()
            t_1.join()

    @Slot()
    def loggin_init(self):
        global manager_logging_init
        gestor_vinculo.set_download_mode()
        print ("MODO DESCARGA")
        gestor_operacion.erase_holter_memory()
        print ("FIN BORRADO DE MEMORIA")
        manager_logging_init.logging_start()
        print ("INICIO DE ESTUDIO")
    
    @Slot()
    def download_init(self):
        t_3 = Thread(target=download_thread, args=(self.total_files, self.downloaded_files),daemon=True)
        t_3.start()
        

def download_thread(total_files, downloaded_files):
    global invocador

    aplication_init('USB_CONNECTION')
    gestor_vinculo.set_download_mode()

    download_subject = DownloadSubject()
    download_observer = DownloadInterfaceObserver(total_files, downloaded_files)
    download_subject.attach(download_observer)
    
    DownloadConfigurator(invocador, download_subject)

def aplication_init(conection_type):
    global gestor_vinculo
    global monitor_ecg
    global manager_logging_init
    global manager_download
    global invocador
    global gestor_operacion


    """ Invocador """
    if conection_type == 0:
        link_usb = 'DONGLE_CONNECTION'
    else:
        link_usb = 'USB_CONNECTION'
    monitor_ecg.link_type = link_usb

    invocador_init = configurador_vinculo.InvocatorInit(link_usb)

    invocador = invocador_init.invocador

    """ Manager Logging Init """

    manager_logging_init = LoggingManager(invocador)

    """ Gestor de vínculo """

    gestor_vinculo = GestorVinculo(invocador)

    """ Gestor de operación """

    gestor_operacion = GestorOperacion(invocador)

    """ Manager Download """

def monitorear(monitor_ecg, lock_monitor,event_monitor):
    global gestor_operacion

    gestor_vinculo.poner_modo_monitoreo()
    gestor_operacion.monitorear_holter(monitor_ecg, lock_monitor,event_monitor)

def print_monitor(monitor_subjet, lock_monitor, event_monitor):
    global monitor_ecg

    while (monitor_ecg.state):
        event_monitor.wait()
        with lock_monitor:
            if  not monitor_ecg.state: # puede ser que esté de más.
                break
            monitor_subjet.some_business_logic() # directamente puede ser notify
            event_monitor.clear()

def iniciar_monitoreo():
    global monitor_subject
    global t_1
    global t_2
    """ Threading: evento y bloqueo """
    event_monitor = Event()
    lock_monitor = Lock()   
    t_1 = Thread(target=monitorear, args=(monitor_ecg, lock_monitor,
                                                        event_monitor), daemon=True)
    t_2 = Thread(target=print_monitor, args=(monitor_subject,lock_monitor,
                                                        event_monitor),daemon=True)
    t_1.start()
    t_2.start()

""" Objeto graficador"""
event_con= Event()
ploter_1 = Plotter()
ploter_2 = Plotter()
ploter_3 = Plotter()
connector = DeviceConnectorMode(event_con)

""" Entidad ECG Monitoreo """ #--> debería ser el DTO
monitor_ecg = MonitorDTO()

""" Subjet and Observer """

monitor_subject = MonitoreoSubject()
observer_a = ObserverMonitorDTO(monitor_ecg, ploter_1, ploter_2, ploter_3)

monitor_subject.attach(observer_a)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('../monitor/resources/images/icono.PNG'))
    engine = QQmlApplicationEngine()

    engine.load(os.fspath(Path(__file__).resolve().parent / "../monitor/main.qml"))
    
    engine.rootObjects()[0].setProperty('plotter', ploter_1)
    engine.rootObjects()[0].setProperty('plotter2', ploter_2)
    engine.rootObjects()[0].setProperty('plotter3', ploter_3)
    engine.rootObjects()[0].setProperty('connector', connector)

    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec())