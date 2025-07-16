from flask import Flask, request
import telegram
import json

app = Flask(__name__)

@app.route('/')
def home():
    return '💖 Kitty is alive 💖'

@app.route('/send-file', methods=['POST'])
def send_file():
    with open('config.json') as f:
        config = json.load(f)

    bot = telegram.Bot(token=config['telegram_bot_token'])
    chat_id = config['telegram_chat_id']
    file_link = config['file_url']

    data = request.json
    if data.get('text') == 'Paid 💸':
        msg = f"Thanks for the payment \nHere’s your file: {file_link}"
        bot.send_message(chat_id=chat_id, text=msg)
        return 'Message sent!', 200

    return 'Ignored', 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
