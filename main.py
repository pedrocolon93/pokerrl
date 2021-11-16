import itertools
from copy import deepcopy
from random import sample

import numpy
import torch
from torch.utils.data import Dataset
import pytorch_lightning as pl

class PokerGamesDataset(Dataset):
    def __init__(self, amount_of_games=1000):
        self.data = []
        for i in range(amount_of_games):
            game = []
            deck = [x for x in range(52)]
            amount_of_people = 2
            cards_per_person = 2
            people_cards = []
            for person in range(amount_of_people):
                samp = sample(deck,cards_per_person)
                people_cards.append(deepcopy(samp))
                for _ in range(len(samp)):
                    deck.pop(deck.index(samp.pop()))
            s = numpy.array([_ for _ in itertools.chain.from_iterable(people_cards)])
            for part_idx, part in enumerate(["preflop","flop","turn","river"]):
                play_cards = numpy.ones(6+amount_of_people*cards_per_person,)*-1
                play_cards[6:]=s
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
        return self.data[idx]

def initialize_internal_context(x):
    return torch.zeros(x.shape)

class PlayerModel(pl.LightningModule):
    def __init__(self, initial_amount, initial_order):
        self.total = initial_amount
        self.current_bet = 0
        self.id = initial_order
        self.order_of_play = initial_order
        self.previous_action = -1
        self.internal_context = None
        self.gru = torch.nn.GRU(input_size)#LEER

    def forward(self, x):
        if self.internal_context is None:
            self.internal_context = initialize_internal_context(x)





class PokerGOD(pl.LightningModule):
    def __init__(self, amount_of_players=2, amount_per_player=100, big_blind=10):
        super().__init__()
        self.big_blind = big_blind
        self.small_blind = int(big_blind/2)
        self.amount_of_players = amount_of_players
        self.players = [PlayerModel(amount_per_player,p) for p in range(amount_of_players)]


    def training_step(self, batch, batch_idx):
        for batch_item in batch:
            context_vector = []
            for part in batch_item:
                context_vector.extend(part)
                past_actions = []
                players_cash = []
                players_current_bet = []
                for player in self.players:
                    past_actions.append(player.previous_action)
                    players_cash.append(player.total)
                    players_current_bet.append(player.current_bet)
                context_vector.extend(past_actions)
                context_vector.extend(players_cash)
                context_vector.extend(players_current_bet)
                players_context_vectors = []
                mask_place = 6
                sec_start = 6

                for player in self.players:
                    pv = deepcopy(context_vector)
                    temp = pv[mask_place:mask_place+1]
                    for loc in range(sec_start,self.amount_of_players*2+sec_start):
                        pv[loc]=-1
                    idx = 0
                    for loc in range(mask_place,mask_place+1):
                        pv[loc] = temp[idx]
                        idx+=1
                    mask_place+=2
                    players_context_vectors.append(pv)

                for idx,pv in players_context_vectors:


        pass

if __name__ == '__main__':
    ds = PokerGamesDataset()
