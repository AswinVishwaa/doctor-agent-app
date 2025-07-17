from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from db.database import SessionLocal
from db.models import Doctor, Patient, Appointment

def seed():
    db: Session = SessionLocal()

    # Define doctors
    doctor_data = [
        {
            "name": "Dr. Ahuja",
            "specialty": "Cardiology",
            "slots": [0, 1],  # today, tomorrow
        },
        {
            "name": "Dr. Patel",
            "specialty": "Dermatology",
            "slots": [1, 2],  # tomorrow, day after
        },
        {
            "name": "Dr. Khan",
            "specialty": "General Physician",
            "slots": [0, 2],  # today, day after
        },
    ]

    doctors = {}
    for d in doctor_data:
        existing = db.query(Doctor).filter(Doctor.name == d["name"]).first()
        if existing:
            doctors[d["name"]] = existing
            print(f"ℹ️ {d['name']} already exists.")
            continue

        now = datetime.now().replace(minute=0, second=0, microsecond=0)
        slots = []
        for offset in d["slots"]:
            slots.append(now + timedelta(days=offset, hours=10))
            slots.append(now + timedelta(days=offset, hours=11))

        doctor = Doctor(
            name=d["name"],
            specialty=d["specialty"],
            available_slots=slots
        )
        db.add(doctor)
        db.commit()
        db.refresh(doctor)
        doctors[d["name"]] = doctor
        print(f"✅ Seeded {d['name']} with slots")

    # Define patients
    patient_data = [
        {"name": "Aswin", "email": "aswin@example.com"},
        {"name": "John Doe", "email": "john@example.com"},
        {"name": "Alice", "email": "alice@example.com"},
        {"name": "Bob", "email": "bob@example.com"},
    ]

    patients = {}
    for p in patient_data:
        existing = db.query(Patient).filter(Patient.email == p["email"]).first()
        if existing:
            patients[p["email"]] = existing
            print(f"ℹ️ Patient {p['name']} exists.")
            continue

        patient = Patient(name=p["name"], email=p["email"])
        db.add(patient)
        db.commit()
        db.refresh(patient)
        patients[p["email"]] = patient
        print(f"✅ Seeded patient {p['name']}")

    # Appointments (some today, some yesterday)
    now = datetime.now()
    yesterday = now - timedelta(days=1)

    appointments = [
        {
            "doctor": "Dr. Ahuja",
            "patient": "john@example.com",
            "slot": now.replace(hour=10, minute=0, second=0, microsecond=0),
            "symptoms": "fever",
        },
        {
            "doctor": "Dr. Patel",
            "patient": "alice@example.com",
            "slot": now.replace(hour=11, minute=0, second=0, microsecond=0),
            "symptoms": "rash",
        },
        {
            "doctor": "Dr. Khan",
            "patient": "bob@example.com",
            "slot": yesterday.replace(hour=9, minute=0, second=0, microsecond=0),
            "symptoms": "cough",
        },
        {
            "doctor": "Dr. Ahuja",
            "patient": "aswin@example.com",
            "slot": yesterday.replace(hour=11, minute=0, second=0, microsecond=0),
            "symptoms": "headache",
        },
    ]

    for appt in appointments:
        doctor = doctors[appt["doctor"]]
        patient = patients[appt["patient"]]
        slot = appt["slot"]

        exists = db.query(Appointment).filter(
            Appointment.doctor_id == doctor.id,
            Appointment.slot == slot
        ).first()
        if exists:
            print(f"ℹ️ Appointment already exists at {slot}")
            continue

        appointment = Appointment(
            doctor_id=doctor.id,
            patient_id=patient.id,
            slot=slot,
            symptoms=appt["symptoms"]
        )
        db.add(appointment)

        # Remove slot from available_slots if exists
        doctor.available_slots = [s for s in doctor.available_slots if s != slot]

    db.commit()
    db.close()
    print("✅ All mock data seeded!")

if __name__ == "__main__":
    seed()
