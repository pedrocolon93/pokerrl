import random
import numpy as np
import math
import itertools
from collections import Counter

my_hand = random.choices(range(0,51),k=2)
op_hand = np.random.choice([n for n in range(0,51) if n not in my_hand],2,False).tolist()
all_cards = np.random.choice([n for n in range(0,51) if n not in my_hand+op_hand],5,False).tolist()

a = set(get_all_combinations(my_hand,all_cards))
b = set(get_all_combinations(op_hand,all_cards))
# pos = [n for n in itertools.combinations(my_hand+all_cards,5)]
# suits = [[int(x/13) for x in n] for n in pos]
# numbers = [[int(x%13) for x in n] for n in pos]
# dups = [[x for x in Counter(n).most_common()] for n in numbers]
# for comb in numbers:
#     comb.sort()
    
def is_flush(hand):
    hand = [int(x/13) for x in hand]
    if len(set(hand))==1:
        return True
    return False
def is_straight(hand):
    hand = [x%13 for x in hand]
    hand.sort()
    if hand == [n for n in range(hand[0],hand[0]+5)]:
        return True
    return False
def max_dups(hand):
    number, duplicates = hand[0]
    if duplicates==4:
        return number,7 # four of a kind
    if duplicates == 3:
        if hand[1][1] == 2:
            return number,6 #full house
    if duplicates == 2:
        if hand[1][1] == 2:
            return max([n[0] for n in hand if n[1]==2]),2.5 #two pairs
    if duplicates == 1:
        all_numbers = [n[0] for n in hand]
        return max(all_numbers),1
    
    return number,duplicates #either pair (2) or three of a kind (3)

def get_all_combinations(my_cards,public_cards):
    possible_hands = [n for n in itertools.combinations(my_cards+public_cards,5)]
    numbers  = [[int(x%13) for x in n] for n in possible_hands]
    dups = [[x for x in Counter(n).most_common()] for n in numbers]
    best_combo = (0,0)
    hand_values = []
    for pos in dups:
        eval_combo = max_dups(pos)
        hand_values.append(eval_combo)
#         print(eval_combo,pos)
        if eval_combo[1]>best_combo[1]:
            best_combo = eval_combo
        if eval_combo[1]==best_combo[1]:
            if eval_combo[0]>best_combo[0]:
                best_combo = eval_combo
#     print(hand_values)
    hand_values+= [(n%13,1) for n in my_cards]
    return hand_values

  def choose_winner(comb_a,comb_b):
    unique_combos = comb_a ^ comb_b
    if len(unique_combos)==0:
        return 'Tie'
    unique_a = sorted(list(comb_a & unique_combos), key=lambda k: k[1],reverse=True)
    unique_b = sorted(list(comb_b & unique_combos), key=lambda k: k[1],reverse=True)
    print()
    for ix in range(len(min(unique_a,unique_b))):
        high_card_a, combo_a = unique_a[ix]
        high_card_b, combo_b = unique_b[ix]
        if combo_a > combo_b:
            return 'A wins',unique_a[ix],unique_b[ix]
        if combo_a < combo_b:
            return 'B wins',unique_a[ix],unique_b[ix]
        if combo_a == combo_b:
            if high_card_a > high_card_b:
                return 'A wins',unique_a[ix],unique_b[ix]
            if high_card_a < high_card_b:
                return 'B wins',unique_a[ix],unique_b[ix]
