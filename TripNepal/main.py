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

# Wrapped inputs inside a container box for the frosted glass effect
    with st.container(border=True):
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
    results, similar_results = get_recommendations(
        user_mood=st.session_state.mood, 
        user_budget_tier=st.session_state.budget, 
        user_travel_type=st.session_state.travel_type,
        destination=st.session_state.destination # Pass the optional filter
    )
    
    # -------- MAIN RECOMMENDATIONS --------

    st.markdown("## 🌄 Your Top Recommendations")

    if results:

        st.success(f"Awesome! We found {len(results)} matching spots for you!")

        for spot in results:

            with st.container(border=True):

                st.markdown(
                    f"##  {spot['name'].title()}"
                )

                st.markdown(
                    f"**📍 Location:** {spot['location'].capitalize()}"
                )

                st.markdown(
                    f"**✨ Experience:** {spot['mood'].capitalize()} | "
                    f"**💰 Budget:** {spot['budget'].capitalize()}"
                )

                st.write(
                    spot['description']
                )

                image_filename = spot['name'].lower().replace(" ", "_") + ".jpg"
                image_path = os.path.join("photos", image_filename)

                if os.path.exists(image_path):
                    st.image(
                        image_path,
                        use_container_width=True
                    )

                st.divider()


    else:

        st.info(
            "No matches found. Try changing your filters!"
        )





    # -------- SECONDARY RECOMMENDATIONS --------

    st.markdown("---")

    st.markdown("### ✨ You May Also Like")

    st.caption(
        "Similar destinations based on your travel vibe"
    )


    if similar_results:

        for spot in similar_results:

            with st.container(border=True):

                st.markdown(
                    f"**{spot['name'].title()}**"
                )

                st.caption(
                    f"📍 {spot['location'].capitalize()} • "
                    f"{spot['mood'].capitalize()} • "
                    f"{spot['budget'].capitalize()} budget"
                )

                st.write(
                    spot['description']
                )

                image_filename = spot['name'].lower().replace(" ", "_") + ".jpg"
                image_path = os.path.join("photos", image_filename)

                if os.path.exists(image_path):
                    st.image(
                        image_path,
                        width=250
                    )

    else:

        st.caption(
            "No similar destinations found."
        )
        # -------- SEARCH AGAIN BUTTON --------

    if st.button("Search again?", use_container_width=True):
        st.session_state.current_view = "search_inputs"
        st.rerun()

