#app.py
import pandas as pd #main code
import streamlit as st

@st.cache_data
def get_recommendations(user_mood, user_budget_tier, user_travel_type, destination=None):

    # 1. Load data 
    try:
        df = pd.read_csv("tripnepal_destinations.csv")
        print(df.columns.tolist())
    except FileNotFoundError:
        print("DEBUG: CSV file not found!")
        return []

    # 2. Standardize column names
    df.columns = df.columns.str.strip().str.lower()

    # 3. Standardize data
    for col in df.columns:
        df[col] = df[col].astype(str).str.strip().str.lower()

    # 4. Standardize inputs
    u_mood = user_mood.strip().lower()
    u_budget = user_budget_tier.strip().lower()
    u_type = user_travel_type.strip().lower()

    # 5. Base filter
    mask = (df['mood'] == u_mood) & \
            (df['travel_type'] == u_type)

    filtered_df = df[mask]
    BUDGET_RANK = {
        "low": 1,
        "medium": 2,
        "high":3
    }
    filtered_df["budget_rank"] = filtered_df["budget"].map(BUDGET_RANK)
    user_rank = BUDGET_RANK[u_budget]
    
    filtered_df = filtered_df[filtered_df["budget_rank"] <= user_rank]

    # 6. Optional destination (logic kept same, just fixed variable use)
    if destination and destination.strip() != "":
        dest_input = destination.strip().lower()

        filtered_df = filtered_df[
            (filtered_df['name'] == dest_input) 
            # (filtered_df['location'] == dest_input)
        ]

    return filtered_df.to_dict('records')