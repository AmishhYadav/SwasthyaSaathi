from twilio.rest import Client
import os

account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
twilio_number = os.getenv("TWILIO_PHONE_NUMBER")  # For SMS
twilio_whatsapp = "whatsapp:" + os.getenv("TWILIO_WHATSAPP_NUMBER")  # For WhatsApp

client = Client(account_sid, auth_token)

def send_sms(to, message):
    client.messages.create(
        body=message,
        from_=twilio_number,
        to=to
    )

def send_whatsapp(to, message):
    client.messages.create(
        body=message,
        from_=twilio_whatsapp,
        to="whatsapp:" + to
    )
