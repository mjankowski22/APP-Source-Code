import serial
import time



serial_gps = serial.Serial('/dev/ttyUSB3', 9600, timeout=1)

def send_command_without_output(command):
    serial_gps.write(command.encode('utf-8'))
    bytesToRead = serial_gps.inWaiting()
    serial_gps.read(bytesToRead).decode('utf-8').rstrip()

def send_command(command):
        serial_gps.write(command.encode('utf-8'))
        time.sleep(0.5)
        bytesToRead = serial_gps.inWaiting()
        return(serial_gps.read(bytesToRead).decode('utf-8').rstrip())

def initialize_gps():
    send_command("AT+CGPS=1\r\n")
    
    


def get_gps_data():
    
    gps_data = send_command('AT+CGPSINFO\r\n')
    gps_data =gps_data[26:].split(',')

    try:
        lon = gps_data[1]+str(float(gps_data[0])/100)
        lat = gps_data[3]+str(float(gps_data[2])/100)
    except:
        lon=0
        lat=0
    return lon,lat


if __name__ == '__main__':
    initialize()
    time.sleep(5)
    
        