import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Business Consultant",
    layout="wide"
)

st.title("🍽️ AI Restaurant Business Consultant")
st.subheader("Smart Decision Support for Restaurant Owners")

# -----------------------------
# LOAD DATA (FIXED FOR STREAMLIT CLOUD)
# -----------------------------
@st.cache_data
def load_data():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, "zomato.csv")
    return pd.read_csv(file_path, encoding="latin1")

df = load_data()

# -----------------------------
# SIDEBAR INPUT
# -----------------------------
st.sidebar.header("Business Inputs")

city = st.sidebar.selectbox(
    "Select City",
    sorted(df["City"].dropna().unique())
)

all_cuisines = (
    df["Cuisines"]
    .dropna()
    .str.split(",")
    .explode()
    .str.strip()
    .unique()
)

cuisine = st.sidebar.selectbox(
    "Select Cuisine",
    sorted(all_cuisines)
)

analyze = st.sidebar.button("Analyze Market")

# -----------------------------
# MAIN LOGIC
# -----------------------------
if analyze:

    st.divider()

    df_city = df[df["City"] == city].copy()

    df_city["Cuisine_List"] = df_city["Cuisines"].str.split(",")
    df_city = df_city.explode("Cuisine_List")
    df_city["Cuisine_List"] = df_city["Cuisine_List"].str.strip()

    df_cuisine = df_city[df_city["Cuisine_List"] == cuisine]

    if df_cuisine.empty:
        st.warning("No sufficient data available for this selection.")
        st.stop()

    # -----------------------------
    # KEY INSIGHTS
    # -----------------------------
    st.markdown("## 📌 Key Market Insights")

    avg_rating = round(df_cuisine["Aggregate rating"].mean(), 2)
    avg_cost = round(df_cuisine["Average Cost for two"].mean(), 0)
    avg_votes = int(df_cuisine["Votes"].mean())
    total_restaurants = len(df_cuisine)

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("⭐ Avg Rating", avg_rating)
    c2.metric("💰 Avg Cost for Two", f"₹{avg_cost}")
    c3.metric("👍 Avg Votes", avg_votes)
    c4.metric("🏪 Restaurants", total_restaurants)

    # -----------------------------
    # DEMAND LEVEL
    # -----------------------------
    if total_restaurants > 150:
        demand_level = "High"
    elif total_restaurants > 70:
        demand_level = "Medium"
    else:
        demand_level = "Low"

    st.info(f"📈 Demand Level for {cuisine} in {city}: {demand_level}")

    # -----------------------------
    # RECOMMENDATION
    # -----------------------------
    st.markdown("## ✅ Business Recommendation")

    if demand_level == "High" and avg_rating >= 3.8:
        recommendation = f"Start a {cuisine} restaurant in {city}. High profit potential."
    elif demand_level == "Medium":
        recommendation = f"Competitive market in {city}. Focus on branding and quality."
    else:
        recommendation = f"High risk in {city}. Try another cuisine or location."

    st.success(recommendation)

    # -----------------------------
    # GRAPHS
    # -----------------------------
    st.markdown("## 📊 Supporting Analysis")

    left, right = st.columns(2)

    # GRAPH 1
    with left:
        st.caption(f"{cuisine} Demand Across Cities")

        cuisine_all = df.copy()
        cuisine_all["Cuisine_List"] = cuisine_all["Cuisines"].str.split(",")
        cuisine_all = cuisine_all.explode("Cuisine_List")
        cuisine_all["Cuisine_List"] = cuisine_all["Cuisine_List"].str.strip()

        cuisine_city = (
            cuisine_all[cuisine_all["Cuisine_List"] == cuisine]
            .groupby("City")
            .size()
            .sort_values(ascending=False)
            .head(8)
        )

        fig1, ax1 = plt.subplots()
        bars = ax1.bar(cuisine_city.index, cuisine_city.values)

        ax1.set_ylabel("Restaurant Count")
        ax1.set_xticklabels(cuisine_city.index, rotation=45, ha="right")

        for bar in bars:
            h = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2, h + 1, int(h), ha="center")

        st.pyplot(fig1)

    # GRAPH 2
    with right:
        st.caption(f"{cuisine} Popularity in {city}")

        cuisine_pop = (
            df_city.groupby("Cuisine_List")
            .size()
            .sort_values(ascending=False)
            .head(8)
        )

        fig2, ax2 = plt.subplots()
        bars = ax2.bar(cuisine_pop.index, cuisine_pop.values)

        ax2.set_ylabel("Restaurant Count")
        ax2.set_xticklabels(cuisine_pop.index, rotation=45, ha="right")

        for bar in bars:
            h = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2, h + 1, int(h), ha="center")

        st.pyplot(fig2)

    # -----------------------------
    # SUMMARY
    # -----------------------------
    st.divider()
    st.markdown("## 📄 Consultant Summary")

    st.write(f"""
    ✔ City: **{city}**  
    ✔ Cuisine: **{cuisine}**

    • Demand Level: **{demand_level}**  
    • Avg Rating: **{avg_rating}**  
    • Avg Cost for Two: **₹{avg_cost}**  
    • Avg Votes: **{avg_votes}**

    🔹 Recommendation: **{recommendation}**
    """)

else:
    st.info("👈 Select inputs and click **Analyze Market** to begin.")