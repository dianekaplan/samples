# -*- coding: utf-8 -*-
# load_data.py
# Diane Kaplan        November 2016
# Load the data we'll use

def load_hands(): 
    example_hands = {
    'hand_1': ["JS", "KS", "10S", "QS", "AS"], # royal flush
    'hand_2': ["9D", "8D", "7D", "6D", "5D"], # straight flush
    'hand_3': ["4H", "4C", "4S", "4D", "2H"], # 4 of a kind, kicker = 2
    'hand_11': ["2H", "2C", "2D", "2C", "KH"], # 4 of a kind, kicker = K
    'hand_4': ["4D", "4C", "4S", "9C", "9H"], # full house   
    'hand_5': ["4H", "3H", "AH", "2H", "9H"], # flush
    'hand_6': ["6H", "7C", "8S", "10C", "9H"], # straight  
    'hand_7': ["6H", "7C", "2S", "2C", "2H"], # 3 of a kind        
    'hand_8': ["JH", "4C", "4S", "3C", "3H"], # 2 pairs, not recognized (0==1)
    'hand_8a': ["JH", "4C", "4S", "JC", "3H"], # 2 pairs, recognized (1==2)
    'hand_9': ["JH", "4C", "4S", "10C", "9H"], # 1 pair
    'hand_10': ["2H", "5C", "JS", "AC", "3D"], # high card
    }
         
    return example_hands
