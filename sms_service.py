import requests
import os

API_KEY = os.getenv("FAST2SMS_API_KEY")

def send_sms(phone, message):
    """
    Send SMS using Fast2SMS API
    
    Args:
        phone: Phone number to send SMS to
        message: Message content
    """
    if not API_KEY:
        raise ValueError("FAST2SMS_API_KEY environment variable is not set")
    
    if not phone or not message:
        raise ValueError("Phone number and message are required")
    
    url = "https://www.fast2sms.com/dev/bulkV2"
    payload = {
        "route": "q",
        "message": message,
        "numbers": phone
    }
    headers = {
        "authorization": API_KEY,
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error sending SMS: {e}")
        raise
