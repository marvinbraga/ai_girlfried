from flask import Flask, render_template, request

from chats.girl_friend import AIChat, VoiceMessage
from chats.settings import Settings

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/send_message", methods=["POST"])
def send_message():
    settings = Settings('.res/voices.json')
    human_input = request.form["human_input"]
    message = AIChat(settings).get(human_input)
    VoiceMessage(settings).get(message)
    return message


if __name__ == '__main__':
    app.run(debug=True)
