# -*- coding: utf-8 -*-
"""
Created on Wed Dec 24 16:39:17 2025

@author: Wendell
"""

import streamlit as st
import pandas as pd

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(
    page_title="Store Price List",
    layout="wide"
)

# ----------------------------
# GOOGLE SHEET CONFIG
# ----------------------------
# Replace this with your SHEET_ID from Google Sheet
SHEET_ID = "1yAXnyZ3N6hQKqnqFjqBCgyDA2Aq-eQh0JAnsLEvDWlQ"

# Construct the CSV export URL
CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

# ----------------------------
# LOAD DATA FUNCTION
# ----------------------------
@st.cache_data(ttl=300)  # cache for 5 minutes
def load_data():
    df = pd.read_csv(CSV_URL)
    # Ensure price column is numeric
    df["Price"] = pd.to_numeric(df["Price"], errors="coerce")
    return df

# Load data
df = load_data()

# ----------------------------
# APP TITLE
# ----------------------------
st.title("🛒 Store Price List")
st.caption("Prices updated automatically from Google Sheet")

# ----------------------------
# FORMAT DATA FOR DISPLAY
# ----------------------------
display_df = df.copy()

# Format price column in Pesos
display_df["Price"] = display_df["Price"].map(lambda x: f"₱{x:,.2f}")

# Hide ItemID from customers
display_df = display_df.drop(columns=["ItemID"])

# ----------------------------
# SEARCH FEATURE (optional but nice for phones/tablets)
# ----------------------------
search_term = st.text_input("Search products:", "")
if search_term:
    display_df = display_df[display_df["Item"].str.contains(search_term, case=False)]

# ----------------------------
# DISPLAY TABLE
# ----------------------------
st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True
)
