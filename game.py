from abc import abstractmethod
from enum import Enum
from typing import *
from treys import *




class Player:
    class Action(Enum):
        START = 0
        CALL = 1
        RAISE = 2
        RE_RAISE = 3
        FOLD = 4
        CHECK = 5
        END = 6
    is_small_blind = False
    is_big_blind = False
    hand:[Card] = []
    score:int = 0
    playing:bool = False
    player_history:[Action]

    @abstractmethod
    def eval_turn(self, public_cards:[Card], other_players):
        pass

class Game:

    deck = Deck()
    players:[Player] = []
    public_cards:[Card] = []
    hand:int = 0
    evaluator = Evaluator()

    def setup_game(self, player_count = 1):
        self.state = Game.State.START
        self.deck.shuffle()
        self.public_cards = self.deck.draw(3)
        for player_number in range(player_count):
            player = Player()
            player.hand = self.deck.draw(2)

    class State(Enum):
        START = 0
        END = -1
        PREFLOP = 1
        FLOP = 2
        TURN = 3
        RIVER = 4

    state = State.START
    #TODO new hand function that shuffles players

    def game_loop(self):
        while self.state != Game.State.END:
            if self.state == Game.State.START:
                for player in self.players:
                    action = player.eval_turn(public_cards=self.public_cards, other_players=self.players)
                    player.player_history.append(action)
                self.state = Game.State.PREFLOP
            elif self.state == Game.State.PREFLOP:
                for player in self.players:
                    action = player.eval_turn(public_cards=self.public_cards, other_players=self.players)
                    player.player_history.append(action)

                self.state = Game.State.FLOP
            elif self.state == Game.State.FLOP:
                for player in self.players:
                    action = player.eval_turn(public_cards=self.public_cards, other_players=self.players)
                    player.player_history.append(action)

                self.state = Game.State.TURN
            elif self.state == Game.State.TURN:
                for player in self.players:
                    action = player.eval_turn(public_cards=self.public_cards, other_players=self.players)
                    player.player_history.append(action)

                self.state = Game.State.RIVER
            elif self.state == Game.State.RIVER:
                for player in self.players:
                    action = player.eval_turn(public_cards=self.public_cards, other_players=self.players)
                    player.player_history.append(action)

                self.state = Game.State.END
        player_scores = [self.evaluator.evaluate(self.public_cards, player.hand) for player in self.players]
        self.hand+=1


#
class Suit(Enum):
    SPADES = 1
    HEARTS = 2
    DIAMONDS = 3
    CLUBS = 4

SuitMap = {
    1:Suit.SPADES,
    2:Suit.HEARTS,
    4:Suit.DIAMONDS,
    8:Suit.CLUBS
}

#
class Cardy:
    _card = None
    rank:int
    suit:int
    def __init__(potato, card:Card):
        potato.rank = Card.get_rank_int(card)
        potato.suit = Card.get_suit_int(card)

    def __str__(self):
        return "Rank:"+str(self.rank)+" Suit:"+str(self.suit)


print("Hello")
if __name__ == '__main__':
    c = Card.new("Ah")
    ca = Cardy(c)
    print(SuitMap[ca.suit])
    print(ca)
