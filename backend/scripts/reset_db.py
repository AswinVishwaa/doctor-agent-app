# scripts/reset_db.py
from db.database import Base, engine
from db.models import Doctor, Patient, Appointment

# DROP ALL
Base.metadata.drop_all(bind=engine)

# RECREATE ALL
Base.metadata.create_all(bind=engine)

print("✅ All tables dropped and recreated.")
