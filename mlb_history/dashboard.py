#4. Dashboard Program


import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

# Connect to your database
conn = sqlite3.connect('../mlb_database_import/mlb_history.db')

# Load data
@st.cache_data
def load_stats():
    return pd.read_sql("SELECT * FROM mlb_stats", conn)

@st.cache_data
def load_events():
    return pd.read_sql("SELECT * FROM mlb_events", conn)

stats_df = load_stats()
events_df = load_events()

# Sidebar controls
st.sidebar.title("MLB Dashboard Filters")
selected_year = st.sidebar.selectbox("Select Year", sorted(stats_df['year'].unique(), reverse=True))
selected_category = st.sidebar.selectbox("Select Stat Category", stats_df['category'].unique())

# Title
st.title("MLB History Dashboard")
st.caption("Visualize top players and events from baseball history")

#Visusalisatin1 Number of stat records per year - this bar chart displays the number of stat records recorded in the
#dataset for each year. It offers a quick snapshot of how comrehensive the data is across time,highlighting which data
#which seasons are mostly represented. Spikes reflect years with more complete coverage or expanded stat tracking,
#while dips can indicate gaps in historical data or limited availability
st.subheader("Number of Stat Records Per Year")

yearly_counts = stats_df['year'].value_counts().reset_index()
yearly_counts.columns = ['year', 'count']
yearly_counts = yearly_counts.sort_values(by='year')

fig = px.bar(
    yearly_counts,
    x='year',
    y='count',
    title='Stat Records by Year',
    text='count'
)
st.plotly_chart(fig, use_container_width=True)

    
    #Visualization2 Player appearance across the stats- tis bar chart shows the 15 players who appear most frequently
    #across all statistical categories in the dataset. A higher number of appearances may indicate consistent performance,
    #dominance in multiple areas of game. The visualization provides a broad view of which athletes have left the biggest,
    #statistical footpronts,regardless of position or speciality.
    
st.subheader("Players with the Most Stat Entries")

player_counts = stats_df['player'].value_counts().reset_index().head(15)
player_counts.columns = ['player', 'appearances']

fig = px.bar(
    player_counts,
    x='player',
    y='appearances',
    title='Top 15 Most Represented Players',
    text='appearances'
)
st.plotly_chart(fig, use_container_width=True)


#  Visualization 3: World Series Titles by Team - this pie chart visualizes which teams have won the most World Series title,
#within the selected year range. Each slice represents a team's share of championships,making it easy to spot dynasties,
#or shifts in dominance across baseball eras. By adjusting the slider,users can explore how powerhouse have risen
#or faded overtime in the postseason spotlight.

st.subheader("World Series Titles by Team")

year_range = st.slider(
    "Select Year Range",
    int(events_df['year'].min()),
    int(events_df['year'].max()),
    (1980, 2020)
)

series = events_df[
    (events_df['year'] >= year_range[0]) &
    (events_df['year'] <= year_range[1])
]

series_filtered = series['world_series'].dropna()
filtered_ws = series_filtered.value_counts().reset_index()
filtered_ws.columns = ['team', 'count']

fig = px.pie(
    filtered_ws,
    names='team',
    values='count',
    title='World Series Titles (Selected Range)'
)
st.plotly_chart(fig, use_container_width=True)
