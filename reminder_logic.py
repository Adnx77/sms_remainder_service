from datetime import datetime, timedelta
from firestore_service import get_children, update_reminder
from whatsapp_service import send_whatsapp

def run_test_whatsapp():
    send_whatsapp(
        "+917306312986",
        "✅ TEST: WhatsApp vaccination reminder system is working."
    )

def run_daily_reminders():
    today = datetime.utcnow().date()

    for card_id, child in get_children():
        phone = child.get("parent_phone")
        name = child.get("name", "your child")
        vaccines = child.get("vaccines", {})

        overdue = [v for v, s in vaccines.items() if s == "due"]

        if overdue:
            msg = (
                f"⚠️ Vaccination Reminder\n\n"
                f"{name} has overdue vaccines:\n"
                f"{', '.join(overdue)}\n\n"
                f"Please visit the nearest health center."
            )

            send_whatsapp(phone, msg)
            update_reminder(card_id, "overdue")
