from deck import Deck, SixDeck, Card
from blackjack_agents import Agent, Hand

DEALER_STAND_LIMIT = 17
ACES_ARE_11 = True

class BJTable:
    # Will Store game state between multiple rounds - master deck, stack size, players etc
    def __init__(self, players, stacks, shuffle_limit = 70):
        self.players = players
        self.deck = SixDeck()
        self.SHUFFLE_LIMIT = shuffle_limit    
    
        if isinstance(stacks, (list, tuple)):
            self.stacks = {players[i]:stacks[i] for i in range(len(players))}
            
        elif isinstance(stacks, (int, float)):
            self.stacks = {p:stacks for p in players}

        else:
            self.stacks = stacks
            
        self.rounds = 1
        
        self.controller = BlackJack()
    
    def reset_round(self):
        for player in self.players:
            player.clear_hand()
            
        if self.deck.get_deck_size() < self.SHUFFLE_LIMIT:
            self.deck.shuffle()
    
    def play_game(self, rounds=1, until_bust = False):
        if until_bust:
            # Play forever
            pass
        
        for _ in range(rounds):
            game = BJRound(self.players, self.controller, self.deck)
            game.play()

        self.reset_round()
        self.rounds += 1
    
class BJRound:
    # Stores a single round of BlackJack - a game
    # Will draw cards, settle bets, turn order 
    def __init__(self, players, controller, deck, min_bet = 1) -> None:
        self.players = players
        self.complete = False
        self.controller = controller
        self.deck = deck
        self.dealer_hand = Hand()
        self.min_bet = min_bet
        self.bets = []

    def play(self):
        # Take bets - TBA
        
        # Give each player two cards
        self.deal_hands()
        
        # Each player takes turns sequentially
        for player in self.players:
            actions = []
            # The player can continue until they go bust or stand
            print(player.get_hand())
            while self.controller.in_play(player.get_hand(), actions):
                action = player.perform_action(self.get_gamestate())
                actions.append(action)
                outcome = self.process_action(player, action)
                  
        # Dealer Acts
        self.operate_dealer()
        
        self.controller.get_winners(self.players, self.dealer_hand)
        self.complete = True
        print(self)
    
    def process_action(self, player, action):
        if action == 0:
            return self.process_stand(player)
        
        if action == 1:
            return self.process_hit(player)
        
        # Return, in_play, drew, bet
            
    
    def process_stand(self, player):
        return False, False, False
    
    def process_hit(self, player):
        self.player_draws(player, 1)
        return True, True, False
    
    def operate_dealer(self):
        action = 1
        while action == 1:
            action = self.controller.perform_dealer(self.dealer_hand)
            if action == 1:
                self.dealer_hand.add_card(self.deck.draw()[0])
        
    
    def player_draws(self, player, cards):
        for card in self.deck.draw(cards):
            player.draw_card(card)
    
    def deal_hands(self):
        for player in self.players:
            self.player_draws(player, 2)
    
        self.dealer_hand.add_card(self.deck.draw()[0])
        self.dealer_hand.add_card(self.deck.draw()[0])
        
    def get_gamestate(self):
        pass
        
    def __repr__(self):
        return [player.get_hand() for player in self.players]
        
    def __str__(self):
        return str([player.get_hand() for player in self.players] + [self.dealer_hand.get_hand()])
    
class BlackJack:
    # Handles the logic of the game
    # If a hand is bust, when the dealer stands etc
    def __init__(self):
        pass
    
    def in_play(self, hand, actions):
        if not actions:
            return True
        if actions[-1] == 0: # Player Held
            return False
        return self.is_bust(hand)
    
    def is_bust(self, hand):
        return hand.total > 21
    
    def perform_dealer(self, hand):
        # Aces are assumed to equal 1 by default, so if bust before checking then no neeed to
        if hand.total > 21:
            return 0
        
        # If no aces, then just stand/hit depending on total
        if not hand.aces:
            return int(hand.total < DEALER_STAND_LIMIT) 
        
        # Dealer must count an ace as 11 if total is between 17-21 and stand
        if ACES_ARE_11:
            # Can not have two aces being coutned as 11 as this will cause a bust
            if DEALER_STAND_LIMIT <= hand.total + 10 <= 21: 
                return 0
            
            # If using one ace as an 11 causes a bust then will determine action with it being equal to 1
            return int(hand.total < DEALER_STAND_LIMIT) 
        
    def get_winners(self, player_hands, dealer_hands):
        pass
    
a = BJTable([Agent(), Agent()], 100)
a.play_game()