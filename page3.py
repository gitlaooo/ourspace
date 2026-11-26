
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# ==========================================
# OURSPACE - PAGE 3
# INTERNATIONAL TRADE INTELLIGENCE
# ==========================================

st.title("🌸 Trade Intelligence Dashboard")
st.subheader("International Export and Import Analysis")

st.write(
    "An interactive dashboard providing insights into "
    "international trade performance across 130 countries, "
    "including export performance, import activity, "
    "trade balance, and country rankings."
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

    required_columns = ["country", "ekspor", "impor"]

    if not all(col in df.columns for col in required_columns):
        st.error(
            "Dataset must contain country, ekspor, and impor."
        )
        st.stop()

    df = df[required_columns].copy()

    df["country"] = df["country"].astype(str).str.strip()
    df["ekspor"] = pd.to_numeric(df["ekspor"], errors="coerce")
    df["impor"] = pd.to_numeric(df["impor"], errors="coerce")

    df = df.dropna(subset=required_columns)
    df = df.drop_duplicates(subset=["country"])

    if df.empty:
        st.error("No valid trade data found.")
        st.stop()

    # ==========================================
    # CALCULATE TRADE INDICATORS
    # ==========================================

    total_export = df["ekspor"].sum()
    total_import = df["impor"].sum()

    df["trade_balance"] = df["ekspor"] - df["impor"]

    df["export_share"] = (
        df["ekspor"] / total_export * 100
        if total_export != 0 else 0
    )

    df["import_share"] = (
        df["impor"] / total_import * 100
        if total_import != 0 else 0
    )

    df["coverage_ratio"] = (
        df["ekspor"] / df["impor"] * 100
        if df["impor"].ne(0).all() else
        df["ekspor"].div(df["impor"].replace(0, float("nan"))) * 100
    )

    df["trade_status"] = df["trade_balance"].apply(
        lambda x: "Surplus" if x > 0
        else "Deficit" if x < 0
        else "Balanced"
    )

    df["total_trade"] = df["ekspor"] + df["impor"]

    # ==========================================
    # GLOBAL FILTER
    # ==========================================

    st.sidebar.header("🌸 Dashboard Filters")

    selected_countries = st.sidebar.multiselect(
        "Select Countries",
        sorted(df["country"].unique()),
        default=sorted(df["country"].unique()),
        help="Choose countries to include in the analysis."
    )

    if not selected_countries:
        st.warning("Please select at least one country.")
        st.stop()

    data = df[df["country"].isin(selected_countries)].copy()

    export_sum = data["ekspor"].sum()
    import_sum = data["impor"].sum()
    balance_sum = export_sum - import_sum
    trade_sum = export_sum + import_sum

    # ==========================================
    # DASHBOARD OVERVIEW
    # ==========================================

    st.header("🌍 Global Trade Overview")

    st.caption(
        "Summary of international trade performance "
        "based on the selected countries."
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Countries",
        f"{data['country'].nunique():,}"
    )

    c2.metric(
        "Total Exports",
        f"{export_sum:,.2f}"
    )

    c3.metric(
        "Total Imports",
        f"{import_sum:,.2f}"
    )

    c4.metric(
        "Trade Balance",
        f"{balance_sum:,.2f}",
        delta="Surplus" if balance_sum >= 0 else "Deficit",
        delta_color="normal"
    )

    c5, c6, c7, c8 = st.columns(4)

    c5.metric(
        "Total Trade",
        f"{trade_sum:,.2f}"
    )

    c6.metric(
        "Surplus Countries",
        int((data["trade_status"] == "Surplus").sum())
    )

    c7.metric(
        "Deficit Countries",
        int((data["trade_status"] == "Deficit").sum())
    )

    c8.metric(
        "Balanced Countries",
        int((data["trade_status"] == "Balanced").sum())
    )

    st.divider()

    # ==========================================
    # TABS
    # ==========================================

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Overview",
        "🏆 Rankings",
        "⚖️ Trade Balance",
        "🔍 Country Analysis",
        "📋 Data Insights"
    ])

    # ==========================================
    # TAB 1 - OVERVIEW
    # ==========================================

    with tab1:

        st.header("Export and Import Performance")

        # Export vs Import
        chart_data = data.melt(
            id_vars="country",
            value_vars=["ekspor", "impor"],
            var_name="Trade Type",
            value_name="Trade Value"
        )

        chart_data["Trade Type"] = chart_data["Trade Type"].map({
            "ekspor": "Export",
            "impor": "Import"
        })

        fig1 = px.bar(
            chart_data,
            x="country",
            y="Trade Value",
            color="Trade Type",
            barmode="group",
            color_discrete_map={
                "Export": "#D979A3",
                "Import": "#9B83BD"
            },
            labels={
                "country": "Country",
                "Trade Value": "Trade Value"
            },
            title="Export vs Import by Country"
        )

        fig1.update_layout(
            height=550,
            xaxis_tickangle=-60,
            legend_title="Trade Category"
        )

        st.plotly_chart(fig1, use_container_width=True)

        # Export and Import Contribution
        st.subheader("Global Export and Import Distribution")

        p1, p2 = st.columns(2)

        with p1:
            export_pie = px.pie(
                data,
                values="ekspor",
                names="country",
                hole=0.45,
                title="Export Share by Country"
            )
            export_pie.update_layout(height=450)
            st.plotly_chart(export_pie, use_container_width=True)

        with p2:
            import_pie = px.pie(
                data,
                values="impor",
                names="country",
                hole=0.45,
                title="Import Share by Country"
            )
            import_pie.update_layout(height=450)
            st.plotly_chart(import_pie, use_container_width=True)

        # Scatter relationship
        st.subheader("Export-Import Relationship")

        fig_scatter = px.scatter(
            data,
            x="ekspor",
            y="impor",
            size="total_trade",
            color="trade_status",
            hover_name="country",
            color_discrete_map={
                "Surplus": "#D979A3",
                "Deficit": "#9B83BD",
                "Balanced": "#E8B96A"
            },
            title="Relationship Between Exports and Imports",
            labels={
                "ekspor": "Export Value",
                "impor": "Import Value",
                "trade_status": "Trade Status"
            }
        )

        st.plotly_chart(
            fig_scatter,
            use_container_width=True
        )

        st.info(
            "Each point represents one country. "
            "Countries above the diagonal relationship "
            "have relatively higher imports than exports."
        )

    # ==========================================
    # TAB 2 - COUNTRY RANKINGS
    # ==========================================

    with tab2:

        st.header("🏆 International Trade Rankings")

        rank1, rank2 = st.columns(2)

        with rank1:

            st.subheader("Top 10 Exporting Countries")

            top_export = data.nlargest(10, "ekspor").sort_values("ekspor")

            fig2 = px.bar(
                top_export,
                x="ekspor",
                y="country",
                orientation="h",
                color="ekspor",
                color_continuous_scale=["#F8DCE9", "#D979A3"],
                labels={
                    "ekspor": "Export Value",
                    "country": "Country"
                }
            )

            fig2.update_layout(height=500)
            st.plotly_chart(fig2, use_container_width=True)

        with rank2:

            st.subheader("Top 10 Importing Countries")

            top_import = data.nlargest(10, "impor").sort_values("impor")

            fig3 = px.bar(
                top_import,
                x="impor",
                y="country",
                orientation="h",
                color="impor",
                color_continuous_scale=["#E6DDF5", "#8E79B8"],
                labels={
                    "impor": "Import Value",
                    "country": "Country"
                }
            )

            fig3.update_layout(height=500)
            st.plotly_chart(fig3, use_container_width=True)

        st.divider()

        st.subheader("Top 10 Countries by Total Trade")

        top_trade = data.nlargest(10, "total_trade").sort_values(
            "total_trade"
        )

        fig4 = px.bar(
            top_trade,
            x="total_trade",
            y="country",
            orientation="h",
            color="total_trade",
            color_continuous_scale=["#F6DCE9", "#B47BA5"],
            labels={
                "total_trade": "Total Trade Value",
                "country": "Country"
            }
        )

        fig4.update_layout(height=500)
        st.plotly_chart(fig4, use_container_width=True)

    # ==========================================
    # TAB 3 - TRADE BALANCE
    # ==========================================

    with tab3:

        st.header("⚖️ Trade Balance Analysis")

        st.write(
            "Trade balance measures the difference between "
            "a country's exports and imports."
        )

        surplus = data[data["trade_balance"] > 0]
        deficit = data[data["trade_balance"] < 0]
        balanced = data[data["trade_balance"] == 0]

        a, b, c = st.columns(3)

        a.metric("Surplus Countries", len(surplus))
        b.metric("Deficit Countries", len(deficit))
        c.metric("Balanced Countries", len(balanced))

        # Status distribution
        status_data = (
            data["trade_status"]
            .value_counts()
            .rename_axis("Trade Status")
            .reset_index(name="Number of Countries")
        )

        fig5 = px.pie(
            status_data,
            names="Trade Status",
            values="Number of Countries",
            hole=0.5,
            color="Trade Status",
            color_discrete_map={
                "Surplus": "#D979A3",
                "Deficit": "#9B83BD",
                "Balanced": "#E8B96A"
            },
            title="Distribution of Trade Status"
        )

        st.plotly_chart(fig5, use_container_width=True)

        # Surplus and deficit chart
        st.subheader("Trade Balance by Country")

        balance_sorted = data.sort_values("trade_balance")

        fig6 = px.bar(
            balance_sorted,
            x="trade_balance",
            y="country",
            orientation="h",
            color="trade_status",
            color_discrete_map={
                "Surplus": "#D979A3",
                "Deficit": "#9B83BD",
                "Balanced": "#E8B96A"
            },
            labels={
                "trade_balance": "Trade Balance",
                "country": "Country",
                "trade_status": "Trade Status"
            }
        )

        fig6.update_layout(height=700)

        st.plotly_chart(fig6, use_container_width=True)

        # Biggest surplus and deficit
        s1, s2 = st.columns(2)

        with s1:

            st.subheader("Top 10 Largest Surpluses")

            top_surplus = data.nlargest(10, "trade_balance")

            st.dataframe(
                top_surplus[
                    ["country", "ekspor", "impor", "trade_balance"]
                ].rename(columns={
                    "country": "Country",
                    "ekspor": "Export",
                    "impor": "Import",
                    "trade_balance": "Surplus"
                }),
                use_container_width=True,
                hide_index=True
            )

        with s2:

            st.subheader("Top 10 Largest Deficits")

            top_deficit = data.nsmallest(10, "trade_balance")

            st.dataframe(
                top_deficit[
                    ["country", "ekspor", "impor", "trade_balance"]
                ].rename(columns={
                    "country": "Country",
                    "ekspor": "Export",
                    "impor": "Import",
                    "trade_balance": "Deficit"
                }),
                use_container_width=True,
                hide_index=True
            )

    # ==========================================
    # TAB 4 - COUNTRY ANALYSIS
    # ==========================================

    with tab4:

        st.header("🔍 Individual Country Analysis")

        country_choice = st.selectbox(
            "Choose a country for detailed analysis",
            sorted(data["country"].unique()),
            key="country_detail"
        )

        country = data[data["country"] == country_choice].iloc[0]

        st.subheader(f"Trade Profile: {country_choice}")

        q1, q2, q3, q4 = st.columns(4)

        q1.metric("Export", f"{country['ekspor']:,.2f}")
        q2.metric("Import", f"{country['impor']:,.2f}")
        q3.metric("Trade Balance", f"{country['trade_balance']:,.2f}")

        q4.metric(
            "Coverage Ratio",
            "N/A" if pd.isna(country["coverage_ratio"])
            else f"{country['coverage_ratio']:.2f}%"
        )

        # Individual comparison
        country_chart = pd.DataFrame({
            "Category": ["Export", "Import"],
            "Value": [country["ekspor"], country["impor"]]
        })

        fig7 = px.bar(
            country_chart,
            x="Category",
            y="Value",
            color="Category",
            color_discrete_map={
                "Export": "#D979A3",
                "Import": "#9B83BD"
            },
            title=f"Export and Import of {country_choice}"
        )

        st.plotly_chart(fig7, use_container_width=True)

        # Interpretation
        st.subheader("Trade Performance Interpretation")

        if country["trade_balance"] > 0:

            st.success(
                f"{country_choice} records a trade surplus. "
                f"Exports exceed imports by "
                f"{country['trade_balance']:,.2f}."
            )

        elif country["trade_balance"] < 0:

            st.warning(
                f"{country_choice} records a trade deficit. "
                f"Imports exceed exports by "
                f"{abs(country['trade_balance']):,.2f}."
            )

        else:

            st.info(
                f"{country_choice} has a balanced trade position."
            )

        if pd.notna(country["coverage_ratio"]):

            if country["coverage_ratio"] > 100:
                st.write(
                    "Export coverage exceeds 100%, indicating "
                    "that export value is greater than import value."
                )

            elif country["coverage_ratio"] < 100:
                st.write(
                    "Export coverage is below 100%, indicating "
                    "that import value is greater than export value."
                )

            else:
                st.write(
                    "Export and import values are equal."
                )

        # Country share
        st.subheader("Contribution to Selected Countries")

        r1, r2 = st.columns(2)

        r1.metric(
            "Export Share",
            f"{country['export_share']:.2f}%"
        )

        r2.metric(
            "Import Share",
            f"{country['import_share']:.2f}%"
        )

    # ==========================================
    # TAB 5 - DATA INSIGHTS
    # ==========================================

    with tab5:

        st.header("📋 Trade Data Insights")

        # Overall coverage ratio
        overall_coverage = (
            export_sum / import_sum * 100
            if import_sum != 0 else float("nan")
        )

        st.subheader("Key Indicators")

        indicator_data = pd.DataFrame({
            "Indicator": [
                "Total Exports",
                "Total Imports",
                "Total Trade",
                "Trade Balance",
                "Export-Import Coverage Ratio",
                "Number of Countries",
                "Surplus Countries",
                "Deficit Countries"
            ],
            "Value": [
                export_sum,
                import_sum,
                trade_sum,
                balance_sum,
                overall_coverage,
                len(data),
                len(surplus),
                len(deficit)
            ]
        })

        st.dataframe(
            indicator_data,
            use_container_width=True,
            hide_index=True
        )

        st.divider()

        st.subheader("Automatic Trade Insights")

        highest_export = data.loc[data["ekspor"].idxmax()]
        highest_import = data.loc[data["impor"].idxmax()]
        highest_surplus = data.loc[data["trade_balance"].idxmax()]
        highest_deficit = data.loc[data["trade_balance"].idxmin()]

        st.markdown(
            f"""
            **1. Leading Exporter**

            {highest_export['country']} records the highest
            export value of {highest_export['ekspor']:,.2f}.

            **2. Leading Importer**

            {highest_import['country']} records the highest
            import value of {highest_import['impor']:,.2f}.

            **3. Largest Trade Surplus**

            {highest_surplus['country']} records the largest
            trade surplus of {highest_surplus['trade_balance']:,.2f}.

            **4. Largest Trade Deficit**

            {highest_deficit['country']} records the largest
            trade deficit of {abs(highest_deficit['trade_balance']):,.2f}.

            **5. Overall Trade Position**

            The selected countries have an aggregate trade
            {"surplus" if balance_sum >= 0 else "deficit"} of
            {abs(balance_sum):,.2f}.
            """
        )

        st.info(
            "These insights describe the recorded export and import "
            "values. They do not establish the causes of trade "
            "performance or economic growth."
        )

    # ==========================================
    # DOWNLOAD REPORT DATA
    # ==========================================

    st.divider()

    st.header("📥 Download Trade Analysis Data")

    export_data = data.copy()

    export_data = export_data.rename(columns={
        "country": "Country",
        "ekspor": "Export",
        "impor": "Import",
        "trade_balance": "Trade Balance",
        "trade_status": "Trade Status",
        "total_trade": "Total Trade",
        "export_share": "Export Share (%)",
        "import_share": "Import Share (%)",
        "coverage_ratio": "Coverage Ratio (%)"
    })

    csv = export_data.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="⬇️ Download Complete Trade Analysis",
        data=csv,
        file_name="ourspace_trade_analysis.csv",
        mime="text/csv"
    )

    st.caption(
        "OURSPACE | International Trade Intelligence Dashboard"
    )

except FileNotFoundError:

    st.error(
        "Excel file not found. Place "
        "ekspor_impor_2025_sederhana.xlsx "
        "in the same folder as page3.py."
    )

except Exception as e:

    st.error(f"Unable to load trade dashboard: {e}")
