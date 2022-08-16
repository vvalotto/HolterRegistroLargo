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
from datetime import date, datetime

CHUNK = 10
FS = 100
LENGTH = 5 * FS
ADCmax = 0xF30000
Vref = 2.4
NOTCH = False
FILTER = True
SAVE = False

class Senial:
    
    def __init__(self):
        self.t = np.linspace(0, LENGTH / FS, LENGTH)
        self.ch1 = np.zeros(LENGTH)
        self.ch2 = np.zeros(LENGTH)
        self.ch3 = np.zeros(LENGTH)

class Filtro:
    def __init__(self):
        self.n_filtro = 4
        self.fc_inferior = 0.67
        self.fc_superior = 40
        self.num, self.den = signal.butter(self.n_filtro, 
                                           [self.fc_inferior, self.fc_superior],
                                           btype='bandpass',
                                           fs=FS)
        self.tran_ch1 = np.zeros(np.max([len(self.num), len(self.den)])-1)
        self.tran_ch2 = np.zeros(np.max([len(self.num), len(self.den)])-1)
        self.tran_ch3 = np.zeros(np.max([len(self.num), len(self.den)])-1)
        
        
    def filtrar(self, senial_ch1, senial_ch2, senial_ch3):
        senial_filt_ch1, self.tran_ch1 = signal.lfilter(self.num, self.den, 
                                                    senial_ch1, zi=self.tran_ch1)
        senial_filt_ch2, self.tran_ch2 = signal.lfilter(self.num, self.den, 
                                                    senial_ch2, zi=self.tran_ch2)
        senial_filt_ch3, self.tran_ch3 = signal.lfilter(self.num, self.den, 
                                                    senial_ch3, zi=self.tran_ch3)
        
        return senial_filt_ch1, senial_filt_ch2, senial_filt_ch3
    
class Notch:
    def __init__(self):
        self.q_filtro = 30
        self.f0 = 20
        self.num, self.den = signal.iirnotch(self.f0, self.q_filtro, fs=FS)
        self.tran_ch1 = np.zeros(np.max([len(self.num), len(self.den)])-1)
        self.tran_ch2 = np.zeros(np.max([len(self.num), len(self.den)])-1)
        self.tran_ch3 = np.zeros(np.max([len(self.num), len(self.den)])-1)
        
        
    def filtrar(self, senial_ch1, senial_ch2, senial_ch3):
        senial_filt_ch1, self.tran_ch1 = signal.lfilter(self.num, self.den, 
                                                    senial_ch1, zi=self.tran_ch1)
        senial_filt_ch2, self.tran_ch2 = signal.lfilter(self.num, self.den, 
                                                    senial_ch2, zi=self.tran_ch2)
        senial_filt_ch3, self.tran_ch3 = signal.lfilter(self.num, self.den, 
                                                    senial_ch3, zi=self.tran_ch3)
        
        return senial_filt_ch1, senial_filt_ch2, senial_filt_ch3

class Adquisidor:
    
    def __init__(self, senial, puerto):
        self.senial = senial
        self.buffer_ch1 = np.zeros(CHUNK)
        self.buffer_ch2 = np.zeros(CHUNK)
        self.buffer_ch3 = np.zeros(CHUNK)
        self.buffer_ch1_v = np.zeros(CHUNK)
        self.buffer_ch2_v = np.zeros(CHUNK)
        self.buffer_ch3_v = np.zeros(CHUNK)
        self.filtro = Filtro()
        self.notch = Notch()
        self.__stop = False
        self.__ok = b'\xA5\x0A\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xAF'
        self.pkg_no_old = 512
        self.pkg_lost = 0
        self.ser = serial.Serial(puerto,
                        115200,
                        timeout=None,
                        bytesize=serial.EIGHTBITS,
                        parity=serial.PARITY_NONE,
                        stopbits=serial.STOPBITS_ONE,
                        rtscts=False)
        if SAVE:
            self.filename = datetime.now().strftime("%d-%m-%Y_%H.%M.%S") + '.csv'
        if not self.ser.is_open:
            self.ser.open()
            
    def start(self):
        # time.sleep(1)
        monitor_cmd = b'\xA5\x81\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x25'
        self.ser.write(monitor_cmd) 
        data = self.ser.read(13)
        if data == self.__ok:
            print("Mode: Monitor")
            
    def actualizar(self, chunk_ch1, chunk_ch2, chunk_ch3):
        if FILTER:
            chunk_ch1, chunk_ch2, chunk_ch3 = self.filtro.filtrar(chunk_ch1, 
                                                                  chunk_ch2, 
                                                                  chunk_ch3)
        if NOTCH:
            chunk_ch1, chunk_ch2, chunk_ch3 = self.notch.filtrar(chunk_ch1, 
                                                                 chunk_ch2, 
                                                                 chunk_ch3)
        self.senial.ch1 = np.roll(self.senial.ch1, -CHUNK)
        self.senial.ch2 = np.roll(self.senial.ch2, -CHUNK)
        self.senial.ch3 = np.roll(self.senial.ch3, -CHUNK)
        
        self.senial.ch1[LENGTH-CHUNK:LENGTH] = chunk_ch1
        self.senial.ch2[LENGTH-CHUNK:LENGTH] = chunk_ch2
        self.senial.ch3[LENGTH-CHUNK:LENGTH] = chunk_ch3
        
    def adquirir(self, index = 0):
        while(not self.__stop):
            if index < CHUNK:
                data = self.ser.read(13)
                
                if data[1] == 100:
                    self.check_integrity(data[11])
                
                    self.buffer_ch1[index] = (data[2]*65536+data[3]*256+data[4])
                    self.buffer_ch2[index] = (data[5]*65536+data[6]*256+data[7])
                    self.buffer_ch3[index] = (data[8]*65536+data[9]*256+data[10])
                    
                    self.buffer_ch1_v[index] = (self.buffer_ch1[index]/ADCmax-0.5)*2*Vref/3.5
                    self.buffer_ch2_v[index] = (self.buffer_ch2[index]/ADCmax-0.5)*2*Vref/3.5
                    self.buffer_ch3_v[index] = (self.buffer_ch3[index]/ADCmax-0.5)*2*Vref/3.5
                    index = index + 1
                
            else:
                actualizar_thread = threading.Thread(target=self.actualizar, 
                                                      args=[self.buffer_ch1_v, 
                                                            self.buffer_ch2_v, 
                                                            self.buffer_ch3_v])
                actualizar_thread.start()
                if SAVE:
                    guardar_thread = threading.Thread(target=self.guardar, 
                                                      args=[self.buffer_ch1, 
                                                            self.buffer_ch2, 
                                                            self.buffer_ch3])
                    guardar_thread.start()
                index = 0
        
        idle_cmd = b'\xA5\x81\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x24'
        self.ser.write(idle_cmd)
        data = self.ser.read(13)
        while not  data == self.__ok:
            data = self.ser.read(13)
        print("Mode: Idle")
        self.ser.close()
        
    def guardar(self, chunk_ch1, chunk_ch2, chunk_ch3):
        chunk = np.vstack([chunk_ch1, chunk_ch2, chunk_ch3])
        with open(self.filename, 'ab') as csvfile:
            np.savetxt(csvfile, np.transpose(chunk),
                       fmt='%d', delimiter=',', newline='\n')
    
    def check_integrity(self, pkg_no):
        if self.pkg_no_old == 512:
            self.pkg_no_old = pkg_no
        else:
            if pkg_no == 0:
                if self.pkg_no_old != 255:
                    # print("Paquete perdido")
                    # print(255 - self.pkg_no_old)
                    self.pkg_lost = self.pkg_lost + (255 - self.pkg_no_old)
            else:
                if (pkg_no - 1) != self.pkg_no_old:
                    # print("Paquete perdido")
                    if pkg_no > self.pkg_no_old:
                        self.pkg_lost = self.pkg_lost + ((pkg_no - 1) - self.pkg_no_old)                    
                        # print(pkg_no - 1 - self.pkg_no_old)
                    else:
                        self.pkg_lost = self.pkg_lost + ((pkg_no - 1) + (255 - self.pkg_no_old))                     
                        # print((pkg_no - 1) + (255 - self.pkg_no_old))
                    
            self.pkg_no_old = pkg_no
    
    def stop(self):
        self.__stop = True
 
def HolterMonitor(puerto):
    senial = Senial()
    adquisidor = Adquisidor(senial, puerto)
    # time.sleep(1)
    adquisidor.start()
    adq_thread = threading.Thread(target=adquisidor.adquirir)
    adq_thread.start()
    
    fig, ax = plt.subplots(3, 1, figsize=(10, 8))
    line1, = ax[0].plot(senial.t, senial.ch1)
    ax[0].set_ylim(-0.0004, 0.0006)
    ax[0].set_title("Canal 1")
    ax[0].set_xlabel("Tiempo [s]")
    ax[0].set_ylabel("Amplitud [V]")
    ax[0].grid()
    line2, = ax[1].plot(senial.t, senial.ch2, color="orange")
    ax[1].set_ylim(-0.001, 0.002)
    ax[1].set_title("Canal 2")
    ax[1].set_xlabel("Tiempo [s]")
    ax[1].set_ylabel("Amplitud [V]")
    ax[1].grid()
    line3, = ax[2].plot(senial.t, senial.ch3, color="green")
    ax[2].set_ylim(-0.0008, 0.0006)
    ax[2].set_title("Canal 3")
    ax[2].set_xlabel("Tiempo [s]")
    ax[2].set_ylabel("Amplitud [V]")
    ax[2].grid()
    
    def animate(i):
        line1.set_data(senial.t, senial.ch1)
        line2.set_data(senial.t, senial.ch2)
        line3.set_data(senial.t, senial.ch3)
        return line1, line2, line3
    
    ani = animation.FuncAnimation(fig, animate, interval=50, blit=True)
    plt.tight_layout()
    plt.show()
    plt.pause(0.001)
    
    adquisidor.stop()
    
if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(
    description="Graficador Holter Bago")

    parser.add_argument('-p', dest='puerto',
                        help="Nombre del puerto donde se encuentra conectado el dispositivo",
                        required=True)
    args = parser.parse_args()
    
    HolterMonitor(args.puerto)
    
    time.sleep(3)
    print("**************FIN DE SCRIPT**************")