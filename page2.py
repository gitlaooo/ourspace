
import streamlit as st
import pandas as pd

st.title("🌸 Trade Data")
st.subheader("International Export and Import Data")

st.write(
    "Explore international trade data covering exports "
    "and imports across 130 countries."
)

st.divider()

# Upload dataset
st.header("📂 Upload Trade Dataset")

uploaded_file = st.file_uploader(
    "Upload Excel Dataset",
    type=["xlsx", "xls"]
)

if uploaded_file is not None:

    try:
        df = pd.read_excel(uploaded_file)

        # Standardize column names
        df.columns = df.columns.str.strip().str.lower()

        # Check required columns
        required_columns = ["country", "ekspor", "impor"]

        if all(col in df.columns for col in required_columns):

            df = df[required_columns].copy()

            # Convert numeric columns
            df["ekspor"] = pd.to_numeric(
                df["ekspor"], errors="coerce"
            )

            df["impor"] = pd.to_numeric(
                df["impor"], errors="coerce"
            )

            df = df.dropna(
                subset=["country", "ekspor", "impor"]
            )

            df["country"] = df["country"].astype(str)

            # Calculate trade balance
            df["trade_balance"] = df["ekspor"] - df["impor"]

            st.success("Dataset successfully uploaded!")

            # Overview
            st.header("📊 Dataset Overview")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "Total Countries",
                    f"{df['country'].nunique():,}"
                )

            with col2:
                st.metric(
                    "Total Exports",
                    f"{df['ekspor'].sum():,.0f}"
                )

            with col3:
                st.metric(
                    "Total Imports",
                    f"{df['impor'].sum():,.0f}"
                )

            st.divider()

            # Search country
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
                ]

            # Dataset table
            st.header("📋 International Trade Dataset")

            st.dataframe(
                filtered_df,
                use_container_width=True,
                hide_index=True
            )

            # Download
            csv = filtered_df.to_csv(
                index=False
            ).encode("utf-8")

            st.download_button(
                "⬇️ Download Trade Data",
                data=csv,
                file_name="ourspace_trade_data.csv",
                mime="text/csv"
            )

        else:
            st.error(
                "Invalid dataset! Required columns: "
                "country, ekspor, impor."
            )

    except Exception as e:
        st.error(f"Error reading dataset: {e}")

else:
    st.info(
        "Please upload your Excel dataset to explore "
        "international trade data."
    )
