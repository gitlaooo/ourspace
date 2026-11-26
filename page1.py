
import streamlit as st
from pathlib import Path

# ==========================================
# OURSPACE - PROFILE
# ==========================================

BASE_DIR = Path(__file__).parent

# ==========================================
# CUSTOM CSS
# ==========================================

st.markdown("""
<style>
    .hero {
        background: linear-gradient(120deg, #E8A1BE, #B96591);
        padding: 55px 25px;
        border-radius: 18px;
        text-align: center;
        color: white;
        margin-bottom: 35px;
    }

    .hero h1 {
        color: white;
        font-size: 48px;
        font-weight: 800;
        letter-spacing: 3px;
        margin-bottom: 10px;
    }

    .hero h3 {
        color: white;
        font-size: 25px;
        font-weight: 500;
    }

    .hero p {
        color: white;
        font-size: 16px;
    }

    .section-title {
        color: #B96591;
        font-size: 27px;
        font-weight: 700;
        margin-top: 28px;
        margin-bottom: 15px;
    }

    .info-card {
        background: #FFF0F6;
        padding: 23px;
        border-radius: 14px;
        border-left: 5px solid #D979A3;
        min-height: 150px;
        margin-bottom: 15px;
    }

    .info-card h4 {
        color: #A84F7C;
        margin-bottom: 10px;
    }

    .info-card p {
        color: #554653;
        line-height: 1.7;
    }

    .member-role {
        color: #B96591;
        font-weight: 600;
        font-size: 14px;
    }

    .member-nim {
        color: #88818A;
        font-size: 13px;
    }

    .quote-box {
        background: linear-gradient(120deg, #F7DCE9, #FCECF3);
        padding: 30px;
        border-radius: 15px;
        text-align: center;
        margin-top: 25px;
    }

    .quote-box h3 {
        color: #A84F7C;
        font-style: italic;
        font-weight: 500;
        line-height: 1.6;
    }

    .quote-box p {
        color: #796477;
        font-size: 13px;
    }
</style>
""", unsafe_allow_html=True)


# ==========================================
# HERO SECTION
# ==========================================

st.markdown("""
<div class="hero">
    <h1>OURSPACE</h1>
    <h3>International Trade Dashboard</h3>
    <p>Understanding Global Trade Through Data</p>
</div>
""", unsafe_allow_html=True)


# ==========================================
# ABOUT OURSPACE
# ==========================================

st.markdown(
    '<div class="section-title">About OURSPACE</div>',
    unsafe_allow_html=True
)

st.write("""
OURSPACE is an interactive platform developed to explore
international trade patterns through export and import data
across 130 countries.

The platform provides an integrated view of global trade
through data presentation, visualization, and economic analysis.
It aims to make international trade information easier to
understand and interpret.
""")

st.divider()


# ==========================================
# VISION AND MISSION
# ==========================================

st.markdown(
    '<div class="section-title">Our Vision & Mission</div>',
    unsafe_allow_html=True
)

vision, mission = st.columns(2)

with vision:
    st.markdown("""
    <div class="info-card">
        <h4>Our Vision</h4>
        <p>
        To provide a clear and insightful understanding of
        global trade through data-driven exploration and analysis.
        </p>
    </div>
    """, unsafe_allow_html=True)

with mission:
    st.markdown("""
    <div class="info-card">
        <h4>Our Mission</h4>
        <p>
        To present reliable trade data, visualize international
        trade patterns, identify export-import performance,
        and develop meaningful economic insights.
        </p>
    </div>
    """, unsafe_allow_html=True)

st.divider()


# ==========================================
# PROJECT OBJECTIVES
# ==========================================

st.markdown(
    '<div class="section-title">What We Explore</div>',
    unsafe_allow_html=True
)

obj1, obj2, obj3 = st.columns(3)

with obj1:
    st.markdown("""
    <div class="info-card">
        <h4>01. Trade Data</h4>
        <p>
        Explore export and import information
        across 130 countries.
        </p>
    </div>
    """, unsafe_allow_html=True)

with obj2:
    st.markdown("""
    <div class="info-card">
        <h4>02. Visualization</h4>
        <p>
        Discover trade patterns and comparisons
        through interactive visualizations.
        </p>
    </div>
    """, unsafe_allow_html=True)

with obj3:
    st.markdown("""
    <div class="info-card">
        <h4>03. Trade Analysis</h4>
        <p>
        Examine trade balances, country performance,
        and economic insights.
        </p>
    </div>
    """, unsafe_allow_html=True)

st.divider()


# ==========================================
# MEET THE TEAM
# ==========================================

st.markdown(
    '<div class="section-title">Meet Our Team</div>',
    unsafe_allow_html=True
)

st.write(
    "Four members, different responsibilities, "
    "one shared objective."
)

members = [
    {
        "name": "Gita Laura Insani",
        "nim": "021002405019",
        "role": "Project Leader",
        "photo": "anggota1.jpeg",
        "description": "Project coordination and overall direction."
    },
    {
        "name": "Sarah Azizah Kamila",
        "nim": "021002405018",
        "role": "Data Visualization",
        "photo": "anggota2.jpeg",
        "description": "Developing interactive charts and visual insights."
    },
    {
        "name": "Asyifa Fitriani",
        "nim": "021002405027",
        "role": "Trade Data",
        "photo": "anggota3.jpeg",
        "description": "Managing, preparing, and organizing trade datasets."
    },
    {
        "name": "Desy Fauziah Susetyo",
        "nim": "021002405022",
        "role": "Trade Analysis",
        "photo": "anggota4.jpeg",
        "description": "Analyzing trade performance and economic findings."
    }
]

columns = st.columns(4)

for col, member in zip(columns, members):

    with col:

        photo_path = BASE_DIR / "image" / member["photo"]

        if photo_path.exists():
            st.image(
                str(photo_path),
                use_container_width=True
            )
        else:
            st.warning(
                f"Photo not found: {member['photo']}"
            )

        st.markdown(
            f"**{member['name']}**"
        )

        st.markdown(
            f'<div class="member-nim">{member["nim"]}</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            f'<div class="member-role">{member["role"]}</div>',
            unsafe_allow_html=True
        )

        st.caption(member["description"])


st.divider()


# ==========================================
# TEAM PRINCIPLE
# ==========================================

st.markdown("""
<div class="quote-box">
    <h3>
    "Behind every number, there is a story
    waiting to be understood."
    </h3>
    <p>OURSPACE — A data-driven perspective on global trade</p>
</div>
""", unsafe_allow_html=True)


# ==========================================
# FOOTER
# ==========================================

st.markdown(
    """
    <div style="text-align:center; padding:25px 0 10px 0;">
        <p style="color:#A58A9B; font-size:13px;">
        OURSPACE | International Trade Dashboard | 2025
        </p>
    </div>
    """,
    unsafe_allow_html=True
)
