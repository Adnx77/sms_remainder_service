import firebase_admin
from firebase_admin import credentials
import os
import json

def init_firebase():
    """
    Initialize Firebase Admin SDK safely.
    This runs only once even if imported multiple times.
    Supports both file-based and environment variable credentials (for cloud deployments).
    """
    if not firebase_admin._apps:
        # Try to get credentials from environment variable first (for cloud deployments like Render)
        firebase_creds_json = os.getenv("FIREBASE_CREDENTIALS_JSON")
        
        if firebase_creds_json:
            # Parse JSON string from environment variable
            try:
                cred_dict = json.loads(firebase_creds_json)
                cred = credentials.Certificate(cred_dict)
            except json.JSONDecodeError:
                raise ValueError("FIREBASE_CREDENTIALS_JSON is not valid JSON")
        else:
            # Fall back to service account key file (for local development)
            service_account_path = os.getenv("FIREBASE_SERVICE_ACCOUNT_PATH", "serviceAccountKey.json")
            if not os.path.exists(service_account_path):
                raise FileNotFoundError(
                    f"Firebase credentials not found. Either set FIREBASE_CREDENTIALS_JSON environment variable "
                    f"or place serviceAccountKey.json in the project root."
                )
            cred = credentials.Certificate(service_account_path)
        
        firebase_admin.initialize_app(cred)
