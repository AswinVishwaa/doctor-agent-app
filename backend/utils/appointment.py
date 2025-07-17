from db.database import SessionLocal
from db.models import Doctor, Patient, Appointment
from utils.email import send_confirmation_email
from googleapiclient.discovery import build
from datetime import datetime, timedelta
import os

def book_appointment(doctor_name, patient_name, patient_email, slot, credentials, calendar_id):
    if not calendar_id:
        raise ValueError("Google Calendar ID is not configured")
    db = SessionLocal()
    try:
        slot_time = datetime.fromisoformat(slot)
        doctor = db.query(Doctor).filter(Doctor.name == doctor_name).first()
        if not doctor:
            raise ValueError(f"Doctor '{doctor_name}' not found")
        
        if slot_time not in doctor.available_slots:
            raise ValueError(f"Slot not available for {doctor_name} on {slot}")
        
        patient = db.query(Patient).filter(Patient.email == patient_email).first()
        if not patient:
            patient = Patient(name=patient_name, email=patient_email)
            db.add(patient)
            db.commit()
            db.refresh(patient)
        
        appointment = Appointment(
            doctor_id=doctor.id,
            patient_id=patient.id,
            slot=slot_time,
            symptoms=""
        )
        db.add(appointment)
        doctor.available_slots = [s for s in doctor.available_slots if s != slot_time]
        
        service = build("calendar", "v3", credentials=credentials)
        event = {
            'summary': f'Appointment: {patient_name} with {doctor.name}',
            'description': 'Auto-booked via Doctor Agent',
            'start': {'dateTime': slot, 'timeZone': 'Asia/Kolkata'},
            'end': {'dateTime': (slot_time + timedelta(minutes=30)).isoformat(), 'timeZone': 'Asia/Kolkata'},
        }
        service.events().insert(calendarId=calendar_id, body=event).execute()
        
        send_confirmation_email(to_email=patient_email, patient_name=patient_name, doctor_name=doctor.name, slot=slot)
        
        db.commit()
        return f"Appointment booked for {patient_name} with Dr. {doctor_name} at {slot}. Confirmation sent."
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()