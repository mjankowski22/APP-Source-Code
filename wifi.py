import subprocess
import time
import os
import requests
import netifaces
from requests.packages.urllib3.util.connection import allowed_gai_family
import socket
from datetime import datetime,timedelta

WIFI_STATUS = False

def check_wifi():

    try:
        addrs = netifaces.ifaddresses('eth0')
        addrs = addrs[netifaces.AF_INET][0]['addr']
    except:
        return False
    if addrs.split('.')[0]!='192':
        return False
    else:
        return addrs
        

