# -*- coding:utf-8 -*-
import time
import gyros  # Gyroscope/Acceleration/Magnetometer
import temp  # Atmospheric Pressure/Temperature and humidity
import swiatlo  # LIGHT
import math
import csv
from datetime import datetime
from w1thermsensor import W1ThermSensor
import os
import shutil
import gps



def measure():
    bme280 = temp.BME280()
    bme280.get_calib_param()
    light = swiatlo.TSL2591()
    icm20948 = gyros.ICM20948()
    data_and_time = datetime.now()
    try:
        ds18b20 = W1ThermSensor()
    except Exception as e:
        print(e)

    try:
        time.sleep(1)
        if not os.path.exists('/home/b-hermanowski/sensors/data.csv'):
            with open("/home/b-hermanowski/sensors/data.csv", 'w', newline='') as new_file:
                csv_writer = csv.writer(new_file)
                header = ["Date and time", "Temperature Inside", "Atmospheric Pressure", "Light Intensity",
                      "Water Temperature", "LocalizationN", "LocalizationE"]
                csv_writer.writerow(header)
                print('Utworzono csv')
        bme = bme280.readData()
        pressure = round(bme[0], 2)
        temperature = round(bme[1], 2)
        hum = round(bme[2], 2)
        lux = round(light.Lux(), 2)
        icm = icm20948.getdata()
        try:
            temp_sonda = ds18b20.get_temperature()
        except Exception as e :
            temp_sonda = 25.4

        loc = gps.get_gps_data()
        with open("/home/b-hermanowski/sensors/data.csv", 'a', newline='') as output_file:
            csv_writer = csv.writer(output_file)
            data = [data_and_time, temperature, pressure, lux, temp_sonda, loc[0], loc[1]]
            csv_writer.writerow(data)
            print('Measured')
    except KeyboardInterrupt:
        exit()
    


def check_memory_size():
    max_memory, used, free_mem = shutil.disk_usage("/")
    free_mem = free_mem / (2 ** 30)
    try:
        file_size = os.path.getsize('/home/b-hermanowski/sensors/data.csv') / (2 ** 30)
    except:
        file_size = 0
    return str(round((file_size / free_mem) * 100, 2))
