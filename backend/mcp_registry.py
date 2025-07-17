from langchain.tools import Tool
from tools import availability

def check_availability_tool():
    def _check(query):
        import requests
        params = {"doctor_name": "Dr. Ahuja", "date": "2025-07-17"}  # Dummy for now, agent will replace
        response = requests.get("http://localhost:8000/check_availability", params=params)
        return response.json()

    return Tool(
        name="CheckAvailability",
        func=_check,
        description="Use this to check if a doctor is free on a given date. Input: natural language with doctor name and date."
    )

def schedule_appointment_tool():
    def _book(query):
        import requests
        params = {
            "doctor_name": "Dr. Ahuja",
            "patient_name": "Aswin",
            "patient_email": "aswinvishwaa@gmail.com",
            "slot": "2025-07-17T10:00:00",
        }
        response = requests.post("http://localhost:8000/schedule_appointment", params=params)
        return response.json()

    return Tool(
        name="ScheduleAppointment",
        func=_book,
        description="Book an appointment with a doctor at a given time. Input: doctor name, patient name, email, slot."
    )
