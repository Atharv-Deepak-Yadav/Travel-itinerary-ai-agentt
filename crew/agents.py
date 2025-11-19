# crew/agents.py
import os
from dotenv import load_dotenv
from crewai import Agent

load_dotenv()

google_llm = {
    "provider": "litellm",
    "model": "gemini-pro-latest",        # CORRECT FORMAT
    "api_key": os.getenv("GEMINI_API_KEY")
}

research_agent = Agent(
    name="Research Agent",
    role="Research",
    goal="Research destination.",
    backstory="Expert travel researcher.",
    llm=google_llm
)

attractions_agent = Agent(
    name="Attractions Agent",
    role="Attractions",
    goal="Find attractions.",
    backstory="Tour guide expert.",
    llm=google_llm
)

hotels_agent = Agent(
    name="Hotels Agent",
    role="Hotels",
    goal="Find hotels.",
    backstory="Hotel reviewer.",
    llm=google_llm
)

budget_agent = Agent(
    name="Budget Agent",
    role="Budget",
    goal="Estimate costs.",
    backstory="Finance planner.",
    llm=google_llm
)

itinerary_agent = Agent(
    name="Itinerary Agent",
    role="Planner",
    goal="Create itinerary.",
    backstory="Trip planner.",
    llm=google_llm
)
