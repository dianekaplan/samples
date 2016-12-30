# -*- coding: utf-8 -*-
# poker_functions.py  Helper functions for poker example 
# Diane Kaplan        November 2016

import numpy

DEBUG = False


# First, save names and values for our hand types 
from collections import namedtuple

hand_info = namedtuple('hand_info', 'name value')

RF = hand_info (name='Royal Flush', value=10)
SF = hand_info (name='Straight Flush', value=9)
FK = hand_info (name='Four of a Kind', value=8)
FH = hand_info (name='Full House', value=7)
FL = hand_info (name='Flush', value=6)
ST = hand_info (name='Straight', value=5)
TK = hand_info (name='Three of a Kind', value=4)
TP = hand_info (name='Two Pair', value=3)
OP = hand_info (name='One Pair', value=2)
HC = hand_info (name='High Card', value=1)


# compare_hands ("function #2") takes two json arrays with 5 cards each 
# it calls the read_hands function to score them each, and
# returns the hand with the higher score
# @TODO: add tiebreak handling for two flush hands
def compare_hands(hand_1, hand_2): 
    winner = 'tie'
    hand_1_outcome = read_hand(hand_1)
    hand_2_outcome = read_hand(hand_2)
    
    if  hand_1_outcome[1] > hand_2_outcome[1]:
        winner = hand_1
    elif  hand_1_outcome[1] < hand_2_outcome[1]: 
        winner = hand_2
    else: 
        
        # Two of the same hand, so let's loop through the ordered hand for highest kicker
        for a, b in zip(hand_1_outcome[2], hand_2_outcome[2]):
            if a > b:
                winner = hand_1
                break;
            elif b > a:
                winner = hand_2
                break;
    return winner
    
# In progress: updated function #2 to compare multiple hands- need to test   
def compare_multiple_hands(array_of_hands): 
    
    highest_verdict = 0 
    this_hand_verdict = 0
    winning_hand = []

    for hand in array_of_hands: 
        this_hand_verdict = read_hand(hand)
        
        # if this hand beats current leader, replace it (score in index 1)
        if this_hand_verdict[1] > highest_verdict[1]:
            highest_verdict = this_hand_verdict
            winning_hand = hand
        
        # if this hand ties current leader, call compare_hands
        if this_hand_verdict[1] == highest_verdict[1]:
            winning_hand = compare_hands(hand, winning_hand) 
                  
    return winning_hand

# find_best_hand ("function #3") takes a json array of 5 or more cards, and 
# returns array with the best 5-card hand we can make with those cards 
def find_best_hand(card_group):
    
    # sort the cards in the group
    
    # approach 1: test for each hand in order of highest value, quit when you get a hit
    # http://www.pokerlistings.com/poker-hand-ranking
    
    # approach 2 (brute force, n choose k): 
    # test all 5-card combinations from card_group: 
        # for each, send them to read_hand, keep track of the best score
    
    verdict = []
    return verdict
    
    
# read_hand ("function #1") takes a json array of 5 cards, and 
# returns array with three elements: name of the hand, score, and  
# the ordered hand (ex: 3H, 3C, 3D, 8S, 10C) used for tiebreak cases
def read_hand(hand): 
    # initialize variables to false/no hand
    has_flush = False
    has_straight = False
    verdict = ['Nothing', 0, 0] 
    values_list=[]
    suit_list=[]
    remainder = []
        
    [values_list, suit_list] = parse_suits_and_values(hand)
    
    # check for flush
    suit_set = set(suit_list) # unique values, will be one if it's a flush
    if len(suit_set) == 1:
        has_flush = True
    
    # check for straight (list average is the same as the middle)
    if values_list[2] == numpy.mean(values_list) and values_list[4]-values_list[0]==4:
        has_straight = True
    
    # check for multiples (pairs, three of a kind, four of a kind)
    # highest_freq will be 4 for four of a kind, etc
    highest_freq = 0
    this_freq = 0
    most_repeated_value = 0
    for number in values_list: 
        this_freq = values_list.count(number)
        
        if this_freq > highest_freq:
            highest_freq = this_freq
            most_repeated_value = number
    
    # if we didn't have any repeats, start the hand at "High Card" 
    if highest_freq ==1: 
             high_card = max(values_list)
             verdict = [HC.name, HC.value, high_card] # @TODO: update with ordered_hand approach
             
    # otherwise (highest_freq > 1), let's get the hand's verdict as a 2/3/4 of a kind or full house
    else: 
        verdict = interpret_multiples(values_list, highest_freq, most_repeated_value)
                             
        
    # Then see if we can upgrade to straight and/or flush
    # @FIXME: third return value not needed here- more confusing to include, or to have different signature?)
    if has_straight: 
        verdict = [ST.name, ST.value, hand]
        
    if has_flush: 
        verdict = [FL.name, FL.value, hand]
            
    if has_flush & has_straight: 
        verdict = [SF.name, SF.value, hand]
        
        # and if highest card ace, it's a royal flush
        if values_list[4] == 14:
            verdict = [RF.name, RF.value, hand]

    return verdict
    


# Helper functions for read_hand
   
def parse_suits_and_values(hand): 
    # initialize variables to false/no hand

    values_list=[];
    numeric_values_list=[];
    suit_list=[];
    swap_list = {'J':'11', 'Q':'12', 'K':'13', 'A':'14'} 
    
    # populate values and suits list
    for card in hand: 
        length = len(card) # we'll have 2 or 3 digits (ex 4H or 10D)
        if length == 2: # one digit for value one char for suit
            values_list.append( card[0] );
            suit_list.append( card[1] );
        if length == 3: # two digits for value (10) one char for suit
            values_list.append( card[0:2] );
            suit_list.append( card[2] );

    # replace J->11, Q->12, K->13, A->14
    for value in values_list:

        if swap_list.get(value):
            value = swap_list[value]
    
        value = int(value) #convert to integer
        numeric_values_list.append(value)
    
    # put the values in order
    numeric_values_list.sort()
    
    return numeric_values_list, suit_list

    
def get_remainder(values_list, value_to_remove): 
    remainder = [value for value in values_list if value != value_to_remove] 
    return remainder
    

def interpret_multiples(values_list, highest_freq, most_repeated_value):

        # When we have multiples, we'll also use the hand's remainder (the other cards)
        # For readability, save the most_repeated_value into value_to_remove 
        value_to_remove = most_repeated_value
        
        # Get the remainder of the hand    
        remainder = get_remainder(values_list, value_to_remove)

        #To start, organize the hand into the 'good part' (may be improved later) and the rest
        hand =  highest_freq * [most_repeated_value] 
        ordered_hand = hand + remainder
            
        # Four of a kind 
        if highest_freq == 4:
            verdict = [FK.name, FK.value, ordered_hand] # we have four of a kind

        # Three of a kind 
        if highest_freq == 3:
            verdict = [TK.name, TK.value, ordered_hand]
            
            # check if that remainder is a pair (if yes, full house)
            if remainder[0] == remainder[1]: 
                verdict = [FH.name, FH.value, ordered_hand]

        # One pair 
        if highest_freq == 2:
            verdict = [OP.name, OP.value, ordered_hand] 
            
            # if remaining 3 cards contains a pair, update to 2 pair and update kicker
            #remainder = get_remainder(values_list, value_to_remove) # This was already done above
            
            # Two pair 
            # The remainder is sorted, so look for middle card matching either of the other two
            if ( remainder[0] == remainder[1] | remainder[1] == remainder[2] ) : 
                
                # note the value of our second pair
                second_pair_value = remainder[1]

                # extract the kicker card 
                value_to_remove = second_pair_value
                remainder = get_remainder(remainder, value_to_remove)  
                
                # update 'hand' to have both pairs, and sort for highest first 
                new_pair = 2 * [ second_pair_value ]
                hand = hand + new_pair
                hand.sort()
                    
                # update ordered_hand accordingly
                ordered_hand = hand + remainder

                # new verdict is 'two pair'
                verdict = [TP.name, TP.value, ordered_hand] 
                
        return verdict
