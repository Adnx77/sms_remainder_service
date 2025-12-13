from firestore_service import get_children, update_reminder
from sms_service import send_sms
import datetime

MAX_DAYS = 14

def run_test_sms():
    send_sms("7306312986", "✅ TEST: Vaccination SMS system is working.")

def run_reminders():
    today = datetime.date.today()

    for doc in get_children():
        child = doc.to_dict()
        card_id = doc.id

        parent = child.get("parent_phone")
        name = child.get("name", "your child")

        reminder = child.get("reminder", {})
        days_sent = reminder.get("days_sent", 0)

        if days_sent >= MAX_DAYS:
            continue

        vaccines = child.get("vaccination", {}).get("schedule", {})

        for vaccine, vdata in vaccines.items():
            status = vdata.get("status")
            due_date = vdata.get("due_date")

            if status == "done" or not due_date:
                continue

            due = datetime.datetime.strptime(due_date, "%Y-%m-%d").date()

            if due < today:
                msg = f"⚠️ ALERT: {name} missed {vaccine} vaccine on {due_date}. Visit clinic immediately."
            elif (due - today).days <= 14:
                msg = f"⏰ REMINDER: {name} is due for {vaccine} vaccine on {due_date}."
            else:
                continue

            send_sms(parent, msg)

            update_reminder(card_id, {
                "last_sent": datetime.datetime.utcnow().isoformat(),
                "days_sent": days_sent + 1
            })
            break
