from fastapi import FastAPI, Request
import requests
import os

app = FastAPI()

TOKEN = os.getenv("TELEGRAM_TOKEN")
SMM_API_KEY = os.getenv("SMM_KEY")
SMM_API_URL = os.getenv("API_URL", "https://galaxysmmpanel.com/api/v2")

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": chat_id, "text": text})

@app.post("/webhook/{token}")
async def webhook(token: str, request: Request):
    if token != TOKEN:
        return {"status": "unauthorized"}
    data = await request.json()
    message = data.get("message", {})
    chat_id = message.get("chat", {}).get("id")
    text = message.get("text", "").lower()

    if text == "/start":
        send_message(chat_id, "👋 Welcome to Rise Online!
Select a platform:
1. Instagram")
    elif "instagram" in text:
        send_message(chat_id, "Choose a service:
1. Followers
2. Comments")
    elif "followers" in text:
        send_message(chat_id, "Enter quantity (e.g., 100):")
    elif text.isdigit():
        price = int(text) * 0.3
        send_message(chat_id, f"💰 Total: ₹{price:.2f}
Pay to UPI: 8188938018@fam
Then send your UTR ID.")
    elif text.startswith("utr"):
        send_message(chat_id, "✅ Order placed successfully!
Thank you for using Rise Online.")
    else:
        send_message(chat_id, "Send /start to begin.")

    return {"ok": True}
