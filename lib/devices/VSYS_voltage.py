from machine import Pin, ADC, mem32
import time

# 2025 Matej Meško
#
# Class for simplifing getting voltage by USYS when using
# for exmaple Pimoroni pico lipo shim in Raspberry pico 2 W with external battery.
# 
# This class do not require to turn of bluetooth, because it stored
# pin 29 state, reinicialize ADC and then puts state back 
# 
# This measurement is crude and provide only voltage
# 
# This class is mixture of code parts from:
#
# https://github.com/pimoroni/pimoroni-pico/blob/main/micropython/examples/pico_lipo_shim/battery_pico.py
# https://github.com/danjperron/PicoWSolar/blob/main/mqtt_ds18B20.py
#      
class VSYS_voltage:

    def __init__(self, 
                 battery_full = 4.3, # full battery voltage
                 battery_empty= 2.8, # empty battery voltage
                 voltage_multiplier = 3  # 3 multiplier is based on  https://github.com/danjperron/PicoWSolar/blob/main/mqtt_ds18B20.py
                 ):      
        self._vbus_pin = Pin('WL_GPIO2', Pin.IN) # VBUS sense is in this virtual pin for PICO 2 W
        self._battery_full  = battery_full
        self._battery_empty =  battery_empty
        self._voltage_multiplier = voltage_multiplier

    # true if USB voltage is connected
    @property
    def is_usb_connected(self):
        return self._vbus_pin.value() == 1
    
    @property
    def battery_voltage(self):

        #if (self.is_usb_connected):
          #  return 5 # voltage from USB is 5V
        
        oldpad = self.getPad(29) # store actual state of pin
        self.setPad(29,128)  #no pulls, no output, no input
        time.sleep(.55) # little sleep to gain more stable result > https://forums.raspberrypi.com/viewtopic.php?t=345234#p2069690
        # set voltage adc, use Pin not ADC id, it will set as pin number
        adc_Vsys = ADC(Pin(29)) # create new ADC so it is corectly inicialized

        raw = adc_Vsys.read_u16() # read the value

        voltage = (raw / 65535) * 3.3 # (3.3 V on Pico)
        real_voltage = voltage * self._voltage_multiplier 

        self.setPad(29,oldpad) # retur pre read state for pin
        return round(real_voltage, 2)
    
    @property
    def power_source(self):
        if (self.is_usb_connected):
            return "USB"
        else:
            return "battery"
    
    @property
    def battery_percentage(self):

        percentage = 100 * ((self.battery_voltage - self._battery_empty) / (self._battery_full - self._battery_empty))
        if (percentage > 100):
            percentage = 100.00
        return round(percentage, 2)

    # grabbed from
    def setPad(self, gpio, value):
        mem32[0x4001c000 | (4+ (4 * gpio))] = value
        
    def getPad(self, gpio):
        return mem32[0x4001c000 | (4+ (4 * gpio))]