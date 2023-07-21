import json
import os
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())


class Settings:
    """
    A classe Settings é responsável por carregar configurações a partir de um arquivo JSON.
    """

    def __init__(self, filename):
        self.filename = filename
        self.values = self.load_settings()
        self.values["ELEVEN_LABS_API_KEY"] = os.environ["ELEVEN_LABS_API_KEY"]

    def load_settings(self):
        with open(self.filename, 'r') as f:
            return json.load(f)

    def get_voice_id(self, name):
        for voice in self.values.get("voices"):
            if voice.get("name") == name:
                return voice.get("voice_id")
        raise Exception("Voice not found.")
