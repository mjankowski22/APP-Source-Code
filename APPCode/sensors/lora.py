import serial
import time
import re
from datetime import datetime
import json
import sonda 
import gps
import fiveg
import wifi

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
        gps_data = gps.get_gps_data()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        msg = f'M,{timestamp},{gps_data[0]},{gps_data[1]},{sonda.check_memory_size()}'
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
                if values.get('5g_check',0)==1:
                    connection = fiveg.check_connection()
                    if connection:
                        msg = f'P,{1}'
                    else:
                        msg = f'P,{0}'
                if values.get('5g_send_whole',0)==1:
                    response = fiveg.send_whole_file()
                    if response:
                        msg = f'G,{1}'
                    else:
                        msg = f'G,{0}'
                if values.get('5g_send_part',0)==1:
                    response = fiveg.send_part(values.get('start'),values.get('end'))
                    if response:
                        msg = f'A,{1}'
                    else:
                        msg = f'A,{0}'
                
                if values.get('wifi_check',0)==1:
                    connection = wifi.check_connection()
                    if connection:
                        msg = f'B,{1}'
                    else:
                        msg = f'B,{0}'
                if values.get('wifi_send_whole',0)==1:
                    response = wifi.send_whole_file()
                    if response:
                        msg = f'C,{1}'
                    else:
                        msg = f'C,{0}'
                if values.get('wifi_send_part',0)==1:
                    response = wifi.send_part(values.get('start'),values.get('end'))
                    if response:
                        msg = f'D,{1}'
                    else:
                        msg = f'D,{0}'
                
                send_command_without_output(f'AT+MSG="{msg}"\r\n')

if __name__ == '__main__':
    initialize()
    time.sleep(5)
    
        