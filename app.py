
import streamlit as st

# ==========================================
# OURSPACE
# INTERNATIONAL TRADE DASHBOARD
# ==========================================

st.set_page_config(
    page_title="OURSPACE | International Trade Dashboard",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# PINK BLOSSOM THEME
# ==========================================

st.markdown("""
<style>

/* MAIN BACKGROUND */
.stApp {
    background: linear-gradient(
        135deg,
        #FFF9FC 0%,
        #FFF1F6 55%,
        #FCE8F1 100%
    );
    color: #393440;
}

/* SIDEBAR BACKGROUND */
[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #F8DDE9 0%,
        #FCEAF1 55%,
        #FFF6FA 100%
    );
    border-right: 2px solid #E9C1D3;
}

/* SIDEBAR PADDING */
[data-testid="stSidebar"] > div:first-child {
    padding-top: 20px;
}

/* NAVIGATION TEXT */
[data-testid="stSidebarNav"] span {
    color: #594957;
    font-size: 14px;
    font-weight: 500;
}

/* ACTIVE NAVIGATION */
[data-testid="stSidebarNav"] li div[aria-current="page"] {
    background-color: #E8CFE0;
    border-radius: 9px;
}

/* MAIN CONTENT */
.block-container {
    max-width: 1200px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* HEADINGS */
h1, h2, h3 {
    color: #393440;
}

/* BUTTON */
.stButton > button {
    background-color: #D979A3;
    color: white;
    border: none;
    border-radius: 9px;
}

.stButton > button:hover {
    background-color: #B96591;
    color: white;
}

/* METRIC CARDS */
[data-testid="stMetric"] {
    background-color: rgba(255,255,255,0.8);
    border: 1px solid #F0D6E2;
    border-radius: 12px;
    padding: 15px;
}

/* DATAFRAME */
[data-testid="stDataFrame"] {
    border: 1px solid #F0D5E2;
    border-radius: 10px;
}

/* FILE UPLOADER */
[data-testid="stFileUploader"] {
    background-color: #FFF8FB;
    border-radius: 12px;
}

/* DIVIDER */
hr {
    border-color: #EBD4DF;
}

/* INPUT */
.stSelectbox, .stMultiSelect, .stTextInput {
    border-radius: 10px;
}

/* HIDE DEFAULT FOOTER */
footer {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# SIDEBAR BRANDING
# ==========================================

st.sidebar.markdown(
    """
    <div style="text-align:center; padding: 5px 0 12px 0;">
        <span style="font-size:30px;">🌸</span>
        <h3 style="
            color:#A84F7C;
            margin:5px 0;
            font-size:22px;
        ">
            OURSPACE
        </h3>
        <p style="
            color:#766776;
            font-size:11px;
            margin:0;
        ">
            International Trade Dashboard
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

st.sidebar.divider()


# ==========================================
# THANK YOU MESSAGE
# ==========================================

# This section appears below the navigation menu.

# ==========================================
# PAGE NAVIGATION
# ==========================================

pages = [

    st.Page(
        "page1.py",
        title="OURSPACE Profile",
        icon="🌸",
        default=True
    ),

    st.Page(
        "page2.py",
        title="Trade Data",
        icon="📊"
    ),

    st.Page(
        "page3.py",
        title="Visualization",
        icon="📈"
    ),

    st.Page(
        "page4.py",
        title="Trade Analysis",
        icon="🌍"
    )

]

pg = st.navigation(pages)


# ==========================================
# SIDEBAR CLOSING MESSAGE
# ==========================================

st.sidebar.divider()

st.sidebar.markdown(
    "<div style='text-align:center; font-size:24px;'>🌸</div>",
    unsafe_allow_html=True
)

st.sidebar.markdown(
    "<div style='text-align:center; color:#A84F7C; font-weight:700;'>Thank You for Visiting!</div>",
    unsafe_allow_html=True
)

st.sidebar.caption(
    "We appreciate your time and interest in exploring OURSPACE."
)

st.sidebar.markdown(
    "<div style='text-align:center; color:#B96591; font-size:12px; font-style:italic;'>Every insight begins with curiosity.</div>",
    unsafe_allow_html=True
)


# ==========================================
# RUN APPLICATION
# ==========================================

pg.run()
