#!/usr/bin/python
# -*- coding:utf-8 -*-
import time
import gyros  # Gyroscope/Acceleration/Magnetometer
import temp  # Atmospheric Pressure/Temperature and humidity
import swiatlo  # LIGHT
from PIL import Image, ImageDraw, ImageFont
import math
import csv
from datetime import datetime
from w1thermsensor import W1ThermSensor

bme280 = temp.BME280()
bme280.get_calib_param()
light = swiatlo.TSL2591()
icm20948 = gyros.ICM20948()
data_and_time = datetime.now()
ds18b20 = W1ThermSensor()
# print(datetime.now())
# print("TSL2591 Light I2C address:0X29")
# print("LTR390 UV I2C address:0X53")
# print("SGP40 VOC I2C address:0X59")
# print("icm20948 9-DOF I2C address:0X68")
# print("bme280 T&H I2C address:0X76")

try:
    time.sleep(1)
    bme = bme280.readData()
    pressure = round(bme[0], 2)
    temp = round(bme[1], 2)
    hum = round(bme[2], 2)
    lux = round(light.Lux(), 2)
    icm = icm20948.getdata()
    temp_sonda = ds18b20.get_temperature()
    # print("==================================================")
    # print("pressure : %7.2f hPa" % pressure)
    # print("temp : %f C" % temp)
    # print("hum : %f " % hum)
    # print("lux : %d " % lux)
    # print("Roll = %.2f , Pitch = %.2f , Yaw = %.2f" % (icm[0], icm[1], icm[2]))
    # print("Acceleration: X = %d, Y = %d, Z = %d" % (icm[3], icm[4], icm[5]))
    # print("Gyroscope:     X = %d , Y = %d , Z = %d" % (icm[6], icm[7], icm[8]))
    # print("Magnetic:      X = %d , Y = %d , Z = %d" % (icm[9], icm[10], icm[11]))

    header = ["Date and time", "Temperature Inside", " Atmospheric Pressure ", "Light Intensity", "Water Temperature"]
    with open("data.csv", 'r', newline='') as check_header:
        csv_reader = csv.reader(check_header)
        first_row = next(csv_reader, None)
        if first_row != header:
            with open("data.csv", 'w', newline='') as write_header:
                csv_writer = csv.writer(write_header)
                csv_writer.writerow(header)
    with open("data.csv", 'a', newline='') as output_file:
        csv_writer = csv.writer(output_file)
        data = [data_and_time, temp, pressure, lux, temp_sonda]
        csv_writer.writerow(data)
except KeyboardInterrupt:
    exit()
