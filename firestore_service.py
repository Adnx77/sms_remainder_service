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
        init_firebase()
        _db = firestore.client()
    return _db


def get_children():
    """
    Fetch all children documents from Firestore
    Yields: (card_id, child_dict)
    """
    db = get_db()
    docs = db.collection("children").stream()

    for doc in docs:
        yield doc.id, doc.to_dict()


def update_reminder(card_id, reminder_data):
    """
    Merge reminder metadata without overwriting child data
    """
    db = get_db()
    db.collection("children").document(card_id).set(
        {
            "tracking": reminder_data
        },
        merge=True
    )
