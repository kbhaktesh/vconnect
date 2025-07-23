from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import csv
import os

app = Flask(__name__)

# Load vendor data from CSV
vendors = []
with open("vendors.csv", newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        vendors.append(row)

@app.route("/whatsapp", methods=["POST"])
def whatsapp_reply():
    incoming_msg = request.values.get("Body", "").lower()
    print(f"User: {incoming_msg}")

    resp = MessagingResponse()
    msg = resp.message()

    matched_vendors = []

    # Simple keyword search
    for vendor in vendors:
        category = vendor["Category"].lower()
        location = vendor["Location"].lower()
        if category in incoming_msg:
            matched_vendors.append(f"{vendor['Name']} - {vendor['Phone']} ({vendor['Location']})")

    if matched_vendors:
        response_text = "🔎 Vendors matching your request:\n" + "\n".join(matched_vendors)
        msg.body(response_text)
    elif "order" in incoming_msg:
        msg.body("✅ Order placed. Vendor will contact you shortly.")
    else:
        msg.body("👋 Welcome to Vconnect!\nType what you’re looking for, e.g.:\n• 'vegetable'\n• 'milk'\n• 'order'")

    return str(resp)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
