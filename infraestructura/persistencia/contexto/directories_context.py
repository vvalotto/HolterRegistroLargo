from infraestructura.persistencia.contexto.context import GenericContext
from dateutil import parser
# from datetime import datetime

import os
from math import ceil
import numpy as np

import tkinter as tk # TODO: Desacoplar interfaz de lógica. Generar acción desde la UI.
from tkinter import filedialog

class DirectoryContext(GenericContext):
    """ Especific context for create and manipulate directories

    Args:
        GenericContext (_type_): _description_
    """
    @property
    def resource(self):
        return self._resource

    def __init__(self, resource):
        super().__init__(resource)
        self._resource = self._adapt_resourse(resource)
        
        self._path = ''
        self._dir_creted = False
        self._path_days = []

        self._create()

    def _adapt_resourse(self, resource):
        name = resource[0]
        date = parser.parse (resource[1])
        amount_days = ceil((self.resource[2])/(24*60))
        return [name, date, amount_days]

    def _create(self):
        self._directory_create ()
        return
    
    def _directory_create(self):
        self._select_location()
        if self._path == '':
            self._path =  self._resource[0] +' '+ str(self._resource[1].date())
        else:
            self._path =  self._path + '/'+ self._resource[0] +' '+ str(self._resource[1].date())
        
        if self._directory_exist():
            print ('ERROR. El directorio ya existe.')
        else:
            os.mkdir(self._path)
            self._dir_creted = True
            self._sub_directories_create()
        return

    def _sub_directories_create(self):
        self._resource[1].month
        self._resource[1].day
        if self._dir_creted:
            for day in range(self._resource[1].day , 
                            (self._resource[1].day + self._resource[2])):
                self._path_days.append((self._path +'/'+ str(self._resource[1].month)
                                + '-' + str(day)))
                os.mkdir(self._path_days[(day-self._resource[1].day)])
        return

    def _directory_exist(self):
        print ('The folder path exist: ', os.path.isdir(self._path))
        return os.path.isdir(self._path)

    def _select_location(self):
        root = tk.Tk()
        root.attributes("-topmost", True)
        root.withdraw()
        self._path = filedialog.askdirectory()
        root.destroy()
        return

    def new_file(self, register_dto, date_init):
        
        file_date = date_init.strftime("%H-%M-%S")
        
        filename = file_date + '.csv'

        with open(filename, 'w') as csvfile:
            np.savetxt(csvfile, [register_dto.channel_1, register_dto.channel_2,
                                register_dto.channel_3], fmt='%s', delimiter=',', newline='\n')
        