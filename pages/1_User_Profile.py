import streamlit as st
import sqlite3
import pandas as pd
from PIL import Image
import io
import base64

# 1. Page Config
st.set_page_config(page_title="User Profile", page_icon="👤", layout="wide")

# 2. Database Connection
conn = sqlite3.connect("database.db", check_same_thread=False)
cursor = conn.cursor()

# 3. Security Check
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Please login first from the Home page.")
    if st.button("Go to Login"):
        st.switch_page("main.py")
    st.stop()

current_user = st.session_state.username
# st.write("Current User:", current_user)
cursor.execute("SELECT username FROM users")
# st.write("Database Users:", cursor.fetchall())

# --- SIDEBAR LOGIC (Circular Photo & Logout) ---
with st.sidebar:
    cursor.execute("SELECT profile_pic FROM users WHERE username = ?", (current_user,))
    res = cursor.fetchone()
    
    st.markdown("""
        <style>
            .side-img {
                width: 120px; height: 120px;
                border-radius: 50%; object-fit: cover;
                border: 2px solid #00d4ff; margin-bottom: 10px;
                display: block; margin-left: auto; margin-right: auto;
            }
        </style>
    """, unsafe_allow_html=True)

    if res and res[0]:
        img_base64 = base64.b64encode(res[0]).decode()
        st.markdown(f'<img src="data:image/png;base64,{img_base64}" class="side-img">', unsafe_allow_html=True)
    else:
        st.image("https://www.w3schools.com/howto/img_avatar.png", width=120)
            
    # st.write(f"Logged in as: **{current_user}**")
    
    if st.button("Logout", type="primary", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.rerun() 

# --- MAIN CONTENT ---
st.title(f"👤 Welcome Back, {current_user}")
st.markdown("---")

# Layout: col1 (Profile Photo Management) | col2 (Account Details & Security)
col1, col2 = st.columns([1, 1.5])

with col1:
    st.subheader("🖼️ Profile Picture")
    
    # st.write("res =", res)
   # Current Photo Display
    if res and res[0]:
        image_bytes = io.BytesIO(res[0])
        img = Image.open(image_bytes)
        st.image(img, width=200, caption="Current Photo")
    else:
        st.info("No profile picture uploaded yet.")
        st.image(
            "https://www.w3schools.com/howto/img_avatar.png",
            width=150
        )


    # Upload Section
    st.markdown("---")
    st.write("### Update Photo")
    uploaded_file = st.file_uploader("Choose a new picture", type=['jpg', 'jpeg', 'png'])
    
    if uploaded_file is not None:
        img = Image.open(uploaded_file)
        st.image(img, width=150, caption="Preview of New Photo")
        
        if st.button("Save Profile Picture", use_container_width=True):
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format=img.format if img.format else "PNG")
            img_blob = img_byte_arr.getvalue()

            cursor.execute(
                "UPDATE users SET profile_pic = ? WHERE username = ?",
                (img_blob, current_user)
            )
            conn.commit()
            
             # Debug Check
            # cursor.execute(
            #     "SELECT length(profile_pic) FROM users WHERE username=?",
            #     (current_user,)
            # )

            st.success("✅ Profile picture updated successfully!")
            st.rerun()

with col2:
    # Account Information Section
    st.subheader("📋 Account Details")
    st.info(f"**Username:** {current_user}")
    
    # Fetching Role/Admin Status
    cursor.execute("SELECT is_admin FROM users WHERE username = ?", (current_user,))
    admin_res = cursor.fetchone()
    role = "⭐ Admin / Developer" if admin_res and admin_res[0] == 1 else "👤 Regular User"
    st.write(f"**Account Type:** {role}")
    
    st.markdown("---")
    
    # Password Management Section
    st.subheader("🔐 Security Settings")
    with st.expander("Change Your Password"):
        new_pass = st.text_input("Enter New Password", type="password")
        confirm_pass = st.text_input("Confirm New Password", type="password")
        
        if st.button("Update Password", use_container_width=True):
            if new_pass == confirm_pass and new_pass != "":
                cursor.execute("UPDATE users SET password = ? WHERE username = ?", (new_pass, current_user))
                conn.commit()
                st.success("✅ Password updated successfully!")
            elif new_pass == "":
                st.error("❌ Password cannot be empty.")
            else:
                st.error("❌ Passwords do not match.")

    # Activity Overview (Optional Visual Touch)
    st.markdown("---")
    st.subheader("📊 Activity Overview")
    st.write("You can manage your analytics and data from the Dashboard in the sidebar.")

conn.close()