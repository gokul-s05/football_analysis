import streamlit as st
import pickle

@st.cache_resource
def load_model():
    with open("model.pkl", "rb") as f:
        return pickle.load(f)

@st.cache_data
def load_team_mapping():
    with open("team_mapping.pkl", "rb") as f:
        return pickle.load(f)
def main():
    model = load_model()
    team_to_id = load_team_mapping()
    team_names = list(team_to_id.keys())

    st.title("**⚽⚽ Match Outcome Predictor 🏆🥇**")
    st.write("Select the **home** and **away** teams to predict the match outcome.")

    team_names_with_placeholder = ["Select a team"] + team_names
    home_team = st.selectbox("Select Home Team", team_names_with_placeholder)
    away_team = st.selectbox("Select Away Team", team_names_with_placeholder)

    if home_team != "Select a team" and away_team != "Select a team":
        home_id = team_to_id[home_team]
        away_id = team_to_id[away_team]
        prediction = model.predict([[home_id, away_id]])[0]
        result_map = {0: "Home Win", 1: "Draw", 2: "Away Win"}
        result = result_map[prediction]
        st.write(f"The prediction for {home_team} vs {away_team} is: {result}")
    else:
        st.write("Please select both home and away teams.")