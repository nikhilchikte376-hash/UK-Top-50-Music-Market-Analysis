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
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# DARK ANALYTICS THEME
# ============================================================
st.markdown("""
<style>
    :root {
        --bg: #090b16;
        --sidebar: #0d1020;
        --panel: #11162a;
        --panel2: #151a31;
        --text: #f6f7ff;
        --muted: #a8aec8;
        --purple: #9b7bff;
        --cyan: #54d8ff;
        --pink: #ff70b7;
        --border: rgba(155,123,255,0.20);
    }

    .stApp {
        background:
            radial-gradient(circle at 78% 0%, rgba(105,70,255,0.12), transparent 28rem),
            radial-gradient(circle at 20% 20%, rgba(84,216,255,0.06), transparent 24rem),
            var(--bg);
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d1020 0%, #0a0d19 100%);
        border-right: 1px solid rgba(155,123,255,0.18);
    }

    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #f6f7ff;
    }

    .block-container {
        padding-top: 3.5rem;
        padding-bottom: 2rem;
        max-width: 1500px;
    }

    h1, h2, h3, p, label {
        color: var(--text);
    }

    .hero {
        position: relative;
        overflow: hidden;
        padding: 1.45rem 1.55rem 1.35rem 1.55rem;
        margin-bottom: 1rem;
        border-radius: 18px;
        border: 1px solid rgba(155,123,255,0.24);
        background:
            linear-gradient(110deg, rgba(155,123,255,0.18), rgba(84,216,255,0.06) 55%, rgba(255,112,183,0.08)),
            #101426;
        box-shadow: 0 12px 34px rgba(0,0,0,0.22);
    }

    .hero-kicker {
        color: #a990ff;
        font-size: 0.78rem;
        font-weight: 800;
        letter-spacing: 0.18em;
        text-transform: uppercase;
        margin-bottom: 0.35rem;
    }

    .hero-title {
        color: #ffffff;
        font-size: 2.35rem;
        line-height: 1.05;
        font-weight: 900;
        letter-spacing: -0.04em;
        margin: 0;
    }

    .hero-title span {
        background: linear-gradient(90deg, #ffffff 0%, #bdaeff 48%, #65ddff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hero-subtitle {
        color: #b7bdd4;
        margin-top: 0.65rem;
        font-size: 0.98rem;
        line-height: 1.5;
        max-width: 900px;
    }

    .hero-meta {
        display: flex;
        flex-wrap: wrap;
        gap: 0.55rem;
        margin-top: 0.9rem;
    }

    .hero-pill {
        display: inline-block;
        color: #dfe3f6;
        background: rgba(255,255,255,0.055);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 999px;
        padding: 0.35rem 0.7rem;
        font-size: 0.78rem;
        font-weight: 650;
    }

    .section-label {
        color: #9b8cff;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        font-size: 0.75rem;
        font-weight: 800;
        margin: 0.25rem 0 0.7rem 0;
    }

    div[data-testid="stMetric"] {
        background: linear-gradient(145deg, rgba(21,26,49,0.98), rgba(14,18,35,0.98));
        border: 1px solid rgba(155,123,255,0.18);
        padding: 15px 17px;
        border-radius: 14px;
        min-height: 114px;
        box-shadow: 0 7px 20px rgba(0,0,0,0.16);
    }

    div[data-testid="stMetric"]:hover {
        border-color: rgba(84,216,255,0.35);
        transform: translateY(-1px);
        transition: 0.18s ease;
    }

    div[data-testid="stMetricLabel"] {
        color: #aeb5ce;
    }

    div[data-testid="stMetricValue"] {
        color: #ffffff;
        font-weight: 850;
    }

    div[data-testid="stMetricDelta"] {
        color: #65ddff;
    }

    [data-testid="stDataFrame"] {
        border: 1px solid rgba(155,123,255,0.18);
        border-radius: 14px;
        overflow: hidden;
    }

    .insight-box {
        background: linear-gradient(145deg, #13182d, #0f1325);
        border: 1px solid rgba(155,123,255,0.18);
        border-left: 3px solid #9b7bff;
        border-radius: 12px;
        padding: 1rem 1.1rem;
        margin-bottom: 0.75rem;
        color: #e6e8f5;
        min-height: 92px;
    }

    .small-note {
        color: #929ab7;
        font-size: 0.82rem;
        margin-bottom: 0.25rem;
    }

    hr {
        border-color: rgba(155,123,255,0.16);
    }

    .stButton > button {
        border-radius: 10px;
        border: 1px solid rgba(155,123,255,0.28);
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# LOAD DATA
# ============================================================
@st.cache_data
def load_data():
    project_root = Path(__file__).resolve().parent.parent
    data_path = project_root / "Data" / "Atlantic_United_Kingdom.csv"
    return pd.read_csv(data_path)

df = load_data()

# ============================================================
# DATA PREPARATION
# ============================================================
df["date"] = pd.to_datetime(df["date"], errors="coerce")
df["position"] = pd.to_numeric(df["position"], errors="coerce")
df["popularity"] = pd.to_numeric(df["popularity"], errors="coerce")
df["duration_ms"] = pd.to_numeric(df["duration_ms"], errors="coerce")
df["duration_minutes"] = df["duration_ms"] / 60000

def create_rank_group(position):
    if pd.isna(position):
        return "Unknown"
    if position <= 10:
        return "Top 10"
    elif position <= 25:
        return "11-25"
    return "26-50"

df["rank_group"] = df["position"].apply(create_rank_group)

# ============================================================
# MUSIC MARKET HERO
# ============================================================

min_year = int(df["date"].dt.year.min()) if df["date"].notna().any() else ""
max_year = int(df["date"].dt.year.max()) if df["date"].notna().any() else ""
year_label = f"{min_year}–{max_year}" if min_year != max_year else str(min_year)

st.markdown(
    f'<div class="hero">'
    f'<div class="hero-kicker">UK CHART INTELLIGENCE</div>'
    f'<div class="hero-title"><span>UK TOP 50</span><br>MUSIC MARKET ANALYSIS</div>'
    f'<div class="hero-subtitle">Discover the artists, songs and chart patterns shaping the UK music market through interactive analysis of popularity, rankings, content mix and track characteristics.</div>'
    f'<div class="hero-meta">'
    f'<span class="hero-pill">{year_label}</span>'
    f'<span class="hero-pill">{len(df):,} chart records</span>'
    f'<span class="hero-pill">{df["artist"].nunique():,} artists</span>'
    f'<span class="hero-pill">{df["song"].nunique():,} songs</span>'
    f'</div>'
    f'</div>',
    unsafe_allow_html=True
)

# ============================================================
# SIDEBAR FILTERS
# ============================================================
st.sidebar.markdown("## Explore the Charts")
st.sidebar.caption("Filter the market view. Every KPI and chart updates automatically.")

def reset_filters():
    keys = [
        "artist_filter",
        "rank_group_filter_final",
        "explicit_filter",
        "date_filter_option",
        "custom_date_filter"
    ]
    for key in keys:
        if key in st.session_state:
            del st.session_state[key]

st.sidebar.button(
    "↻ Reset Filters",
    use_container_width=True,
    on_click=reset_filters
)

artist_list = sorted(df["artist"].dropna().unique())

selected_artists = st.sidebar.multiselect(
    "Artist",
    artist_list,
    key="artist_filter"
)

rank_group_options = ["Top 10", "11-25", "26-50", "Unknown"]

selected_rank_groups = st.sidebar.multiselect(
    "Rank Group",
    rank_group_options,
    placeholder="All rank groups",
    key="rank_group_filter_final"
)

explicit_filter = st.sidebar.selectbox(
    "Explicit Content",
    ["All", "Explicit", "Non-Explicit"],
    key="explicit_filter"
)

st.sidebar.markdown("### Date Filter")

date_filter_option = st.sidebar.radio(
    "Date range",
    ["All Dates", "Custom Date Range"],
    key="date_filter_option"
)

selected_date_range = None
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

if (
    date_filter_option == "Custom Date Range"
    and selected_date_range is not None
    and len(selected_date_range) == 2
):
    start_date, end_date = selected_date_range
    filtered_df = filtered_df[
        (filtered_df["date"].dt.date >= start_date)
        & (filtered_df["date"].dt.date <= end_date)
    ]

if selected_artists:
    filtered_df = filtered_df[
        filtered_df["artist"].isin(selected_artists)
    ]

if selected_rank_groups:
    filtered_df = filtered_df[
        filtered_df["rank_group"].isin(selected_rank_groups)
    ]

if explicit_filter == "Explicit":
    filtered_df = filtered_df[filtered_df["is_explicit"] == True]
elif explicit_filter == "Non-Explicit":
    filtered_df = filtered_df[filtered_df["is_explicit"] == False]

# ============================================================
# FILTER STATUS
# ============================================================
remaining_pct = (
    len(filtered_df) / len(df) * 100
    if len(df) else 0
)

st.markdown(
    f'<div class="small-note">Showing <b>{len(filtered_df):,}</b> of '
    f'<b>{len(df):,}</b> records ({remaining_pct:.1f}% of dataset)</div>',
    unsafe_allow_html=True
)

if filtered_df.empty:
    st.warning("No records match the selected filters. Reset or change the filters.")
    st.stop()

# ============================================================
# KPI SECTION
# ============================================================
st.markdown('<div class="section-label">Market overview</div>', unsafe_allow_html=True)

avg_popularity = filtered_df["popularity"].mean()
top10_count = (filtered_df["rank_group"] == "Top 10").sum()
known_rank_count = filtered_df["rank_group"].isin(
    ["Top 10", "11-25", "26-50"]
).sum()
top10_share = (
    top10_count / known_rank_count * 100
    if known_rank_count else 0
)

k1, k2, k3, k4, k5 = st.columns(5)

k1.metric("Chart Records", f"{len(filtered_df):,}")
k2.metric("Unique Artists", f"{filtered_df['artist'].nunique():,}")
k3.metric("Unique Songs", f"{filtered_df['song'].nunique():,}")
k4.metric("Avg. Popularity", f"{avg_popularity:.2f}")
k5.metric("Top 10 Share", f"{top10_share:.1f}%")

st.markdown("---")

# ============================================================
# CHART HELPERS
# ============================================================
def dark_ax(ax):
    """Apply consistent dark-dashboard styling to Matplotlib axes."""
    panel_bg = "#11162a"
    text_main = "#f6f7ff"
    text_muted = "#aeb5ce"
    border = "#2a3150"

    ax.set_facecolor(panel_bg)
    ax.figure.set_facecolor(panel_bg)

    ax.tick_params(
        axis="both",
        colors=text_muted,
        labelcolor=text_muted,
        labelsize=9
    )

    ax.xaxis.label.set_color(text_muted)
    ax.yaxis.label.set_color(text_muted)

    # Matplotlib/pandas may recreate title text, so set it explicitly.
    ax.title.set_color(text_main)

    for spine in ax.spines.values():
        spine.set_color(border)

    ax.grid(
        axis="y",
        color="#4a5273",
        alpha=0.20,
        linewidth=0.7
    )
    ax.set_axisbelow(True)

# ============================================================
# ROW 1: TREND + TOP ARTISTS
# ============================================================
left, right = st.columns(2)

with left:
    st.markdown('<div class="section-label">Chart activity trend</div>', unsafe_allow_html=True)

    trend = (
        filtered_df.dropna(subset=["date"])
        .assign(month=lambda x: x["date"].dt.to_period("M").dt.to_timestamp())
        .groupby("month")
        .size()
    )

    if not trend.empty:
        fig, ax = plt.subplots(figsize=(8, 4.2))
        ax.plot(trend.index, trend.values, marker="o", linewidth=2)
        dark_ax(ax)
        ax.set_title("Monthly Chart Records", loc="left", fontsize=13, fontweight="bold", color="#f6f7ff", pad=10)
        ax.set_xlabel("")
        ax.set_ylabel("Records")
        fig.autofmt_xdate(rotation=30, ha="right")
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)
    else:
        st.info("No dated records are available for this selection.")

with right:
    st.markdown('<div class="section-label">Artist concentration</div>', unsafe_allow_html=True)

    top_artists = filtered_df["artist"].value_counts().head(10)

    fig, ax = plt.subplots(figsize=(8, 4.2))
    top_artists.sort_values().plot(kind="barh", ax=ax)
    dark_ax(ax)
    ax.set_title("Top 10 Artists by Chart Appearances", loc="left",
                 fontsize=13, fontweight="bold", color="#f6f7ff", pad=10)
    ax.set_xlabel("Chart Appearances")
    ax.set_ylabel("")
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

# ============================================================
# ROW 2: POPULARITY + EXPLICIT
# ============================================================
left, right = st.columns(2)

with left:
    st.markdown('<div class="section-label">Popularity by chart position</div>',
                unsafe_allow_html=True)

    popularity_by_rank = (
        filtered_df.groupby("rank_group")["popularity"]
        .mean()
        .reindex(["Top 10", "11-25", "26-50"])
        .dropna()
    )

    if not popularity_by_rank.empty:
        fig, ax = plt.subplots(figsize=(8, 4.1))
        popularity_by_rank.plot(kind="bar", ax=ax)
        dark_ax(ax)
        ax.set_title("Average Popularity by Rank Group", loc="left",
                     fontsize=13, fontweight="bold", color="#f6f7ff", pad=10)
        ax.set_xlabel("")
        ax.set_ylabel("Average Popularity")
        ax.tick_params(axis="x", rotation=0)

        for container in ax.containers:
            ax.bar_label(container, fmt="%.1f", padding=3, color="#e7e9f5")

        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)
    else:
        st.info("No ranked popularity data for this selection.")

with right:
    st.markdown('<div class="section-label">Content mix</div>',
                unsafe_allow_html=True)

    explicit_counts = filtered_df["is_explicit"].value_counts()

    if not explicit_counts.empty:
        labels = [
            "Explicit" if value is True else "Non-Explicit"
            for value in explicit_counts.index
        ]

        fig, ax = plt.subplots(figsize=(8, 4.1))
        wedges, texts, autotexts = ax.pie(
            explicit_counts.values,
            labels=labels,
            autopct="%1.1f%%",
            startangle=90,
            wedgeprops={"width": 0.42, "edgecolor": "#11162a"}
        )
        fig.set_facecolor("#11162a")
        ax.set_facecolor("#11162a")

        for text in texts + autotexts:
            text.set_color("#dce9e4")

        ax.set_title(
            "Explicit vs Non-Explicit",
            loc="left",
            fontsize=13,
            fontweight="bold",
            color="#f6f7ff",
            pad=10
        )

        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

# ============================================================
# ROW 3: DURATION + RANK DISTRIBUTION
# ============================================================
left, right = st.columns(2)

with left:
    st.markdown('<div class="section-label">Track characteristics</div>',
                unsafe_allow_html=True)

    duration_by_rank = (
        filtered_df.groupby("rank_group")["duration_minutes"]
        .mean()
        .reindex(["Top 10", "11-25", "26-50"])
        .dropna()
    )

    if not duration_by_rank.empty:
        fig, ax = plt.subplots(figsize=(8, 4.1))
        duration_by_rank.plot(kind="bar", ax=ax)
        dark_ax(ax)
        ax.set_title("Average Track Duration by Rank", loc="left",
                     fontsize=13, fontweight="bold", color="#f6f7ff", pad=10)
        ax.set_xlabel("")
        ax.set_ylabel("Minutes")
        ax.tick_params(axis="x", rotation=0)

        for container in ax.containers:
            ax.bar_label(container, fmt="%.2f", padding=3, color="#e7e9f5")

        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

with right:
    st.markdown('<div class="section-label">Chart distribution</div>',
                unsafe_allow_html=True)

    rank_counts = (
        filtered_df["rank_group"]
        .value_counts()
        .reindex(["Top 10", "11-25", "26-50", "Unknown"])
        .dropna()
    )

    fig, ax = plt.subplots(figsize=(8, 4.1))
    rank_counts.plot(kind="bar", ax=ax)
    dark_ax(ax)
    ax.set_title("Records by Rank Group", loc="left",
                 fontsize=13, fontweight="bold", color="#f6f7ff", pad=10)
    ax.set_xlabel("")
    ax.set_ylabel("Records")
    ax.tick_params(axis="x", rotation=0)

    for container in ax.containers:
        ax.bar_label(container, fmt="%d", padding=3, color="#e7e9f5")

    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

# ============================================================
# TOP SONGS
# ============================================================
st.markdown("---")
st.markdown('<div class="section-label">Top-performing tracks</div>',
            unsafe_allow_html=True)

top_songs = (
    filtered_df.dropna(subset=["popularity"])
    .sort_values("popularity", ascending=False)
    [["song", "artist", "popularity", "position"]]
    .drop_duplicates(subset=["song", "artist"])
    .head(10)
    .rename(columns={
        "song": "Song",
        "artist": "Artist",
        "popularity": "Popularity",
        "position": "Chart Position"
    })
)

st.dataframe(
    top_songs,
    use_container_width=True,
    hide_index=True
)

# ============================================================
# DYNAMIC MARKET INSIGHTS
# ============================================================
st.markdown("---")
st.markdown('<div class="section-label">What the market tells us</div>',
            unsafe_allow_html=True)

top_artist = (
    filtered_df["artist"].value_counts().index[0]
    if filtered_df["artist"].notna().any()
    else "N/A"
)

top_artist_count = (
    filtered_df["artist"].value_counts().iloc[0]
    if filtered_df["artist"].notna().any()
    else 0
)

non_explicit_share = (
    (filtered_df["is_explicit"] == False).mean() * 100
    if filtered_df["is_explicit"].notna().any()
    else 0
)

best_pop_rank = (
    popularity_by_rank.idxmax()
    if not popularity_by_rank.empty
    else "N/A"
)

avg_duration = filtered_df["duration_minutes"].mean()

i1, i2 = st.columns(2)

with i1:
    st.markdown(
        f"""
        <div class="insight-box">
            <b>Leading artist</b><br>
            {top_artist} has the most chart appearances in the current
            selection with <b>{top_artist_count:,}</b> records.
        </div>

        <div class="insight-box">
            <b>Popularity pattern</b><br>
            <b>{best_pop_rank}</b> currently has the highest average
            popularity among the ranked groups shown.
        </div>
        """,
        unsafe_allow_html=True
    )

with i2:
    st.markdown(
        f"""
        <div class="insight-box">
            <b>Content mix</b><br>
            Non-explicit records account for approximately
            <b>{non_explicit_share:.1f}%</b> of the current selection.
        </div>

        <div class="insight-box">
            <b>Typical track length</b><br>
            Average track duration for the current selection is
            <b>{avg_duration:.2f} minutes</b>.
        </div>
        """,
        unsafe_allow_html=True
    )

# ============================================================
# DATASET SUMMARY
# ============================================================
with st.expander("Dataset Summary"):
    s1, s2, s3, s4 = st.columns(4)
    s1.metric("Full Dataset", f"{len(df):,}")
    s2.metric("Artists", f"{df['artist'].nunique():,}")
    s3.metric("Songs", f"{df['song'].nunique():,}")
    s4.metric(
        "Unknown Rank",
        f"{(df['rank_group'] == 'Unknown').sum():,}"
    )

# ============================================================
# FOOTER
# ============================================================
st.markdown("---")
st.caption(
    "UK Top 50 Music Market Analysis • Built by Nikhil Chikte • "
    "Python • Pandas • Matplotlib • Streamlit"
)
