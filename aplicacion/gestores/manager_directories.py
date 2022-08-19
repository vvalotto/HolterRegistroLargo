import os
import sys

import tkinter as tk
from tkinter import filedialog

sys.path.append('../../')

from aplicacion.gestores.manager_study import StudyManager
from dominio.entidades.study import StudyEKG

from dateutil import parser

class DirectoriesManager:

    def __init__(self, folder_path = ''):
        
        self._folder_path = folder_path

        self._study = StudyEKG()
        self.study_manager = StudyManager(self._study)
        self._information_study = None

    def get_study_data(self):
        
        self._information_study = self.study_manager.get_study_configuration(self._study)
       
    def create_dir(self, name_study = 'Estudio Holter'):
        self.get_study_data()
        study_init = self._information_study[0]
        date = parser.parse(study_init)
        # a = datetime.strptime(study_init,'%Y-%m-%d %H:%M:%S' )
        # name = '{}_{}_{}_{}_{}_{}'.format(name_study, date.hour,date.minute, date.day, date.month, date.year)
        
        self.select_location()
        
        if self._folder_path == '':
            self._folder_path =  name_study +' '+ str(date.date())
        else:
            self._folder_path =  self._folder_path + '/'+ name_study +' '+ str(date.date())
        
        if self._dir_exist():
            print ('ERROR. El directorio ya existe.')
        else:
            os.mkdir(self._folder_path)
        
    def _dir_exist(self):
        print ('The folder path exist: ',os.path.isdir(self._folder_path))
        return os.path.isdir(self._folder_path)
    
    def select_location(self):
        root = tk.Tk()
        root.attributes("-topmost", True)
        root.withdraw()
        self._folder_path = filedialog.askdirectory()
        

a = DirectoriesManager()
object =os.getcwd()
a.create_dir()

 



