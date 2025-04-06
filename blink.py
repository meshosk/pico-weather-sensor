# just test file

from machine import Pin
import time

# VBUS je pripojený na GPIO 24
vbus_pin = Pin('WL_GPIO2', Pin.IN)


while True:
    print(vbus_pin.value())  # Vytlačí hodnotu na pinu (0 alebo 1)
    time.sleep(1)