from Arduino_class import *

def temperature_function(hours):
    # Ejemplo: decrecimiento del setpoint cada 2 horas
    base_temperature = 55.  # Temperatura base en grados Celsius
    increment = -0.25  # decrecimiento de temperatura cada hora
    return round(base_temperature + (increment * (hours // 1)),2)

control_system = Control(cooling_function = temperature_function,
                         working_hours = 120,
                         serial_port = '/dev/ttyUSB0',
                         badios = 9600)