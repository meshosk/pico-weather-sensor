# The pico weather sensor

Code for my home-made weather sensor using:

* BME280 - it is collecting tempererature, humidity, air pressure and calculated sea level air pressure
* Pimoroni LiPo SHIM - for backup battery and resistor for VSYS voltage reading

It is using BLE to send following data in as binary (grabbed from testing html file for BLE run verification):

```javascript
d = {
          temperature : dataView.getFloat32(0).toFixed(2),
          humidity: dataView.getFloat32(4).toFixed(2),
          pressure: dataView.getFloat32(8).toFixed(2),
          seaPressure: dataView.getFloat32(12).toFixed(2),
          batteryVoltage: dataView.getFloat32(16).toFixed(2),
          batteryPercentage: dataView.getFloat32(20).toFixed(2),
          usbPlugged: dataView.getUint8(24)
      }
```

_Current state it is not fully energy or code (use of AI for faster development) optimized and will change in future._
