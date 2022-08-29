import os
import sys

import tkinter as tk
from tkinter import filedialog

import math

sys.path.append('../../')

from aplicacion.gestores.manager_study import StudyManager
from dominio.entidades.study import StudyEKG

from dateutil import parser

class DirectoriesManager:

    def __init__(self, folder_path = ''):
        
        self._folder_path = folder_path
        self._folder_path_days = []

        self._study = StudyEKG()
        self.study_manager = StudyManager(self._study)
        self._information_study = None

        self._dir_creted = False

    def _get_study_data(self):
        
        self._information_study = self.study_manager.get_study_configuration(self._study)
        return self._information_study
       
    def create_dir(self, name_study = 'Estudio Holter'):
        self._get_study_data()
        study_init = self._information_study[0]
        date = parser.parse(study_init)

        self.select_location()
        
        if self._folder_path == '':
            self._folder_path =  name_study +' '+ str(date.date())
        else:
            self._folder_path =  self._folder_path + '/'+ name_study +' '+ str(date.date())
        
        if self._dir_exist():
            print ('ERROR. El directorio ya existe.')
        else:
            os.mkdir(self._folder_path)
            self._dir_creted = True
            self._sub_dir_create()
        
    def _dir_exist(self):
        print ('The folder path exist: ', os.path.isdir(self._folder_path))
        return os.path.isdir(self._folder_path)
    
    def _sub_dir_create(self):
        if self._dir_creted:
            amount_days = math.ceil((self._information_study[1])/(24*60))
            for day in range(1, amount_days+1):
                self._folder_path_days.append((self._folder_path + '/dia '+ str(day)))
                os.mkdir(self._folder_path_days[day-1])

    def select_location(self):
        root = tk.Tk()
        root.attributes("-topmost", True)
        root.withdraw()
        self._folder_path = filedialog.askdirectory()
        
# El .json se encuentra en gestores sólo para las pruebas.. ya que se está 
# probando desde este directorio.

a = DirectoriesManager()
object =os.getcwd()
a.create_dir()

 



