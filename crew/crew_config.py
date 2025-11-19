# crew/crew_config.py
from crewai import Crew

def build_crew(tasks):
    return Crew(
        name="travel_planner_crew",
        tasks=tasks,
        verbose=True
    )
