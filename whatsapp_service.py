import os
from twilio.rest import Client

client = Client(
    os.environ["TWILIO_ACCOUNT_SID"],
    os.environ["TWILIO_AUTH_TOKEN"]
)

FROM_NUMBER = os.environ["TWILIO_WHATSAPP_FROM"]

def send_whatsapp(to, message):
    msg = client.messages.create(
        body=message,
        from_=FROM_NUMBER,
        to=f"whatsapp:{to}"
    )
    return msg.sid
