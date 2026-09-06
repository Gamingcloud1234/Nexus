import streamlit as st
from database import (
    init_db, register_user, get_stats, get_users,
    generate_code, revoke_code, get_codes
)

st.set_page_config(
    page_title="NEXUS MC",
    page_icon="✦",
    layout="centered",
    initial_sidebar_state="collapsed",
)

YOUTUBE_URL = "https://www.youtube.com/@mtfverse"
DISCORD_URL = "https://discord.gg/5P9CzwQp"

st.markdown("""
<style>
:root { --ink:#111827; --muted:#6b7280; --line:#e5e7eb; --soft:#f8fafc; }
html, body, [data-testid="stAppViewContainer"] { background:#ffffff !important; color:var(--ink); }
[data-testid="stHeader"] { background:#ffffff !important; }
.block-container { max-width: 920px; padding-top: 2.5rem; padding-bottom: 4rem; }
.hero { text-align:center; padding: 18px 0 26px; }
.logo { font-size: 14px; font-weight:800; letter-spacing:4px; color:#111827; }
h1 { font-size: clamp(42px,7vw,72px) !important; letter-spacing:-3px; margin:8px 0 5px !important; }
.sub { color:var(--muted); font-size:16px; }
.card { border:1px solid var(--line); border-radius:24px; padding:28px; background:#fff; box-shadow:0 10px 35px rgba(17,24,39,.06); }
.stat { border:1px solid var(--line); border-radius:18px; padding:18px; background:var(--soft); text-align:center; }
.stat b { display:block; font-size:27px; color:#111827; }
.stat span { color:var(--muted); font-size:12px; text-transform:uppercase; letter-spacing:1px; }
.codebox { border:2px dashed #111827; border-radius:18px; padding:22px; text-align:center; background:#fafafa; margin:18px 0; }
.code { font-size:34px; font-weight:900; letter-spacing:5px; }
.note { color:var(--muted); font-size:13px; text-align:center; margin-top:12px; }
[data-testid="stTextInput"] input { border-radius:14px !important; border:1px solid #d1d5db !important; background:#fff !important; color:#111827 !important; }
.stButton > button { border-radius:14px !important; min-height:46px; font-weight:750 !important; border:1px solid #111827 !important; }
.primary-btn button { background:#111827 !important; color:#fff !important; }
.secondary-btn button { background:#fff !important; color:#111827 !important; }
a { color:#111827 !important; }
hr { border-color:#eeeeee !important; }
</style>
""", unsafe_allow_html=True)

init_db()

# Return flow: ?access=1 tells the app the visitor returned from YouTube.
returned = st.query_params.get("access") == "1"

st.markdown("""
<div class="hero">
  <div class="logo">NEXUS MC</div>
  <h1>Access Portal</h1>
  <div class="sub">A clean community access portal for NEXUS MC.</div>
</div>
""", unsafe_allow_html=True)

stats = get_stats()
c1,c2,c3 = st.columns(3)
with c1:
    st.markdown(f'<div class="stat"><b>{stats["users"]:,}</b><span>Players Joined</span></div>', unsafe_allow_html=True)
with c2:
    st.markdown(f'<div class="stat"><b>{stats["active_codes"]:,}</b><span>Active Codes</span></div>', unsafe_allow_html=True)
with c3:
    st.markdown(f'<div class="stat"><b>24/7</b><span>Portal</span></div>', unsafe_allow_html=True)

st.write("")

if "issued_code" not in st.session_state:
    st.session_state.issued_code = None

tab1, tab2 = st.tabs(["ACCESS", "ADMIN"])

with tab1:
    st.markdown('<div class="card">', unsafe_allow_html=True)

    username = st.text_input("Minecraft username", placeholder="Enter your username", max_chars=32)

    if returned:
        st.success("Welcome back. Your access code is ready.")
        code = st.session_state.issued_code
        if not code:
            # Generate a one-time portal code after the user returns.
            code = generate_code()
            st.session_state.issued_code = code

        st.markdown(f'<div class="codebox"><div class="code">{code}</div><div class="note">Save this code before continuing.</div></div>', unsafe_allow_html=True)
        st.code(code, language=None)
        if st.button("CONTINUE TO DISCORD", key="discord_return"):
            st.markdown(f'<meta http-equiv="refresh" content="0;url={DISCORD_URL}">', unsafe_allow_html=True)

        st.markdown(f'<div class="note"><a href="{DISCORD_URL}" target="_blank">Open Discord manually</a></div>', unsafe_allow_html=True)

    else:
        st.markdown("### Get your access code")
        st.write("Click below to visit the NEXUS MC YouTube channel. When you return to this page, a code will appear automatically.")
        if st.button("GET ACCESS CODE", key="get_code"):
            if not username.strip():
                st.warning("Enter your username first.")
            else:
                st.session_state.pending_username = username.strip()
                st.markdown(f'<meta http-equiv="refresh" content="0;url={YOUTUBE_URL}">', unsafe_allow_html=True)
                st.info("Opening YouTube… return to this page after visiting the channel.")

        st.markdown(f'<div class="note"><a href="{YOUTUBE_URL}" target="_blank">Open YouTube channel</a></div>', unsafe_allow_html=True)

    if st.session_state.issued_code and not returned:
        st.session_state.issued_code = None

    st.markdown("</div>", unsafe_allow_html=True)

    if returned and st.session_state.get("pending_username"):
        if st.button("REGISTER PLAYER", key="register"):
            register_user(st.session_state.pending_username, st.session_state.issued_code)
            st.success("Player registered successfully.")

    st.write("")
    st.caption("YouTube visit is not treated as proof of subscription. This portal does not request Minecraft or Microsoft passwords.")

with tab2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    password = st.text_input("Admin password", type="password", key="admin_pw")
    admin_password = st.secrets.get("ADMIN_PASSWORD", "CHANGE-ME")
    if password == admin_password:
        st.success("Admin access granted.")
        a = get_stats()
        x,y,z = st.columns(3)
        x.metric("Players", a["users"])
        y.metric("Generated codes", a["codes"])
        z.metric("Active codes", a["active_codes"])

        st.markdown("### Generate code")
        if st.button("GENERATE NEW CODE"):
            st.success(f"New code: {generate_code()}")

        st.markdown("### Active codes")
        st.dataframe(get_codes(), use_container_width=True, hide_index=True)

        st.markdown("### Players")
        st.dataframe(get_users(), use_container_width=True, hide_index=True)
    elif password:
        st.error("Incorrect admin password.")
    else:
        st.write("Admin tools are hidden until the correct password is entered.")
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown('<div class="note">NEXUS MC • Community Access Portal</div>', unsafe_allow_html=True)
