from flask import Flask, render_template, request

from chats.girl_friend import AIChat, VoiceMessage
from chats.settings import Settings

app = Flask(__name__)
settings = Settings('.res/voices.json')
name = "Bella"
chat = AIChat(settings, name)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/send_message", methods=["POST"])
def send_message():
    human_input = request.form["human_input"]
    message = chat.get(human_input)
    VoiceMessage(settings, name).get(message)
    return message


@app.route("/voices", methods=["GET"])
def get_voices():
    return VoiceMessage(settings, name).list()


if __name__ == '__main__':
    app.run(debug=True)
