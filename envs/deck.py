import random

SUITS = ['HEARTS', 'DIAMONDS', 'CLUBS', 'SPADES']
SUITS_TO_VALS = {s:k+1 for k, s in enumerate(SUITS)}
NUMS_TO_VALS = {1: 'Ace', 11: 'Jack', 12: 'Queen', 13: 'King'}

class Deck:
    def __init__(self):
        new_deck = self._create_deck()
        self.master_deck = new_deck.copy()
        self.deck = new_deck.copy()
        self.shuffle()
    
    def _create_deck(self):
        return [Card(n, s) for n in range(1, 14) for s in SUITS] 
    
    def shuffle(self, full_deck = True):
        # Full_deck = True resets the game to use all 52 cards
        # False will only shuffle carrds cuyrrently in the deck
        if full_deck:
            self.deck = self.master_deck.copy()
        random.shuffle(self.deck)
    
    def get_deck_size(self):
        return len(self.deck)
    
    def draw(self, cards = 1):
        drawn_cards = []
        for _ in range(cards):
            drawn_cards.append(self.deck.pop(0))
        return drawn_cards

    def __repr__(self):
        return f'{self.get_deck_size()} cards in the deck. \n {self.deck}'
    
class SixDeck(Deck):
    def _create_deck(self):
        return [BlackJackCard(n, s) for n in range(1, 14) for s in SUITS]  * 6
    
class Card:
    def __init__(self, number, suit):
        self.number = number
        self.name = NUMS_TO_VALS.get(number, number)
        self.suit = suit
        self.suit_num = SUITS_TO_VALS[suit]
        
    def get_int(self):
        return self.suit_num * 100 + self.number
        
    def get_name(self):
        pass
        
    def __repr__(self):
        return f'{self.name} {self.suit}'
    
    def __str__(self):
        return f'{self.name} {self.suit}'
    
class BlackJackCard(Card):
    def __init__(self, number, suit):
        super().__init__(number, suit)
        if number > 10:
           self.bj_number = 10
        else:
            self.bj_number = number 
            
        self.is_ace = (number == 1)
            
        