from flask import Flask, request
import os
import json
import gspread
from google.oauth2.service_account import Credentials
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

# --- Load Google credentials from Render environment variable ---
service_account_info = json.loads(os.getenv("GOOGLE_CREDENTIALS"))
creds = Credentials.from_service_account_info(service_account_info)
client = gspread.authorize(creds)

# --- Open your Google Sheet ---
# Replace with your actual Google Sheet ID
SHEET_ID = "YOUR_GOOGLE_SHEET_ID"
sheet = client.open_by_key(SHEET_ID).sheet1


# --- WhatsApp webhook route ---
@app.route("/webhook", methods=["POST"])
def webhook():
    # Get message and sender details from Twilio
    msg = request.form.get("Body")
    sender = request.form.get("From")

    # Log to Google Sheet
    sheet.append_row([sender, msg])

    # Respond back to the user
    response = MessagingResponse()
    response.message("✅ Message received and saved to Google Sheets!")

    return str(response)


@app.route("/", methods=["GET"])
def home():
    return "WhatsApp Bot is running!"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
