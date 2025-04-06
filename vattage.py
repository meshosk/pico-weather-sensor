# just test file

import ubluetooth
import time
from machine import Pin, ADC

ble = ubluetooth.BLE()


def suspend_ble():
    
  #  ble.gap_advertise(None)  # Zastaví advertising
    
    ble.active(False)
    
    
def resume_ble():
    ble.active(True)
   # ble.gap_advertise(interval_us=1000)  # Opäť začne advertising

def read_battery_voltage():
    time.sleep(1)
    adc = ADC(Pin(29))  # GP29 (ADC3)
    raw = adc.read_u16()
    voltage = (raw / 65535) * 3.3
    return voltage * 2  # Ak máš deliaci mostík 100k/100k

while True:
    suspend_ble()  # Vypneme BLE pred meraním
    battery_voltage = read_battery_voltage()
    print("Batéria:", round(battery_voltage, 2), "V")
    resume_ble()  # Obnovíme BLE po meraní
