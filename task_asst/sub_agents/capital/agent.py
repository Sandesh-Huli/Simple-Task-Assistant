from google.adk.agents import Agent
from google.adk.tools.tool_context import ToolContext
import json
import os

# Load country-capital data from a JSON file
DB_PATH = os.path.join(os.path.dirname(__file__), "country_capitals.json")
if os.path.exists(DB_PATH):
    with open(DB_PATH, "r", encoding="utf-8") as f:
        COUNTRY_CAPITALS = json.load(f)
else:
    COUNTRY_CAPITALS = {}

def get_capital(country: str, tool_context: ToolContext) -> dict:
    """
    Returns the capital city of the requested country using a local database file.

    Args:
        country (str): The country name.
        tool_context (ToolContext): Context object for tools and environment.

    Returns:
        dict: Capital city information.
    """
    country_key = country.strip().lower()
    capital = COUNTRY_CAPITALS.get(country_key)
    if capital:
        return {
            "message": f"The capital of {country.title()} is {capital}.",
            "country": country.title(),
            "capital": capital,
            "delegate_to_root":True
        }
    else:
        return {
            "message": f"Could not find the capital for '{country.title()}'.",
            "country": country.title(),
            "capital": None,
            "delegate_to_root":True
        }

capital_agent = Agent(
    name="capital_agent",
    description="Provides the capital city of a requested country.",
    instruction=(
        "Use the get_capital tool to answer questions about the capital city of any country. "
        "Always respond with the capital city if known, or say you don't know if it is not available."
    ),
    model="gemini-2.0-flash",
    tools=[get_capital]
)