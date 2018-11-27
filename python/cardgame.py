# Implements a cards shuffler and dealer.

import random

class Card():
    suit = ["Spades", "Hearts", "Clubs", "Diamonds"]
    value = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]

    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def __str__(self):
        return f"{suit} of {value}"
        
class Deck():
    
    def shuffle(self):
        random.shuffle(cards)
        
    def deal(self, card):
        if card in self.cards:
            self.cards.remove(card)
            return True
        else:
            return False
    
    def __init__(self):
        self.suits = ['Hearts','Diamonds','Clubs','Spades']
        self.values = ['A','2','3','4','5','6','7','8','9','10','J','Q','K']
        
        self.cards = []
        for suit in range(4):
            for value in range(1, 14):
                self.cards.append(Card(suit, value))
     
    def __str__(self):
        return f"{len(self.cards)} cards in the deck"
        
if __name__ == "__main__":
    deck = Deck()
    card = deck.deal('card')
    print(card)
