import streamlit as st
import pickle
import pandas as pd

# 1. Set up the web page title and description
st.set_page_config(page_title="IPL Win Predictor", layout="centered")
st.title(" IPL Win Probability Predictor")
st.markdown("Predict the live progression and winning chances of a T20 chase using Machine Learning.")

try:
    with open('pipe.pkl', 'rb') as file:
        model = pickle.load(file)
except FileNotFoundError:
    st.error("Could not find 'pipe.pkl'. Make sure it is in the same folder as this script!")
    
    
teams = ['Chennai Super Kings', 'Delhi Capitals', 'Kings XI Punjab', 'Kolkata Knight Riders', 'Mumbai Indians', 'Rajasthan Royals', 'Royal Challengers Bangalore', 'Sunrisers Hyderabad']
cities = ['Bangalore', 'Chennai', 'Delhi', 'Durban', 'Hyderabad', 'Indore', 'Jaipur', 'Kolkata', 'Mumbai', 'Pune', 'Sharjah']

col1, col2 = st.columns(2)

with col1:
    batting_team = st.selectbox('select chasing team(batting second)',sorted(teams))
with col2:
    bowling_team = st.selectbox("select defending team(batting first)",sorted(teams))
    
target_city = st.selectbox('select host city',sorted(cities))
target_score = st.number_input('target score set by first inning',min_value = 1, max_value = 300, value = 180)

st.markdown('---')
st.subheader('live match progress(2nd inning)')

col3, col4, col5 = st.columns(3)

with col3:
    current_runs = st.number_input('current score(runs)',min_value = 0, max_value = 300, value  = 100)
with col4:
    overs_completed = st.slider('overs completed', min_value=0.0, max_value=20.0, value=10.0, step=0.1)
with col5:
    wickets_out = st.slider('wickets fallen',min_value=0, max_value=9, value=3)
    
toss_winner = st.radio('who won the toss?',('chasing team', 'defending team'))

if st.button('predict win probability'):
    runs_left = target_score - current_runs
    ball_left = 120 - (overs_completed * 6)
    wickets_left = 10 - wickets_out
    
    crr = (current_runs * 6) / (overs_completed * 6) if overs_completed > 0 else 0
    rrr = (runs_left * 6) / ball_left if ball_left > 0 else 0
    
    chaser_won_toss = 1 if toss_winner == 'chasing team' else 0
    
    input_data = pd.DataFrame([{
        'chaser_won_toss': chaser_won_toss,
        'runs_left': runs_left,
        'balls_left': ball_left,
        'wickets_left': wickets_left,
        'total_runs': target_score,
        'crr': crr,
        'rrr': rrr
        
    }]) 
    
    result = model.predict_prob(input_data)[0]
    win_probability = round(result[1] * 100,1)
    loss_probability = round(result[0] * 100,1)
    
    st.markdown('---')
    st.subheader('live prediction details')
    
    col1, col2 = st.columns(2)
    col1.metric("Current Run Rate (CRR)", round(crr, 2))
    col2.metric("Required Run Rate (RRR)", round(rrr, 2))
    
    st.markdown("### Win / Loss Probability Breakdown")
    
    # Create a small DataFrame formatted specifically for the bar chart
    chart_data = pd.DataFrame({
        "Probability (%)": [win_probability, loss_probability]
    }, index=[f"{batting_team} (Chase)", f"{bowling_team} (Defend)"])
    
    # Display the interactive Streamlit bar chart
    st.bar_chart(chart_data)
    
    # Also print out the text percentages clearly underneath for quick reading
    st.markdown(f"**{batting_team}**: {win_probability}% chance to win")
    st.markdown(f"**{bowling_team}**: {loss_probability}% chance to win")