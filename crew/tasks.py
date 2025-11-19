# crew/tasks.py
from crewai import Task
from gemini_client import generate_text
from utils.places_api import nearby_search
from crew.agents import (
    research_agent,
    attractions_agent,
    hotels_agent,
    budget_agent,
    itinerary_agent
)

class ResearchTask(Task):
    def __init__(self):
        super().__init__(
            description="Research the destination and provide overview.",
            expected_output="Summary of destination including climate, best time and tips.",
            agent=research_agent
        )

    def run(self, destination: str):
        prompt = f"""
        Give a detailed overview about {destination} including:
        - Climate
        - Best time to visit
        - Safety + travel tips
        - Top 10 places
        """
        return {"summary": generate_text(prompt, max_output_tokens=700)}

class AttractionsTask(Task):
    def __init__(self):
        super().__init__(
            description="Get top attractions.",
            expected_output="Top attractions with descriptions.",
            agent=attractions_agent
        )

    def run(self, destination: str):
        prompt = f"List top 10 attractions in {destination} with one-line description."
        return {"attractions": generate_text(prompt, max_output_tokens=600)}

class HotelsTask(Task):
    def __init__(self):
        super().__init__(
            description="Find top hotels.",
            expected_output="List of best hotels with rating + address.",
            agent=hotels_agent
        )

    def run(self, destination: str):
        data = nearby_search(destination, "hotels")
        if data and "results" in data:
            return {
                "hotels": [
                    {
                        "name": r.get("name"),
                        "address": r.get("formatted_address"),
                        "rating": r.get("rating")
                    }
                    for r in data["results"][:7]
                ]
            }

        prompt = f"List 7 good hotels in {destination}."
        return {"hotels": generate_text(prompt, max_output_tokens=500)}

class BudgetTask(Task):
    def __init__(self):
        super().__init__(
            description="Estimate trip budget.",
            expected_output="Total cost estimation.",
            agent=budget_agent
        )

    def run(self, origin: str, destination: str, days: int, travel_mode: str):
        prompt = f"""
        Estimate budget for {days}-day trip from {origin} to {destination} by {travel_mode}.
        Include stay, food, travel, attractions and final total.
        """
        return {"budget": generate_text(prompt, max_output_tokens=500)}

class ItineraryTask(Task):
    def __init__(self):
        super().__init__(
            description="Create itinerary.",
            expected_output="Day-by-day travel plan.",
            agent=itinerary_agent
        )

    def run(self, destination: str, days: int, attractions: str):
        prompt = f"""
        Create a {days}-day itinerary for {destination}
        using these attractions: {attractions}.
        Include timing + details per day.
        """
        return {"itinerary": generate_text(prompt, max_output_tokens=800)}
