# exercise_poker_functions.py  
# This file uses hand data from load_data.py and functions from poker_functions.py  
# Diane Kaplan        November 2016
#
# Usage:
#     % python exercise_poker_functions.py 

from load_data import load_hands 
from poker_functions_v2 import read_hand, compare_hands #, compare_multiple_hands, find_best_hand
#import profile  # uncomment, with last line, to see call count/times/etc

all_hands = load_hands()

# evaluate the example hands in our data
print ('\n First, evaluate example hands: ')
for hand in all_hands: 
    this_hand = all_hands[hand]
    outcome = read_hand(this_hand)[0]
    kicker = read_hand(this_hand)[2]
    print ('\n', this_hand, 'evaluates to:', outcome, 'with kicker: ', kicker)

# call specific matchups to see the winners 

# save them locally for display
hand_1 = all_hands['hand_1']
hand_2 = all_hands['hand_2']
hand_3 = all_hands['hand_3']
hand_4 = all_hands['hand_4']
hand_6 = all_hands['hand_6']
hand_7 = all_hands['hand_7']
hand_8a = all_hands['hand_8a']
hand_9 = all_hands['hand_9']
hand_10 = all_hands['hand_10']
hand_11 = all_hands['hand_11']

# get their scores
hand_1_outcome = read_hand(hand_1)
hand_2_outcome = read_hand(hand_2)
hand_3_outcome = read_hand(hand_3)
hand_6_outcome = read_hand(hand_6)
hand_7_outcome = read_hand(hand_7)
hand_8a_outcome = read_hand(hand_8a)
hand_9_outcome = read_hand(hand_9)
hand_10_outcome = read_hand(hand_10)
hand_11_outcome = read_hand(hand_11)

# now compare hands and show matchups/winners
print ('\n Then, matchup time:')

print ('\n Flush vs 4 of a kind: ', hand_2, 'vs', hand_3 )
print ('The winner is:' , compare_hands(hand_2, hand_3) )

print ('\n Straight vs 3 of a kind: ', hand_6, 'vs', hand_7 )
print ('The winner is:' , compare_hands(hand_6, hand_7) )

print ('\n 4 of kind tiebreak: ', hand_3, 'vs', hand_11 )
print ('The winner is:' , compare_hands(hand_3, hand_11))

print ('\n Royal flush vs straight flush: ', hand_1, 'vs', hand_2 )
print ('The winner is:' , compare_hands(hand_1, hand_2))

print ('\n Two pairs vs full house: ', hand_8a, 'vs', hand_4 )
print ('The winner is:' , compare_hands(hand_8a, hand_4))

print ('\n One pair vs high card: ', hand_9, 'vs', hand_10 )
print ('The winner is:' , compare_hands(hand_9, hand_10))


#profile.run('compare_hands(hand_6, hand_7)')