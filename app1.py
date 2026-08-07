import streamlit as st
import pandas as pd

from app import STATE_ABBREV

@st.cache_data
def load_data():
    # Load dataset
    df = pd.read_csv("Nassau Candy Distributor.csv")

    # -----------------------------
    # Convert Order Date
    # -----------------------------
    if "Order Date" in df.columns:
        df["Order Date"] = pd.to_datetime(
            df["Order Date"],
            dayfirst=True,
            errors="coerce"
        )

    # -----------------------------
    # Convert Ship Date
    # -----------------------------
    if "Ship Date" in df.columns:
        df["Ship Date"] = pd.to_datetime(
            df["Ship Date"],
            dayfirst=True,
            errors="coerce"
        )

    # -----------------------------
    # Create Month Column
    # -----------------------------
    if "Order Date" in df.columns:
        df["Month"] = df["Order Date"].dt.to_period("M").astype(str)

    # -----------------------------
    # Create Shipping Lead Time
    # -----------------------------
    if "Order Date" in df.columns and "Ship Date" in df.columns:
        df["Shipping Lead Time"] = (
            df["Ship Date"] - df["Order Date"]
        ).dt.days

        # Remove invalid lead times
        df = df[df["Shipping Lead Time"] >= 0]

    # -----------------------------
    # State Code Mapping
    # -----------------------------
    if "State/Province" in df.columns:
        df["State Code"] = df["State/Province"].map(STATE_ABBREV)

    return df