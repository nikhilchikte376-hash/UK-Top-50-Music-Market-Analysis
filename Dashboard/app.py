import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="UK Top 50 Music Market Analysis",
    page_icon="🎵",
    layout="wide"
)


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():

    # Project root -> Data folder
    project_root = Path(__file__).resolve().parent.parent

    data_path = (
        project_root
        / "Data"
        / "Atlantic_United_Kingdom.csv"
    )

    df = pd.read_csv(data_path)

    return df


df = load_data()


# ============================================================
# DATA PREPARATION
# ============================================================

df["date"] = pd.to_datetime(
    df["date"],
    errors="coerce"
)

df["position"] = pd.to_numeric(
    df["position"],
    errors="coerce"
)

df["popularity"] = pd.to_numeric(
    df["popularity"],
    errors="coerce"
)

df["duration_ms"] = pd.to_numeric(
    df["duration_ms"],
    errors="coerce"
)


# ============================================================
# TRACK DURATION IN MINUTES
# ============================================================

df["duration_minutes"] = (
    df["duration_ms"] / 60000
)


# ============================================================
# CREATE RANK GROUP
# ============================================================

def create_rank_group(position):

    if pd.isna(position):
        return "Unknown"

    if position <= 10:
        return "Top 10"

    elif position <= 25:
        return "11-25"

    else:
        return "26-50"


df["rank_group"] = df["position"].apply(
    create_rank_group
)


# ============================================================
# DASHBOARD TITLE
# ============================================================

st.title(
    "🎵 UK Top 50 Music Market Analysis"
)

st.markdown(
    """
    ### Interactive Music Market Dashboard

    Explore UK Top 50 chart performance through artist appearances,
    song popularity, chart position, track duration, and explicit
    content analysis.
    """
)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title(
    "🔎 Dashboard Filters"
)

st.sidebar.markdown(
    "Use the filters below to explore the dataset."
)


# ============================================================
# ARTIST FILTER
# ============================================================

artist_list = sorted(
    df["artist"]
    .dropna()
    .unique()
)

selected_artists = st.sidebar.multiselect(
    "🎤 Select Artist",
    artist_list,
    key="artist_filter"
)


# ============================================================
# RANK GROUP FILTER
# ============================================================

rank_group_options = [
    "All Rank Groups",
    "Top 10",
    "11-25",
    "26-50",
    "Unknown"
]

selected_rank_groups = st.sidebar.multiselect(
    "🏆 Select Rank Group",
    rank_group_options,
    default=["All Rank Groups"],
    key="rank_group_filter_final"
)


# ============================================================
# EXPLICIT CONTENT FILTER
# ============================================================

explicit_filter = st.sidebar.selectbox(
    "🔞 Explicit Content",
    [
        "All",
        "Explicit",
        "Non-Explicit"
    ],
    key="explicit_filter"
)


# ============================================================
# DATE FILTER
# ============================================================

st.sidebar.subheader(
    "📅 Date Filter"
)

date_filter_option = st.sidebar.radio(
    "Select Date Range",
    [
        "All Dates",
        "Custom Date Range"
    ],
    key="date_filter_option"
)

if date_filter_option == "Custom Date Range":

    min_date = df["date"].min().date()
    max_date = df["date"].max().date()

    selected_date_range = st.sidebar.date_input(
        "Choose Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
        key="custom_date_filter"
    )


# ============================================================
# APPLY FILTERS
# ============================================================

filtered_df = df.copy()


# ------------------------------------------------------------
# DATE FILTER
# ------------------------------------------------------------

if date_filter_option == "Custom Date Range":

    if len(selected_date_range) == 2:

        start_date, end_date = selected_date_range

        filtered_df = filtered_df[
            (filtered_df["date"].dt.date >= start_date)
            &
            (filtered_df["date"].dt.date <= end_date)
        ]


# ------------------------------------------------------------
# ARTIST FILTER
# ------------------------------------------------------------

if selected_artists:

    filtered_df = filtered_df[
        filtered_df["artist"].isin(
            selected_artists
        )
    ]


# ------------------------------------------------------------
# RANK GROUP FILTER
# ------------------------------------------------------------

if (
    selected_rank_groups
    and "All Rank Groups" not in selected_rank_groups
):

    filtered_df = filtered_df[
        filtered_df["rank_group"].isin(
            selected_rank_groups
        )
    ]


# ------------------------------------------------------------
# EXPLICIT CONTENT FILTER
# ------------------------------------------------------------

if explicit_filter == "Explicit":

    filtered_df = filtered_df[
        filtered_df["is_explicit"] == True
    ]


elif explicit_filter == "Non-Explicit":

    filtered_df = filtered_df[
        filtered_df["is_explicit"] == False
    ]


# ============================================================
# KPI SECTION
# ============================================================

st.subheader(
    "📊 Key Performance Indicators"
)

col1, col2, col3, col4 = st.columns(4)


# Total records
col1.metric(
    "Chart Records",
    f"{len(filtered_df):,}"
)


# Unique artists
col2.metric(
    "Unique Artists",
    f"{filtered_df['artist'].nunique():,}"
)


# Unique songs
col3.metric(
    "Unique Songs",
    f"{filtered_df['song'].nunique():,}"
)


# Average popularity
if len(filtered_df) > 0:

    avg_popularity = (
        filtered_df["popularity"].mean()
    )

else:

    avg_popularity = 0


col4.metric(
    "Avg. Popularity",
    f"{avg_popularity:.2f}"
)


# ============================================================
# DIVIDER
# ============================================================

st.markdown("---")


# ============================================================
# TOP 10 ARTISTS
# ============================================================

st.subheader(
    "🏆 Top 10 Artists by Chart Appearances"
)

top_artists = (
    filtered_df["artist"]
    .value_counts()
    .head(10)
)


if not top_artists.empty:

    fig, ax = plt.subplots(
        figsize=(10, 5)
    )

    top_artists.sort_values().plot(
        kind="barh",
        ax=ax
    )

    ax.set_xlabel(
        "Chart Appearances"
    )

    ax.set_ylabel(
        "Artist"
    )

    ax.set_title(
        "Top 10 Artists by Chart Appearances"
    )

    plt.tight_layout()

    st.pyplot(
        fig,
        use_container_width=False
    )

    plt.close(fig)

else:

    st.warning(
        "No artist data available for the selected filters."
    )


# ============================================================
# AVERAGE POPULARITY BY RANK GROUP
# ============================================================

st.subheader(
    "📈 Average Popularity by Rank Group"
)

popularity_by_rank = (
    filtered_df
    .groupby("rank_group")["popularity"]
    .mean()
    .reindex(
        ["Top 10", "11-25", "26-50"]
    )
)


if popularity_by_rank.notna().any():

    fig, ax = plt.subplots(
        figsize=(8, 5)
    )

    popularity_by_rank.plot(
        kind="bar",
        ax=ax
    )

    ax.set_xlabel(
        "Rank Group"
    )

    ax.set_ylabel(
        "Average Popularity"
    )

    ax.set_title(
        "Average Popularity by Rank Group"
    )

    plt.xticks(
        rotation=0
    )

    plt.tight_layout()

    st.pyplot(
        fig,
        use_container_width=False
    )

    plt.close(fig)

else:

    st.warning(
        "Popularity data is not available for the selected filters."
    )


# ============================================================
# AVERAGE TRACK DURATION
# ============================================================

st.subheader(
    "🎵 Average Track Duration by Rank Group"
)

duration_by_rank = (
    filtered_df
    .groupby("rank_group")["duration_minutes"]
    .mean()
    .reindex(
        ["Top 10", "11-25", "26-50"]
    )
)


if duration_by_rank.notna().any():

    fig, ax = plt.subplots(
        figsize=(8, 5)
    )

    duration_by_rank.plot(
        kind="bar",
        ax=ax
    )

    ax.set_xlabel(
        "Rank Group"
    )

    ax.set_ylabel(
        "Average Duration (Minutes)"
    )

    ax.set_title(
        "Average Track Duration by Rank Group"
    )

    plt.xticks(
        rotation=0
    )

    plt.tight_layout()

    st.pyplot(
        fig,
        use_container_width=False
    )

    plt.close(fig)

else:

    st.warning(
        "Duration data is not available for the selected filters."
    )


# ============================================================
# EXPLICIT CONTENT DISTRIBUTION
# ============================================================

st.subheader(
    "🔞 Explicit vs Non-Explicit Tracks"
)

explicit_counts = (
    filtered_df["is_explicit"]
    .value_counts()
)


if not explicit_counts.empty:

    explicit_counts.index = (
        explicit_counts.index.map(
            {
                True: "Explicit",
                False: "Non-Explicit"
            }
        )
    )

    # Smaller figure so the complete chart fits
    # properly inside the dashboard screenshot.
    fig, ax = plt.subplots(
        figsize=(6, 4)
    )

    ax.pie(
        explicit_counts.values,
        labels=explicit_counts.index,
        autopct="%1.1f%%",
        startangle=90,
        radius=0.85,
        pctdistance=0.60,
        labeldistance=1.05,
        textprops={
            "fontsize": 11
        }
    )

    ax.set_title(
        "Explicit Content Distribution",
        fontsize=15,
        pad=10
    )

    ax.axis("equal")

    plt.tight_layout(
        pad=1.0
    )

    st.pyplot(
        fig,
        use_container_width=False
    )

    plt.close(fig)

else:

    st.warning(
        "Explicit-content data is not available."
    )


# ============================================================
# TOP 10 SONGS
# ============================================================

st.subheader(
    "🎶 Top 10 Songs by Popularity"
)

top_songs = (
    filtered_df
    .sort_values(
        "popularity",
        ascending=False
    )
    [
        [
            "song",
            "artist",
            "popularity",
            "position"
        ]
    ]
    .head(10)
)


if not top_songs.empty:

    st.dataframe(
        top_songs,
        use_container_width=True,
        hide_index=True
    )

else:

    st.warning(
        "No song data available for the selected filters."
    )


# ============================================================
# BUSINESS INSIGHTS
# ============================================================

st.markdown("---")

st.subheader(
    "💡 Business Insights"
)

st.markdown(
    """
    ### 1. Strong Artist Concentration

    A relatively small number of artists account for a large
    number of repeated chart appearances. Taylor Swift has the
    highest number of appearances in the analyzed dataset.

    ### 2. Popularity and Chart Position

    Top 10 tracks have the highest average popularity compared
    with lower rank groups, indicating a relationship between
    chart position and popularity.

    ### 3. Track Duration

    Average track duration remains relatively similar across
    the different rank groups, suggesting that track length alone
    is not a major differentiator of chart performance.

    ### 4. Explicit Content

    Non-explicit tracks represent the majority of records in
    the analyzed dataset.

    ### 5. Market Diversity

    The dataset contains hundreds of artists and songs,
    demonstrating a broad range of music represented in the
    UK Top 50 market.
    """
)


# ============================================================
# DATASET SUMMARY
# ============================================================

st.markdown("---")

st.subheader(
    "📋 Dataset Summary"
)

summary_col1, summary_col2, summary_col3 = (
    st.columns(3)
)


summary_col1.metric(
    "Total Records",
    f"{len(df):,}"
)


summary_col2.metric(
    "Unique Artists",
    f"{df['artist'].nunique():,}"
)


summary_col3.metric(
    "Unique Songs",
    f"{df['song'].nunique():,}"
)


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.markdown(
    """
    **UK Top 50 Music Market Analysis**  
    Built by **Nikhil Chikte** | Data Analytics Project  
    Python • Pandas • Matplotlib • Streamlit
    """
)