"""
Final Project
Name: Nick Codianni
"""

import streamlit as st
import pandas as pd
import pydeck as pdk
import matplotlib.pyplot as plt


df = pd.read_csv("Meteorite_Landings.csv")

# Convert year to numeric
df["year"] = pd.to_numeric(df["year"], errors="coerce")

# Drop invalid/missing years
df = df.dropna(subset=["year"])

# Limit data to realistic years
df = df[(df["year"] >= 1963) & (df["year"] <= 2013)]

# Drop rows without coordinates (required for map)
df = df.dropna(subset=["reclat", "reclong"])

# Convert year to int for dropdown cleanliness
df["year"] = df["year"].astype(int)


st.title("Meteorite Landings Explorer")

st.write("Explore meteorite landings from the NASA dataset.")


# Build dropdown list: All Years + sorted list of years
year_options = ["All Years"] + sorted(df["year"].unique().tolist())

selected_year = st.selectbox("Select a year:", year_options)

# Filter based on selection
if selected_year == "All Years":
    filtered_df = df.copy()
else:
    filtered_df = df[df["year"] == selected_year]

st.subheader(f"Showing meteorites from: **{selected_year}**")
st.write(f"Total meteorites: **{len(filtered_df)}**")


if len(filtered_df) > 0:
    st.pydeck_chart(
        pdk.Deck(
            map_style="mapbox://styles/mapbox/light-v9",
            initial_view_state=pdk.ViewState(
                latitude=20,
                longitude=0,
                zoom=1,
                pitch=0,
            ),
            layers=[
                pdk.Layer(
                    "ScatterplotLayer",
                    data=filtered_df,
                    get_position='[reclong, reclat]',
                    get_radius=50000,
                    get_color=[255, 60, 60],
                    pickable=True
                )
            ],
        )
    )
else:
    st.write("No meteorites recorded for this year.")


st.subheader("Meteorite Data Table")
st.dataframe(filtered_df[["name", "id", "mass (g)", "year", "reclat", "reclong"]])


st.subheader("Meteorite Statistics")

# 1. Bar chart: Count of meteorites per year
counts = df["year"].value_counts().sort_index()

fig1, ax1 = plt.subplots(figsize=(10, 4))
ax1.bar(counts.index, counts.values)
ax1.set_title("Meteorite Count by Year")
ax1.set_xlabel("Year")
ax1.set_ylabel("Count")
st.pyplot(fig1)

# 2. Bar chart: Average mass per year
mass_by_year = df.groupby("year")["mass (g)"].mean()

fig2, ax2 = plt.subplots(figsize=(10, 4))
ax2.bar(mass_by_year.index, mass_by_year.values)
ax2.set_title("Average Meteorite Mass by Year")
ax2.set_xlabel("Year")
ax2.set_ylabel("Average Mass (g)")
st.pyplot(fig2)





