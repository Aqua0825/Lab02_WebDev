
# This creates the page for displaying data visualizations.

import streamlit as st
import json
import matplotlib.pyplot as plt
import pandas as pd

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Visuals",
    page_icon="📈",
)

# PAGE TITLE
st.title("Data Visualizations 📈")
tab1, tab2 = st.tabs(["Video Game Data", "Survey Data"])

with tab1:
# PART 1: GRAPHS FROM data.json

    with open("data.json", "r") as file:
        data = json.load(file)

    games = data["data_points"]

# STATIC VISUALIZATION: PIE CHART BY GENRE
    genreSales = {}
    for game in games:
        genre = game["genre"]
        sales = game["sales"]
        if genre not in genreSales:
            genreSales[genre] = 0
        genreSales[genre] += sales
    st.subheader("Video Game Sales by Genre")
    
    fig, ax = plt.subplots(figsize = (10,7))
    wedges, title, autotexts = ax.pie(genreSales.values(), labels=None, autopct="%1.1f%%")
    ax.set_title(data["chart_title"])

    ax.legend(wedges, genreSales.keys(), title="Genres", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1), fontsize=9)
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

    # DYNAMIC VISUALIZATION: TOP-SELLING GAMES BY PLATFORM

    st.subheader("Top-Selling Games by Platform")
    platforms = []
    for game in games:
        if game["platform"] not in platforms:
            platforms.append(game["platform"])
    platformOptions = ["All"] + platforms
    if "platform" not in st.session_state:
        st.session_state["platform"] = "All"
    selectedPlatform = st.selectbox(
        "Choose a platform",
        platformOptions,
        key="platform"
    )
    platformGames = []
    for game in games:
        if selectedPlatform == "All" or game["platform"] == selectedPlatform:
            platformGames.append(game)

    platformGames.sort(key=lambda game: game["sales"], reverse=True)

    fig2, ax2 = plt.subplots(figsize=(8, 4))
    gameNames = []
    gameSales = []
    for game in platformGames:
        gameNames.append(game["title"])
        gameSales.append(game["sales"])

    ax2.bar(gameNames, gameSales)
    ax2.set_title("Top-Selling Games on " + selectedPlatform)
    ax2.set_xlabel("Game")
    ax2.set_ylabel("Sales (millions)")
    plt.xticks(rotation=45, ha="right", fontsize=8)
    fig2.tight_layout()

    st.pyplot(fig2)
    plt.close(fig2)

with tab2:
# PART 2: GRAPHS FROM data.csv
# --- YOUR CODE GOES HERE ---
    data = pd.read_csv("data.csv")
    st.subheader("DATA FROM SURVEY")
    st.dataframe(data)
    averageRatings = data.groupby("Genre")["Rating"].mean()

    st.subheader("Average Rating by Genre")
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(averageRatings.index, averageRatings.values)
    ax.set_title("Average Rating by Genre")
    ax.set_xlabel("Genre")
    ax.set_ylabel("Average Rating")
    st.pyplot(fig)
    plt.close(fig)

    st.subheader("Hours Played vs. Game Rating")
    platforms = data["Platform"].unique().tolist()
    platformOptions = ["All"] + platforms
    selectedPlatform = st.selectbox(
        "Choose a platform:",
        platformOptions,
        key="surveyPlatform"
    )
    if selectedPlatform == "All":
        filteredData = data
    else:
        filteredData = data[data["Platform"] == selectedPlatform]
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.scatter(filteredData["Hours"], filteredData["Rating"])
    ax.set_title("Hours Played vs. Game Rating")
    ax.set_xlabel("Hours Played")
    ax.set_ylabel("Rating (out of 10)")
    ax.set_ylim(0, 15)
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)
