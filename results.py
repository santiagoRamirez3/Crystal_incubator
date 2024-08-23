import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

plt.close()

for i in os.listdir('./csv_data'):
    df = pd.read_csv('./csv_data/'+i,)

    # Convertir la columna 'time' a datetime
    df['time'] = pd.to_datetime(df['time'])

    # Calcular la diferencia en tiempo desde el primer valor
    df['time_diff'] = df['time'] - df['time'].iloc[0]

    # Convertir la diferencia de tiempo a horas
    df['hours_elapsed'] = df['time_diff'].dt.total_seconds() / 3600

    fig, ax = plt.subplots(1,1)
    ax.plot(df['hours_elapsed'],df['temperature'],label='lectura termómetro')
    ax.plot(df['hours_elapsed'],df['setpoint'],label='setpoint')
    ax.set_title('Prueba de funcionamiento sistema de control')
    ax.set_ylabel('Temperatura (°C)')
    ax.set_xlabel('Tiempo (h)')
    ax.legend()
    plt.savefig('./Result_plots/'+i+'.png', dpi=72)
    plt.close()

