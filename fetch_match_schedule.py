import streamlit as st
import http.client
import json
from datetime import datetime


def fetch_cricket_data(match_type):
    conn = http.client.HTTPSConnection("cricbuzz-cricket.p.rapidapi.com")
    headers = {
        "x-rapidapi-key": "b47bf660cfmsh7e60068f13d7a82p1e1035jsn3dcf254717ea",
        "x-rapidapi-host": "cricbuzz-cricket.p.rapidapi.com",
    }
    conn.request("GET", f"/matches/v1/{match_type}", headers=headers)
    res = conn.getresponse()
    data = json.loads(res.read().decode("utf-8"))
    return data


def format_date(timestamp):
    return datetime.fromtimestamp(int(timestamp) / 1000).strftime("%Y-%m-%d %H:%M")


def display_match(match):
    match_info = match["matchInfo"]
    match_score = match.get("matchScore", {})

    col1, col2 = st.columns(2)

    with col1:
        st.write(f"**{match_info['team1']['teamName']}**")
        if "team1Score" in match_score:
            score = match_score["team1Score"].get("inngs1", {})
            st.write(f"Score: {score.get('runs', 'N/A')}/{score.get('wickets', 'N/A')}")
            st.write(f"Overs: {score.get('overs', 'N/A')}")

    with col2:
        st.write(f"**{match_info['team2']['teamName']}**")
        if "team2Score" in match_score:
            score = match_score["team2Score"].get("inngs1", {})
            st.write(f"Score: {score.get('runs', 'N/A')}/{score.get('wickets', 'N/A')}")
            st.write(f"Overs: {score.get('overs', 'N/A')}")

    st.write(f"**Status:** {match_info['status']}")
    st.write(
        f"**Venue:** {match_info['venueInfo']['ground']}, {match_info['venueInfo']['city']}"
    )
    st.write(f"**Date:** {format_date(match_info['startDate'])}")
    st.markdown("---")


def main():
    st.title("🏏 Upcoming/Recent Cricket Matches")

    # Add match type selector
    match_type = st.selectbox(
        "Select Match Type",
        ["recent", "upcoming"],
        format_func=lambda x: x.title()
    )

    try:
        data = fetch_cricket_data(match_type)

        # Create tabs for different match types
        match_types = ["International", "League", "Domestic", "Women"]
        tabs = st.tabs(match_types)

        for tab, match_type in zip(tabs, match_types):
            with tab:
                st.header(f"{match_type} Matches")

                # Find matches for this type
                type_matches = next(
                    (tm for tm in data["typeMatches"] if tm["matchType"] == match_type),
                    None,
                )

                if type_matches:
                    for series in type_matches["seriesMatches"]:
                        if "seriesAdWrapper" in series:
                            series_info = series["seriesAdWrapper"]
                            st.subheader(series_info["seriesName"])

                            for match in series_info["matches"]:
                                display_match(match)
                else:
                    st.write("No matches found for this category.")

    except Exception as e:
        st.error(f"Error fetching data: {str(e)}")


if __name__ == "__main__":
    main()
