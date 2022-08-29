"""
Se implementa el repositorio del Registro de la señal.
"""
from dominio.repositories.base_signal_repository import *
from infraestructura.persistencia.modelo.directories_register import * 
from infraestructura.persistencia.mapeadores.mapper import AbsMapper # no es necesario

import tkinter as tk
from tkinter import filedialog

import os


class SignalRegisterRepository (BaseSignalRepository):

    def __init__(self, context, mapper:AbsMapper):
        super().__init__(context)
        self._mapper = mapper
        self._path = ''
        self._dir_creted = False
        self._path_days = []
        
    def create(self):
        self._dir_create (self.context.resource)
        return
    
    def read(self, id):
        return super().read(id)
    
    def update(self, register):
        # Archivo por archivo
        dto = self._mapper.entity_to_dto(register)
        return super().update(register)
        #save_files
    
    def delete(self, id):
        return super().delete(id)

    def _dir_create(self, resource):
        self._select_location()
        if self._path == '':
            self._path =  resource[0] +' '+ str(resource[1].date())
        else:
            self._path =  self._path + '/'+ resource[0] +' '+ str(resource[1].date())
        
        if self._dir_exist():
            print ('ERROR. El directorio ya existe.')
        else:
            os.mkdir(self._path)
            self._dir_creted = True
            self._sub_dir_create()
        return   

    def _sub_dir_create(self, resource):
        if self._dir_creted:
            for day in range(1, resource[2]+1):
                self._path_days.append((self._path + '/dia '+ str(day)))
                os.mkdir(self._path_days[day-1])
        return
    
    def _dir_exist(self):
        print ('The folder path exist: ', os.path.isdir(self._path))
        return os.path.isdir(self._path)

    def _select_location(self):
        root = tk.Tk()
        root.attributes("-topmost", True)
        root.withdraw()
        self._path = filedialog.askdirectory()
        return

    