import random
import os
from conf import Config

def generate_number_sequence(n_words = 6, rep = 25):
    numbers = list(range(1, n_words + 1)) * rep  # Each number appears rep times
    random.shuffle(numbers)
    
    # Ensure that no number occurs consecutively
    for i in range(1, len(numbers)):
        if numbers[i] == numbers[i-1]:
            # Find the first non-equal number and swap
            for j in range(i+1, len(numbers)):
                if numbers[j] != numbers[i]:
                    numbers[i], numbers[j] = numbers[j], numbers[i]
                    break
    
    # If after the loop there are still consecutive numbers, shuffle again
    while any(numbers[i] == numbers[i+1] for i in range(len(numbers) - 1)):
        random.shuffle(numbers)
        for i in range(1, len(numbers)):
            if numbers[i] == numbers[i-1]:
                for j in range(i+1, len(numbers)):
                    if numbers[j] != numbers[i]:
                        numbers[i], numbers[j] = numbers[j], numbers[i]
                        break

    return numbers

def save_sequences(n_streams = 6, n_words = 6, rep = 25, rnd_seed = None):
    if rnd_seed is not None:
        random.seed(rnd_seed)  # Set seed once before generating all sequences
    
    streams_dir = os.path.join("streams")
    os.makedirs(streams_dir, exist_ok=True)
    
    for i in range(n_streams):
        sequence = generate_number_sequence(n_words, rep)
        sequence_str = " ".join(map(str, sequence))
        file_path = os.path.join(streams_dir, f"stream_{i + 1}.txt")
        with open(file_path, 'w') as f:
            f.write(sequence_str)
        print(f"Stream {i + 1} saved to {file_path}")


if __name__ == "__main__":
    cfg = Config()
    save_sequences(cfg.n_streams, len(cfg.al_lexicon.keys()), cfg.n_reps, cfg.rnd_seed)