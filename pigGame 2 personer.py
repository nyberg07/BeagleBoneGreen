import random

def kasta(spelare):
    sum = 0
    while True:
        num =  random.randint(1,6)
        print(f"{spelare} kastade en {num}")

        if num == 1:
            print(f"Sorry, du tappade dina poäng från denna runda")
            return 0
        sum += num
        print(f"{spelare}s rundpoäng: {sum}")

        val = input(f"{spelare}, tryck på 'k' för att kasta igen eller 's' för att spara dina poäng: ")
        match val: 
            case "k":
                continue
            case "s":
                return sum
            case _: print("Ogiltigt val, försök igen.")

def main():
    poäng = {"Spelare 1": 0, "Spelare 2": 0}
    tur = "Spelare 1"

    while True:
        print(f"\n--- {tur}s tur ---")

        poäng[tur] += kasta(tur)
        print(f"{tur}s totala poäng: {poäng[tur]}")
 
        if poäng[tur] >= 100:
            print(f"\n {tur} vann spelet med {poäng[tur]}!")
            
            break
        
        tur = "Spelare 2" if tur == "Spelare 1" else "Spelare 1"
        input("Tryck 'enter' för att byta spelare...")

if __name__ == "__main__":
    main()