import pandas as pd
from sklearn.cluster import KMeans
import streamlit as st


@st.cache_data
def get_recommendations(user_mood, user_budget_tier, user_travel_type, destination=None):

    df = pd.read_csv("tripnepal_destinations.csv")

    # Clean
    df.columns = df.columns.str.strip().str.lower()

    for col in df.columns:
        df[col] = df[col].astype(str).str.strip().str.lower()


    mood = user_mood.lower()
    budget = user_budget_tier.lower()
    travel_type = user_travel_type.lower()


    # ---------- CLUSTERING ----------

    features = pd.get_dummies(
        df[["mood", "budget", "travel_type"]]
    )


    kmeans = KMeans(
        n_clusters=4,
        random_state=42,
        n_init=10
    )

    df["cluster"] = kmeans.fit_predict(features)



    # ---------- RECOMMENDATIONS ----------

    budget_rank = {
        "low": 1,
        "medium": 2,
        "high": 3
    }


    df["budget_rank"] = df["budget"].map(budget_rank)

    user_budget_rank = budget_rank.get(budget, 1)


    recommendations = df[
        (df["mood"] == mood) &
        (df["travel_type"] == travel_type) &
        (df["budget_rank"] <= user_budget_rank)
    ].copy()



    # ---------- SIMILAR DESTINATIONS ----------

    similar = pd.DataFrame()


    if destination:

        selected = df[
            df["name"] == destination.lower()
        ]


        if not selected.empty:

            cluster_id = selected.iloc[0]["cluster"]

            similar = df[
                (df["cluster"] == cluster_id) &
                (df["name"] != destination.lower())
            ]



    # If no destination selected, use recommendation cluster

    if similar.empty and not recommendations.empty:

        cluster_id = recommendations.iloc[0]["cluster"]

        similar = df[
            (df["cluster"] == cluster_id) 
        ].copy()

        # remove exact recommendations only if other places exist
        remaining = similar[
            ~similar["name"].isin(recommendations["name"])
        ]

        if not remaining.empty:
            similar = remaining



    return (
        recommendations.to_dict("records"),
        similar.to_dict("records")
    )