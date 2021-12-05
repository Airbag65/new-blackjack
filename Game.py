import random
import pwinput
import json
import encr_table
import os
import sys
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
        print(f"\n{self.first_name} {self.last_name} was added!")
        time.sleep(1)


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
            login_or_create = input("Login to existing account or create new account? [L/C]")
            if login_or_create.lower() == "l":
                self.login()
            elif login_or_create.lower() == "c":
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
                self.player.balance = account['balance']
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
            time.sleep(.75)
            self.menu()
        
    
    def decode(self, password) -> str:
        temp_pass = ""
        for letter in password:
            if letter in encr_table.table():
                temp_pass += encr_table.table()[letter]
            else:
                temp_pass += letter
        password = temp_pass
        return password
            
    
    def menu(self) -> None:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"Welcome Back {self.player.first_name}!")
        print(f"\nYour balance is at the moment: {self.player.balance} SEK")
        print("What would you like to do?")
        menu_choice = input("Start playing / Quit / Deposit / Withdraw? [S/Q/D/W]: ")
        if menu_choice.lower() == 'd':
            self.deposit()
        elif menu_choice.lower() == 'w':
            self.withdraw()
        elif menu_choice.lower() == 'q':
            self.quit()
        elif menu_choice.lower() == 's':
            self.play()
        else:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Input not reqognized!")
            time.sleep(.7)
            self.menu()
            

    def deposit(self) -> None:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("NOT YET IMPLEMENTED!\n")
        time.sleep(1)
        print("Redirecting to MENU...")
        time.sleep(1)
        self.menu()


    def withdraw(self) -> None:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("NOT YET IMPLEMENTED!\n")
        time.sleep(1)
        print("Redirecting to MENU...")
        time.sleep(1)
        self.menu()


    def quit(self) -> None:
        os.system('cls' if os.name == 'nt' else 'clear')
        self.save()
        print(f"\nSorry to see you go {self.player.first_name}\nSHUTTING DOWN...\n")
        time.sleep(1)


    def save(self) -> None:
        with open ("game.json", "r") as open_file:
            data = json.load(open_file)
            open_file.close()
        accounts = data['accounts']
        for account in accounts:
            if account['username'] == self.player.username:
                account['balance'] = self.player.balance
                break
            else:
                continue
        write_file = open("game.json", "w+")
        write_file.write(json.dumps(data, indent = 4, sort_keys = True))
        write_file.close()


    def play(self) -> None:
        os.system('cls' if os.name == 'nt' else 'clear')
        self.place_bet()
        for i in range(2):
            print("")
            self.player.draw_card()
        if self.player.hand[0].value == 1 or self.player.hand[1].value == 1:
            pass
        print(f"Your total is {self.player.total}\n")
        self.player.choice()
        if self.player.total == 21 and len(self.player.hand) == 2:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"\nBLACKJACK!\nYou win {self.player.current_bet*2.5} SEK")
            self.player.balance += self.player.current_bet*2.5
        if self.player.stayed:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"\nYour total is {self.player.total}\n")
            print("Dealer wins!\n")
            print(f"\nYour balance is now {self.player.balance} SEK")
        elif self.player.total > 21:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"\nYour total is {self.player.total}\n")
            print("Dealer wins!\n")
            print(f"\nYour balance is now {self.player.balance} SEK")
        self.player.hand = []
        self.player.current_bet = None
        self.player.action = None
        self.player.total = None
        self.replay()


    def replay(self) -> None:
        again = input("Replay or go back to MENU: [R/M]")
        if again.lower() == "r":
            self.play()
        elif again.lower() == "m":
            self.menu()
        else:
            print("Input not reqognized!")
            self.replay()


    def place_bet(self) -> None:
        print(f"Your current balance is: {self.player.balance} SEK")
        requested_bet = float(input("Enter your amount to bet (SEK): "))
        self.player.current_bet = requested_bet
        print(f"\nYour bet is {self.player.current_bet} SEK\n")
        self.player.balance -= self.player.current_bet


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
        self.current_bet = None


    def draw_card(self) -> None:
        new_card = Card()
        new_card.generate_card()
        self.hand.append(new_card)
        if new_card.face_value == 1:
            self.total += 11
        else:
            self.total += new_card.value


    def choice(self) -> None:
        self.action = input("Would you like to HIT or STAY? [H/S]")
        if self.total < 21 and self.stayed != True:
            if self.action.lower() == "h":
                self.draw_card()
                print(f"Your total is now {self.total}")
                self.choice()
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