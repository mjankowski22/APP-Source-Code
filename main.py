import lora,gps
import time
import sonda
import fiveg
import RPi.GPIO as GPIO
from flask import Flask
import threading
import sys
import os
from ina import initialize_ina

sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

def create_app():
    app = Flask(__name__)

    with app.app_context():
        from routes import init_routes
        init_routes(app)

    return app

def run_flask_app():
    app = create_app()
    app.run(host='0.0.0.0', port=5000)

def init():
    time.sleep(10)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(21,GPIO.OUT)
    GPIO.output(21,GPIO.HIGH)
    lora.initialize_lora()
    try:
        gps.initialize_gps()
    except:
        pass
    try:
        initialize_ina()
    except:
        pass

    fiveg.init5g()
    try:
        sonda.measure()
    except:
        pass



def loop():
    time_start = time.time()
    while True:
        time_now = time.time()
        if time_now-time_start>30:
            try:
                sonda.measure()
            except:
                pass
            time_start=time_now
        lora.lora_loop_step()
        time.sleep(0.3)


if __name__=='__main__':
    init()
    flask_thread = threading.Thread(target=run_flask_app)
    flask_thread.daemon = True
    flask_thread.start()
    time.sleep(3)
    loop()
