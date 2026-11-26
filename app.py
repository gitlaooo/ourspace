
import streamlit as st


# ==================================
# OURSPACE PINK FLORAL BACKGROUND
# ==================================

st.markdown("""
<style>

/* BACKGROUND */
.stApp {
    background:
        radial-gradient(circle at 5% 10%,
        #FCE4EC, transparent 28%),
        radial-gradient(circle at 95% 90%,
        #F8DCE8, transparent 28%),
        #FFF9FC;
}

/* SIDEBAR */
[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #F8DCE8,
        #FFF0F5,
        #FCEAF1
    );
}

/* JUDUL */
h1, h2, h3 {
    color: #A64D76;
}

/* TOMBOL */
.stButton > button {
    background-color: #D979A3;
    color: white;
    border-radius: 12px;
    border: none;
}

/* DEKORASI BUNGA */
.stApp::before {
    content: "🌸  ✿  🌷  ❀";
    position: fixed;
    top: 90px;
    right: 25px;
    font-size: 25px;
    opacity: 0.45;
    pointer-events: none;
    z-index: 0;
}

.stApp::after {
    content: "🌼  🌸  ✿";
    position: fixed;
    bottom: 20px;
    left: 320px;
    font-size: 25px;
    opacity: 0.35;
    pointer-events: none;
    z-index: 0;
}

</style>
""", unsafe_allow_html=True)


st.set_page_config(
    page_title="OURSPACE | International Trade",
    page_icon="🌸",
    layout="wide"
)

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
pg.run()
