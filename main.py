from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import logging
from dotenv import load_dotenv
from firebase_utils import get_drug_status
from hedera_utils import verify_drug_on_chain

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(level=logging.INFO)

@app.get("/")
def health():
    return {"status": "ok"}

@app.post("/ussd")
async def ussd(request: Request):
    try:
        data = await request.json()
    except Exception as e:
        logging.warning(f"Invalid JSON or connection test: {e}")
        return {"response": "END Connection test OK", "sessionId": "test-session"}

    session_id = data.get("sessionId", "")
    service_code = data.get("serviceCode", "")
    phone_number = data.get("phoneNumber", "")
    text = data.get("text", "")

    if service_code != "*384#":
        return {"response": "END Invalid service code", "sessionId": session_id}

    if text == "":
        response = "CON Welcome to Drug Checker\nEnter Drug Batch ID:"
    else:
        batch_id = text.strip().upper()
        drug_data = get_drug_status(batch_id)
        if drug_data:
            status = verify_drug_on_chain(batch_id)
            expiry = drug_data.get("expiry", "Unknown")
            drug_name = drug_data.get("drugName", "Unknown")
            manufacturer = drug_data.get("manufacturer", "Unknown")
            tokenId = drug_data.get("tokenId", "Unknown")
            batchId = drug_data.get("batchId", "Unknown")
            response = (
                f"END Drug Status: {status}\n"
                f"Expiry: {expiry}\n"
                f"Drug Name: {drug_name}\n"
                f"Manufacturer: {manufacturer}\n"
                f"Token ID: {tokenId}\n"
                f"Batch ID: {batchId}"
            )
        else:
            response = "END Batch ID not found."

    logging.info(f"Response: {response}")
    return {
        "response": response,
        "sessionId": session_id
    }
