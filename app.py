from flask import Flask, request
import pandas as pd

app = Flask(__name__)

# Load vendors data
vendors_df = pd.read_csv("vendors.csv")

# Helper function to filter vendors by category
def get_vendors_by_category(category):
    category = category.lower()
    matches = vendors_df[vendors_df['Category'].str.lower() == category]
    if matches.empty:
        return "Sorry, no vendors found for that category."
    result = "Here are some vendors:\n"
    for _, row in matches.iterrows():
        result += f"- {row['Name']} ({row['Location']}), Contact: {row['Phone']}\n"
    return result

@app.route("/whatsapp", methods=["POST"])
def whatsapp_bot():
    incoming_msg = request.values.get('Body', '').strip().lower()
    response = get_vendors_by_category(incoming_msg)
    
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Message>{response}</Message>
</Response>"""

if __name__ == "__main__":
    app.run(debug=True)
