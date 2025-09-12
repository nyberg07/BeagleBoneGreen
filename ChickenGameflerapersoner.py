import random

try:
    antal_spelare = int(input("Hur många spelare är ni? (2 eller fler): ").strip())
    if antal_spelare < 2:
        print("Ni måste vara åtmistone 2 spelare!")
        exit()

    players = []
    for i in range(antal_spelare):
        namn = input(f"Ange namn för spelare {i + 1}: ").strip()

    while True:
        goal = random.randint(20, 50)
        scores = {player: 0 for player in players}
        stopped = {player: False for player in players}
        quit_game = {player: False for player in players}
        print(f"\nMålet är att nå {goal} poäng utan att gå över\n")

        turn = 0

        while True:
            active_players = [p for p in players if not stopped[p] and not quit_game[p]]
            if not active_players:
                print("\nAlla spelare har slutat eller stannat. Spelet avslutas.\n")
                break

            current_player = players[turn % antal_spelare]

            if stopped[current_player] or quit_game[current_player]:
                turn += 1
                continue

            print(f"{current_player}s tur. Du har nu {scores[current_player]} poäng och målet är {goal}.")
            val = input("skriv '+' för att kasta på nytt eller '-' för att stanna, eller 'q' för att sluta: ").strip()
            if val == "+":
                num = random.randint(1, 15)
                print(f"Du kastade {num} och har nu totalt {scores[current_player] + num} poäng\n")
                scores[current_player] += num
                if scores[current_player] > goal:
                    print(f"BUST! {current_player} har {scores[current_player]} vilket gick över \n")
                    scores[current_player] = 0
                    stopped[current_player] = True
            elif val == "-":
                print(f"{current_player} har stannat på {scores[current_player]} poäng!")
                stopped[current_player] = True
            elif val.lower() == "q":
                print(f"{current_player} har valt att sluta spelet.")
                quit_game[current_player] = True
                stopped[current_player] = True
            else:
                print("ogiltigt val, försök igen")
                continue

            # Check if both players have stopped
            if all(stopped[p] or quit_game[p] for p in players):
                winner = None
                closest_diff = float('inf')
                for player in players:
                    if scores[player] <= goal:
                        diff = goal - scores[player]
                        if diff < closest_diff:
                            closest_diff = diffwinner = player
                        elif diff == closest_diff:
                            winner = None
                if winner:
                    print(f"\n{winner} vinner med {scores[winner]} poäng, närmast målet {goal}!\n")
                else:
                    print(f"\nOavgjort! Alla är lika nära målet {goal}.\n")
                break

            turn += 1

        play_again = input("Vill ni spela igen? (j/n): ")
        if play_again.lower() != 'j':
            print("Tack för att ni spelade!")
            break
except KeyboardInterrupt:
    print("\nSpelet avslutat. Tack för att ni spelade!")