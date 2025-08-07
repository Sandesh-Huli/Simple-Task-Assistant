from google.adk.agents import Agent
from google.adk.tools.tool_context import ToolContext

def get_weather(location: str, tool_context: ToolContext) -> dict:
    """
    Retrieves the current weather for the specified location.

    Args:
        location (str): The location for which to get the weather.
        tool_context (ToolContext): Context object for tools and environment.

    Returns:
        dict: Weather information for the location.
    """
    # Parameters/Arguments
    weather_details = {
        "location": location,
        "user": tool_context.user_id if hasattr(tool_context, "user_id") else "unknown"
    }

    # List: Add more details if needed
    # e.g., weather_details["temperature"] = "25°C"
    # e.g., weather_details["condition"] = "Sunny"

    # Comment: Here you would integrate with a weather API or service
    return {
        "message": f"Weather for location: '{location}' is currently unavailable (mock response).",
        "details": weather_details,
        "delegate_to_root":True
    }


# Instantiate the get_weather agent
weather_agent = Agent(
    name="weather_agent",
    description="Provides current weather information for a given location.",
    instruction=(
        "You are responsible for providing current weather information to users. "
        "When a user provides a location, respond with the weather details for that location. "
        "If weather data is unavailable, inform the user accordingly. "
        "Always respond with a clear message and include all relevant details."
    ),
    model="gemini-2.0-flash",
    tools=[get_weather]
)