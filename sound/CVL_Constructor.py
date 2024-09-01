# CVL_Constructor.py
# For constructing speech streams of an artificial language used to study
# the effects of onset/vowel lengthening on speech segmentation 

from ALTool import *

class CVL_AL(AL):
    def __init__(self, sequence, word_dict, partwords):
        super().__init__(sequence, word_dict)
        self.partwords = partwords
        self.original = self.sequence[:]

    def set_leng_condition(self, onset_leng = [True, False, False],
                           vowel_leng = [False, False, False]):
        """ Modify the AL sequence such that onsets or vowels are lengthened
        according to the conditioh. The first argument specifies which 
        syllable in the (trisyllabic) AL words received onset lengthening; 
        the second argument specifies wihch syllable receives vowel lengthening. 
        For example, the default setting onset_leng = {True, False, False}
        represents initial onset lengthening. """

        new_seq = []
        tri_syll_string = []
        index, start = 0, 0
        for syll in self.original[:]:
            tri_syll_string.append(syll)
            if len(tri_syll_string) >= 3:
                tri_syll_string = self.__process_leng_marking(tri_syll_string,
                                                              onset_leng,
                                                              vowel_leng)
                new_seq.extend(tri_syll_string)
                tri_syll_string = []
                
        # Replace the AL sequence with one modified to the specified 
        # lengthening condition.
        self.sequence = new_seq
  
    def set_to_TP_only(self):
        self.sequence = self.original[:]

    def __process_leng_marking(self, sequence, onset_leng, vowel_leng):
        new_sequence = sequence[:]
        
        for index, leng in enumerate(onset_leng):
            if leng: new_sequence[index] = new_sequence[index] + "_OL"
        
        for index, leng in enumerate(vowel_leng):
            if leng: new_sequence[index] = new_sequence[index] + "_VL"

        return new_sequence

    def __count(self, sequence, string):
        count = 0
        for i in sequence:
            if string in i:
                count += 1
        return count
            
word_dict = {"1" : ["ba", "nu", "me"],
             "2" : ["ne", "bo", "gi"],
             "3" : ["ge", "ni", "go"],
             "4" : ["mi", "ma", "bu"],
             "5" : ["no", "ga", "mu"],
             "6" : ["bi", "mo", "na"]}

partwords = [["ma", "bu", "ge"],
             ["bo", "gi", "no"],
             ["ni", "go", "mi"],
             ["gi", "ba", "nu"],
             ["na", "ne", "bo"],
             ["me", "bi", "mo"]]

# Function for generate the 6 speech streams for each condition
def generate_all_streams(n, onset_leng_pattern, vowel_leng_pattern):
    for i in range(1, n+1):
        sequence_infile = open('stream_{}.txt'.format(i), 'r')
        sequence = sequence_infile.readline().split()
        
        AL = CVL_AL(sequence, word_dict, partwords)
        
        AL.set_leng_condition(onset_leng = onset_leng_pattern,
                              vowel_leng = vowel_leng_pattern)
        AL.generate_sound(filename = 'Stream_{}'.format(i))
    print("Done!")

# TP-only (No lengthening)
generate_all_streams(6, onset_leng_pattern = [False, False, False],
                      vowel_leng_pattern = [False, False, False])

# Initial onset lengthening
generate_all_streams(6, onset_leng_pattern = [True, False, False],
                      vowel_leng_pattern = [False, False, False])

# Final onset lengthening
generate_all_streams(6, onset_leng_pattern = [False, False, True],
                      vowel_leng_pattern = [False, False, False])

# Initial vowel lengthening
generate_all_streams(6, onset_leng_pattern = [False, False, False],
                      vowel_leng_pattern = [True, False, False])

# Final vowel lengthening
generate_all_streams(6, onset_leng_pattern = [False, False, False],
                      vowel_leng_pattern = [False, False, True])

# IO+FV lengthening
generate_all_streams(6, onset_leng_pattern = [True, False, False],
                      vowel_leng_pattern = [False, False, True])


# Generate the sounds files for the words
def get_words(words = word_dict):
    for word in words:
        concatenated = AudioSegment.empty()
        for syllable in words[word]:
            concatenated += AudioSegment.from_wav(str(syllable) + ".wav")
        concatenated.export(str(word) + ".wav", format="wav")
    print("Done!")
get_words()


# Generate the sounds files for the partwords
def get_partwords(partwords = partwords):
    for index, partword in enumerate(partwords):
        concatenated = AudioSegment.empty()
        for syllable in partword:
            concatenated += AudioSegment.from_wav(str(syllable) + ".wav")
        concatenated.export(str(index+1) + ".wav", format="wav")
    print("Done!")
get_partwords()


