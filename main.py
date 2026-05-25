# import streamlit as st
# import sqlite3
# import os

# st.write("Current Path:", os.getcwd())
# st.write("Style Exists:", os.path.exists("assets/style.css"))

# # ================= PAGE CONFIG =================
# st.set_page_config(
#     page_title="Login",
#     layout="wide",
#     initial_sidebar_state="collapsed"
# )

# # ================= LOAD CSS =================
# # Try-except block taaki agar file missing ho toh error na aaye
# try:
#     with open("assets/style.css") as f:
#         st.markdown({f.read}, unsafe_allow_html=True)
# except FileNotFoundError:
#     st.error("style.css file not found in assets folder!")

# # ================= HIDE STREAMLIT UI =================
# st.markdown("""
# <style>
# #MainMenu {visibility:hidden;}
# footer {visibility:hidden;}
# header {visibility:hidden;}
# [data-testid="stSidebar"] {display:none;}
# </style>
# """, unsafe_allow_html=True)

# # ================= DATABASE =================
# conn = sqlite3.connect("database.db", check_same_thread=False)
# cursor = conn.cursor()
# cursor.execute("CREATE TABLE IF NOT EXISTS users(username TEXT, password TEXT)")
# conn.commit()

# # ================= SESSION =================
# if "logged_in" not in st.session_state:
#     st.session_state.logged_in = False

# # ================= SIGNUP FUNCTION =================
# def signup():
#     st.markdown("<div class='form-title'>Create Account</div>", unsafe_allow_html=True)
#     new_user = st.text_input("Username", key="signup_user", placeholder="Enter username")
#     new_password = st.text_input("Password", type="password", key="signup_pass", placeholder="Enter password")
    
#     if st.button("Signup", use_container_width=True):
#         if new_user and new_password:
#             cursor.execute("INSERT INTO users VALUES (?, ?)", (new_user, new_password))
#             conn.commit()
#             st.success("Account Created Successfully!")
#         else:
#             st.warning("Please fill all fields")

# # ================= LOGIN FUNCTION =================
# def login():
#     st.markdown("<div class='form-title'>Login to your account</div>", unsafe_allow_html=True)
#     username = st.text_input("Username", key="login_user", placeholder="Enter your username")
#     password = st.text_input("Password", type="password", key="login_pass", placeholder="Enter your password")
    
#     if st.button("Login", use_container_width=True):
#         cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
#         data = cursor.fetchone()
#         if data:
#             st.session_state.logged_in = True
#             st.rerun() # Latest Streamlit version mein st.rerun() use hota hai
#         else:
#             st.error("Invalid Username or Password")

# # ================= MAIN LOGIC =================
# if st.session_state.logged_in:
#     # Dashboard check - make sure this file exists
#     try:
#         st.switch_page("pages/dashboard.py")
#     except:
#         st.write("Logged In! ")
#         if st.button("Logout"):
#             st.session_state.logged_in = False
#             st.rerun()
# else:
#     # ===== HERO SECTION (Fixed single-line HTML to avoid raw text error) =====
#     hero_html = (
#         '<div class="hero-section">'
#         '<div class="logo-circle">S</div>'
#         '<div class="main-title">Welcome Back</div>'
#         '<div class="sub-title">Sign in to continue to your dashboard</div>'
#         '</div>'
#     )
#     st.markdown(hero_html, unsafe_allow_html=True)

#     # ===== CENTER CARD =====
#     left, center, right = st.columns([1, 1.5, 1])

#     with center:
#         # Streamlit tabs automatically apply styles from style.css
#         tab1, tab2 = st.tabs(["Login", "Signup"])
        
#         with tab1:
#             login()
            
#         with tab2:
#             signup()


import streamlit as st
import sqlite3
import os

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="Login",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ================= LOAD CSS =================
try:
    with open("assets/style.css") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )
except Exception as e:
    st.error(f"CSS Error: {e}")

# ================= HIDE STREAMLIT UI =================
st.markdown("""
<style>
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}
[data-testid="stSidebar"] {display:none;}
</style>
""", unsafe_allow_html=True)

# ================= DATABASE =================
conn = sqlite3.connect("database.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    username TEXT UNIQUE,
    password TEXT
)
""")
conn.commit()

# ================= SESSION =================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ================= SIGNUP FUNCTION =================
def signup():
    st.subheader("Create Account")
    new_user = st.text_input("Username", key="signup_user", placeholder="Enter username")
    new_password = st.text_input("Password", type="password", key="signup_pass", placeholder="Enter password")
    
    if st.button("Signup", use_container_width=True):
        if new_user and new_password:
            cursor.execute("INSERT INTO users VALUES (?, ?)", (new_user, new_password))
            conn.commit()
            st.success("Account Created Successfully!")
        else:
            st.warning("Please fill all fields")

# ================= LOGIN FUNCTION =================
def login():
    st.subheader("Login to your account")
    username = st.text_input("Username", key="login_user", placeholder="Enter your username")
    password = st.text_input("Password", type="password", key="login_pass", placeholder="Enter your password")
    
    if st.button("Login", use_container_width=True):
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        data = cursor.fetchone()
        print(data)
        if data:
            st.session_state.logged_in = True
            print(st.session_state.logged_in)
            st.rerun()
        else:
            st.error("Invalid Username or Password")

# ================= MAIN LOGIC =================
if st.session_state.logged_in:
    try:
        st.switch_page("pages/dashboard.py")
    except Exception as e:
        st.error(f"Dashboard not found: {e}")

else:
    # This wrapper allows the CSS Flexbox to work
    st.markdown('<div class="hero-section">', unsafe_allow_html=True)

    # Use columns to separate the text (Left) and the Card (Right)
    left_col, right_col = st.columns([1.2, 1])

    with left_col:
        st.markdown("""
            <div class="left-side">
                <h1 class="main-title">Welcome Back</h1>
                <p class="sub-title">Sign in to continue to your dashboard</p>
            </div>
        """, unsafe_allow_html=True)

    with right_col:
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        st.markdown('<div class="logo-circle">⚡</div>', unsafe_allow_html=True)

        # Your original Tabs logic
        tab1, tab2 = st.tabs(["Login", "Signup"])
        with tab1:
            login()
        with tab2:
            signup()

        # Added your footer elements inside the card
        st.markdown("""
            <div class="google-btn">
                <img src="https://upload.wikimedia.org/wikipedia/commons/5/53/Google_%22G%22_Logo.svg" width="20">
                Login with Google
            </div>
            <div class="footer-text">
                Secure • Fast • Reliable <br>
                Your data is protected with enterprise-grade security.
            </div>
        """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True) # Close login-card

    st.markdown('</div>', unsafe_allow_html=True) # Close hero-section