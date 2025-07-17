from datetime import datetime
from sqlalchemy.orm import Session
from db.database import SessionLocal
from db.models import Doctor, Patient

def seed():
    db: Session = SessionLocal()

    # Check if doctor already exists
    existing = db.query(Doctor).filter(Doctor.name == "Dr. Ahuja").first()
    if existing:
        print("✅ Dr. Ahuja already seeded.")
        return

    # Doctor data
    doctor = Doctor(
        name="Dr. Ahuja",
        specialty="Cardiology",
        available_slots=[
            datetime.fromisoformat("2025-07-25T10:00:00"),
            datetime.fromisoformat("2025-07-25T11:00:00"),
            datetime.fromisoformat("2025-07-26T10:00:00"),
            datetime.fromisoformat("2025-07-28T09:30:00")
        ]
    )

    db.add(doctor)

    # Optional: Add a patient
    patient = Patient(
        name="Aswin",
        email="aswinvishwaa@gmail.com"
    )
    db.add(patient)

    db.commit()
    db.close()
    print("✅ Mock data seeded successfully.")

if __name__ == "__main__":
    seed()
