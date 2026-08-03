import streamlit as st
import sqlite3
import pandas as pd
import os
from score_calculator import calculate_points

# Database helper functions
DB_PATH = os.path.join(os.path.dirname(__file__), 'fantasy_cricket.db')

def get_connection():
    return sqlite3.connect(DB_PATH)

def load_players():
    conn = get_connection()
    df = pd.read_sql_query("SELECT player, value, ctg FROM stats", conn)
    conn.close()
    return df

def load_teams():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM teams;")
    teams = [row[0] for row in cursor.fetchall()]
    conn.close()
    return teams

def get_team_players(team_name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT players, value FROM teams WHERE name = ?;", (team_name,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return row[0].split(','), row[1]
    return [], 0

def save_team(team_name, players, value):
    conn = get_connection()
    cursor = conn.cursor()
    players_str = ",".join(players)
    cursor.execute("SELECT name FROM teams WHERE name = ?", (team_name,))
    if cursor.fetchone():
        cursor.execute("UPDATE teams SET players = ?, value = ? WHERE name = ?", (players_str, value, team_name))
    else:
        cursor.execute("INSERT INTO teams (name, players, value) VALUES (?, ?, ?)", (team_name, players_str, value))
    conn.commit()
    conn.close()

def get_match_stats(player_name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM match WHERE Player = ?;", (player_name,))
    data = cursor.fetchone()
    conn.close()
    return data

# Main App Layout
st.set_page_config(page_title="Fantasy Cricket", layout="wide")

st.sidebar.title("🏏 Fantasy Cricket")
page = st.sidebar.radio("Navigation", ["Manage Team", "Evaluate Team"])

players_df = load_players()
bat_players = players_df[players_df['ctg'] == 'BAT']['player'].tolist()
bow_players = players_df[players_df['ctg'] == 'BOW']['player'].tolist()
ar_players = players_df[players_df['ctg'] == 'AR']['player'].tolist()
wk_players = players_df[players_df['ctg'] == 'WK']['player'].tolist()

if page == "Manage Team":
    st.title("Manage Your Team")
    
    # Mode selection
    mode = st.radio("Choose Action:", ["Create New Team", "Open Existing Team"], horizontal=True)
    
    if "current_team_name" not in st.session_state:
        st.session_state.current_team_name = ""
    
    selected_team_players = []
    
    if mode == "Open Existing Team":
        teams = load_teams()
        if not teams:
            st.warning("No saved teams found. Please create a new one.")
        else:
            team_to_open = st.selectbox("Select Team to Open", teams)
            if team_to_open:
                st.session_state.current_team_name = team_to_open
                selected_team_players, _ = get_team_players(team_to_open)
    else:
        st.session_state.current_team_name = st.text_input("Enter New Team Name:", value=st.session_state.current_team_name)
    
    st.divider()
    
    # Initialize defaults for multiselect based on loaded team
    default_bat = [p for p in selected_team_players if p in bat_players]
    default_bow = [p for p in selected_team_players if p in bow_players]
    default_ar = [p for p in selected_team_players if p in ar_players]
    default_wk = [p for p in selected_team_players if p in wk_players]

    # Handle Streamlit state reset for multiselects when changing teams
    if "last_opened_team" not in st.session_state or st.session_state.last_opened_team != st.session_state.current_team_name:
        st.session_state.last_opened_team = st.session_state.current_team_name
        st.session_state.sel_bat = default_bat
        st.session_state.sel_bow = default_bow
        st.session_state.sel_ar = default_ar
        st.session_state.sel_wk = default_wk

    # Layout for selection
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Select Players")
        sel_bat = st.multiselect("Batsmen (BAT)", bat_players, default=st.session_state.sel_bat, key="sel_bat")
        sel_bow = st.multiselect("Bowlers (BOW)", bow_players, default=st.session_state.sel_bow, key="sel_bow")
        sel_ar = st.multiselect("Allrounders (AR)", ar_players, default=st.session_state.sel_ar, key="sel_ar")
        sel_wk = st.multiselect("Wicket-keepers (WK)", wk_players, default=st.session_state.sel_wk, key="sel_wk")
        
    all_selected = sel_bat + sel_bow + sel_ar + sel_wk
    
    # Calculate points
    points_used = players_df[players_df['player'].isin(all_selected)]['value'].sum()
    points_avail = 1200 - points_used
    
    with col2:
        st.subheader("Team Status")
        
        # Display Metrics
        m1, m2 = st.columns(2)
        m1.metric("Points Available", points_avail, delta=f"-{points_used} Used", delta_color="inverse")
        m2.metric("Total Players", f"{len(all_selected)}/11")
        
        # Display counts
        st.write("### Category Breakdown")
        st.write(f"🏏 **Batsmen:** {len(sel_bat)}")
        st.write(f"🥎 **Bowlers:** {len(sel_bow)}")
        st.write(f"🏃‍♂️ **Allrounders:** {len(sel_ar)}")
        st.write(f"🧤 **Wicket-keepers:** {len(sel_wk)}")
        
        st.divider()
        
        # Validation checks
        errors = []
        if len(all_selected) != 11:
            errors.append(f"Team must have exactly 11 players. (Currently {len(all_selected)})")
        if len(sel_bat) > 5:
            errors.append("Maximum 5 Batsmen allowed.")
        if len(sel_bow) > 5:
            errors.append("Maximum 5 Bowlers allowed.")
        if len(sel_ar) > 3:
            errors.append("Maximum 3 Allrounders allowed.")
        if len(sel_wk) != 1:
            errors.append("Exactly 1 Wicket-keeper required.")
        if points_avail < 0:
            errors.append("Not enough points available!")
        if not st.session_state.current_team_name:
            errors.append("Team Name cannot be empty.")
            
        for err in errors:
            st.error(err)
            
        if not errors:
            st.success("Team is valid and ready to be saved!")
            if st.button("Save Team", type="primary"):
                save_team(st.session_state.current_team_name, all_selected, int(points_used))
                st.toast("Team saved successfully!", icon="✅")

elif page == "Evaluate Team":
    st.title("Evaluate Team Performance")
    
    teams = load_teams()
    if not teams:
        st.warning("No saved teams found.")
    else:
        col1, col2 = st.columns(2)
        with col1:
            selected_team = st.selectbox("Select Team", teams)
        with col2:
            match_selected = st.selectbox("Select Match", ["Match 1"])
            
        if st.button("Calculate Score", type="primary"):
            players, _ = get_team_players(selected_team)
            
            results = []
            total_team_score = 0
            
            for player in players:
                stats = get_match_stats(player)
                points = 0
                if stats:
                    points = calculate_points(stats)
                total_team_score += points
                results.append({"Player": player, "Points": points})
                
            st.divider()
            st.subheader(f"Total Score: {total_team_score}")
            
            df_results = pd.DataFrame(results)
            st.dataframe(df_results, use_container_width=True)
