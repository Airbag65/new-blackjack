import random

class Game:
    def __init__(self) -> None:
        self.player = None
        self.dealer = None
        self.card = None
        self.play()

    def play(self) -> None:
        self.player = Player()
        if self.player.balance == None:
            self.buy_in()
            print("\n")
        for i in range(2):
            self.player.draw_card() 
        while(self.player.total < 21):
            print(f"Your total is {self.player.total}")
            if self.player.stayed == False:
                self.player.choice()
                break
    
    def buy_in(self) -> None:
        requested_balance = float(input("Enter your wanted buy-in amount: "))
        confirm_buy_in = input(f"You want to pay €{requested_balance} as buy-in? [Y/N] ")
        if confirm_buy_in.lower() == "y":
            self.player.balance = requested_balance
            print(f"\nYour balance is €{self.player.balance}")
        elif confirm_buy_in.lower() == "n":
            print(f"You denied the amount €{requested_balance}")
            self.buy_in()
        else:
            print(f"You did neither confirm nor deny the amount €{requested_balance}\n")
            self.buy_in()

       

class Card:
    def __init__(self) -> None:
        self.type = None
        self.value = None
        self.face_value = None
        self.possible_types = {
            1: "clubs",
            2: "spades",
            3: "diamonds",
            4: "hearts"
        }
        self.possible_face_values = {
            1: "Ace",
            2: "Two",
            3: "Three",
            4: "Four",
            5: "Five",
            6: "Six",
            7: "Seven",
            8: "Eight",
            9: "Nine",
            10: "Ten",
            11: "Jack",
            12: "Queen",
            13: "King"
            }
    
    def generate_card(self) -> None:
        gen_type = random.randint(1,4)
        gen_face_value = random.randint(1,13)
        self.type = self.possible_types[gen_type]
        self.face_value = self.possible_face_values[gen_face_value]
        if gen_face_value >= 10:
            self.value = 10
        else:
            self.value = gen_face_value
        print(self.face_value + " of " + self.type)
        print(self.value)



class Player:
    def __init__(self) -> None:
        self.hand = []
        self.total = 0
        self.action = ""
        self.stayed = False
        self.balance = None

    def draw_card(self) -> None:
        self.new_card = Card()
        self.new_card.generate_card()
        self.hand.append(self.new_card)
        self.total += self.new_card.value

    def choice(self) -> None:
        self.action = input("Would you like to HIT or STAY? [H/S]")
        if self.total < 21:
            if self.action.lower() == "h":
                self.draw_card()
                self.choice()
                print(f"Your total is {self.total}")
            elif self.action.lower() == "s":
                self.stayed = True
            else:
                print("Neither HIT nor STAY was chosen!\nTry again!\n")
                self.choice()
        else:
            print(f"Your total is {self.total}")


        
if __name__ == "__main__":
    new_game = Game()