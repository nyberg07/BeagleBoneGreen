import smbus2
import time

# Exempel på SHT35 I2C-adress och register
I2C_ADDR = 0x44
CMD_MEASURE_HIGHREP_STRETCH = [0x2C, 0x06]

def read_temperature():
    bus = smbus2.SMBus(1)  # I2C bus 1 (vanligt på BeagleBone)
    bus.write_i2c_block_data(I2C_ADDR, CMD_MEASURE_HIGHREP_STRETCH[0], [CMD_MEASURE_HIGHREP_STRETCH[1]])
    time.sleep(0.5)
    data = bus.read_i2c_block_data(I2C_ADDR, 0, 6)

    temp_raw = data[0] << 8 | data[1]
    temperature = -45 + (175 * (temp_raw / 65535.0))
    return temperature

if __name__ == "__main__":
    temp = read_temperature()
    print(f"Temperatur: {temp:.2f}°C")

