from fastapi import APIRouter, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime
from db.database import get_db
from db.models import Doctor
from fastapi import Depends 

router = APIRouter()

@router.get("/check_availability")
def check_availability(doctor_name: str = Query(...),
    date: str = Query(...),
    db: Session = Depends(get_db)):
    try:
        doctor = db.query(Doctor).filter(Doctor.name == doctor_name).first()
        if not doctor:
            raise HTTPException(status_code=404, detail="Doctor not found")

        requested_day = datetime.strptime(date, "%Y-%m-%d").date()
        available = [slot for slot in doctor.available_slots if slot.date() == requested_day]
        if not available:
            return f"Dr. {doctor_name} has no available slots on {date}."
        else:
            slot_str = ", ".join([s.strftime("%I:%M %p") for s in available])
            return f"Dr. {doctor_name} is available on {date} at: {slot_str}"
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
