import requests
import os

FAST2SMS_API_KEY = os.environ.get("FAST2SMS_API_KEY")

def send_sms(phone, message):
    if not FAST2SMS_API_KEY:
        print("FAST2SMS_API_KEY not set")
        return

    payload = {
        "route": "v3",
        "sender_id": "TXTIND",
        "message": message,
        "language": "english",
        "numbers": phone
    }

    headers = {
        "authorization": FAST2SMS_API_KEY,
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(
            "https://www.fast2sms.com/dev/bulkV2",
            json=payload,
            headers=headers,
            timeout=10
        )

        print("FAST2SMS STATUS:", response.status_code)
        print("FAST2SMS RESPONSE:", response.text)

    except Exception as e:
        print("SMS ERROR:", str(e))

