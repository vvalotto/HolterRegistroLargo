from __future__ import annotations
from abc import ABC, abstractmethod
from random import randrange
from typing import List



class AbsSubjet(ABC):

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
    def update(self, subjet : AbsSubjet)-> None:
        pass


class MonitoreoSubjet(AbsSubjet):

    _state: int = None 

    _observers: List[AbsObserver] = []

    def attach(self, observer : AbsObserver):
        print("Subject: Attached an observer.")
        self._observers.append(observer)      
    
    def detach(self, observer : AbsObserver):
        self._observers.remove(observer)

    def notify(self):
        print("Subject: Notifying observers...")
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
        self._state = 1
        self.notify()


class ObserverMonitorDTO(AbsObserver):
    def __init__(self,objet_monitor, ploter, ploter_2, ploter_3) -> None:
        self._ecg_monitor = objet_monitor
        self.ploter = ploter
        self.ploter_2 = ploter_2
        self.ploter_3 = ploter_3
        self.ploter._channel_1 = self._ecg_monitor._channel_1
        self.ploter_2._channel_1 = self._ecg_monitor._channel_2
        self.ploter_3._channel_1 = self._ecg_monitor._channel_3

    def update(self, subject: MonitoreoSubjet) -> None:
        print("ConcreteObserverA: Reacted to the event")
        print ('Vincular con el presentador')
        print ('OBSERVADOR')

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


# if __name__ == "__main__":
#     # The client code.

#     subject = MonitoreoSubjet()

#     observer_a = ObserverMonitorDOT()
#     subject.attach(observer_a)

#     subject.some_business_logic()
#     subject.some_business_logic()

#     subject.some_business_logic()


#     subject.detach(observer_a)

#     subject.some_business_logic()