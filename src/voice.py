import os
import warnings
from pathlib import Path

from openai import OpenAI
from pydub import AudioSegment
from pydub.playback import play

warnings.filterwarnings("ignore", category=DeprecationWarning)

client = OpenAI()


def generateSentence(word: str) -> str:
    """Generate a sentence using the word

    Args:

    word (str): word to be used in a sentence

    Returns:

    str: sentence using the word

    """
    from openai import OpenAI

    client = OpenAI()

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": f"Make a sentance using the word {word} to give context to what {word} means.",
            },
        ],
    )
    return completion.choices[0].message.content


def getVoice(word: str) -> str:
    """Get adio file of the word being used in a sentence

    Args:

    word (str): word to be used in a sentence

    Returns:

    str: path to the audio file

    """
    speech_file_path = f"voice/{word}.mp3"
    response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=f'spell "{word}" as in "{generateSentence(word)} {word}',
    )

    response.stream_to_file(speech_file_path)


def playVoice(word: str) -> None:
    """Play the audio file

    Args:

    word (str): word to be played
    """
    audio = AudioSegment.from_file(f"voice/{word}.mp3")
    play(audio)


def deleteVoice(word: str) -> None:
    """Delete the audio file of the word

    Args:

    word (str): word to be deleted

    """
    os.remove(f"voice/{word}.mp3")


def speak(word: str) -> None:
    """Speak the word

    Args:

    word (str): word to be spoken

    """
    getVoice(word)
    playVoice(f"voice/{word}.mp3")


def clearVoice() -> None:
    """Clear all the audio files in the voice directory"""
    for file in Path("voice").glob("*.mp3"):
        os.remove(file)
