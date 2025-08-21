import os
from hedera import Client, AccountId, PrivateKey
from dotenv import load_dotenv

load_dotenv()

account_id_str = os.getenv("HEDERA_ACCOUNT_ID")
private_key_str = os.getenv("HEDERA_PRIVATE_KEY")

if not account_id_str or not private_key_str:
    raise ValueError("Missing Hedera credentials")

OPERATOR_ID = AccountId.fromString(account_id_str)
OPERATOR_KEY = PrivateKey.fromString(private_key_str)

client = Client.forTestnet()
client.setOperator(OPERATOR_ID, OPERATOR_KEY)

def verify_drug_on_chain(batch_id):
    # Simulated logic — replace with Hedera SDK calls
    if batch_id.startswith("GEN"):
        return "Genuine"
    return "Fake"
