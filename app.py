# app.py
import streamlit as st
from crew.crew_config import build_crew
from crew.tasks import ResearchTask, HotelsTask, AttractionsTask, BudgetTask, ItineraryTask

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

    crew = build_crew([
        research_task,
        attractions_task,
        hotels_task,
        budget_task,
        itinerary_task
    ])

    # Run tasks
    research = research_task.run(destination)
    attractions = attractions_task.run(destination)
    hotels = hotels_task.run(destination)
    budget = budget_task.run(origin, destination, days, travel_mode)
    itinerary = itinerary_task.run(destination, days, attractions["attractions"])

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

    st.markdown("## 🗓 Day-by-Day Itinerary")
    st.markdown(f"<div class='card'>{itinerary['itinerary']}</div>", unsafe_allow_html=True)
