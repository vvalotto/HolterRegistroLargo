from abc import abstractmethod, ABCMeta, ABC
from distutils.util import change_root
from importlib.resources import Package

import serial
from serial.tools.list_ports import comports

from blatann import BleDevice
from blatann.nrf import nrf_events
from blatann.services import nordic_uart
from blatann.gatt import MTU_SIZE_FOR_MAX_DLE

import re
import subprocess

class AbsEnlace(metaclass=ABCMeta):
    DEVICE_NAME = 'Holter_Bago'
    DEVICE_ADRESS = "F1:05:2B:EC:08:76,s"
    PACKAGE_LENGTH = 13

    def __init__(self):
        self._puerto = None
        self._datos = None

    @abstractmethod
    def conectar(self):
        pass

    @abstractmethod
    def desconectar(self):
        pass

    @abstractmethod
    def enviar(self, datos):
        pass

    @abstractmethod
    def recibir(self, amount_packages = 1):
        pass

    def _restart_parameters(self):
        self._puerto = None
        self._datos = None
        self._uart_service = None
        self._peer = None
        self._ble_device = None

    def _listar_puertos_series(self):
        puertos = list(comports())
        for puerto in puertos:
            # print (puerto.description[:], "description")
            print (puerto.name, "name")
        return puertos

    def _nombre_puerto(puertos):
        try:
            for i in puertos:
                try: 
                    print(i.name)
                    puerto = serial.Serial(i.name, 115200, timeout = 2)
                    if puerto.read(12) == b'\xa5\x0a\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00':
                        name = i.name
                        puerto.close()
                        return name
                    else:
                        print (i[0], ': Puerto incorrecto')
                    puerto.close()
                except: 
                    pass
        except: 
            print ('Puerto no encontrado - Dispositivo no enlazado')


class EnlaceUSB(AbsEnlace, ABC):

    def conectar(self):
        try:
            if self._puerto.isOpen():
                self._puerto.close()
        except:
            pass

        try:
            ports = self._listar_puertos_series()
            print (ports[0].name, type(ports[0].name))
            self._puerto = serial.Serial(ports[0].name,115200, timeout = 2) #COM 3 PLACA DESARROLLO
            # print (self._puerto)
            print ('Puerto enlazado')
        except:
            print ('Error para enlazar puerto. Puerto no enlazado')
            pass

        # self.listar_puertos_series()

    def desconectar(self):
        try:
            self._puerto.reset_input_buffer()
            self._puerto.close()
            print('Puerto desenlazado')
        except:
            print ('El puerto indicado no se encontraba enlazado')
            pass

    def enviar(self, datos):
        try:
            if self._puerto.isOpen():
                print('puerto abierto')
                self._puerto.write(datos)
                print('se enviaron los datos')
            else:
                print ('No se enviaron los datos. Puerto no enlazado')
        except:
            print ("No se enviaron los datos")
            pass

    def recibir(self, amount_packages):
        amount_bytes = self.PACKAGE_LENGTH * amount_packages
        try:
            if self._puerto.isOpen():
                recibido = self._puerto.read(amount_bytes)
                return recibido
            else:
                print ('No se recibieron datos. Puerto no enlazado')
        except:
            print ('Error de comunicación (self._puerto.read). No se recibieron los datos')
            pass


class EnlaceDongle(AbsEnlace, ABC):
    
    _uart_service = None
    _peer = None
    _ble_device = None
    _change_data = False

    def conectar(self):
        # Open the BLE Device and suppress spammy log messages
        ports = self._listar_puertos_series()
        print (ports[0].name, type(ports[0].name))
        self._ble_device = BleDevice(ports[0].name) #5
        self._ble_device.event_logger.suppress(nrf_events.GapEvtAdvReport)
        # Configure the BLE device to support MTU sizes which allow the max data length extension PDU size
        # Note this isn't 100% necessary as the default configuration sets the max to this value also

        self._ble_device.configure(att_mtu_max_size=MTU_SIZE_FOR_MAX_DLE)
        self._ble_device.open(clear_bonding_data=True)

        # Set scan duration for 4 seconds
        self._ble_device.scanner.set_default_scan_params(timeout_seconds=1)
        self._ble_device.set_default_peripheral_connection_params(7.5, 15, 4000)    
        target_address = None
        # Start scan and wait for it to complete
        scan_report = self._ble_device.scanner.start_scan().wait()
        # Search each peer's advertising data for the Nordic UART Service UUID to be advertised
        for report in scan_report.advertising_peers_found:
            if report.device_name == self.DEVICE_NAME: # and report.peer_address == self.DEVICE_ADRESS:
                target_address = report.peer_address
                break
        if not target_address:
            print("No se encuentra el dispositivo Holter Bago")
            self._ble_device.close()
            return
        # Initiate connection and wait for it to finish
        print("Holter Bago encontrado: conectando a {}".format(target_address))
        self._peer = self._ble_device.connect(target_address).wait()
        if not self._peer:
            print("Conexión caducada")
            self.desconectar()
            return

        # Exchange MTU
        self._peer.exchange_mtu(self._peer.max_mtu_size).wait(10)
         # Initiate service discovery and wait for it to complete
        _, event_args = self._peer.discover_services().wait(exception_on_timeout=False)

        self._uart_service = nordic_uart.find_nordic_uart_service(self._peer.database)
        if not self._uart_service:
            print("No se encuentra Nordic UART service")
            self.desconectar()
            return
        # # # Initialize the service
        self._uart_service.initialize().wait(5)
        self._uart_service.on_data_received.register(self.on_data_rx)

    def enviar(self, datos):
        try:
            self._uart_service.write(datos).wait(5)
            print('se enviaron los datos')
        except:
            print ("Error en 'enviar'. No se enviaron los datos")
            pass
    
    def desconectar(self):
        try:
            # self._peer.disconnect().wait()
            self._uart_service.on_data_received.clear_handlers()
            self._uart_service.on_data_received.deregister(self.on_data_rx)
            self._ble_device.close()
            print ('ble_device se desconectó')
            self._restart_parameters()
            # self._peer.disconnect().wait()
            print('Puerto desenlazado')
        except:
            print ('Error de desconexión. El puerto indicado no se encontraba enlazado')
            pass

    def recibir(self, amount_packages):

        try:
            
            if not float.is_integer(len(self._datos)/self.PACKAGE_LENGTH):
                print ('Se perdieron datos. Se reiniciará la conexión')
                self.desconectar()
                return [False]
            cicle_limit = 0
            while (not self._change_data)and(cicle_limit<1000):
                pass
            self._change_data = False
        except:
            pass
        return self._datos
    
    def on_data_rx(self, service, data):
        self._datos = data
        self._change_data = True
        
