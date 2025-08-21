from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import logging

app = FastAPI()

# Enable CORS (optional but useful)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Basic logging
logging.basicConfig(level=logging.INFO)

@app.get("/")
def health_check():
    logging.info("Health check pinged.")
    return {"status": "ok"}

@app.post("/ussd")
async def ussd_handler(request: Request):
    data = await request.form()
    session_id = data.get("sessionId")
    phone_number = data.get("phoneNumber")
    text = data.get("text")

    logging.info(f"USSD request received: {data}")

    # Sample USSD logic
    if text == "":
        response = "CON Welcome to Shuaibu's USSD App\n1. Check Balance\n2. Buy Airtime"
    elif text == "1":
        response = "END Your balance is ₦1,500"
    elif text == "2":
        response = "END Airtime purchase successful"
    else:
        response = "END Invalid option"

    return response
