
import streamlit as st

# =========================
# OURSPACE PROFILE DESIGN
# =========================

st.markdown("""
<style>
.main-header {
    background: linear-gradient(120deg, #E8A1BD, #B85C83);
    padding: 35px;
    border-radius: 18px;
    text-align: center;
    color: white;
}

.section-title {
    color: #B85C83;
}

.member-card {
    background-color: #FCEAF1;
    padding: 12px;
    border-radius: 15px;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)


# HEADER
st.markdown("""
<div class="main-header">
    <h1>🌸 OURSPACE 🌸</h1>
    <h2>International Trade Dashboard</h2>
    <p>Exploring Global Export & Import Performance</p>
</div>
""", unsafe_allow_html=True)

st.write("")


# WELCOME
st.header("💗 Welcome to OURSPACE")

st.write("""
Welcome to OURSPACE!

Kami merupakan kelompok yang mengembangkan aplikasi
analisis perdagangan internasional, khususnya mengenai
perkembangan ekspor dan impor antarnegara.

Melalui aplikasi ini, kami menyajikan informasi perdagangan
internasional melalui pengolahan data, visualisasi,
dan analisis yang informatif.
""")

st.divider()


# TEAM PROFILE
st.header("👩‍💻 Meet Our Team")

members = [
    {
        "name": "Gita Laura Insani",
        "nim": "021002405019",
        "role": "Project Leader",
        "photo": "Image/anggota1.jpeg"
    },
    {
        "name": "Sarah Azizah Kamila",
        "nim": "021002405018",
        "role": "Data Analyst",
        "photo": "Image/anggota2.jpeg"
    },
    {
        "name": "Asyifa Fitriani",
        "nim": "02100240527",
        "role": "Data Visualization",
        "photo": "Image/anggota3.jpeg"
    },
    {
        "name": "Desy Fauziah Susetyo",
        "nim": "021002405026",
        "role": "Research Analyst",
        "photo": "Image/anggota4.jpeg"
    }
]

cols = st.columns(4)

for col, member in zip(cols, members):
    with col:
        st.image(
            member["photo"],
            use_container_width=True
        )

        st.markdown(
            f"**{member['name']}**"
        )

        st.caption(member["nim"])
        st.caption(member["role"])


st.divider()


# ABOUT PROJECT
st.header("🌍 About Our Project")

st.write("""
OURSPACE merupakan aplikasi berbasis Streamlit yang
bertujuan untuk menyajikan informasi mengenai perdagangan
internasional melalui analisis nilai ekspor dan impor
antarnegara, visualisasi data, serta analisis neraca perdagangan.
""")


# OBJECTIVES
st.header("🎯 Our Objectives")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("📊 Data Exploration")
    st.write("Mengeksplorasi data perdagangan internasional.")

with col2:
    st.subheader("📈 Visualization")
    st.write("Membandingkan nilai ekspor dan impor antarnegara.")

with col3:
    st.subheader("🌍 Trade Analysis")
    st.write("Menganalisis perkembangan perdagangan global.")


st.divider()

st.markdown(
    "<center>🌸 OURSPACE | International Trade Dashboard 🌸</center>",
    unsafe_allow_html=True
)
