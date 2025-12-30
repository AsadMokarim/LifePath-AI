from flask import Flask, request, jsonify, redirect, render_template
from dotenv import load_dotenv


from agent.llm import ask_gemini
from tools.task_tool import get_tasks
from tools.calendar_tool import get_events
from agent.agent_logic import handle_user_message

from agent.agent_logic import AGENT_CONTEXT





# Load environment variables from .env
load_dotenv()

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return render_template('index1.html')

@app.route("/chat", methods=["POST"])
def chat():
    """
    Main chat endpoint
    Input: { "message": "Schedule a 2-hour coding session after lunch" }
    Output: AI response
    """
    
    if request.method == "POST":
        # Read the textarea named 'chat_data' directly from the form
        user_message = request.form.get("chat_data", "")

    if not user_message:
        return jsonify({"error": "Message is required"}), 400

    response_text = handle_user_message(user_message)
    return jsonify({"response": response_text})



@app.route("/mcp/context", methods=["GET"])
def mcp_context():
    """
    Model Context Protocol endpoint.
    Exposes agent state, memory, and reasoning.
    """
    return jsonify({
        "agent": "AI Productivity Agent",
        "framework": "Google ADK (conceptual)",
        "context": AGENT_CONTEXT,
        "memory": {
            "tasks": get_tasks(),
            "calendar_events": get_events()
        },
        "capabilities": [
            "Intent detection",
            "Tool orchestration",
            "Time extraction",
            "Agent self-reflection",
            "User productivity reflection"
        ]
    })




@app.route("/tasks", methods=["GET"])
def list_tasks():
    return jsonify(get_tasks())


@app.route("/calendar", methods=["GET"])
def view_calendar():
    return jsonify(get_events())



if __name__ == "__main__":
    app.run(debug=True, port=8000)
