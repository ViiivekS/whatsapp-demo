from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import os
import json
import re
from google.oauth2 import service_account
from googleapiclient.discovery import build

app = Flask(__name__)

# ---------------- Google Sheets Setup ----------------
creds_json = os.getenv("GOOGLE_CREDENTIALS_JSON")  # set this in Render env
creds_dict = json.loads(creds_json)
creds = service_account.Credentials.from_service_account_info(creds_dict)
sheet_service = build('sheets', 'v4', credentials=creds)
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")  # create a Google Sheet and set this env

def append_to_sheet(name, email, phone):
    sheet = sheet_service.spreadsheets()
    values = [[name, email, phone]]
    sheet.values().append(
        spreadsheetId=SPREADSHEET_ID,
        range="Sheet1!A:C",
        valueInputOption="RAW",
        body={"values": values}
    ).execute()

# ---------------- Data Extraction ----------------
def extract_details(text):
    # Extract email
    email_match = re.search(r"[\w\.-]+@[\w\.-]+", text)
    email = email_match.group(0) if email_match else ""

    # Extract phone number (simple patterns)
    phone_match = re.search(r"\+?\d[\d\s]{7,}\d", text)
    phone = phone_match.group(0) if phone_match else ""

    # Extract name (first line as naive approach)
    name = text.strip().split("\n")[0] if text.strip() else ""
    return name, email, phone

# ---------------- Flask Routes ----------------
@app.route('/')
def home():
    return "WhatsApp Resume Parser is running!"

@app.route('/whatsapp', methods=['POST'])
def whatsapp_reply():
    incoming_msg = request.values.get('Body', '').strip()
    sender = request.values.get('From', '')
    
    # Extract info
    name, email, phone = extract_details(incoming_msg)
    
    # Append to Google Sheet
    if name or email or phone:
        append_to_sheet(name, email, phone)
    
    # Respond on WhatsApp
    resp = MessagingResponse()
    msg = resp.message()
    msg.body(f"Hi {name or 'there'}! Your details have been recorded.\nEmail: {email}\nPhone: {phone}")
    return str(resp)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
