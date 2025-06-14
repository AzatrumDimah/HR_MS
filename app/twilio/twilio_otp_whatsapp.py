# twilio_otp.py

from twilio.rest import Client
from dotenv import load_dotenv
import os

load_dotenv()

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_NUMBER = "whatsapp:+14155238886"  # Twilio sandbox WhatsApp number

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

def send_otp(phone_number: str, otp: str) -> bool:
    """
    Send an OTP message to the given phone number via WhatsApp using Twilio.
    Returns True if successful, False otherwise.
    """
    try:
        message = client.messages.create(
            body=f"🔐 Your OTP is: {otp}",
            from_=TWILIO_WHATSAPP_NUMBER,
            to=f"whatsapp:{phone_number}"
        )
        print("✅ WhatsApp Message SID:", message.sid)
        return True
    except Exception as e:
        print("❌ Failed to send WhatsApp OTP:", str(e))
        return False


if __name__ == "__main__":
    test_number = "+918500072152"  # Without 'whatsapp:' prefix, we add it in the code
    test_otp = "Hi Murtaza (WhatsApp test)"
    send_otp(test_number, test_otp)
