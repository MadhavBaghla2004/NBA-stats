import pandas as pd
import streamlit as st
import plotly.express as px
import base64




# import data
df = pd.read_csv('NBAlineup.csv')


# Title for app
st.set_page_config(layout="wide")
st.title('NBA Lineup Analysis Tool')
st.markdown("""
```  
Using this tool we can analyse some key statistics in the NBA for the 2021-22 season, picking our best starting lineup.
You can see the difference in 4 key metrics- namely <span style="color: green;">minutes</span>, <span style="color: green;">plus minus</span>, <span style="color: green;">field goal percentage</span>, and <span style="color: green;">3 point percentage</span>.
We can pick the best starting lineup using these <span style="color: orange;"> four key metrics.
```
""",True)


# User chooses team
team = st.selectbox(
     'Choose Your Team:',
     df['team'].unique())

df_team = df[df['team'] == team].reset_index(drop=True)
df_team['players_list'] = df_team['players_list'].str.replace(r"[\"\' \[\]]", '').str.split(',')
df_team['FG_PCT'] = (df_team['FG_PCT'] * 100).round(2)
df_team['FG3_PCT'] = (df_team['FG3_PCT'] * 100).round(2)
duplicate_roster = df_team['players_list'].apply(pd.Series).stack()
roster = duplicate_roster.unique()
roster = [player.replace('[', '').replace(']', '').strip().strip("'").replace("'", "") for player in roster]
roster = list(set(roster))
roster.sort() 




# Allow user to select players randomly without a default selection
players = st.multiselect(
     'Select your players',
     roster)




# Check if exactly 5 players are selected
if len(players) == 5:
    df_team['players_list_stripped'] = df_team['players_list'].apply(lambda x: [p.replace('[', '').replace(']', '').strip().strip("'").replace("'", "")for p in x])
    # Filter df_team based on FG_PCT matching for a given set of players
    df_lineup = df_team[df_team['players_list_stripped'].apply(lambda x: set(x)==set(players))]

  

    # Check if a lineup is found
    if not df_lineup.empty:
     
        df_important = df_lineup[['MIN', 'PLUS_MINUS','FG_PCT', 'FG3_PCT']].reset_index(drop=True)
        df_display=df_important.copy()
        df_display.columns = ['MINUTES', 'PLUS_MINUS', 'FG_PERCENTAGE', '3_POINT_PERCENTAGE']

        df_display['STAT'] = 'VALUE'
        df_display.set_index('STAT', inplace=True)
        st.markdown(
   """
    <style>
    table {
        color: white;
        background-color: #333333;
    }
    </style>
    """,
    unsafe_allow_html=True
)

        st.table(df_display)

        with st.container():
            fig = px.scatter(df_team, x="MIN", y="GP", title="Scatter Plot of Minutes vs. Games Played For the Squad",
                            hover_data={'MIN': True, 'GP': True, 'GROUP_NAME': 'True'})
            fig.update_traces(hovertemplate='Minutes: %{x}<br>Games played: %{y}<br>Lineup: %{customdata[0]}')
            fig.update_xaxes(title_text="MINUTES")
            fig.update_yaxes(title_text="GAMES PLAYED")
            min_value = df_important['MIN'].values[0]
            gp_value = df_lineup['GP'].values[0]
            group_name = df_lineup['GROUP_NAME'].values[0]
            fig.add_scatter(x=[min_value], y=[gp_value], mode="markers", marker=dict(color='green', size=10, opacity=1), name="Selected lineup", 
                  text=[f"MINUTES: {min_value}<br>GAMES_PLAYED: {gp_value}<br>LINEUP: {group_name}"], hoverinfo="text")
            mean_min = round(df_team['MIN'].mean(), 2)
            fig.add_vline(x=mean_min, line_dash="dot", line_color="red", annotation_text=f"Team Mean: {mean_min}", annotation_position="bottom right")
            fig.update_traces(marker=dict(size=20, opacity=1))
            st.plotly_chart(fig, use_container_width=True)

            fig2 = px.scatter(df_team, x="PLUS_MINUS", y="GP", title="Scatter Plot of Plus/Minus vs. Games Played For the Squad",
                            hover_data={'PLUS_MINUS': True, 'GP': True, 'GROUP_NAME': 'True'})
            fig2.update_traces(hovertemplate='Plus/Minus: %{x}<br>Games played: %{y}<br>Lineup: %{customdata[0]}')
            fig2.update_xaxes(title_text="PLUS/MINUS")
            fig2.update_yaxes(title_text="GAMES PLAYED")
            plus_minus_value = df_important['PLUS_MINUS'].values[0]
            gp_value = df_lineup['GP'].values[0]
            group_name = df_lineup['GROUP_NAME'].values[0]
            fig2.add_scatter(x=[plus_minus_value], y=[gp_value], mode="markers", marker=dict(color='green', size=10, opacity=1), name="Selected lineup", 
               text=[f"PLUS/MINUS: {plus_minus_value}<br>GAMES_PLAYED: {gp_value}<br>LINEUP: {group_name}"], hoverinfo="text")
            mean_plusminus = round(df_team['PLUS_MINUS'].mean(),2)
            fig2.add_vline(x=mean_plusminus, line_dash="dot", line_color="red", annotation_text=f"Team Mean: {mean_plusminus}", annotation_position="bottom right")
            fig2.update_traces(marker=dict(size=20, opacity=1))
            st.plotly_chart(fig2, use_container_width=True)


          

            fig3 = px.scatter(df_team, x="FG_PCT", y="GP", title="Scatter Plot of Field Goal Percentage vs. Games Played For the Squad",
                            hover_data={'FG_PCT': True, 'GP': True, 'GROUP_NAME': 'True'})
            fig3.update_traces(hovertemplate='Field Goal Percentage: %{x}<br>Games played: %{y}<br>Lineup: %{customdata[0]}')
            fig3.update_xaxes(title_text="Field Goal Percentage")
            fig3.update_yaxes(title_text="GAMES PLAYED")
            fg_pct_value = df_important['FG_PCT'].values[0]
            gp_value = df_lineup['GP'].values[0]
            group_name = df_lineup['GROUP_NAME'].values[0]
            fig3.add_scatter(x=[fg_pct_value], y=[gp_value], mode="markers", marker=dict(color='green', size=10, opacity=1), name="Selected lineup", 
               text=[f"Field Goal Percentage: {fg_pct_value}<br>GAMES_PLAYED: {gp_value}<br>LINEUP: {group_name}"], hoverinfo="text")
            mean_fg_pct = round(df_team['FG_PCT'].mean(),2)
            fig3.add_vline(x=mean_fg_pct, line_dash="dot", line_color="red", annotation_text=f"Team Mean: {mean_fg_pct}", annotation_position="bottom right")
            fig3.update_traces(marker=dict(size=20, opacity=1))
            st.plotly_chart(fig3, use_container_width=True)

            fig4 = px.scatter(df_team, x="FG3_PCT", y="GP", title="Scatter Plot of 3-Point Field Goal Percentage vs. Games Played For the Squad",
                            hover_data={'FG3_PCT': True, 'GP': True, 'GROUP_NAME': 'True'})
            fig4.update_traces(hovertemplate='3-Point Field Goal Percentage: %{x}<br>Games played: %{y}<br>Lineup: %{customdata[0]}')
            fig4.update_xaxes(title_text="3-Point Field Goal Percentage")
            fig4.update_yaxes(title_text="GAMES PLAYED")
            fg3_pct_value = df_important['FG3_PCT'].values[0]
            gp_value = df_lineup['GP'].values[0]
            group_name = df_lineup['GROUP_NAME'].values[0]
            fig4.add_scatter(x=[fg3_pct_value], y=[gp_value], mode="markers", marker=dict(color='green', size=10, opacity=1), name="Selected lineup", 
               text=[f"3-Point Field Goal Percentage: {fg3_pct_value}<br>GAMES_PLAYED: {gp_value}<br>LINEUP: {group_name}"], hoverinfo="text")
            mean_fg3_pct = round(df_team['FG3_PCT'].mean(),2)
            fig4.add_vline(x=mean_fg3_pct, line_dash="dot", line_color="red", annotation_text=f"Team Mean: {mean_fg3_pct}", annotation_position="bottom right")
            fig4.update_traces(marker=dict(size=20, opacity=1))
            st.plotly_chart(fig4, use_container_width=True)



     
    else:
        possible_lineup = df_team.loc[0, 'players_list_stripped']
        warning_message="This group of players did not play together this season, hence there is no data available. Please select a different group."
        possible_lineup_message = f"Possible lineup: {possible_lineup}"
        st.warning(warning_message)
        st.write(f'<span style="color:pink; font-weight:bold; background-color:blue; padding: 5px;">{possible_lineup_message}</span>', unsafe_allow_html=True)

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










