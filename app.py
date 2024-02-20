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


# User chooses team
team = st.selectbox(
     'Choose Your Team:',
     df['team'].unique())


df_team = df[df['team'] == team].reset_index(drop=True)
df_team['players_list'] = df_team['players_list'].str.replace(r"[\"\' \[\]]", '').str.split(',')
duplicate_roster = df_team['players_list'].apply(pd.Series).stack()
uniq_names = set(duplicate_roster)
roster = [player.replace('[', '').replace(']', '').strip("'").replace("'", "") for player in uniq_names]



# Allow user to select players randomly
players = st.multiselect(
     'Select your players',
     roster,
     roster[0:5])

# Check if exactly 5 players are selected
if len(players) == 5:
    # Find the lineup that matches the selected players
    # Ensure that player names in df_team are stripped of square brackets too
    df_team['players_list_stripped'] = df_team['players_list'].apply(lambda x: [p.replace('[', '').replace(']', '').strip("'").replace("'", "") for p in x])
    df_lineup = df_team[df_team['players_list_stripped'].apply(lambda x: set(x) == set(players))]

    # Check if a lineup is found
    if not df_lineup.empty:
        df_important = df_lineup[['MIN', 'PLUS_MINUS','FG_PCT', 'FG3_PCT']]

        st.dataframe(df_important)

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            fig_min = px.histogram(df_team, x="MIN")
            fig_min.add_vline(x=df_important['MIN'].values[0],line_color='red',name='Selected Players')
            fig_min.add_vline(x=df_team['MIN'].mean(),line_color='green',name='Team Mean')
            st.plotly_chart(fig_min, use_container_width=True)

        with col2:
            fig_2 = px.histogram(df_team, x="PLUS_MINUS")
            fig_2.add_vline(x=df_important['PLUS_MINUS'].values[0],line_color='red',name='Selected Players')
            fig_2.add_vline(x=df_team['PLUS_MINUS'].mean(),line_color='green',name='Team Mean')
            st.plotly_chart(fig_2, use_container_width=True)

        with col3:
            fig_3 = px.histogram(df_team, x="FG_PCT")
            fig_3.add_vline(x=df_important['FG_PCT'].values[0],line_color='red',name='Selected Players')
            fig_3.add_vline(x=df_team['FG_PCT'].mean(),line_color='green',name='Team Mean')
            st.plotly_chart(fig_3, use_container_width=True)

        with col4:
            fig_4 = px.histogram(df_team, x="FG3_PCT")
            fig_4.add_vline(x=df_important['FG3_PCT'].values[0],line_color='red',name='Selected Players')
            fig_4.add_vline(x=df_team['FG3_PCT'].mean(),line_color='green',name='Team Mean')
            st.plotly_chart(fig_4, use_container_width=True)
    else:
        st.warning("No lineup found for the selected players.")
else:
    st.warning("Please select exactly 5 players for the lineup.")




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





