# twilio_otp.py

from twilio.rest import Client
from dotenv import load_dotenv
import os

load_dotenv()

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")  # e.g., 'whatsapp:+14155238886' or just SMS number

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

def send_otp(phone_number: str, otp: str) -> bool:
    """
    Send an OTP message to the given phone number using Twilio.
    Returns True if successful, False otherwise.
    """
    try:
        message = client.messages.create(
            body=f"🔐 Your OTP is: {otp}",
            from_=TWILIO_PHONE_NUMBER,
            to=phone_number
        )
        print("✅ Message SID:", message.sid)
        return True
    except Exception as e:
        print("❌ Failed to send OTP:", str(e))
        return False


# Run this for testing purposes
if __name__ == "__main__":
    test_number = "+918500072152"  # Replace or set in .env
    test_otp = "Hi Murtaza"
    send_otp(test_number, test_otp)
