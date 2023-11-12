import random
from abc import abstractmethod
from enum import Enum
from typing import *
from treys import *




class Player:
    class Action(Enum):
        START = 0
        CALL = 1
        RAISE = 2
        FOLD = 3
        CHECK = 4
        END = 6
    is_small_blind = False
    is_big_blind = False
    hand:[Card] = []
    score:int = 0
    playing:bool = False
    player_history:[Action] = []

    @abstractmethod
    def eval_turn(self, public_cards:[Card], other_players, other_raised):
        pass


class HumanPlayer(Player):

    def eval_turn(self, public_cards: [Card], other_players, other_raised):
        print("Your cards are:")
        print([Card.int_to_pretty_str(x) for x in self.hand])
        print("The public cards are:")
        print([Card.int_to_pretty_str(x) for x in public_cards])
        print("What action do you do?")
        move = input("1 - CALL, 2 - RAISE, 3 - FOLD, 4 - CHECK")
        move = Player.Action(int(move))
        print("Your action is: ",move.name)
        return move

class RandomPlayer(Player):

    def eval_turn(self, public_cards: [Card], other_players, other_raised):
        print("Your cards are:")
        print([Card.int_to_pretty_str(x) for x in self.hand])
        print("The public cards are:")
        print([Card.int_to_pretty_str(x) for x in public_cards])
        print("What action do you do?")
        if other_raised != None:
            move = random.randint(1,
                                  2)  # If someone else raised then we need to either call (match bet) or raise
        else:
            move = random.randint(1,4) # TODO Need to take into account illogical actions and decrease the odds that it folds as turns progress
        move = Player.Action(move)
        print("Your action is: ",move.name)
        return move

class Game:
    deck = Deck()
    players:[Player] = []
    public_cards:[Card] = []
    hand:int = 0
    evaluator = Evaluator()
    max_raise_count = 2

    def setup_game(self, player_count = 1, use_human_players=False):
        self.state = Game.State.START
        self.deck.shuffle()
        self.public_cards = self.deck.draw(3)
        for player_number in range(player_count):
            if use_human_players:
                player = HumanPlayer()
            else:
                player = RandomPlayer()
            player.hand = self.deck.draw(2)
            self.players.append(player)

    class State(Enum):
        START = 0
        END = -1
        PREFLOP = 1
        FLOP = 2
        TURN = 3
        RIVER = 4

    state = State.START
    #TODO new hand function that shuffles players

    def _turn_loop(self):
        player_raised = None
        turn_raise_count = 0
        while True:
            for player in self.players:
                # Skip the folded players
                if len(player.player_history) > 0:
                    if player.player_history[-1] == Player.Action.FOLD:
                        continue
                # Check if we went around completely
                if player_raised is player:
                    # We went a full round with other people not matching
                    break
                while True:
                    action = player.eval_turn(public_cards=[], other_players=self.players,
                                              other_raised=player_raised is None)
                    if action == Player.Action.RAISE and turn_raise_count == self.max_raise_count:  # Ensure that bots / people only call /check  or fold if max amount of raises has been reached
                        print("Max raises done, please call or fold.")
                        continue
                    break
                player.player_history.append(action)
                # If someone raised successfully then we count that and set who raised
                if action == Player.Action.RAISE:
                    turn_raise_count += 1
                    player_raised = player
            if player_raised is None:
                break
    def game_loop(self):
        while self.state != Game.State.END:
            # TODO take into account folds and re-raise
            # TODO add betting / amounts
            if self.state == Game.State.START:
                self.state = Game.State.PREFLOP
            elif self.state == Game.State.PREFLOP:
                print("Starting the game...")
                # Initial round of betting without seeing the table...
                self._turn_loop()
                self.state = Game.State.FLOP
            elif self.state == Game.State.FLOP:
                print("In flop...")
                self._turn_loop()
                self.state = Game.State.TURN
            elif self.state == Game.State.TURN:
                additional = self.deck.draw(1)
                self.public_cards.extend(additional)
                self._turn_loop()
                self.state = Game.State.RIVER
            elif self.state == Game.State.RIVER:
                additional = self.deck.draw(1)
                self.public_cards.extend(additional)
                self._turn_loop()
                self.state = Game.State.END
        player_scores = [self.evaluator.evaluate(self.public_cards, player.hand) for player in self.players]
        print(player_scores)
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


if __name__ == '__main__':
    g = Game()
    g.setup_game(player_count=1,use_human_players=False)
    g.game_loop()
