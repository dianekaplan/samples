# -*- coding: utf-8 -*-
# find_splice_functions.py    
# This file contains helper functions for my project to find splice sites
# Diane Kaplan        April-May 2015
#
# Context:
# Genetic sequences include introns and exons, and only exons are translated code. 
# Seeing the functional importance of a sequence means cleanly removing the introns. 
# My project goes through a DNA sequence and: 
# 1) breaks it up into rough chunks where intron transitions are happening (based on changes in base frequencies), 
# 2) at those sites, iterate in the immediate area (99 base pairs) to find the best scoring donor or acceptor 
# motifs, and save their locations, and 
# 3) pass the original sequence with best scoring donor and acceptor sites to a function to 
# return the cleaned up ('transcribed') sequence with the introns removed
#
# Citations: 
# I'm using the general base frequencies for humans from here: http://seqanswers.com/forums/archive/index.php/t-12359.html
# find_change_points logic is based on these frequencies: http://www.ncbi.nlm.nih.gov/pmc/articles/PMC403801/figure/fig1/

import string
import sys
import profile
from cs58FileUtil import prepare, readFastaFile

DEBUG = False

# Take a short string you're testing and a type of motif (donor or acceptor)
# Return its probability as this motif if higher than happening by chance, otherwise return false
def evaluate_motif(string, motif_type): 
    seq = string
    prob_general = 0
    prob_in_motif = 0
    length = len(seq)

    # SETUP
    # Confirm that a valid type has been given
    # (Only called internally now, add usage check if ever called externally)
    valid_types = ["donor", "acceptor"]
    if motif_type not in valid_types:
        print "Expecting motif type of donor or acceptor"
        sys.exit()  

    # Emission probabilities:  
    # General human DNA probabilities from resource cited above
    general_prob = {'A': .2725, 'C': .189, 'G': .189, 'T':.2728}     
     
    # Approximated donor site probabilities (from motif logo in text)
    if motif_type == "donor":  
        pos1_prob = {'A': .4, 'C': .4, 'G': 0, 'T':.2}
        pos2_prob = {'A': .4, 'C': .2, 'G': .2, 'T':.2}
        pos3_prob = {'A': .13, 'C': .13, 'G': .61, 'T':.13}
        pos4_prob = {'A': 0, 'C': 0, 'G': 1, 'T':.0}
        pos5_prob = {'A': 0, 'C': 0, 'G': 0, 'T':1}
        pos6_prob = {'A': .4, 'C': .1, 'G': .4, 'T':.1}
        pos7_prob = {'A': .61, 'C': .13, 'G': .13, 'T':.13}
        pos8_prob = {'A': .1, 'C': .1, 'G': .7, 'T':.1}
        pos9_prob = {'A': .25, 'C': .25, 'G': .25, 'T':.25}    
        
        # Put these dictionaries into a list for easy comparison at that position
        library_list = [pos1_prob, pos2_prob, pos3_prob, pos4_prob, pos5_prob, pos6_prob, pos7_prob, pos8_prob, pos9_prob] 

        # Give higher weights to the positions with the highest degree of conservation
        weight_list = [1, 1, 2, 4, 4, 1.5, 1, 1, 1]  

    # Approximated acceptor site probabilities (from motif logo in text)
    elif motif_type == "acceptor": 
        pos1_prob = {'A': .20, 'C': .3, 'G': .2, 'T':.3} 
        pos2_prob = {'A': .20, 'C': .3, 'G': .2, 'T':.3} 
        pos3_prob = {'A': .20, 'C': .3, 'G': .2, 'T':.3} 
        pos4_prob = {'A': .20, 'C': .3, 'G': .2, 'T':.3} 
        pos5_prob = {'A': .20, 'C': .3, 'G': .2, 'T':.3} 
        pos6_prob = {'A': .20, 'C': .3, 'G': .2, 'T':.3}  
        pos7_prob = {'A': .15, 'C': .30, 'G': .1, 'T':.45}
        pos8_prob = {'A': .15, 'C': .30, 'G': .1, 'T':.45}
        pos9_prob = {'A': .25, 'C': .25, 'G': .25, 'T':.25}
        pos10_prob = {'A': .1, 'C': 6, 'G': 0, 'T':.3}
        pos11_prob = {'A': 1, 'C': 0, 'G': 0, 'T':0}
        pos12_prob = {'A': 0, 'C': 0, 'G': 1, 'T':0}  
        pos13_prob = {'A': .2, 'C': .2, 'G': .3, 'T':.2}  
        pos14_prob = {'A': .2725, 'C': .189, 'G': .189, 'T':.2728} 
        
        # Put these dictionaries into a list for easy comparison at that position
        library_list = [pos1_prob, pos2_prob, pos3_prob, pos4_prob, pos5_prob, pos6_prob, pos7_prob, pos8_prob, pos9_prob, pos10_prob, pos11_prob, pos12_prob, pos13_prob, pos14_prob]             

        #Give higher weights to the positions with the highest degree of conservation                 
        weight_list = [1, 1, 1, 1, 1, 1, 1, 1, 1.5, 2, 4, 4, 1.5, 1.5]  
        
    # First, get the general probability of emitting this short sequence (normal state- overall for human DNA)
    cursor=0
    tally = 1
    this_dict = general_prob
    while cursor < length:
        base = seq[cursor]  
        this_prob = (this_dict[base])
        tally *= this_prob
        cursor += 1
    prob_general= tally

    # Then, get the probability of this being emitted from our selected motif state
    cursor = 0
    tally = 1
    while (cursor < length) and tally > 0:  #we drop out if it becomes impossible
        base = seq[cursor]
        this_dict = library_list[cursor]
        this_weight = weight_list[cursor]
        this_prob = (this_dict[base])

        tally *= this_prob * this_weight
        cursor += 1
    prob_in_motif = tally
    
    if prob_in_motif > prob_general: 
        verdict = prob_in_motif
        
    # If likelihood by chance is higher, don't include in the candidates list
    else: 
        verdict = False 
    
    return verdict
    
# Take a sequence and predicted motif type and find a list of potential splice sites.  
# When this is called repeatedly for a sequence with multiple sites, we pass a 
# starting_offset value for start position (not cursor)
def find_motif(seq, motif_type, starting_offset): 
    total_length = len(seq)
    cursor = 0
    candidate_list = []  #This is where we'll save good results: starting position (not cursor), snippet, and score
    
    #Confirm that a valid type has been given.
    # (Only called internally now, add usage check if ever called externally)
    valid_types = ["donor", "acceptor"]
    if motif_type not in valid_types:
        print "Expecting motif type of donor or acceptor"
        sys.exit()  

    # Our convention above evaluates motifs in these lengths. 
    if motif_type == 'donor':  
            length_to_check = 9
            
    if motif_type == 'acceptor':
            length_to_check = 14
    
    while (cursor <= total_length-length_to_check): 
        this_segment = seq[cursor:cursor+length_to_check] 
        score = evaluate_motif(this_segment, motif_type)
        if score:
            candidate_list.append([cursor+starting_offset , this_segment, score])
        cursor += 1
    return candidate_list


# Take a list of lists for the splice sites identified, and return the one with the highest probability
# We assume the list-of-lists returned by the find_motif function above, where each list's element 2 is the score
# This could be simpler (and use max()) if I pass in a different format, but I want to be able to run them in sequence
def get_winner (list): 
    top_score = 0
    winning_list = ''
    for x in list:  
        if x[2] > top_score:
            top_score = x[2]  
            winning_list = x      
    return winning_list
    

# Take a sequence, list of donor sites, and list of acceptor sites, and return sequence with introns removed
# From the earlier functions, we'll assume the same format (list-of-lists) for donor sites and acceptor sites
def make_clean_seq (seq, donor_list, acceptor_list): 
    orig_seq = (seq)
    clean_seq = ''
    total_length = len(orig_seq)
    donor_list = donor_list
    acceptor_list = acceptor_list
    cursor = 0
    in_intron = False 
    in_exon = False  
    
    # Our convention for evaluate_motif uses a specific position, 9mers for donor sites and 14mers for acceptor sites
    # For donor motif: the first 3 bases are still exon, intron starts at 4
    # For acceptor motif: we look at 14bp, first 12 bases are intron, last 2 bases are exon (ex: acag|AG).  
    # Therefore when slicing, we'll have an offset to take only the exon bases
    donor_offset = +3-1 #(+3 as those are still exon, and -1 because we have the position and want to use the cursor)
    acceptor_offset = +14-2-1 #(+14 to get to the end, -2 to keep the last 2 exon bases, and -1 for cursor not position)

    # Upcoming code assumes list elements, so check whether the donor or acceptor list is empty  
    error_message = "Please supply both lists. If you only want to splice one or the other, pass list with position higher than sequence.  Ex: [[len(seq)]]" 
    if not donor_list or not acceptor_list:
        print error_message
        sys.exit()  
                
    donor_positions_list = [x[0] for x in donor_list]  
    first_donor = min(donor_positions_list)
    last_donor = max(donor_positions_list)
    
    acceptor_positions_list = [x[0] for x in acceptor_list]  
    first_acceptor = min(acceptor_positions_list)   
    last_acceptor = max(acceptor_positions_list)
    
    # Determine our starting state (intron or exon), and update variable accordingly       
    if first_donor < first_acceptor: #if there's a donor site first, we're starting in an exon
        in_exon= True

    if first_acceptor < first_donor: #if there's an acceptor site first, we're starting in an intron
        in_intron= True

    # Continue through our sequence until we've dealt with all state transitions 
    # For each stretch of exon, we'll add those bases to our new clean_seq
    while (cursor < total_length ) and (in_exon or in_intron): 
        if in_exon: # We'll add to the clean_seq, up to the next donor splice or the seq end if there are no more
            if (DEBUG):
                print  "Cursor is: ", cursor, "and I'm in an exon"
            next_donors = [x for x in donor_positions_list if (x>cursor)]
            if next_donors:
                upcoming_donor = min(next_donors) 
                clean_seq += seq[cursor:upcoming_donor+donor_offset] 
          
                # Move the cursor up to the next intron, and update our states accordingly
                cursor = min(next_donors) 
                in_intron = True
                in_exon = False
                if (DEBUG):
                    print "clean_seq is: ", clean_seq
                    
            # if there are no more donor sites, add the rest of the seq, update state, and we're done
            else: 
                if (DEBUG):
                    print "we're ending in an exon"
                clean_seq += seq[cursor:]
                cursor += 1
                if (DEBUG):
                    print "clean_seq is: ", clean_seq
            in_exon = False 
            
        if in_intron:
            if (DEBUG):
                print "Cursor is: ", cursor, "and I'm in an intron"
            next_acceptors = [x for x in acceptor_positions_list if (x>cursor)]

            if next_acceptors:
                if (DEBUG):
                    print "next_acceptor starts at: ", min(next_acceptors) 
                    
                cursor = min(next_acceptors) + acceptor_offset 
                in_exon = True 
                in_intron = False
                if (DEBUG):
                    print "clean_seq is: ", clean_seq
                    
            # if there are no more acceptor sites, we're ending in an intron.  Update the state, and we're done
            else: 
                cursor +=1
                if (DEBUG):
                    print "clean_seq is: ", clean_seq
            in_intron = False

    return clean_seq

# Take a big long sequence (covering multiple exons/introns), and look for 
# changes in base frequencies to find a list of general change points. 
# This list will guide us in where to look for motifs. 
def find_change_points(sequence):
    seq = sequence
    seq = prepare(seq)
    length = len(seq)
    cursor = 0
    segments_list=[] # store the starting position and frequencies for each chunk
    change_points_list = [] # store the starting position where there's a significant delta from chunk to chunk
    change_threshold = .23 # threshold for significance
    chunk_size_to_check = 25.0  # chose small size in case of short exons

    # First, grab chunks of bases (based on size specified above) and save the base frequencies in each chunk
    while (cursor < length):
        this_chunk = seq[cursor:cursor+int(chunk_size_to_check)]

        this_chunk_A_freq = this_chunk.count('A')/chunk_size_to_check
        this_chunk_C_freq = this_chunk.count('C')/chunk_size_to_check
        this_chunk_G_freq = this_chunk.count('G')/chunk_size_to_check
        this_chunk_T_freq = this_chunk.count('T')/chunk_size_to_check
    
        segments_list.append([cursor+1, this_chunk_A_freq, this_chunk_C_freq, this_chunk_G_freq, this_chunk_T_freq]) #+1 for position (rather than cursor)
        cursor += int(chunk_size_to_check)
        
        
    # Next, let's see which ones had a big (quantify) change from one chunk to the next
    number_of_chunks = len(segments_list)
    counter = 0
    motif_type = ''
    while (counter < number_of_chunks-1):
        first_list = segments_list[counter]
        second_list = segments_list[counter+1]
        big_change_found = False
        
        A_delta = (first_list[1]-second_list[1])
        C_delta = (first_list[2]-second_list[2])
        G_delta = (first_list[3]-second_list[3])
        T_delta = (first_list[4]-second_list[4])

        # If any of the frequencies change a lot, save this to our change_points_list: donor or acceptor depending on the details      
        # Before-vs-after donor sites, C&G go down and T goes up
        if C_delta > change_threshold or G_delta > change_threshold or (T_delta*-.01) > change_threshold: 
            motif_type = 'donor'
            big_change_found = True
            
        # Before-vs-after acceptor sites, C&G go up and T goes down
        if T_delta > change_threshold or (C_delta *-1.0) > change_threshold or (G_delta *-1.0) > change_threshold: 
            motif_type = 'acceptor'
            big_change_found = True
            
        if big_change_found:
            change_points_list.append([first_list[0], motif_type, A_delta, C_delta, G_delta, T_delta])        
            
        counter += 1
    
    return change_points_list

# Take a sequence, and use find_change_points to identify which chunks to pass to find_motif
def put_it_all_together(sequence):
    seq = sequence
    seq = prepare(seq)
    cleaned_up_seq = ''
    winning_donor= []
    winning_acceptor=[]
    confirmed_donor_list=[]
    confirmed_acceptor_list=[]
   
    # First, we need to break it up into the rough chunks where transitions are happening 
    chunk_locations_list = find_change_points(seq)
    
    # We have our positions for where something's generally happening, so let's search a nice window (99bp) for exact motif location
    for chunk in chunk_locations_list: 
        temp_string = seq[chunk[0]-1:chunk[0]+100] # at the beginning of the slice, subtract 1 to go from position to cursor
        motif_type = chunk[1]
        
        if motif_type =='donor':
            this_string_donors= find_motif(temp_string, 'donor', chunk[0])
            winning_donor = get_winner(this_string_donors) 
            confirmed_donor_list.append(winning_donor)

        if motif_type =='acceptor':         
            this_string_acceptors = find_motif(temp_string, 'acceptor',chunk[0])
            winning_acceptor = get_winner(this_string_acceptors) 
            confirmed_acceptor_list.append(winning_acceptor)

    cleaned_up_seq = make_clean_seq (seq, confirmed_donor_list, confirmed_acceptor_list)    
    return cleaned_up_seq
        

if (DEBUG):
    print "Debug mode is turned on. "
