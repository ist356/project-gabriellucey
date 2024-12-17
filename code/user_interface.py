import pandas as pd
import streamlit as st
import folium
import streamlit_folium as sf
from folium import Marker
from folium.plugins import AntPath
import plotly.express as px

#load in data from cache
FILE = "./cache/nfl_team_stats.csv"
df = pd.read_csv(FILE)

#function to generate folium map
def generate_map(team1, team2):
    team1_data = df[df['team'] == team1].iloc[0]
    team2_data = df[df['team'] == team2].iloc[0]
    
    #Create the map centered between the two stadiums
    center_lat = (team1_data['latitude'] + team2_data['latitude']) / 2
    center_lon = (team1_data['longitude'] + team2_data['longitude']) / 2
    nfl_map = folium.Map(location=[center_lat, center_lon], zoom_start=4)

    #new function AntPath to draw a line between the two stadiums
    Marker([team1_data['latitude'], team1_data['longitude']], popup=team1).add_to(nfl_map)
    Marker([team2_data['latitude'], team2_data['longitude']], popup=team2).add_to(nfl_map)
    AntPath([[team1_data['latitude'], team1_data['longitude']],
             [team2_data['latitude'], team2_data['longitude']]], color="blue", weight=3).add_to(nfl_map)
    
    return nfl_map


st.title(":football: NFL Team Statistics Comparison")

#create dropdowns for team selection
team_options = df['team'].unique()
team1 = st.selectbox("Select Team 1", team_options, key="team1")
team2 = st.selectbox("Select Team 2", team_options, key="team2")

if "button_clicked" not in st.session_state:
    st.session_state.button_clicked = False

#callback function for button click
def handle_button_click():
    st.session_state.button_clicked = True

st.button(":mag: Generate Statistics Comparison", on_click=handle_button_click)

#display stats comparison if button is clicked
if st.session_state.button_clicked:
    if team1 == team2:
        st.warning(":exclamation: Please select two different teams.")
    else:
        st.subheader(f":bar_chart: Comparing **{team1}** vs **{team2}**")

        #dropdown for selecting stat to compare and removing unnecessary columns
        stat_options = df.columns.drop(['team', 'latitude', 'longitude'])
        selected_stat = st.selectbox("Select Stat to Compare", stat_options, key="stat_select")

        #get values for selected teams and display NFL average and leader
        team1_value = df.loc[df['team'] == team1, selected_stat].values[0]
        team2_value = df.loc[df['team'] == team2, selected_stat].values[0]
        nfl_average = df[selected_stat].mean()
        nfl_leader_team = df.loc[df[selected_stat] == df[selected_stat].max(), 'team'].values[0]
        nfl_leader_value = df[selected_stat].max()
        st.markdown(f"**:trophy: NFL Average for {selected_stat}:** `{nfl_average:.4f}`")
        st.markdown(f"**:medal: NFL Leader in {selected_stat}:** `{nfl_leader_team} ({nfl_leader_value})`")

        #use plotly express to create interactive bar chart
        stats_data = pd.DataFrame({
            "Team": [team1, team2, "NFL Average", f"Leader: {nfl_leader_team}"],
            "Value": [team1_value, team2_value, nfl_average, nfl_leader_value],
            "Color": ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728"]
        })

        fig = px.bar(
            stats_data,
            x="Team",
            y="Value",
            title=f"{selected_stat} Comparison",
            color="Team",
            color_discrete_sequence=stats_data["Color"],
            hover_data={"Value": True, "Team": True} #show value and team name on hover
        )
        st.plotly_chart(fig, use_container_width=True)

        #use sf.st_folium to display map
        st.subheader(":round_pushpin: Stadium Locations")
        nfl_map = generate_map(team1, team2)
        sf.st_folium(nfl_map, width=700, height=500)
