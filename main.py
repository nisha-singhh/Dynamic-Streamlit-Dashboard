import streamlit as st
import sqlite3
import os

# ================= DATABASE INITIALIZATION =================

def init_db():
    conn = sqlite3.connect("database.db", check_same_thread=False)
    cursor = conn.cursor()
    # Create table with is_admin column included from the start
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        username TEXT UNIQUE,
        password TEXT,
        is_admin INTEGER DEFAULT 0
    )
    """)
    
    # Check if we need to add the column for older databases
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN is_admin INTEGER DEFAULT 0")
    except sqlite3.OperationalError:
        pass # Column already exists
    
    # Set the admin (Professional touch: change 'nisha' to your username)
    cursor.execute("""
        UPDATE users 
        SET is_admin = 1 
        WHERE username = 'nisha' AND password = 'singh'
    """)    
    conn.commit()
    return conn, cursor


conn, cursor = init_db()

# ================= PAGE CONFIG =================
# Must stay at the top!
st.set_page_config(
    page_title="Login | Sales Analytics",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ================= HIDE STREAMLIT UI & CUSTOM CSS =================
st.markdown("""
<style>
    #MainMenu {visibility:hidden;}
    footer {visibility:hidden;}
    header {visibility:hidden;}
    [data-testid="stSidebar"] {display:none;}
    
    /* Smooth transitions for the login card */
    .login-card {
        transition: transform 0.3s ease;
    }
    .login-card:hover {
        transform: translateY(-5px);
    }
</style>
""", unsafe_allow_html=True)

# Load External CSS
try:
    with open("assets/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except Exception as e:
    st.info("Custom CSS file not found, using default styles.")

# ================= SESSION STATE =================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = None

# ================= FUNCTIONS =================
def signup():
    st.subheader("Create Account")
    new_user = st.text_input("Username", key="signup_user", placeholder="Choose a username")
    new_password = st.text_input("Password", type="password", key="signup_pass", placeholder="Choose a password")
    
    if st.button("Create Account", use_container_width=True):
        if new_user and new_password:
            try:
                # Use a tuple for the values to ensure SQL safety
                cursor.execute("INSERT INTO users (username, password, is_admin) VALUES (?, ?, ?)", 
                               (new_user, new_password, 0))
                
                # CRITICAL: Yahan commit hona bahut zaruri hai
                conn.commit() 
                
                st.success("✅ Account Created! You can now login.")
            except sqlite3.IntegrityError:
                st.error("❌ Username already exists. Try another one.")
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.warning("⚠️ Please fill all fields")

def login():
    st.subheader("Welcome Back")
    username = st.text_input("Username", key="login_user", placeholder="Enter username")
    password = st.text_input("Password", type="password", key="login_pass", placeholder="Enter password")
    
    if st.button("Login", use_container_width=True):
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        data = cursor.fetchone()
        
        if data:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success(f"Logged in as {username}")
            st.rerun()
        else:
            st.error("Invalid Username or Password")

# ================= MAIN UI LOGIC =================
if st.session_state.logged_in:
    st.switch_page("pages/dashboard.py")
else:
    st.markdown('<div class="hero-section">', unsafe_allow_html=True)
    left_col, right_col = st.columns([1.2, 1])

    with left_col:
        st.markdown(f"""
            <div class="left-side">
                <h1 class="main-title">Sales Analytics <br>Dashboard</h1>
                <p class="sub-title">Actionable insights for your business growth.</p>
            </div>
        """, unsafe_allow_html=True)

    with right_col:
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        st.markdown('<div class="logo-circle">⚡</div>', unsafe_allow_html=True)

        tab1, tab2 = st.tabs(["Login", "Signup"])
        with tab1:
            login()
        with tab2:
            signup()

        st.markdown("""
            <div class="google-btn">
                <img src="https://upload.wikimedia.org/wikipedia/commons/5/53/Google_%22G%22_Logo.svg" width="20">
                Continue with Google
            </div>
            <div class="footer-text">
                Secure • Enterprise Grade • Reliable
            </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True) 
    st.markdown('</div>', unsafe_allow_html=True)