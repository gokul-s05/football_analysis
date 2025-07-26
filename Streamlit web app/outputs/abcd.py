import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import ast
import os

# Setting Streamlit page configuration
st.set_page_config(page_title="Euros 2024 Match Heatmap Dashboard", layout="wide")

# Defining function to load and clean data
@st.cache_data
def load_and_clean_data(file_path):
    try:
        # Loading CSV
        df = pd.read_csv(file_path, low_memory=False)
        
        # Cleaning and processing data
        def parse_location(loc):
            try:
                # Converting string "[x, y]" to list of floats
                loc_list = ast.literal_eval(loc)
                return [float(loc_list[0]), float(loc_list[1])]
            except (ValueError, SyntaxError):
                return [None, None]
        
        # Applying location parsing
        df[['x', 'y']] = df['location'].apply(parse_location).apply(pd.Series)
        
        # Converting xG to numeric, handling errors
        df['shot_statsbomb_xg'] = pd.to_numeric(df['shot_statsbomb_xg'], errors='coerce').fillna(0)
        
        # Selecting relevant columns and filtering invalid rows
        df = df[['match_id', 'team', 'player', 'x', 'y', 'shot_outcome', 'shot_statsbomb_xg', 'minute', 'period']]
        df = df.dropna(subset=['x', 'y', 'match_id', 'shot_outcome'])
        
        # Converting minute and period to integers
        df['minute'] = df['minute'].astype(int)
        df['period'] = df['period'].astype(int)
        
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

# Defining function to create shot heatmap
def create_shot_heatmap(data, pitch_image_path):
    # Defining outcome colors
    outcome_colors = {
        'Goal': 'green',
        'Saved': 'blue',
        'Blocked': 'red',
        'Off T': 'orange',
        'Post': 'purple',
        'Wayward': 'gray'
    }
    
    # Creating scatter traces for each outcome
    fig = go.Figure()
    for outcome, color in outcome_colors.items():
        outcome_data = data[data['shot_outcome'] == outcome]
        if not outcome_data.empty:
            fig.add_trace(
                go.Scatter(
                    x=outcome_data['x'],
                    y=outcome_data['y'],
                    mode='markers',
                    name=outcome,
                    marker=dict(
                        size=outcome_data['shot_statsbomb_xg'].apply(lambda x: max(5, min(15, x * 20))),
                        color=color,
                        opacity=0.7
                    ),
                    text=outcome_data.apply(
                        lambda row: (
                            f"Player: {row['player']}<br>"
                            f"Team: {row['team']}<br>"
                            f"Outcome: {row['shot_outcome']}<br>"
                            f"xG: {row['shot_statsbomb_xg']:.3f}<br>"
                            f"Minute: {row['minute']}<br>"
                            f"Period: {row['period']}"
                        ), axis=1
                    ),
                    hoverinfo='text'
                )
            )
    
    # Setting layout with pitch image
    fig.update_layout(
        title="Shot Heatmap",
        xaxis=dict(range=[0, 120], showgrid=False, zeroline=False, title="X (meters)"),
        yaxis=dict(range=[0, 80], showgrid=False, zeroline=False, title="Y (meters)"),
        showlegend=True,
        width=800,
        height=600,
        images=[dict(
            source=f"file://{os.path.abspath(pitch_image_path)}",
            xref="x",
            yref="y",
            x=0,
            y=80,
            sizex=120,
            sizey=80,
            sizing="stretch",
            opacity=0.8,
            layer="below"
        )]
    )
    
    return fig

# Main dashboard function
def main():
    st.title("Euros 2024 Match Heatmap Dashboard")
    
    # Loading data
    data = load_and_clean_data("euros_2024_shot_map.csv")
    
    if data.empty:
        st.error("No valid data loaded. Please check the CSV file.")
        return
    
    # Getting unique match IDs
    matches = sorted(data['match_id'].unique())
    
    # Creating match selector
    st.subheader("Select Match")
    selected_match = st.selectbox(
        "Match ID",
        matches,
        format_func=lambda x: f"Match ID: {x} ({data[data['match_id'] == x]['team'].iloc[0]} vs Opponent)"
    )
    
    # Filtering data for selected match
    filtered_data = data[data['match_id'] == selected_match]
    
    # Displaying summary statistics
    st.subheader("Match Summary")
    total_shots = len(filtered_data)
    total_goals = len(filtered_data[filtered_data['shot_outcome'] == 'Goal'])
    total_xg = filtered_data['shot_statsbomb_xg'].sum()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Shots", total_shots)
    with col2:
        st.metric("Total Goals", total_goals)
    with col3:
        st.metric("Total xG", f"{total_xg:.2f}")
    
    # Displaying interesting fact
    st.subheader("Interesting Fact")
    if not filtered_data.empty:
        player_xg = filtered_data.groupby('player')['shot_statsbomb_xg'].sum()
        top_player = player_xg.idxmax()
        top_xg = player_xg.max()
        st.info(f"{top_player} had the highest xG in this match with {top_xg:.2f} expected goals!")
    else:
        st.info("No shots recorded for this match.")
    
    # Displaying shot heatmap
    st.subheader("Shot Heatmap")
    pitch_image_path = "pitch.png"
    if os.path.exists(pitch_image_path):
        fig = create_shot_heatmap(filtered_data, pitch_image_path)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.error("Pitch image (pitch.png) not found in the current directory.")

if __name__ == "__main__":
    main()