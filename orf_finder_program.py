# orfFinder_program.py   Adapted from orfFinder.py, for demo without fasta file
#
# Open Reading Frame Finder (ORF Finder)
# This program reads in a FASTA file and prints the ORF information for all 6 reading frames
# Diane Kaplan        February 2015
#
# Context: In a genetic sequence, the open reading frame is the part 
# that can be transcribed, bookended by a start codon (ATG) and stop codon (TAA, 
# TAG, TGA). A given sequence has 6 possible reading frames: starting our codons 
# from position 1, 2, or 3, and reading forward or the reverse complement. This
# program will find the possible ORFs for all 6 reading frames. 
# 
# Usage:
#     % python orfFinder.py <filename> [<minimal ORF length>]
#
# Assumptions & Limitations: This program doesn't include overlapping ORFs
# I print from inside the print_ORFs function
#
# Citations: I use Jeff Parker's cs58FileUtil.py for file reading & cleanup

import string
import sys
from cs58FileUtil import prepare
import profile

# How many base pairs long must an ORF be? Override default with a Command Line Parameter
limit = 300  

# How many bp to print for each (assumed to be less than limit, otherwise we'll go out of bounds)
snippet_length= 45 

DEBUG = False

# Take a sequence and return its reverse complement 
def reverseComplement(sequence):
    seq = sequence
    seq_backward = seq[::-1] 
    base_partners = {"A":"T", "C":"G", "G":"C", "T":"A"} 
    seq_converted = ""  
    
    # Loop through and look up the complement to create the new sequence
    for char in seq_backward: 
        seq_converted += base_partners[char]

    return seq_converted
    
# For the given sequence and offset, find the Open Reading Frames 
def find_ORFs (text, offset):
    seq_length = len(text)
    start_codons=['ATG']
    stop_codons=['TAA', 'TAG', 'TGA']
    this_frame_ORFs = {} # we'll save pairs: start and stop position for each ORF
    
    cursor = offset  # use offset to use correct reading frame
    number_of_codons = (seq_length-offset)/3  # Even division, to ignore extra bases on the end
    codon_cursor = 0
    in_ORF = False
    
    while codon_cursor < number_of_codons:
        this_codon = text[cursor:cursor+3]
        if in_ORF == False: # We're not in an ORF yet, so look for start codon
            if this_codon in start_codons:
                
                # add one to give position number (starts at 1, not 0) 
                this_start =cursor + 1 
                
                # initialize stop as 0: if it's not replaced, ORF spans past our sequence
                this_frame_ORFs[this_start] = 0   
                
                in_ORF = True
                
        if in_ORF: #We're in an ORF, so next we look for stop codon
            if this_codon in stop_codons:
                
                # save the stop position for the current ORF
                this_frame_ORFs[this_start] = cursor + 3
                
                in_ORF = False

        codon_cursor +=1    
        cursor += 3
    return this_frame_ORFs    

# Print the results for a specific reading frame
def print_ORFs(frame, ORF_dict, min_ORF_length, sequence):
    
    # Get our orientation from the reading frame: negative value for antisense 
    # strand (offsets from the end), otherwise forward (offset from beginning)
    is_antisense= False 
    if frame[0] == '-': 
        is_antisense= True
        seq_length= len(sequence) 
        
    count = len(ORF_dict)
    if count ==0: 
        print "There were no ORFs in this sequence."
    else: 
        for ORF in ORF_dict: 
            # we want the length in bases, so just like slicing we need to go one past the end
            length = ORF_dict[ORF] + 1 - ORF 
            
            if length >= min_ORF_length:
                if is_antisense: 
                    print frame, "Start", seq_length-ORF_dict[ORF]+1, "End", seq_length-ORF+1,"Len" ,length, "Seq", sequence[ORF-1:ORF-1 + snippet_length] 
                else: 
                    print frame, "Start", ORF, "End", ORF_dict[ORF],"Len" ,length, "Seq", sequence[ORF-1:ORF-1 + snippet_length] 
                
            if (DEBUG):
                if length > 0:
                    print "(An ORF below size limit starts at position",ORF, "and ends at", ORF_dict[ORF],": length:" ,length , "bases)."
                else: 
                    print "(There was also a start codon at position", ORF, "without a stop codon before the end of this sequence, we may want to look further out)."          
    return True
                    
def process_all_reading_frames(text, min_ORF_length):  
    seq = prepare(text)    # clean up sequence
    antisense = reverseComplement(seq) # get the reverse complement 

    # Get results for each reading frame, with appropriate offset for cursor) 
    frame_1_ORFs= find_ORFs(seq, 0) 
    frame_2_ORFs= find_ORFs(seq, 1) 
    frame_3_ORFs= find_ORFs(seq, 2) 
    
    frame_a1_ORFs= find_ORFs(antisense, 0) 
    frame_a2_ORFs= find_ORFs(antisense, 1) 
    frame_a3_ORFs= find_ORFs(antisense, 2) 
    
    # Then print the results
    print_ORFs('+1', frame_1_ORFs, min_ORF_length, seq)
    print_ORFs('+2', frame_2_ORFs, min_ORF_length, seq)   
    print_ORFs('+3', frame_3_ORFs, min_ORF_length, seq)
    
    print_ORFs('-1', frame_a1_ORFs, min_ORF_length, antisense)
    print_ORFs('-2', frame_a2_ORFs, min_ORF_length, antisense)   
    print_ORFs('-3', frame_a3_ORFs, min_ORF_length, antisense)

    return True


#if ((len(sys.argv) < 2) or (len(sys.argv) > 3)):
#    print "Usage: python", sys.argv[0], "<filename> [<min ORF length>]"
#else:
#    fileName = sys.argv[1]
#    if (len(sys.argv) > 2):             # This should be an integer
#        try:
#            limit = int(sys.argv[2])    # Convert string to integer
#        except ValueError:              # try-except catches errors
#            print "\n\tExpecting an integer to define min ORF length, found",
#            print sys.argv[2]
#            exit()
#   
#   print "ORF must be at least", limit, "Base pairs long"
    

# Find ORFs for our sequence
#sequence = cs58FileUtil.readFastaFile(fileName)
sequence= 'GAATTCCGGATGAGCATTCATCAGGCGGGCAAGAATGTGAATAAAGGCCGGATAAAACTTGTGCTTATTTTTCTTTACGGTCTTTAAAAAGGCCGTAATATCCAGCTGAACGGTCTGGTTATAGGTACATTGAGCAACTGACTGAAATGCCTCAAAATGTTCTTTACGATGCCATTGGGATATATCAACGGTGGTATATCCAGTGATTTTTTTCTCCATTTTAGCTTCCTTAGCTCCTGAAAATCTCGATAACTCAAAAAATACGCCCGGTAGTGATCTTATTTCATTATGGTGAAAGTTGGAACCTCTTACGTGCCGATCAACGTCTCATTTTCGCCAAAAGTTGGCCCAGGGCTTCCCGGTATCAACAGGGACACCAGGATTTATTTATTCTGCGAAGTGATCTTCCGTCACAGGTATTTATTCGGCGCAAAGTGCGTCGGGTGATGCTGCCAACTTACTGATTTAGTGTATGATGGTGTTTTTGAGGTGCTCCAGTGGCTTCTGTTTCTATCAGCTGTCCCTCCTGTTCAGCTACTGACGGGGTGGTGCGTAACGGCAAAAGCACCGCCGGACATCAGCGCTAGCGGAGTGTATACTGGCTTACTATGTTGGCACTGATGAGGGTGTCAGTGAAGTGCTTCATGTGGCAGGAGAAAAAAGGCTGCACCGGTGCGTCAGCAGAATATGTGATACAGGATATATTCCGCTTCCTCGCTCACTGACTCGCTACGCTCGGTCGTTCGACTGCGGCGAGCGGAAATGGCTTACGAACGGGGCGGAGATTTCCTGGAAGATGCCAGGAAGATACTTAACAGGGAAGTGAGAGGGCCGCGGCAAAGCCGTTTTTCCATAGGCTCCGCCCCCCTGACAAGCATCACGAAATCTGACGCTCAAATCAGTGGTGGCGAAACCCGACAGGACTATAAAGATACCAGGCGTTTCCCCCTGGCGGCTCCCTCGTGCGCTCTCCTGTTCCTGCCTTTCGGTTTACCGGTGTCATTCCGCTGTTATGGCCGCGTTTGTCTCATTCCACGCCTGACACTCAGTTCCGGGTAGGCAGTTCGCTCCAAGCTGGACTGTATGCACGAACCCCCCGTTCAGTCCGACCGCTGCGCCTTATCCGGTAACTATCGTCTTGAGTCCAACCCGGAAAGACATGCAAAAGCACCACTGGCAGCAGCCACTGGTAATTGATTTAGAGGAGTTAGTCTTGAAGTCATGCGCCGGTTAAGGCTAAACTGAAAGGACAAGTTTTGGTGACTGCGCTCCTCCAAGCCAGTTACCTCGGTTCAAAGAGTTGGTAGCTCAGAGAACCTTCGAAAAACCGCCCTGCAAGGCGGTTTTTTCGTTTTCAGAGCAAGAGATTACGCGCAGACCAAAACGATCTCAAGAAGATCATCTTATTAATCAGATAAAATATTTCTAGATTTCAGTGCAATTTATCTCTTCAAATGTAGCACCTGAAGTCAGCCCCATACGATATAAGTTGTAATTCTCATGTTTGACAGCTTATCATCGATAAGCTTTAATGCGGTAGTTTATCACAGTTAAATTGCTAACGCAGTCAGGCACCGTGTATGAAATCTAACAATGCGCTCATCGTCATCCTCGGCACCGTCACCCTGGATGCTGTAGGCATAGGCTTGGTTATGCCGGTACTGCCGGGCCTCTTGCGGGATATCGTCCATTCCGACAGCATCGCCAGTCACTATGGCGTGCTGCTAGCGCTATATGCGTTGATGCAATTTCTATGCGCACCCGTTCTCGGAGCACTGTCCGACCGCTTTGGCCGCCGCCCAGTCCTGCTCGCTTCGCTACTTGGAGCCACTATCGACTACGCGATCATGGCGACCACACCCGTCCTGTGGATCCTCTACGCCGGACGCATCGTGGCCGGCATCACCGGCGCCACAGGTGCGGTTGCTGGCGCCTATATCGCCGACATCACCGATGGGGAAGATCGGGCTCGCCACTTCGGGCTCATGAGCGCTTGTTTCGGCGTGGGTATGGTGGCAGGCCCCGTGGCCGGGGGACTGTTGGGCGCCATCTCCTTGCATGCACCATTCCTTGCGGCGGCGGTGCTCAACGGCCTCAACCTACTACTGGGCTGCTTCCTAATGCAGGAGTCGCATAAGGGAGAGCGTCGACCGATGCCCTTGAGAGCCTTCAACCCAGTCAGCTCCTTCCGGTGGGCGCGGGGCATGACTATCGTCGCCGCACTTATGACTGTCTTCTTTATCATGCAACTCGTAGGACAGGTGCCGGCAGCGCTCTGGGTCATTTTCGGCGAGGACCGCTTTCGCTGGAGCGCGACGATGATCGGCCTGTCGCTTGCGGTATTCGGAATCTTGCACGCCCTCGCTCAAGCCTTCGTCACTGGTCCCGCCACCAAACGTTTCGGCGAGAAGCAGGCCATTATCGCCGGCATGGCGGCCGACGCGCTGGGCTACGTCTTGCTGGCGTTCGCGACGCGAGGCTGGATGGCCTTCCCCATTATGATTCTTCTCGCTTCCGGCGGCATCGGGATGCCCGCGTTGCAGGCCATGCTGTCCAGGCAGGTAGATGACGACCATCAGGGACAGCTTCAAGGATCGCTCGCGGCTCTTACCAGCCTAACTTCGATCACTGGACCGCTGATCGTCACGGCGATTTATGCCGCCTCGGCGAGCACATGGAACGGGTTGGCATGGATTGTAGGCGCCGCCCTATACCTTGTCTGCCTCCCCGCGTTGCGTCGCGGTGCATGGAGCCGGGCCACCTCGACCTGAATGGAAGCCGGCGGCACCTCGCTAACGGATTCACCACTCCAAGAATTGGAGCCAATCAATTCTTGCGGAGAACTGTGAATGCGCAAACCAACCCTTGGCAGAACATATCCATCGCGTCCGCCATCTCCAGCAGCCGCACGCGGCGCATCTCGGGCAGCGTTGGGTCCTGGCCACGGGTGCGCATGATCGTGCTCCTGTCGTTGAGGACCCGGCTAGGCTGGCGGGGTTGCCTTACTGGTTAGCAGAATGAATCACCGATACGCGAGCGAACGTGAAGCGACTGCTGCTGCAAAACGTCTGCGACCTGAGCAACAACATGAATGGTCTTCGGTTTCCGTGTTTCGTAAAGTCTGGAAACGCGGAAGTCCCCTACGTGCTGCTGAAGTTGCCCGCAACAGAGAGTGGAACCAACCGGTGATACCACGATACTATGACTGAGAGTCAACGCCATGAGCGGCCTCATTTCTTATTCTGAGTTACAACAGTCCGCACCGCTGTCCGGTAGCTCCTTCCGGTGGGCGCGGGGCATGACTATCGTCGCCGCACTTATGACTGTCTTCTTTATCATGCAACTCGTAGGACAGGTGCCGGCAGCGCCCAACAGTCCCCCGGCCACGGGGCCTGCCACCATACCCACGCCGAAACAAGCGCCCTGCACCATTATGTTCCGGATCTGCATCGCAGGATGCTGCTGGCTACCCTGTGGAACACCTACATCTGTATTAACGAAGCGCTAACCGTTTTTATCAGGCTCTGGGAGGCAGAATAAATGATCATATCGTCAATTATTACCTCCACGGGGAGAGCCTGAGCAAACTGGCCTCAGGCATTTGAGAAGCACACGGTCACACTGCTTCCGGTAGTCAATAAACCGGTAAACCAGCAATAGACATAAGCGGCTATTTAACGACCCTGCCCTGAACCGACGACCGGGTCGAATTTGCTTTCGAATTTCTGCCATTCATCCGCTTATTATCACTTATTCAGGCGTAGCACCAGGCGTTTAAGGGCACCAATAACTGCCTTAAAAAAATTACGCCCCGCCCTGCCACTCATCGCAGTACTGTTGTAATTCATTAAGCATTCTGCCGACATGGAAGCCATCACAGACGGCATGATGAACCTGAATCGCCAGCGGCATCAGCACCTTGTCGCCTTGCGTATAATATTTGCCCATGGTGAAAACGGGGGCGAAGAAGTTGTCCATATTGGCCACGTTTAAATCAAAACTGGTGAAACTCACCCAGGGATTGGCTGAGACGAAAAACATATTCTCAATAAACCCTTTAGGGAAATAGGCCAGGTTTTCACCGTAACACGCCACATCTTGCGAATATATGTGTAGAAACTGCCGGAAATCGTCGTGGTATTCACTCCAGAGCGATGAAAACGTTTCAGTTTGCTCATGGAAAACGGTGTAACAAGGGTGAACACTATCCCATATCACCAGCTCACCGTCTTTCATTGCCATACG'

process_all_reading_frames(sequence,limit)
profile.run("process_all_reading_frames(sequence,limit)")