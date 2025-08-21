import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

def get_drug_status(batch_id):
    doc = db.collection("drug_batches").document(batch_id).get()
    if doc.exists:
        return doc.to_dict()
    return None
