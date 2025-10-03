# Temperaturstyrd Fläktkontroll för BeagleBone – Enkel Guide

Detta projekt visar hur du styr en fläkt på din BeagleBone baserat på temperaturen. Fläkten slås på när temperaturen är hög och stängs av när den är låg.

---

## Vad behöver du?

- En BeagleBone med Debian Linux installerad.
- En fläkt ansluten till GPIO-pin 4 på BeagleBone (fysisk pinne kan behöva kollas).
- Grundläggande kunskaper i att använda terminalen (kommandoraden).
- Internetuppkoppling för att installera nödvändiga program.

---

## Steg 1: Förbered systemet

Öppna terminalen och skriv:

```bash
sudo apt update
sudo apt install python3 python3-libgpiod

Detta uppdaterar systemet och installerar Python samt biblioteket för att styra GPIO.

Steg 2: Skapa Python-skriptet
    1. Skriv i terminalen:
nano fan_control.py

Klistra in följande kod i editorn (för att klistra in, högerklicka eller använd Shift+Insert):
import gpiod
import time

def setup_gpio():
    chip = gpiod.Chip('gpiochip0')
    line = chip.get_line(4)
    line.request(consumer='fan_control', type=gpiod.LINE_REQ_DIR_OUT)
    return line

def read_temperature():
    # Här kan du koppla in riktig temperaturavläsning.
    # Just nu simuleras en temperatur på 22 grader.
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
                line.set_value(1)  # Slå på fläkt
            else:
                line.set_value(0)  # Stäng av fläkt
            time.sleep(1)
    except KeyboardInterrupt:
        print("Avslutar program...")

if __name__ == "__main__":
    main()

-------------------------------------------
Steg 3: Starta programmet
Skriv i terminalen:
sudo python3 fan_control.py



    Programmet körs och skriver ut aktuell temperatur varje sekund.

    När temperaturen är över 22°C slås fläkten på.

    När temperaturen är under 22°C stängs fläkten av.

Steg 4: Avsluta programmet
Tryck Ctrl+C för att stoppa programmet när du vill.
Tips och råd
    • Behöver du hjälp? Fråga gärna en erfaren användare eller i BeagleBone-forum.
    • Temperaturavläsning: Koden läser just nu bara ett fast värde (22°C). Du kan byta ut funktionen read_temperature() mot riktig sensoravläsning.
    • Anslutningar: Kontrollera att fläkten är korrekt kopplad till GPIO 4.
    • Behörigheter: Programmet måste köras med sudo för att få tillgång till GPIO.

Felsökning vanliga problem
    • Om du får felmeddelande om att gpiod saknar attribut som LineRequest, se till att du installerat python3-libgpiod via apt, inte via pip.
    • Om fläkten inte startar, kontrollera kopplingar och att GPIO-numret är rätt.

Så här kan du fortsätta
    • Lägg till riktig temperaturavläsning med sensor.
    • Skapa en tjänst så att programmet startar automatiskt när BeagleBone startar.
    • Spara temperaturdata i en loggfil för uppföljning.

Grattis!
Du har nu en fungerande temperaturstyrd fläktkontroll på din BeagleBone. 🎉

