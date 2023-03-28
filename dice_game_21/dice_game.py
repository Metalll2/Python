from function import randomize_dice
import time

def game_dice():
    VALUES_DICE = (1,2,3,4,5,6)
    queue_throw = ["BOT"]
    point = {"BOT": 0}

    print('''-------------------------------------------------------------------------------------------------------------------------------
             A game similar to 21, only with a die. The goal is to reach 21 points, whoever scores first wins. Whoever gets close to 21 wins.
            --------------------------------------------------------------------------------------------------------------------------------
                                                        ████████████████████████████████████████
                                                        ██████████▀▀▀▀██████████████████████████
                                                        ███████▀░░░░░░░░░▄██████████████████████
                                                        ████▀▀░░░░▀▀░░▄▄█▀░░████████████████████
                                                        ███▄░░░░░░░░▄█▀░░░██░███████████████████
                                                        ██▀▀▀▀██▄▄▄▀▀░░░░░░░░▀██████████████████
                                                        ███░░░░▄▄▀█░░██░░░░░░░██████████████████
                                                        ████░░░░▀░█▄░░░░░▄▄▄█▄▄█████████████████
                                                        ████▄▄▄░░░░█▄░░░▄███▄░░░░░░░░▀▀█████████
                                                        ███████░░░░▀█░░██▀░░▀█▄▄░░░▀█▄░░▀▀██████
                                                        █████████▄▄░▀█░██░░░░░░▀█▄░░░░░░░░░░████
                                                        ████████████████░░░░░░░░░▀▀█▄▄███▀▀▀▀▀██
                                                        ████████████████░░░░░░░██░░█▀░▄░░░░▄░███
                                                        ███████████████░▄▄░░░░░▀▀░▄█░██░░░▀█████
                                                        ███████████████░██░░░░░░░░█░░░░░░░░░████
                                                        ████████████████▄░░░░░░░░██░░░░░░▄░█████
                                                        ██████████████████▄▄░░░░░█░▄▄░░░██▄█████
                                                        █████████████████████▄░░██▀█▀░░▄▄▄██████
                                                        ███████████████████████▄█▄▄▄████████████
    ''')

    start = str(input("Play?(yes/no)"))

    if start == "yes":
        start = True
        point[f'Player 1'] = 0
        queue_throw.append(f'Player 1')
    else:
        start = False
        pass

    while start:
        for i in queue_throw:
            if i == "BOT":
                    if point[i]<21:
                        print("BOT throw")
                        time.sleep(2)
                        throw_dice = randomize_dice(VALUES_DICE)
                        print(throw_dice)
                        point["BOT"]+=throw_dice
                        time.sleep(2)
                        print(f"{i} points:{point[i]}")
                    elif point[i] == 21 and point["Player 1"] != 21:
                        print(f'{i} winner, points:{point[i]}. Player 1 losses.')
                        start=False
                        break
                    elif point[i]>21 and (point["Player 1"] == 21 or point["Player 1"] < 21):
                        print(f'{i} loses, points:{point[i]}.Player 1 winner.')
                        start=False
                        break
            else:
                vubor=str(input("Throw(yes or no): "))
                if vubor=="yes":
                    if point[i]<21:
                        print(f"{i} throw")
                        time.sleep(2)
                        throw_dice = randomize_dice(VALUES_DICE)
                        print(throw_dice)
                        point[i]+=throw_dice
                        time.sleep(2)
                        print(f"{i} points:{point[i]}")
                    elif point[i]==21 and point["BOT"] != 21:
                        print(f'{i} winner, points:{point[i]}.BOT losses.')
                        start=False
                        break
                    elif point[i]>21 and  point["BOT"] < 21:
                        print(f'{i} loses, points:{point[i]}.BOT winner.')
                        start=False
                        break
                elif vubor=="no":
                        print(f'{i} loses, points:{point[i]}.BOT winner.')
                        start=False
                        break

