import random
import getpass
import pwinput
import json
import encr_table
import os
import time


class Create_Account:
    def __init__(self) -> None:
        self.username = None
        self.first_name = None
        self.last_name = None
        self.phone_number = None
        self.password = None
        self.encr_password = None
        self.encr_table = encr_table.table()
        
    
    def create_account(self) -> None:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Create new account\nMake sure to check that what has been typed is correct before proceeding!\n")
        self.username = input("Username: ")
        self.first_name = input("First Name: ")
        self.last_name = input("Last Name: ")
        self.phone_number = input("Phone Number: ")
        self.new_account_password()
        self.encr_password = ""
        for letter in self.password:
            if letter in self.encr_table:
                self.encr_password += self.encr_table[letter]
            else:
                self.encr_password += letter
        new_account = {
            'username': f'{self.username}',
            'first_name': f'{self.first_name}',
            'last_name': f'{self.last_name}',
            'phone_number': f'{self.phone_number}',
            'password': f'{self.encr_password}',
            'balance': 0
            }

        with open ("game.json", "r") as open_file:
            data = json.load(open_file)
            open_file.close()

        data['accounts'].append(new_account)

        write_file = open("game.json", "w+")
        write_file.write(json.dumps(data, indent = 4, sort_keys = True))
        write_file.close()


    def new_account_password(self):
        password = pwinput.pwinput()
        print("Confirm password: ")
        confirm_pass = pwinput.pwinput()
        if password == confirm_pass:
            self.password = password
        else:
            print("\nPasswords don't match")
            self.new_account_password()



class Game:
    def __init__(self) -> None:
        self.player = None
        self.dealer = None
        self.card = None


    def boot_game(self) -> None:
        self.start_page()


    def start_page(self) -> None:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("\n\nWelcome To BLACKJACK TERMINAL!\n\n")
            login_create = input("Login to existing account or create new account? [L/C]")
            if login_create.lower() == "l":
                self.login()
            elif login_create.lower() == "c":
                new_account = Create_Account()
                new_account.create_account()
                self.start_page()


    def login(self) -> None:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Login to existing account!\n")
        self.player = Player()
        with open ("game.json", "r") as open_file:
            data = json.load(open_file)
            open_file.close()
        entered_username = input("Username: ")
        for account in data['accounts']:
            if entered_username == account['username']:
                print(f"\nAccount with username: {entered_username} found!\n")
                self.player.username = entered_username
                self.player.password = account['password']
                self.player.first_name = account['first_name']
                self.player.last_name = account['last_name']
                self.player.phone_number = account['phone_number']
                break
            else:
                continue
        if self.player.username != entered_username:
            print(f"Account with username: {entered_username} not found!")
            time.sleep(.5)
            self.login()
        else:
            entered_password = pwinput.pwinput()
            entered_password = self.decode(entered_password)
        if entered_password != self.player.password:
            print("\nLogin attempt failed: WRONG PASSWORD")
            time.sleep(1)
            self.login()
        else:
            print("Login Successful!")
            self.player.logged_in = True
            print(self.player.logged_in)
            

    def decode(self, password) -> str:
        temp_pass = ""
        for letter in password:
            if letter in encr_table.table():
                temp_pass += encr_table.table()[letter]
            else:
                temp_pass += letter
        password = temp_pass
        return password




    def play(self) -> None:
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
        self.username = None
        self.first_name = None
        self.last_name = None
        self.phone_number = None
        self.password = None
        self.logged_in = False


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
                print(f"Your total is now {self.total}")
            elif self.action.lower() == "s":
                self.stayed = True
            else:
                print("Neither HIT nor STAY was chosen!\nTry again!\n")
                self.choice()
        else:
            print(f"Your total is {self.total}")


        
if __name__ == "__main__":
    new_game = Game()
    new_game.boot_game()