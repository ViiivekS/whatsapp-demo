from flask import Flask, request
import os
import json
import gspread
from google.oauth2.service_account import Credentials
from twilio.twiml.messaging_response import MessagingResponse
from datetime import datetime

app = Flask(__name__)

# --- Load Google credentials from Render environment variable ---
service_account_info = json.loads(os.getenv("GOOGLE_CREDENTIALS"))

# ✅ Scopes required for Google Sheets and Drive
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# Build credentials with scopes
creds = Credentials.from_service_account_info(service_account_info, scopes=SCOPES)

# Authorize gspread
client = gspread.authorize(creds)

# --- Open your Google Sheet ---
# Replace with your actual Google Sheet ID
SHEET_ID = os.getenv("SHEET_ID", "1jwFeDwca9NK1lgkLfdW7cY4xANmgLrSUeDzu7j4PXmo")
sheet = client.open_by_key(SHEET_ID).sheet1

# --- WhatsApp webhook route ---
@app.route("/webhook", methods=["POST"])
def webhook():
    # Get message and sender details from Twilio
    msg = request.form.get("Body")
    sender = request.form.get("From")

    # Get current timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Log to Google Sheet (timestamp, sender, message)
    sheet.append_row([timestamp, sender, msg])

    # Respond back to the user
    response = MessagingResponse()
    response.message("✅ Message received and saved to Google Sheets!")

    return str(response)

@app.route("/", methods=["GET"])
def home():
    return "WhatsApp Bot is running!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
