from flask import Flask, request
import json
import telegram
import logging

app = Flask(__name__)

# Load config
with open("config.json", "r") as f:
    config = json.load(f)

BOT_TOKEN = config["telegram_bot_token"]
FILE_URL = config["delivery_link"]
LOG_FILE = config["log_file"]

bot = telegram.Bot(token=BOT_TOKEN)

# Setup logging
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(message)s')

@app.route('/payment-hook', methods=['POST'])
def handle_webhook():
    try:
        data = request.json
        if data["event"] == "payment.captured":
            payment = data["payload"]["payment"]["entity"]
            chat_id = payment["notes"].get("chat_id")

            if chat_id:
                bot.send_message(chat_id=chat_id, text=f"Thanks for the payment 😘\nHere’s your file:\n{FILE_URL}")
                logging.info(f"{chat_id} | {payment['email']} | ₹{payment['amount']/100:.2f} | Auto Delivered ✅")
                return "Delivered", 200
            else:
                logging.warning("❌ No chat_id found in payment notes.")
                return "Missing chat_id", 400
        else:
            return "Ignored non-payment event", 200

    except Exception as e:
        logging.error(f"Webhook error: {str(e)}")
        return "Error", 500

if __name__ == "__main__":
    app.run(port=5000)
