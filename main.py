from flask_ngrok import run_with_ngrok
from flask import Flask, request, jsonify, json, send_from_directory
import os

from bot_server import BotServer

app = Flask(__name__, static_url_path='')
port = int(os.environ.get("PORT", 5000))
run_with_ngrok(app)   #starts ngrok when the app is run

@app.route('/')
def index():
    """
    This route at the home page renders the index.html template with blank
    variables.
    """
    
    return jsonify(
        messages = [
            {
                "message": "Hello!",
                "fromBot": True
            },
            {
                "message": "How are you?",
                "fromBot": True
            },
            {
                "message": "You can ask me what ever you want about coronavirus.",
                "fromBot": True
            }
        ]
    )

@app.route('/dialog', methods=['POST'])
def dialog():
    """
    This route uses the POST method to take user request and return the result
    of passing it to the BotServer similarity matching function.
    """
    return bot.bot_dialog(request)

@app.route('/records/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    return send_from_directory(directory='./records/out', filename=filename)


"""
Default Python entrypoint creates Botserver object and runs Flask app.
"""
bot = BotServer('./data/faq-text-preprocessed.csv')

app.run(debug=True,host='0.0.0.0',port=port)
