import React, { useState } from "react";
import axios from "axios";

const ChatPage = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [role, setRole] = useState("patient");
  const [loading, setLoading] = useState(false);

  const session_id = "aswin-session-001";

  const sendQuery = async () => {
    if (!input.trim()) return;

    const newUserMessage = { role: "user", content: input };
    setMessages((prev) => [...prev, newUserMessage]);
    setLoading(true);

    try {
      const res = await axios.post("http://localhost:8000/chat", {
        query: input,
        session_id: session_id,
        role: role,
      });

      const response = res.data?.response?.output || "🤖 No reply from agent.";
      const newBotMessage = { role: "bot", content: response };
      setMessages((prev) => [...prev, newBotMessage]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { role: "bot", content: "❌ Error: " + err.message },
      ]);
    }

    setInput("");
    setLoading(false);
  };

  const handleKey = (e) => {
    if (e.key === "Enter" && !loading) sendQuery();
  };

  return (
    <div
      style={{
        maxWidth: 700,
        margin: "60px auto",
        fontFamily: "'Segoe UI', sans-serif",
        padding: 20,
        background: "#fff",
        borderRadius: 12,
        boxShadow: "0 8px 24px rgba(0,0,0,0.1)",
      }}
    >
      <h2 style={{ textAlign: "center", marginBottom: 20 }}>🧠 Doctor Assistant Agent</h2>

      {/* Role Selector */}
      <div style={{ marginBottom: 15, textAlign: "center" }}>
        <label style={{ fontWeight: 500, marginRight: 8 }}>Select Role:</label>
        <select
          value={role}
          onChange={(e) => setRole(e.target.value)}
          style={{
            padding: "6px 12px",
            borderRadius: 6,
            border: "1px solid #ccc",
            fontSize: 14,
          }}
        >
          <option value="patient">Patient</option>
          <option value="doctor">Doctor</option>
        </select>
      </div>

      {/* Chat Box */}
      <div
        style={{
          border: "1px solid #e0e0e0",
          borderRadius: 10,
          padding: 15,
          height: 400,
          overflowY: "auto",
          backgroundColor: "#fafafa",
          marginBottom: 20,
        }}
      >
        {messages.map((msg, idx) => (
          <div
            key={idx}
            style={{
              display: "flex",
              justifyContent: msg.role === "user" ? "flex-end" : "flex-start",
              marginBottom: 10,
            }}
          >
            <div
              style={{
                backgroundColor: msg.role === "user" ? "#d0ebff" : "#e9ecef",
                padding: "10px 14px",
                borderRadius: "14px",
                maxWidth: "75%",
                fontSize: 15,
                whiteSpace: "pre-wrap",
              }}
            >
              {msg.content}
            </div>
          </div>
        ))}
        {loading && (
          <div style={{ fontStyle: "italic", color: "#666" }}>
            Agent is thinking...
          </div>
        )}
      </div>

      {/* Input Row */}
      <div style={{ display: "flex", alignItems: "center" }}>
        <input
          type="text"
          placeholder="Type your message..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKey}
          style={{
            flex: 1,
            padding: "12px 14px",
            fontSize: 15,
            borderRadius: 6,
            border: "1px solid #ccc",
            marginRight: 10,
          }}
        />
        <button
          onClick={sendQuery}
          disabled={loading}
          style={{
            padding: "12px 20px",
            backgroundColor: "#007bff",
            color: "white",
            border: "none",
            borderRadius: 6,
            fontWeight: "bold",
            cursor: loading ? "not-allowed" : "pointer",
          }}
        >
          Send
        </button>
      </div>
    </div>
  );
};

export default ChatPage;
