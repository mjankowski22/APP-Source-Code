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
    try:
        gps_data = send_command('AT+CGPSINFO\r\n')
        gps_data =gps_data[26:].split(',')
        print(gps_data)
    except:
        return 0,0
    try:
        # Konwersja szerokości geograficznej
        lat_deg = float(gps_data[0][:2])
        lat_min = float(gps_data[0][2:])
        lat = lat_deg + lat_min / 60.0
        lat = gps_data[1]+str(lat)
        
        # Konwersja długości geograficznej
        lon_deg = float(gps_data[2][:2])
        lon_min = float(gps_data[2][2:])
        lon = lon_deg + lon_min / 60.0
        lon = gps_data[3]+str(lon)
    except:
        lon = 0
        lat = 0

    return lon, lat


if __name__ == '__main__':
    initialize_gps()
    time.sleep(5)
    
        
