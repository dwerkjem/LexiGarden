import multiprocessing as mp
import os

import dotenv

import src.ai as ai
import src.voice as voice

if os.path.exists(".env"):
    dotenv.load_dotenv(".env")


def api_key():
    try:
        # Try to get the API key from the environment variables first.
        return os.getenv("OPENAI_API_KEY")
    except KeyError:
        # If the key is not found, return None.
        return None


def spell_check_loop():
    if api_key() is None:
        print("API key not found")
        return
    run = True
    count = 0
    correct = 0

    while run:
        randomWord = ai.getRandomWord()
        p1 = mp.Process(target=voice.speak, args=(randomWord,))
        p1.start()

        guess = input("Spell the word: ").strip().lower()

        if guess == "#":
            run = False

        # Assuming randomWord is also processed to be lowercase and stripped.
        elif guess == randomWord.lower().strip():
            print("Correct")
            correct += 1
        else:
            print("Incorrect")
            print("The correct spelling is:", randomWord)
            print(" ")
        print("tpye ! for stats and # to exit")
        print(" ")
        p1.terminate()
        count += 1
        print("you are on word", count)
    print("You got", correct, "correct out of", count, "words")
    print(" ")
    print("That is", (correct / count) * 100, "%")


if __name__ == "__main__":
    spell_check_loop()
