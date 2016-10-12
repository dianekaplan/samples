package rosalind;
import java.util.List;

/**
 * Created by Diane Kaplan on 10/9/2016.

 Rosalind problem lcsm: Find the longest common shared motif among a list of fasta sequences
 http://rosalind.info/problems/lcsm/
 */

public class lcsm {

    public static void main(String[] args) {

        // Use fasta_utils to extract list of sequences from fasta file
        String file_to_use = "C:\\Users\\Diane\\Documents\\GitHub\\playtime\\JavaPlaytime\\src\\src\\rosalind\\dna.txt";
        List<String> seq_list = rosalind.fasta_utils.get_seq_strings(file_to_use);

        System.out.println("Longest common substring is: " + find_longest_substring(seq_list));
    }

    // Go through a list of sequences and return the longest common substring
    private static String find_longest_substring(List<String> list) {

        boolean DEBUG = false;

        int sequence_count = list.size();
        if (DEBUG) {System.out.println("Our list has: " + sequence_count + " strings:" + list);}

        String winning_substring = "";
        boolean found_the_answer = false;

        // Use shortest sequence in the bunch to identify substrings
        String shortest_seq = find_shortest_seq(list);
        int size_of_shortest_seq = shortest_seq.length();

        // We'll try one size at a time, from 2bp up to length of the shortest seq (best case scenario)
        // When you find a common string of one size, save and go to the next size up
        // Return the longest one that's found in all of the sequences

        // Try one size at a time
        for (int i = 2; (i < size_of_shortest_seq) && !found_the_answer; i++) {

            // Go base by base to find a snippet of this size, until we find one contained in all sequences
            for (int j = 0; j < (size_of_shortest_seq - i); j++) {
                String temp_snippet = shortest_seq.substring(j, j + i);

                // For this snippet, test whether it is found in all the other strings
                // If so, save it as our winner, break, and go to the next size
                // Also reset j to 0 so we start at the beginning of the string
                if (check_all_strings (temp_snippet, list )) {
                    winning_substring = temp_snippet;
                    if (DEBUG) {System.out.println(temp_snippet + " is a winner");}
                    i++;
                    j = 0;
                }
                // If we reach the end of the first string without a winner for that length,
                // we won't improve and our saved choice is the best
                found_the_answer = true;
            }
        }
        return winning_substring;
    }

    // Check to see whether a snippet is contained in all the strings of a list
    private static boolean check_all_strings(String snippet, List<String> list) {

        int sequence_count = list.size();
        boolean is_found_everywhere = true;

        for (int i = 1; (i < sequence_count) && is_found_everywhere; i++) {

            String this_seq = list.get(i);
            int found_at = this_seq.lastIndexOf(snippet);

            // if it's missing from any of the strings, stop the search
            if (found_at < 0) {
                is_found_everywhere = false;
                break;
            }
        }
        return is_found_everywhere;
    }


    // In a list of sequences, return the shortest one
    private static String find_shortest_seq(List<String> list) {

        // initialize to the first string and compare/replace from there
        String shortest_seq = list.get(0);
        int shortest_seq_len = shortest_seq.length();

        for (String str : list) {
            if (str.length() < shortest_seq_len) {
                shortest_seq_len = str.length();
            }
        }
        return shortest_seq;
    }

}