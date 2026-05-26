import streamlit as st
import sqlite3
import pandas as pd
import base64

# 1. Page Config
st.set_page_config(page_title="User Profile", page_icon="👤", layout="wide")

# 2. Check if logged in
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Please login first from the Home page.")
    if st.button("Go to Login"):
        st.switch_page("main.py")
    st.stop()

# 3. Database Connection
conn = sqlite3.connect("database.db", check_same_thread=False)
cursor = conn.cursor()

# Current User helper
current_user = st.session_state.get("username", "User")

# --- SIDEBAR LOGIC (Refined for Circular Photo) ---
with st.sidebar:
    cursor.execute("SELECT profile_pic FROM users WHERE username = ?", (current_user,))
    res = cursor.fetchone()
    
    # Circular CSS
    st.markdown("""
        <style>
            .side-img {
                width: 120px; height: 120px;
                border-radius: 50%; object-fit: cover;
                border: 2px solid #00d4ff; margin-bottom: 10px;
            }
        </style>
    """, unsafe_allow_html=True)

    if res and res[0]:
        img_base64 = base64.b64encode(res[0]).decode()
        st.markdown(f'<img src="data:image/png;base64,{img_base64}" class="side-img">', unsafe_allow_html=True)
    else:
        st.image("https://www.w3schools.com/howto/img_avatar.png", width=120)
            
    st.write(f"Logged in as: **{current_user}**")
    
    if st.button("Logout", type="primary", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.rerun() 

# --- MAIN CONTENT ---
st.title(f"👤 Welcome, {current_user}!")
st.markdown("---")

# Profile UI Layout
col1, col2 = st.columns([1, 2])

with col1:
    # Display Actual Profile Pic or Placeholder
    if res and res[0]:
        st.image(res[0], caption="Current Profile Photo", width=200)
    else:
        st.image("https://www.w3schools.com/howto/img_avatar.png", width=200, caption="Default Avatar")

with col2:
    st.subheader("📋 Account Details")
    st.info(f"**Username:** {current_user}")
    
    # Fetching admin status for display
    cursor.execute("SELECT is_admin FROM users WHERE username = ?", (current_user,))
    admin_res = cursor.fetchone()
    role = "⭐ Admin / Developer" if admin_res and admin_res[0] == 1 else "👤 Regular User"
    st.write(f"**Account Type:** {role}")
    
    st.markdown("---")
    
    # Password Feature (Expander inside col2 for better structure)
    with st.expander("🔐 Change Password"):
        new_pass = st.text_input("New Password", type="password")
        confirm_pass = st.text_input("Confirm New Password", type="password")
        
        if st.button("Update Password", use_container_width=True):
            if new_pass == confirm_pass and new_pass != "":
                cursor.execute("UPDATE users SET password = ? WHERE username = ?", (new_pass, current_user))
                conn.commit()
                st.success("Password updated successfully!")
            elif new_pass == "":
                st.error("Password cannot be empty.")
            else:
                st.error("Passwords do not match.")

# Data summary for user (Optional refined touch)
st.markdown("### 📊 Activity Overview")
st.write("You can manage your dashboard and view your analytics from the Sidebar.")

conn.close()