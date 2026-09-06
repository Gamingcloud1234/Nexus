import streamlit as st
from database import init_db, register_user, verify_access_code, get_stats, get_users, delete_user, generate_code, revoke_code, get_codes
import secrets

st.set_page_config(page_title="NEXUS MC", page_icon="⚡", layout="wide")

init_db()

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;700;800&display=swap');
html,body,[class*="css"]{font-family:'Orbitron',sans-serif}
.stApp{
 background:radial-gradient(circle at 50% 0%,#123d48 0%,#050b10 42%,#020509 100%);
 color:#e9ffff;
}
.block-container{max-width:1150px;padding-top:2rem}
.hero{
 padding:35px;border:1px solid #16414a;border-radius:18px;
 background:linear-gradient(135deg,rgba(0,255,255,.08),rgba(0,0,0,.35));
 box-shadow:0 0 45px rgba(0,255,255,.08);margin-bottom:25px
}
.title{font-size:44px;font-weight:800;letter-spacing:5px;color:#00ffff;text-shadow:0 0 22px #00ffff}
.sub{color:#7e9ba2;font-size:13px;line-height:1.8}
.card{
 padding:22px;border:1px solid #153841;border-radius:14px;
 background:rgba(4,15,20,.78);margin-bottom:16px
}
.stat{
 padding:20px;border:1px solid #163b43;border-radius:12px;
 background:rgba(0,255,255,.035)
}
.stat h2{color:#00ffff;margin:0}.stat p{color:#6d8a91;font-size:11px}
section[data-testid="stSidebar"]{background:#03090d;border-right:1px solid #12333b}
</style>
""", unsafe_allow_html=True)

YOUTUBE = "https://www.youtube.com/@mtfverse"
DISCORD = "https://discord.gg/5P9CzwQp"

if "admin" not in st.session_state:
    st.session_state.admin = False

with st.sidebar:
    st.markdown("## ⚡ NEXUS MC")
    page = st.radio("NAVIGATION", ["Access Portal", "Admin Panel"])
    st.divider()
    st.caption("Community access portal")
    st.caption("No Minecraft credentials are collected.")

def access_portal():
    st.markdown("""
    <div class="hero">
      <div class="title">NEXUS // MC</div>
      <div class="sub">COMMUNITY ACCESS NETWORK<br>Verify your community code and continue to the NEXUS Discord.</div>
    </div>
    """, unsafe_allow_html=True)

    stats = get_stats()
    c1,c2,c3 = st.columns(3)
    with c1:
        st.markdown(f'<div class="stat"><h2>{stats["users"]:,}</h2><p>TOTAL PLAYERS JOINED</p></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="stat"><h2>{stats["active_codes"]:,}</h2><p>ACTIVE ACCESS CODES</p></div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="stat"><h2>ONLINE</h2><p>SYSTEM STATUS</p></div>', unsafe_allow_html=True)

    st.markdown("### ACCESS VERIFICATION")
    username = st.text_input("MINECRAFT USERNAME", max_chars=16, placeholder="Enter username...")
    code = st.text_input("ACCESS CODE", type="password", placeholder="Enter access code...")

    if st.button("⚡ VERIFY ACCESS", use_container_width=True):
        username = username.strip()
        code = code.strip()
        if len(username) < 3:
            st.error("Enter a valid username.")
        elif not code:
            st.error("Enter your access code.")
        else:
            ok, msg = verify_access_code(code)
            if not ok:
                st.error(msg)
            else:
                if register_user(username, code):
                    st.success(f"ACCESS GRANTED — Welcome, {username}.")
                else:
                    st.info("This username is already registered.")
                st.link_button("💬 JOIN DISCORD SERVER", DISCORD, use_container_width=True)

    st.markdown("---")
    st.markdown("**DON'T HAVE AN ACCESS CODE?**")
    st.caption("Visit MTF Verse to find the current community access code.")
    st.link_button("▶ GET A NEW ACCESS CODE", YOUTUBE, use_container_width=True)

def admin_panel():
    st.markdown("""
    <div class="hero">
      <div class="title">ADMIN // CORE</div>
      <div class="sub">NEXUS COMMUNITY MANAGEMENT CONSOLE</div>
    </div>
    """, unsafe_allow_html=True)

    if not st.session_state.admin:
        password = st.text_input("ADMIN PASSWORD", type="password")
        if st.button("🔐 LOGIN", use_container_width=True):
            if password == st.secrets.get("ADMIN_PASSWORD", "CHANGE-ME"):
                st.session_state.admin = True
                st.rerun()
            else:
                st.error("Invalid admin password.")
        st.warning("Set ADMIN_PASSWORD in Streamlit Secrets before production use.")
        return

    if st.button("Logout"):
        st.session_state.admin = False
        st.rerun()

    stats = get_stats()
    a,b,c = st.columns(3)
    with a: st.metric("TOTAL USERS", stats["users"])
    with b: st.metric("ACTIVE CODES", stats["active_codes"])
    with c: st.metric("USED CODES", stats["used_codes"])

    st.markdown("### 🎟️ ACCESS CODE GENERATOR")
    n = st.number_input("Codes to generate", 1, 20, 1)
    if st.button("GENERATE CODES", use_container_width=True):
        codes = [generate_code() for _ in range(n)]
        st.success("Codes generated.")
        st.code("\n".join(codes))

    st.markdown("### 👥 USERS")
    users = get_users()
    if users:
        for user_id, username, used_code, joined_at in users:
            c1,c2,c3 = st.columns([2,2,3])
            c1.write(username)
            c2.write(used_code)
            c3.write(joined_at)
            if st.button("🗑️ Delete", key=f"del_{user_id}"):
                delete_user(user_id)
                st.rerun()
    else:
        st.info("No users registered yet.")

    st.markdown("### 🔑 ACCESS CODES")
    for cid, code, active, used, created in get_codes():
        c1,c2,c3,c4 = st.columns([3,1,1,3])
        c1.code(code)
        c2.write("ACTIVE" if active else "REVOKED")
        c3.write("USED" if used else "NEW")
        if active and not used and c4.button("Revoke", key=f"rev_{cid}"):
            revoke_code(cid)
            st.rerun()

if page == "Access Portal":
    access_portal()
else:
    admin_panel()
