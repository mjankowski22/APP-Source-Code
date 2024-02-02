import lora,gps
import time
import sonda
import fiveg

def init():
    lora.initialize_lora()
    gps.initialize_gps()
    fiveg.init5g()
    sonda.measure()


def loop():
    time_start = time.time()
    while True:
        time_now = time.time()
        if time_now-time_start>30:
            sonda.measure()
            time_start=time_now
        lora.lora_loop_step()
        time.sleep(0.3)


if __name__=='__main__':
    init()
    time.sleep(3)
    loop()