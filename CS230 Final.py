"""Name:
Tnaliyev Mirlan
CS230 Final Project
Data: Airports Around the World
Description:
    This program improts the dataset "Airports" and create interactive  dashboards on Streamlit platform, thus, allowing to display insughts from the massive data. It utilizes filtering through data, includes widgets, and generally have vizualisations using Python libraries
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import folium
import matplotlib.plt as plt


# Load the CSV file into a DataFrame
df = pd.read_csv("airports.csv")
first_fifty = filtered_df = df.head(50)

# Set up the Streamlit UI
st.title("Airports Data Visualization")
st.sidebar.title("Filters")


# Add interactive widgets for filtering
country = st.sidebar.selectbox("Select a country", sorted(df["iso_country"]).unique())
elevation = st.sidebar.slider("Select minimum elevation (ft)", min_value=0, max_value=15000, value=0)
types = st.sidebar.multiselect("Select airport types", df["type"].unique())

# Filter the DataFrame based on user input
filtered_df= df[(df["iso_country"] == country) & (df["elevation_ft"] >= elevation) & (df["type"].isin(types))]

# Display a data table of the filtered results
st.write(f"Showing {len(filtered_df)} airports in {country} with elevation >= {elevation} ft and selected types: {types}")
st.write(filtered_df)

# Create a bar chart showing the number of airports in each country
fig1 = px.histogram(df, x="iso_country", title="Number of airports in each country")
st.plotly_chart(fig1)

# Create a histogram showing the distribution of airport elevations
fig2 = px.histogram(filtered_df, x="elevation_ft", nbins=20, title="Distribution of airport elevations")
st.plotly_chart(fig2)


# Create a pie chart showing the distribution of airport categories
fig3 = px.pie(filtered_df, names='type', title="Distribution of airport categories")
st.plotly_chart(fig3)


# Create a scatter plot showing the location of each airport on a map
m = folium.Map(location=[filtered_df["coordinates"].str.split(",", expand=True).iloc[0, 1], filtered_df["coordinates"].str.split(",", expand=True).iloc[0, 0]], zoom_start=3)

for index, row in df.iterrows():
     lat, lon = row["coordinates"].split(", ")
     folium.Marker([float(lon), float(lat)], popup=row["name"]).add_to(m)
     break

st.write("Map showing the location of each airport")
st.write(m)

