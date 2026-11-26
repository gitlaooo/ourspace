
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# ==========================================
# PAGE 4 - TRADE ANALYSIS
# ==========================================

st.title("🌸 Trade Analysis")
st.subheader("International Trade Performance & Economic Insights")

st.write(
    "This page provides an analytical overview of international "
    "trade performance across 130 countries, focusing on export "
    "performance, import activity, trade balance, and economic insights."
)

st.divider()

# ==========================================
# LOAD DATA
# ==========================================

file_path = (
    Path(__file__).parent /
    "ekspor_impor_2025_sederhana.xlsx"
)

try:
    df = pd.read_excel(file_path)

    df.columns = df.columns.str.strip().str.lower()

    required = ["country", "ekspor", "impor"]

    if not all(col in df.columns for col in required):
        st.error("Dataset must contain country, ekspor, and impor.")
        st.stop()

    df = df[required].copy()

    df["country"] = df["country"].astype(str).str.strip()
    df["ekspor"] = pd.to_numeric(df["ekspor"], errors="coerce")
    df["impor"] = pd.to_numeric(df["impor"], errors="coerce")

    df = df.dropna(subset=required)
    df = df.drop_duplicates(subset=["country"])

    if df.empty:
        st.error("No valid data available.")
        st.stop()

    # ==========================================
    # CALCULATE INDICATORS
    # ==========================================

    df["trade_balance"] = df["ekspor"] - df["impor"]
    df["total_trade"] = df["ekspor"] + df["impor"]

    df["coverage_ratio"] = (
        df["ekspor"] / df["impor"].replace(0, float("nan")) * 100
    )

    df["export_share"] = (
        df["ekspor"] / df["ekspor"].sum() * 100
        if df["ekspor"].sum() != 0 else 0
    )

    df["import_share"] = (
        df["impor"] / df["impor"].sum() * 100
        if df["impor"].sum() != 0 else 0
    )

    df["trade_status"] = df["trade_balance"].apply(
        lambda x: "Surplus" if x > 0
        else "Deficit" if x < 0
        else "Balanced"
    )

    # ==========================================
    # GLOBAL TRADE SUMMARY
    # ==========================================

    st.header("1. Global Trade Performance")

    total_export = df["ekspor"].sum()
    total_import = df["impor"].sum()
    total_balance = total_export - total_import
    total_trade = total_export + total_import

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Total Countries", f"{len(df):,}")
    c2.metric("Total Exports", f"{total_export:,.2f}")
    c3.metric("Total Imports", f"{total_import:,.2f}")
    c4.metric("Aggregate Trade Balance", f"{total_balance:,.2f}")

    if total_balance > 0:
        st.success(
            f"The aggregate trade balance is positive, "
            f"with exports exceeding imports by {total_balance:,.2f}."
        )
    elif total_balance < 0:
        st.warning(
            f"The aggregate trade balance is negative, "
            f"with imports exceeding exports by {abs(total_balance):,.2f}."
        )
    else:
        st.info("Aggregate exports and imports are equal.")

    st.divider()

    # ==========================================
    # EXPORT PERFORMANCE
    # ==========================================

    st.header("2. Export Performance Analysis")

    highest_export = df.loc[df["ekspor"].idxmax()]
    lowest_export = df.loc[df["ekspor"].idxmin()]

    a, b = st.columns(2)

    a.metric(
        "Highest Exporter",
        highest_export["country"],
        f"{highest_export['ekspor']:,.2f}"
    )

    b.metric(
        "Lowest Exporter",
        lowest_export["country"],
        f"{lowest_export['ekspor']:,.2f}"
    )

    top_export = df.nlargest(10, "ekspor").sort_values("ekspor")

    fig1 = px.bar(
        top_export,
        x="ekspor",
        y="country",
        orientation="h",
        color="ekspor",
        color_continuous_scale=["#F8DCE9", "#D979A3"],
        title="Top 10 Exporting Countries",
        labels={"ekspor": "Export Value", "country": "Country"}
    )

    fig1.update_layout(height=480)

    st.plotly_chart(fig1, use_container_width=True)

    st.write(
        f"**Finding:** {highest_export['country']} is the leading "
        f"exporter in the dataset, contributing "
        f"{highest_export['export_share']:.2f}% of total exports."
    )

    st.divider()

    # ==========================================
    # IMPORT PERFORMANCE
    # ==========================================

    st.header("3. Import Dependency Analysis")

    highest_import = df.loc[df["impor"].idxmax()]
    lowest_import = df.loc[df["impor"].idxmin()]

    a, b = st.columns(2)

    a.metric(
        "Highest Importer",
        highest_import["country"],
        f"{highest_import['impor']:,.2f}"
    )

    b.metric(
        "Lowest Importer",
        lowest_import["country"],
        f"{lowest_import['impor']:,.2f}"
    )

    top_import = df.nlargest(10, "impor").sort_values("impor")

    fig2 = px.bar(
        top_import,
        x="impor",
        y="country",
        orientation="h",
        color="impor",
        color_continuous_scale=["#E6DDF5", "#8E79B8"],
        title="Top 10 Importing Countries",
        labels={"impor": "Import Value", "country": "Country"}
    )

    fig2.update_layout(height=480)

    st.plotly_chart(fig2, use_container_width=True)

    st.write(
        f"**Finding:** {highest_import['country']} has the highest "
        f"import value, contributing "
        f"{highest_import['import_share']:.2f}% of total imports."
    )

    st.info(
        "A high import value does not automatically indicate "
        "economic weakness or excessive import dependency. "
        "Imports may include productive inputs, capital goods, "
        "and consumer goods."
    )

    st.divider()

    # ==========================================
    # TRADE BALANCE
    # ==========================================

    st.header("4. Trade Balance Analysis")

    surplus = df[df["trade_balance"] > 0]
    deficit = df[df["trade_balance"] < 0]
    balanced = df[df["trade_balance"] == 0]

    a, b, c = st.columns(3)

    a.metric("Surplus Countries", len(surplus))
    b.metric("Deficit Countries", len(deficit))
    c.metric("Balanced Countries", len(balanced))

    balance_status = df["trade_status"].value_counts().reset_index()
    balance_status.columns = ["Status", "Countries"]

    fig3 = px.pie(
        balance_status,
        names="Status",
        values="Countries",
        hole=0.5,
        color="Status",
        color_discrete_map={
            "Surplus": "#D979A3",
            "Deficit": "#8E79B8",
            "Balanced": "#E8B96A"
        },
        title="Distribution of Trade Balance"
    )

    st.plotly_chart(fig3, use_container_width=True)

    # Biggest surplus and deficit
    biggest_surplus = df.loc[df["trade_balance"].idxmax()]
    biggest_deficit = df.loc[df["trade_balance"].idxmin()]

    a, b = st.columns(2)

    a.metric(
        "Largest Trade Surplus",
        biggest_surplus["country"],
        f"{biggest_surplus['trade_balance']:,.2f}"
    )

    b.metric(
        "Largest Trade Deficit",
        biggest_deficit["country"],
        f"{biggest_deficit['trade_balance']:,.2f}"
    )

    st.divider()

    # ==========================================
    # COUNTRY COMPETITIVENESS
    # ==========================================

    st.header("5. Country Trade Competitiveness")

    st.write(
        "This section compares export and import values "
        "to identify countries with stronger export positions."
    )

    fig4 = px.scatter(
        df,
        x="ekspor",
        y="impor",
        size="total_trade",
        color="trade_status",
        hover_name="country",
        color_discrete_map={
            "Surplus": "#D979A3",
            "Deficit": "#8E79B8",
            "Balanced": "#E8B96A"
        },
        labels={
            "ekspor": "Export Value",
            "impor": "Import Value",
            "trade_status": "Trade Status"
        },
        title="Export and Import Position by Country"
    )

    st.plotly_chart(fig4, use_container_width=True)

    st.subheader("Export-Import Coverage Ratio")

    st.write(
        "Coverage ratio measures how much of import value "
        "is covered by export value."
    )

    coverage_data = df.dropna(subset=["coverage_ratio"]).copy()

    top_coverage = coverage_data.nlargest(
        10, "coverage_ratio"
    ).sort_values("coverage_ratio")

    fig5 = px.bar(
        top_coverage,
        x="coverage_ratio",
        y="country",
        orientation="h",
        color="coverage_ratio",
        color_continuous_scale=["#F8DCE9", "#D979A3"],
        labels={
            "coverage_ratio": "Coverage Ratio (%)",
            "country": "Country"
        },
        title="Top 10 Countries by Export-Import Coverage"
    )

    st.plotly_chart(fig5, use_container_width=True)

    st.divider()

    # ==========================================
    # AUTOMATIC ECONOMIC INSIGHTS
    # ==========================================

    st.header("6. Economic Insights and Recommendations")

    st.subheader("Key Findings")

    st.markdown(
        f"""
        **1. Export Leadership**

        {highest_export['country']} records the largest export
        value among the countries observed.

        **2. Import Activity**

        {highest_import['country']} records the largest import
        value in the dataset.

        **3. Trade Surplus**

        {len(surplus)} countries record export values greater
        than import values.

        **4. Trade Deficit**

        {len(deficit)} countries record import values greater
        than export values.

        **5. Aggregate Trade Position**

        The combined trade balance is
        {"a surplus" if total_balance > 0 else "a deficit" if total_balance < 0 else "balanced"}
        of {abs(total_balance):,.2f}.
        """
    )

    st.subheader("Strategic Recommendations")

    st.markdown(
        """
        - **Export Development:** Countries can strengthen
          export competitiveness through productivity,
          product diversification, and market expansion.

        - **Import Efficiency:** Governments can improve
          import management by supporting domestic production
          while maintaining access to essential inputs.

        - **Trade Balance Monitoring:** Countries should
          evaluate the composition and sustainability of
          trade flows rather than focusing only on surplus
          or deficit figures.

        - **International Cooperation:** Countries can
          strengthen trade relationships through cooperation,
          market access, and efficient trade facilitation.
        """
    )

    st.caption(
        "Recommendations are general policy considerations, "
        "not causal conclusions derived from this dataset."
    )

    st.divider()

    # ==========================================
    # COMPLETE TRADE ANALYSIS TABLE
    # ==========================================

    st.header("7. Comprehensive Trade Analysis")

    search = st.text_input(
        "Search country",
        placeholder="Enter country name..."
    )

    display = df.copy()

    if search:
        display = display[
            display["country"].str.contains(
                search, case=False, na=False
            )
        ]

    result = display.rename(
        columns={
            "country": "Country",
            "ekspor": "Export",
            "impor": "Import",
            "trade_balance": "Trade Balance",
            "total_trade": "Total Trade",
            "coverage_ratio": "Coverage Ratio (%)",
            "export_share": "Export Share (%)",
            "import_share": "Import Share (%)",
            "trade_status": "Trade Status"
        }
    )

    st.dataframe(
        result,
        use_container_width=True,
        hide_index=True
    )

    csv = result.to_csv(index=False).encode("utf-8")

    st.download_button(
        "⬇️ Download Trade Analysis",
        data=csv,
        file_name="ourspace_trade_analysis.csv",
        mime="text/csv"
    )

    st.caption(
        "OURSPACE | International Trade Analysis | 2025 Dataset"
    )

except FileNotFoundError:
    st.error(
        "Excel file not found. Make sure "
        "ekspor_impor_2025_sederhana.xlsx "
        "is in the same folder as page4.py."
    )

except Exception as e:
    st.error(f"Error analyzing trade data: {e}")
