import os
import sys
import shutil
import pandas as pd
from conf import Config
from gen_seq import generate_number_sequence
import parselmouth
import numpy as np
from parselmouth.praat import call
from collections import Counter

def calculate_transitional_probabilities(syll_w, lexicon):
    # Flatten the syll_w into a single list
    syll_list = [syllable for word in syll_w for syllable in word]

    # Calculate frequency counts for individual syllables and pairs of syllables
    syll_freq = Counter(syll_list)
    pair_freq = Counter((syll_list[i], syll_list[i+1]) for i in range(len(syll_list)-1))
    
    # Dictionary to store the average TPs for each word
    tp_dict = {}

    # Calculate the TP for each word in the lexicon
    for word_id, word_syllables in lexicon.items():
        tps = []
        for i in range(len(word_syllables) - 1):
            # Calculate TP for each pair of adjacent syllables
            pair = (word_syllables[i], word_syllables[i + 1])
            tp = pair_freq[pair] / syll_freq[word_syllables[i]]
            tps.append(tp)
        
        # Calculate the average TP for the word
        average_tp = sum(tps) / len(tps)
        tp_dict[word_id] = average_tp
    
    return tp_dict

def manipulate_pitch(sound, pitch_value):
    manipulation = call(sound, "To Manipulation", 0.01, 50, 600)
    pitch_tier = call(manipulation, "Extract pitch tier")
    call(pitch_tier, "Formula", str(pitch_value))
    call([pitch_tier, manipulation], "Replace pitch tier")
    resynthesized_sound = call(manipulation, "Get resynthesis (overlap-add)")
    return resynthesized_sound

def process_word(word, mu_w, cfg):
    syllables_sounds = []
    pitch_values = []
    for syllable in word:
        pitch_value = np.random.normal(mu_w, cfg.sd_w)  # Sample pitch for the syllable
        pitch_values.append(pitch_value)
        wav_path = os.path.join("sound", f"{syllable}.wav")
        
        # Load the syllable sound
        sound = parselmouth.Sound(wav_path)
        
        # Manipulate the pitch
        resynthesized_sound = manipulate_pitch(sound, pitch_value)
        
        # Append the resynthesized sound
        syllables_sounds.append(resynthesized_sound)
    
    return syllables_sounds, pitch_values

def make_words_partword_sounfiles(lexicon, pitch_value, output_path):
    for w in lexicon:
        sylls = lexicon[w]
        sounds = []
        for s in sylls:
            wav_path = os.path.join("sound", f"{s}.wav")
            sound = parselmouth.Sound(wav_path)
            resynthesized_sound = manipulate_pitch(sound, pitch_value)
            sounds.append(resynthesized_sound)
        concatenated_sound = concatenate_sounds(sounds)
        sound_output_path = os.path.join(output_path, f"{w}.wav")
        concatenated_sound.save(sound_output_path, "WAV")
        
def concatenate_sounds(sounds):
    concatenated_sound = sounds[0]
    for sound in sounds[1:]:
        concatenated_sound = parselmouth.Sound.concatenate([concatenated_sound, sound])
    return concatenated_sound

def apply_fade_effects(sound, fade_in_dur, fade_out_dur, alpha):
    total_dur = sound.get_total_duration()
    sampling_rate = sound.sampling_frequency
    
    # Apply fade-in
    if fade_in_dur > 0:
        fade_in_samples = int(fade_in_dur * sampling_rate)
        fade_in = np.linspace(0.0, 1.0, fade_in_samples) * alpha
        fade_in = np.exp(fade_in) / np.max(np.exp(fade_in))
        # sound.xs()[0:int(fade_in_dur * sound.sampling_frequency)] *= fade_in
        sound.values[:, :fade_in_samples] *= fade_in
    
    # Apply fade-out
    if fade_out_dur > 0:
        fade_out_samples = int(fade_out_dur * sampling_rate)
        fade_out = np.linspace(1.0, 0.0, fade_out_samples) * alpha
        fade_out = np.exp(fade_out) / np.max(np.exp(fade_out))
        # sound.xs()[-int(fade_out_dur * sound.sampling_frequency):] *= fade_out
        sound.values[:, -fade_out_samples:] *= fade_out
    
    return sound

def generate_speech_stream(syll_w, cfg):
    all_syllables = []
    all_pitch_values = []
    for word in syll_w:
        mu_w = np.random.normal(cfg.mu, cfg.sd)  # Sample pitch for the word
        syllables_sounds, pitch_values = process_word(word, mu_w, cfg)
        all_syllables.extend(syllables_sounds)
        all_pitch_values.extend(pitch_values)
    
    # Concatenate all syllables into a long speech stream
    speech_stream = concatenate_sounds(all_syllables)
    
    # Apply fade-in and fade-out effects
    speech_stream = apply_fade_effects(speech_stream, cfg.fade_in_dur, cfg.fade_out_dur, cfg.alpha)
    
    return speech_stream, all_pitch_values

def make_al(output_dir):
    cfg = Config()
    
    # Create output directories
    os.makedirs(output_dir, exist_ok=True)
    speech_stream_dir = os.path.join(output_dir, "speech_streams")
    os.makedirs(speech_stream_dir, exist_ok=True)
    stats_dir = os.path.join(output_dir, "stats")
    os.makedirs(stats_dir, exist_ok=True)
    
    # Save the config.py file to the output directory
    shutil.copy("conf.py", os.path.join(output_dir, "config.py"))
    
    # Load all stream txt files
    streams_dir = "streams"
    stream_files = [f for f in os.listdir(streams_dir) if f.endswith(".txt")]
    
    al_tp_data = []
    partwords_tp_data = []
    pitch_history = []
    
    print("Generating speech streams...")
    for i, stream_file in enumerate(stream_files):
        
        # Step 1: Read in the number list
        with open(os.path.join(streams_dir, stream_file), 'r') as f:
            sequence = list(map(int, f.read().strip().split()))
        syll_w = [cfg.al_lexicon[number] for number in sequence]
        
        # Step 2: Compute TPs for al_lexicon and partwords
        al_tp = calculate_transitional_probabilities(syll_w, cfg.al_lexicon)
        partwords_tp = calculate_transitional_probabilities(syll_w, cfg.partwords)
        
        al_tp_data.append(al_tp)
        partwords_tp_data.append(partwords_tp)
        
        # Step 3: Generate the audio and save it
        speech_stream, all_pitch_values = generate_speech_stream(syll_w, cfg)
        stream_output_path = os.path.join(speech_stream_dir, f"stream_{i + 1}.wav")
        speech_stream.save(stream_output_path, "WAV")
        
        # Save pitch values
        pitch_history.append(f"stream_{i + 1}.wav\n" + ", ".join(map(str, all_pitch_values)))
    
    print
    # Step 4: Save TP statistics and pitch history
    print("Saving transitional probability statistics...")
    al_tp_df = pd.DataFrame(al_tp_data, index=[f"stream_{i + 1}.txt" for i in range(len(stream_files))])
    partwords_tp_df = pd.DataFrame(partwords_tp_data, index=[f"stream_{i + 1}.txt" for i in range(len(stream_files))])
    
    al_tp_df.to_excel(os.path.join(stats_dir, "al_lexicon_tps.xlsx"))
    partwords_tp_df.to_excel(os.path.join(stats_dir, "partwords_tps.xlsx"))
    
    with open(os.path.join(stats_dir, "pitch_history.txt"), 'w') as f:
        f.write("\n\n".join(pitch_history))
        
    # Step 5: Make the soundfiles of the AL word and partword stimuli. Set the pitch value to mu.
    print("Marking the sounds files for the AL words and partwords...")
    al_word_path = os.path.join(output_dir, 'al_words')
    os.makedirs(al_word_path, exist_ok=True)
    make_words_partword_sounfiles(cfg.al_lexicon, cfg.mu, al_word_path)
    
    partword_path = os.path.join(output_dir, 'partwords')
    os.makedirs(partword_path, exist_ok=True)
    make_words_partword_sounfiles(cfg.partwords, cfg.mu, partword_path)

    print(f"All processing complete. Outputs saved in the {output_dir} directory.")


if __name__ == "__main__":
    output_dir = sys.argv[1] if len(sys.argv) > 1 else "output"
    make_al(output_dir)