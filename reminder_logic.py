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
    two_days_from_now = today + timedelta(days=2)

    for card_id, child in get_children():
        try:
            if not isinstance(child, dict):
                continue

            # ---- BASIC INFO ----
            parent = child.get("parent", {})
            phone = parent.get("phone")
            if not phone:
                continue

            identity = child.get("identity", {})
            name = identity.get("name", "your child")

            # ---- IDEMPOTENCY ----
            tracking = child.get("tracking", {})
            last_sent = tracking.get("last_notification")
            if last_sent == today.isoformat():
                continue

            # ---- VACCINATION DATA ----
            vaccination = child.get("vaccination", {})
            schedule = vaccination.get("schedule", {})

            overdue = []
            upcoming = []

            for vaccine, info in schedule.items():
                if not isinstance(info, dict):
                    continue

                status = info.get("status")
                due_date_str = info.get("due_date")

                if not status or not due_date_str:
                    continue

                try:
                    due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date()
                except:
                    continue

                # 🔴 Overdue
                if status == "due" and due_date < today:
                    overdue.append(vaccine)

                # 🟡 2 days before
                elif status == "due" and due_date == two_days_from_now:
                    upcoming.append(vaccine)

            # ---- DECIDE MESSAGE ----
            if overdue:
                msg = (
                    f"⚠️ Vaccination Overdue Alert\n\n"
                    f"{name} has missed the following vaccines:\n"
                    f"{', '.join(overdue)}\n\n"
                    f"Please visit the nearest health center immediately."
                )
                reminder_type = "overdue"

            elif upcoming:
                msg = (
                    f"⏰ Upcoming Vaccination Reminder\n\n"
                    f"{name} has vaccines scheduled in 2 days:\n"
                    f"{', '.join(upcoming)}\n\n"
                    f"Please be prepared to visit the health center."
                )
                reminder_type = "upcoming"

            else:
                continue

            # ---- SEND WHATSAPP ----
            send_whatsapp(phone, msg)

            # ---- MERGE UPDATE (NO OVERWRITE) ----
            db.collection("children").document(card_id).set(
                {
                    "tracking": {
                        "last_notification": today.isoformat(),
                        "last_notification_type": reminder_type
                    }
                },
                merge=True
            )

        except Exception as e:
            # Never let one child crash cron
            print(f"Reminder failed for {card_id}: {e}")
            continue

