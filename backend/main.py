from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from langchain.memory import ConversationBufferMemory
from langchain.memory.chat_message_histories import ChatMessageHistory
from agent.agent import build_agent

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
SESSION_STORE = {}
@app.post("/chat")
async def chat(request: Request):
    body = await request.json()
    query = body.get("query")
    session_id = body.get("session_id", "default")
    role = body.get("role", "patient")

    if not query:
        return {"error": "Missing query"}

    # Restore history
    if session_id not in SESSION_STORE:
        SESSION_STORE[session_id] = ChatMessageHistory()

    history = SESSION_STORE[session_id]

    # Attach history to memory
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
        output_key="output",
        chat_memory=history
    )

    agent = build_agent(memory,role)

    result = agent.invoke({"input": query})

    return {"response": result}
