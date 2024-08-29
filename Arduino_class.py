import serial
import time
from datetime import datetime
import csv
import numpy as np

class Control():
    def __init__(self, cooling_function, working_hours, serial_port, badios):
        # Configurar el puerto serial (ajusta el puerto según sea necesario)
        ser = serial.Serial(serial_port, badios)
        
        # Configurar el tiempo de inicio
        start_time = datetime.now()
        working_time = 0

        fields = ['time','temperature','setpoint','power']
        filename = 'CsvData_saved/temperature_data_'+ start_time.strftime("%Y-%m-%d_%H-%M-%S") +'.csv'


        with open(filename, 'w') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(fields)

            print('Se ha generado csv y los datos se guardaran en: ./csvData_saved/'+filename)
            print('Iniciando control')

            while working_time <= working_hours:
                # Calcular las horas transcurridas desde el inicio
                elapsed_time = datetime.now() - start_time
                hours = elapsed_time.total_seconds()/3600
                working_time = hours

                # Calcular el setpoint
                setpoint = cooling_function(hours)

                # Enviar el setpoint al Arduino
                ser.write(f"{setpoint}\n".encode())

                time.sleep(0.5)

                temperature = ser.readline().decode().strip()
                dim = ser.readline().decode().strip()
                #out = ser.readline().decode().strip()

                power = round(100*(84-int(dim))/84,1) #potencia(float(dim))
                writer.writerow([datetime.now(),temperature,setpoint,power])
                time_passed = str(elapsed_time).split('.')[0]
                print(f"Temp: {temperature}°C, Setpoint: {setpoint}°C, potencia: {power}%, Tiempo(H:MM:SS): {time_passed}")
                #print(out)
            setpoint = 0
            ser.write(f"{setpoint}\n".encode())
            print('Control finalizado con exito')
            ser.close()
        return

def potencia(dim):
    P = 422.45*np.arctan((84-dim)*0.0637275) + 455.68
    return round(P,1)
