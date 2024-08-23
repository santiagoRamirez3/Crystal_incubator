from Arduino_class import *

def temperature_function(hours):
    # Ejemplo: decrecimiento del setpoint cada 2 horas
    base_temperature = 44.  # Temperatura base en grados Celsius
    increment = -1  # decrecimiento de temperatura cada hora
    return base_temperature + (increment * (hours // 1))

control_system = Control(cooling_function = temperature_function,
                         working_hours = 6,
                         serial_port = '/dev/ttyUSB0',
                         badios = 9600)