
===File list: 
exercise_poker_functions.py	Demonstrate poker functions
poker_functions.py		Functions for reading & comparing poker hands
load_data.py			File to load the data we'll use 

===Usage: 
python exercise_poker_functions.py 

===Done: 
- function #1 (read_hand()) evaluates all the hand types with kicker
- function #2 (compare_hands()) evaluates two hands and gives the winner

===Not done: 
- update compare_hands to take more than 2 hands: I started in compare_multiple_hands, 
need to finish/test
- find_best_hand() function
- poker_functions.py: I'd rather save that hand_info data out of the way (pickle dump it on 
load_data.py and pickle load on poker.functions.py?)
- tiebreak case for flush
- tiebreak testing for straight

===Open issues: 
- read_hand(), two pair case: not recognizing second pair when it's smaller than the kicker 


