import json

class StudyMapper:

    def set_time_init(self, study,current_time):
        study.time_init = current_time
        print (current_time, 'STUDY MAPPER')

    def update_study_config(self, study):
        # with open('./study_configuration_data.json') as file:
        with open('D:\Repositorios\GitHub\HolterRegistroLargo\presentacion\monitoreo\study_configuration_data.json') as file:
            configuration = json.load(file)
            study.time_init = configuration['time_init']
            print ('UPDATE', study.time_init)
            study.time_stop = configuration['time_stop']
            study.channels = configuration['channels']
            study.events_type_byte_1 = configuration['events_type_byte_1']
            study.events_type_byte_2 = configuration['events_type_byte_2']
            study.interface = configuration['interface']

    def get_study_config(self, study):
        # study.time_init debe ser un datetime igual al current time
        information = [ study.time_init, study.time_stop, study.channels,
                        study.events_type_byte_1, study.events_type_byte_2,
                        study.interface]
        return information

    def defect_study_config(self, current_time):
        fileName = "./study_configuration_data.json"
        jsonObject = {
            "time_init": str(current_time),#current_time.strftime('%S/%M/%H'), # datetime to string
            "time_stop": 7200,
            "channels": 3,
            "events_type_byte_1": 0,
            "events_type_byte_2": 0,
            "interface": 0,
            }
        file = open(fileName, "w")
        json.dump(jsonObject, file)
        file.close()    
