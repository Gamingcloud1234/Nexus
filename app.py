import streamlit as st
import streamlit.components.v1 as components
from database import init_db, register_user, get_stats, get_users, generate_code, get_codes

st.set_page_config(page_title="NEXUS MC", page_icon="✦", layout="centered")
YOUTUBE_URL = "https://www.youtube.com/@mtfverse"
DISCORD_URL = "https://discord.gg/5P9CzwQp"

st.markdown("""
<style>
html,body,[data-testid="stAppViewContainer"]{background:#fff!important;color:#111827}
[data-testid="stHeader"]{background:#fff!important}
.block-container{max-width:900px;padding:2.4rem 1rem 4rem}
.hero{text-align:center;padding:12px 0 28px}
.logo{font-size:13px;font-weight:900;letter-spacing:5px}
h1{font-size:clamp(42px,8vw,70px)!important;letter-spacing:-3px;margin:8px 0!important}
.sub{color:#6b7280}
.card{border:1px solid #e5e7eb;border-radius:24px;padding:28px;background:#fff;box-shadow:0 12px 40px rgba(17,24,39,.07)}
.stat{border:1px solid #e5e7eb;border-radius:18px;padding:17px;text-align:center;background:#fafafa}
.stat b{display:block;font-size:27px}.stat span{font-size:11px;color:#6b7280;letter-spacing:1px}
.codebox{border:2px dashed #111827;border-radius:18px;padding:24px;text-align:center;background:#fafafa;margin:18px 0}
.code{font-size:30px;font-weight:900;letter-spacing:4px}
.stButton>button{border-radius:14px!important;min-height:48px;font-weight:800!important;border:1px solid #111827!important}
</style>
""", unsafe_allow_html=True)

init_db()

# The URL fragment is used only as a client-side return signal.
returned = st.query_params.get("returned") == "1"
if returned and not st.session_state.get("code_issued"):
    st.session_state.code_issued = generate_code()

st.markdown('<div class="hero"><div class="logo">NEXUS MC</div><h1>Access Portal</h1><div class="sub">Community access, made simple.</div></div>', unsafe_allow_html=True)

s=get_stats()
a,b,c=st.columns(3)
a.markdown(f'<div class="stat"><b>{s["users"]:,}</b><span>PLAYERS JOINED</span></div>',unsafe_allow_html=True)
b.markdown(f'<div class="stat"><b>{s["active_codes"]:,}</b><span>ACTIVE CODES</span></div>',unsafe_allow_html=True)
c.markdown('<div class="stat"><b>24/7</b><span>PORTAL</span></div>',unsafe_allow_html=True)

st.write("")
access,admin=st.tabs(["ACCESS","ADMIN"])

with access:
    st.markdown('<div class="card">',unsafe_allow_html=True)
    username=st.text_input("Minecraft username",placeholder="Enter your username",max_chars=32)

    if returned and st.session_state.get("code_issued"):
        code=st.session_state.code_issued
        st.success("You're back. Your access code is ready.")
        st.markdown(f'<div class="codebox"><div class="code">{code}</div></div>',unsafe_allow_html=True)
        st.code(code, language=None)
        st.markdown(f'<p style="text-align:center"><a href="{DISCORD_URL}" target="_blank">OPEN DISCORD</a></p>',unsafe_allow_html=True)
        if username.strip() and st.button("REGISTER PLAYER"):
            register_user(username.strip(),code)
            st.success("Player registered.")
    else:
        st.markdown("### Get your access code")
        st.write("Visit the NEXUS MC YouTube channel in a new browser tab. When you come back, your code will appear here.")
        # Normal top-level browser navigation is deliberately used.
        components.html(f"""
        <script>
        function openYT() {{
            const returnUrl = window.parent.location.origin + window.parent.location.pathname + '?returned=1';
            window.parent.location.href = "{YOUTUBE_URL}";
        }}
        </script>
        <button onclick="openYT()" style="width:100%;height:50px;border:1px solid #111827;border-radius:14px;background:#111827;color:white;font-weight:800;font-size:15px;cursor:pointer">
        GET ACCESS CODE
        </button>
        """, height=62)
        st.caption("Tip: Your browser will open YouTube normally instead of embedding it.")

    st.markdown("</div>",unsafe_allow_html=True)
    st.caption("The YouTube visit is not subscription verification. Never enter Minecraft or Microsoft passwords here.")

with admin:
    st.markdown('<div class="card">',unsafe_allow_html=True)
    pw=st.text_input("Admin password",type="password")
    if pw == st.secrets.get("ADMIN_PASSWORD","CHANGE-ME"):
        st.success("Admin access granted.")
        st.write(get_stats())
        if st.button("GENERATE NEW CODE"):
            st.success(generate_code())
        st.dataframe(get_codes(),use_container_width=True,hide_index=True)
        st.dataframe(get_users(),use_container_width=True,hide_index=True)
    elif pw:
        st.error("Incorrect password.")
    st.markdown("</div>",unsafe_allow_html=True)
