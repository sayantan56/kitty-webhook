from flask import Flask, request
import json
import hmac
import hashlib
import telegram

app = Flask(__name__)

# Load config
with open("config.json", "r") as f:
    config = json.load(f)

BOT_TOKEN = config["telegram_bot_token"]
CHAT_ID = config["telegram_chat_id"]
FILE_URL = config["file_url"]
WEBHOOK_SECRET = config["razorpay_secret"]

bot = telegram.Bot(token=BOT_TOKEN)

@app.route("/", methods=["GET"])
def home():
    return "💖 Kitty Webhook is alive 💖"

@app.route("/webhook", methods=["POST"])
def webhook():
    payload = request.data
    received_signature = request.headers.get('X-Razorpay-Signature')

    # Verify webhook signature
    generated_signature = hmac.new(
        bytes(WEBHOOK_SECRET, 'utf-8'),
        msg=payload,
        digestmod=hashlib.sha256
    ).hexdigest()

    if not hmac.compare_digest(received_signature, generated_signature):
        return "❌ Invalid signature", 403

    data = json.loads(payload)
    print("📥 Verified webhook:", data)

    if data.get("event") == "payment.captured":
        msg = f"Thanks for the payment 😘\nHere’s your file: {FILE_URL}"
        bot.send_message(chat_id=CHAT_ID, text=msg)
        return "✅ File sent", 200

    return "❌ Ignored", 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
