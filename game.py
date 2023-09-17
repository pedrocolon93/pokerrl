
class Game:
    deck:[Card] = []
    players:[Player] = []
    public_cards:[Card] = []
    hand:Int = 0

    def setup_game(self, player_count = 1):
        pass

    def start_hand(self):
        pass

    def game_loop(self):
        pass

class Action(Enum):
    START = 0
    CALL = 1
    RAISE = 2
    RE_RAISE = 3
    FOLD = 4
    CHECK = 5
    END = 6

class Player:
    hand:[Card] = []
    score:Int = 0
    playing:Bool = False
    player_history:[Action]
    def eval_turn(self, public_cards:[Card], other_players:[Player]):
        pass

class Suit(Enum):
    SPADES = 1
    DIAMONDS = 2
    CLOVER = 3
    HEARTS = 4

class Card:
    rank:Int
    suit:Suit
