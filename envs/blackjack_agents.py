"""
Action Codes:
0: Stand
1: Hit
2: Split - TBA
3: Double Down - TBA
4: Insurance - TBA
"""

import random

class Hand:
    def __init__(self):
        self.aces = 0
        self.total = 0
        self._hand = []
        
    def add_card(self, card):
        self._hand.append(card)
        if card.is_ace:
            self.aces += 1
        self.total += card.bj_number
            
    def get_hand(self):
        return self._hand
    
    def __repr__(self):
        return str(self._hand)
        

class Player:
    def __init__(self) -> None:
        self.hand = Hand()
        self.stack = 0

    def draw_card(self, card):
        self.hand.add_card(card)
        
    def clear_hand(self):
        self.hand = Hand()
    
    def set_stack(self, stack):
        self.stack = stack
    
    def perform_action(self, gamestate):
        raise NotImplementedError()
    
    def get_hand(self):
        return self.hand     
         

class Agent(Player):
    def load_policy(self,a):
        pass
    
    def perform_action(self, gamestate):
        return random.choice([0,1])
        # return 0