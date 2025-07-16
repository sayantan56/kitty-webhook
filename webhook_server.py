from flask import Flask, request
import telegram
import json

app = Flask(__name__)

with open("config.json", "r") as f:
    config = json.load(f)

BOT_TOKEN = config["telegram_bot_token"]
CHAT_ID = config["telegram_chat_id"]
FILE_URL = config["file_url"]

bot = telegram.Bot(token=BOT_TOKEN)

@app.route("/", methods=["GET"])
def home():
    return "💖 Kitty Webhook is alive 💖"

@app.route("/send-file", methods=["POST"])
def send_file():
    data = request.json
    print("📥 Incoming webhook:", data)

    if data and data.get("event") == "payment.captured":
        msg = f"Thanks for the payment 😘\nHere’s your file: {FILE_URL}"
        bot.send_message(chat_id=CHAT_ID, text=msg)
        return "✅ File sent", 200
    return "❌ Ignored", 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
