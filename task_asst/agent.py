from google.adk.agents import Agent
from task_asst.sub_agents.reminder import reminder_agent
from task_asst.sub_agents.weather import weather_agent
from task_asst.sub_agents.notes import notes_agent
from task_asst.sub_agents.capital import capital_agent


root_agent = Agent(
    name="task_assistant",
    model="gemini-2.0-flash",
    description="Simple Task Assistant",
    instruction="""
    I am a productivity assistant who can handle reminders, notes, weather, and capital city questions.
    After each sub-agent handles a request, control should return to me for further assistance.
    """,
    sub_agents=[reminder_agent, weather_agent, notes_agent, capital_agent],
)