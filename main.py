"""Name: 
Tnaliyev Mirlan
CS230: Section XXX
Data: Which data set you used
Description:
This program ... (a few sentences about your program and the queries and charts)
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import folium


# ident,type,name,elevation_ft,continent,iso_country,iso_region,municipality,gps_code,iata_code,local_code,coordinates
columns = {
}

# Load the CSV file into a DataFrame
df = pd.read_csv("airports.csv")

# Set up the Streamlit UI
st.title("Airports Data Visualization")
st.sidebar.title("Filters")

# Add interactive widgets for filtering
country = st.sidebar.selectbox("Select a country", df["iso_country"].unique())
elevation = st.sidebar.slider("Select minimum elevation (ft)", min_value=0, max_value=15000, value=0)

# Filter the DataFrame based on user input
filtered_df = df[(df["iso_country"] == country) & (df["elevation_ft"] >= elevation)]

# Display a data table of the filtered results
st.write(f"Showing {len(filtered_df)} airports in {country} with elevation >= {elevation} ft")
st.write(filtered_df)

# Create a bar chart showing the number of airports in each country
fig1 = px.histogram(df, x="iso_country", title="Number of airports in each country")
st.plotly_chart(fig1)

# Create a histogram showing the distribution of airport elevations
fig2 = px.histogram(df, x="elevation_ft", nbins=20, title="Distribution of airport elevations")
st.plotly_chart(fig2)

# Create a scatter plot showing the location of each airport on a map
m = folium.Map(location=[df["coordinates"].str.split(",", expand=True).iloc[0, 1], df["coordinates"].str.split(",", expand=True).iloc[0, 0]], zoom_start=3)

for index, row in df.iterrows():
    lat, lon = row["coordinates"].split(", ")
    folium.Marker([float(lon), float(lat)], popup=row["name"]).add_to(m)

st.write("Map showing the location of each airport")
st.write(m)