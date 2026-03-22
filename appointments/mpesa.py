import requests   # ✅ CORRECT
import base64
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()  


def get_access_token():
    url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"

    res = requests.get(  
        url,
        auth=(os.getenv('CONSUMER_KEY'), os.getenv('CONSUMER_SECRET'))
    )

    return res.json().get("access_token")


def stk_push(phone, amount, appointment_id):
    access_token = get_access_token()

    url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"

    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')

    password = base64.b64encode(
        (os.getenv('SHORTCODE') + os.getenv('PASSKEY') + timestamp).encode()
    ).decode("utf-8")

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    payload = {
        "BusinessShortCode": os.getenv('SHORTCODE'),
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": int(amount),
        "PartyA": phone,
        "PartyB": os.getenv('SHORTCODE'),
        "PhoneNumber": phone,
        "CallBackURL": os.getenv('CALLBACK_URL'),
        "AccountReference": f"{appointment_id}WasafiSalon",
        "TransactionDesc": "Appointment Payment"
    }

    response = requests.post(url, json=payload, headers=headers)

    return response.json()