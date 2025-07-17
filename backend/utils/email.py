import smtplib
import os
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = os.getenv("EMAIL_PORT")
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

def send_confirmation_email(to_email, patient_name, doctor_name, slot):
    msg = EmailMessage()
    msg["Subject"] = "Your Appointment is Confirmed"
    msg["From"] = EMAIL_USER
    msg["To"] = to_email

    body = f"""
    Hi {patient_name},

    Your appointment with {doctor_name} has been confirmed for {slot}.

    Regards,
    Doctor Agent Team
    """

    msg.set_content(body)

    try:
        with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASS)
            server.send_message(msg)
            print("Email sent to", to_email)
    except Exception as e:
        print("❌ Email Error:", e)
