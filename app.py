from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

# Sample vendor data
vendors = {
    "vegetables": [
        {"name": "Fresh Veggies", "location": "Downtown", "contact": "123-456-7890"},
        {"name": "Green Grocer", "location": "Uptown", "contact": "987-654-3210"}
    ],
    "fruits": [
        {"name": "Fruit Basket", "location": "Midtown", "contact": "555-555-5555"},
        {"name": "Tropical Fruits", "location": "Eastside", "contact": "444-444-4444"}
    ],
    "dairy": [
        {"name": "Dairy Farm", "location": "Westside", "contact": "333-333-3333"},
        {"name": "Milk & More", "location": "Southside", "contact": "222-222-2222"}
    ]
}

@app.route('/whatsapp', methods=['POST'])
def whatsapp_reply():
    msg = request.form.get('Body', '').strip().lower()
    response = MessagingResponse()

    if msg in vendors:
        vendor_info = "\n".join(
            f"{v['name']} - {v['location']} - {v['contact']}" for v in vendors[msg]
        )
        response.message(f"Here are the nearby {msg} vendors:\n{vendor_info}")
    else:
        response.message(
            "Welcome to Vconnect! 🛒\nSend one of the following to get vendor info:\n"
            "- vegetables\n- fruits\n- dairy"
        )

    return str(response)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
