from google.adk.agents import Agent
from google.adk.tools.tool_context import ToolContext

# In-memory notes storage (for demo; use a database for production)
NOTES_STORE = {}

def take_note(note: str, tool_context: ToolContext) -> dict:
    """
    Saves a note for the user.

    Args:
        note (str): The note content.
        tool_context (ToolContext): Context object for tools and environment.

    Returns:
        dict: Confirmation message.
    """
    user = getattr(tool_context, "user_id", "default")
    NOTES_STORE.setdefault(user, []).append(note)
    return {
        "message": f"Note saved: '{note}'",
        "notes": NOTES_STORE[user],
        "delegate_to_root":True
    }

def show_notes(tool_context: ToolContext) -> dict:
    """
    Displays all notes for the user.

    Args:
        tool_context (ToolContext): Context object for tools and environment.

    Returns:
        dict: List of notes.
    """
    user = getattr(tool_context, "user_id", "default")
    notes = NOTES_STORE.get(user, [])
    if notes:
        return {
            "message": "Here are your notes:",
            "notes": notes,
            "delegate_to_root":True
        }
    else:
        return {
            "message": "You have no notes saved.",
            "notes": [],
            "delegate_to_root":True
        }

notes_agent = Agent(
    name="notes_agent",
    description="Handles taking and displaying notes for the user.",
    instruction=(
        "Use the take_note tool to save notes when the user wants to remember something. "
        "Use the show_notes tool when the user asks to see their notes. "
        "Always confirm when a note is saved and display all notes when requested."
    ),
    model="gemini-2.0-flash",
    tools=[take_note,show_notes]
)