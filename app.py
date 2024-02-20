import pandas as pd
import streamlit as st
import plotly.express as px
import base64



# import data
df = pd.read_csv('NBAlineup.csv')

# Title for app
st.set_page_config(layout="wide")
st.title('NBA Lineup Analysis Tool')
st.write('Using this tool we can analyse some key statistics in the NBA, picking our best starting lineup.')
st.write('You can see the difference in 3 key metrics- namely plus minus, field goal percentage and 3 point percentage.')
st.write('We can pick the best starting lineup using these key metrics.')



# Ask user to select a team
selected_team = st.selectbox('Select a team', df['team'].unique())

# Filter the dataset based on the selected team
team_df = df[df['team'] == selected_team]

# Extract players from the selected team's lineup
players_list = team_df['players_list'].iloc[0]  # Assuming each lineup is a string with players separated by comma
players = [player.strip() for player in players_list.split(',')]  # Convert string to list of players

# Allow user to select 5 players from the team's lineup
selected_players = st.multiselect('Select 5 players', players, players[:5])

if len(selected_players) == 5:
    # Calculate league average of PLUS_MINUS, FG_PCT, FG3_PCT
    league_avg_plus_minus = df['PLUS_MINUS'].mean()
    league_avg_fg_pct = df['FG_PCT'].mean()
    league_avg_fg3_pct = df['FG3_PCT'].mean()

    # Visualize selected players' statistics in comparison to league average
    selected_players_df = team_df[team_df['players_list'].apply(lambda x: set(x.split(',')) == set(selected_players))]
    selected_players_plus_minus_avg = selected_players_df['PLUS_MINUS'].mean()
    selected_players_fg_pct_avg = selected_players_df['FG_PCT'].mean()
    selected_players_fg3_pct_avg = selected_players_df['FG3_PCT'].mean()

    st.write(f"League average PLUS_MINUS: {league_avg_plus_minus}")
    st.write(f"League average FG_PCT: {league_avg_fg_pct}")
    st.write(f"League average FG3_PCT: {league_avg_fg3_pct}")

    st.write(f"Selected players' average PLUS_MINUS: {selected_players_plus_minus_avg}")
    st.write(f"Selected players' average FG_PCT: {selected_players_fg_pct_avg}")
    st.write(f"Selected players' average FG3_PCT: {selected_players_fg3_pct_avg}")

    # You can further visualize the comparison using plots or charts
else:
    st.warning("Please select exactly 5 players.")


def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
    unsafe_allow_html=True
    )
add_bg_from_local('bg.png')





