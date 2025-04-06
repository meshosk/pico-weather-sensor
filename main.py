from lib.devices.VSYS_voltage import VSYS_voltage
from machine import Pin, I2C, ADC
import lib.devices.bme280_float as bme280
from lib.ble.mble import *
import time
import bluetooth
import struct


i2c = I2C(1, sda=Pin(14), scl=Pin(15))

led = Pin(16, Pin.OUT)
led.off()

devices = i2c.scan()

if not devices:
    print("Žiadne I2C zariadenie nebolo nájdené.")
else:
    print("Nájdené I2C zariadenia:", [hex(d) for d in devices])


battery = VSYS_voltage()

bme = bme280.BME280(i2c=i2c)
# Create a BLE instance and a BLEText peripheral
ble = bluetooth.BLE()
ble_text = MBLE(ble, "pico2w")

bme_result = []

while True:
    

    
    print()
    print("################")

    nabija = str(battery.battery_voltage) + "v" + " " + str(battery.battery_percentage) + "%"
    print("Napajanie:" , nabija)
    print("Senzor: ", bme.values[0], "norm:",bme.values[1], bme.values[2], "sea.lvl:",bme.sealevel/10, "hPha")
   
    if ble_text.is_connected():
        
        # read bytes only id there is device conected
        bme_result = bme.read_compensated_data(bme_result)
        # sending float with 2 presition number data as integers, so the need of multiply by 100
        # send_data = struct.pack(
        #     '>ffffHHH', 
        #     bme_result[0], # temperature
        #     bme_result[1], # humidity
        #     bme_result[2], # pressure
        #     bme.sealevel, # sea level presure
        #     battery.battery_voltage, # VSYS voltage
        #     battery.battery_percentage, # battery percentage
        #     battery.is_usb_connected # 1 - if has USB bower; 0 = running on internap battery
        # )
        
        send_data = b''.join([
            struct.pack('>ffffff',
                            bme_result[0], # temperature
                            bme_result[2], # humidity
                            bme_result[1]/100, # pressure
                            bme.sealevel/100, # sea level presure
                            battery.battery_voltage, # VSYS voltage
                            battery.battery_percentage # battery percentage
                         ),  # float ako 4 bajty
            # struct.pack('<HH', 
            #                 battery.battery_voltage, # VSYS voltage
            #                 battery.battery_percentage, # battery percentage
            #             ),     # int ako 2 bajty
            struct.pack('B', battery.is_usb_connected)         # boolean ako 1 bajt
        ])

        print(send_data)

        led.on()
        # ble_text.activate(True) # turn on BLE
        ble_text.send_bytes(send_data)
        # ble_text.activate(False) # turn off BLE to save energy
        led.off()
        print("Data send by BLE")
        
    else:
        print("No BLE device connected")
    
    time.sleep(1)    