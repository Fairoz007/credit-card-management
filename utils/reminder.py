
from twilio.rest import Client

def send_payment_reminder(phone_number, card_name, due_date):
    client = Client("TWILIO_SID", "TWILIO_AUTH_TOKEN")
    message = f"Reminder: Your credit card {card_name} bill is due on {due_date}."
    client.messages.create(to=phone_number, from_="TWILIO_PHONE_NUMBER", body=message)
