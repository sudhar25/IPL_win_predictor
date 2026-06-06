import streamlit as st
import pickle
import pandas as pd

# 1. Set up the web page title and description
st.set_page_config(page_title="IPL Win Predictor", layout="centered")
st.title("🏏 IPL Win Probability Predictor")
st.markdown("Predict the live progression and winning chances of a T20 chase using Machine Learning.")

try:
    with open('pipe.pkl', 'rb') as file:
        model = pickle.load(file)
except FileNotFoundError:
    st.error("Could not find 'pipe.pkl'. Make sure it is in the same folder as this script!")