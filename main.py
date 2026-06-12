import streamlit as st
import sqlite3
import base64
from google_auth_oauthlib.flow import Flow
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests


# ================= DATABASE INITIALIZATION (SQLite) =================
conn = sqlite3.connect("database.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    first_name TEXT,
    last_name TEXT,
    profile_pic BLOB,
    is_admin INTEGER DEFAULT 0
)
""")
conn.commit()

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="Login | Sales Analytics",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ================= HIDE STREAMLIT UI =================
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    [data-testid="stSidebar"] {display: none;}
</style>
""", unsafe_allow_html=True)

# Load External CSS
try:
    with open("assets/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except Exception:
    st.info("Custom CSS file not found.")

# ================= SESSION STATE =================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = None

# ================= GOOGLE OAUTH CONFIG & CALLBACK =================
def get_google_flow():
    client_config = {
        "web": {
            "client_id": st.secrets["google_oauth"]["client_id"],
            "client_secret": st.secrets["google_oauth"]["client_secret"],
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "redirect_uris": [st.secrets["google_oauth"]["redirect_uri"]]
        }
    }
    return Flow.from_client_config(
        client_config,
        scopes=[
            "openid",
            "https://www.googleapis.com/auth/userinfo.profile",
            "https://www.googleapis.com/auth/userinfo.email"
        ],
        redirect_uri=st.secrets["google_oauth"]["redirect_uri"]
    )

def handle_google_callback():
    params = st.query_params
    if "code" in params:
        try:
            flow = get_google_flow()
            # PKCE disable karo
            flow.fetch_token(
                code=params["code"],
                include_client_id=True
            )
            
            id_info = id_token.verify_oauth2_token(
                flow.credentials.id_token,
                google_requests.Request(),
                st.secrets["google_oauth"]["client_id"]
            )
            
            email = id_info.get("email")
            first_name = id_info.get("given_name", "")
            username = email.split("@")[0]

            # Users Checking or Insertion in DB
            cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
            user = cursor.fetchone()
            if not user:
                cursor.execute(
                    "INSERT INTO users (username, email, password, first_name) VALUES (?, ?, ?, ?)",
                    (username, email, "google_auth", first_name)
                )
                conn.commit()

            # Session maintain
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.first_name = first_name
            
            # URL Parameters clear and reload
            st.query_params.clear()
            st.rerun()
        except Exception as e:
            st.error(f"❌ Google Login Failed: {e}")

# Page lifecycle ke start par check lagao
handle_google_callback()


# ================= BACKGROUND IMAGE =================
def set_bg(image_file):
    try:
        with open(image_file, "rb") as f:
            data = f.read()
        encoded = base64.b64encode(data).decode()
        st.markdown(f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """, unsafe_allow_html=True)
    except Exception:
        pass  # Agar image nahi mili toh CSS gradient use hoga

set_bg("assets/login_bg.png")

# ================= FUNCTIONS =================
def signup():
    st.markdown('<p class="form-subtitle">Apna naya account banayein</p>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        f_name = st.text_input("First Name", placeholder="Nisha", key="signup_fname")
    with col2:
        l_name = st.text_input("Last Name", placeholder="Singh", key="signup_lname")

    username = st.text_input("Username", placeholder="nisha123", key="signup_username")
    email = st.text_input("Email Address", placeholder="example@mail.com", key="signup_email")

    p_col1, p_col2 = st.columns(2)
    with p_col1:
        new_password = st.text_input("Password", type="password", placeholder="••••••••", key="signup_pass")
    with p_col2:
        confirm_password = st.text_input("Confirm Password", type="password", placeholder="••••••••", key="signup_confirm")

    if st.button("Create Account →", use_container_width=True, key="signup_btn"):
        if not (f_name and l_name and username and email and new_password and confirm_password):
            st.warning("⚠️ Please fill all fields")
        elif new_password != confirm_password:
            st.error("❌ Passwords do not match!")
        else:
            try:
                cursor.execute(
                    "INSERT INTO users (username, email, password, first_name, last_name) VALUES (?, ?, ?, ?, ?)",
                    (username, email, new_password, f_name, l_name)
                )
                conn.commit()
                st.success("✅ Account Created! Now please login.")
                st.balloons()
            except Exception as e:
                st.error(f"❌ Database Error: {e}")


def login():
    st.markdown('<p class="form-subtitle">Wapas aaiye! Sign in karein apne account mein</p>', unsafe_allow_html=True)

    email = st.text_input("Email Address", placeholder="example@mail.com", key="login_user")
    password = st.text_input("Password", type="password", placeholder="••••••••", key="login_pass")

    if st.button("Sign In →", use_container_width=True, key="login_btn"):
        if email and password:
            cursor.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
            user_info = cursor.fetchone()
            if user_info:
                st.session_state.logged_in = True
                st.session_state.username = user_info[1]
                st.session_state.email = user_info[2]
                st.session_state.first_name = user_info[4]
                st.success(f"✅ Welcome back, {user_info[4]}!")
                st.rerun()
            else:
                st.error("❌ Invalid Email or Password")
        else:
            st.warning("⚠️ Please fill all fields")

     # Google logo base64 encode karke load karo
    try:
        with open("assets/Logo.jpeg", "rb") as img_file:
            google_logo = base64.b64encode(img_file.read()).decode()
        logo_html = f'<img src="data:image/jpeg;base64,{google_logo}" width="18" style="border-radius:3px;">'
    except Exception:
        logo_html = ""
 
    def login():

    # ... (Tumhara normal sign in UI form) ...

        st.markdown('<div class="divider-row">or continue with</div>', unsafe_allow_html=True)
    
        if st.button("Continue with Google", use_container_width=True, key="google_btn"):
            import os
            os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"  # localhost ke liye
            flow = get_google_flow()
            auth_url, state = flow.authorization_url(
                prompt="select_account",
                access_type="offline"  # state parameter hatao
            )
            st.session_state.oauth_state = state
            st.markdown(f'<meta http-equiv="refresh" content="0;url={auth_url}">', unsafe_allow_html=True)
            st.stop()


# ================= MAIN UI LOGIC =================
if st.session_state.logged_in:
    st.switch_page("pages/dashboard.py")
else:
    st.markdown('<div class="hero-section">', unsafe_allow_html=True)
    left_col, right_col = st.columns([1.2, 1])

    with left_col:
        st.markdown("""
            <div class="left-side">
                <h1 class="main-title">Sales Analytics<br><span>Dashboard</span></h1>
                <p class="sub-title">
                    Apne business ke liye actionable insights.<br>
                    Track karo, grow karo, succeed karo.
                </p>
                <div class="feature-pills">
                    <span class="pill">⚡ Real-time Data</span>
                    <span class="pill">🔒 Enterprise Grade</span>
                    <span class="pill">📊 Smart Reports</span>
                    <span class="pill">🛡️ Secure</span>
                </div>
            </div>
        """, unsafe_allow_html=True)

    with right_col:
        st.markdown('<div class="login-card">', unsafe_allow_html=True)

        tab1, tab2 = st.tabs(["🔑 Login", "✨ Signup"])

        with tab1:
            login()

        with tab2:
            signup()

        st.markdown("""
            <div class="footer-text">
                SECURE &nbsp;•&nbsp; ENTERPRISE GRADE &nbsp;•&nbsp; RELIABLE
            </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)