import os

import dotenv
import openai

import src.ai as ai
import src.randomWord as rw

if os.path.exists(".env"):
    dotenv.load_dotenv(".env")


def api_key():
    if dotenv.get_key(".env", "OPENAI_API_KEY") is not None:
        return dotenv.get_key(".env", "OPENAI_API_KEY")
    else:
        try:
            return os.environ["OPENAI_API_KEY"]
        except KeyError:
            return None


def getSentance(word):
    openai.api_key = api_key()
    client = openai.Client()
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": f"You make a sentance using the word '{word}' asuming it is not a name.",
            },
        ],
    )
    return response.choices[0].message.content


if api_key() is not None:
   
else:
    print("API key not found")
