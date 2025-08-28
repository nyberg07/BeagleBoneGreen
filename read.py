import smbus2
import bme280
import time

# Sensoradress (från i2cdetect)
address = 0x76

# Initiera I2C-buss 2
bus = smbus2.SMBus(2)

# Initiera BME280
calibration_params = bme280.load_calibration_params(bus, address)

# Läs kontinuerligt
while True:
    data = bme280.sample(bus, address, calibration_params)
    
    print(f"Temperatur: {data.temperature:.1f} °C")
    print(f"Luftfuktighet: {data.humidity:.1f} %")
    print(f"Lufttryck: {data.pressure:.1f} hPa")
    print("-------------------------------")
    time.sleep(2)
