import os 
import streamlit as st 
import pandas as pd # Import pandas 
import styles 
from app import get_recommendations 

# 1. Load data to get the list of names for the dropdown
df_temp = pd.read_csv("tripnepal_destinations.csv")
all_destinations = df_temp['destination'].unique().tolist()

st.set_page_config(page_title="TripNepal Explorer", page_icon="🔍", layout="centered")
styles.apply_custom_theme()

if "current_view" not in st.session_state:
    st.session_state.current_view = "search_inputs"

if st.session_state.current_view == "search_inputs":
    st.title("TripNepal: A Travel Explorer")
    st.caption("Discover your perfect Nepali getaway based on your personal vibe and budget!")
    st.write("---")

    st.subheader("🧳 Tell us about your trip:")

    travel_type = st.selectbox(
        "What type of travel experience do you want?",
        options=["Travel destination", "Tour site"],
        index=None, 
        placeholder="Select..."
    )

    destination_filter = st.selectbox(
    "Where do you want to go? (Optional)",
    options=all_destinations,
    index=None,
    placeholder="Optional"
)
    
    col1, col2 = st.columns(2)
    with col1:
        mood = st.selectbox(
            "What is your trip's vibe/mood?",
            options=["Adventure", "Religious", "Fun", "Peaceful", "Relax", "Nature"],
            index=None,
            placeholder="Select a mood..."
        )
    with col2:
        budget = st.radio(
            "Select your budget level:",
            options=["Low", "Medium", "High"],
            help="Low: Up to 5k NPR | Medium: 10k-40k NPR | High: 40k+ NPR",
            index=None,
            horizontal=True
        )
    if st.button("🔍 Find Matching Spots", use_container_width=True):
        if not travel_type or not mood or not budget:
            st.warning("⚠️ Please select the options above to see your recommendations.")
        else:
            st.session_state.mood = mood
            st.session_state.budget = budget
            st.session_state.travel_type = travel_type
            st.session_state.destination = destination_filter # Save this too
            
            st.session_state.current_view = "results_display"
            st.rerun()

elif st.session_state.current_view == "results_display":
    st.title("✨ Your Custom Recommendations:")
    st.write("---")

    # Run the function with the destination filter included
    results = get_recommendations(
        user_mood=st.session_state.mood, 
        user_budget_tier=st.session_state.budget, 
        user_travel_type=st.session_state.travel_type,
        destination=st.session_state.destination # Pass the optional filter
    )
    
    if results:
        st.success(f"Awesome! We found {len(results)} matching spots:")
        for spot in results:
            with st.container(border=True):
                st.markdown(f"### ●  {spot['name']}")
                st.markdown(f"Location: {spot['location'].capitalize()}")
                st.write(f"{spot['description']}")
                
                image_filename = spot['name'].lower().replace(" ", "_") + ".jpg"
                image_path = os.path.join("photos", image_filename)
                
                if os.path.exists(image_path):
                    st.image(image_path, use_container_width=True)
                else:
                    st.warning(f"Image not found: {image_filename}")
    else:
        st.info("No matches found. Try changing your filters!")

    if st.button("Search again?", use_container_width=True):
        st.session_state.current_view = "search_inputs"
        st.rerun()

    #  CategoryLabelPrice Range (NPR)LowlowUp to 5,000  Mediummedium10,001 – 40,000   HighhighAbove 40,000