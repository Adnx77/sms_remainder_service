from firebase_admin import firestore
from firebase_init import init_firebase

# Lazy initialization - don't create client at module level
_db = None

def get_db():
    """
    Get Firestore database client, initializing if necessary.
    This ensures Firebase is initialized before creating the client.
    """
    global _db
    if _db is None:
        # Ensure Firebase is initialized
        init_firebase()
        _db = firestore.client()
    return _db

def get_children():
    """
    Fetch all children documents from Firestore
    """
    db = get_db()
    return db.collection("children").stream()

def update_reminder(card_id, reminder_data):
    """
    Merge reminder metadata without overwriting child data
    """
    db = get_db()
    db.collection("children").document(card_id).set({
        "reminder": reminder_data
    }, merge=True)
