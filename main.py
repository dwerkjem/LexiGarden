import os

import dotenv
import openai

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


if api_key() is not None:

    print("API Key found see README.md for more information")

openai.api_key = api_key()
