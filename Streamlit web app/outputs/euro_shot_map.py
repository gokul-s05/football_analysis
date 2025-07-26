
import json

import pandas as pd
import streamlit as st

import subprocess, sys
try:
    from mplsoccer import VerticalPitch
except ModuleNotFoundError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "mplsoccer==1.5.1"])
    from mplsoccer import VerticalPitch


st.title("Euros 2024 Shot Map")
st.subheader("Filter to any team/player to see all their shots taken!")

df = pd.read_csv('euros_2024_shot_map.csv')
df = df[df['type'] == 'Shot'].reset_index(drop=True)
df['location'] = df['location'].apply(json.loads)

def filter_data(df: pd.DataFrame, team: str, player: str):
    if team:
        df = df[df['team'] == team]
    if player:
        df = df[df['player'] == player]
    return df

def plot_shots(df, ax, pitch):
    for x in df.to_dict(orient='records'):
        pitch.scatter(
            x=float(x['location'][0]),
            y=float(x['location'][1]),
            ax=ax,
            s=1000 * x['shot_statsbomb_xg'],
            color='green' if x['shot_outcome'] == 'Goal' else 'white',
            edgecolors='black',
            alpha=1 if x['type'] == 'goal' else .5,
            zorder=2 if x['type'] == 'goal' else 1
        )

def app():
    st.title("Euros 2024 Shot Map")
    st.subheader("Filter to any team/player to see all their shots taken!")
    teams = ['--'] + sorted(df['team'].dropna().unique().tolist())
    team = st.selectbox("Select a team", teams)

    # Only filter player options if a valid team is selected
    players = ['--']
    if team != '--':
         players+= sorted(df[df['team'] == team]['player'].dropna().unique().tolist())
    player = st.selectbox("Select a player", players)

    # Filter DataFrame
    filtered_df = filter_data(df, None if team == '--' else team, None if player == '--' else player)


    pitch = VerticalPitch(pitch_type='statsbomb', line_zorder=2, pitch_color='#f0f0f0', line_color='black', half=True)
    fig, ax = pitch.draw(figsize=(10, 10))
    plot_shots(filtered_df, ax, pitch)

    st.pyplot(fig)
# Main entry
if __name__ == "__main__":
    app()