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


def playVoice(path: str) -> None:
    """Play the audio file

    Args:

    path (str): path to the audio file

    """
    audio = AudioSegment.from_file(path)
    play(audio)


def stopVoice():
    """Stop the audio"""
    play(AudioSegment.empty())


def deleteVoice(path: str) -> None:
    """Delete the audio file of the word

    Args:

    path (str): path to the audio file

    """
    os.remove(path)


def speak(word: str) -> None:
    """Speak the word

    Args:

    word (str): word to be spoken

    """
    getVoice(word)
    playVoice(f"voice/{word}.mp3")
