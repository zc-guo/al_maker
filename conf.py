class Config:
    def __init__(self):
        
        # Articial language (AL) lexicon settings
        # (Normally you don't need to change any of these.)
        self.n_reps = 25    # No. repetitions of each word in each stream
        self.n_streams = 6  # No. AL streams needed
        self.al_lexicon = {
            1: ["ba", "nu", "me"],
            2: ["ne", "bo", "gi"],
            3: ["ge", "ni", "go"],
            4: ["mi", "ma", "bu"],
            5: ["no", "ga", "mu"],
            6: ["bi", "mo", "na"]
        }
        self.partwords = {
            1: ["ma", "bu", "ge"],
            2: ["bo", "gi", "no"],
            3: ["ni", "go", "mi"],
            4: ["gi", "ba", "nu"],
            5: ["na", "ne", "bo"],
            6: ["me", "bi", "mo"]
        }

        # Pitch value settings
        # These settings control the pitch values of the AL words and their component syllables.
        # For each AL word instance, sample a pitch value mu_w from a normal distribution with mean of 
        # self.mu and standard deviation of self.sd. Then, for the syllables inside this word, 
        # sample pitch values from a normal distribution with mean of mu_w and standard deviation of 
        # self.sd_w.
        self.mu = 130  # Mean pitch for all AL words (Hz)
        self.sd = 15   # Standard deviation for word pitch
        self.sd_w = 5  # Standard deviation for syllable pitch within a word

        # Audio fade-in/out settings
        self.fade_in_dur = 5   # in seconds
        self.fade_out_dur = 5  # in seconds
        self.alpha = 6         # Higher values give more abrupt fdae-in/fade-out effect
        
        self.rnd_seed = 2024