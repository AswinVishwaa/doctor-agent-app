from db.database import SessionLocal
from db.models import Appointment
from datetime import datetime, timedelta
import os
import requests
from dotenv import load_dotenv

load_dotenv()
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

def send_to_slack(message: str):
    if not SLACK_WEBHOOK_URL:
        print("⚠️ Slack webhook URL not set.")
        return

    try:
        payload = {"text": message}
        response = requests.post(SLACK_WEBHOOK_URL, json=payload)
        if response.status_code != 200:
            print(f"❌ Slack error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Slack send failed: {e}")

def generate_doctor_summary(input_str: str):
    try:
        db = SessionLocal()
        now = datetime.now()
        today = now.date()
        yesterday = today - timedelta(days=1)

        input_str = input_str.lower()

        if "today" in input_str and "appointment" in input_str:
            appointments = db.query(Appointment).filter(
                Appointment.slot >= datetime.combine(today, datetime.min.time()),
                Appointment.slot <= datetime.combine(today, datetime.max.time())
            ).all()
            message = f"📅 You have {len(appointments)} appointments today."
            send_to_slack(message)
            return message

        elif "yesterday" in input_str and "appointment" in input_str:
            appointments = db.query(Appointment).filter(
                Appointment.slot >= datetime.combine(yesterday, datetime.min.time()),
                Appointment.slot <= datetime.combine(yesterday, datetime.max.time())
            ).all()
            message = f"📅 You had {len(appointments)} appointments yesterday."
            send_to_slack(message)
            return message

        elif "fever" in input_str:
            appointments = db.query(Appointment).filter(
                Appointment.symptoms.ilike('%fever%')
            ).all()
            message = f"🤒 You have {len(appointments)} patients reporting fever symptoms."
            send_to_slack(message)
            return message

        elif "cough" in input_str:
            appointments = db.query(Appointment).filter(
                Appointment.symptoms.ilike('%cough%')
            ).all()
            message = f"😷 You have {len(appointments)} patients reporting cough symptoms."
            send_to_slack(message)
            return message

        else:
            return "🤖 Sorry, I didn't understand the report type. Try phrases like 'appointments today' or 'fever patients'."

    except Exception as e:
        return f"❌ Failed to generate report: {str(e)}"
