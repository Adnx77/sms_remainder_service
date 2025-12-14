from flask import Flask, request, jsonify
from reminder_logic import run_daily_reminders, run_test_whatsapp
import os

app = Flask(__name__)

def authorized(req):
    return req.args.get("secret") == os.environ["CRON_SECRET"]

@app.route("/")
def home():
    return "WhatsApp Reminder Service Running"

@app.route("/run-daily")
def run_daily():
    secret = request.args.get("secret")
    if secret != os.environ.get("CRON_SECRET"):
        return "Unauthorized", 401

    try:
        run_daily_reminders()
    except Exception as e:
        # 🔥 THIS IS CRITICAL
        print("RUN-DAILY ERROR:", str(e))
        import traceback
        traceback.print_exc()
        return "ERROR", 500

    return "OK", 200


@app.route("/run-test")
def run_test():
    if not authorized(request):
        return jsonify({"error": "Unauthorized"}), 401

    run_test_whatsapp()
    return jsonify({"status": "Test WhatsApp sent"})

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)



