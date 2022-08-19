from atexit import register
import numpy as np

class SignalMapper:

    def __init__(self, signal_DTO ) -> None:     
        self._signal = signal_DTO

    def monitor_channels(self, channels):
        if not self._signal.channel_1 == channels[0]: # condición de verificación -> mejorar
            self._signal.channel_1 = channels[0].copy()
            self._signal.channel_2 = channels[1].copy()
            self._signal.channel_3 = channels[2].copy()
    
    def register_channels(self, register_data, page_samples, page_bytes):
        """
        Éste método obtiene la información comprimida del archivo descargado. Genera
        una lista con la totalidad de la información de los 3 canales juntos.

        Args:
            register_data (list): Datos descargados (comprimidos). Cada elemento de la lista es el conjunto de
            payloads de una página.
            page_samples (dict): Cantidad de muestras por página.
            page_bytes (dict): Cantidad de bytes por página.

        Returns:
            list: Lista de datos de canales sin decodificar.
        """
        # voy a obtener los canales por archivo
        channels_not_decodified = []
        for page_number in range (len(register_data)):
            sample_number = -1 
            byte_number = 0
            channel_data = np.zeros ((page_samples[page_number]+1))

            while byte_number < page_bytes[page_number][byte_number]:
                shift = 0
                result = 0
                while True:
                    val= int (register_data[page_number][byte_number]) #IMPORTANTE. Ver en generacion de register_data. Es probable que el índice no coincida con el nro de página
                    result |= (val & 0x7f) << shift
                    shift += 7
                    byte_number = byte_number + 1
                    if not (val & 0x80):
                        sample_number = sample_number +1
                        break
                channel_data[sample_number] = result
                if (sample_number == page_samples[page_number]):
                    break
            
            channels_not_decodified.append(channel_data[:-1])
        
        return channels_not_decodified

    def decode_register_channels(self, register_data, channels_not_decodified):
        zigzag_dec_channels = []
        for page_number in range(len(register_data)):
            zigzag_dec = []
            for data_number in range(0, len(channels_not_decodified[page_number])):    
                data = ((int(channels_not_decodified[page_number][data_number]) >> 1) ^ -(int(channels_not_decodified[page_number][data_number]) & 1))
                if data < 0:
                    data = data & 0x0000000000FFFFFF
                    data = data*-1 -1
                zigzag_dec.append(data)   
            zigzag_dec_channels.append(zigzag_dec)
        
        #Decodificación delta
        ekg = []
        for page_number in range(len(register_data)):
            delta_dec = []
            for data_number in range(0, len(zigzag_dec_channels[page_number])):
                if(data_number==0):
                    delta_dec.append(zigzag_dec_channels[page_number][data_number])
                else:
                    delta_dec.append(zigzag_dec_channels[page_number][data_number]+delta_dec[data_number-1])  
            ekg.append(delta_dec)
        
        ch_1 = []
        ch_2 = []
        ch_3 = []

        for page_number in range (int (len(register_data)/3)):
            ch_1 = ch_1 +  ekg [page_number*3]
            ch_2 = ch_2 +  ekg [page_number*3+1]
            ch_3 = ch_3 +  ekg [page_number*3+2]

        self._signal.channel_1 = ch_1.copy()
        self._signal.channel_2 = ch_2.copy()
        self._signal.channel_3 = ch_3.copy()
    
    def save_data_csv(self, file_number):
        
        filename = f"file{file_number}.csv"

        with open(filename, 'w') as csvfile:
            np.savetxt(csvfile, [self._signal.channel_1, self._signal.channel_2,
                                self._signal.channel_3], fmt='%s', delimiter=',', newline='\n')


    def eventos():
        pass