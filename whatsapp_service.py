import os
from twilio.rest import Client

ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
FROM_NUMBER = os.environ.get("TWILIO_WHATSAPP_FROM")

# HARD FAIL if env vars missing
if not ACCOUNT_SID:
    raise RuntimeError("TWILIO_ACCOUNT_SID missing")
if not AUTH_TOKEN:
    raise RuntimeError("TWILIO_AUTH_TOKEN missing")
if not FROM_NUMBER:
    raise RuntimeError("TWILIO_WHATSAPP_FROM missing")

client = Client(ACCOUNT_SID, AUTH_TOKEN)

def send_whatsapp(to, message):
    msg = client.messages.create(
        body=message,
        from_=FROM_NUMBER,
        to=f"whatsapp:{to}"
    )
    print("TWILIO MESSAGE SID:", msg.sid)
    print("STATUS:", msg.status)
    return msg.sid
