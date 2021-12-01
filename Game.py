import random

import Dealer
import Player

class Game:
    def __init__(self) -> None:
        self.player_balance = None
        self.player = None
        self.dealer = None
        self.card = None
        self.play()

    def play(self) -> None:
        self.player = Player()
        self.player.draw_card()

       

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
    
    def generate_card(self):
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
    def __init__(self):
        self.hand = []
        self.total = 0

    def draw_card(self):
        self.new_card = Card()
        self.new_card.generate_card()
        self.hand.append(self.new_card)
        self.total += self.new_card.value

        

new_game = Game()

