import numpy as np

def channel_splitter (register_data, page_samples, page_bytes):
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
    channels_undecoded = []
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
            
        channels_undecoded.append(channel_data[:-1])
        
    return channels_undecoded