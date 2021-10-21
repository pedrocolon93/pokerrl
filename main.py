from random import sample

import numpy
from torch.utils.data import Dataset


class PokerGamesDataset(Dataset):
    def __init__(self, amount_of_games=1000):
        self.data = []
        for i in range(amount_of_games):
            game = []
            deck = [x for x in range(52)]
            for part_idx, part in enumerate(["preflop","flop","turn","river"]):
                play_cards = numpy.ones(6,)*-1
                play_cards[0] = part_idx
                if part == "preflop":
                    pass
                elif part == "flop":
                    flop_cards = sample(deck,3)
                    for flop_idx, flop_card in enumerate(flop_cards):
                        play_cards[flop_idx+1] = flop_card
                    for i in range(len(flop_cards)):
                        deck.pop(deck.index(flop_cards.pop()))
                elif part == "turn":
                    flop_cards = sample(deck, 1)
                    for flop_idx, flop_card in enumerate(game[-1][1:4].tolist()+flop_cards):
                        play_cards[flop_idx + 1] = flop_card
                    for i in range(len(flop_cards)):
                        deck.pop(deck.index(flop_cards.pop()))
                elif part == "river":
                    flop_cards = sample(deck,1)
                    for flop_idx, flop_card in enumerate(game[-1][1:5].tolist()+flop_cards):
                        play_cards[flop_idx+1] = flop_card
                    for i in range(len(flop_cards)):
                        deck.pop(deck.index(flop_cards.pop()))
                game.append(play_cards)
            self.data.append(game)
    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        return self.data[i]

if __name__ == '__main__':
    PokerGamesDataset()
