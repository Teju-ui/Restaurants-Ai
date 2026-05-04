import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="AI Restaurant Consultant", layout="wide")

# -----------------------------
# SESSION STATE (LOGIN)
# -----------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "users" not in st.session_state:
    st.session_state.users = {}   # stores users temporarily

# -----------------------------
# LOGIN / REGISTER UI
# -----------------------------
def login_page():
    st.title("🔐 Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in st.session_state.users and st.session_state.users[username] == password:
            st.session_state.logged_in = True
            st.success("Login successful!")
            st.rerun()
        else:
            st.error("Invalid username or password")

    if st.button("Go to Register"):
        st.session_state.page = "register"
        st.rerun()


def register_page():
    st.title("📝 Register")

    new_user = st.text_input("New Username")
    new_pass = st.text_input("New Password", type="password")

    if st.button("Register"):
        if new_user in st.session_state.users:
            st.warning("User already exists")
        else:
            st.session_state.users[new_user] = new_pass
            st.success("Registration successful! Go to login.")

    if st.button("Back to Login"):
        st.session_state.page = "login"
        st.rerun()


# -----------------------------
# LOAD DATA
# -----------------------------
@st.cache_data
def load_data():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, "zomato.csv")
    return pd.read_csv(file_path, encoding="latin1")


# -----------------------------
# MAIN DASHBOARD
# -----------------------------
def main_app():
    st.title("🍽️ AI Restaurant Business Consultant")
    st.subheader("Smart Decision Support for Restaurant Owners")

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    df = load_data()

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

    if analyze:

        df_city = df[df["City"] == city].copy()
        df_city["Cuisine_List"] = df_city["Cuisines"].str.split(",")
        df_city = df_city.explode("Cuisine_List")
        df_city["Cuisine_List"] = df_city["Cuisine_List"].str.strip()

        df_cuisine = df_city[df_city["Cuisine_List"] == cuisine]

        if df_cuisine.empty:
            st.warning("No sufficient data available.")
            return

        st.markdown("## 📌 Insights")

        avg_rating = round(df_cuisine["Aggregate rating"].mean(), 2)
        avg_cost = round(df_cuisine["Average Cost for two"].mean(), 0)
        total = len(df_cuisine)

        c1, c2, c3 = st.columns(3)
        c1.metric("⭐ Rating", avg_rating)
        c2.metric("💰 Cost", f"₹{avg_cost}")
        c3.metric("🏪 Count", total)

        # GRAPH
        fig, ax = plt.subplots()
        ax.hist(df_cuisine["Aggregate rating"], bins=10)
        st.pyplot(fig)


# -----------------------------
# ROUTING
# -----------------------------
if "page" not in st.session_state:
    st.session_state.page = "login"

if not st.session_state.logged_in:
    if st.session_state.page == "login":
        login_page()
    else:
        register_page()
else:
    main_app()