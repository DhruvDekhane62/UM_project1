"""UK Top 50 Playlist Analysis - Streamlit Dashboard for Atlantic Recording Corporation."""

import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import plotly.express as px
from datetime import datetime

from src.load import get_processed_data
from src.metrics import (
    explode_artist_credits,
    filter_dataset,
    calculate_summary_kpis,
    get_top_artists_leaderboard,
    get_daily_unique_artists,
    get_collab_breakdown_by_rank,
    get_explicit_breakdown,
    get_album_type_breakdown,
    get_duration_breakdown,
    get_collaboration_network_data,
)
from src.charts import (
    build_top_artists_chart,
    build_daily_unique_artists_chart,
    build_collab_rank_chart,
    build_explicit_chart,
    build_album_type_chart,
    build_duration_charts,
    generate_network_html,
)

# Page Configuration
st.set_page_config(
    page_title="UK Top 50 Music Market Analysis",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded",
)


@st.cache_data
def load_data():
    """Load cleaned parquet dataset."""
    return get_processed_data(force_reprocess=False)


def main():
    # Custom CSS for modern, premium look
    st.markdown(
        """
        <style>
        .main-header {
            font-size: 2.2rem;
            font-weight: 700;
            background: linear-gradient(90deg, #6366F1 0%, #06B6D4 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.2rem;
        }
        .sub-header {
            color: #64748B;
            font-size: 1.05rem;
            margin-bottom: 1.5rem;
        }
        .stMetric {
            background-color: #F8FAFC;
            padding: 0.8rem;
            border-radius: 0.5rem;
            border: 1px solid #E2E8F0;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="main-header">UK Top 50 Market Structure Analytics</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="sub-header">Executive Dashboard for Atlantic Recording Corporation | Market structure, artist dominance, and song format insights</div>',
        unsafe_allow_html=True,
    )

    # Load dataset
    try:
        raw_cleaned_df = load_data()
    except Exception as e:
        st.error(f"Failed to load dataset. Please verify data processing: {e}")
        return

    # Extract filter bounds
    min_date = raw_cleaned_df["date"].min().date()
    max_date = raw_cleaned_df["date"].max().date()
    all_artists = sorted(
        list(set(explode_artist_credits(raw_cleaned_df)["artist_name"]))
    )
    all_album_types = sorted(list(raw_cleaned_df["album_type"].unique()))

    # Sidebar Filters
    st.sidebar.header("🔍 Filters & Options")

    # Date Filter
    date_selection = st.sidebar.date_input(
        "Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
    )

    if isinstance(date_selection, (list, tuple)):
        if len(date_selection) == 2:
            start_date = pd.Timestamp(date_selection[0])
            end_date = pd.Timestamp(date_selection[1])
        else:
            st.warning(
                "Please select both a start and end date to update the analysis."
            )
            return
    else:
        start_date = pd.Timestamp(date_selection)
        end_date = pd.Timestamp(date_selection)

    # Artist Filter
    selected_artists = st.sidebar.multiselect(
        "Filter by Artist(s)",
        options=all_artists,
        default=[],
        help="Select one or more artists to filter tracks where they are credited.",
    )

    # Solo vs Collaboration Toggle
    collab_option = st.sidebar.radio(
        "Track Type",
        options=["All", "Solo Only", "Collaborations Only"],
        index=0,
    )

    # Album Type Filter
    selected_album_types = st.sidebar.multiselect(
        "Release Format",
        options=all_album_types,
        default=all_album_types,
    )

    # Apply Filters
    filtered_df = filter_dataset(
        df=raw_cleaned_df,
        start_date=start_date,
        end_date=end_date,
        selected_artists=selected_artists,
        collab_option=collab_option,
        selected_album_types=selected_album_types,
    )

    # Empty State Check
    if filtered_df.empty:
        st.warning(
            "⚠️ No data matches your filter criteria. Please widen the date range or clear the artist filter."
        )
        return

    # KPI Summary Header Cards
    kpis = calculate_summary_kpis(filtered_df)

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("Unique Artists", f"{kpis['unique_artists']:,}")
    with col2:
        st.metric("Collab Ratio", f"{kpis['collab_ratio']:.1f}%")
    with col3:
        st.metric("Explicit Share", f"{kpis['explicit_share']:.1f}%")
    with col4:
        st.metric("Single Share", f"{kpis['single_share']:.1f}%")
    with col5:
        st.metric("Top 5 Artist Share", f"{kpis['top5_artist_share']:.1f}%")

    st.markdown("---")

    # Main Tabs
    tab_artists, tab_collabs, tab_explicit, tab_format, tab_duration = st.tabs(
        [
            "🎤 Artist Dominance",
            "🤝 Collaborations",
            "🔞 Explicit Content",
            "💿 Release Formats",
            "⏱️ Track Duration",
        ]
    )

    # TAB 1: ARTIST DOMINANCE
    with tab_artists:
        st.subheader("Artist Dominance & Concentration")
        col_chart, col_table = st.columns([7, 5])

        leaderboard_df = get_top_artists_leaderboard(filtered_df, top_n=15)
        with col_chart:
            st.plotly_chart(
                build_top_artists_chart(leaderboard_df), use_container_width=True
            )

        with col_table:
            st.markdown("##### Top 15 Artists Leaderboard")
            st.dataframe(leaderboard_df, hide_index=True, use_container_width=True)

        st.markdown("---")
        st.subheader("Daily Unique Artist Diversity Trend")
        daily_df = get_daily_unique_artists(filtered_df)
        st.plotly_chart(
            build_daily_unique_artists_chart(daily_df), use_container_width=True
        )

        col_hhi, col_entropy = st.columns(2)
        with col_hhi:
            st.info(
                f"**Herfindahl-Hirschman Index (HHI)**: `{kpis['hhi_index']:.4f}`\n\n*(Measures market concentration; lower indicates higher competition)*"
            )
        with col_entropy:
            st.info(
                f"**Content Variety Index (Normalized Shannon Entropy)**: `{kpis['shannon_entropy']:.4f}`\n\n*(Measures artist diversity; 1.0 represents maximum variety)*"
            )

    # TAB 2: COLLABORATIONS
    with tab_collabs:
        st.subheader("Collaboration Analysis & Network")
        collab_rank_df = get_collab_breakdown_by_rank(filtered_df)
        st.plotly_chart(
            build_collab_rank_chart(collab_rank_df), use_container_width=True
        )

        st.markdown("---")
        st.subheader("Interactive Collaboration Network Graph")
        st.caption(
            "Nodes represent top artists (sized by total appearances). Edges represent co-crediting on unique songs."
        )

        nodes, edges = get_collaboration_network_data(filtered_df, top_n_artists=30)
        if nodes and edges:
            net_html = generate_network_html(nodes, edges)
            components.html(net_html, height=520, scrolling=False)
        else:
            st.info(
                "Insufficient collaboration data in the selected filter slice to build a network graph."
            )

    # TAB 3: EXPLICIT CONTENT
    with tab_explicit:
        st.subheader("Explicit Content Distribution & Popularity")
        rank_explicit_df, pop_explicit_df = get_explicit_breakdown(filtered_df)

        c1, c2 = st.columns(2)
        fig_share, fig_pop = build_explicit_chart(rank_explicit_df, pop_explicit_df)
        with c1:
            st.plotly_chart(fig_share, use_container_width=True)
        with c2:
            st.plotly_chart(fig_pop, use_container_width=True)

    # TAB 4: RELEASE FORMATS
    with tab_format:
        st.subheader("Release Format (Single vs Album)")
        c1, c2 = st.columns([5, 7])

        album_df = get_album_type_breakdown(filtered_df)
        with c1:
            st.plotly_chart(build_album_type_chart(album_df), use_container_width=True)

        with c2:
            st.markdown("##### Total Tracks per Album Distribution")
            st.caption("Total tracks on the parent release for charting songs.")
            fig_tracks = px.histogram(
                filtered_df,
                x="total_tracks",
                nbins=30,
                title="Total Tracks on Parent Release",
                labels={"total_tracks": "Total Tracks"},
                template="plotly_white",
                color_discrete_sequence=["#06B6D4"],
            )
            st.plotly_chart(fig_tracks, use_container_width=True)

    # TAB 5: DURATION
    with tab_duration:
        st.subheader("Track Duration Analysis")
        bucket_df = get_duration_breakdown(filtered_df)
        fig_hist, fig_duration_pop = build_duration_charts(filtered_df, bucket_df)

        c1, c2 = st.columns(2)
        with c1:
            st.plotly_chart(fig_hist, use_container_width=True)
        with c2:
            st.plotly_chart(fig_duration_pop, use_container_width=True)


if __name__ == "__main__":
    main()
