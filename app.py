from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import pandas as pd

app = Flask(__name__)

# Load vendors.csv
vendors_df = pd.read_csv("vendors.csv")

# Ensure consistent formatting
vendors_df['Category'] = vendors_df['Category'].str.strip().str.lower()
vendors_df['Location'] = vendors_df['Location'].str.strip().str.lower()

@app.route("/whatsapp", methods=["POST"])
def whatsapp_reply():
    incoming_msg = request.values.get("Body", "").strip().lower()
    print(f"User: {incoming_msg}")

    resp = MessagingResponse()
    msg = resp.message()

    # Keyword to Category Mapping
    keyword_map = {
        "vegetable": "vegetables",
        "veggies": "vegetables",
        "grocery": "grocery",
        "milk": "dairy",
        "curd": "dairy",
        "paneer": "dairy",
        "dairy": "dairy",
        "fruit": "fruits",
        "apple": "fruits",
        "banana": "fruits",
        "bread": "bakery",
        "cake": "bakery",
        "bakery": "bakery"
    }

    matched = None
    for word in keyword_map:
        if word in incoming_msg:
            matched = keyword_map[word]
            break

    if matched:
        filtered = vendors_df[
            (vendors_df['Category'] == matched) & (vendors_df['Location'] == "vidisha")
        ]
        if filtered.empty:
            msg.body(f"❌ No {matched} vendors found in Vidisha.")
        else:
            reply = f"🛍️ {matched.capitalize()} vendors in Vidisha:\n"
            for _, row in filtered.iterrows():
                reply += f"• {row['Name']} - {row['Phone']}\n"
            msg.body(reply)
    elif "order" in incoming_msg:
        msg.body("✅ Order placed. The vendor will contact you shortly.")
    else:
        msg.body(
            "👋 Welcome to Vconnect!\n"
            "Type a category or item to get vendor info:\n"
            "• 'vegetables'\n"
            "• 'grocery'\n"
            "• 'milk'\n"
            "• 'fruits'\n"
            "• 'bread'\n"
            "Or type 'order' to place an order."
        )

    return str(resp)

if __name__ == "__main__":
    app.run(port=10000)
