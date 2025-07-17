from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy.orm import Session
from db.database import get_db
from db.models import Doctor, Patient, Appointment
from datetime import datetime, timedelta
import uuid
import os
import google.auth
from google.oauth2 import service_account
from googleapiclient.discovery import build
from utils.email import send_confirmation_email

router = APIRouter()

# Load Google credentials
SERVICE_ACCOUNT_FILE = "credentials.json"
SCOPES = ['https://www.googleapis.com/auth/calendar']
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

calendar_id = os.getenv("GOOGLE_CALENDAR_ID")  # Must share with service account

@router.post("/schedule_appointment")
def schedule_appointment(
    doctor_name: str = Query(...),
    patient_name: str = Query(...),
    patient_email: str = Query(...),
    slot: str = Query(...),  # ISO string: "2025-07-17T10:00:00"
    db: Session = Depends(get_db)
):
    slot_time = datetime.fromisoformat(slot)
    doctor = db.query(Doctor).filter(Doctor.name == doctor_name).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    if slot_time not in doctor.available_slots:
        raise HTTPException(status_code=400, detail="Slot not available")

    # Insert patient if new
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
    doctor.available_slots.remove(slot_time)  # Remove booked slot
    db.commit()

    # Add to Google Calendar
    service = build("calendar", "v3", credentials=credentials)
    event = {
        'summary': f'Appointment: {patient_name} with {doctor.name}',
        'description': f'Auto-booked via Doctor Agent',
        'start': {'dateTime': slot, 'timeZone': 'Asia/Kolkata'},
        'end': {'dateTime': (slot_time + timedelta(minutes=30)).isoformat(), 'timeZone': 'Asia/Kolkata'},
    }
    print("Inserting event into calendar:", calendar_id)
    print("Event payload:", event)

    try:
        service.events().insert(calendarId=calendar_id, body=event).execute()
        send_confirmation_email(
    to_email=patient_email,
    patient_name=patient_name,
    doctor_name=doctor.name,
    slot=slot
)
        return f"Appointment booked for {patient_name} with Dr. {doctor_name} at {slot}. Confirmation sent."
    except Exception as e:
        print("Calendar Error:", e)
    raise HTTPException(status_code=500, detail="Calendar insert failed")
