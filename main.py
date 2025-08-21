from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import logging
import firebase_admin
from firebase_admin import credentials, firestore
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
HEDERA_ACCOUNT_ID = os.getenv("HEDERA_ACCOUNT_ID", "0.0.6519209")
HEDERA_PRIVATE_KEY = os.getenv("HEDERA_PRIVATE_KEY", "0x6ba6ad73a002994df73118024eb9ae6e8e484e641627f5e2c0401d7ff19c7d01")
DRUG_VERIFICATION_TOPIC_ID = os.getenv("DRUG_VERIFICATION_TOPIC_ID")

# Initialize Firebase
cred = credentials.Certificate(r"C:\Users\Gezawa\Documents\New folder (16)\drug-verification-ussd\serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# Simulated Hedera check (to be replaced with actual SDK logic)
def verify_drug_on_chain(batch_id):
    # Placeholder for Hedera logic using Testnet (replace with real SDK calls)
    hedera_verified_batches = ["ABC123", "XYZ789"]
    return "Verified" if batch_id in hedera_verified_batches else "Unverified"

# Firebase drug metadata lookup
def get_drug_status(batch_id):
    try:
        doc_ref = db.collection("drugs").document(batch_id)
        doc = doc_ref.get()
        if doc.exists:
            return doc.to_dict()
    except Exception as e:
        logging.error(f"Firebase error: {e}")
    return None

# Initialize FastAPI app
app = FastAPI()

# Enable CORS for FlowSim
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Enable logging
logging.basicConfig(level=logging.INFO)

# USSD route
@app.post("/ussd")
async def ussd(request: Request):
    try:
        data = await request.json()
    except Exception as e:
        logging.warning(f"Connection test or invalid JSON: {e}")
        return {"response": "END Connection test OK", "sessionId": "test-session"}

    logging.info(f"Received JSON: {data}")
    print("Received JSON:", data)

    session_id = data.get("sessionId", "")
    service_code = data.get("serviceCode", "")
    if service_code != "*384#":
        return {"response": "END Invalid service code", "sessionId": session_id}

    phone_number = data.get("phoneNumber", "")
    text = data.get("text", "")

    if text == "":
        response = "CON Welcome to Drug Checker\nEnter Drug Batch ID:"
    else:
        batch_id = text.strip().upper()
        drug_data = get_drug_status(batch_id)
        if drug_data:
            #status = verify_drug_on_chain(batch_id)
            expiry = drug_data.get("expiry", "Unknown")
            drug_name = drug_data.get("drugName", "Unknown")
            manufacturer = drug_data.get("manufacturer", "Unknown")
            tokenId = drug_data.get("tokenId", "Unknown")
            batchId = drug_data.get("batchId", "Unknown")
            response = (
                #f"END Drug Status: {status}\n"
                f"Expiry: {expiry}\n"
                f"Drug Name: {drug_name}\n"
                f"Manufacturer: {manufacturer}\n"
                f"tokenId: {tokenId}\n"
                f"batchId: {batchId}\n"
            )
        else:
            response = "END Batch ID not found."

    logging.info(f"Response: {response}")
    return {
        "response": response,
        "sessionId": session_id
    }