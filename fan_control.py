import gpiod
import time

def setup_gpio():
    chip = gpiod.Chip('gpiochip0')
    line = chip.get_line(4)  # GPIO 4
    line.request(consumer='fan_control', type=gpiod.LINE_REQ_DIR_OUT)
    return line

def read_temperature():
    # Här ska din temperaturavläsning in
    # Just nu simulerar vi med en fast temperatur
    return 22.0

def main():
    print("Startar temperaturbaserad fläktkontroll...")
    line = setup_gpio()

    try:
        while True:
            temp = read_temperature()
            print(f"Aktuell temperatur: {temp:.2f}°C")
            if temp > 22.0:
                print("🔛 Temperatur hög – fläkt på.")
                line.set_value(1)
            else:
                line.set_value(0)
            time.sleep(1)
    except KeyboardInterrupt:
        print("Avslutar program...")

if __name__ == "__main__":
    main()

