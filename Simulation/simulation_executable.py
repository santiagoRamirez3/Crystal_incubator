from Classes import *

time = ['00:00','01:07','01:49','02:36','03:17','03:55','04:47','05:26','06:10',
        '06:55','07:36','08:28','09:03','09:53','10:37','11:25','12:09','12:58',
        '13:34','14:23','15:22','15:57','16:36','17:21','18:11','19:05','19:50',
        '20:36','21:28','22:14','23:07','24:29','25:19','26:09','27:03','27:52',
        '28:43','29:36','30:20','31:35','32:08','32:57','33:50','34:47','35:31',
        '36:36','37:26','38:15','39:14','40:13','41:07','41:56','49:55','52:03']

temperature = [24.3, 25. , 25.5, 26. , 26.5, 27. , 27.5, 28. , 28.5, 29. , 29.5, 30. ,
               30.5, 31. , 31.5, 32. , 32.5, 33. , 33.5, 34. , 34.5, 35. , 35.5,
               36. , 36.5, 37. , 37.5, 38. , 38.5, 39. , 39.5, 40. , 40.5, 41. ,
               41.5, 42. , 42.5, 43. , 43.5, 44. , 44.5, 45. , 45.5, 46. , 46.5,
               47. , 47.5, 48. , 48.5, 49. , 49.5, 50.,  54.,  55.]

#----------------------------------------------------------------------------------------

tank = Tank_characterizer(data_time = time,
                          data_temperature = temperature,
                          liters = 20,
                          ambient_temperature = 25.0,
                          mode = 'HEATING')                # 'HEATING' or 'COOLING'

#----------------------------------------------------------------------------------------

# Esta es la funcion de enfriamiento o calentamiento que depende 

def cooling_function(hours):
    base_temperature = 55.  # Temperatura base en grados Celsius
    increment = -0.5         # decrecimiento de temperatura cada hora
    return base_temperature + (increment * (hours // 2))



#print(tank.k)

tank.simulation(setpoint_function = cooling_function,
                file_name = 'simulation_example_2',
                kp = 35,
                ki = 30,
                kd = 0,
                water_initial_temperature = 55.,
                external_temperature = 25.,
                final_time = 12,
                presition = 0.1)