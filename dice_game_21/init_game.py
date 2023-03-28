from dice_game import game_dice
class Person:
    def __init__(self, name, sex, age):
        self.name = name
        self.sex = sex
        self.age = age
        self.init_game()
    
    def init_game(self):
        try:
            if str(input("Input yes: ")) == "yes":
                game_dice()
            else:
                pass
        except Exception as e:
            print(e)
        finally:
            print("Run game...")

if __name__ == "__main__":
    person = Person("Astra","woman", "27")
