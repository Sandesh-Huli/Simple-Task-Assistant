from google.adk.agents import Agent
from google.adk.tools.tool_context import ToolContext
from datetime import datetime
import threading
import time
from plyer import notification
import dateparser

# In-memory reminder store (for demo; use a database for production)
REMINDER_STORE = {}

def set_reminder(message: str, time_str: str, tool_context: ToolContext) -> dict:
    """
    Sets a reminder for the user based on the provided message and time.
    Args:
        message (str): The reminder topic or message.
        time_str (str): The time for the reminder (natural language).
        tool_context (ToolContext): Context object for tools and environment.
    Returns:
        dict: Confirmation message with reminder details.
    """
    user = getattr(tool_context, "user_id", "default")
    reminder_time = dateparser.parse(time_str)
    if not reminder_time:
        return {
            "message": f"Could not understand the time '{time_str}'. Please provide a valid time.",
            "delegate_to_root": True
        }
    REMINDER_STORE.setdefault(user, []).append({
        "message": message,
        "done": False,
        "time": reminder_time.isoformat()
    })
    return {
        "message": f"Reminder set for: '{message}' at {reminder_time.strftime('%Y-%m-%d %H:%M:%S')}. Delegating back to the main assistant.",
        "reminders": REMINDER_STORE[user],
        "delegate_to_root": True
    }

def list_reminders(tool_context: ToolContext) -> dict:
    """
    Lists all reminders for the user, showing their status.
    Args:
        tool_context (ToolContext): Context object for tools and environment.
    Returns:
        dict: List of reminders with status.
    """
    user = getattr(tool_context, "user_id", "default")
    reminders = REMINDER_STORE.get(user, [])
    if reminders:
        reminders_with_status = [
            {
                "message": r["message"],
                "time": r.get("time"),
                "status": "Done" if r.get("done") else "Pending"
            }
            for r in reminders
        ]
        return {
            "message": "Here are your reminders with their status. Delegating back to the main assistant.",
            "reminders": reminders_with_status,
            "delegate_to_root": True
        }
    else:
        return {
            "message": "You have no reminders. Delegating back to the main assistant.",
            "reminders": [],
            "delegate_to_root": True
        }

def delete_reminder(index: int, tool_context: ToolContext) -> dict:
    """
    Deletes a reminder by its index (1-based).
    Args:
        index (int): The index of the reminder to delete.
        tool_context (ToolContext): Context object for tools and environment.
    Returns:
        dict: Confirmation message.
    """
    user = getattr(tool_context, "user_id", "default")
    reminders = REMINDER_STORE.get(user, [])
    if 0 < index <= len(reminders):
        removed = reminders.pop(index - 1)
        return {
            "message": f"Deleted reminder: '{removed['message']}'. Delegating back to the main assistant.",
            "reminders": reminders,
            "delegate_to_root": True
        }
    else:
        return {
            "message": "Invalid reminder index. Delegating back to the main assistant.",
            "reminders": reminders,
            "delegate_to_root": True
        }

def mark_reminder_done(index: int, tool_context: ToolContext) -> dict:
    """
    Marks a reminder as done by its index (1-based).
    Args:
        index (int): The index of the reminder to mark as done.
        tool_context (ToolContext): Context object for tools and environment.
    Returns:
        dict: Confirmation message.
    """
    user = getattr(tool_context, "user_id", "default")
    reminders = REMINDER_STORE.get(user, [])
    if 0 < index <= len(reminders):
        reminders[index - 1]["done"] = True
        return {
            "message": f"Marked reminder as done: '{reminders[index - 1]['message']}'. Delegating back to the main assistant.",
            "reminders": reminders,
            "delegate_to_root": True
        }
    else:
        return {
            "message": "Invalid reminder index. Delegating back to the main assistant.",
            "reminders": reminders,
            "delegate_to_root": True
        }

def send_notification(title: str, message: str):
    notification.notify(
        title=title,
        message=message,
        timeout=10
    )

def reminder_notifier():
    while True:
        now = datetime.now()
        for user, reminders in REMINDER_STORE.items():
            for reminder in reminders:
                if not reminder["done"] and "time" in reminder:
                    reminder_time = dateparser.parse(reminder["time"])
                    if reminder_time and now >= reminder_time:
                        send_notification("Reminder", f"Hey {user}, reminder: {reminder['message']}")
                        reminder["done"] = True
        time.sleep(10)  # Check every 10 seconds

# Start the background notifier thread
notifier_thread = threading.Thread(target=reminder_notifier, daemon=True)
notifier_thread.start()

reminder_agent = Agent(
    name="reminder_agent",
    description="Handles setting, listing, deleting, marking, and notifying reminders for the user.",
    instruction=(
        "Use the set_reminder tool to save reminders when the user asks, including the time. "
        "Use the list_reminders tool to show all reminders. "
        "Use the delete_reminder tool to remove a reminder by its number. "
        "Use the mark_reminder_done tool to mark a reminder as completed. "
        "Always confirm each operation and delegate back to the root agent after responding."
    ),
    model="gemini-2.0-flash",
    tools=[set_reminder, list_reminders, delete_reminder, mark_reminder_done]
)