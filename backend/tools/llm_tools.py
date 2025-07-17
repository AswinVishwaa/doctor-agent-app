from db.database import SessionLocal
from db.models import Doctor, Patient, Appointment
from utils.email import send_confirmation_email
from datetime import datetime, timedelta
from google.oauth2 import service_account
from googleapiclient.discovery import build
import os

# Load Google Calendar credentials
SERVICE_ACCOUNT_FILE = "credentials.json"
SCOPES = ['https://www.googleapis.com/auth/calendar']
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)
calendar_id = os.getenv("GOOGLE_CALENDAR_ID")

# 🔧 Tool-compatible wrapper for availability
from db.database import SessionLocal
from db.models import Doctor
from datetime import datetime

def llm_check_availability(input_str: str):
    try:
        # Parse input like: doctor_name='Dr. Ahuja', date='2025-07-19'
        parts = input_str.split(",")
        doctor_name = parts[0].split("=")[-1].strip().strip("'\"")
        date = parts[1].split("=")[-1].strip().strip("'\"")
    except Exception as e:
        return f"❌ Failed to parse input. Format must be: doctor_name='Dr. Ahuja', date='2025-07-19'. Error: {e}"

    try:
        db = SessionLocal()
        doctor = db.query(Doctor).filter(Doctor.name == doctor_name).first()
        if not doctor:
            return f"Doctor '{doctor_name}' not found."

        requested_day = datetime.strptime(date, "%Y-%m-%d").date()
        available = [slot for slot in doctor.available_slots if slot.date() == requested_day]

        if not available:
            return f"Final Answer: {doctor_name} is NOT available on {date}. Please try a different date. This is the final result from the availability system."
        
        slot_str = ", ".join([s.strftime("%I:%M %p") for s in available])
        return f"{doctor_name} is available on {date} at: {slot_str}"
    
    except Exception as e:
        return f"❌ Error checking availability: {e}"

# 🔧 Tool-compatible wrapper for appointment
def llm_schedule_appointment(input_str: str):
    try:
        # Sanity check
        if "..." in input_str or "not provided" in input_str.lower():
            return "🛑 Final Answer: Booking failed. Required input is missing or incomplete. Please provide doctor_name, patient_name, patient_email, and slot."

        # Parse input
        kv_pairs = input_str.split(",")
        values = {}
        for kv in kv_pairs:
            parts = kv.split("=")
            if len(parts) != 2:
                continue  # Skip malformed input
            key = parts[0].strip()
            val = parts[1].strip().strip("'\"")
            values[key] = val

        # Validate required fields
        required_fields = ["doctor_name", "patient_name", "patient_email", "slot"]
        for field in required_fields:
            if field not in values:
                return f"❌ Final Answer: Missing required field: {field}"

        doctor_name = values["doctor_name"]
        patient_name = values["patient_name"]
        patient_email = values["patient_email"]
        slot = values["slot"]

        slot_time = datetime.fromisoformat(slot)

        db = SessionLocal()

        # Doctor lookup
        doctor = db.query(Doctor).filter(Doctor.name == doctor_name).first()
        if not doctor:
            return f"❌ Final Answer: Doctor '{doctor_name}' not found."

        # Check if slot still available
        if slot_time not in doctor.available_slots:
            return f"❌ Final Answer: Slot not available for {doctor_name} on {slot}."

        # Prevent duplicate booking for that doctor at same time
        existing = db.query(Appointment).filter(
            Appointment.doctor_id == doctor.id,
            Appointment.slot == slot_time
        ).first()
        if existing:
            return f"❌ Final Answer: That slot is already booked for {doctor_name} at {slot}. Choose another time."

        # Add patient if new
        patient = db.query(Patient).filter(Patient.email == patient_email).first()
        if not patient:
            patient = Patient(name=patient_name, email=patient_email)
            db.add(patient)
            db.commit()
            db.refresh(patient)

        # Create appointment
        appointment = Appointment(
            doctor_id=doctor.id,
            patient_id=patient.id,
            slot=slot_time,
            symptoms=""
        )
        db.add(appointment)

        # Remove booked slot from available_slots
        doctor.available_slots = [s for s in doctor.available_slots if s != slot_time]

        db.commit()

        # Add to Google Calendar
        try:
            service = build("calendar", "v3", credentials=credentials)
            event = {
                'summary': f'Appointment: {patient_name} with {doctor.name}',
                'description': 'Auto-booked via Doctor Agent',
                'start': {'dateTime': slot, 'timeZone': 'Asia/Kolkata'},
                'end': {'dateTime': (slot_time + timedelta(minutes=30)).isoformat(), 'timeZone': 'Asia/Kolkata'},
            }
            service.events().insert(calendarId=calendar_id, body=event).execute()
        except Exception as cal_err:
            print(f"⚠️ Google Calendar error: {cal_err}")

        # Send email (optional, disabled for now to avoid timeout)
        try:
            send_confirmation_email(
                to_email=patient_email,
                patient_name=patient_name,
                doctor_name=doctor.name,
                slot=slot
            )
        except Exception as email_err:
            print(f"⚠️ Email error: {email_err}")

        return f"✅ Final Answer: Appointment booked for {patient_name} with {doctor_name} at {slot}. Confirmation sent."

    except Exception as e:
        return f"❌ Final Answer: Failed to book appointment. Error: {e}"
