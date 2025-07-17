from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from db.database import get_db
from db.models import Appointment

router = APIRouter()

@router.post("/update_symptoms")
def update_symptoms(appointment_id: int, symptoms: str, db: Session = Depends(get_db)):
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    appointment.symptoms = symptoms
    db.commit()
    return {"message": f"Symptoms updated for appointment {appointment_id}"}