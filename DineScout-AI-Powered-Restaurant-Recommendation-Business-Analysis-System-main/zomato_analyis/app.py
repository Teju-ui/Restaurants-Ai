import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Business Consultant",
    layout="wide"
)

st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
        <h2 style="margin: 0; padding: 0; color: #1e293b;">AI Business Consultant</h2>
        <a href="https://restaurants-ai-sigma.vercel.app/login.html" target="_self">
            <button style="background: #ff5722; color: white; border: none; padding: 8px 15px; cursor: pointer; border-radius: 5px; font-weight: bold;">
                Logout
            </button>
        </a>
    </div>
""", unsafe_allow_html=True)

# Inject custom CSS to match owner-dashboard.html theme exactly
st.markdown("""
    <style>
    /* Main Background */
    .stApp {
        background-color: #f5f7fb;
    }
    
    /* Sidebar styling to match #1e293b */
    [data-testid="stSidebar"] {
        background-color: #1e293b;
        color: white;
    }
    
    /* Sidebar text color for labels and headers */
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3, 
    [data-testid="stSidebar"] label {
        color: white !important;
    }
    
    /* Ensure select dropdown text is black */
    div[data-baseweb="select"] * {
        color: black !important;
    }
    
    /* Primary buttons to be orange */
    .stButton > button {
        background-color: #ff5722 !important;
        color: white !important;
        border: none !important;
        border-radius: 5px !important;
        padding: 10px 24px !important;
    }
    .stButton > button:hover {
        background-color: #e64a19 !important;
    }
    
    /* Metric cards styling */
    [data-testid="metric-container"] {
        background-color: white;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 0 5px rgba(0,0,0,0.1);
        text-align: center;
    }
    
    /* Metric label styling */
    [data-testid="metric-container"] > div:first-child {
        color: #ff5722 !important;
        font-weight: bold !important;
    }
    
    /* Hide default Streamlit footer and menu */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# LOAD DATA
# -----------------------------
@st.cache_data
def load_data():
    return pd.read_csv("zomato.csv", encoding="latin1")

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

    # Prepare city data
    df_city = df[df["City"] == city].copy()

    df_city["Cuisine_List"] = df_city["Cuisines"].str.split(",")
    df_city = df_city.explode("Cuisine_List")
    df_city["Cuisine_List"] = df_city["Cuisine_List"].str.strip()

    df_cuisine = df_city[df_city["Cuisine_List"] == cuisine]

    if len(df_cuisine) == 0:
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
    # BUSINESS RECOMMENDATION
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
    # TOP CUISINES IN CITY
    # -----------------------------
    st.markdown("---")
    st.markdown(f"### 📌 Top Cuisines in {city}")
    
    top_city_cuisines = (
        df_city["Cuisine_List"]
        .value_counts()
        .head(10)
        .to_dict()
    )
    
    html_city_cuisines = "<ul>"
    for k, v in top_city_cuisines.items():
        html_city_cuisines += f"<li>{k} ({v})</li>"
    html_city_cuisines += "</ul>"
    
    st.markdown(html_city_cuisines, unsafe_allow_html=True)
    
    # -----------------------------
    # TOP CITIES FOR CUISINE
    # -----------------------------
    st.markdown(f"### 🌍 Top Cities for {cuisine}")
    
    # Needs to get all data for cuisine, not just city data
    cuisine_all = df.copy()
    cuisine_all["Cuisine_List"] = cuisine_all["Cuisines"].str.split(",")
    cuisine_all = cuisine_all.explode("Cuisine_List")
    cuisine_all["Cuisine_List"] = cuisine_all["Cuisine_List"].str.strip()
    
    top_cuisine_cities = (
        cuisine_all[cuisine_all["Cuisine_List"] == cuisine]["City"]
        .value_counts()
        .head(10)
        .to_dict()
    )
    
    html_cuisine_cities = "<ul>"
    for k, v in top_cuisine_cities.items():
        html_cuisine_cities += f"<li>{k} ({v})</li>"
    html_cuisine_cities += "</ul>"
    
    st.markdown(html_cuisine_cities, unsafe_allow_html=True)
    
    # -----------------------------
    # BEST BUSINESS OPTIONS
    # -----------------------------
    st.markdown("### 💡 Best Business Options")
    
    best_option_1 = f"Start {cuisine} restaurant in {city}"
    
    if len(top_cuisine_cities) > 0:
        best_city = list(top_cuisine_cities.keys())[0]
        best_option_2 = f"Try {cuisine} in {best_city}"
    else:
        best_option_2 = "Explore new cities"
        
    st.markdown(f"<ul><li>{best_option_1}</li><li>{best_option_2}</li></ul>", unsafe_allow_html=True)

else:
    st.info("👈 Select inputs and click **Analyze Market** to begin.")