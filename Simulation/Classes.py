from scipy.optimize import curve_fit
from random import gauss
import matplotlib.pyplot as plt
import numpy as np

#-------------------------------------------------------------------------------------

class Tank_characterizer():
    def __init__(self, data_time, data_temperature, liters,
                 ambient_temperature, mode):
        '''
        Using a model of heating or coling, estimate the coling
        constant (k) for the tank.

        Parameters:
        data_time: list of strings of minutes and seconds for each value of temperature, with format 'MM:SS'.

        data_temperature: list of floats with the value of temperature for each value of time.

        liters: capacity of the water tank in liters (L).

        mode: ('HEATING','COOLING') 
        '''
        self.seconds = convert_to_seconds(data_time)
        self.temperatures = data_temperature
        initial_temperature = data_temperature[0]
        #++++++++++++++++++++++++++++++++++++++++++++

        if mode == 'HEATING':
            power = 1000.
        elif mode == 'COOLING':
            power = 0.
        else:
            print('Incorrect mode')

        #++++++++++++++++++++++++++++++++++++++++++++

        stimation_func = lambda t,k: heating(t,k, P=power, Ti=initial_temperature,
                                             Ta=ambient_temperature, L=liters)
        
        self.k = curve_fit(stimation_func,self.seconds/60,self.temperatures)[0][0]/60
        return
#-------------------------------------------------------------------------------------  
    def simulation(self, setpoint_function, file_name:str , kp:int, ki:int, kd:int,
                   water_initial_temperature:float, external_temperature:float, final_time, presition:float):
        
        hours = np.arange(0,final_time,1/360)
        
        n = len(hours)

        sets = np.zeros(n)
        errores = np.zeros(n)
        temperaturas = np.zeros(n+1)
        temperaturas[0] = water_initial_temperature

        for step in range(n):
            time = hours[step]
            set = setpoint_function(time)
            sets[step] = set
            error = set - (temperaturas[step] + gauss(0,presition))
            errores[step] = error
            dim = PID(error,time, errores, kp, ki, kd)
            P = potencia(dim)
            New_T = instant_temperature(self.k,P, temperaturas[step], external_temperature, temperaturas[step])
            temperaturas[step +1] = New_T

        
        fig, ax = plt.subplots(1,1)
        ax.plot(hours,temperaturas[0:-1], label='Lectura termómetro')
        ax.plot(hours,sets, label='Setpoint')
        ax.set_ylabel('Temperatura (°C)')
        ax.set_xlabel(f'''Tiempo (h)
                   

    kp={kp}  ki={ki} kd={kd}''')
        ax.set_title(f'Simulación con varianza de termómetro de {presition}°C')
        ax.legend()
        plt.tight_layout()
        plt.savefig('Simulation_plots/'+file_name+'.png', dpi=72)
        return

#-------------------------------------------------------------------------------------

def convert_to_seconds(time_list):
    """
    Convert a list of strings with format 'MM:SS' to numerical value of total seconds.
    
    :param time_list: List of time strings with format 'MM:SS'
    :return: List of integers of total seconds
    """
    seconds_list = []
    
    for time_str in time_list:
        minutes, seconds = map(int, time_str.split(':'))
        total_seconds = minutes * 60 + seconds
        seconds_list.append(total_seconds)
    
    return np.array(seconds_list)

def heating(t,k,P,Ti,Ta,L, C=4182):
    T = Ti*np.exp(k*t) + (Ta - 60 * (P/(L*C*k))) * (1 - np.exp(k*t))
    return T

instant_temperature = lambda k,P,Ti,Ta,L: heating(t=10,k=k,P=P,Ti=Ti,Ta=Ta,L=L)

def PID(e, t, errores, kp, ki, kd, dt=10):
    y = int(kp*e + ki*np.mean(errores)*t + kd*(e - errores[-1])/dt)

    if y < 0:
        y = 0
    elif y > 32:
        y = 32
    return y


def potencia(dim):
    #P = 1.22647602*x**(1.73489126)
    P = 422.45*np.arctan((84-dim)*0.0637275) + 455.68
    return P