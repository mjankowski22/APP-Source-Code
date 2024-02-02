import subprocess
import time
import os
import requests
import netifaces
from requests.packages.urllib3.util.connection import allowed_gai_family
import socket
import pandas as pd
from datetime import datetime,timedelta

def get_interface_ip(interface_name):
    print(netifaces.interfaces())
    addrs = netifaces.ifaddresses(interface_name)
    print(addrs)
    return addrs[netifaces.AF_INET][0]['addr']




def check_connection():
    interface_ip = get_interface_ip('eth0')
    
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
        response = session.get('http://192.168.88.252:5000', timeout=5)
        return response.status_code == 200
    except requests.RequestException:
        return False
    finally:
        s.close()


def send_whole_file():
    interface_ip = get_interface_ip('eth0')
    
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
        files = {'file': open('data.csv', 'rb')}
        print(files)
        response = session.post('http://192.168.88.252:5000/upload_file', files=files)
        print(response)
        return response.status_code == 200
    except requests.RequestException:
        return False
    finally:
        s.close()


def send_part(start, end):
    start = start[:10]
    end = end[:10]

    interface_ip = get_interface_ip('eth0')
    
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
        
        df = pd.read_csv('data.csv')
        
        # Tworzenie nowej kolumny tylko z datą dla porównania
        df['Date'] = pd.to_datetime(df['Date and time']).dt.date
        
        # Filtrowanie używając nowej kolumny 'Date'
        filtered_df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]
        
        if filtered_df.empty:
            return False
        
        # Usunięcie kolumny 'Date' przed zapisaniem, aby zachować oryginalny format
        filtered_df.drop(columns=['Date'], inplace=True)
        
        filtered_df.to_csv('data_to_send.csv', index=False)
        files = {'file': open('data_to_send.csv', 'rb')}
        response = session.post('http://192.168.88.252:5000/upload_file', files=files)
        print(response)
        if response.status_code == 200:
            os.remove('data.csv')
            os.remove('data_to_send.csv')
            return True
    except requests.RequestException:
        return False
    finally:
        s.close()
