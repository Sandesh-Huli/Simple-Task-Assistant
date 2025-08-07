# Task Assistant

A modular AI-powered productivity assistant built with the Google Agent Development Kit (ADK).  
It supports reminders, notes, weather queries, and capital city lookups via sub-agents.

## Features

- **Reminders:** Set, list, delete, mark as done, and receive notifications for reminders.
- **Notes:** Take and display notes.
- **Weather:** Get current weather for any city.
- **Capital:** Find the capital city of any country.

## Structure

```
task_asst/
    agent.py                # Root agent
    sub_agents/
        reminder/
            agent.py
            README.md
        notes/
            agent.py
            README.md
        weather/
            agent.py
            README.md
        capital/
            agent.py
            country_capitals.json
            README.md
```

## Setup

1. **Clone the repo and install dependencies:**
    ```
    pip install -r requirements.txt
    ```

2. **Set up your `.env` file:**
    ```
    GOOGLE_API_KEY=your_google_api_key
    WEATHER_API_KEY=your_openweathermap_api_key
    ```

3. **Run the agent using ADK tools or your preferred method.**

---

