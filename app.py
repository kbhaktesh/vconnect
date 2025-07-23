from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route("/whatsapp", methods=["POST"])
def whatsapp_reply():
    incoming_msg = request.values.get("Body", "").lower()
    print(f"User said: {incoming_msg}")
    
    resp = MessagingResponse()
    msg = resp.message()

    if "vegetable" in incoming_msg:
        msg.body("Here are nearby vegetable vendors:\n1. Raj Veggies - +91XXXXXXX\n2. Local Fresh - +91YYYYYYY")
    elif "grocery" in incoming_msg:
        msg.body("Top Grocery Stores:\n1. Sharma Kirana - +91AAAAAAA")
    elif "order" in incoming_msg:
        msg.body("Thanks! Your order has been recorded. A vendor will contact you soon.")
    else:
        msg.body("👋 Welcome to Vconnect!\nReply with:\n• 'vegetable'\n• 'grocery'\n• 'order milk'")

    return str(resp)

if __name__ == "__main__":
    app.run(port=5000)
