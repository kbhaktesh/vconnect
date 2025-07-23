from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route("/whatsapp", methods=["POST"])
def whatsapp_reply():
    incoming_msg = request.values.get("Body", "").lower()
    print(f"User: {incoming_msg}")

    resp = MessagingResponse()
    msg = resp.message()

    if "vegetable" in incoming_msg:
        msg.body("🧅🥕 Vendors near you:\n1. Raj Veggies - +91XXXXXXXXXX")
    elif "grocery" in incoming_msg:
        msg.body("🛒 Grocery Options:\n1. Sharma Kirana - +91XXXXXXXXXX")
    elif "order" in incoming_msg:
        msg.body("✅ Order placed. Vendor will contact you shortly.")
    else:
        msg.body("👋 Welcome to Vconnect!\nType:\n• 'vegetable'\n• 'grocery'\n• 'order milk'")

    return str(resp)

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # fallback to 10000 for local
    app.run(host="0.0.0.0", port=port)

