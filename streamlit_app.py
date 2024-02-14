import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime


import streamlit as st
from streamlit_option_menu import option_menu

from data_loader import *
from data_process import *
from pages import *

st. set_page_config(layout="wide")

# Data assets spreed-sheet infos
sheet_id = "1hwdM9FykkIdUfc8FYSsqot_spsmaeUfpgJJST9CWpn8"
sheet_names = ["Etienne", "Alex", "Ivan", "Baptiste", "Lucas"]
name_decorators = {"Etienne": "🗿", "Alex": "💪", "Ivan": "🐁", "Baptiste": "👽", "Lucas": "🦧"}

# Load data
data_assets = get_data(sheet_id=sheet_id, sheet_names=sheet_names)

# Update or create st s ticker
update_tickers(data_assets)

# Load data prices
data_prices = get_prices(data_assets)



def test_page(text):
    st.markdown("<h1 style='text-align: center;'>📈 T-Corp Portfolio 📈</h1>", unsafe_allow_html=True)
    st.markdown(text)


with st.sidebar:
    selected = option_menu(
        menu_title="Main Menu",
        options=["Home", "🗿 Etienne", "💪 Alex", "🐁 Ivan", "👽 Baptiste", "🦧 Lucas", "☎️ About"],
        icons=["🗿", "💪", "🐁", "👽", "🦧"],
        menu_icon="cast",
        default_index=0,
        # orientation = "horizontal",
    )


if selected == "Home":
    home_page()

if selected == "🗿 Etienne":
    person_page(data_assets, data_prices, "Etienne")
    # test_page("Etienne")

if selected == "💪 Alex":
    # person_page(data, "Alex")
    test_page("Alex")

if selected == "🐁 Ivan":
    # person_page(data, "Ivan")
    test_page("Ivan")

if selected == "👽 Baptiste":
    # person_page(data, "Baptiste")
    test_page("Baptiste")

if selected == "🦧 Lucas":
    # person_page(data, "Lucas")
    test_page("Lucas")
    st.markdown("<br>Ouvre toi un PEA mec.</br>", unsafe_allow_html=True)
    st.page_link("https://www.boursorama.com/", label="Boursorama", icon="💰")


if selected == "☎️ About":
    st.markdown("<h1 style='text-align: center;'>📈 T-Corp Portfolio 📈</h1>", unsafe_allow_html=True)
    st.markdown("La darone d'Alex suce : 0657836589")


