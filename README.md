# 🧠 Doctor Assistant Agent (LLM + MCP Integration)

A smart doctor appointment and reporting assistant built using LangChain + Groq, FastAPI, PostgreSQL, React, and the Model Context Protocol (MCP). This project showcases agentic workflows like booking appointments, generating summary reports, sending email and Slack notifications — all via natural language.

---

## 🚀 Features

- 📅 Book doctor appointments using plain English.
- 📊 Doctors can request summary reports (e.g. "appointments today", "patients with fever").
- 💌 Email notifications sent to patients after booking.
- 🔔 Slack notifications sent to doctors with daily summaries.
- 🧠 Context-aware multi-turn chat with memory.
- 📦 PostgreSQL database (via Docker) with seed data.
- 🌐 Google Calendar integration for auto-syncing appointments.
- 🧑‍⚕️ Doctor/Patient role toggle (no login required).

---

## 🛠️ Tech Stack

- **Frontend**: React (Vite)
- **Backend**: FastAPI
- **Database**: PostgreSQL (Dockerized)
- **LLM Agent**: LangChain + Groq (LLaMA3)
- **Notifications**: Gmail SMTP, Slack Incoming Webhook
- **Calendar API**: Google Calendar
- **Session Memory**: LangChain's `ConversationBufferMemory`

---

## 📦 Setup Instructions

### 1. Clone the repo

git clone https://github.com/your-username/doctor-assistant-agent.git
cd doctor-assistant-agent

### 2. Start PostgreSQL (Docker)

docker-compose up -d

### 3. Backend Setup

cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows


# Create tables & seed mock data

python -c "from db.database import Base, engine; import db.models; Base.metadata.create_all(bind=engine)"
python scripts/seed_mock_data.py

### 4. Environment Variables

Create .env in backend/:

env

DATABASE_URL=postgresql://doctor:doctorpass@localhost:5432/doctorai
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USER=your_email@gmail.com
EMAIL_PASS=your_app_password
GOOGLE_CALENDAR_ID=your_calendar_id
GROQ_API_KEY=your_groq_key
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/your/webhook/url
Add your credentials.json for Google Calendar in backend/.

### 5. Start Backend Server

uvicorn main:app --reload

### 6. Frontend Setup

cd frontend
npm install
npm run dev

## 🧪 Sample Prompts
### 👨‍⚕️ Doctor Role
- “How many appointments today?”

- “How many patients had fever yesterday?”

- “How many appointments do I have tomorrow?”

### 👩‍💼 Patient Role
- “Book an appointment with Dr. Ahuja tomorrow at 10AM.”

- “Check if Dr. Patel is available at 11 AM.”

- “Book the 11AM slot for me.”

## 📬 API Endpoints
Endpoint	Method	Description
/chat	POST	Main agent endpoint (LLM + memory)
/check_availability	GET	MCP tool: doctor availability
/schedule_appointment	POST	MCP tool: book appointment

## 📸 Screenshots

✅ Chat UI with prompt: “Book with Dr. Ahuja…”

✅ Agent response

✅ Email confirmation in inbox (optional)

✅ Slack message with summary

## 🎥 Demo Video evaluation folder

✅ Agent response

## ✅ Status
✔️ Core features completed
✔️ Bonus: Slack, Email, Calendar integration
✔️ Dockerized DB with seed script
⚠️ **Known: Occasional LLM hallucination due to natural language complexity**

📄 License
MIT — free to use and modify.

Built with 💡 and LLMs for the FSE Internship Assignment (Agentic AI + MCP).

---



