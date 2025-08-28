import smbus2

try:
    bus = smbus2.SMBus(2)
    who_am_i = bus.read_byte_data(0x76, 0xD0)
    print(f"Sensor svarar! WHO_AM_I = 0x{who_am_i:02X}")
except Exception as e:
    print("Ingen sensor hittades eller fel uppstod:")
    print(e)
