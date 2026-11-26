
import streamlit as st
import pandas as pd
from pathlib import Path

# ==========================================
# PAGE 2 - TRADE DATA
# ==========================================

st.title("🌸 Trade Data")
st.subheader("International Export and Import Data")

st.write(
    "Explore international trade data covering exports "
    "and imports across 130 countries."
)

st.divider()

# ==========================================
# READ EXCEL DATA AUTOMATICALLY
# ==========================================

file_path = (
    Path(__file__).parent /
    "ekspor_impor_2025_sederhana.xlsx"
)

try:
    df = pd.read_excel(file_path)

    # Standardize column names
    df.columns = df.columns.str.strip().str.lower()

    # Check required columns
    required_columns = ["country", "ekspor", "impor"]

    if not all(col in df.columns for col in required_columns):
        st.error(
            "Dataset columns must contain: "
            "country, ekspor, and impor."
        )
        st.stop()

    # Select required columns
    df = df[required_columns].copy()

    # Clean data
    df["country"] = df["country"].astype(str).str.strip()
    df["ekspor"] = pd.to_numeric(df["ekspor"], errors="coerce")
    df["impor"] = pd.to_numeric(df["impor"], errors="coerce")

    df = df.dropna(subset=required_columns)

    # Calculate trade balance
    df["trade_balance"] = df["ekspor"] - df["impor"]

    # ==========================================
    # DATASET OVERVIEW
    # ==========================================

    st.success("International trade dataset loaded successfully!")

    st.header("📊 Dataset Overview")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Countries",
        f"{df['country'].nunique():,}"
    )

    col2.metric(
        "Total Exports",
        f"{df['ekspor'].sum():,.2f}"
    )

    col3.metric(
        "Total Imports",
        f"{df['impor'].sum():,.2f}"
    )

    st.divider()

    # ==========================================
    # COUNTRY SEARCH
    # ==========================================

    st.header("🔎 Search Country")

    countries = sorted(df["country"].unique())

    selected_country = st.selectbox(
        "Select a country",
        ["All Countries"] + countries
    )

    if selected_country == "All Countries":
        filtered_df = df.copy()
    else:
        filtered_df = df[
            df["country"] == selected_country
        ].copy()

    # ==========================================
    # TRADE DATA TABLE
    # ==========================================

    st.header("📋 International Trade Dataset")

    display_df = filtered_df.rename(
        columns={
            "country": "Country",
            "ekspor": "Export",
            "impor": "Import",
            "trade_balance": "Trade Balance"
        }
    )

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )

    st.caption(
        f"Showing {len(filtered_df)} countries."
    )

    # ==========================================
    # DOWNLOAD DATA
    # ==========================================

    st.divider()

    csv = display_df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="⬇️ Download Trade Data",
        data=csv,
        file_name="ourspace_trade_data.csv",
        mime="text/csv"
    )

except FileNotFoundError:

    st.error(
        "Excel file not found. Make sure "
        "ekspor_impor_2025_sederhana.xlsx "
        "is in the same folder as page2.py."
    )

except Exception as e:

    st.error(f"Error reading dataset: {e}")
