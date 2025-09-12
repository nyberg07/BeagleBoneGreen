import random

try:
    # Get player names
    player1 = input("Ange namn för spelare 1: ").strip()
    player2 = input("Ange namn för spelare 2: ").strip()
    player3 = input("Ange namn för spelare 3: ").strip()
    players = [player1, player2, player3]

    while True:
        goal = random.randint(20, 50)  # Slutmål
        scores = {player1: 0, player2: 0, player3: 0}
        print(f"\nMålet är att nå {goal} poäng utan att gå över\n")
        scores = {player1: 0, player2: 0, player3: 0}
        stopped = {player1: False, player2: False, player3: False}
        quit_game = {player1: False, player2: False, player3: False}
        turn = 0  # 0 for player1, 1 for player2, 2 for player3

        while True:
            #Find next player who hasn't quit or stopped
            active_players = [p for p in players if not stopped[p] and not quit_game[p]]
            if not active_players:
                print("\nAlla spelare har slutat eller stannat. Spelet avslutas.\n")
                break
            current_player = players[turn % 3]
            # Skip if player has quit or stopped
            if stopped[current_player] or quit_game[current_player]:
                turn += 1
                continue

            print(f"{current_player}s tur. Du har nu {scores[current_player]} poäng och målet är {goal}.")
            val = input("skriv '+' för att kasta på nytt eller '-' för att stanna, eller 'q' för att sluta: ").strip()
            if val == "+":
                num = random.randint(1, 15)  # "tärningen"
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
            if all(stopped.values()):
                # Determine winner
                diff1 = goal - scores[player1] if scores[player1] <= goal else float('inf')
                diff2 = goal - scores[player2] if scores[player2] <= goal else float('inf')
                diff3 = goal - scores[player3] if scores[player3] <= goal else float('inf')
                if diff1 < diff2:
                    print(f"\n{player1} vinner med {scores[player1]} poäng, närmast målet {goal}!\n")
                elif diff2 < diff1:
                    print(f"\n{player2} vinner med {scores[player2]} poäng, närmast målet {goal}!\n")
                elif diff2 < diff3:
                    print(f"\n{player3} vinner med {scores[player3]} poäng, närmaste målet {goal}!\n")
                else:
                    print(f"\nOavgjort! Båda är lika nära målet {goal}.\n")
                break

            turn += 1  # Next player's turn

        play_again = input("Vill ni spela igen? (j/n): ")
        if play_again.lower() != 'j':
            print("Tack för att ni spelade!")
            break
except KeyboardInterrupt:
    print("\nSpelet avslutat. Tack för att ni spelade!")