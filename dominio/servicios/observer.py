from __future__ import annotations
from abc import ABC, abstractmethod
from random import randrange
from typing import List


class AbsSubject(ABC):

    """ Tema """

    @abstractmethod
    def attach(self, observer : AbsObserver)-> None:
        """ Incorporar Observador """
        pass

    @abstractmethod
    def detach(self,observer : AbsObserver)-> None:
        """ Eliminar Observador """
        pass

    @abstractmethod
    def notify(self) -> None:
        """ Notificador de cambio """
        pass


class AbsObserver(ABC):
    """ Observador """

    @abstractmethod
    def update(self, subjet : AbsSubject)-> None:
        pass


class MonitoreoSubject(AbsSubject):

    # _state: int = None 
    _state: None
    _observers: List[AbsObserver] = []

    def attach(self, observer : AbsObserver):
        # print("Subject: Attached an observer.")
        self._observers.append(observer)      
    
    def detach(self, observer : AbsObserver):
        self._observers.remove(observer)

    def notify(self):
        # print("Subject: Notifying observers...")
        for observer in self._observers:
            observer.update(self)

    def some_business_logic(self) -> None:
        """
        Usually, the subscription logic is only a fraction of what a Subject can
        really do. Subjects commonly hold some important business logic, that
        triggers a notification method whenever something important is about to
        happen (or after it).
        """

        # print("\nSubject: I'm doing something important.")
        # self._state = randrange(0, 10)

        # print(f"Subject: My state has just changed to: {self._state}")
        self._state = True
        self.notify()


class ObserverMonitorDTO(AbsObserver):
    def __init__(self,objet_monitor, ploter, ploter_2, ploter_3) -> None:
        self._ecg_monitor = objet_monitor
        self.ploter = ploter
        self.ploter_2 = ploter_2
        self.ploter_3 = ploter_3
        self.ploter._channel_1 = self._ecg_monitor.channel_1
        self.ploter_2._channel_1 = self._ecg_monitor.channel_2
        self.ploter_3._channel_1 = self._ecg_monitor.channel_3

    def update(self, subject: MonitoreoSubject) -> None:
        # print("ConcreteObserverA: Reacted to the event")
        # print ('Vincular con el presentador')
        # print ('OBSERVADOR')

        self.ploter._channel_1 = self._ecg_monitor._channel_1
        self.ploter.data_update()
        self.ploter.refresh_buffer()
        self.ploter.update_buffer_data()

        self.ploter_2._channel_1 = self._ecg_monitor._channel_2
        self.ploter_2.data_update()
        self.ploter_2.refresh_buffer()
        self.ploter_2.update_buffer_data()

        self.ploter_3._channel_1 = self._ecg_monitor._channel_3
        self.ploter_3.data_update()
        self.ploter_3.refresh_buffer()
        self.ploter_3.update_buffer_data()


class DownloadSubject(AbsSubject):

    _state: None
    _observers: List[AbsObserver] = []

    def attach(self, observer : AbsObserver):
        # print("Download Subject: Attached an observer.")
        self._observers.append(observer)      
    
    def detach(self, observer : AbsObserver):
        self._observers.remove(observer)

    def notify(self):
        # print("Download Subject: Notifying observers...")
        if self._observers[0].flag:
            self._observers[0].update(self)
            self._observers[1].downloaded_files = self._observers[0].downloaded_files
            self._observers[1].amount_files = self._observers[0].amount_files
            self._observers[1].update(self)
        else:
            self._observers[1].update(self)
            self._observers[0].downloaded_files = self._observers[1].downloaded_files
            self._observers[0].amount_files = self._observers[1].amount_files
            self._observers[0].update(self)

        
        # for observer in self._observers:
        #     observer.update(self)


class DownloadObserver(AbsObserver):
    def __init__(self, download_observer) -> None:
        self.flag = True
        self.download_observer = download_observer
        self.amount_files = 0
        self.downloaded_files = 0

    def update(self, subject: DownloadSubject) -> None:
        # print("Download Observer: Reacted to the event")
        self.amount_files = self.download_observer.amount_files
        self.downloaded_files = self.download_observer.file_number


class DownloadInterfaceObserver(AbsObserver):
    def __init__(self,total_files, downloaded_files ) -> None:
        self.flag = False
        self.total_files_signal = total_files
        self.downloaded_files_signal = downloaded_files
        self.amount_files = 0
        self.downloaded_files = 0

    def update(self, subject: DownloadSubject) -> None:
        # print("Download int Observer: Reacted to the event")
        self.total_files_signal.emit(self.amount_files)
        # print ('emit total:', self.amount_files )
        self.downloaded_files_signal.emit(self.downloaded_files+1)
        # print ('emit archivo:', self.downloaded_files )
