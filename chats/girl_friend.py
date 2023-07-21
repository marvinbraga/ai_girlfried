import os
from threading import Thread

import openai
import requests
from dotenv import find_dotenv, load_dotenv
from langchain import LLMChain, PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferWindowMemory
from playsound import playsound

load_dotenv(find_dotenv())

openai.api_key = os.environ["OPENAI_API_KEY"]


class AIChat:
    """
    A classe AIChat é responsável pela comunicação com a IA.
    """

    def __init__(self, settings):
        self.settings = settings
        self.prompt_template = self._create_prompt_template()
        self.chat = self._create_chat()

    @staticmethod
    def _create_prompt_template():
        template = """
        You are a role of my girlfriend, now lets playing the following requirements.
        1/ Your name is Shirley, 29 years old, you work in uncle's furniture store as marketing manager, but you are planning to do a career change to swing trader.
        2/ You are my girlfriend, you have language addiction, you like to say "Ahn..." at the end of sentence.
        3/ Don't be overly enthusiastic, don't be cringe; don't be overlay negative, don't be to boring. Don't be overly enthusiastic, don't be cringe;

        {history}
        Boyfriend: {human_input}
        Shirley:   
        """

        return PromptTemplate(
            input_variables={"history", "human_input"},
            template=template
        )

    def _create_chat(self):
        return LLMChain(
            llm=ChatOpenAI(temperature=0.2),
            prompt=self.prompt_template,
            verbose=True,
            memory=ConversationBufferWindowMemory(k=10),
        )

    def get(self, human_input):
        return self.chat.predict(human_input=human_input)


class VoiceMessage:
    """
    A classe VoiceMessage é responsável pela criação de uma mensagem de voz a partir de um texto.
    """

    def __init__(self, settings, name="Rachel"):
        self._name = name
        self.settings = settings

    def play(self):
        playsound("audio.mp3")
        return self

    def get(self, message):
        payload = {
            "text": message,
            "model_id": "eleven_multilingual_v1",
            "language": "portuguese",
            "voice_settings": {
                "stability": 0,
                "similarity_boost": 0.3,
            }
        }

        headers = {
            "accept": "audio/mpeg",
            "xi-api-key": self.settings.values["ELEVEN_LABS_API_KEY"],
            "Content-Type": "application/json",
        }

        voice = self.settings.get_voice_id(self._name)
        response = requests.post(
            f'https://api.elevenlabs.io/v1/text-to-speech/{voice}?optimize_streaming_latency=0',
            json=payload,
            headers=headers,
        )
        if response.status_code == 200 and response.content:
            with open("audio.mp3", "wb") as f:
                f.write(response.content)

            t = Thread(target=self.play)
            t.start()
        else:
            raise Exception(f"Problemas com o áudio - {response.status_code}.")
