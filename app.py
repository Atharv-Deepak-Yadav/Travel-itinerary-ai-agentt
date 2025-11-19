# app.py (Modified)
import streamlit as st
from crew.crew_config import build_crew
# 1. NEW IMPORT: Add CuisineTask
from crew.tasks import ResearchTask, HotelsTask, AttractionsTask, BudgetTask, ItineraryTask, CuisineTask

st.set_page_config(page_title="AI Travel Planner", page_icon="🌍", layout="wide")

# ---------- CUSTOM CSS ----------
st.markdown("""
    <style>
    .big-title {
        font-size: 42px !important;
        font-weight: 800 !important;
        color: #0072F5 !important;
        text-align: center;
        margin-bottom: 10px;
    }
    .subtitle {
        text-align: center;
        font-size: 18px;
        color: #555;
        margin-bottom: 30px;
    }
    .card {
        padding: 20px;
        border-radius: 15px;
        background-color: #ffffff;
        box-shadow: 0px 6px 20px rgba(0,0,0,0.06);
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# ---------- TITLE ----------
st.markdown("<h1 class='big-title'>🌍 AI Travel Itinerary Planner</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Powered by Gemini + CrewAI Agents</p>", unsafe_allow_html=True)

# ---------- INPUT FORM ----------
st.markdown("### ✈️ Plan Your Trip")
with st.form("form"):
    col1, col2 = st.columns(2)
    with col1:
        origin = st.text_input("🟦 Your Origin", "Mumbai")
        days = st.number_input("📅 Number of Days", 1, 30, 3)
    with col2:
        destination = st.text_input("🟨 Destination", "Goa")
        travel_mode = st.selectbox("🚗 Mode of Travel", ["car", "train", "flight"])

    # 2. NEW INPUT: Travel Preference for personalization
    travel_style = st.selectbox(
        "✨ Travel Style Preference",
        ["General Interest", "Relaxation (Beaches, Spas)", "Adventure (Hiking, Sports)", "Cultural (Museums, History)", "Foodie (Local Cuisine)"],
        index=0 # Default to General Interest
    )

    generate = st.form_submit_button("✨ Generate Complete Itinerary")

# ---------- MAIN OUTPUT ----------
if generate:
    st.info("⏳ Please wait while we prepare your travel plan...")

    # Initialize tasks
    research_task = ResearchTask()
    attractions_task = AttractionsTask()
    hotels_task = HotelsTask()
    budget_task = BudgetTask()
    itinerary_task = ItineraryTask()
    # 3. NEW TASK INITIALIZATION
    cuisine_task = CuisineTask()

    crew = build_crew([
        research_task,
        attractions_task,
        hotels_task,
        budget_task,
        itinerary_task,
        cuisine_task # 4. ADD NEW TASK TO CREW
    ])

    # Run tasks - Adjusting calls to pass 'travel_style' and run 'cuisine_task'
    # NOTE: You must update your Task classes in crew/tasks.py to accept and use these new arguments.
    research = research_task.run(destination)
    attractions = attractions_task.run(destination, travel_style) # Pass style for filtering
    hotels = hotels_task.run(destination, travel_style) # Pass style for personalized hotel tier
    budget = budget_task.run(origin, destination, days, travel_mode, travel_style) # Pass style for better budget estimate
    cuisine = cuisine_task.run(destination) # 5. RUN NEW TASK
    itinerary = itinerary_task.run(destination, days, attractions["attractions"], travel_style, cuisine["recommendations"]) # Use all new info for final plan

    # ---------- OUTPUT SECTIONS ----------
    st.markdown("## 🌎 Destination Overview")
    st.markdown(f"<div class='card'>{research['summary']}</div>", unsafe_allow_html=True)

    st.markdown("## 🏖 Top Attractions")
    st.markdown(f"<div class='card'>{attractions['attractions']}</div>", unsafe_allow_html=True)

    st.markdown("## 🏨 Recommended Hotels")
    hotel_html = "<div class='card'>"
    if isinstance(hotels["hotels"], list):
        for h in hotels["hotels"]:
            hotel_html += f"""
            <p><b>{h['name']}</b> — ⭐ {h.get('rating', 'N/A')}<br>
            <span style='color:#666;'>{h.get('address','')}</span></p>
            <hr>
            """
    else:
        hotel_html += hotels["hotels"]

    hotel_html += "</div>"
    st.markdown(hotel_html, unsafe_allow_html=True)

    st.markdown("## 💸 Estimated Budget")
    st.markdown(f"<div class='card'>{budget['budget']}</div>", unsafe_allow_html=True)

    # 6. NEW OUTPUT SECTION: Local Cuisine
    st.markdown("## 🍲 Unique Local Tastes & Experiences")
    st.markdown(f"<div class='card'>{cuisine['recommendations']}</div>", unsafe_allow_html=True)

    st.markdown("## 🗓 Day-by-Day Itinerary")
    st.markdown(f"<div class='card'>{itinerary['itinerary']}</div>", unsafe_allow_html=True)
