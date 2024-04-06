import os
from multiprocessing import Process, Queue

import dotenv

import src.ai as ai
import src.voice as voice

if os.path.exists(".env"):
    dotenv.load_dotenv(".env")


def api_key():
    return os.getenv("OPENAI_API_KEY")


def generate_voice(word):
    voice.getVoice(word)


def preload_word(cache):
    while cache.qsize() < 3:
        word = ai.getRandomWord()
        generate_voice(word)
        cache.put(word)


def play_word(word):
    # Function to play the word's voice
    voice.playVoice(word)


def spell_check_loop():
    if api_key() is None:
        print("API key not found")
        return

    word_cache = Queue()
    preload_process = Process(target=preload_word, args=(word_cache,))
    preload_process.start()

    run = True
    count = 0
    correct = 0

    while run:
        randomWord = word_cache.get()

        # Flag to repeat the current word
        repeat_word = True

        while repeat_word:
            # Play the pre-generated voice for the current word
            p2 = Process(target=play_word, args=(randomWord,))
            p2.start()

            guess = (
                input("Spell the word (# - quit, ? or blank to here again)\n")
                .strip()
                .lower()
            )

            if guess == "#":
                run = False
                repeat_word = False
            elif guess == "?" or guess == "":
                p2.terminate()
                continue  # Repeat the loop, hence replaying the word
            else:
                repeat_word = False  # Proceed to evaluate the guess

                if guess == randomWord.lower().strip():
                    print("Correct")
                    correct += 1
                    count += 1
                else:
                    print(f"Incorrect. The correct spelling is: {randomWord}")
                    count += 1
        print(f"Correct: {correct}/{count}")
        voice.deleteVoice(randomWord)  # Assuming this cleans up the voice file
        p2.terminate()

        if word_cache.qsize() < 3 and not preload_process.is_alive():
            preload_process = Process(target=preload_word, args=(word_cache,))
            preload_process.start()

    preload_process.terminate()  # Ensure the preload process is terminated when exiting
    preload_process.join()
    voice.clearVoice()  # Clean up any remaining voice files

    if count > 0:
        print(f"You got {correct} correct out of {count} words.")
        print(f"That is {(correct / count) * 100:.2f}%")


if __name__ == "__main__":
    voice.clearVoice()  # Clean up any previous voice files before starting
    spell_check_loop()
