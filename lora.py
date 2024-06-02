import serial
import time
import re
from datetime import datetime
import json
import sonda 
import gps
import fiveg
import wifi
import RPi.GPIO as GPIO
from ina import get_voltage



INTERVAL = 10
time_start = time.time()
serial_lora = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)

def send_command_without_output(command):
    serial_lora.write(command.encode('utf-8'))

def send_command(command):
        serial_lora.write(command.encode('utf-8'))
        time.sleep(0.5)
        bytesToRead = serial_lora.inWaiting()
        print(serial_lora.read(bytesToRead).decode('utf-8').rstrip())

def initialize_lora():
    send_command("AT+DR=EU868\r\n")
    send_command("AT+CH=NUM,0-2\r\n")
    send_command('AT+MODE=LWOTAA\r\n')
    send_command('AT+JOIN\r\n')
    


def lora_loop_step():
    global INTERVAL
    global time_start
    
    
    time_now = time.time()
    if time_now-time_start>INTERVAL:
        try:
            gps_data = gps.get_gps_data()
        except:
            gps_data = [0,0]
        try:
            voltage = get_voltage()
        except:
            voltage = 0
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        fiveg_connection = 1 if fiveg.check_connection() else 0
        wifi_addr = wifi.check_wifi()
        wifi_addr = '' if wifi_addr == False else wifi_addr
        msg = f'M,{wifi_addr},{gps_data[0]},{gps_data[1]},{sonda.check_memory_size()},{fiveg_connection},{voltage}'
        print(msg)
        send_command_without_output(f'AT+MSG="{msg}"\r\n')
        time_start=time_now
        
    received_data = serial_lora.readline().decode('utf-8').rstrip()
    if(received_data != ""):
        if(received_data == "+MSG: Done"):
            print("Message sent succesfully")
        elif(received_data == "+MSG: Please join network first"):
            send_command_without_output('AT+JOIN\r\n')
        elif("RX" in received_data):
            data = re.search(r'"([^"]*)"', received_data)
            if(data):
                data=data.group(1)
                data=bytes.fromhex(data)
                data = data.decode('utf-8')
                print(f"Data received: {data}")
                values = json.loads(data)
                print(values)
                if values.get('interval',0)!=0:
                    INTERVAL = values['interval']
                    msg = f'I,{INTERVAL}'
                    send_command_without_output(f'AT+MSG="{msg}"\r\n')
                if values.get('5g_send_whole',0)==1:
                    response = fiveg.send_whole_file(values.get('delete',0))
                    if response:
                        msg = f'G,{1}'
                    else:
                        msg = f'G,{0}'
                    send_command_without_output(f'AT+MSG="{msg}"\r\n')
                if values.get('5g_send_part',0)==1:
                    response = fiveg.send_part(values.get('start'),values.get('end'),values.get('delete',0))
                    if response:
                        msg = f'G,{1}'
                    else:
                        msg = f'G,{0}'
                    send_command_without_output(f'AT+MSG="{msg}"\r\n')
                
                if values.get('turn_wifi',0)==1:
                    state = GPIO.input(21)
                    if state == GPIO.HIGH:
                        GPIO.output(21,GPIO.LOW)
                    else:
                        GPIO.output(21,GPIO.HIGH)
                
                
                
                

if __name__ == '__main__':
    initialize_lora()
    time.sleep(5)
    
        
