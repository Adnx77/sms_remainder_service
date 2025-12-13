from flask import Flask, request, jsonify
from firebase_init import init_firebase
import os

# Initialize Firebase FIRST before importing other modules that depend on it
try:
    init_firebase()
except Exception as e:
    print(f"Error initializing Firebase: {e}")
    raise

# Now safe to import modules that use Firestore
from reminder_logic import run_reminders, run_test_sms

app = Flask(__name__)

CRON_SECRET = os.getenv("CRON_SECRET")

def is_authorized(req):
    return req.args.get("secret") == CRON_SECRET

@app.route("/")
def health_check():
    return "SMS Reminder Service is running"

@app.route("/run-daily", methods=["GET"])
def run_daily():
    if not is_authorized(request):
        return jsonify({"error": "Unauthorized"}), 401

    run_reminders()
    return jsonify({"status": "Daily reminders executed successfully"})

@app.route("/run-test", methods=["GET"])
def run_test():
    if not is_authorized(request):
        return jsonify({"error": "Unauthorized"}), 401

    run_test_sms()
    return jsonify({"status": "Test SMS sent successfully"})

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
