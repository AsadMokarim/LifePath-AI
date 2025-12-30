# LifePath AI  
### An Agentic Personal Productivity Assistant

LifePath AI is an AI-powered productivity agent that helps users plan their day, manage tasks, schedule time intelligently, and reflect on execution. Unlike traditional productivity tools, LifePath AI acts as an **agent** that reasons over user goals, uses tools, maintains context, and performs self-reflection.

---

## 🚀 Problem Statement

Managing daily tasks and schedules is fragmented and manual. Existing productivity tools are largely static and rule-based, lacking intelligent reasoning, contextual memory, and adaptability. There is a need for an AI-driven productivity agent that understands natural language goals, orchestrates actions, and adapts dynamically.

---

## 💡 Solution Overview

LifePath AI is a **single agentic system** that:
- Understands natural language user goals
- Converts them into actionable tasks and schedules
- Uses tools such as task memory and calendar scheduling
- Reflects on its own execution
- Exposes internal context transparently via MCP

---

## 🧠 Key Features

- **Intelligent Goal Understanding**  
  Uses Gemini LLM to interpret natural language user intent.

- **Smart Scheduling & Tool Orchestration**  
  Extracts time and duration from user input and schedules tasks using a calendar tool.

- **Task Memory Management**  
  Stores and retrieves tasks using persistent JSON-based memory.

- **Agent Self-Reflection**  
  Evaluates whether all planned steps were completed successfully and suggests corrective actions.

- **MCP Context Exposure**  
  Exposes agent state, memory, and reasoning through an MCP-style endpoint for transparency.

---

## 🏗️ System Architecture

User / UI
   ↓
Flask API
   ↓
AI Agent (Gemini)
   ↓
Intent Detection & Time Extraction
   ↓
Tool Orchestration
   ↙          ↘
Task Memory   Calendar Scheduler
   ↓
Agent Self-Reflection
   ↓
MCP Context Exposure




---

## 🔍 Implementation Details

- **LLM**: Gemini API is used for intent detection, reasoning, and structured time extraction.
- **Backend**: Flask serves as the agent entry point and API layer.
- **Tools**:
  - Task Tool: JSON-based persistent memory
  - Calendar Tool: Mock Google Calendar-style scheduler
- **Self-Reflection**:
  - Agent verifies whether intended steps were completed
  - Reflects on failures and suggests next actions
- **MCP**:
  - Exposes agent context, memory, and reasoning via `/mcp/context`

---

## 🔄 User Journey

1. User sends a natural language request (e.g., “Schedule a 2-hour coding session after lunch”)
2. Agent detects intent and extracts time information
3. Agent orchestrates task or calendar tools
4. Action is executed and stored in memory
5. Agent performs self-reflection on execution
6. Agent state is exposed via MCP

---

## 📡 API Endpoints

| Endpoint | Method | Description |
|--------|--------|-------------|
| `/chat` | POST | Interact with the AI agent |
| `/tasks` | GET | Retrieve stored tasks |
| `/calendar` | GET | Retrieve scheduled events |
| `/mcp/context` | GET | Expose agent context (MCP) |

---

## 🛠️ Tech Stack

- **Backend**: Python, Flask  
- **LLM**: Google Gemini (`google-generativeai`)  
- **Memory**: JSON-based storage  
- **Agent Design**: Google ADK (conceptual alignment)  
- **Protocol**: Model Context Protocol (MCP-style)  

---

## 🔮 Future Evolutions

- Real Google Calendar API integration
- Personalized scheduling based on user behavior
- Multi-agent collaboration (planner, reviewer, notifier)
- Advanced observability using tools like Langfuse or Arize Phoenix
- Full frontend dashboard integration

---

## 🏁 Conclusion

LifePath AI demonstrates how productivity tools can evolve into **agentic AI systems** that reason, act, and reflect. The project showcases core principles of modern AI agents—tool orchestration, context awareness, and self-reflection—within a scalable and extensible architecture.

---

## 📹 Demo

A short video demonstrating the complete user journey, data flow, and agent behavior is included in the submission.

---

## 👤 Author

**Mohammad Asad Mokarim**  
Hackathon Project Submission
