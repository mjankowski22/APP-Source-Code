from ina219 import INA219

ina = None

def initialize_ina():
    global ina
    ina = INA219(shunt_ohms=0.1,
                max_expected_amps = 0.6,
                address=0x40)

    ina.configure(voltage_range=ina.RANGE_16V,
                gain=ina.GAIN_AUTO,
                bus_adc=ina.ADC_128SAMP,
                shunt_adc=ina.ADC_128SAMP)
    return ina


def get_voltage():
    global ina
    v = ina.voltage()
    return v
        
        
