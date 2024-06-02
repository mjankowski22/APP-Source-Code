import subprocess
import time
import os
import requests
import netifaces
from requests.packages.urllib3.util.connection import allowed_gai_family
import socket
import csv
from datetime import datetime, timedelta

def get_interface_ip(interface_name):
    print(netifaces.interfaces())
    addrs = netifaces.ifaddresses(interface_name)
    print(addrs)
    return addrs[netifaces.AF_INET][0]['addr']

# Ścieżka do pliku wykonywalnego
command = "/home/b-hermanowski/SIM8200_for_RPI/Goonline/simcom-cm"

def init5g():
    # Uruchomienie polecenia z sudo
    process = subprocess.Popen(['sudo', command], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    pgid = os.getpgid(process.pid)
    print('5g initialized')

def check_connection():
    try:
        interface_ip = get_interface_ip('wwan0')
    except:
        return False
    
    # Tworzenie niestandardowego gniazda związane z konkretnym interfejsem
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((interface_ip, 0))  # Łączy gniazdo z adresem IP interfejsu

    # Używanie tego gniazda z requests
    adapter = requests.adapters.HTTPAdapter()
    session = requests.Session()

    # Dostosowanie sesji do używania niestandardowego gniazda
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    try:
        response = session.get('http://153.19.55.87:5000', timeout=5)
        return response.status_code == 200
    except requests.RequestException:
        return False
    finally:
        s.close()

def send_whole_file(delete):
    interface_ip = get_interface_ip('wwan0')
    
    # Tworzenie niestandardowego gniazda związane z konkretnym interfejsem
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((interface_ip, 0))  # Łączy gniazdo z adresem IP interfejsu

    # Używanie tego gniazda z requests
    adapter = requests.adapters.HTTPAdapter()
    session = requests.Session()

    # Dostosowanie sesji do używania niestandardowego gniazda
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    try:
        print('OK')
        files = {'file': open('/home/b-hermanowski/sensors/data.csv', 'rb')}
        response = session.post('http://153.19.55.87:5000/upload_file', files=files)
        if response.status_code == 200:
            if delete == 1:
                os.remove('data.csv')
            return True
    except requests.RequestException:
        return False
    finally:
        s.close()

def send_part(start, end, delete):
    start = start[:10]
    end = end[:10]

    interface_ip = get_interface_ip('wwan0')
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((interface_ip, 0))
    
    adapter = requests.adapters.HTTPAdapter()
    session = requests.Session()
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    
    try:
        print('OK')
        start_date = datetime.strptime(start, "%Y-%m-%d").date()
        end_date = datetime.strptime(end, "%Y-%m-%d").date()
        end_date = (datetime.combine(end_date, datetime.min.time()) + timedelta(days=1) - timedelta(seconds=1)).date()

        with open('/home/b-hermanowski/sensors/data.csv', 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            fieldnames = reader.fieldnames
            rows_to_send = []

            for row in reader:
                row_date = datetime.strptime(row['Date and time'], "%Y-%m-%d %H:%M:%S").date()
                if start_date <= row_date <= end_date:
                    rows_to_send.append(row)

        if not rows_to_send:
            return False

        with open('/home/b-hermanowski/sensors/data_to_send.csv', 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows_to_send)

        files = {'file': open('data_to_send.csv', 'rb')}
        response = session.post('http://153.19.55.87:5000/upload_file', files=files)
        print(response)
        os.remove('/home/b-hermanowski/sensors/data_to_send.csv')
        if response.status_code == 200:
            if delete == 1:
                os.remove('/home/b-hermanowski/sensors/data.csv')
                
            return True
    except requests.RequestException:
        return False
    finally:
        s.close()
