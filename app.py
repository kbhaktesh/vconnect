from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

vendors = {
    "vegetables": [
        {"name": "Ram Veggies", "location": "Vidisha", "contact": "9876543210"},
        {"name": "Krishna Veggies", "location": "Vidisha", "contact": "9876054321"}
    ],
    "fruits": [
        {"name": "Fresh Fruits", "location": "Bhopal", "contact": "9897123540"}
    ],
    "dairy": [
        {"name": "Dairy King", "location": "Vidisha", "contact": "9876345019"},
        {"name": "Fresh Dairy", "location": "Vidisha", "contact": "9876123045"}
    ],
    "grocery": [
        {"name": "Kirana Point", "location": "Vidisha", "contact": "9876543201"},
        {"name": "Mohan Kirana", "location": "Vidisha", "contact": "9876541230"},
        {"name": "All in One Store", "location": "Vidisha", "contact": "7654321890"}
    ]
}

@app.route('/', methods=['GET'])
def home():
    return "✅ Vconnect WhatsApp Bot is live! Use /whatsapp with Twilio."

@app.route('/whatsapp', methods=['POST'])
def whatsapp_reply():
    msg = request.form.get('Body', '').strip().lower()
    response = MessagingResponse()

    if not msg:
        response.message("❌ Empty message received. Please send a valid keyword.")
    elif msg in vendors:
        vendor_info = "\n".join(
            f"{v['name']} - {v['location']} - {v['contact']}" for v in vendors[msg]
        )
        response.message(f"📦 Nearby {msg} vendors:\n{vendor_info}")
    else:
        response.message(
            "👋 Welcome to Vconnect!\n"
            "Please send one of the following keywords:\n"
            "• vegetables\n• fruits\n• dairy\n• grocery"
        )

    return str(response)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
