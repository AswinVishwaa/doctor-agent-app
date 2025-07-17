from langchain.agents import initialize_agent, Tool
from langchain.agents.agent_types import AgentType
from langchain.memory import ConversationBufferMemory
from langchain_groq import ChatGroq 
import os
from tools.reports import generate_doctor_summary
from tools.schedule import schedule_appointment
from tools.availability import check_availability
from tools.llm_tools import llm_schedule_appointment, llm_check_availability

# Setup LLM
llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama3-70b-8192"
)

# user input fallback tool
def ask_user(prompt: str):
    return prompt

# List of tools for the agent
tools = [
    Tool(
        name="check_doctor_availability",
        func=llm_check_availability,
        description=(
            "Use this to check if a doctor is available on a specific date. "
            "Input format: doctor_name='Dr. Ahuja', date='2025-07-20'. "
            "Use this before booking."
        )
    ),
    Tool(
        name="doctor_summary",
        func=generate_doctor_summary,
        description="Use this to get doctor report summaries like number of appointments today, yesterday, or patients with symptoms like fever. Input: natural language like 'appointments today'."
    ),
    Tool(
        name="schedule_appointment",
        func=llm_schedule_appointment,
        description=(
            "Use this to directly book an appointment. Required inputs: "
            "doctor_name, patient_name, patient_email, and slot (in ISO format like '2025-07-19T10:00:00'). "
            "Only use when all values are confirmed."
        )
    ),
    Tool(
        name="confirm_and_book",
        func=llm_schedule_appointment,
        description=(
            "Use this when the user says 'Book that slot for me' or 'Confirm the appointment'. "
        "Only call this if you already know all the following from previous messages:\n"
        "- doctor_name (e.g., 'Dr. Ahuja')\n"
        "- patient_name (e.g., 'Aswin')\n"
        "- patient_email (e.g., 'aswin@gmail.com')\n"
        "- slot (e.g., '2025-07-21T10:00:00')\n"
        "Input must be in format: doctor_name='Dr. Ahuja', patient_name='Aswin', patient_email='aswin@gmail.com', slot='2025-07-21T10:00:00'"
        )
    ),
    Tool(
        name="ask_user",
        func=ask_user,
        description=(
            "Use this to ask the user for missing details like doctor name, patient name, email, or date. "
            "Use only when information is clearly missing and no previous slot/date is known."
        )
    ),
    Tool(
    name="doctor_summary",
    func=generate_doctor_summary,
    description="Use this to get doctor report summaries like appointments today, patients with fever..."
)
]


#  Function that accepts memory and returns the agent
def build_agent(memory: ConversationBufferMemory, role: str = "patient"):
    allowed_tools = tools  # default: all tools

    if role == "doctor":
        allowed_tools = [t for t in tools if t.name in ["doctor_summary", "ask_user"]]
    elif role == "patient":
        allowed_tools = [t for t in tools if t.name != "doctor_summary"]
    return initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        memory=memory,
        verbose=True,
        return_intermediate_steps=False,
        handle_parsing_errors=True,
        max_iterations=7,
    )
