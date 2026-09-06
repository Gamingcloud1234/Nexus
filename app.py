import streamlit as st
from database import init_db, register_user, get_stats, get_users

st.set_page_config(
    page_title="NEXUS MC",
    page_icon="✦",
    layout="centered"
)

ACCESS_CODE = "mtfverse"
DISCORD_URL = "https://discord.gg/5P9CzwQp"

init_db()

st.markdown("""
<style>
html, body, [data-testid="stAppViewContainer"] {
    background: #ffffff !important;
    color: #111827 !important;
}

[data-testid="stHeader"] {
    background: #ffffff !important;
}

.block-container {
    max-width: 850px;
    padding-top: 45px;
}

.hero {
    text-align: center;
    padding: 20px 0 35px;
}

.logo {
    font-size: 13px;
    font-weight: 900;
    letter-spacing: 5px;
}

.hero h1 {
    font-size: 65px !important;
    font-weight: 900 !important;
    letter-spacing: -4px;
    margin: 8px 0 !important;
}

.subtitle {
    color: #6b7280;
    font-size: 16px;
}

.card {
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 24px;
    padding: 30px;
    box-shadow: 0 12px 40px rgba(0,0,0,.06);
}

.stat {
    background: #fafafa;
    border: 1px solid #e5e7eb;
    border-radius: 18px;
    padding: 18px;
    text-align: center;
}

.stat b {
    display: block;
    font-size: 27px;
}

.stat span {
    color: #6b7280;
    font-size: 11px;
    letter-spacing: 1px;
}

.code-box {
    background: #fafafa;
    border: 2px dashed #111827;
    border-radius: 18px;
    padding: 22px;
    text-align: center;
    margin: 20px 0;
}

.code {
    font-size: 32px;
    font-weight: 900;
    letter-spacing: 4px;
}

.stButton > button {
    width: 100%;
    min-height: 48px;
    border-radius: 14px !important;
    border: 1px solid #111827 !important;
    font-weight: 800 !important;
}
</style>
""", unsafe_allow_html=True)


# ---------------- HEADER ----------------

st.markdown("""
<div class="hero">
    <div class="logo">NEXUS MC</div>
    <h1>Access Portal</h1>
    <div class="subtitle">
        Enter your username and NEXUS MC access code.
    </div>
</div>
""", unsafe_allow_html=True)


# ---------------- STATS ----------------

stats = get_stats()

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown(
        f'<div class="stat"><b>{stats["users"]:,}</b>'
        '<span>PLAYERS JOINED</span></div>',
        unsafe_allow_html=True
    )

with c2:
    st.markdown(
        '<div class="stat"><b>1</b>'
        '<span>ACCESS CODE</span></div>',
        unsafe_allow_html=True
    )

with c3:
    st.markdown(
        '<div class="stat"><b>24/7</b>'
        '<span>PORTAL</span></div>',
        unsafe_allow_html=True
    )


st.write("")


# ---------------- ACCESS ----------------

st.markdown('<div class="card">', unsafe_allow_html=True)

st.markdown("### Get Access")

username = st.text_input(
    "Minecraft Username",
    placeholder="Enter your username",
    max_chars=32
)

code = st.text_input(
    "Access Code",
    placeholder="Enter access code",
    type="password"
)

if st.button("ENTER NEXUS MC"):

    if not username.strip():
        st.warning("Please enter your username.")

    elif code.strip().lower() != ACCESS_CODE:
        st.error("Invalid access code.")

    else:
        register_user(username.strip(), ACCESS_CODE)

        st.success("Access granted!")

        st.markdown(
            f"""
            <div class="code-box">
                <div>ACCESS CODE</div>
                <div class="code">mtfverse</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.link_button(
            "JOIN NEXUS MC DISCORD",
            DISCORD_URL,
            use_container_width=True
        )

st.markdown("</div>", unsafe_allow_html=True)


# ---------------- ADMIN ----------------

st.write("")
st.markdown("### Admin")

admin_password = st.text_input(
    "Admin Password",
    type="password"
)

real_password = st.secrets.get(
    "ADMIN_PASSWORD",
    "CHANGE-ME"
)

if admin_password == real_password:

    st.success("Admin access granted.")

    stats = get_stats()

    a, b = st.columns(2)

    with a:
        st.metric("Total Players", stats["users"])

    with b:
        st.metric("Access Code", "mtfverse")

    st.markdown("### Players")

    users = get_users()

    if users:
        st.dataframe(
            users,
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No players registered yet.")

elif admin_password:
    st.error("Incorrect admin password.")
