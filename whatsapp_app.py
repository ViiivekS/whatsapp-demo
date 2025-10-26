from flask import Flask, request
import os

app = Flask(__name__)

@app.route("/whatsapp", methods=["POST"])
def whatsapp_webhook():
    # Get incoming message details
    from_number = request.values.get("From", "")
    body = request.values.get("Body", "")
    
    print(f"Received message from {from_number}: {body}")
    
    # Respond to Twilio (optional)
    return "Message received", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
