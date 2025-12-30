# from agent.llm import ask_gemini
# from tools.task_tool import add_task, get_tasks
# from tools.calendar_tool import schedule_event
# from datetime import datetime


# def decide_intent(user_message: str) -> str:
#     """
#     Decide what the user wants to do.
#     Very simple intent detection.
#     """
#     message = user_message.lower()

#     if ("task" in message or "todo" in message) and "add" in message:
#         return "add_task"

#     if "schedule" in message or "calendar" in message:
#         return "schedule_event"

#     if "show" in message and "task" in message:
#         return "show_tasks"

#     return "chat"


# def handle_user_message(user_message: str) -> str:
#     """
#     Main agent function.
#     """
#     intent = decide_intent(user_message)

#     # 1️⃣ ADD TASK
#     if intent == "add_task":
#         task = add_task(title=user_message)
#         return f"✅ Task added: {task['title']}"

#     # 2️⃣ SHOW TASKS
#     if intent == "show_tasks":
#         tasks = get_tasks()
#         if not tasks:
#             return "📭 You have no tasks."
        
#         response = "📋 Your tasks:\n"
#         for i, task in enumerate(tasks, start=1):
#             response += f"{i}. {task['title']} ({task['status']})\n"
#         return response

#     # 3️⃣ SCHEDULE EVENT
#     if intent == "schedule_event":
#         # Simple default: now + 1 hour, duration 2 hours
#         start_time = datetime.now()
#         duration = 120 #take input from user

#         result = schedule_event(
#             title=user_message,
#             start_time=start_time,
#             duration_minutes=duration
#         )

#         if result["success"]:
#             return f"📅 Event scheduled successfully!"
#         else:
#             return f"❌ {result['message']}"

#     # 4️⃣ NORMAL CHAT
#     return ask_gemini(user_message)








from agent.llm import ask_gemini
from tools.task_tool import add_task, get_tasks
from tools.calendar_tool import schedule_event
from datetime import datetime



# Simple in-memory context for MCP
AGENT_CONTEXT = {
    "last_user_message": None,
    "last_intent": None,
    "last_agent_reflection": None
}


def decide_intent(user_message: str) -> str:
    """
    Uses Gemini to classify user intent.
    Returns one of:
    add_task, show_tasks, schedule_event, chat
    """

    prompt = f"""
You are an AI intent classifier for a productivity assistant.

Classify the user message into ONE of these intents:
- add_task
- show_tasks
- schedule_event
- chat

User message:
\"\"\"{user_message}\"\"\"

Respond with ONLY the intent name.
"""

    intent = ask_gemini(prompt).strip().lower()

    # Safety fallback
    valid_intents = ["add_task", "show_tasks", "schedule_event", "chat"]
    if intent not in valid_intents:
        return "chat"
    if "reflect" in user_message.lower() or "review" in user_message.lower():
        return "self_reflect"

    return intent


def extract_schedule_details(user_message: str):
    """
    Uses Gemini to extract scheduling details.
    Returns dict with start_time (ISO) and duration_minutes.
    """

    prompt = f"""
        You are a scheduling assistant.

        Extract scheduling details from the user message.

        Return ONLY valid JSON in this format:
        {{
        "start_time": "YYYY-MM-DD HH:MM",
        "duration_minutes": number
        }}

        Rules:
        - If time is vague like "after lunch", assume 15:00 today
        - If "tomorrow", use tomorrow's date
        - If duration missing, assume 60 minutes
        - Use 24-hour time
        - Do NOT add explanations

        User message:
        \"\"\"{user_message}\"\"\"
        """

    response = ask_gemini(prompt)

    try:
        import json
        data = json.loads(response)
        return data
    except Exception:
        return {
            "start_time": None,
            "duration_minutes": 60
        }




def user_productivity_reflection():
    """
    Agent checks its memory and reflects on tasks.
    """
    tasks = get_tasks()

    if not tasks:
        return "🧠 Reflection: You had no tasks today. Consider planning tomorrow."

    completed = [t for t in tasks if t["status"] == "done"]
    pending = [t for t in tasks if t["status"] != "done"]

    reflection_prompt = f"""
You are a productivity assistant reflecting on a user's day.

Tasks completed:
{[t['title'] for t in completed]}

Tasks pending:
{[t['title'] for t in pending]}

Write a short reflection:
- What went well
- What can be improved
- One suggestion for tomorrow
"""

    return ask_gemini(reflection_prompt)


def handle_user_message(user_message: str) -> str:
    AGENT_CONTEXT["last_user_message"] = user_message

    intent = decide_intent(user_message)
    AGENT_CONTEXT["last_intent"] = intent


    # 1️⃣ ADD TASK
    if intent == "add_task":
        task = add_task(title=user_message)
        return f"✅ Task added: {task['title']}"

    # 2️⃣ SHOW TASKS
    if intent == "show_tasks":
        tasks = get_tasks()
        if not tasks:
            return "📭 You have no tasks."

        response = "📋 Your tasks:\n"
        for i, task in enumerate(tasks, start=1):
            response += f"{i}. {task['title']} ({task['status']})\n"
        return response


    # 3️⃣ SCHEDULE EVENT
    if intent == "schedule_event":
        plan = [
            "Detect scheduling intent",
            "Extract time and duration",
            "Schedule event using calendar tool",
            "Confirm with user"
        ]

        details = extract_schedule_details(user_message)

        if not details["start_time"]:
            reflection = agent_self_reflect(plan, "Failed to extract time")
            AGENT_CONTEXT["last_agent_reflection"] = reflection

            return f"❌ Could not understand time.\n\n🧠 Agent reflection:\n{reflection}"

        start_time = datetime.strptime(
            details["start_time"], "%Y-%m-%d %H:%M"
        )
        duration = details["duration_minutes"]

        result = schedule_event(
            title=user_message,
            start_time=start_time,
            duration_minutes=duration
        )

        if result["success"]:
            reflection = agent_self_reflect(plan, "Event scheduled successfully")
            AGENT_CONTEXT["last_agent_reflection"] = reflection
            return f"📅 Event scheduled.\n\n🧠 Agent reflection:\n{reflection}"
        else:
            reflection = agent_self_reflect(plan, result["message"])
            AGENT_CONTEXT["last_agent_reflection"] = reflection
            return f"❌ {result['message']}\n\n🧠 Agent reflection:\n{reflection}"

    # if intent == "schedule_event":
    #     details = extract_schedule_details(user_message)

    #     if not details["start_time"]:
    #         return "❌ Could not understand the time. Please be more specific."

    #     start_time = datetime.strptime(
    #         details["start_time"], "%Y-%m-%d %H:%M"
    #     )
    #     duration = details["duration_minutes"]

    #     result = schedule_event(
    #         title=user_message,
    #         start_time=start_time,
    #         duration_minutes=duration
    #     )

    #     if result["success"]:
    #         return f"📅 Scheduled for {start_time.strftime('%H:%M')} ({duration} mins)"
    #     else:
    #         return f"❌ {result['message']}"


    # 4️⃣ SELF REFLECTION
    if intent == "self_reflect":
        return user_productivity_reflection()

    # 4️⃣ NORMAL CHAT
    return ask_gemini(user_message)



def agent_self_reflect(plan, outcome):
    """
    Agent reflects on whether it completed all steps.
    """
    prompt = f"""
You are an AI agent performing self-reflection.

Planned steps:
{plan}

Outcome:
{outcome}

Answer:
- Did the agent complete all steps?
- If not, what went wrong?
- What should the agent do next?

Be concise.
"""
    return ask_gemini(prompt)
